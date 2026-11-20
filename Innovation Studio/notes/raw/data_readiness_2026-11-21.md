# 資料就緒盤點:能不能訓練、老師講的處理做到哪、能不能接 application(2026-11-21)

> 工單 IS-1121-DATA-READY-A。只讀盤點:沒訓練、沒重跑任何程式、沒算新數字、沒上網。數字都來自 repo 現成檔,證據欄寫「檔:行號」或我實際跑的指令。
> 縮寫:`29` = `Innovation Studio/notes/29_核心目標對應數據_草稿.md`;`20` = `notes/20_雪梨深度分析.md`;`初稿` = `notes/raw/teammate_stanly_AT2_draft_2026-11-19.txt`(L = 行號);`初稿查核` = `notes/raw/teammate_stanly_AT2_draft_check_2026-11-19.md`;`zoom4` = `notes/raw/zoom4_2026-11-19_整理.md`;`syd_w` = `notes/raw/syd_w_inventory_clean_2026-11-14.md`;`syd_b` = `analysis/sydney/syd_b_positioning.py`;`syd_v` = `analysis/sydney/syd_v_model_error.py`。

## 一、一句話結論

- **Q1 能不能直接拿來訓練?** 原始檔(2026-09 期 listings 20,833 列 × 90 欄、評論 829,163 則)可以直接讀來訓練價格模型,而且已經訓練過一次;但「清好的訓練表」和「存好的模型」都不存在,清洗只活在腳本的記憶體裡、而且資料只在 Kenny 的電腦上(`scratchpad/` 被 git 忽略)。評論文字沒有任何處理或標註,還不能訓練。
- **Q2 老師講的處理做到哪?** 缺失值、篩選(縮減)、轉換、取樣、監督式模型、視覺化、分組切分驗證都做過;離群值只有一條規則(>2,000 澳幣);相關係數與熱力圖、聚類、評論前處理、調參都還沒做,而且現在就能開始(除了評論標註要人工)。老師 11/19 沒有講離群值、標準化、特徵工程、訓練/驗證/測試比例(grep 沒命中,見第四節)。
- **Q3 能不能接 application?** T1、T3、T7 的核心運算(同區同房數分組、設施普及率、評論月份指數)已有現成腳本邏輯,可以包成函式;T2 的百分位和模型有結果但模型沒存檔、沒有「輸入一間房就出參考價」的函式;T4–T5 評論方面分析從零開始(只有原始評論文字);T6 只有公式沒有程式。

## 二、現有資料清單

