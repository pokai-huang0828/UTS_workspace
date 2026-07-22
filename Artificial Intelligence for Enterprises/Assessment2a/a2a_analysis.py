# A2a 分析主幹 — 依 2026-07-22 兩腦決議 13 條(見 notes/A2a_作戰計畫.md §六)
# 跑通後移植進課程範本 notebook;本檔為驗證基準(R-完成證據)。
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, RepeatedStratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.inspection import permutation_importance

RS = 42
pd.set_option('display.width', 200)

# ── 資料與切分(決議 1:stratified 80/20,random_state=42)──
df = pd.read_csv('Assessment 2a Cellphone-1.csv')
X, y = df.drop(columns=['Churn']), df['Churn']          # 決議 10:Churn=1 = 正類(流失)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=RS)  # 0.3 對齊課程範本;stratify+RS 為本作業改進
neg, pos = int((y_tr == 0).sum()), int((y_tr == 1).sum())
spw = neg / pos                                          # XGB 的 scale_pos_weight 候選值

# ── 六模型 × 配置候選(決議 5:class_weight/scale_pos_weight 進 CV;決議 7:Pipeline 防洩漏)──
def build(name, weighted):
    cw = 'balanced' if weighted else None
    if name == 'RandomForest':
        return RandomForestClassifier(random_state=RS, class_weight=cw)
    if name == 'DecisionTree':
        return DecisionTreeClassifier(random_state=RS, class_weight=cw)
    if name == 'KNN':
        return Pipeline([('scaler', StandardScaler()), ('model', KNeighborsClassifier())])
    if name == 'SVC':
        return Pipeline([('scaler', StandardScaler()), ('model', SVC(random_state=RS, class_weight=cw))])
    if name == 'LogisticRegression':
        return Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression(max_iter=1000, random_state=RS, class_weight=cw))])
    if name == 'XGBoost':
        return XGBClassifier(random_state=RS, eval_metric='logloss',
                             scale_pos_weight=(spw if weighted else 1.0))

MODELS = ['RandomForest', 'KNN', 'DecisionTree', 'SVC', 'LogisticRegression', 'XGBoost']
HAS_WEIGHT = {'RandomForest', 'DecisionTree', 'SVC', 'LogisticRegression', 'XGBoost'}  # KNN 無
# 決議 2:AdaBoost 為範本附帶的第七分類器 → notebook 附加項,不進六模型主表與選模
from sklearn.ensemble import AdaBoostClassifier
def build_ada():
    return AdaBoostClassifier(random_state=RS, algorithm='SAMME')

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RS)          # 閾值掃描用
# R1 修訂(2026-07-22 實跑發現 0.2/0.3 切分會翻轉贏家):選模 CV 升級為 5×5 重複分層,
# 以 25 折均值消除單次 5-fold 的抽樣噪音;測試集仍只碰一次。
cv_sel = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=RS)
scoring = {'f1': 'f1', 'recall': 'recall', 'precision': 'precision', 'accuracy': 'accuracy'}

# ── 決議 1+5:訓練集 5-fold CV 選配置與選模(主準則 churn-F1)──
cv_rows = []
cv_raw_scores = {}
for name in MODELS:
    for weighted in ([False, True] if name in HAS_WEIGHT else [False]):
        res = cross_validate(build(name, weighted), X_tr, y_tr, cv=cv_sel, scoring=scoring)
        cv_raw_scores[(name, weighted)] = res
        cv_rows.append({
            'model': name, 'weighted': weighted,
            'cv_f1_mean': res['test_f1'].mean(),   'cv_f1_std': res['test_f1'].std(),
            'cv_recall_mean': res['test_recall'].mean(),
            'cv_precision_mean': res['test_precision'].mean(),
            'cv_accuracy_mean': res['test_accuracy'].mean(),
        })
cv_df = pd.DataFrame(cv_rows)

# 每模型取配置:balanced 的 CV-F1 改善 > 0.01 才採用(決議 5「實質改善」),否則預設
chosen = {}
for name in MODELS:
    sub = cv_df[cv_df.model == name].set_index('weighted')
    if True in sub.index and sub.loc[True, 'cv_f1_mean'] - sub.loc[False, 'cv_f1_mean'] > 0.01:
        chosen[name] = True
    else:
        chosen[name] = False
sel = cv_df[[chosen[r.model] == r.weighted for r in cv_df.itertuples()]].copy()

# 選模規則(決議 1/9):CV churn-F1 → recall → CV std 小 → 可解釋性
interp_rank = {'DecisionTree': 0, 'LogisticRegression': 1, 'RandomForest': 2, 'XGBoost': 3, 'SVC': 4, 'KNN': 5}
sel['interp'] = sel.model.map(interp_rank)
sel = sel.sort_values(['cv_f1_mean', 'cv_recall_mean', 'cv_f1_std', 'interp'],
                      ascending=[False, False, True, True]).reset_index(drop=True)
winner = sel.loc[0, 'model']

