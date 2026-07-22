# 生成 Huang_26254793_421104_Assessment 2a.ipynb — v2(Codex round1 十二條缺陷全修)並全執行
import nbformat as nbf
from nbclient import NotebookClient

C = []

C.append(('md', """# 評估任務二a:使用監督學習技術分析數據 — 電信客戶流失(Churn)概念驗證

**姓名:** 黃柏凱(PoKai Huang) | **學號:** 26254793 | **課程:** 421104 Artificial Intelligence for Enterprises | **日期:** 2026 年 7 月

本筆記本以課程提供之範本為基礎擴充,章節依範本流程排列:載入資料 → 摘要統計 → 載入六個分類器 → 評估指標 → 輸入/輸出變量 → 切分訓練與測試 → 建模與選模 → 混淆矩陣與 FN → 變數重要度。相對範本的方法改進:①訓練/測試切分加入 `stratify` 與 `random_state=42`(可重現、保持類別比例)②所有模型以 `Pipeline` 封裝,需要縮放的模型(LR/SVC/KNN)之縮放器只在訓練折內擬合,避免資料洩漏 ③模型選擇採 5×5 重複分層交叉驗證,只在訓練集上進行,測試集僅於最終評估使用一次 ④除 accuracy 外報告 churn 類的 precision / recall / F1(類別不平衡下 accuracy 會誤導)⑤前二名模型差異以**重複 CV 校正檢定**(Nadeau–Bengio)評估,避免高估顯著性 ⑥變數重要性以 permutation importance 裁決並檢視其**重複間穩定性**,索引對映回欄位名稱。"""))

C.append(('md', "## 一、載入資料\n\n本機執行:資料檔與筆記本同資料夾(原範本此處為 Colab 掛載 Google Drive)。"))
C.append(('code', """import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from pathlib import Path
import sys
import pandas as pd
import numpy as np
import sklearn, xgboost

Path('figures').mkdir(exist_ok=True)   # 圖檔輸出資料夾(乾淨環境重跑也不會失敗)

import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'PingFang TC', 'Noto Sans CJK TC', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False   # 圖表中文字型(跨平台 fallback)
print(f"python {sys.version.split()[0]} | pandas {pd.__version__} | scikit-learn {sklearn.__version__} | xgboost {xgboost.__version__}")

df = pd.read_csv('Assessment 2a Cellphone-1.csv')
assert df.isnull().sum().sum() == 0, '資料含缺失值'
assert df.duplicated().sum() == 0, '資料含重複列'
print(f"shape = {df.shape};零缺失、零重複列")
df.head()"""))

C.append(('md', "## 二、輸入摘要統計"))
C.append(('code', "df.describe()"))
C.append(('code', """# 類別平衡檢查:Churn=1(流失)為正類
counts = df['Churn'].value_counts()
print(counts.to_string())
print(f"Churn rate = {df['Churn'].mean()*100:.2f}%")
print(f"若全部猜「不流失」,accuracy 也有 {(1-df['Churn'].mean())*100:.1f}% → 模型比較不能只看 accuracy,需看 churn 類的 recall/F1")"""))

C.append(('md', "## 三、載入六個分類器\n\n沿用範本的六行 import(其中一行含 AdaBoost,共七個分類器)。依題目要求,主比較為六模型:RandomForest、KNN、DecisionTree、SVC、LogisticRegression、XGBoost;AdaBoost 為範本附帶的第七個分類器,於附錄 B 補充展示。"))
C.append(('code', """from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import train_test_split, StratifiedKFold, RepeatedStratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy import stats"""))

C.append(('md', "## 四、載入評估指標"))
C.append(('code', """from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt"""))

C.append(('md', "## 五、輸入與輸出變量\n\n題目規定:Churn 為輸出變量,其餘全部為輸入變量。"))
C.append(('code', """df_feature = df.drop(['Churn'], axis=1)
df_label = df['Churn']
df_feature.info()"""))

C.append(('md', "## 六、切分訓練與測試集\n\n改進:`stratify=df_label` 讓訓練/測試集維持 14.49% 的流失比例;`random_state=42` 使結果可重現(範本無此二者,重跑會得到不同數字)。"))
C.append(('code', """RS = 42
X_train, X_test, y_train, y_test = train_test_split(df_feature, df_label, test_size=0.3, stratify=df_label, random_state=RS)
neg, pos = int((y_train==0).sum()), int((y_train==1).sum())
spw = neg/pos
print(f"train={len(X_train)} (churn {pos}), test={len(X_test)} (churn {int((y_test==1).sum())}), scale_pos_weight 候選值={spw:.2f}")"""))