| 資料 | 路徑 | 期別 | 列數/大小 | 原始檔還是處理過 | 證據 |
|---|---|---|---|---|---|
| Inside Airbnb 雪梨 listings | `scratchpad/insideairbnb_sydney/<期別>/data/listings.csv(.gz)` | 2025-12-12 / 2026-03-21 / 2026-06-16 / 2026-09-16 | 20,436 / 13,563 / 20,573 / 20,833 列;2025-12 為 85 欄,其餘 90 欄;2026-09 的 .gz 12.7 MB、.csv 60.8 MB | 原始(官方下載,sha256 對過 manifest) | `ls -la scratchpad/insideairbnb_sydney/*/data`;`syd_w:4-6`、`syd_w:77`;`初稿查核` L61 列(85–90 欄) |
| 雪梨 reviews(含評論全文) | 同上 `reviews.csv(.gz)` | 四期 | 737,733 / 649,874 / 801,398 / 829,163 則(2026-09 的 .csv 230 MB) | 原始;`head` 看到有 `comments` 欄,內含 `<br/>` 這類 HTML 標記 | `head -c 400 .../2026-09-16/data/reviews.csv`(表頭 `listing_id,id,date,reviewer_id,reviewer_name,comments`);數字見 `初稿查核` L25 列 |
| 雪梨 calendar | 同上 `calendar.csv(.gz)` | 四期 | 7,459,152 / 4,950,495 / 7,509,145 / 7,604,045 列(2026-09 的 .csv 277 MB) | 原始;欄位只有 `listing_id,date,available,minimum_nights,maximum_nights`,沒有每日價格 | `head -1 .../calendar.csv`;`初稿查核` L61 列;`syd_z` 檔頭註解(`analysis/sydney/syd_z_calendar_dates.py:1-9`) |
| 區界線 | 同上 `visualisations/neighbourhoods.geojson`、`neighbourhoods.csv` | 四期 | 38 區;geojson 4.27 MB | 原始 | `manifest.tsv`;`syd_w:105`(38 區) |
| listings / reviews 精簡版 | 同上 `visualisations/listings.csv`、`reviews.csv` | 四期 | 2026-09:3.9 MB / 20.4 MB | 原始(官方精簡版),18 個檔我們還沒用到 | `manifest.tsv`;`syd_w:7` |
| 2026-09 listings 的另一份複本 | `scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz`(+`profile.json`) | 2026-09-16 | 12,747,164 bytes,20,833 列 × 90 欄 | 原始(和上面 2026-09 的 .gz 位元組數相同) | `profile.json` 的 source/rows/columns;`ls -la` |
| 雪梨 listings 早期複本 | `scratchpad/airbnb_history_2026-11-11/sydney_*/listings.csv.gz` | 2025-12 / 2026-03 / 2026-06 | 例:2026-03 為 9,036,609 bytes | 原始(重複) | `ls -la scratchpad/airbnb_history_2026-11-11/sydney_2026-03-21` |
| 雪梨評論摘要(舊) | `scratchpad/airbnb_2024_two_cities/sydney_reviews_summary.csv` | 推測是 2026-09 的精簡版 | 20.4 MB | 原始(大小和 `visualisations/reviews.csv` 的 20,407,613 bytes 相同,推測同一檔) | `ls -la` 位元組數比對 |
| 墨爾本四期(不在題目範圍) | `scratchpad/insideairbnb_melbourne/`、`airbnb_2024_two_cities/melbourne_*`、`airbnb_history_2026-11-11/melbourne_*` | 2025-12 / 2026-03 / 2026-06 / 2026-09 | 沒逐檔查大小 | 原始 | `ls`;題目只做雪梨:`29:57` |
| ABS SAL 區域界線 | `scratchpad/abs_sal_2026-11-14/` | 2021 | geojson 兩頁(1.57 MB + 0.75 MB)、`derived/sal_clean.json` 2.4 MB | 原始 + 一份整理過的 json;用途**沒查到**(沒讀 SOURCE.txt) | `ls -la scratchpad/abs_sal_2026-11-14 scratchpad/abs_sal_2026-11-14/derived` |
| 價格模型的預測輸出 | `scratchpad/syd_v_model_error/oof_predictions_6615.csv`(516 KB,6,615 列)、`extremes_24_predictions.csv`(1.1 KB) | 2026-09 | 6,615 + 24 列 | **處理後的結果**(欄位:id、fold、actual、pred_B0/B1/M1/M2),不是訓練表 | `head -c 400 oof_predictions_6615.csv`;`syd_v:96`、`syd_v:98` |
| 外部參考檔(電價、裝修、保險、網路、入境人數、假期…) | `Innovation Studio/refs/external_2026-11-17/`(14 個 PDF/xlsx)、`refs/external_2026-11-18/`(假期 csv 89 KB、ABS Table 11 xlsx 81 KB) | 2025–2026 | 見檔案 | 原始檔,**還沒轉成表**;`refs/external_2026-11-17/` 被 git 忽略 | `ls -la Innovation Studio/refs/external_*`;`.gitignore:264` |
| 酒店資料(別的候選題) | `scratchpad/hotel1107/hotels.csv`(16.9 MB) | — | — | 與本題無關 | `ls -la scratchpad/hotel1107` |
| 清洗後的訓練表(csv / parquet / feather) | 沒有 | — | — | **不存在** | `find . -name "*.parquet" -o -name "*.feather"` 無輸出;`grep -rn "to_csv\|to_parquet\|to_pickle\|joblib.dump\|pickle.dump" Innovation Studio/analysis` 只有 `syd_v:96`、`syd_v:98` 兩處(都是預測輸出) |
| 存好的模型 | 沒有 | — | — | **不存在** | `find` 找 `*.pkl *.joblib *.onnx *.pt` 在 `scratchpad/` 與 `Innovation Studio/` 都無輸出 |

