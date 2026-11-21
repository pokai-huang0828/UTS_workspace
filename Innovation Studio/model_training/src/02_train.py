"""processed → runs/<本次>/ 的全部產出(切分、調參、測試集評估、對帳、時間外驗證、學習曲線、重要性、分段誤差、最終模型、圖)。
執行:python "Innovation Studio/model_training/src/02_train.py" [run 名稱,預設 run_2026-11-21_01]
測試集(依房東切出的兩成)只在最後評一次;調參、選模型、選設施名單都只用訓練集。
"""
import datetime
import json
import platform
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import joblib  # noqa: E402
import lightgbm  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import sklearn  # noqa: E402
import xgboost  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from lightgbm import LGBMRegressor  # noqa: E402
from sklearn.base import clone  # noqa: E402
from sklearn.compose import ColumnTransformer  # noqa: E402
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor  # noqa: E402
from sklearn.linear_model import Ridge  # noqa: E402
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, ParameterSampler  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # noqa: E402
from xgboost import XGBRegressor  # noqa: E402

RUN_NAME = sys.argv[1] if len(sys.argv) > 1 else 'run_2026-11-21_01'
RUN = C.RUNS / RUN_NAME
FIG = RUN / 'figures'
N_JOBS = 24
N_ITER = 25
SEED = C.SEED
plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

MODELS = ['Ridge', 'RandomForest', 'HistGradientBoosting', 'XGBoost', 'LightGBM']
LABEL = {'B0': 'B0 全體中位數', 'B1': 'B1 同區同臥室中位數', 'Ridge': 'Ridge 線性', 'RandomForest': '隨機森林',
         'HistGradientBoosting': 'HistGB 梯度提升', 'XGBoost': 'XGBoost', 'LightGBM': 'LightGBM'}
SPACE = {
    'Ridge': {'alpha': [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000]},   # 網格,全部試
    'RandomForest': {'n_estimators': [300, 500], 'max_depth': [None, 10, 15, 20, 30],
                     'min_samples_leaf': [1, 2, 4, 8], 'max_features': [0.2, 0.33, 0.5, 0.7, 1.0]},
    'HistGradientBoosting': {'learning_rate': [0.02, 0.03, 0.05, 0.08, 0.1], 'max_iter': [200, 400, 700, 1000],
                             'max_leaf_nodes': [15, 31, 63], 'min_samples_leaf': [10, 20, 40, 80],
                             'l2_regularization': [0.0, 0.1, 1.0, 3.0]},
    'XGBoost': {'n_estimators': [300, 600, 1000], 'learning_rate': [0.02, 0.03, 0.05, 0.1],
                'max_depth': [3, 4, 5, 6, 8], 'subsample': [0.6, 0.8, 1.0], 'colsample_bytree': [0.5, 0.7, 0.9, 1.0],
                'min_child_weight': [1, 3, 5, 10], 'reg_lambda': [0.5, 1.0, 3.0, 10.0]},
    'LightGBM': {'n_estimators': [300, 600, 1000], 'learning_rate': [0.02, 0.03, 0.05, 0.1],
                 'num_leaves': [15, 31, 63], 'min_child_samples': [10, 20, 40], 'subsample': [0.6, 0.8, 1.0],
                 'subsample_freq': [1], 'colsample_bytree': [0.5, 0.7, 0.9, 1.0], 'reg_lambda': [0.0, 1.0, 3.0, 10.0]},
}
SYD_B_HGB = dict(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20, l2_regularization=1.0)  # syd_b 第 198 行


class Tee:
    def __init__(self, path):
        self.f = open(path, 'w', encoding='utf-8')
        self.o = sys.stdout

    def write(self, s):
        self.o.write(s)
        self.f.write(s)
        self.f.flush()

    def flush(self):
        self.o.flush()
        self.f.flush()


def make_model(name, params, nfeat):
    if name == 'Ridge':   # 類別欄 one-hot、其餘標準化
        ct = ColumnTransformer([('oh', OneHotEncoder(handle_unknown='ignore'), [0, 1]),
                                ('sc', StandardScaler(), list(range(2, nfeat)))])
        return Pipeline([('prep', ct), ('m', Ridge(**params))])
    if name == 'RandomForest':
        return RandomForestRegressor(random_state=SEED, n_jobs=1, **params)
    if name in ('HistGradientBoosting', 'syd_b_HGB'):
        mask = np.zeros(nfeat, bool)
        mask[:2] = True   # 區、房型細類當類別(同 syd_b make_tree)
        return HistGradientBoostingRegressor(categorical_features=mask, random_state=SEED, **params)
    if name == 'XGBoost':   # 區、房型細類以整數代碼輸入(當順序數值)
        return XGBRegressor(random_state=SEED, n_jobs=1, tree_method='hist', **params)
    if name == 'LightGBM':  # 同上,整數代碼
        return LGBMRegressor(random_state=SEED, n_jobs=1, verbose=-1, **params)
    raise ValueError(name)