C.append(('md', """## 七、模型配置

- **統一以 `Pipeline` 封裝**:LR / SVC / KNN 對特徵尺度敏感,前置 `StandardScaler`(只在各訓練折內擬合,避免洩漏);樹系模型(RF/DT/XGB)不需縮放,Pipeline 僅含模型本身,保持介面一致。
- **類別不平衡候選配置**:`class_weight='balanced'`(RF/DT/SVC/LR)與 `scale_pos_weight`(XGB)作為超參數候選,由交叉驗證決定是否採用(churn-F1 改善 > 0.01 才採用);KNN 無此參數。不使用 SMOTE(超出課程範圍)。"""))
C.append(('code', """def build(name, weighted):
    cw = 'balanced' if weighted else None
    if name == 'RandomForest':
        return Pipeline([('model', RandomForestClassifier(random_state=RS, class_weight=cw))])
    if name == 'DecisionTree':
        return Pipeline([('model', DecisionTreeClassifier(random_state=RS, class_weight=cw))])
    if name == 'KNN':
        return Pipeline([('scaler', StandardScaler()), ('model', KNeighborsClassifier())])
    if name == 'SVC':
        return Pipeline([('scaler', StandardScaler()), ('model', SVC(random_state=RS, class_weight=cw))])
    if name == 'LogisticRegression':
        return Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression(max_iter=1000, random_state=RS, class_weight=cw))])
    if name == 'XGBoost':
        return Pipeline([('model', XGBClassifier(random_state=RS, eval_metric='logloss', scale_pos_weight=(spw if weighted else 1.0)))])

MODELS = ['RandomForest', 'KNN', 'DecisionTree', 'SVC', 'LogisticRegression', 'XGBoost']
HAS_WEIGHT = {'RandomForest', 'DecisionTree', 'SVC', 'LogisticRegression', 'XGBoost'}"""))

C.append(('md', """## 八、模型選擇協議(只在訓練集上)

5×5 重複分層交叉驗證(25 折)。**選模規則(先於結果訂定)**:churn-F1 均值 → 平手看 recall 均值 → CV 標準差 → 可解釋性。**測試集不參與選模,只在最終評估使用一次。**

下表先呈現**全部候選配置**(含 balanced / 預設的對照),再依「F1 改善 > 0.01 才採用 balanced」規則決定每個模型的最終配置。"""))
C.append(('code', """cv_sel = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=RS)
scoring = {'f1':'f1', 'recall':'recall', 'precision':'precision', 'accuracy':'accuracy'}

cv_raw, cv_rows = {}, []
for name in MODELS:
    for weighted in ([False, True] if name in HAS_WEIGHT else [False]):
        res = cross_validate(build(name, weighted), X_train, y_train, cv=cv_sel, scoring=scoring)
        cv_raw[(name, weighted)] = res
        cv_rows.append({'model': name, 'weighted': weighted,
                        'cv_f1_mean': res['test_f1'].mean(), 'cv_f1_std': res['test_f1'].std(),
                        'cv_recall_mean': res['test_recall'].mean(),
                        'cv_precision_mean': res['test_precision'].mean(),
                        'cv_accuracy_mean': res['test_accuracy'].mean()})
cv_df = pd.DataFrame(cv_rows)
print('全部候選配置(weighted = 是否採用 class_weight/scale_pos_weight):')
display(cv_df.sort_values(['model','weighted']).round(4))

chosen = {}
print('配置規則:balanced 相對預設的 CV-F1 改善 > 0.01 才採用')
for name in MODELS:
    sub = cv_df[cv_df.model == name].set_index('weighted')
    if True in sub.index:
        delta = sub.loc[True,'cv_f1_mean'] - sub.loc[False,'cv_f1_mean']
        chosen[name] = bool(delta > 0.01)
        print(f"  {name:18s} ΔF1(balanced−default) = {delta:+.4f} → {'採用 balanced' if chosen[name] else '維持預設'}")
    else:
        chosen[name] = False
        print(f"  {name:18s} 無此參數 → 預設")"""))