## 三、已經做過的處理與訓練

| 做了什麼 | 哪支程式 | 產出在哪 | 能不能從原始檔重跑 | 證據 |
|---|---|---|---|---|
| 篩到 6,639 套:整套(room_type=Entire home/apt)→ 1–2 房 → 可住 2–4 人 → 最低 1–7 晚 → 有開價(price 欄非空);2026-09 期各步 16,445 → 10,823 → 8,904 → 7,565 → 6,639 | `syd_b` 的 `scope()`(L68)+`prep()`(L98);規則表在 `syd_w`;預期值寫死在 `EXPECT`(L40) | 只輸出彙總到 `notes/raw/syd_b_positioning_2026-11-11.json/.md`,**沒存篩出的表** | 能,前提是 `scratchpad/insideairbnb_sydney/` 還在(`DATA = ROOT/'scratchpad/insideairbnb_sydney'`,L34);`syd_w` 已把四期逐步筆數重算過且對上 | `syd_w:62-65`、`syd_w:77-83`;`syd_b:34`、`syd_b:40` |
| 清洗細節:讀成字串、空白不當缺值;price 去 `$,` 轉數字(要求 >0);床數缺 → 用房間數補 + 缺值旗標;浴室字串解析成數字(缺 → 1.0 + 旗標);設施 JSON 解析成集合;price 取 log 當目標 | `syd_b` `prep()`、`parse_bath()`、`parse_amen()` | 記憶體內,沒落地 | 能 | `syd_b:75-120`(`sed -n 36,121p` 讀的) |
| 離群值:每晚 >2,000 澳幣的 24 間不進模型訓練與主要誤差(6,639 → 6,615);分位數類統計仍用全部 | `syd_b` `EXTREME_CAP`(L45) | 24 間的預測在 `scratchpad/syd_v_model_error/extremes_24_predictions.csv` | 能 | `syd_w:77-83` 最後一列;`syd_v:98`;`20:149`(放回去 M2 MAE 93.4 → 113.5) |
| **E1 參考價試算(MAE 122.5 / 101.7 / 93.4 那張表)**:5 折交叉驗證 6,615 套,B0 全市中位數 122.5、B1 區×房間數中位數 101.7(組內不足 30 間改「同房間數、最近 30 間」)、M1 Ridge 95.7、M2 梯度提升樹 93.4 | `analysis/sydney/syd_b_positioning.py`(`run_cv` L231;B1 在 L138-151;M1/M2 在 L202-216);`syd_v_model_error.py` 用同一套切法重跑並印出逐房預測 | 數字在 `notes/raw/syd_b_positioning_2026-11-11.json/.md`、`notes/20_雪梨深度分析.md:136-139`;逐房預測在 `scratchpad/syd_v_model_error/oof_predictions_6615.csv` | 能。固定 seed=42(`syd_b:32`);`syd_v` 重跑後 6,615 間結果與既有數字完全一樣(sklearn 1.4.2) | `syd_v_model_error_2026-11-14.md:15-26`(重跑表);`20:136-139` |
| E1 的用到的特徵(M2 共約 50 欄):區、房型細類、緯度、經度、房間數、可住人數、床數、浴室數、最少入住晚數、設施數,加前 40 項設施旗標。**故意不用**:評論數/評分/首評、estimated_occupancy/revenue、availability_*、price_quote_*、房東資料 | `syd_b` `X_tree()`(L180-192)、`FEATURES_ALLOWED`/`FEATURES_BANNED`(L48-57) | — | 能 | `syd_b:48-57`、`syd_b:180-192`;`20:130` |
| E1 的模型:只有 Ridge(alpha=1,先標準化)和 `HistGradientBoostingRegressor`(400 輪、lr 0.05、31 葉、每葉至少 20、l2=1.0,參數寫死,沒有調參);初稿 L72 寫的隨機森林、XGBoost、LightGBM、SHAP **沒跑** | `syd_b` `make_tree()`(L195-199)、`fit_predict()`(L202-216);imports 只有 `HistGradientBoostingRegressor`、`Ridge`、`GroupKFold/KFold`、`StandardScaler`(L26-30) | — | 能 | `syd_b:26-30`、`syd_b:195-199`;`初稿` L72 |
| **模型有沒有存檔:沒有。** 腳本只在每折裡訓練再預測,沒有 `joblib.dump` / `pickle` / `.save`;`syd_b` 內有 `demo(amen)`(L675)和單折示範(L623),但沒落地成檔(內容我沒細讀) | `syd_b` | 沒有 | — | `grep -rn "to_csv\|to_parquet\|to_pickle\|joblib.dump\|pickle.dump\|\.save(" analysis` 只命中 `syd_v:96/98`;`find` 無模型檔 |
| 驗證設計:主要用 GroupKFold(5),同一房東的房源同一折;對照用隨機 KFold(隨機切比分組切低 4.7,偏樂觀);另有「時間外」檢查:用 2026-06 期 6,747 間訓練、猜 9 月新出現 821 間(B0 122.0、B1 103.2、M1 99.3、M2 94.1) | `syd_b` `run_cv`(L231-239)和 d_temporal_check | json/md 同上 | 能 | `syd_b_positioning_2026-11-11.md:47-49`;`20:148`(注意:821 間裡 49.6% 的房東 6 月就出現過,不是沒見過的房東) |
| 同類百分位:B1 的分組(區×房間數)、p25/50/75 附錄例子(1,291 套同類) | `syd_b`(定位表) | `20:277-279` | 能 | `初稿查核` 最後第 2 列(L172 全對) |
| 設施分析:設施數中位數 41、共 2,445 種、最常見 Smoke alarm 96.8% 等;設施與價格的同組比較(只是關聯,不是因果) | `syd_b` 的 `c_amenities`(L533 附近) | `20:108`、`20:122` | 能 | `29:42`;`syd_b:533` |
| 新手房東(年資欄推算)960 間對比;三期變化;跨期差異 | `syd_c_hosts_time.py` | `notes/raw/syd_c_hosts_time_2026-11-11.json` | 能 | `29:43`;`analysis/sydney/syd_c_hosts_time.py:1-8` |
| 評論月份淡旺季指數(2024+2025 兩年平均,11 月最高 135.5、5 月最低 75.3)、每月新上架 | `syd_y_2024_2026.py`(獨立重算腳本 `syd_y_verify.py`) | `20:192-201`;`notes/figures/syd_y_*` | 能 | `20:198`;`初稿查核` L62 月度指數列 |
| 日曆「哪些日子特別滿」(只用 available 與 minimum_nights,沒有價格) | `syd_z_calendar_dates.py` | `notes/raw/syd_z_calendar_dates_2026-11-14.json/.md` | 能(需 calendar 四期 .gz) | `analysis/sydney/syd_z_calendar_dates.py:1-9` |
| 四期資料清點:28 個檔都讀得進、sha256 與 manifest 一致;四期都出現的同一間房 9,879 間;清洗後有價且去高價:0 / 5,898 / 6,747 / 6,615 | `syd_w_inventory_clean.py` | `notes/raw/syd_w_inventory_clean_2026-11-14.md/.json` | 能(數分鐘) | `syd_w:1-12` |
| 獨立重算驗證(非產出者) | `syd_verify.py`、`syd_y_verify.py` | `notes/raw/syd_verify_2026-11-11.md`、`syd_v_verify_2026-11-14.md`、`syd_w_verify_2026-11-14.md` | 能 | `ls notes/raw/`;`20:314-318`(另有只有 Claude 驗過、Codex 沒驗的項目) |