# R1 補強 v2:前二名以 Nadeau–Bengio 校正重採樣檢定(重複 CV 折間相依,普通配對 t 會高估顯著性)
from scipy import stats
def corrected_ttest(a, b, k=25, rho=0.25):
    d = np.asarray(a) - np.asarray(b)
    var = d.var(ddof=1)
    if var == 0:
        return 0.0, 1.0
    t = d.mean() / np.sqrt(var * (1 / k + rho))
    return t, 2 * stats.t.sf(abs(t), df=k - 1)

top2 = list(sel.model[:2])
paired = {}
for metric in ('f1', 'recall', 'precision'):
    a = cv_raw_scores[(top2[0], chosen[top2[0]])]['test_' + metric]
    b = cv_raw_scores[(top2[1], chosen[top2[1]])]['test_' + metric]
    t, p = corrected_ttest(a, b)
    paired[metric] = {'diff_mean': float((a - b).mean()), 'corrected_p': float(p), 'significant': bool(p < 0.05)}

# ── 測試集只碰一次:六模型最終配置的原生 predict(決議 4:不動閾值)──
test_rows, fitted = [], {}
for name in MODELS:
    m = build(name, chosen[name]).fit(X_tr, y_tr)
    fitted[name] = m
    yp = m.predict(X_te)
    tn, fp, fn, tp = confusion_matrix(y_te, yp, labels=[0, 1]).ravel()   # 決議 10:固定順序
    test_rows.append({
        'model': name, 'weighted': chosen[name],
        'accuracy': accuracy_score(y_te, yp), 'precision': precision_score(y_te, yp),
        'recall': recall_score(y_te, yp), 'f1': f1_score(y_te, yp),
        'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp),
    })
test_df = pd.DataFrame(test_rows).set_index('model')

# 附加:AdaBoost(第七分類器,僅 notebook 展示,不參與選模)
ada = build_ada().fit(X_tr, y_tr)
yp_ada = ada.predict(X_te)
atn, afp, afn, atp = confusion_matrix(y_te, yp_ada, labels=[0, 1]).ravel()
ada_row = {'accuracy': accuracy_score(y_te, yp_ada), 'precision': precision_score(y_te, yp_ada),
           'recall': recall_score(y_te, yp_ada), 'f1': f1_score(y_te, yp_ada),
           'tn': int(atn), 'fp': int(afp), 'fn': int(afn), 'tp': int(atp)}

# ── 決議 3+10:FN 稽核與三層損失 ──
yp_w = fitted[winner].predict(X_te)
tn, fp, fn, tp = confusion_matrix(y_te, yp_w, labels=[0, 1]).ravel()
fn_mask = (y_te.values == 1) & (yp_w == 0)
fn_idx = X_te.index[fn_mask]
fn_monthly = X_te.loc[fn_idx, 'MonthlyCharge']
audit3 = df.loc[fn_idx[:3], ['Churn', 'MonthlyCharge']]                  # 抽 3 筆逐列核對
gross = {m: float(fn_monthly.sum() * m) for m in (6, 12, 24)}            # 毛暴露上限
SAVE_RATE = 0.30                                                          # 假設:主動挽留可救回 30%(報告引文獻)
expected = {m: v * SAVE_RATE for m, v in gross.items()}                  # 預期可挽回損失
churn_te = int((y_te == 1).sum())
extrap = {m: float(v / churn_te * 483) for m, v in gross.items()}        # 外推全客群(標「推估」)

# ── 決議 9:permutation importance(測試集,n_repeats=30,scoring=f1)──
pi = permutation_importance(fitted[winner], X_te, y_te, n_repeats=30, random_state=RS, scoring='f1')
pi_df = pd.DataFrame({'feature': X.columns, 'mean': pi.importances_mean, 'std': pi.importances_std}) \
          .sort_values('mean', ascending=False).reset_index(drop=True)
native = {}
for name in ('RandomForest', 'DecisionTree', 'XGBoost'):
    imp = fitted[name].feature_importances_
    native[name] = pd.Series(imp, index=X.columns).sort_values(ascending=False)

# ── 決議 4:閾值敏感度(僅贏家;成本比要有依據)──
# 成本假設:FN 成本 = 該客戶月費×12(流失一年);FP 成本 = 挽留 offer ≈ 1 個月月費 → 比約 12:1
FN_COST_M, FP_COST_M = 12, 1
proba_cv = cross_val_predict(build(winner, chosen[winner]), X_tr, y_tr, cv=cv, method='predict_proba')[:, 1]
med_fee = float(df['MonthlyCharge'].median())
ths = np.arange(0.05, 0.951, 0.01)
costs = []
for t in ths:
    yp_t = (proba_cv >= t).astype(int)
    _tn, _fp, _fn, _tp = confusion_matrix(y_tr, yp_t, labels=[0, 1]).ravel()
    costs.append(_fn * FN_COST_M * med_fee + _fp * FP_COST_M * med_fee)