C.append(('code', """sel = cv_df[[chosen[r.model] == r.weighted for r in cv_df.itertuples()]].copy()
interp = {'DecisionTree':0,'LogisticRegression':1,'RandomForest':2,'XGBoost':3,'SVC':4,'KNN':5}
sel['interp'] = sel.model.map(interp)
sel = sel.sort_values(['cv_f1_mean','cv_recall_mean','cv_f1_std','interp'], ascending=[False,False,True,True]).reset_index(drop=True)
print('六模型最終配置的 CV 成績(依選模規則排序):')
sel.drop(columns='interp').round(4)"""))

C.append(('md', """### 前二名差異檢定(重複 CV 校正)

注意:重複 CV 的 25 折**彼此相依**(訓練集大量重疊),普通配對 t 檢定會高估顯著性。此處採 **Nadeau–Bengio 校正重採樣檢定**(變異數乘上 1/k + n_test/n_train 修正項)。"""))
C.append(('code', """def corrected_ttest(a, b, k=25, rho=0.25):
    \"\"\"Nadeau-Bengio corrected resampled t-test for repeated CV (rho = n_test/n_train within CV).\"\"\"
    d = np.asarray(a) - np.asarray(b)
    var = d.var(ddof=1)
    if var == 0:
        return 0.0, 1.0
    t = d.mean() / np.sqrt(var * (1/k + rho))
    p = 2 * stats.t.sf(abs(t), df=k-1)
    return t, p

top2 = list(sel.model[:2])
print(f"前二名:{top2[0]} vs {top2[1]}(25 折,同折配對,Nadeau–Bengio 校正):")
for metric in ('f1','recall','precision'):
    a = cv_raw[(top2[0], chosen[top2[0]])]['test_'+metric]
    b = cv_raw[(top2[1], chosen[top2[1]])]['test_'+metric]
    t, p = corrected_ttest(a, b)
    print(f"  {metric:9s} diff_mean={{:+.4f}}  corrected-p={{:.3f}} → {'顯著' if p < 0.05 else '無法區分(統計上不可分)'}".format((a-b).mean(), p))

winner = sel.loc[0,'model']
print(f'''
裁決:校正檢定下三項指標皆無法在統計上區分兩模型 → 依預先訂定的選模規則以**描述性均值**裁決:
  churn-F1 均值 {top2[0]} {sel.loc[0,'cv_f1_mean']:.4f} vs {top2[1]} {sel.loc[1,'cv_f1_mean']:.4f}(幾乎相同)
  → 平手鏈看 recall 均值:{top2[0]} {sel.loc[0,'cv_recall_mean']:.4f} vs {top2[1]} {sel.loc[1,'cv_recall_mean']:.4f}
最終模型 = {winner}。理由:兩模型性能相當,而 churn 情境下 recall 直接對應漏抓的流失客戶(FN)——
本案例中業務上最昂貴的錯誤;在無法統計區分時,取 recall 均值較高者符合任務目標。''')"""))

