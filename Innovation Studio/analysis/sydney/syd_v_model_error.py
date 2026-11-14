"""雪梨價格模型誤差拆解(IS-1114-modelerror-01):M2 平均猜差 93.4 澳幣是從哪裡來的。可重跑:python -I syd_v_model_error.py
讀:scratchpad/insideairbnb_sydney/2026-09-16/data/listings.csv.gz(唯讀;透過 syd_b_positioning.load 讀,另外只多讀
    id + hosts_time_as_host_years/months 三欄算房東年資)。
寫:Innovation Studio/notes/raw/syd_v_model_error_2026-11-14.json、.md;
    每間房的樣本外預測值存 scratchpad/syd_v_model_error/(不進 repo)。
重現做法:直接 import syd_b_positioning 的 load / scope / prep / Spec / fit_predict / metrics / EXTREME_CAP / SEED;
    5 折切法照 syd_b_positioning.py 第 231-239 行 run_cv 的 group 分支(GroupKFold(5),group = host_id),
    只跑 B0、B1、M1、M2(run_cv 會連 _host 對照一起跑,這裡用不到;每個模型的 random_state 固定,少跑幾個不影響結果)。
    極端值放回去的算法照 syd_b_positioning.py 第 594-597 行。
    新手 / 老手照 syd_c_hosts_time.py 第 101 行:年資月數 = hosts_time_as_host_years * 12 + hosts_time_as_host_months,<= 12 為新手。
json / md 只放分組後的數字,不放房源編號、名稱、房東名。
"""
import json
import site
import sys
from pathlib import Path

sys.path.append(site.getusersitepackages())  # 同 syd_b:python -I 會略過使用者層 site-packages
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # 只為了 import 同資料夾的 syd_b_positioning

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.model_selection import GroupKFold  # noqa: E402

import syd_b_positioning as B  # noqa: E402

ROOT = B.ROOT
NOTES = ROOT / 'Innovation Studio/notes'
OUT_JSON = NOTES / 'raw/syd_v_model_error_2026-11-14.json'
OUT_MD = NOTES / 'raw/syd_v_model_error_2026-11-14.md'
SCR = ROOT / 'scratchpad/syd_v_model_error'
METHODS = ['B0', 'B1', 'M1', 'M2']
# 既有數字:notes/20_雪梨深度分析.md 第 134-149 行(來源 syd_b_positioning_2026-11-11.json)
PUBLISHED = {'B0': {'MAE_aud': 122.5, 'MdAPE_pct': 26.0, 'within20_pct': 40.1},
             'B1': {'MAE_aud': 101.7, 'MdAPE_pct': 21.2, 'within20_pct': 47.8},
             'M1': {'MAE_aud': 95.7, 'MdAPE_pct': 19.7, 'within20_pct': 50.5},
             'M2': {'MAE_aud': 93.4, 'MdAPE_pct': 18.9, 'within20_pct': 51.9}}
PUBLISHED_M2_WITH_EXT = 113.5
MIN_CELL = 20      # 第 3 項:同區 × 同臥室數 × 同可住人數,至少 20 間才算
TOP5 = 5


def r1(x):
    return round(float(x), 1)