best_t = float(ths[int(np.argmin(costs))])
proba_te = fitted[winner].predict_proba(X_te)[:, 1]
yp_bt = (proba_te >= best_t).astype(int)
btn, bfp, bfn, btp = confusion_matrix(y_te, yp_bt, labels=[0, 1]).ravel()

# ── 圖(報告用)──
import os
os.makedirs('figures', exist_ok=True)
ax = test_df[['f1', 'recall', 'precision', 'accuracy']].plot.bar(figsize=(9, 4.5), rot=15)
ax.set_title('Six classifiers on the held-out test set (Churn class)'); ax.set_ylabel('score')
plt.tight_layout(); plt.savefig('figures/fig1_model_comparison.png', dpi=130); plt.close()

fig, axm = plt.subplots(figsize=(4, 3.5))
cm = np.array([[tn, fp], [fn, tp]])
axm.imshow(cm, cmap='Blues')
for (i, j), v in np.ndenumerate(cm):
    axm.text(j, i, f'{v}', ha='center', va='center',
             color='white' if v > cm.max()/2 else 'black', fontsize=14)
axm.set_xticks([0, 1], ['Pred 0', 'Pred 1']); axm.set_yticks([0, 1], ['True 0', 'True 1'])
axm.set_title(f'{winner} confusion matrix (test)')
plt.tight_layout(); plt.savefig('figures/fig2_confusion_winner.png', dpi=130); plt.close()

fig, axp = plt.subplots(figsize=(7, 4))
axp.barh(pi_df.feature[::-1], pi_df['mean'][::-1], xerr=pi_df['std'][::-1])
axp.set_title(f'Permutation importance on test (n_repeats=30, scoring=F1) — {winner}')
plt.tight_layout(); plt.savefig('figures/fig3_perm_importance.png', dpi=130); plt.close()

fig, axc = plt.subplots(figsize=(6, 3.5))
axc.plot(ths, costs); axc.axvline(best_t, ls='--', c='r')
axc.set_xlabel('threshold'); axc.set_ylabel('expected cost (A$, CV on train)')
axc.set_title(f'Cost-based threshold sweep (FN:FP = 12:1) — min at {best_t:.2f}')
plt.tight_layout(); plt.savefig('figures/fig4_threshold_cost.png', dpi=130); plt.close()

# ── 輸出 ──
out = {
    'split': {'train': len(X_tr), 'test': len(X_te), 'churn_train': pos, 'churn_test': churn_te, 'scale_pos_weight': spw},
    'chosen_config': chosen, 'winner': winner,
    'cv_table': sel.drop(columns='interp').round(4).to_dict('records'),
    'test_table': test_df.round(4).reset_index().to_dict('records'),
    'fn_audit': {'fn': int(fn), 'fn_monthly_sum': float(fn_monthly.sum()),
                 'fn_monthly_mean': float(fn_monthly.mean()),
                 'gross_exposure': gross, 'save_rate': SAVE_RATE, 'expected_recoverable': expected,
                 'extrapolated_all_customers': extrap},
    'perm_importance': pi_df.round(4).to_dict('records'),
    'native_importance_top3': {k: v.head(3).round(4).to_dict() for k, v in native.items()},
    'threshold': {'best_t': best_t, 'assumption': 'FN=12 months median fee, FP=1 month median fee',
                  'test_at_best_t': {'tn': int(btn), 'fp': int(bfp), 'fn': int(bfn), 'tp': int(btp)}},
    'adaboost_supplementary': {k: (round(v, 4) if isinstance(v, float) else v) for k, v in ada_row.items()},
    'paired_ttest_top2': {'models': top2, 'metrics': paired},
}
json.dump(out, open('a2a_results.json', 'w'), indent=1)

print('=== CV selection (training set, chosen configs) ===')
print(sel.drop(columns='interp').round(4).to_string(index=False))
print('\nWINNER by pre-committed rule:', winner, '| config weighted =', chosen[winner])
print('\n=== Test set (one shot, native predict) ===')
print(test_df.round(4).to_string())
print('\n=== FN audit (winner) ===')
print(f'FN={fn}  sum(MonthlyCharge of FN)={fn_monthly.sum():.1f}  mean={fn_monthly.mean():.2f}')
print('audit rows (df values match X_te):'); print(audit3.to_string())
print('gross exposure 6/12/24m:', {k: round(v) for k, v in gross.items()})
print('expected recoverable @30%:', {k: round(v) for k, v in expected.items()})
print('extrapolated to 483 churners:', {k: round(v) for k, v in extrap.items()})
print('\n=== Permutation importance (test, mean±std) ===')
print(pi_df.round(4).to_string(index=False))
print('\nnative top3:', {k: list(v.head(3).index) for k, v in native.items()})
print('\n=== Threshold ===')
print(f'best_t={best_t:.2f}  test at best_t: tn={btn} fp={bfp} fn={bfn} tp={btp}  (default FN={fn})')