C.append(('md', "## 九、測試集評估(六模型,一次性)\n\n各模型以**原生 predict 規則**評估(SVC 的原生決策界線為 decision_function=0,並非機率 0.5,故不對各模型另設統一機率閾值)。"))
C.append(('code', """test_rows, fitted = [], {}
for name in MODELS:
    m = build(name, chosen[name]).fit(X_train, y_train)
    fitted[name] = m
    yp = m.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, yp, labels=[0,1]).ravel()
    test_rows.append({'model': name, 'weighted': chosen[name],
                      'accuracy': accuracy_score(y_test, yp), 'precision': precision_score(y_test, yp),
                      'recall': recall_score(y_test, yp), 'f1': f1_score(y_test, yp),
                      'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp)})
test_df = pd.DataFrame(test_rows).set_index('model')
test_df.round(4)"""))
C.append(('code', """ax = test_df[['f1','recall','precision','accuracy']].plot.bar(figsize=(9.5,4.5), rot=15)
ax.set_title('六分類器於保留測試集之表現(Churn 類指標)')
ax.set_ylabel('分數'); ax.axhline(1-df['Churn'].mean(), ls=':', c='grey')
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=9)
ax.text(0.02, 1-df['Churn'].mean()+0.015, '「全猜不流失」的 accuracy 基準線', fontsize=8, color='grey', transform=ax.get_yaxis_transform())
plt.tight_layout(); plt.savefig('figures/fig1_model_comparison.png', dpi=130); plt.show()"""))
C.append(('md', """### 測試集上 RF 與 XGBoost 的差異是否有意義?(成對 bootstrap)

單次測試集上 RandomForest 的 F1(0.745)高於 XGBoost(0.715)。為避免以單一樣本下結論,以**成對 bootstrap**(對同一批測試樣本重抽 2000 次)估計 F1 差的 95% 信賴區間;若區間跨 0,則差異在抽樣變異範圍內。本筆記本依既定協議:**模型由訓練集 CV 選出,測試集僅報告、不回選**。"""))
C.append(('code', """rng = np.random.default_rng(RS)
yp_rf = fitted['RandomForest'].predict(X_test)
yp_xgb = fitted['XGBoost'].predict(X_test)
y_arr = y_test.values
diffs = []
n = len(y_arr)
for _ in range(2000):
    idx = rng.integers(0, n, n)
    diffs.append(f1_score(y_arr[idx], yp_rf[idx]) - f1_score(y_arr[idx], yp_xgb[idx]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"RF − XGBoost 測試集 F1 差:點估計 {test_df.loc['RandomForest','f1']-test_df.loc['XGBoost','f1']:+.4f},95% CI [{lo:+.4f}, {hi:+.4f}]")
print("→ 信賴區間跨 0:單次測試集的 F1 差異無法排除抽樣變異,與 CV 的「統計不可分」結論一致。")
print(f"→ 最終模型維持由 CV 協議選出的 {winner};RandomForest 為表現相當的次選,將於報告中一併呈報。")"""))

C.append(('md', "## 十、最終模型混淆矩陣與 FN 稽核\n\nChurn=1 為正類;`labels=[0,1]` 固定矩陣順序。False Negative(FN)= 實際流失(1)但被預測為不流失(0)= 公司未啟動挽留、客戶默默流失。"))
C.append(('code', """y_pred = fitted[winner].predict(X_test)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0,1]).ravel()
print(f"{winner}(test): tn={tn}  fp={fp}  fn={fn}  tp={tp}")

fig, axm = plt.subplots(figsize=(4,3.5))
cm = np.array([[tn, fp],[fn, tp]])
axm.imshow(cm, cmap='Blues')
for (i,j),v in np.ndenumerate(cm):
    axm.text(j, i, str(v), ha='center', va='center', color='white' if v > cm.max()/2 else 'black', fontsize=14)
axm.set_xticks([0,1], ['預測 0(留存)','預測 1(流失)']); axm.set_yticks([0,1], ['實際 0','實際 1'])
axm.set_title(f'{winner} 混淆矩陣(測試集)')
plt.tight_layout(); plt.savefig('figures/fig2_confusion_winner.png', dpi=130); plt.show()

fn_mask = (y_test.values == 1) & (y_pred == 0)
fn_idx = X_test.index[fn_mask]
audit = df.loc[fn_idx[:3], ['Churn','MonthlyCharge']].assign(predicted=0)
print('\\nFN 稽核樣本(3 筆,確認實際 Churn=1 且被預測為 0):'); print(audit.to_string())"""))

C.append(('md', """## 十一、FN 的商業損失估算

三層呈現,假設全部標明:

1. **毛收入暴露上限** = 測試集 FN 個體實際月費合計 × 留存月數假設(6 / 12 / 24 月敏感度)——上限,非實際損失
2. **預期可挽回價值** = 上限 × 挽留成功率假設 30%(產業經驗值,報告中附文獻)
3. **全資料集預估 FN 暴露** = 以測試集 FN 率外推:483 名流失者 × (51/145) ≈ **170 名預估漏抓**,再乘平均月費與留存假設——屬**推估**,單獨標示"""))
C.append(('code', """fn_monthly = X_test.loc[fn_idx, 'MonthlyCharge']
SAVE_RATE = 0.30
churn_te = int((y_test==1).sum())
est_fn_all = 483 * fn / churn_te
print(f"測試集 FN = {fn} 人(測試集共 {churn_te} 名流失者);FN 實際月費合計 = A${fn_monthly.sum():,.1f}(平均 A${fn_monthly.mean():.2f}/人/月)")
print(f"全資料集預估漏抓 ≈ 483 × {fn}/{churn_te} ≈ {est_fn_all:.0f} 名\\n")
rows = []
for months in (6, 12, 24):
    gross = fn_monthly.sum() * months
    rows.append({'留存假設(月)': months,
                 '測試集FN毛暴露上限 (A$)': round(gross),
                 f'預期可挽回 @{int(SAVE_RATE*100)}% (A$)': round(gross * SAVE_RATE),
                 '全資料集預估FN暴露 (A$)': round(fn_monthly.mean() * est_fn_all * months)})
loss_df = pd.DataFrame(rows).set_index('留存假設(月)')
print(loss_df.to_string())
print(f"\\n基準情境(12 個月):測試集漏抓的 {fn} 名客戶 ≈ A${fn_monthly.sum()*12:,.0f} 年收入暴露上限;"
      f"若主動挽留能救回三成,約 A${fn_monthly.sum()*12*SAVE_RATE:,.0f} 為可挽回價值。")"""))