def main():
    # ---------------- 讀檔(同 syd_b main() 第 457-462 行)----------------
    raw = B.load(B.MAIN)
    assert len(raw) == B.EXPECT['rows'], len(raw)
    sc = B.scope(raw)
    assert len(sc) == B.EXPECT['scope'], len(sc)
    d_all = B.prep(sc)
    assert len(d_all) == B.EXPECT['scope_price'], len(d_all)
    ten = pd.read_csv(B.DATA / B.MAIN / 'data/listings.csv.gz', dtype=str, keep_default_na=False,
                      usecols=['id', 'hosts_time_as_host_years', 'hosts_time_as_host_months']).set_index('id')
    assert ten.index.is_unique
    yrs = pd.to_numeric(d_all.id.map(ten.hosts_time_as_host_years), errors='coerce')
    mos = pd.to_numeric(d_all.id.map(ten.hosts_time_as_host_months), errors='coerce')
    d_all['t_host'] = yrs * 12 + mos
    d_all['hostcnt_missing'] = pd.to_numeric(d_all.calculated_host_listings_count, errors='coerce').isna()
    sizes = d_all.grp.value_counts()            # 同區同臥室數那一組的大小,照 syd_b a_grouping(用全部 6,639 間)
    d_all['grp_size'] = d_all.grp.map(sizes)
    nb_n = d_all.nb.value_counts()              # 前 5 區照 syd_b 第 514、578 行(用全部 6,639 間排)
    top5 = list(nb_n.index[:TOP5])

    d = d_all[d_all.price_num <= B.EXTREME_CAP].reset_index(drop=True)
    ext = d_all[d_all.price_num > B.EXTREME_CAP].reset_index(drop=True)
    assert len(d) == 6615 and len(ext) == 24, (len(d), len(ext))
    spec = B.Spec(d)
    y = d.price_num.values

    # ---------------- 1. 重現(依房東分組 5 折,樣本外預測)----------------
    oof = {m: np.zeros(len(d)) for m in METHODS}
    fold = np.zeros(len(d), int)
    for k, (tr_i, te_i) in enumerate(GroupKFold(5).split(d, groups=d.host_id)):
        tr, te = d.iloc[tr_i], d.iloc[te_i]
        for m in METHODS:
            oof[m][te_i] = B.fit_predict(m, tr, te, spec)
        fold[te_i] = k
    ext_pred = B.fit_predict('M2', d, ext, spec)
    y_all = np.concatenate([y, ext.price_num.values])
    with_ext = B.metrics(y_all, np.concatenate([oof['M2'], ext_pred]))
    repro = {}
    for m in METHODS:
        got = B.metrics(y, oof[m])
        repro[m] = {'rerun': got, 'published': PUBLISHED[m],
                    'diff': {k: r1(got[k] - PUBLISHED[m][k]) for k in PUBLISHED[m]}}
    repro['M2_with_24_extremes'] = {'rerun': with_ext, 'published_MAE_aud': PUBLISHED_M2_WITH_EXT,
                                    'diff_MAE': r1(with_ext['MAE_aud'] - PUBLISHED_M2_WITH_EXT)}
    ext_ae = np.abs(ext_pred - ext.price_num.values)

    SCR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({'id': d.id, 'fold': fold, 'actual': y, **{f'pred_{m}': oof[m] for m in METHODS}}) \
        .to_csv(SCR / 'oof_predictions_6615.csv', index=False)
    pd.DataFrame({'id': ext.id, 'actual': ext.price_num.values, 'pred_M2_trained_on_6615': ext_pred}) \
        .to_csv(SCR / 'extremes_24_predictions.csv', index=False)

    # ---------------- 共用:一組的數字 ----------------
    p2 = oof['M2']
    err = p2 - y
    ae = np.abs(err)
    ape = ae / y
    b1ae = np.abs(oof['B1'] - y)
    total_ae = float(ae.sum())

    def row(mask, label):
        m = np.asarray(mask, bool)
        return {'label': label, 'n': int(m.sum()),
                'price_min': r1(y[m].min()), 'price_max': r1(y[m].max()), 'price_median': r1(np.median(y[m])),
                'mean_actual': r1(y[m].mean()), 'mean_pred_M2': r1(p2[m].mean()),
                'M2_MAE': r1(ae[m].mean()), 'M2_MdAPE_pct': r1(100 * np.median(ape[m])),
                'M2_within20_pct': r1(100 * np.mean(ape[m] <= 0.2)),
                'M2_mean_signed': r1(err[m].mean()), 'B1_MAE': r1(b1ae[m].mean()),
                'B1_minus_M2_sum_abs_err': round(float(b1ae[m].sum() - ae[m].sum()), 1),
                'sum_abs_err': round(float(ae[m].sum()), 2),
                'share_of_total_abs_err_pct': r1(100 * ae[m].sum() / total_ae)}

    # ---------------- 2. 依實際開價分 5 等份 + 最貴一成 ----------------
    order = np.argsort(y, kind='stable')       # 同價的照原本順序;邊界同價的房子可能分到相鄰兩組
    qid = np.empty(len(y), int)
    for k, idx in enumerate(np.array_split(order, 5)):
        qid[idx] = k
    n10 = int(round(0.1 * len(y)))
    top10 = np.zeros(len(y), bool)
    top10[order[-n10:]] = True
    quint = [row(qid == k, f'第 {k + 1} 等份({["最便宜", "偏便宜", "中間", "偏貴", "最貴"][k]}兩成)') for k in range(5)]
    top10_row = row(top10, '最貴的一成')
    cuts = np.cumsum([len(s) for s in np.array_split(order, 5)])[:-1]
    tie_prices = [r1(y[order[c]]) for c in cuts if y[order[c - 1]] == y[order[c]]]
    boundary_ties = len(tie_prices)
    chk_n = sum(r['n'] for r in quint)
    chk_sum = sum(r['sum_abs_err'] for r in quint)
    assert chk_n == len(d) == 6615, chk_n
    assert abs(chk_sum - total_ae) < 0.05, (chk_sum, total_ae)
    assert abs(total_ae - ae.mean() * len(d)) < 1e-6
    sec2 = {'quintiles': quint, 'top10pct': top10_row,
            'share_top10_pct': top10_row['share_of_total_abs_err_pct'], 'share_top20_pct': quint[4]['share_of_total_abs_err_pct'],
            'MAE_bottom80': r1(ae[qid < 4].mean()), 'n_bottom80': int((qid < 4).sum()),
            'MAE_bottom90': r1(ae[~top10].mean()), 'n_bottom90': int((~top10).sum()),
            'pred_range_M2': {'p1': r1(np.percentile(p2, 1)), 'p50': r1(np.median(p2)), 'p99': r1(np.percentile(p2, 99)),
                              'max': r1(p2.max())},
            'actual_range': {'p1': r1(np.percentile(y, 1)), 'p50': r1(np.median(y)), 'p99': r1(np.percentile(y, 99)),
                             'max': r1(y.max())},
            'checks': {'n_sum': chk_n, 'sum_abs_err_quintiles': round(chk_sum, 2), 'total_abs_err': round(total_ae, 2),
                       'MAE_x_n': round(float(ae.mean() * len(d)), 2), 'boundary_ties_between_quintiles': boundary_ties,
                       'boundary_tie_prices': tie_prices},
            'split_rule': '照實際開價由低到高排序(同價照原順序),np.array_split 切 5 份;最貴一成 = 排最後 round(0.1×n) 間'}

    # ---------------- 3. 同類房子本來就差多少 ----------------
    d['cell'] = d.nb + '|' + d.bedrooms + '|' + d.acc.astype(str)
    g = d.groupby('cell').price_num
    cs = pd.DataFrame({'n': g.size(), 'p25': g.quantile(0.25), 'p50': g.median(), 'p75': g.quantile(0.75)})
    big = cs[cs.n >= MIN_CELL].copy()
    big['iqr'] = big.p75 - big.p25
    big['ratio'] = big.iqr / big.p50
    in_big = d.cell.isin(big.index).values
    cell_med = d.cell.map(cs.p50).values
    sec3 = {'cell_def': '同一區 × 同樣臥室數 × 同樣能住的人數(6,615 間模型樣本),至少 20 間的組',
            'n_cells_total': int(len(cs)), 'n_cells_ge20': int(len(big)), 'n_listings_in_cells_ge20': int(in_big.sum()),
            'iqr_aud_across_cells': {'median': r1(big.iqr.median()), 'p25': r1(big.iqr.quantile(.25)), 'p75': r1(big.iqr.quantile(.75))},
            'iqr_over_median_pct_across_cells': {'median': r1(100 * big.ratio.median()), 'p25': r1(100 * big.ratio.quantile(.25)),
                                                 'p75': r1(100 * big.ratio.quantile(.75))},
            'cell_median_price_across_cells': {'median': r1(big.p50.median())},
            'peek_reference': {'what': '用「自己那一組的中間價」去猜組內每一間(組內含自己,等於偷看答案),只當對照',
                               'MAE_aud': r1(np.abs(y - cell_med)[in_big].mean()),
                               'M2_MAE_same_listings': r1(ae[in_big].mean()),
                               'B1_MAE_same_listings': r1(b1ae[in_big].mean())}}

    # ---------------- 4. 其他切法 ----------------
    t = d.t_host.values
    hc = d.hostcnt.values
    sec4 = {
        'bedrooms': [row(d.bed_n.values == 1, '1 個臥室'), row(d.bed_n.values == 2, '2 個臥室')],
        'district': [row(d.nb.isin(top5).values, '房子最多的前 5 區'), row(~d.nb.isin(top5).values, '其他區')],
        'group_size': [row(d.grp_size.values >= 30, '同區同臥室數那組 30 間以上'),
                       row(d.grp_size.values < 30, '同區同臥室數那組不到 30 間')],
        'host_tenure': [row(t <= 12, '新手(當房東 12 個月內)'), row(t > 12, '老手(超過 12 個月)')],
        'host_listings': [row(hc == 1, '房東名下只有 1 間'), row((hc >= 2) & (hc <= 9), '名下 2 到 9 間'),
                          row(hc >= 10, '名下 10 間以上')],
    }
    if np.isnan(t).any():
        sec4['host_tenure'].append(row(np.isnan(t), '年資欄空白'))
    meta4 = {'top5_districts': top5, 'tenure_missing_n': int(np.isnan(t).sum()),
             'hostcnt_missing_filled_as_1_n': int(d.hostcnt_missing.sum()),
             'group_size_basis': '組大小用全部 6,639 間算(同 syd_b a_grouping),含房子自己',
             'tenure_def': 'syd_c_hosts_time.py 第 101 行:hosts_time_as_host_years*12 + hosts_time_as_host_months,<=12 為新手'}
    for k, rows in sec4.items():
        assert sum(r['n'] for r in rows) == len(d), k

    # ---------------- 5. 模型看不到什麼 ----------------
    _, tree_names = B.X_tree(d.head(3), spec)
    cites = [
        ('20_雪梨深度分析.md', 303, '清潔費', '房東開的價中位數不是房東賺到的;成交價、清潔費、折扣看不到'),
        ('21_1111組會錄音整理.md', 120, '裝修欄', '掛牌價不是成交價;calendar 沒有價格欄;入住與收入是評論推算;沒有清潔費、買房價、租金、裝修欄'),
        ('raw/ab_branch_redteam_2026-11-11.md', 17, '折扣', 'calendar 欄位沒有價格;清潔費、服務費、押金、週月折扣、買價或租金的關鍵字掃描全是「沒有」'),
        ('17_定題與三層目標_v1.md', 44, '逐日價格', 'calendar 沒有逐日價格,量不出假期漲多少'),
        ('17_定題與三層目標_v1.md', 47, '裝修', 'listings 裡沒有裝修欄'),
        ('11_Airbnb與酒店取消_可行性與資料來源.md', 43, '成交價', '公開標價不是成交價,也沒有需求對價格變化的反應'),
        ('19_墨爾本深度分析.md', 222, '隨機偏移', '(墨爾本筆記,同一個 Inside Airbnb 來源)沒有成交價與真實入住;經緯度有隨機偏移'),
    ]
    cite_out = []
    for f, ln, kw, summ in cites:
        line = (NOTES / f).read_text(encoding='utf-8').splitlines()[ln - 1]
        assert kw in line, (f, ln, kw)
        cite_out.append({'file': f'Innovation Studio/notes/{f}', 'line': ln, 'keyword_checked': kw, 'says': summ})
    sec5 = {'features_used_M2': tree_names[:10] + [f'前 {B.TOP_N_AMEN} 項設施旗標(各一欄)'],
            'n_features_M2': len(tree_names), 'features_allowed_doc': B.FEATURES_ALLOWED,
            'in_data_but_deliberately_not_used': B.FEATURES_BANNED,
            'note_host_variant': '加房東名下房源數的對照版 M2 = 92.6(20_雪梨深度分析.md 第 140 行),只比 93.4 少 0.8',
            'not_in_data_per_notes': cite_out}

    out = {'scope_id': 'IS-1114-modelerror-01', 'batch': B.MAIN, 'seed': B.SEED,
           'versions': {'python': sys.version.split()[0], 'sklearn': __import__('sklearn').__version__,
                        'pandas': pd.__version__, 'numpy': np.__version__},
           'sample': {'n_model': len(d), 'n_extremes_excluded': len(ext), 'n_scope_price': len(d_all),
                      'target': '房東開的價(每晚掛牌價,澳幣),不是成交價'},
           '1_reproduction': repro,
           '1b_extremes_24': {'n': len(ext), 'M2_MAE_on_24': r1(ext_ae.mean()), 'M2_mean_signed_on_24': r1((ext_pred - ext.price_num.values).mean()),
                              'price_min': r1(ext.price_num.min()), 'price_max': r1(ext.price_num.max()),
                              'share_of_abs_err_6639_pct': r1(100 * ext_ae.sum() / (total_ae + ext_ae.sum()))},
           '2_by_actual_price': sec2, '3_within_same_kind_spread': sec3,
           '4_other_slices': sec4, '4_meta': meta4, '5_what_model_cannot_see': sec5}
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    write_md(out)
    print(json.dumps({'repro': {m: repro[m]['rerun'] for m in METHODS}, 'with_ext': with_ext,
                      'ext': out['1b_extremes_24'], 'sec2': {k: v for k, v in sec2.items() if k != 'split_rule'},
                      'sec3': sec3, 'sec4': {k: [{kk: r[kk] for kk in ('label', 'n', 'price_median', 'M2_MAE', 'M2_MdAPE_pct',
                                                                       'M2_mean_signed', 'B1_MAE')} for r in v] for k, v in sec4.items()},
                      'meta4': meta4}, ensure_ascii=False))


