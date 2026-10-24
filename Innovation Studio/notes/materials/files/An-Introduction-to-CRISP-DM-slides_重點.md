# CRISP-DM 簡介投影片(An Introduction to the CRISP-DM methodology)— 重點

- **來源**:Canvas file 14041255。單元頁的連結文字是「CRISP-DM 简介.pdf」,實際檔名是 **An-Introduction-to-CRISP-DM-slides.pdf**(1,032,477 B,41 頁,4:3 投影片轉成的 PDF)
- **作者/出處**:Smart Vision Europe(英國 IBM SPSS / SAS 代理商)John McConnell(Services and Implementation)與 Rachel Clinton(Business Development)的網路研討會投影片;PDF 建立於 2016-02-22。內容是英文,課程沒有翻譯。
- **出現位置**:單元一 第二週 →「1.6 項目管理方法論」頁最後的「想了解更多?」延伸閱讀第 1 項(inventory `M352282#10`,slug `1-dot-6-xiang-mu-guan-li-fang-fa-lun`)
- **原檔**:[An-Introduction-to-CRISP-DM-slides.pdf](An-Introduction-to-CRISP-DM-slides.pdf)|文字版:[An-Introduction-to-CRISP-DM-slides.txt](An-Introduction-to-CRISP-DM-slides.txt)(pdftotext -layout;圖表內容在下方依頁面截圖補上)

---

## 0. 一句話

CRISP-DM(Cross-Industry Standard Process for Data Mining,跨產業資料探勘標準流程)把一個預測分析專案拆成 **6 個會反覆循環的階段**;這份投影片用一個「零售商預測首購客戶會不會回購」的完整例子(IBM SPSS Modeler 操作),示範每個階段要做什麼、產出什麼,最後用「當初在業務理解階段訂的成功標準」來判定模型合不合格。

---

## 1. 逐頁內容(繁體整理)

### 開場(第 1–4 頁)
- **p1** 標題頁:An Introduction to the CRISP DM methodology;Smart Vision Europe(A Select International Company)。
- **p2** FAQ:研討會有錄影、投影片可下載、可替同事重開一場、用聊天室發問。(與內容無關)
- **p3** 公司介紹:IBM 與 SAS 的認證合作夥伴,專精 SPSS、SAS 進階分析;團隊每人有 20 年以上預測分析經驗(前 SPSS 團隊)。
- **p4** 三大支柱(3 Pillars,IBM 的分類,適用大多數資料探勘專案):
  | 支柱 | 三個動詞 |
  |---|---|
  | 預測性客戶分析 Predictive Customer Analytics | 獲客 Acquire/成長 Grow/留存 Retain |
  | 預測性營運分析 Predictive Operational Analytics | 管理 Manage/維護 Maintain/最大化 Maximize |
  | 預測性威脅與詐欺分析 Predictive Threat & Fraud Analytics | 監控 Monitor/偵測 Detect/控制 Control |
  
  每個領域都有一個流程/生命週期,以及一連串想要**預測(predict)**和**描繪(profile)**的事件。

### CRISP-DM 總覽(第 5–9 頁)
- **p5 / p9** CRISP-DM 流程圖:6 個方塊順時針排成一圈 → 1. 業務理解 Business Understanding → 2. 數據理解 Data Understanding → 3. 數據準備 Data Preparation → 4. 建模 Modelling → 5. 評估 Evaluation → 6. 部署 Deployment →(回到 1)。
- **p6 KDnuggets 2014 年調查**「你的分析/資料探勘/資料科學專案主要用什麼方法論?」(200 票;括號內是 2014 票數):
  | 方法論 | 2014 | 2007 |
  |---|---|---|
  | CRISP-DM (86) | 43% | 42% |
  | 自己的方法 My own (55) | 27.5% | 19% |
  | SEMMA (17) | 8.5% | 13% |
  | 其他非特定領域 (16) | 8% | 4% |
  | KDD Process (15) | 7.5% | 7.3% |
  | 自己組織的方法 (7) | 3.5% | 5.3% |
  | 特定領域方法論 (4) | 2% | 4.7% |
  | 沒有 None (0) | 0% | 4.7% |
  
  投票者地區:美國/加拿大 45.5%、歐洲 28.5%、亞洲 14%、拉丁美洲 9.5%、其他 2.5%。→ 重點:CRISP-DM 是最多人用的方法論。