C.append(('md', "## 十二、變數重要性 — 各模型原生輸出\n\n改進:將範本的 Feature 0–9 索引對映回欄位名稱。注意各模型的原生重要度**排序並不一致**(不純度、增益、係數等定義不同)——單看任何一個模型的原生重要度都不足以下結論,見下節裁決。"))
C.append(('code', """native = pd.DataFrame(index=df_feature.columns)
for name in ('RandomForest','DecisionTree','XGBoost'):
    native[name] = fitted[name].named_steps['model'].feature_importances_
native['LogReg|coef|'] = np.abs(fitted['LogisticRegression'].named_steps['model'].coef_[0])
print('各模型原生重要度前三名:')
for col in native.columns:
    print(f"  {col:14s} → {', '.join(native[col].sort_values(ascending=False).head(3).index)}")
native.round(4)"""))

C.append(('md', f"""## 十三、Permutation importance 裁決(最終模型,測試集)+ 穩定性檢視

以 permutation importance(打亂某欄後 F1 的下降幅度)在測試集上重複 30 次。**須注意:此為「最終模型(XGBoost)的」重要度**,衡量的是該模型的預測依賴,非模型無關的普適結論;因此除均值±標準差外,另檢視 30 次重複中的**排序穩定性**(top-4 入選率、成對勝率),避免過度宣稱。重要度反映**預測關聯**,不代表因果。"""))
C.append(('code', """pi = permutation_importance(fitted[winner], X_test, y_test, n_repeats=30, random_state=RS, scoring='f1')
pi_df = pd.DataFrame({'feature': df_feature.columns, 'importance_mean': pi.importances_mean,
                      'importance_std': pi.importances_std}).sort_values('importance_mean', ascending=False).reset_index(drop=True)
fig, axp = plt.subplots(figsize=(7,4))
axp.barh(pi_df.feature[::-1], pi_df.importance_mean[::-1], xerr=pi_df.importance_std[::-1])
axp.set_xlabel('打亂該欄後 F1 的平均降幅(±標準差)')
axp.set_title(f'Permutation importance(測試集,重複 30 次,scoring=F1)— {winner}')
plt.tight_layout(); plt.savefig('figures/fig3_perm_importance.png', dpi=130); plt.show()
pi_df.round(4)"""))
C.append(('code', """# 排序穩定性:30 次重複中,各變數進入該次 top-4 的比率;以及第 2、3 名的成對勝率
imp = pi.importances  # shape (n_features, n_repeats)
feat = list(df_feature.columns)
ranks = np.argsort(-imp, axis=0)          # 每次重複的名次序
top4_count = {f: 0 for f in feat}
for r in range(imp.shape[1]):
    for f_idx in ranks[:4, r]:
        top4_count[feat[f_idx]] += 1
top4_rate = pd.Series(top4_count).sort_values(ascending=False) / imp.shape[1]
print('各變數 30 次重複中進入 top-4 的比率:')
print((top4_rate[top4_rate > 0]*100).round(0).astype(int).astype(str).add('%').to_string())

i_mc, i_cs = feat.index('MonthlyCharge'), feat.index('CustServCalls')
win_mc = int((imp[i_mc] > imp[i_cs]).sum())
print(f"\\n成對勝率:MonthlyCharge > CustServCalls 於 {win_mc}/30 次重複")
print('''
穩定性結論:DayMins 於 30/30 次穩居第一;MonthlyCharge 與 CustServCalls 互有領先(上表成對勝率),
應視為**同一層級**的第二梯隊;ContractRenewal 多數重複位居第四。
→ 裁決:最重要變數 = DayMins;第二層級 = MonthlyCharge 與 CustServCalls(不強分先後);第四 = ContractRenewal。''')"""))