## 四、老師講的處理/運算清單

老師 11/19 講的範圍是 Canvas 第 4 週的概念介紹(描述性/預測性、監督/無監督、資料預處理、聚類、視覺化),大部分是「簡介、細節在學習內容裡」,沒有講到具體做法。我用 grep 搜 `zoom4` 與 `91_上課紀錄.md` 的「離群、標準化、歸一、特徵、訓練集、驗證、測試集、過擬合」:離群、標準化、歸一、訓練集、驗證集、測試集**零命中**;「特徵」只在 `91` 命中「數據分析的特徵」(不是機器學習特徵);「訓練」只出現在「用標註好的訓練資料訓練模型」(監督學習的定義)。所以下表沒有這幾項,不替老師補話。

| 老師講的項目 | 出處 | 我們的狀態 | 缺什麼 |
|---|---|---|---|
| 資料預處理可用在 AT2 處理原始資料;處理缺失、有雜訊、不一致的資料;清洗/集成/轉換/縮減 | `zoom4:50`、`zoom4:208-209`(〔00:20:18〕–〔00:21:31〕);`91:319` | **已做(部分)**:缺失(床數、浴室補值+旗標)、篩選縮減(20,833 → 6,639)、轉換(log price、設施旗標)、四期集成(9,879 間四期都在)。**還缺**:`syd_w` 列了 11 項「建議但沒做」(價格 0/負、人數與房數對不上、`amenities` 寫成 `[]` 要不要當缺值、座標檢查、重複上架…) | 缺失率與異常值的檢查表(`syd_w` 的建議 1–11);評論文字的雜訊處理(HTML 標記 `<br/>`、語言) |
| 平滑雜訊(例:清洗裡怎麼處理缺失、怎麼平滑雜訊) | `zoom4:208`(〔00:21:13〕) | **沒做** | 價格是掛牌價、沒有平滑需求;評論月份指數沒平滑(只是兩年平均)。要不要做,小組沒決定 |
| 資料取樣(「你們可以取樣取一部分資料」);結果不理想對作業沒影響,但用到實際可能有問題 | `zoom4:152`(〔01:09:03〕);`91:252` | **已做**:我們用的是篩選後子集(6,639),不是隨機抽樣;評論還沒抽樣 | 評論若要標註只能抽樣(初稿 E2 設計 300 條),抽樣方法與分層比例還沒定 |
| 監督式學習:用標註好的訓練資料訓練模型 | `zoom4:201`(〔00:18:03〕) | **已做**:價格預測(Ridge、梯度提升),目標是掛牌價,有現成真值 | 評論方面分類沒有標註資料(見第六節) |
| 無監督(K 均值、層次聚類、Apriori、PCA)、K 最近鄰是監督不是聚類 | `zoom4:203-204`(〔00:18:55〕〔00:19:16〕) | **沒做**:沒查到任何聚類/PCA 程式(`analysis` grep 無 KMeans);T1 現在是規則分組,不是聚類 | **現在就能開始**:用 `listings` 的區、房間數、人數、設施旗標做聚類來找「同類」,資料已夠;要跑才知道結果 |
| 資料聚類:硬/軟聚類、相似性與距離、選算法的標準 | `zoom4:212`(〔00:22:15〕–〔00:23:06〕) | 部分:T1 設計用 Jaccard 相似度(初稿 L71),B1 退回規則用經緯度最近 30 間(`syd_b:138-151`) | Jaccard 排序與 10–20 套名單還沒寫(`初稿查核`:Jaccard「找不到」) |
| 資料視覺化:圖表/表格/圖示;說明性 vs 探索性;條形圖、直方圖、散點圖、熱力圖、折線圖 | `zoom4:221-223`(〔00:23:17〕–〔00:29:04〕) | **已做**:matplotlib 圖在 `notes/figures/`(定位、設施、MAE、散點、淡旺季…);腳本 `syd_b:243-340` 有 `fig_*`。**還缺**:熱力圖 | 熱力圖 |
| 熱力圖可呈現資料之間的相關性 | `zoom4:223`(〔00:28:56〕);`91:320` | **沒做**:初稿 L63 寫「【待补:相关系数矩阵和热力图,计划第 4 周完成后插入】」;`analysis` 內只有 `np.corrcoef`(評論月份兩年指數的相關)與 Spearman(品質檢查),沒有欄位間相關矩陣 | **現在就能做**:欄位都在 `listings`(價格、bedrooms、accommodates、設施數、`review_scores_*`)。注意相關係數用掛牌價、評分擠在接近滿分(`29:42`) |
| 表格比圖表適合精確數值;資料值差異過大無法統一刻度時用表格 | `zoom4:224`(〔00:29:37〕–〔00:30:08〕) | 已做(報告用表) | — |
| 好的視覺化(易懂、清晰、一致…);工具 Matplotlib/Seaborn/Plotly/Tableau/Power BI | `zoom4:231-232`(〔00:31:45〕–〔00:33:06〕) | 已做(Matplotlib) | — |
| AT3 第 8 週起學「分析解決方案開發、超參數調優」,第 10–11 週學評估與部署 | `91:130` | **還沒到**:我們的 HistGradientBoosting 參數寫死(`syd_b:195-199`),沒調參 | 調參與最終模型的選擇;目前候選 RF/XGBoost/LightGBM/SHAP 只寫在初稿 L72,沒跑 |
| AT3 的「系統」可以是原型或機器學習模型;可以做 demo,預期成果就寫 demo | `91:129`;`zoom4:322`(〔01:10:43〕) | 小組要自己投票決定 demo 還是真系統(對話中「組內投票」,學生語) | 決定 |
| (老師沒講,但初稿用了)按房東分組切分、時間外驗證 | — | 已做(第三節) | 沒有獨立的 test set 與調參分開;現在是交叉驗證分數直接當結果(推測:對作業夠用,AT3 要不要拆開沒查到老師要求) |