- **p7 人員與角色(People and Roles)**,四象限:
  | 角色 | 負責 | 備註 |
  |---|---|---|
  | 業務 Business | 領域知識 Domain、主題專業 Subject Matter、商業面 Commercial | |
  | 分析 Analytical | 方法論 Methodologies、什麼時候用什麼方法 | 包含「資料科學家 Data Scientist」角色 |
  | 數據 Data | 數據管理 Management、結構 Structure、意義 Meaning | 包含「資料工程師 Data Engineer」角色 |
  | 技術 Technology | 系統整合 Integration、開發應用 Building apps、支援部署 | |
- **p8 CRISP 各階段由誰主導**:1 業務理解 → 業務＋分析;2 數據理解 → 分析＋數據;3 數據準備 → 分析＋數據;4 建模 → 分析;5 評估 → 業務＋分析;6 部署 → 技術/分析/業務/數據(全員)。

### 階段 1:業務理解(第 10–16 頁)
- **p10 要做的事**:
  - 弄清楚業務目標,例如:降低流失率(churn)、取得高價值客戶、交叉銷售/向上銷售(cross-sell/up-sell)、防詐。
  - **約定成功標準(success criteria)**,例如:年流失率從 5% 降到 3%。
  - 評估現況;盡可能把業務目標**轉譯成分析目標**;評估成本效益。
  - 清楚知道結果出來後**要怎麼採取行動**(怎麼部署)。
  - 記錄相關資源、限制條件、系統。
- **p11 業務目標範例**:自來水公司想減少污染;線上博弈公司想找出詐欺下注;慈善機構想提高捐款人終身價值;多通路訂閱制雜誌想提高續訂率;地方政府規劃人員想知道某選區明年能否維持;航運公司想找出可能藏有走私品的貨櫃;咖啡零售商想知道調價對需求的影響;醫院想知道每班急診(A&E)要排多少人;網路零售商想提高回購率。
- **p12 實作範例(貫穿全份投影片)**:
  - 零售商想**提高營收與利潤**,方法是提高客戶終身價值(Lifetime Value, LTV);他們認為自己落後競爭對手。
  - 策略之一是**提高回購**;他們認為數位通路客戶的回購率有問題。
  - **成功標準**:有成本限制(激勵回購要花錢)→ **要在全部客戶中挑出 20%,裡面要涵蓋至少 40% 最可能回購的客戶**。
  - **分析上**要:①替每位首購客戶打一個**回購傾向分數(propensity to repurchase)**;②找出回購(或只買一次)的「b」(原文就寫「the b of repurchase」,應是漏字,推測是 drivers/behaviour 驅動因素)。
- **p13 假設(Hypotheses)**:業務與分析團隊一起列出可能影響回購的因素 —— 通路體驗、首購買了什麼商品、首購金額、首購是否促銷品、之後有沒有再給促銷(以及時機)、客戶人生階段、首購時間(月份、星期幾、時段)、配送方式(店取、快遞等)。
- **p14 CRM 的預測分析**:圖是一條「客戶生命週期營收曲線」(先虧損、再獲利、最後下滑),上面標 Attract 吸引 → Grow 成長 → Retain 留存。重點:**客戶生命週期上的任何事件都可以拿來建模預測和描繪**。
- **p15 建模資料視窗 — 流失(Churn)**:a) 用「最後一期(例如上個月)之前」的客戶資料;b) 去對照最後一期已知的行為(流失或留下)來建模。
- **p16 建模資料視窗 — 回購(Repurchase)**:a) 用「首購當下」所知道的客戶資料;b) 去對照首購之後已知的行為(有沒有回購)來建模。

### 階段 2:數據理解(第 17–22 頁)
- **p18 高層次**:找出可能和業務/分析目標有關的資料來源和欄位;看資料結構(schema)與文件;什麼看起來相關?格式是什麼(資料庫、文字檔、Excel…)?欄位名稱(metadata)?**最關鍵:哪一個是對應業務目標的目標欄位(target field)** —— 例如客戶購買、機器故障、營收/利潤/ROI、網站造訪、偵測到 DoS 攻擊、客戶流失。
- **p19 低層次**:探索資料、找欄位之間的模式;用**單變量與雙變量分析(uni-/bi-variate)**,一次看一個或一對欄位,常用視覺化;**檢驗假設**(例如捐款人年齡能否預測捐款金額);**驗證資料**(找出異常);累積理解並指導建模。
- **p20 實作**:用 IBM SPSS Modeler 示範(Modeler 的專案視窗就有 CRISP-DM 六個資料夾)。建一條 Modeler「stream」,從目標欄位 RepeatPurchase 開始。**樣本:225,793 位客戶,約 20% 會回購**(長條圖 FALSE 約 18 萬、TRUE 約 4.5 萬)。
- **p21 稽核以驗證(Audit to Validate)**:檢查要用來建模的欄位,特別找**缺失值、不尋常值、無效值**。截圖是欄位稽核表(欄位、樣本圖、測量類型、最小、最大、平均、標準差),例如 FirstOrderMonth 1–12(平均 7.837)、FirstOrder_OrderValue 0–5,984.3(平均 91.408)、FirstOrder_NumberOfOrderItems 1–83(平均 2.34)、FirstOrder_odate 2006-08-11 至 2011-12-05;Channel、Delivery_Type 是類別欄位。
- **p22 視覺化探索關係**:**堆疊長條圖**證實「某些通路比較會帶動回購」;**網狀圖(web plot)**顯示某些配送方式與促銷也有較高回購率。