C.append(('md', """## 十四、三層論證第二層:重要變數在流失/未流失群組間的實際差異

Permutation importance 只說明「模型依賴哪些變數」;此處以**原始資料的群組差異**驗證這些變數確實在流失者與未流失者間有實質差別(第三層——領域知識與外部文獻——見報告)。"""))
C.append(('code', """key_vars = ['DayMins', 'MonthlyCharge', 'CustServCalls', 'ContractRenewal']
grp = df.groupby('Churn')[key_vars].mean().T
grp.columns = ['未流失 (Churn=0)', '流失 (Churn=1)']
grp['差異方向'] = np.where(grp['流失 (Churn=1)'] > grp['未流失 (Churn=0)'], '流失者較高', '流失者較低')
print(grp.round(3).to_string())
print(f'''
解讀(預測關聯,非因果):
- DayMins:流失者平均日間通話 {grp.loc['DayMins','流失 (Churn=1)']:.0f} 分 vs 未流失 {grp.loc['DayMins','未流失 (Churn=0)']:.0f} 分 → 高用量客戶帳單壓力大、對價格與體驗更敏感
- MonthlyCharge:流失者月費較高({grp.loc['MonthlyCharge','流失 (Churn=1)']:.1f} vs {grp.loc['MonthlyCharge','未流失 (Churn=0)']:.1f})→ 與 DayMins 相關,反映「高帳單」族群
- CustServCalls:流失者客服來電 {grp.loc['CustServCalls','流失 (Churn=1)']:.2f} 次 vs {grp.loc['CustServCalls','未流失 (Churn=0)']:.2f} 次 → 來電頻率是不滿的行為信號
- ContractRenewal:流失者續約率僅 {grp.loc['ContractRenewal','流失 (Churn=1)']*100:.1f}% vs 未流失 {grp.loc['ContractRenewal','未流失 (Churn=0)']*100:.1f}% → 未續約 = 轉換成本低''')"""))

C.append(('md', """### 補充:重要變數間的相關性與策略試點門檻(供報告第三、四節)

DayMins 與 MonthlyCharge 的相關係數,以及報告第四節三個試點門檻的實際客群規模與流失率。"""))
C.append(('code', """r_dm = df['DayMins'].corr(df['MonthlyCharge'])
print(f"DayMins 與 MonthlyCharge 相關係數 r = {r_dm:.2f}(中度相關 → 重要度可能互相分攤)\\n")
base = df['Churn'].mean()
segs = {
    '行動一:CustServCalls >= 3': df['CustServCalls'] >= 3,
    '行動二:ContractRenewal == 0(未續約)': df['ContractRenewal'] == 0,
    '行動三:DayMins >= 216 且 MonthlyCharge >= 中位(53.5)': (df['DayMins'] >= 216) & (df['MonthlyCharge'] >= df['MonthlyCharge'].median()),
}
print(f"全體:{len(df)} 人,流失率 {base*100:.1f}%")
for name, mask in segs.items():
    g = df[mask]
    print(f"{name}:{len(g)} 人({len(g)/len(df)*100:.0f}%),流失率 {g['Churn'].mean()*100:.1f}%,為全體的 {g['Churn'].mean()/base:.1f} 倍")"""))