## 五、application 七個功能 T1–T7

(初稿 L43–L49 的 T1–T7;方法 L70–L93)

| 功能 | 需要的資料 | 需要的運算或模型 | 現況:可直接接/要補 | 要補什麼 |
|---|---|---|---|---|
| T1 同類匹配 | `listings`:區(`neighbourhood_cleansed`)、`room_type`、`bedrooms`、`accommodates`、`amenities`、經緯度 | 區×房間數分組;不足 30 間退回「同房間數最近 30 間」;組內按人數和設施 Jaccard 排序,回 10–20 套 | **要補(核心邏輯已有一半)**:分組與 30 間退回已在 `syd_b:138-151`(`b1_predict`,但是為了預測價格、輸出的是價格中位數,不是競品名單);Jaccard、名單、匹配理由沒寫 | 把 `b1_predict` 的分組改成「回名單」的函式;寫 Jaccard;E3(隨機抽 50 套、兩人判斷是否可比)還沒做 |
| T2 價格定位與參考價 | 同上 + `price`(掛牌價) | 同類 p25/50/75 + 目標房源百分位;參考價模型(M2 已訓練一版,MAE 93.4) | **部分可接**:百分位邏輯有(`20:277-279` 附錄例);模型有結果但沒存檔、沒有「輸入一間房 → 參考價」的函式 | 模型存檔或在 app 啟動時用 6,615 間重訓(`syd_b` 可重跑);把使用者輸入轉成 `X_tree` 的欄位(含前 40 項設施旗標);RF/XGBoost/LightGBM/SHAP 初稿 L72 寫了但沒跑;價格是掛牌價,UI 要寫明 |
| T3 設施差距 | `amenities`(同類房源全部設施) | 同類每項設施普及率;普及 ≥80% 而目標房源沒有的列出 | **可直接接**:設施解析與普及率已有(`syd_b` `parse_amen`/`amen_counts`;`20:108-122`);「≥80%」門檻是新設計,repo 沒有(`初稿查核` L73 列「找不到」) | 設施名稱 2,445 種的同義合併(推測需要;`20:108` 只提到 2,445 種,沒提合併);「裝了不等於漲價」要在 UI 註明(`29:42`) |
| T4 評論方面級情感分析 | `reviews.csv` 的 `comments`(2026-09 期 829,163 則)、`listing_id` 連回 listings | 方面抽取 + 正負情感(初稿:LLM;基準 VADER、Sentence-BERT) | **要補(從零)**:沒有任何評論程式;`grep -rn "VADER\|sentiment\|comments" analysis` 無命中(只有 `reconcile_verify_2026-11-12.py:87` 讀 `listing_id,date` 兩欄) | 評論清洗(HTML、語言);抽樣與雙人標註 300 條(E2);LLM 呼叫(成本沒估);按房源彙總 |
| T5 改進優先級與避坑清單 | T4 的結果 + `review_scores_*`(accuracy、cleanliness、checkin、communication、location、value,欄位都在 listings) | 把方面情感和分項評分合成優先級;評論 <5 條提示證據不足 | **要補(依賴 T4)**:分項評分欄位存在(`profile.json` 欄名),但現有分析只用總分 `review_scores_rating`(`29:42`、`20:70-74`);評分擠在接近滿分(`29:42`) | T4 完成後才能做;合成規則沒設計 |
| T6 收入情景(低/中/高) | `price`、`estimated_occupancy_l365d`、成本參考(電、網路、保險、市政)、服務費 3% / 15.5%、180 天上限 | 年收入 = 價格 × 估算入住晚數 ×(1−服務費)− 成本;價格與入住取同類分位 | **要補**:公式只在初稿 L75,沒有程式(`grep "180" analysis` 無相關命中);入住晚數是用評論推算(中位數 60、0 晚占 12.4%、達上限 255 晚占 6.4%,`29:44`),沒有真值可驗;成本參考只是下載來的 PDF/xlsx 原檔,沒轉成表 | 把外部數字抄成一張小表(附來源日期);寫公式函式;表上要寫「估計不是帳務」(`29:73`) |
| T7 淡旺季與高需求日期 | `reviews.csv` 的 `date`;calendar 的 `available`;公眾假期 csv(2021–2025,沒有 2026);NSW 入境人數 xlsx | 評論月份指數、日曆「特別滿」的日子;假期對照 | **部分可接**:月指數(`syd_y`)與日曆日期(`syd_z`)都有程式和結果;初稿 L75 說「列出假期、活動」 | 2026 的假期表沒有(`29:43`);活動資料(TODO 提到的 Ticketmaster)沒查到已取得;評論月份只是需求方向、只含 2026-09 還在架的房源(`20:202`、`29:75`);日曆「不可訂」分不出已訂與房東關閉(`初稿` L65) |