def a(x):
    """澳幣顯示:千分位、最多一位小數,.0 去掉。"""
    s = f'{x:,.1f}'
    return s[:-2] if s.endswith('.0') else s


def sg(x):
    return f'猜高 {a(x)}' if x > 0 else (f'猜低 {a(-x)}' if x < 0 else '不偏')


def slice_table(rows):
    t = ['| 哪一群 | 間數 | 中間價 | M2 平均猜差 | 誤差中位數 | 平均猜高/猜低 |', '|---|---|---|---|---|---|']
    for r in rows:
        t.append(f'| {r["label"]} | {r["n"]:,} | {a(r["price_median"])} | {a(r["M2_MAE"])} | {r["M2_MdAPE_pct"]}% | '
                 f'{sg(r["M2_mean_signed"])} |')
    return '\n'.join(t)


def write_md(o):
    rp, s2, s3, s4, s5, ex = (o['1_reproduction'], o['2_by_actual_price'], o['3_within_same_kind_spread'],
                              o['4_other_slices'], o['5_what_model_cannot_see'], o['1b_extremes_24'])
    q = s2['quintiles']
    t10 = s2['top10pct']
    m2 = rp['M2']['rerun']
    b1 = rp['B1']['rerun']
    pk = s3['peek_reference']
    bed1, bed2 = s4['bedrooms']
    top5, oth = s4['district']
    g30, g_lt = s4['group_size']
    newh, oldh = s4['host_tenure'][:2]
    h1, h2_9, h10 = s4['host_listings']
    n = o['sample']['n_model']
    gain_by_q = [r['B1_minus_M2_sum_abs_err'] for r in q]
    L = []
    w = L.append
    w('# 雪梨價格模型:平均猜差 93.4 澳幣是從哪裡來的(2026-11-14)')
    w('')
    w(f'- **93.4 是 {n:,} 間的平均,大部分房子沒差這麼多**:房東開的價(每晚掛牌價,不是成交價)最低的八成({s2["n_bottom80"]:,} 間)平均只差 {a(s2["MAE_bottom80"])} 澳幣。')
    w(f'- **最貴的兩成({q[4]["n"]:,} 間,每晚 {a(q[4]["price_min"])} 澳幣以上)占了全部猜差的 {s2["share_top20_pct"]}%**;'
      f'最貴的一成({t10["n"]:,} 間)就占 {s2["share_top10_pct"]}%。')
    w(f'- **模型會往中間猜**:最貴兩成平均{sg(q[4]["M2_mean_signed"])},最便宜兩成平均{sg(q[0]["M2_mean_signed"])}。')
    w(f'- **條件一樣的房子,房東開的價本來就很散**:同區、同臥室數、同人數的小組裡,排 25% 到排 75% 的價差 {a(s3["iqr_aud_across_cells"]["median"])} 澳幣'
      f'(各組中間值),約是該組中間價的 {s3["iqr_over_median_pct_across_cells"]["median"]}%。')
    w('')
    w('## 先講清楚猜的是什麼')
    w('')
    w('- 模型猜的是「房東開的價」(掛牌價,每晚、澳幣;不是成交價,也不含清潔費和折扣)。')
    w(f'- 樣本:雪梨 {o["batch"]} 期,整套出租、1 到 2 個臥室、住 2 到 4 人、最少住 1 到 7 晚、有開價,拿掉一晚超過 2,000 澳幣的 {o["sample"]["n_extremes_excluded"]} 間,共 {n:,} 間。')
    w('- 每一間的預測都是「沒看過這一間的房東」的模型猜的:同一個房東的房子放在同一份,分 5 份輪流猜。')
    w('- 中間價 = 排在正中間那一間的價。平均猜差 = 每一間猜的價跟真的開價差多少(不管猜高猜低),全部平均。')
    w('- 誤差中位數 = 每一間差了幾 %,排在正中間的那個 %。')
    w('')
    w('## 1. 先重跑一次,數字對得上')
    w('')
    w(f'照原本的腳本(syd_b_positioning.py,同一份資料、同樣的切法和隨機種子 {o["seed"]},sklearn {o["versions"]["sklearn"]})重跑,{n:,} 間的結果跟既有數字一樣。')
    w('')
    w('| 方法 | 既有平均猜差 | 重跑平均猜差 | 重跑誤差中位數 | 重跑差 20% 以內 |')
    w('|---|---|---|---|---|')
    names = {'B0': 'B0 全市中間價', 'B1': 'B1 同區同臥室數的中間價', 'M1': 'M1 線性模型', 'M2': 'M2 梯度提升樹'}
    for m in ('B0', 'B1', 'M1', 'M2'):
        r = rp[m]
        w(f'| {names[m]} | {a(r["published"]["MAE_aud"])} | {a(r["rerun"]["MAE_aud"])} | {r["rerun"]["MdAPE_pct"]}% | {r["rerun"]["within20_pct"]}% |')
    w('')
    w(f'- 把那 {ex["n"]} 間超貴的放回去(共 {rp["M2_with_24_extremes"]["rerun"]["n"]:,} 間),M2 平均猜差變 {a(rp["M2_with_24_extremes"]["rerun"]["MAE_aud"])}(既有 113.5,一樣)。')
    w(f'- 這 {ex["n"]} 間每晚 {a(ex["price_min"])} 到 {a(ex["price_max"])} 澳幣,模型平均{sg(ex["M2_mean_signed_on_24"])};'
      f'光這 {ex["n"]} 間就占 {rp["M2_with_24_extremes"]["rerun"]["n"]:,} 間猜差總和的 {ex["share_of_abs_err_6639_pct"]}%。以下都只看 {n:,} 間。')
    w('')
    w('## 2. 貴的房子是不是誤差的主要來源')
    w('')
    w(f'這張表把 {n:,} 間照「房東開的價」由低到高分成 5 等份(每份 {q[0]["n"]:,} 間),再把最貴的一成單獨列,看每一段猜差多少、偏哪邊。')
    w('')
    w('| 哪一段 | 間數 | 開價範圍(澳幣) | 中間價 | M2 平均猜差 | 誤差中位數 | 平均猜高/猜低 | B1 平均猜差 | 占全部猜差 |')
    w('|---|---|---|---|---|---|---|---|---|')
    for r in q + [t10]:
        w(f'| {r["label"]} | {r["n"]:,} | {a(r["price_min"])}–{a(r["price_max"])} | {a(r["price_median"])} | {a(r["M2_MAE"])} | '
          f'{r["M2_MdAPE_pct"]}% | {sg(r["M2_mean_signed"])} | {a(r["B1_MAE"])} | {r["share_of_total_abs_err_pct"]}% |')
    w('')
    ck = s2['checks']
    w(f'- 對帳:5 等份間數加起來 {ck["n_sum"]:,};5 等份的猜差總和加起來 {a(ck["sum_abs_err_quintiles"])},等於全部 {a(ck["total_abs_err"])}(= {a(m2["MAE_aud"])} × {n:,} 的未四捨五入值)。'
      f'最貴一成是第 5 等份的一部分,不另外加。')
    w(f'- 相鄰兩段的邊界上有 {ck["boundary_ties_between_quintiles"]} 處同價(表上 {" 和 ".join(a(v) for v in ck["boundary_tie_prices"])} 出現在兩段),同價的房子照原本順序分到兩邊。')
    w(f'- **看澳幣**:最貴兩成平均差 {a(q[4]["M2_MAE"])},是中間兩成({a(q[2]["M2_MAE"])})的 {q[4]["M2_MAE"] / q[2]["M2_MAE"]:.1f} 倍。')
    w(f'- **看百分比,也是兩頭比較難猜**:中間兩成誤差中位數 {q[2]["M2_MdAPE_pct"]}%,最便宜兩成 {q[0]["M2_MdAPE_pct"]}%,最貴兩成 {q[4]["M2_MdAPE_pct"]}%,最貴一成 {t10["M2_MdAPE_pct"]}%。'
      '所以貴的房子不只是「價錢大、差的澳幣自然多」,按比例也比較難猜。')
    w(f'- **模型猜的範圍比真的窄**:{n:,} 間裡,M2 猜的價排在 99% 的是 {a(s2["pred_range_M2"]["p99"])},最高只猜到 {a(s2["pred_range_M2"]["max"])};'
      f'真的開價排在 99% 的是 {a(s2["actual_range"]["p99"])},最高 {a(s2["actual_range"]["max"])}。所以越貴越容易被猜低,越便宜越容易被猜高。')
    w(f'- **M2 比 B1 好在哪一段**:M2 比 B1 少差的總和,第 1 段 {a(gain_by_q[0])}、第 2 段 {a(gain_by_q[1])}、第 3 段 {a(gain_by_q[2])}、'
      f'第 4 段 {a(gain_by_q[3])}、第 5 段 {a(gain_by_q[4])}(負數 = M2 反而差比較多)。在中間兩段,簡單的「同區同臥室數中間價」反而猜得比較近。')
    w('')
    w('## 3. 同類的房子,房東開的價本來就差很多嗎')
    w('')
    w(f'這張表看「條件一樣」的房子開價有多散:把 {n:,} 間分成「同一區 × 同樣臥室數 × 能住的人數」的小組,只算至少 {MIN_CELL} 間的組。')
    w('')
    w('| 項目 | 數字 |')
    w('|---|---|')
    w(f'| 小組數(全部 / 至少 {MIN_CELL} 間) | {s3["n_cells_total"]} / {s3["n_cells_ge20"]} |')
    w(f'| 至少 {MIN_CELL} 間的組共有幾間房 | {s3["n_listings_in_cells_ge20"]:,} |')
    w(f'| 排 25% 到排 75% 的價差(各組的中間值) | {a(s3["iqr_aud_across_cells"]["median"])} 澳幣(一半的組落在 {a(s3["iqr_aud_across_cells"]["p25"])} 到 {a(s3["iqr_aud_across_cells"]["p75"])}) |')
    w(f'| 這個價差占該組中間價幾 %(各組的中間值) | {s3["iqr_over_median_pct_across_cells"]["median"]}%(一半的組落在 {s3["iqr_over_median_pct_across_cells"]["p25"]}% 到 {s3["iqr_over_median_pct_across_cells"]["p75"]}%) |')
    w(f'| 各組中間價的中間值 | {a(s3["cell_median_price_across_cells"]["median"])} 澳幣 |')
    w('')
    w(f'- 意思是:同一區、同樣臥室數、能住一樣多人的房子,中間那一半的開價,高低就差 {a(s3["iqr_aud_across_cells"]["median"])} 澳幣左右。')
    w(f'- 對照(偷看答案的做法):直接拿「自己那一組的中間價」去猜組裡每一間(組裡包含自己),這 {s3["n_listings_in_cells_ge20"]:,} 間平均還是差 {a(pk["MAE_aud"])}。'
      f'M2 在同一群房子是 {a(pk["M2_MAE_same_listings"])},B1 是 {a(pk["B1_MAE_same_listings"])}。')
    w(f'- 也就是說,光知道區、臥室數、人數,就算偷看答案,平均也差 {a(pk["MAE_aud"])};M2 多看了設施、經緯度等,也只比偷看答案的做法少差 {a(pk["MAE_aud"] - pk["M2_MAE_same_listings"])}。')
    w('')
    w('## 4. 其他切法')
    w('')
    w(f'下面每張表都是同一批 {n:,} 間、同一個 M2 的預測,只是換一種分法。「中間價」是那一群房東開的價的中間價。')
    w('')
    w('**1 個臥室對 2 個臥室**:看臥室數不同,猜差差多少。')
    w('')
    w(slice_table(s4['bedrooms']))
    w('')
    w(f'- 2 個臥室平均多差 {a(bed2["M2_MAE"] - bed1["M2_MAE"])} 澳幣,但誤差中位數只差 {bed2["M2_MdAPE_pct"] - bed1["M2_MdAPE_pct"]:.1f} 個百分點;2 個臥室本來就比較貴(中間價 {a(bed2["price_median"])} 對 {a(bed1["price_median"])})。')
    w('')
    w(f'**房子最多的前 5 區對其他區**:前 5 區是 {"、".join(o["4_meta"]["top5_districts"])}(用 6,639 間排)。')
    w('')
    w(slice_table(s4['district']))
    w('')
    w(f'- 前 5 區平均多差 {a(top5["M2_MAE"] - oth["M2_MAE"])},誤差中位數幾乎一樣({top5["M2_MdAPE_pct"]}% 對 {oth["M2_MdAPE_pct"]}%);前 5 區比較貴(中間價 {a(top5["price_median"])} 對 {a(oth["price_median"])})。')
    w('')
    w('**同區同臥室數那一組有 30 間以上,對不到 30 間**:組大小用 6,639 間算、含自己。看房子少的組是不是比較難猜。')
    w('')
    w(slice_table(s4['group_size']))
    w('')
    w(f'- 不到 30 間的組反而平均差比較少({a(g_lt["M2_MAE"])},{g_lt["n"]:,} 間),這群房子也比較便宜(中間價 {a(g_lt["price_median"])})。')
    w('')
    w('**新手對老手**:年資 = 當房東的年數 × 12 + 月數(照 syd_c_hosts_time.py),12 個月以內算新手。')
    w('')
    w(slice_table(s4['host_tenure']))
    w('')
    w(f'- 新手的房子({newh["n"]:,} 間)平均差 {a(newh["M2_MAE"])},沒有比老手({a(oldh["M2_MAE"])})差;新手整體幾乎不偏({sg(newh["M2_mean_signed"])}),老手平均{sg(oldh["M2_mean_signed"])}。')
    w('')
    w('**房東名下有幾間**:用資料裡的 calculated_host_listings_count(房東在雪梨名下的房源數;模型沒有用這一欄)。')
    w('')
    w(slice_table(s4['host_listings']))
    w('')
    w(f'- 名下 10 間以上的房子({h10["n"]:,} 間)平均{sg(h10["M2_mean_signed"])},是各群裡偏最多的;但誤差中位數最低({h10["M2_MdAPE_pct"]}%)。這只是一起出現的現象,不知道原因。')
    w('')
    w('## 5. 模型看不到什麼')
    w('')
    w(f'**模型用了哪些欄位**(M2 共 {s5["n_features_M2"]} 欄,來源 syd_b_positioning.py 第 49–51、180–192 行):'
      + '、'.join(f.replace('房間數', '臥室數') for f in s5['features_used_M2']) + '。')
    w('')
    w('**資料裡有、但模型刻意不用的**(syd_b_positioning.py 第 52–58 行,理由是新房東上架前沒有,或會直接洩漏答案):'
      '評論數與評分、可訂天數、推算的入住與營收、報價欄、超讚房東與房東名下房源數。'
      f'加了房東名下房源數的對照版,M2 平均猜差 92.6,只比 93.4 少 0.8(20_雪梨深度分析.md 第 140 行)。')
    w('')
    w('**既有筆記已經寫過「資料裡沒有」的東西**(只引用筆記原本寫的):')
    w('')
    for c in s5['not_in_data_per_notes']:
        w(f'- {c["says"]}。〔{c["file"]} 第 {c["line"]} 行〕')
    w('')
    w('**推測,沒有資料佐證**(以下是我想到可能影響開價、但模型沒有、筆記也沒寫過的,沒有驗證):')
    w('')
    w('- 照片、裝潢新舊、看不看得到海或港、樓層。')
    w('- 房源標題和描述文字(資料裡有這些欄,這次的模型沒讀)。')
    w('- 房東自己的策略:想快點租出去就開低、想試水溫就開高、多久改一次價。')
    w('- 抓資料那天剛好是什麼日子:開價可能是那幾天的價,不是平常的價(筆記只記了「沒有逐日價格」,沒記這件事)。')
    w('')
    w('## 6. 所以為什麼差 93.4')
    w('')
    w(f'93.4 是 {n:,} 間的平均,大部分房子沒差這麼多:開價最低的八成({s2["n_bottom80"]:,} 間)平均只差 {a(s2["MAE_bottom80"])}。'
      f'平均被最貴的一段拉高:最貴兩成({q[4]["n"]:,} 間,{a(q[4]["price_min"])} 澳幣以上)平均差 {a(q[4]["M2_MAE"])},占全部猜差的 {s2["share_top20_pct"]}%。'
      f'模型會往中間猜,最貴兩成平均{sg(q[4]["M2_mean_signed"])}、最便宜兩成平均{sg(q[0]["M2_mean_signed"])}。'
      f'條件一樣的房子,房東開的價本來就差很多:中間那一半高低差 {a(s3["iqr_aud_across_cells"]["median"])}(約中間價的 {s3["iqr_over_median_pct_across_cells"]["median"]}%),就算偷看每組的中間價去猜,平均也差 {a(pk["MAE_aud"])}。'
      f'模型只有 {s5["n_features_M2"]} 欄可用,筆記也記了資料裡沒有成交價、裝修、清潔費、折扣與逐日價格,剩下的差距沒辦法用這份資料再往下拆。')
    w('')
    w('## 怎麼講才對')
    w('')
    w(f'- 不要說「模型不準」→ 改說「模型平均差 {a(m2["MAE_aud"])} 澳幣,一半的房子差在 {m2["MdAPE_pct"]}% 以內;開價最低的八成平均差 {a(s2["MAE_bottom80"])},差最多的是最貴的兩成。它比只看同區同臥室數中間價的做法({a(b1["MAE_aud"])})少差 {a(b1["MAE_aud"] - m2["MAE_aud"])}」。')
    w(f'- 不要說「93.4 就是每間都差 93.4」→ 改說「這是 {n:,} 間的平均,被最貴的兩成拉高;最貴兩成占了全部猜差的 {s2["share_top20_pct"]}%」。')
    w(f'- 不要說「貴的房子猜不準,是因為裝修好、景觀好」→ 改說「最貴兩成平均{sg(q[4]["M2_mean_signed"])};資料裡沒有裝修、照片這類欄位,所以說不出是什麼原因」。')
    w('- 不要說「模型猜的是房子租得到的價錢」或「成交價」→ 改說「猜的是房東開的價(掛牌價),不是成交價,也不含清潔費和折扣」。')
    w(f'- 不要說「2 個臥室比較難猜」→ 改說「2 個臥室平均差的澳幣比較多({a(bed2["M2_MAE"])} 對 {a(bed1["M2_MAE"])}),但按百分比差不多({bed2["M2_MdAPE_pct"]}% 對 {bed1["M2_MdAPE_pct"]}%),跟它比較貴有關」。')
    w(f'- 不要說「名下房子多的房東被模型低估,是因為他們故意開高價」→ 改說「名下 10 間以上的房子,模型平均{sg(h10["M2_mean_signed"])};這是一起出現(關聯),不是原因(因果)」。')
    w(f'- 不要說「條件一樣的房子應該開一樣的價,開不一樣的是開錯」→ 改說「條件一樣的房子,中間那一半的開價本來就差 {a(s3["iqr_aud_across_cells"]["median"])} 左右,這是房東開的價本身的散法」。')
    w(f'- 不要說「拿掉 24 間是為了讓數字好看」→ 改說「這 24 間一晚超過 2,000 澳幣,另外看;放回去平均猜差變 {a(rp["M2_with_24_extremes"]["rerun"]["MAE_aud"])},光它們就占 {rp["M2_with_24_extremes"]["rerun"]["n"]:,} 間猜差總和的 {ex["share_of_abs_err_6639_pct"]}%」。')
    w('')
    w('<sub>來源:Innovation Studio/analysis/sydney/syd_v_model_error.py(可重跑:python -I syd_v_model_error.py);'
      '數字見 syd_v_model_error_2026-11-14.json;既有數字見 20_雪梨深度分析.md 第 126–155 行。'
      '每間房的預測值只存在 scratchpad/syd_v_model_error/,不進 repo。</sub>')
    OUT_MD.write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