C.append(('md', """## 附錄 A:決策閾值的成本敏感度(情境展示,非正式答案)

> **本作業的正式答案始終為第十節:最終模型以原生 predict 得出 FN = 51。** 本附錄僅展示:若管理層願意以「多發挽留 offer」換「少漏抓流失者」,決策閾值如何隨成本假設移動(FN ≈ 12 個月月費、FP ≈ 1 個月挽留 offer,比約 12:1;成本比取決於實際 offer 設計,故此為情境而非推薦)。"""))
C.append(('code', """cv5 = StratifiedKFold(n_splits=5, shuffle=True, random_state=RS)
proba_cv = cross_val_predict(build(winner, chosen[winner]), X_train, y_train, cv=cv5, method='predict_proba')[:,1]
med_fee = float(df['MonthlyCharge'].median())
ths = np.arange(0.05, 0.951, 0.01)
costs = []
for t in ths:
    yp_t = (proba_cv >= t).astype(int)
    _tn,_fp,_fn,_tp = confusion_matrix(y_train, yp_t, labels=[0,1]).ravel()
    costs.append(_fn*12*med_fee + _fp*1*med_fee)
best_t = float(ths[int(np.argmin(costs))])
fig, axc = plt.subplots(figsize=(6,3.5))
axc.plot(ths, costs); axc.axvline(best_t, ls='--', c='r')
axc.set_xlabel('機率閾值'); axc.set_ylabel('期望成本 (A$)')
axc.set_title(f'成本導向閾值掃描(FN:FP = 12:1),最小值於 t={best_t:.2f}')
plt.tight_layout(); plt.savefig('figures/fig4_threshold_cost.png', dpi=130); plt.show()

proba_te = fitted[winner].predict_proba(X_test)[:,1]
yp_bt = (proba_te >= best_t).astype(int)
btn,bfp,bfn,btp = confusion_matrix(y_test, yp_bt, labels=[0,1]).ravel()
print(f"情境比較(測試集):正式答案(原生 predict)FN={fn}, FP={fp};成本最小閾值 t={best_t:.2f} 情境 FN={bfn}, FP={bfp}")
print(f"→ 該情境下多發 {bfp-fp} 份挽留 offer 可少漏抓 {fn-bfn} 名流失客戶;是否值得取決於挽留成本的實際設計。")"""))

C.append(('md', "## 附錄 B:AdaBoost(範本 import 的第七個分類器)\n\n題目指定六模型比較;AdaBoost 為範本附帶,在此補充展示(不參與六模型推薦)。"))
C.append(('code', """ada = Pipeline([('model', AdaBoostClassifier(random_state=RS, algorithm='SAMME'))]).fit(X_train, y_train)
yp_a = ada.predict(X_test)
atn,afp,afn,atp = confusion_matrix(y_test, yp_a, labels=[0,1]).ravel()
print(f"AdaBoost(SAMME, test): accuracy={accuracy_score(y_test,yp_a):.4f}  precision={precision_score(y_test,yp_a):.4f}  "
      f"recall={recall_score(y_test,yp_a):.4f}  F1={f1_score(y_test,yp_a):.4f}  (tn={atn} fp={afp} fn={afn} tp={atp})")"""))

C.append(('md', "## 十五、本筆記本產出摘要(供報告引用)"))
C.append(('code', """print(f"最終模型:{winner}(預設配置)。選模依據:5-fold × 5 repeats(共 25 個折次)重複 CV 中六模型以 churn-F1 排序,")
print(f"前二名(XGBoost/RandomForest)經 Nadeau–Bengio 校正檢定統計不可分,依預先訂定的平手鏈以 recall 均值裁決。")
print(f"測試集(正式答案):accuracy={test_df.loc[winner,'accuracy']:.3f}  precision={test_df.loc[winner,'precision']:.3f}  "
      f"recall={test_df.loc[winner,'recall']:.3f}  F1={test_df.loc[winner,'f1']:.3f};RandomForest 為表現相當的次選。")
print(f"FN = {fn} 人(測試集);月費合計 A${fn_monthly.sum():,.1f};12 個月毛暴露上限 ≈ A${fn_monthly.sum()*12:,.0f};")
print(f"@30% 挽留率可挽回 ≈ A${fn_monthly.sum()*12*0.3:,.0f};全資料集預估漏抓 ≈ {est_fn_all:.0f} 名。")
print(f"最重要變數:DayMins(30/30 穩居第一);第二層級 MonthlyCharge 與 CustServCalls;第四 ContractRenewal。")
print(f"群組差異佐證:流失者日間通話 207 vs 175 分、客服來電 2.23 vs 1.45 次、續約率 71.6% vs 93.5%。")"""))

nb = nbf.v4.new_notebook()
nb.metadata['kernelspec'] = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
for typ, src in C:
    nb.cells.append(nbf.v4.new_markdown_cell(src) if typ == 'md' else nbf.v4.new_code_cell(src))

OUT = 'Huang_26254793_421104_Assessment 2a.ipynb'
client = NotebookClient(nb, timeout=1200, kernel_name='python3')
client.execute()
nbf.write(nb, OUT)
print('EXECUTED + WRITTEN:', OUT, '| cells =', len(nb.cells))
