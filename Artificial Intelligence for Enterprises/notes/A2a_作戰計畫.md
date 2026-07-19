# A2a 作戰計畫(2026-07-19;截止 7/26 23:59 雪梨,佔 20%)

> 題目與 rubric 原文:[A2a_題目與rubric.md](A2a_題目與rubric.md)。本檔 = 怎麼打。

## 一、從 rubric 反推的戰略判斷

**配分結構決定時間分配:這題 60% 是「論證與商業寫作」,40% 才是「建模正確性」。**

| 條目 | 分 | 優異 vs 優良的差距(= 我們要多做的事) |
|---|---|---|
| 1 模型評估 | 20 | 差在「**深入**理解性能」+ 正確報告最終模型 → 不只列表格,要解釋為何這樣選(不平衡資料下 accuracy 會騙人 → 看 recall/F1,3.2.4 已排練) |
| 2 FN 識別 | 20 | 差在「**深入**理解損失」→ 不只數 FN 個數,要**量化金額**(FN 數 × 客戶價值 × 假設留存期,假設標明+佐證) |
| 3 最重要變量 | 25 | 差在「**出色**論證」= 老師 Zoom 親自示範的**三層論證**:模型輸出 → 案例/領域解釋 → 外部佐證(引文獻/產業報告,APA 7) |
| 4 策略制定 | 25 | rubric 原文「**完全基於**最重要變量」→ 每條策略開頭直接點名它針對哪個變量,一對一掛鉤;不寫泛泛留客套話 |
| 5 形式 | 10 | 「足以提交高級企業受眾」→ A1 模板(封面+真 TOC+APA 7)+ 這次補**獨立結論**;圖表全進報告,高管不看 notebook |

其他檔次情報:及格地板很高(不及格都給 10~12.5),分數擠在頂部 → 拿分關鍵全在「優異 vs 優良」那一格的形容詞。

## 二、六天工作排程(D1=7/20)

| 天 | 事項 | 產出 |
|---|---|---|
| D1 | 下載兩附件 → `Assessment2a/`;讀課程 notebook 確認「六種模型」清單與代碼慣例;EDA(欄位型別/缺失/極端值/churn 比例/分布圖) | EDA cells + 前處理決策清單(每步附為什麼) |
| D2 | 前處理(encoding/scaling 視模型)→ stratified train/test → **六模型全跑**:accuracy/precision/recall/F1 + 混淆矩陣 | 模型比較總表 + 六張混淆矩陣 |
| D3 | 選最佳模型(業務導向論證:churn 場景 FN 最貴 → 重 recall/F1,非 accuracy)→ FN 計數 → 收入損失估算 | 報告第 1、2 節草稿 |
| D4 | feature importance(內建 importance + permutation importance 交叉驗證)→ 三層論證(找 2–3 篇電信 churn 文獻/產業數據佐證) | 報告第 3 節草稿 |
| D5 | 策略(每條掛一個 top 變量)→ 全文組裝(A1 模板)+ 圖表嵌入 | 報告完整草稿 + notebook Restart & Run All 乾淨版 |
| D6(7/25) | Codex 對抗審查(數字對賬 + rubric 逐條核對)→ 修訂 → 匯出 docx(檔名 `Huang_26254793_421104_Assessment2a`)| 交件包(docx + ipynb) |

## 三、技術要點與地雷

- **六種模型以課程 notebook 為準**(⚠️未下載前推測:LogisticRegression / DecisionTree / kNN / SVM / RandomForest / NaiveBayes 之類)。題目說「应用所有可用模型」= 不自己加花哨模型,量力而行(老師原話)。
- **類別不平衡**:電信 churn 常見 ~14%;split 要 stratify;不炫技上 SMOTE(課程沒教),報 per-class 指標 + 說明就到位。
- **FN 定義寫死**:正類 = 流失(churn);FN = 實際流失但被預測為不流失 → 公司沒挽留 → 收入流失。跟 3.2.4 的方向一致,報告裡放混淆矩陣標注哪格是 FN。
- **損失估算的假設鏈**:FN 數 × 平均月費(從資料集算)× 假設留存月數(引產業佐證)——每個數字有出處,呼應 A1 教訓(6 處漏引註不再犯)。
- **用詞分寸**:feature importance「對預測貢獻最大/與流失高度相關」,不寫「導致流失」(老師:importance ≠ 因果)。
- **報告獨立性**:四節結構照題目;高管讀報告不讀 code;每節都嵌 notebook 產的圖表。
- 引用:外部佐證用 APA 7(文內作者+年份、reference list 懸掛縮排);其餘格式自由但專業。