## 六、卡住的地方

| 卡住的地方 | 證據 |
|---|---|
| 沒有實際入住與成交價:價格是掛牌價、入住晚數與收入是由評論推算的代理;日曆沒有每日價格;「不可訂」分不出已訂或關閉。T2 的誤差衡量的是「猜中別人掛多少」,不是「定多少訂得出去」 | `初稿` L65;`29:72-73`;`20:144`;calendar 欄位 `listing_id,date,available,minimum_nights,maximum_nights` |
| 評論沒有人工標註:E2 設計「兩人獨立標註 300 條」,沒查到任何已標註檔或標註指引 | `初稿` L81;`grep -rn "標註" notes/20_雪梨深度分析.md notes/17_定題與三層目標_v1.md notes/raw/syd_w_inventory_clean_2026-11-14.md` 只命中與評論無關的一行(`20:359`) |
| 獨立房間(4,282 間,占 20.6%)還沒分析,全部數字只有整套房 | `20:24`;`29:41`;`初稿查核` 倒數第 2 列(L170) |
| 外部資料只下載了原檔,沒轉成表,而且被 git 忽略;初稿 L64 列的 TfNSW GTFS、OpenStreetMap、短租登記冊 API、NSW 租金報告**沒下載**,其中登記冊、車站距離 Kenny 11/18 已決定不做 | `ls Innovation Studio/refs/external_*`;`.gitignore:264`;`29:60`;`TODO.md:57`;`初稿` L64;`external_downloads_2026-11-18.md:35-37`(8、5、6、7、10、12、13 項沒下載) |
| 資料只在 Kenny 本機:`scratchpad/` 整個被 git 忽略,隊友 clone 後沒有原始檔,腳本讀不到;腳本路徑寫死 `scratchpad/insideairbnb_sydney` | `.gitignore:261`(`/scratchpad/`);`git check-ignore -v scratchpad/insideairbnb_sydney/manifest.tsv` 命中;`syd_b:34` |
| 初稿 L69 說處理層結果「以 Parquet 格式存儲」,但沒有任何 parquet 檔,清洗在每支腳本裡各自重做 | `find . -name "*.parquet"` 無輸出;`syd_w` 的 RULES 表把規則「照抄並註明出處行號」(`syd_w:1-8`) |
| 初稿 L72 的候選方法(隨機森林、XGBoost、LightGBM、SHAP)沒跑;初稿表 3 的基準寫「線性回歸」,但表 4 沒有 M1(Ridge 95.7 已有結果) | `syd_b:26-30`(imports);`初稿` L80、L88-91;`syd_v_model_error_2026-11-14.md:22-25`(M1 95.7) |
| 清洗還有缺口:價格 0/負/過低、人數與房數對不上、`amenities=[]`、座標超界、疑似重複上架、價格含不含清潔費(資料說明沒寫)、2,000 澳幣上限 1 房與 2 房共用一個數字 | `syd_w` 「建議但沒做」第 1–11 項(約 `syd_w:190-215`) |
| 價格只有三期,有價比例 99.4% / 86.5% / 85.1%;2025-12 價格整欄空;三期入住季節不同,不能當成房東調價;2026-03 期房源數只有 13,563 | `29:41`、`29:56`、`29:74`;`初稿` L56-59 |
| 驗證設計的限制:時間外 821 間有 49.6% 房東 6 月就出現過;同房東互相提示(隨機切比分組切低 4.7);誤差 44% 來自最貴兩成房源 | `20:148`;`syd_b_positioning_2026-11-11.md:47`;`初稿查核` L93 列 |
| 相關係數矩陣與熱力圖初稿標「待補」,沒做 | `初稿` L63 |
| 欄位意思沒查完:`hosts_time_as_host_*`(新手定義用它)官方說明沒查到;短租 180 天規定 2025–2026 有沒有修法沒查到 | `29:77`;`20:164`、`20:324` |