### 階段 3:數據準備(第 23–25 頁)
- **p24 要點**:由數據理解來設計這一步;和數據理解加起來**常比預期耗時 —— 有時佔專案 80%**,新專案尤其如此;通常要整合不同來源、彙總(aggregate)、建立複合指標(例如分組變數 band variables、用公式算年化數字與比率);**類似 ETL(Extract–Transform–Load)**。
- **p25 回購例子**:這次拿到的是資料倉儲匯出的單一檔案(常可請 DBA 幫忙做部分或全部資料準備);**多數時候要整合多個檔案/資料表**;假設中的欄位沒全拿到,但可以用 **Derive 節點**自己造一個缺的欄位 —— 「首購星期幾」:公式 `datetime_weekday(FirstOrder_odate)`,欄位名 FirstOrderDayOfWeek(順序型 Ordinal),長條圖顯示星期 6 的筆數最多。

### 階段 4:建模(第 26–28 頁)
- **p27 要點**:嘗試多種建模技術;候選清單在理解階段就先列出 —— **由資料型態決定、受可用工具限制**。兩種風格:a) **假設導向(hypothesis led)**,只放你相信會影響結果的欄位;b) **資料導向(data led)**,一開始放很多欄位再逐步刪減(或讓演算法刪)。**哪個演算法最好,取決於具體資料和問題。**
- **p28 回購例子**:Partition 節點做 **70:30 切分**;Type 節點選輸入欄位(predictors/drivers)和目標欄位(RepeatPurchase);建模節點選 **CHAID 決策樹**。截圖中 Input 欄位包含 FirstOrder_NumberOfOrderItems、Channel、OrderValue、Delivery_Type、odate、Month、Promotion、Title、FirstOrderDayOfWeek 等;Target = RepeatPurchase。

### 階段 5:評估(第 29–31 頁)
- **p29 要點**:**模型一定要用沒看過的資料(unseen data)測試**;通常隨機切成 2(或 3)組,例如 70%:30% —— 1. 訓練(建模)集、2. 測試(保留 holdout)集、3. 評估集。**用業務理解階段約定的成功標準來評估**;常看模型在某個價值標準(例如營收)上的表現。
- **p30 實作**:建好的模型叫「nugget」。可看到:
  - **預測變數重要性(Predictor Importance)**,由高到低:FirstOrderDayOfWeek > FirstOrderMonth > FirstOrder_Promotion > FirstOrder_Delivery_Type ≈ FirstOrder_NumberOfOrderItems > FirstOrder_Channel > Title > FirstOrder_OrderValue(依圖讀出的順序)。
  - **規則/回購輪廓**:Rule 1 for TRUE(6,121 筆;0.704):若 FirstOrderMonth > 9 且 ≤ 10、FirstOrderDayOfWeek > 5、FirstOrder_Promotion = "F"、Title 屬於 Miss/Dr/Mrs/Ms、Delivery_Type 為空值 → 預測會回購。
- **p31 預測準確度(增益圖 gain chart)**:回顧成功標準是「在 20% 客戶中抓到 40% 回購者」;**這個模型在分數最高的 20% 客戶中抓到 56% 回購者** → 超過標準。(圖分訓練與測試兩欄,讀測試欄的 20% 對應 56%。)