## 四、分工

- **Agent(我)**:EDA/建模/圖表代碼與 notebook 組裝、兩節草稿與論證素材、文獻蒐集、Codex 驗證線、對 rubric 逐條自查。
- **Kenny**:下載附件(需登入)、在本機跑 notebook(交的必須是自己環境跑出的輸出)、報告定稿的口吻取捨、上傳交件。

## 五、附件實讀後的確認事實(2026-07-19;檔案已入 `Assessment2a/`)

### 資料集 Cellphone1.csv(= "Assessment 2a Cellphone-1.csv")
- **3333 列 × 11 欄,零缺失、零重複列,全數值型** → 前處理重點不在清洗,在「不平衡+尺度」的處理與論證。
- 欄位:Churn(目標)+ AccountWeeks / ContractRenewal / DataPlan / DataUsage / CustServCalls / DayMins / DayCalls / MonthlyCharge / OverageFee / RoamMins。
- **Churn 率 14.49%(483/3333)** → 全猜「不流失」就有 85.5% accuracy = 報告第 1 節「為何不能只看 accuracy」的現成論據。
- 初步相關(|r| 對 Churn):ContractRenewal .26(負)、CustServCalls .21(正)、DayMins .21(正)>> 其餘;流失者畫像:**沒續約、客服電話多(2.23 vs 1.45)、日間通話多(207 vs 175 分)、月費較高** → 第 3 節領域故事的骨架。

### 課程範本 notebook(Assessment_2a_課程範本.ipynb)
- Colab 範本(drive.mount + `pd.read_csv('Cellphone1.csv')`);本機跑要改路徑,其餘可沿用。
- **「六個分類器 import 行」實為 7 個分類器**:KNN / LogisticRegression / SVC / RandomForest+AdaBoost(同一行)/ XGBClassifier / DecisionTree。⚠️報告寫「六種」時要處理這個計數(建議:全跑 7 個,報告註明 import 六行含七個分類器,或以「六類技術」表述)。
- 範本只實跑 3 個:RF(93.6%)、DT(89.1%)、LR(84.2%,**有未收斂警告**);**KNN/SVC/AdaBoost/XGB 留白 = 學生要補的部分**。
- 範本已示範:RF/XGB/DT/LR 的 feature importance(但用 Feature 0–9 索引,報告要對映欄位名)、混淆矩陣 ravel 拆 tn/fp/fn/tp(LR 例:fn=128)→ 第 2 節的計算模式照抄即可。
- 範本缺陷 = 我們的改進點(每項都是第 1 節論證素材):①無 random_state(結果不可重現)②split 無 stratify ③LR/SVM/KNN 無標準化(LR 因此不收斂、SVC/KNN 會吃虧)→ 加 StandardScaler(只對需要的模型)④只看 accuracy → 補 per-class precision/recall/F1 + 混淆矩陣。
- 課程慣例:permutation_importance 已 import 未用 → 我們用它交叉驗證 impurity importance(第 3 節論證加分)。

### 「最重要變量」預判(待正式跑分確認)
範本輸出 + 相關性交叉看:樹系模型一致把 **DayMins** 排第一(RF .216 / DT .225),MonthlyCharge、CustServCalls 居前;XGB 把 DataPlan/ContractRenewal 排前。正式版用固定 random_state + permutation importance 做裁決,報告需說明「不同模型的 importance 排序不同」本身就是發現。