## 七、沒查到或沒查完的

- 我沒有重跑任何程式,所以「能重跑」是根據:程式內容、固定 seed、`syd_v` 的重跑報告(`syd_v_model_error_2026-11-14.md:15-26`)、`syd_w` 驗證檔;本次沒有自己驗證。
- `meeting_1118/` 裡的資料盤點(md/json)與 `notes/raw/data_inventory_2026-11-15.md` 沒讀,第二節是靠 `ls` 與 `29`、`syd_w` 交叉得來。
- 每個 listings 欄位的缺失率沒逐欄查(`syd_w` 有部分,我沒全讀);`29:48` 也寫了 `hosts_time_as_host_*`、`license` 填寫率沒查到。
- `scratchpad/abs_sal_2026-11-14/SOURCE.txt` 沒讀,SAL 資料的用途沒查到。
- `scratchpad/airbnb_2024_two_cities/sydney_reviews_summary.csv` 與 `visualisations/reviews.csv` 是否同一檔,只憑位元組數相同推測,沒比對 sha。
- `91_上課紀錄.md` 只用 grep 找關鍵字、讀了命中附近幾行,歷次上課沒逐段讀;`handoff.md` 沒讀。
- `syd_b` 裡 `demo(amen)`(L675)與單折示範(L623)到底輸出什麼,沒細讀。
- 墨爾本的腳本與資料沒看內容(不在題目範圍)。
- 評論檔的語言分布、有多少則是空白或非英文,沒查(沒讀評論文字)。
- 老師在 11/19 之前的歷次上課是否講過離群值、標準化、訓練/驗證/測試切分:`91` grep 沒命中,但 `91` 是整理稿,不是逐字稿,原錄音沒聽。