def fit_pred(model, Xa, ya, Xb):
    m = clone(model).fit(Xa, ya)
    return m.predict(Xb)


def cv_job(name, params, X, y, tr_i, va_i):
    p = fit_pred(make_model(name, params, X.shape[1]), X[tr_i], y[tr_i], X[va_i])
    return C.mae_aud(y[va_i], p)


def host_subset(tr, frac, seed):
    """依房東抽:房東隨機排序後依序加入,直到列數 ≥ frac × 訓練集列數。"""
    hosts = np.array(sorted(tr.host_id.unique()))
    rng = np.random.default_rng(seed)
    rng.shuffle(hosts)
    cum = np.cumsum(tr.host_id.value_counts().loc[hosts].values)
    k = min(int(np.searchsorted(cum, frac * len(tr))) + 1, len(hosts))
    return tr[tr.host_id.isin(set(hosts[:k]))].reset_index(drop=True)


def lc_job(name, params, tr, te, frac, rep):
    sub = host_subset(tr, frac, SEED + rep)
    spec = C.Spec(sub)
    Xa, _ = C.make_X(sub, spec)
    Xb, _ = C.make_X(te, spec)
    p = np.exp(fit_pred(make_model(name, params, Xa.shape[1]), Xa, sub.y.values, Xb))
    b1 = C.b1_predict(sub, te)[0]
    return {'訓練比例': frac, '重複': rep + 1, '抽樣種子': SEED + rep, '訓練間數': len(sub), '訓練房東數': sub.host_id.nunique(),
            '選中模型_MAE': round(float(np.mean(np.abs(p - te.price_num.values))), 2),
            'B1_MAE': round(float(np.mean(np.abs(b1 - te.price_num.values))), 2)}