### 階段 6:部署(第 32–37 頁)
- **p33 部署(1)**:可以簡單到**一份名單加上預測分數**(例如郵寄名單);也可以複雜到把模型包成程式、嵌入營運系統**即時預測、自動決策**(例如觸發警示);也可以放進「What-if 模擬器」。**要分清楚建模階段和部署階段的模型**:建模階段會建很多模型、試很多選項;部署階段**冠軍模型是固定的**(例如固定形狀的決策樹)。
- **p34 建模資料視窗 — 回購(訓練時)**:用「最後一期之前」的資料,對照已知行為(有沒有回購)。
- **p35 建模資料視窗 — 替新客戶打分數(部署時)**:a) 用只買過一次的客戶**到目前為止**的資料;b) 預測他們回購的可能性。
- **p36 部署實作**:把冠軍模型接進另一條 Modeler stream(NewSinglePurchaseCus… → FirstOrderDayOfWeek → RepeatPurchase 模型 → Filter → Sort → Table),**預測結果常送到資料庫或檔案,或直接送進營運系統**;輸出表是 URN_Customer 與 PropensityToRepurchase(例如 0.733)。
- **p37 部署(2)— 監控**:做得好的話,部署後表現應該和評估時一致,但**其他因素可能介入**;模型要長期使用就要**持續評估(monitoring)**;有些模型保存期限較長;近年有會自我調整的模型(self adapting),但**更常見的是冠軍/挑戰者(champion/challenger)模型或定期更新(model refresh)**。

### 收尾(第 38–41 頁)
- **p38 CRISP-DM 再看一次**:**流程通常是反覆迭代的(iterative)**;圖上除了外圈順時針的黑色箭頭,還有 4 組綠色回頭箭頭:部署 → 評估;評估 → 回到業務理解或數據理解;數據理解 → 業務理解;數據準備 → 數據理解(做到後面發現問題,可以退回前面階段重做)。
- **p39 執行預測專案總結**:
  - 預測分析專案**比較像研發(R&D)專案**:我們做得出成功的模型嗎?有人做過嗎?達不到目標的風險多大?
  - **所以專案可能失敗**。
  - 不只是分析師的事:大專案通常需要更大的跨領域團隊。
  - CRISP-DM 每個階段都有詳細的任務和產出(作者網站有更多細節)。
- **p40–41** 廠商自我推銷與聯絡方式(訓練課程、顧問等),與內容無關。

---

## 2. 和課程頁(單元一 1.6)對照

| 課程頁 1.6 的說法 | 這份投影片補充了什麼 |
|---|---|
| 六階段:業務理解、數據理解、數據準備、建模、評估、部署 | 每階段的具體任務清單＋一個完整的零售回購案例 |
| CRISP-DM 以迭代方式實施 | p38 的回頭箭頭圖 |
| 常見錯誤「缺乏明確性」(業務目標與成功指標沒想清楚) | p10、p12:成功標準要在一開始就**量化**(40% / 20%),p31 再拿來驗收 |
| 常見錯誤「盲目移交給 IT 團隊」 | p7–p8 角色分工:部署階段需要技術/分析/業務/數據全員參與 |
| 常見錯誤「未能進行迭代」(模型會老化) | p37 監控、champion/challenger、model refresh |

---

## 3. 這份資料在課程哪裡用得到

- **單元一 1.6 項目管理方法論**:延伸閱讀第 1 項;課程頁只列六階段定義,這份投影片是唯一有完整案例的 CRISP-DM 教材。
- **單元一第二週其他頁**:1.7 理解業務情境、1.8 界定業務問題範圍、1.10 **定義成功標準**(p10、p12、p31 是很好的成功標準示範)、1.11 項目規劃。
- **AT2 數據分析專案計畫與設計(30%)**,範本各節可直接對應:
  | AT2 範本章節 | 對應的 CRISP-DM 階段/投影片頁 |
  |---|---|
  | 背景、業務目標 | 業務理解 p10–p13(業務目標 → 成功標準 → 假設) |
  | 分析目標和任務 | p10「轉譯成分析目標」、p12「打回購傾向分數」 |
  | 數據與資源 | 數據理解 p18–p22(目標欄位、稽核缺失/異常/無效值、探索關係) |
  | 分析方法 | 建模 p27(假設導向 vs. 資料導向;依資料型態選演算法) |
  | 實驗與評估方法 | 評估 p29–p31(訓練/測試/評估切分;用成功標準驗收;增益圖) |
  | 實施設計、時間表 | p24「資料準備可能佔 80% 時間」→ 排時程要留足 |
  | 風險管理 | p39「預測專案像研發,可能失敗」 |
- **AT3 專案分析報告(40%)**:範本有「部署計劃 Deployment plan」一節 → 用 p33–p37(名單 vs. 嵌入系統、固定冠軍模型、監控、champion/challenger、model refresh)。評分中「業務影響＋部署計畫＋發現與建議」佔 30 分。
- **單元六(第 10–11 週)評估與部署**:目前未開放,但 p29–p37 就是同一主題的入門版。
- 搭配:[技术目标检查清单_重點.md](技术目标检查清单_重點.md) —— p12 的「20% 客戶抓 40% 回購者」正好示範技術目標清單要求的「指標＋目標值＋評估數據」。