def group_cv_oof(d, X, name, params):
    """syd_b 的 5 折協定:GroupKFold(5) 依房東、不洗牌;設施名單用全部 d 決定(同 syd_b run_cv)。"""
    folds = list(GroupKFold(5).split(X, groups=d.host_id))
    preds = Parallel(n_jobs=5)(delayed(fit_pred)(make_model(name, params, X.shape[1]), X[a], d.y.values[a], X[b])
                               for a, b in folds)
    oof = np.zeros(len(d))
    for (a, b), p in zip(folds, preds):
        oof[b] = np.exp(p)
    b0, b1 = np.zeros(len(d)), np.zeros(len(d))
    for a, b in folds:
        b0[b] = np.median(d.price_num.values[a])
        b1[b] = C.b1_predict(d.iloc[a], d.iloc[b])[0]
    return oof, b0, b1


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    sys.stdout = Tee(RUN / 'train_log.txt')
    T = {}
    t_all = time.time()
    print(f'開始 {datetime.datetime.now():%Y-%m-%d %H:%M:%S};run = {RUN_NAME};種子 {SEED}')

    # ---------- 1. 樣本 ----------
    d = C.load_processed('train_table_2026-09.csv')
    ext = C.load_processed('extremes_dropped_24.csv')
    assert len(d) + len(ext) == 6639, len(d) + len(ext)
    assert len(d) == 6615, len(d)
    print(f'[樣本] 篩選且有價 {len(d) + len(ext):,} 列;去掉每晚 > 2,000 的 {len(ext)} 列 → {len(d):,} 列(assert 通過)')

    # ---------- 4. 切分 ----------
    tr_i, te_i = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED).split(d, groups=d.host_id))
    tr, te = d.iloc[tr_i].reset_index(drop=True), d.iloc[te_i].reset_index(drop=True)
    inter = set(tr.host_id) & set(te.host_id)
    assert len(inter) == 0
    split = {'method': 'GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42),依 host_id 分組',
             'train': {'listings': len(tr), 'hosts': int(tr.host_id.nunique()),
                       'price_median_aud': float(np.median(tr.price_num))},
             'test': {'listings': len(te), 'hosts': int(te.host_id.nunique()),
                      'price_median_aud': float(np.median(te.price_num))},
             'host_overlap': len(inter), 'test_share_of_listings_pct': round(100 * len(te) / len(d), 1)}
    json.dump(split, open(RUN / 'split_summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'[切分] 訓練 {len(tr):,} 間 / {split["train"]["hosts"]:,} 位房東;測試 {len(te):,} 間 / '
          f'{split["test"]["hosts"]:,} 位房東;房東交集 {len(inter)}(assert 通過)')

    spec = C.Spec(tr)   # 設施名單、區、房型細類清單只看訓練集
    Xtr, names = C.make_X(tr, spec)
    Xte, _ = C.make_X(te, spec)
    ytr = tr.y.values
    nfeat = Xtr.shape[1]
    print(f'[特徵] {nfeat} 欄:{names[:10]} + 40 個設施旗標;設施名單(訓練集出現比例前 40):{spec.top_amen}')

    # ---------- 6. 調參(訓練集內 5 折 GroupKFold) ----------
    t = time.time()
    folds = list(GroupKFold(5).split(Xtr, groups=tr.host_id))
    cands = {m: (list(ParameterSampler(SPACE[m], n_iter=N_ITER, random_state=SEED)) if m != 'Ridge'
                 else [{'alpha': a} for a in SPACE['Ridge']['alpha']]) for m in MODELS}
    jobs = [(m, ci, p, fi) for m in MODELS for ci, p in enumerate(cands[m]) for fi in range(5)]
    res = Parallel(n_jobs=N_JOBS, verbose=0)(delayed(cv_job)(m, p, Xtr, ytr, folds[fi][0], folds[fi][1])
                                             for m, ci, p, fi in jobs)
    rows = {}
    for (m, ci, p, fi), v in zip(jobs, res):
        r = rows.setdefault((m, ci), {'model': m, 'config_id': ci, 'params': json.dumps(p, sort_keys=True)})
        r[f'fold{fi + 1}_MAE'] = round(v, 2)
    cv = pd.DataFrame(rows.values())
    fcols = [f'fold{i}_MAE' for i in range(1, 6)]
    cv['mean_MAE'] = cv[fcols].mean(axis=1).round(2)
    cv['std_MAE'] = cv[fcols].std(axis=1).round(2)
    cv['rank_in_model'] = cv.groupby('model').mean_MAE.rank(method='first').astype(int)
    cv = cv[['model', 'config_id', 'rank_in_model', 'mean_MAE', 'std_MAE'] + fcols + ['params']]
    cv.sort_values(['model', 'rank_in_model']).to_csv(RUN / 'cv_results.csv', index=False, encoding='utf-8-sig')
    best = {m: cv[(cv.model == m) & (cv.rank_in_model == 1)].iloc[0] for m in MODELS}
    best_params = {m: json.loads(best[m].params) for m in MODELS}
    sel = min(MODELS, key=lambda m: best[m].mean_MAE)
    T['tuning_sec'] = round(time.time() - t, 1)
    print(f'[調參] {len(jobs)} 次擬合,{T["tuning_sec"]} 秒')
    for m in MODELS:
        print(f'  {m:22s} CV MAE {best[m].mean_MAE:7.2f} ± {best[m].std_MAE:5.2f}  參數 {best_params[m]}')
    print(f'[選模型] 交叉驗證 MAE 最低:{sel}')

    # ---------- 5 + 7. 測試集只評一次 ----------
    t = time.time()
    yte = te.price_num.values
    preds = {'B0': np.full(len(te), np.median(tr.price_num)), 'B1': C.b1_predict(tr, te)[0]}
    fitted = {}
    for m in MODELS:
        fitted[m] = make_model(m, best_params[m], nfeat).fit(Xtr, ytr)
        preds[m] = np.exp(fitted[m].predict(Xte))
    test_metrics = {k: {**C.metrics(yte, v), 'selected': k == sel,
                        'cv_MAE_train5fold': (float(best[k].mean_MAE) if k in MODELS else None)}
                    for k, v in preds.items()}
    pd.DataFrame({'id': te.id, 'actual_aud': yte, **{f'pred_{k}': np.round(v, 2) for k, v in preds.items()}}) \
        .to_csv(RUN / 'predictions_test.csv', index=False, encoding='utf-8-sig')
    T['test_eval_sec'] = round(time.time() - t, 1)
    print('[測試集] (每個只評一次)')
    for k, v in test_metrics.items():
        print(f'  {k:22s} {v}')

    # ---------- 8. 對帳:syd_b 原設定 5 折 + 選中模型同協定 ----------
    t = time.time()
    spec_all = C.Spec(d)
    Xall, _ = C.make_X(d, spec_all)
    oof_hgb, b0o, b1o = group_cv_oof(d, Xall, 'syd_b_HGB', SYD_B_HGB)
    oof_sel, _, _ = group_cv_oof(d, Xall, sel, best_params[sel])
    recon = {'protocol': 'syd_b 原協定:6,615 間、GroupKFold(5) 依房東(不洗牌)、設施名單用全部 6,615 間決定',
             'B0': C.metrics(d.price_num, b0o), 'B1': C.metrics(d.price_num, b1o),
             'syd_b_HGB_fixed_params': C.metrics(d.price_num, oof_hgb), 'old_report_value_MAE': 93.4,
             f'selected_{sel}': C.metrics(d.price_num, oof_sel)}
    recon['syd_b_HGB_matches_93.4'] = recon['syd_b_HGB_fixed_params']['MAE_aud'] == 93.4
    pd.DataFrame({'id': d.id, 'actual_aud': d.price_num, 'oof_B0': b0o, 'oof_B1': np.round(b1o, 2),
                  'oof_syd_b_HGB': np.round(oof_hgb, 2), f'oof_{sel}': np.round(oof_sel, 2)}) \
        .to_csv(RUN / 'predictions_oof.csv', index=False, encoding='utf-8-sig')
    T['reconcile_sec'] = round(time.time() - t, 1)
    print('[對帳]', json.dumps(recon, ensure_ascii=False))

    # ---------- 9. 時間外驗證 ----------
    t = time.time()
    d6 = C.load_processed('timeout_train_2026-06.csv')
    tt = C.load_processed('timeout_test_2026-09_new.csv')
    assert len(d6) == 6747 and len(tt) == 821, (len(d6), len(tt))
    spec6 = C.Spec(d6)
    X6, _ = C.make_X(d6, spec6)
    Xt, _ = C.make_X(tt, spec6)
    tout = {'train': f'{C.PREV} 期篩選、有價、去極端後 {len(d6):,} 間', 'test': f'{C.MAIN} 期 6,615 間中 id 不在 6 月整期的 {len(tt)} 間',
            'B0': C.metrics(tt.price_num, np.full(len(tt), np.median(d6.price_num))),
            'B1': C.metrics(tt.price_num, C.b1_predict(d6, tt)[0]),
            f'selected_{sel}': C.metrics(tt.price_num, np.exp(make_model(sel, best_params[sel], nfeat).fit(X6, d6.y.values).predict(Xt))),
            'syd_b_HGB_fixed_params(對照)': C.metrics(tt.price_num, np.exp(make_model('syd_b_HGB', SYD_B_HGB, nfeat).fit(X6, d6.y.values).predict(Xt))),
            'old_report_values_MAE': {'B0': 122.0, 'B1': 103.2, 'M2': 94.1}}
    T['timeout_sec'] = round(time.time() - t, 1)
    print('[時間外]', json.dumps(tout, ensure_ascii=False))

    # ---------- 10. 學習曲線 ----------
    t = time.time()
    fr = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
    lc = pd.DataFrame(Parallel(n_jobs=N_JOBS)(delayed(lc_job)(sel, best_params[sel], tr, te, f, r)
                                              for f in fr for r in range(3)))
    lc.to_csv(RUN / 'learning_curve.csv', index=False, encoding='utf-8-sig')
    lcs = lc.groupby('訓練比例').agg(間數=('訓練間數', 'mean'), MAE=('選中模型_MAE', 'mean'), 最低=('選中模型_MAE', 'min'),
                                 最高=('選中模型_MAE', 'max'), B1=('B1_MAE', 'mean')).round(1)
    T['learning_curve_sec'] = round(time.time() - t, 1)
    print('[學習曲線]\n' + lcs.to_string())

    # ---------- 11. 排列重要性(測試集,澳元 MAE 增加量) ----------
    t = time.time()
    model = fitted[sel]
    base = float(np.mean(np.abs(preds[sel] - yte)))
    rng = np.random.default_rng(SEED)
    perms = [rng.permutation(len(te)) for _ in range(10)]
    targets = [('單欄', n, [i]) for i, n in enumerate(names)] + [('分組', g, ix) for g, ix in C.feature_groups(names).items()]

    def imp_job(cols):
        out = []
        for pm in perms:
            Xp = Xte.copy()
            Xp[:, cols] = Xte[pm][:, cols]
            out.append(float(np.mean(np.abs(np.exp(model.predict(Xp)) - yte))) - base)
        return out
    vals = Parallel(n_jobs=N_JOBS, backend='threading')(delayed(imp_job)(c) for _, _, c in targets)
    fi = pd.DataFrame([{'類型': k, '特徵': n, '欄數': len(c), 'MAE增加_平均': round(float(np.mean(v)), 2),
                        'MAE增加_標準差': round(float(np.std(v)), 2)} for (k, n, c), v in zip(targets, vals)])
    fi['排名'] = fi.groupby('類型').MAE增加_平均.rank(ascending=False, method='first').astype(int)
    fi = fi.sort_values(['類型', '排名'])
    fi.to_csv(RUN / 'feature_importance.csv', index=False, encoding='utf-8-sig')
    T['importance_sec'] = round(time.time() - t, 1)
    print(f'[重要性] 測試集基準 MAE {base:.2f};分組:\n' + fi[fi.類型 == '分組'].to_string(index=False))
    print('單欄前 10:\n' + fi[fi.類型 == '單欄'].head(10).to_string(index=False))

    # ---------- 12. 分段誤差 ----------
    p, b1 = preds[sel], preds['B1']
    tot = np.abs(p - yte).sum()
    top5 = list(tr.nb.value_counts().index[:5])
    qn = pd.qcut(te.price_num, 5, labels=False).values
    segs = [('臥室數', f'{b} 臥室', te.bed_n.values == b) for b in (1, 2)] + \
           [('實際價格五等分', f'第 {k + 1} 等份({yte[qn == k].min():.0f}–{yte[qn == k].max():.0f})', qn == k) for k in range(5)] + \
           [('區', '房源數前 5 多的區(依訓練集)', te.nb.isin(top5).values), ('區', '其他區', ~te.nb.isin(top5).values)]
    seg = pd.DataFrame([{'分組方式': g, '區段': lab, '間數': int(mk.sum()),
                         '實際價中位數': round(float(np.median(yte[mk])), 1),
                         '選中模型_MAE': round(float(np.mean(np.abs(p[mk] - yte[mk]))), 1),
                         '選中模型_MdAPE_pct': round(float(100 * np.median(np.abs(p[mk] - yte[mk]) / yte[mk])), 1),
                         '選中模型_20pct內_pct': round(float(100 * np.mean(np.abs(p[mk] - yte[mk]) / yte[mk] <= 0.2)), 1),
                         '平均偏差_預測減實際': round(float(np.mean(p[mk] - yte[mk])), 1),
                         '占總絕對誤差_pct': round(float(100 * np.abs(p[mk] - yte[mk]).sum() / tot), 1),
                         'B1_MAE': round(float(np.mean(np.abs(b1[mk] - yte[mk]))), 1)} for g, lab, mk in segs])
    seg.to_csv(RUN / 'error_by_segment.csv', index=False, encoding='utf-8-sig')
    top20_share = float(seg[seg.分組方式 == '實際價格五等分'].iloc[-1]['占總絕對誤差_pct'])
    print(f'[分段誤差] 前 5 大區 {top5};最貴兩成占總絕對誤差 {top20_share}%\n' + seg.to_string(index=False))

    # ---------- 13. 最終模型(全部 6,615 間) ----------
    t = time.time()
    final = make_model(sel, best_params[sel], nfeat).fit(Xall, d.y.values)
    joblib.dump({'model': final, 'model_name': sel, 'params': best_params[sel], 'spec': spec_all.to_dict(),
                 'feature_names': names}, RUN / 'model_final.joblib')
    ptc = d.property_type.value_counts()
    vers = {'python': platform.python_version(), 'scikit-learn': sklearn.__version__, 'xgboost': xgboost.__version__,
            'lightgbm': lightgbm.__version__, 'pandas': pd.__version__, 'numpy': np.__version__,
            'joblib': joblib.__version__, 'matplotlib': matplotlib.__version__}
    card = {'model_name': sel, 'params': best_params[sel], 'target': 'ln(每晚掛牌價,澳元);預測後取 exp 換回澳元',
            'trained_on': f'{C.MAIN} 期篩選、有價、每晚 ≤ 2,000 澳元的全部 {len(d):,} 間({d.host_id.nunique():,} 位房東)',
            'train_date': datetime.date.today().isoformat(), 'feature_order': names,
            'categorical_codes': {'區': spec_all.nb_levels, '房型細類': spec_all.pt_levels,
                                  'unknown': '區沒見過 → -1;房型細類沒見過或不足 30 間 → Other'},
            'top_amenities': spec_all.top_amen,
            'defaults_for_predict_one': {'nb_centroid_median_latlon': {k: [round(float(g.lat.median()), 5), round(float(g.lon.median()), 5)]
                                                                       for k, g in d.groupby('nb')},
                                         'property_type_most_common': ptc.index[0], 'min_nights_median': int(d.min_n.median())},
            'scope': '整套出租、臥室 1–2、可住 2–4 人、最少 1–7 晚;範圍外的房子不要用這個模型',
            'banned_features': C.FEATURES_BANNED,
            'test_metrics_note': '下面的測試集成績來自「只用 80% 訓練集」訓練的同一組參數;本檔模型用 100% 資料重訓,沒有另外可評的測試集',
            'test_metrics_80pct_version': test_metrics[sel], 'cv_MAE_train5fold': float(best[sel].mean_MAE),
            'package_versions': vers}
    json.dump(card, open(RUN / 'model_card.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    T['final_fit_sec'] = round(time.time() - t, 1)

    # ---------- 圖 ----------
    order = sorted(preds, key=lambda k: test_metrics[k]['MAE_aud'], reverse=True)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    cols = ['#9aa0a6' if k in ('B0', 'B1') else ('#e07b1a' if k == sel else '#1f5fa8') for k in order]
    ax.barh([LABEL[k] for k in order], [test_metrics[k]['MAE_aud'] for k in order], color=cols)
    for i, k in enumerate(order):
        ax.text(test_metrics[k]['MAE_aud'] + 1, i, f"{test_metrics[k]['MAE_aud']:.1f}" + ('(選中)' if k == sel else ''),
                va='center', fontsize=9)
    ax.set_xlabel('平均猜差(澳元/晚,越小越好)')
    ax.set_xlim(0, max(test_metrics[k]['MAE_aud'] for k in order) * 1.22)
    ax.set_title(f'測試集 {len(te):,} 間:各方法平均猜差\n(灰=不用模型的基準;橘=用交叉驗證選中的模型)', fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / 'fig1_test_mae_by_model.png', dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.errorbar(lcs.間數, lcs.MAE, yerr=[lcs.MAE - lcs.最低, lcs.最高 - lcs.MAE], marker='o', color='#e07b1a',
                capsize=4, label=f'{LABEL[sel]}(3 次抽樣平均,線段=最低到最高)')
    ax.plot(lcs.間數, lcs.B1, marker='s', color='#9aa0a6', label='B1 同區同臥室中位數')
    for x, y, f in zip(lcs.間數, lcs.MAE, lcs.index):
        ax.annotate(f'{int(f * 100)}%:{y:.1f}', (x, y), textcoords='offset points', xytext=(0, -16), ha='center', fontsize=8)
    ax.set_xlabel('拿來學的房子數(間)')
    ax.set_ylabel('測試集平均猜差(澳元/晚)')
    ax.set_title('資料越多會不會越準:學習曲線(同一組測試集)', fontsize=11)
    ax.legend(fontsize=9, loc='upper right')
    ax.set_ylim(min(lcs.最低.min(), lcs.B1.min()) - 8, max(lcs.最高.max(), lcs.B1.max()) + 12)
    fig.tight_layout()
    fig.savefig(FIG / 'fig2_learning_curve.png', dpi=200)
    plt.close(fig)

    g = fi[fi.類型 == '分組'].sort_values('MAE增加_平均')
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.barh(g.特徵, g.MAE增加_平均, xerr=g.MAE增加_標準差, color='#1f5fa8', capsize=3)
    for i, v in enumerate(g.MAE增加_平均):
        ax.text(v + 1, i + 0.25, f'+{v:.1f}', fontsize=9)
    ax.set_xlim(0, float((g.MAE增加_平均 + g.MAE增加_標準差).max()) * 1.18)
    ax.set_xlabel(f'把這組資料打亂後,平均猜差變大多少(澳元/晚;原本 {base:.1f})')
    ax.set_title('電腦最看重哪一類條件(測試集,打亂 10 次平均)', fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / 'fig3_group_importance.png', dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.scatter(yte, p, s=6, alpha=0.35, color='#1f5fa8', edgecolors='none')
    lo, hi = 60, 2100
    xx = np.array([lo, hi])
    ax.plot(xx, xx, color='#222222', lw=1, label='猜得剛好')
    ax.fill_between(xx, xx * 0.8, xx * 1.2, color='#e07b1a', alpha=0.15, label='差 20% 以內')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    tk = [100, 200, 300, 500, 1000, 2000]
    ax.set_xticks(tk)
    ax.set_xticklabels(tk)
    ax.set_yticks(tk)
    ax.set_yticklabels(tk)
    ax.minorticks_off()
    ax.set_xlabel('房東實際開價(澳元/晚,對數刻度)')
    ax.set_ylabel(f'{LABEL[sel]} 猜的價(澳元/晚)')
    ax.set_title(f'測試集 {len(te):,} 間:實際價 vs 猜的價', fontsize=11)
    ax.legend(fontsize=9, loc='upper left')
    fig.tight_layout()
    fig.savefig(FIG / 'fig4_actual_vs_pred.png', dpi=200)
    plt.close(fig)

    s5 = seg[seg.分組方式 == '實際價格五等分']
    xs = np.arange(len(s5))
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.bar(xs - 0.2, s5.選中模型_MAE, 0.4, color='#e07b1a', label=LABEL[sel])
    ax.bar(xs + 0.2, s5.B1_MAE, 0.4, color='#9aa0a6', label='B1 同區同臥室中位數')
    for x, v, sh in zip(xs, s5.選中模型_MAE, s5.占總絕對誤差_pct):
        ax.text(x - 0.2, v + 3, f'{v:.0f}\n占{sh:.0f}%', ha='center', fontsize=8)
    ax.set_xticks(xs)
    ax.set_xticklabels([lab.replace('(', '\n(') for lab in s5.區段], fontsize=8)
    ax.set_ylabel('平均猜差(澳元/晚)')
    ax.set_ylim(0, max(s5.選中模型_MAE.max(), s5.B1_MAE.max()) * 1.25)
    ax.set_title('各價格區段猜差多少(測試集依實際價分五等份;「占」= 占全部猜差的比例)', fontsize=10)
    ax.legend(fontsize=9, loc='upper left')
    fig.tight_layout()
    fig.savefig(FIG / 'fig5_error_by_price_band.png', dpi=200)
    plt.close(fig)

    # ---------- 寫 metrics / config ----------
    T['total_sec'] = round(time.time() - t_all, 1)
    metrics = {'selected_model': sel, 'selection_rule': '訓練集內 5 折 GroupKFold(依房東)的平均澳元 MAE 最低',
               'test_set': {'n': len(te), 'note': '每個方法只在測試集評一次', 'results': test_metrics},
               'reconcile_5fold_6615': recon, 'timeout_check': tout,
               'learning_curve_summary': lcs.reset_index().to_dict(orient='records'),
               'top20pct_price_share_of_abs_error_pct': top20_share}
    json.dump(metrics, open(RUN / 'metrics.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    config = {'run': RUN_NAME, 'seed': SEED, 'data': 'data/processed/train_table_2026-09.csv(6,615 列)',
              'target': 'ln(price)', 'split': split['method'], 'cv_for_tuning': 'GroupKFold(5),依 host_id,只在訓練集內',
              'n_iter_random_search': N_ITER, 'search_space': SPACE, 'n_configs_tried': {m: len(cands[m]) for m in MODELS},
              'best_params': best_params, 'best_cv_MAE': {m: float(best[m].mean_MAE) for m in MODELS},
              'selected_model': sel, 'syd_b_fixed_HGB_params': SYD_B_HGB,
              'categorical_handling': {'Ridge': 'one-hot', 'HistGradientBoosting': '原生類別', 'RandomForest/XGBoost/LightGBM': '整數代碼(當順序數值)'},
              'feature_names': names, 'package_versions': vers, 'n_jobs': N_JOBS, 'timing_sec': T,
              'finished_at': datetime.datetime.now().isoformat(timespec='seconds')}
    json.dump(config, open(RUN / 'config.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'[完成] 各段秒數 {T}')


if __name__ == '__main__':
    main()
