# 候選題研究:旅遊/俱樂部/賽事活動＋跨領域(scope IS-T2-travel,2026-10-30)
> 資料連結皆於 2026-10-30 實際打開核對;「(未確認)」=沒核對到,「(推論)」=合理推測。隊員代稱:Kenny／隊友 A(運維總監)／隊友 B(雲端機房運維)／隊友 C(旅遊賽事)。
> 「中國大陸可直連?」欄全是推論(未從大陸實測)。網路請求合計 30 次、下載約 156 MB(皆在上限內)。目標值(如「誤差降 15%」)是提案,不是已知結果。

## V1 雪梨短租 × 大型活動需求雷達(量化活動對各區短租需求的拉抬,再用 LLM 讀評論給行動建議)
- **一句話**:用 Inside Airbnb 雪梨快照加手工整理的活動日程,估算除夕煙火、Vivid 等活動對各區需求的拉抬,並用 LLM 從評論萃取體驗問題,產出給房東與主辦方的行動清單。
- **業務情境**:企業=雪梨短租代管公司(管 50–200 間房,情境假設)或活動接待規劃單位;痛點=活動週定價/排房憑感覺、活動期間負評集中卻沒人彙整。
  - BO1 活動週不漏賺 → AG1 估各活動對各區需求的拉抬幅度 → T1 事件研究(event study)＋需求預測
  - BO2 活動期間少負評 → AG2 找出活動期間評論的主要抱怨面向 → T2 LLM 面向萃取(aspect extraction)
  - BO3 主辦方提早備戰 → AG3 預測下個活動各區的未來訂房緊張度 → T3 預測＋風險排序
  - 成功標準:活動週需求預測誤差(MASE)比季節性基準低 ≥15%;LLM 抱怨分類與人工標註一致率 Cohen's κ ≥0.6;行動清單經 C 評為「可執行」≥70%。
- **資料(2026-10-30 核對)**:基底 B=`https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/`;頁面 https://insideairbnb.com/get-the-data/ 200

| 表格 | 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|---|
| listings | listings.csv.gz | B+listings.csv.gz | 200 | 12.7 MB | 20,833 筆×90 欄;快照 2026-09-17 | CC BY 4.0(get-the-data 頁原文)＋使用政策限制 | 否 | 未確認 |
| calendar | calendar.csv.gz | B+calendar.csv.gz | 200 | 18.4 MB | 7,604,045 筆;2026-09-17~2027-09-16(**未來** 365 天;**沒有價格欄**) | 同上 | 否 | 未確認 |
| reviews | reviews.csv.gz | B+reviews.csv.gz | 200 | 87.3 MB | 829,163 筆;2009-12-05~2026-09-17 | 同上 | 否 | 未確認 |
| 活動日程 | 無官方開放 CSV(搜尋 NSW/Destination NSW 沒找到) | — | — | — | 需 C 手工整理(量級 30–60 場/年,推論) | 各主辦方網站(未確認) | 否 | 未確認 |
- **使用限制(原文,https://insideairbnb.com/data-policies/ 200)**:「Do not republish the data」「download the data once, not each time you run your analysis」「Only take the data you need」「should be attributed and cited appropriately」;歷史資料需另提 Archived Data Request,「use outside the project's mission may be refused or asked to pay」。get-the-data 頁只列出 2026-09-16 一期快照,舊期要申請。
- **重要欄位**:listings=`id, neighbourhood_cleansed, latitude/longitude, room_type, accommodates, price, review_scores_*(6 個子分數), number_of_reviews_ltm, reviews_per_month, estimated_occupancy_l365d`(後者是站方估計值,非真實);calendar=`listing_id, date, available(t/f), minimum_nights`;reviews=`listing_id, date, comments`(多語)。`instant_bookable` 整欄為空(資料品質瑕疵)。
- **EDA 可以看什麼**:
  - 分布 1:價格極右偏——中位數 337.8、p99 3,481.7、最大 96,887.6(欄位為 "$"、雪梨推論 AUD),要取 log 並處理離群。
  - 分布 2:評論量由 2017 年約 1.9k/月升到 2025–26 年 15–22k/月,且 2020-04 只剩 701 筆(COVID 斷層),需先拆趨勢與季節。
  - 相關 1:log(price) 與 accommodates Spearman 0.71、與 location 子分數 0.33、與總評分 0.23;reviews_per_month 與價格幾乎無關(−0.05)。
  - 相關 2(活動訊號):2026-12-31 的「不可訂」比例 66.9%,對比 12-10 的 40.0%;2026-01-01 當日評論 1,477 則,對比 12–1 月日中位數 577。但「不可訂」含房東自行封鎖,不等於被訂走。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 需求預測(每區每日評論量/不可訂率) | 季節性 naive、SARIMA/ETS | Chronos、TimesFM 零樣本;含活動共變數用 TabPFN-TS | MASE;活動週/非活動週分開報 |
| 活動效應量化 | 迴歸加活動虛擬變數 | 同上模型加共變數,比較係數穩定度 | 效應 CI、置換檢定 |
| 評論面向萃取 | TF-IDF＋關鍵字、BERTopic | LLM few-shot 面向萃取(InstructABSA 思路);本地小模型 vs 雲端 API | 200 則人工標註的 micro-F1、κ、每千則成本 |
| 行動建議 | 規則模板 | LLM 生成(附引用評論)＋LLM-as-judge＋C 人審 | 可執行性 1–5 分、judge 與人一致率 |
  - 選擇標準:精度提升是否顯著(配對檢定)、延遲、成本(筆電＋免費額度)、可解釋性、大陸可用性(A 只能跑本地模型)。
  - 文獻:[Chronos: Learning the Language of Time Series](https://arxiv.org/abs/2403.07815)、[A decoder-only foundation model for time-series forecasting(TimesFM)](https://arxiv.org/abs/2310.10688)、[From Tables to Time: Extending TabPFN-v2 to Time Series Forecasting](https://arxiv.org/abs/2501.02945)、[InstructABSA](https://arxiv.org/abs/2302.08624)、[BERTopic](https://arxiv.org/abs/2203.05794)、[Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)(標題皆已用 arXiv API 核對)。
- **AT3 系統長什麼樣**:地圖(區×未來 90 天緊張度)＋活動時間軸;點區看預測帶與「活動期間抱怨 Top 面向」;按鈕「產生房東行動清單」「產生主辦方接待簡報」「匯出 CSV」。Demo:①選「除夕煙火」,看某區預測 vs 基準與不確定區間;②按「產生行動清單」,LLM 引用 3 則原評論,給 3 條含預估影響與信心的行動。
- **4 人分工**:專案管理 Kenny(備 C)｜利害關係人 C(備 Kenny)｜方法論 Kenny(備 B)｜業務理解 C(備 A)｜軟體工程 Kenny(備 B)。Kenny=清理、預測與 LLM 管線、介面;C=建活動日程(來源/日期/規模)、判斷建議可不可行、扮房東訪談;A=部署計畫、風險與成本章節、驗收「現場穩定」;B=資料管線(只下載一次並快取)、部署與監控。**A、B 的主場:弱**(只有部署/管線,運維本業用不上)。
- **風險與備案**:①只有單一快照,calendar 無歷史無價格 → 以評論日期＋未來不可訂率當代理,不談「真實營收」;②活動日程無開放資料 → C 建 ≤40 場並標來源;③「不可再發布」→ repo 不放原檔,只放腳本與下載說明,Kenny 下載後僅隊內共享;④與 Inside Airbnb「房屋與社區」使命有張力 → 報告的社會影響章節要正面處理(活動是否推高房租、擠壓長租供給);⑤舊期快照申請可能被拒 → 備案只用單快照＋評論時間序列。
- **最大缺點**:沒有真實訂單與價格歷史,「需求」全是代理指標,活動與季節的因果切分很難站穩。

## V2 旅客評論 → 體驗改善 Copilot(有星等的評論當標準答案,比較 LLM 與傳統情感模型,再產出改善工單)
- **一句話**:用 Yelp Open Dataset 的旅遊/活動相關商家評論(有星等、有日期),比較傳統情感模型與 LLM 面向情感分析的成本與準確度,並輸出「改善工單＋回覆草稿」。
- **業務情境**:企業=飯店/景點/俱樂部/賽事營運方(情境假設);痛點=評論多到沒人讀,負評原因散落、回覆慢。
  - BO1 縮短發現問題的時間 → AG1 偵測評分/面向突降 → T1 時間序列異常偵測＋LLM 摘要
  - BO2 提升可行動性 → AG2 把評論轉成有優先級的改善項 → T2 面向情感分析(ABSA)
  - BO3 降低回覆人力 → AG3 產生合規回覆草稿 → T3 LLM 生成＋人審
  - 成功標準:星等預測 MAE 與基準相比,每千則成本下降 ≥50% 而 macro-F1 不低於 −2 點;從負評爆量到出工單 <1 天(回放驗證)。
- **資料(2026-10-30 核對)**:

| 表格 | 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|---|
| Yelp Open Dataset | Yelp-JSON.zip(5 個 JSON＋PDF) | https://business.yelp.com/data/resources/open-dataset/ | 頁面可讀(WebFetch,未回碼) | 4.35 GB(展開 8.65 GB;**未下載**) | 6,990,280 則評論、150,346 商家、11 個都會區;時間範圍頁面未載(未確認) | 頁面僅稱「intended for educational use」;完整條款在壓縮包文件/ToS(未確認) | 頁面未見註冊要求(實際下載是否填表未確認) | 未確認 |
| 備案:Disneyland Reviews | Kaggle(第三方描述約 42,000 則,TripAdvisor 來源,月粒度日期) | https://www.kaggle.com/datasets/arushchillar/disneyland-reviews | WebFetch 只拿到標題 | 未確認 | 未確認 | **未確認**;且來源為 TripAdvisor 爬取,條款風險(推論) | 未確認 | 推論:Kaggle 需翻牆 |
- **重要欄位**(依 Yelp 官方文件,本次未打開 JSON,屬推論):review=`stars, date, text, business_id`;business=`categories, city, state, review_count, attributes`。可用 categories 篩出 Hotels & Travel、Active Life、Arts & Entertainment、Event Planning 等子集。
- **EDA 可以看什麼**(下載後才能驗證,以下是計畫):分布 1=星等 J 型分布(正評偏多)；分布 2=評論長度與評論量的長尾(熱門商家 vs 一般商家)。相關 1=評論長度與星等(負評較長?);相關 2=月份/週末與評分、類別與評分。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 星等/情感 | VADER、TF-IDF＋邏輯迴歸 | LLM 零樣本/few-shot(依 Reality Check 論文:LLM 在簡單二元情感強、在細粒度任務未必贏) | macro-F1、MAE、每千則成本與延遲 |
| 面向情感(服務/價格/位置/整潔/等待) | BERTopic＋情感分數 | InstructABSA、LLM 結構化輸出 | 面向 F1(人工標註 200 則) |
| 異常偵測＋摘要 | 滾動 z-score | 基礎模型預測區間(Chronos)＋LLM 摘要突降原因 | 偵測延遲、誤報率 |
| 工單/回覆草稿 | 模板 | LLM＋LLM-as-judge＋C 人審 | 可執行性、語氣、事實一致 |
  - 文獻:[Sentiment Analysis in the Era of Large Language Models: A Reality Check](https://arxiv.org/abs/2305.15005)、[InstructABSA](https://arxiv.org/abs/2302.08624)、[BERTopic](https://arxiv.org/abs/2203.05794)、[Chronos](https://arxiv.org/abs/2403.07815)、[LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)。
- **AT3 系統長什麼樣**:選一個場所→看評分時間線、面向熱圖、Top 抱怨;按鈕「產生改善工單(含優先級)」「產生回覆草稿」「與競品比較」。Demo:①選一家評分近期突降的商家,系統指出「等待時間」面向惡化;②按「產生工單」得到 3 條行動＋引用原評論，再按「回覆草稿」。
- **4 人分工**:專案管理 Kenny(備 A)｜利害關係人 C(備 Kenny)｜方法論 Kenny(備 B)｜業務理解 C(備 A)｜軟體工程 Kenny(備 B)。Kenny=下載 4.35 GB、篩子集、模型比較、介面;C=定義「可行動」與回覆範本、人工標註;A=成本/風險/部署計畫;B=推論服務穩定與成本壓測。**A、B 的主場:弱**。
- **風險與備案**:①Yelp 以美加城市為主(推論),與澳洲/UTS 脈絡脫節;②「僅教育用途」不可商用,子集再分享規則未確認;③4.35 GB 只有 Kenny 下載,篩成 <500 MB 子集再給隊內;④Yelp/情感分類在 NLP 課很常見,「與眾不同」要靠「成本—準確度選型＋工單」而非情感分類本身;⑤備案=改用 V1 的 Inside Airbnb 評論(無逐則星等,但有 6 個子分數可當弱標籤)。
- **最大缺點**:非澳洲、非嚴格旅遊資料,離「與眾不同」最遠,且 A、B 幾乎沒有主場。

## V3 航班延誤/取消 → 旅客通知與改票建議 Copilot(運維 × 旅遊,以重播方式模擬即時)
- **一句話**:用 BTS 班次級資料預測取消與大延誤,對受影響旅客自動產生通知與同日改票方案,並用 BITRE 看澳洲路線的長期趨勢。
- **業務情境**:企業=旅行社/線上旅遊平台/企業差旅公司的客服中心(情境假設);痛點=大面積延誤時電話暴增、通知慢、改票靠人工。
  - BO1 更早通知 → AG1 預測出發前數小時的取消/大延誤風險 → T1 二元分類(含機尾連鎖特徵)
  - BO2 降低改票人工量 → AG2 推薦同起訖、同日、風險較低的替代班次 → T2 檢索＋排序
  - BO3 降低客訴 → AG3 個人化通知(含原因與下一步) → T3 LLM 生成＋審核
  - 成功標準:取消/大延誤預測 PR-AUC 勝過基準 ≥ 5 點;通知中的班次/時間與資料 100% 一致(可自動驗證);改票方案回測「實際準點」比例 ≥ 75%;單則通知產生 <3 秒。
- **資料(2026-10-30 核對)**:

| 表格 | 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|---|
| BTS 準點(月檔) | On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2026_8.zip | https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2026_8.zip | 200 | 32.0 MB(展開 275.8 MB) | 608,389 筆×110 欄;2026-08-01~31;站方稱資料 1987~2026-08(每月一檔) | 公有領域(推論:data.gov 相近 BTS 條目標 Public Domain;TranStats 頁面無條款原文) | 否 | 未確認(美國政府站,可能慢) |
| BTS 欄位頁 | DL_SelectFields | https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr | 200 | — | 「Latest Available Data: August 2026」 | 同上 | 否 | 未確認 |
| BITRE 準點 | otp_time_series_web.csv | https://data.gov.au/data/dataset/29128ebd-dbaa-4ff5-8b86-d9f30de56452/resource/cf663ed1-0c5e-497f-aea9-e74bfda9cf44/download/otp_time_series_web.csv | 200 | 10.2 MB | 119,970 筆×14 欄;2004-01~2026-09;163 條路線、20 個航空公司標籤；**月彙總,非班次級** | CC BY 3.0 AU(data.gov.au 元資料) | 否 | 未確認(推論:澳洲政府站多半可) |
- **重要欄位**:BTS=`FlightDate, Reporting_Airline, Tail_Number, Origin, Dest, CRSDepTime, DepDelay, DepDel15, ArrDelay, ArrDel15, Cancelled, CancellationCode, Diverted, CarrierDelay/WeatherDelay/NASDelay/SecurityDelay/LateAircraftDelay`;BITRE=`Route, Airline, Sectors_Scheduled/Flown, Cancellations, Arrivals_Delayed, Year, Month_Num`。
- **EDA 可以看什麼**(2026-08 單月):
  - 分布 1:到站延誤極右偏——中位數 0、p90 65 分、p99 258 分、最大 4,381 分;ArrDel15 26.9%、取消率 1.86%、改道 0.47%。
  - 分布 2:延誤成因分鐘占比——晚到飛機 41.3%、航空公司 29.3%、空管(NAS)23.3%、天氣 6.0%、安檢 0.1%(成因欄只有 159,636 筆有值);取消代碼 B 5,274／A 3,119／C 2,920(代碼意義依 BTS 慣例,未打開 lookup)。
  - 相關 1:同機尾前一班到站延誤與本班出發延誤相關 0.425(446,159 對)；出發與到站延誤相關 0.973。
  - 相關 2:出發延誤 15 分以上比例從 05 時的 7% 升到 19–20 時的 44%;取消率最高的熱門機場 DCA 7.1%。BITRE 年度取消率:2019 2.16%、2020 7.49%、2022 4.97%、2025 2.53%。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 取消/大延誤預測 | 邏輯迴歸、梯度提升樹(GBM) | TabPFN(小樣本表格基礎模型;60 萬列需抽樣,預期 GBM 仍可能勝,這是誠實比較的點) | PR-AUC、Brier 校準、提前量 |
| 替代班次推薦 | 規則:同 OD、同日、最近出發 | 檢索＋LLM 重排並解釋 | 回測準點命中率 |
| 通知/改票話術 | 模板 | LLM 生成＋LLM-as-judge＋C 人審 | 事實一致率(自動驗證)、語氣分 |
  - 文獻:[TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second](https://arxiv.org/abs/2207.01848)、[Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)。
- **AT3 系統長什麼樣**:「重播日」航班風險看板(紅黃綠)→點航班看風險原因與同日替代班次;按鈕「產生旅客通知草稿」「列 3 個改票方案」「升級人工」。Demo:①選 2026-08 某個延誤嚴重的日子與機場,看風險燈號隨時間變紅;②按「產生通知＋改票」,系統附上班次資料出處並自動檢查數字一致。
- **4 人分工**:專案管理 A(備 Kenny)｜利害關係人 C(備 A)｜方法論 Kenny(備 B)｜業務理解 A(備 C)｜軟體工程 Kenny(備 B)。Kenny=特徵/模型/LLM 管線;C=旅客視角、通知語氣與改票政策、合成旅客劇本;A=事件管理(incident management)流程類比:SLA、升級規則、通知時限;B=可靠的推論服務、佇列、監控與壓測。**A、B 的主場:中**(事件處置流程與服務可靠度是本業,但資料是航空不是 IT)。
- **風險與備案**:①BTS 是美國資料,與雪梨/UTS 脈絡無關,BITRE 只有月彙總不能做班次預測 → 以 BTS 做主、BITRE 做澳洲趨勢輔助;②沒有旅客/訂位資料 → 用合成旅客並明講;③沒有即時航班與天氣 → 用歷史重播;天氣資料(NOAA 等)本次未核對;④Kaggle 上航班延誤預測很常見 → 新角度放在「通知＋改票 Copilot」而非單純預測;⑤一個月就 60 萬列,取 3–6 個月即可。
- **最大缺點**:只有航班、沒有旅客那一半,價值鏈最後一哩(通知成效、改票接受率)只能模擬。

## V4 訪澳客源市場需求預測 → 接待容量情境規劃(ETS/ARIMA vs 時間序列基礎模型)
- **一句話**:用 ABS 月度入境資料(含國別階層)比較傳統預測與 Chronos/TimesFM,並把預測轉成房量/人力/座位的情境缺口。
- **業務情境**:企業=州或區域旅遊局(DMO)或連鎖飯店/地勤/景點營運(情境假設);痛點=客源市場復甦速度不一,排班、房量、行銷預算憑感覺。
  - BO1 提前排班與房量 → AG1 預測各客源市場未來 6–12 個月到訪量與區間 → T1 多序列預測
  - BO2 行銷預算投向 → AG2 找復甦最快/最慢市場 → T2 預測偏差與分群分析
  - BO3 容量情境 → AG3 把到訪量轉成旺季缺口 → T3 情境模擬(停留天數、每房人數為假設參數)
  - 成功標準:疫情後測試段的 MASE 與 80% 區間覆蓋率優於基準;情境表讓 C 能回答「下季哪個月缺多少房/人」。
- **資料(2026-10-30 核對)**:

| 表格 | 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|---|
| ABS OAD_COUNTRY | SDMX API(Accept: application/vnd.sdmx.data+csv) | https://data.api.abs.gov.au/rest/data/OAD_COUNTRY/all?startPeriod=2019-01&endPeriod=2026-08 | 200 | 0.71 MB | 12,846 筆;月資料 2019-01~2026-08;77 個國別/彙總代碼(含 TOT、TO1、TO5、TO6 等彙總→天然階層)×2 類旅客;每序列 75–92 個月 | ABS 頁尾標示 Creative Commons,版本未在頁面確認(推論 CC BY 4.0) | 否(本次未帶金鑰成功) | 未確認(推論:多半可) |
| ABS 發布頁 | OAD 最新發布 | https://www.abs.gov.au/statistics/industry/tourism-and-transport/overseas-arrivals-and-departures-australia/latest-release | 200 | — | 2026 年 8 月資料,2026-10-13 發布;短期訪客入境 755,530(+0.3% 年增);下次 2026-11-12 | 同上 | 否 | 未確認 |
| ABS 資料流清單 | dataflow/all | https://data.api.abs.gov.au/rest/dataflow/all?detail=allcompletestubs | 200 | 2.7 MB | 1,228 個資料流;另有 `OAD_REASON`(停留期間/目的)未下載 | 同上 | 否 | 未確認 |
| Monash tourism(教學基準) | Zenodo 4656096(月)/4656093(季)/4656103(年) | https://zenodo.org/records/4656096 | 200(API 查詢) | 199,791／93,833／36,749 B | 內容未下載,筆數/期間(未確認) | CC BY 4.0(Zenodo 元資料) | 否 | 未確認 |
- **區域資料的老實話**:data.gov.au 上的 Tourism Research Australia 區域資料只看到 2006–2015 年度版(CC-BY-3.0-AU,AURIN 連結,未打開);近期州/區域資料、BITRE 國際座位容量**本次未核對到**。ABS 彙總代碼的對照名稱表也沒抓(未確認)。
- **重要欄位**:`CAT_TRAVELLER`(5/6 兩類,對應名稱未確認)、`COUNTRY_RESID`(代碼)、`TIME_PERIOD`(月)、`OBS_VALUE`。
- **EDA 可以看什麼**:分布 1=疫情斷崖——2020-07 的加總只剩 2019-07 的 0.9%(加總是否重複計算彙總列未確認,只看比例);分布 2=各序列長度不一(75–92 個月)與量級跨數個級距。相關 1=各國復甦曲線的落後相關(誰先回來);相關 2=季節強度（南北半球客源)差異與 ACF。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 各國月預測 | seasonal naive、ETS、ARIMA | Chronos、TimesFM、Moirai 零樣本；LLMTime 作對照 | MASE、sMAPE,滾動起點;疫情前後分段報 |
| 階層調和(國→區域→總計) | bottom-up、MinT | 基礎模型輸出再調和 | 一致性、MASE |
| 預測區間 | ETS 區間 | 分位數預測 | 覆蓋率、pinball loss |
| 備戰簡報 | 人工 | LLM 讀預測＋歷史→簡報 | 數字一致率 |
  - 選型依據:用 GIFT-Eval 的評測思路。文獻:[Chronos](https://arxiv.org/abs/2403.07815)、[TimesFM](https://arxiv.org/abs/2310.10688)、[Unified Training of Universal Time Series Forecasting Transformers(Moirai)](https://arxiv.org/abs/2402.02592)、[GIFT-Eval: A Benchmark For General Time Series Forecasting Model Evaluation](https://arxiv.org/abs/2410.10393)、[Large Language Models Are Zero-Shot Time Series Forecasters](https://arxiv.org/abs/2310.07820)。
- **AT3 系統長什麼樣**:國別×月份預測圖（含區間),側欄情境滑桿(平均停留天、每房人數、成長假設)→房量/人力缺口;按鈕「產生季度備戰簡報」「匯出排班需求表」。Demo:①選某客源市場,比較 ETS 與 Chronos 預測誤差;②拉滑桿看旺季缺口,按「產生簡報」。
- **4 人分工**:專案管理 Kenny(備 C)｜利害關係人 C(備 A)｜方法論 Kenny(備 B)｜業務理解 C(備 A)｜軟體工程 Kenny(備 B)。Kenny=預測管線與評估;C=接待/行銷情境與假設參數;A=容量規劃(headroom、情境)方法與運維同構,審情境模型;B=預測服務化、排程重跑。**A、B 的主場:弱到中**(容量規劃思維可轉用,但資料與領域非本業)。
- **風險與備案**:①沒有區域/州近期資料與供給端容量資料 → 「區域」承諾降為客源市場層級,容量靠假設參數;②月資料每序列僅 ~92 點,基礎模型未必贏 ETS——這正是誠實比較的賣點,但也可能「沒有故事」;③資料量小,「系統跑得順」容易但不夠有分量;④tourism 預測在 Kaggle/教科書很常見 → 靠 ABS 新資料＋疫情斷裂＋決策情境區隔。
- **最大缺點**:缺區域與供給端資料,「接待容量」不是資料驅動,只是假設推算。

## V5 大型活動售票/報名尖峰 → 系統容量預測與擴容建議(關注度預測＋自建壓測＋擴容模擬)
- **一句話**:用維基百科頁面瀏覽量當「關注度」代理預測活動開賣尖峰,B 自建小型售票系統量測承載曲線,模擬不同擴容策略的服務水準(SLO)與成本,並由 LLM 產出擴容建議書。
- **業務情境**:企業=賽事/演唱會/馬拉松的售票與報名平台營運團隊(情境假設);痛點=開賣瞬間流量暴增(flash crowd)崩潰,或常態過度配置燒錢。
  - BO1 開賣不當機 → AG1 預測尖峰請求量(RPS)與持續時間 → T1 關注度＋日程特徵的時間序列預測
  - BO2 成本可控 → AG2 找最省的擴容時程 → T2 模擬固定閾值 vs 預測式預擴容的 SLO 違反與成本
  - BO3 與主辦方溝通 → AG3 建議開賣時段/排隊機制 → T3 LLM 產生 runbook 與主辦方簡報
  - 成功標準:模擬 N 場活動,p95 延遲超標時間 <1%,相對「全時段過度配置」成本降 X%(X 待實驗,提案目標 30%);尖峰漏報率最低。
- **資料(2026-10-30 核對)**:

| 表格 | 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|---|
| Wikimedia Pageviews API | per-article 日資料 | https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/Vivid_Sydney/daily/20150701/20260930 | **429**(兩次,本環境被限流,未取回資料) | — | 資料起點(未確認;dumps 說明稱 2015-05 起) | CC0(dumps readme 原文:「All Analytics datasets are available under the Creative Commons CC0 dedication」) | 否(需 User-Agent) | **推論不可**(維基百科在大陸被封鎖) |
| Wikimedia 小時檔 | pageviews dumps | https://dumps.wikimedia.org/other/pageviews/readme.html | 200 | 每小時一檔(大小未確認) | 2015-05 起 | CC0(同上) | 否 | 推論不可 |
| Azure 公開 traces | VM 2017/2019、Functions 2019(2 週)、LLM 推論 2023/2024 等 | https://raw.githubusercontent.com/Azure/AzurePublicDataset/master/README.md | 200 | 各 trace 大小(未確認) | 見左 | README 無授權條文、要求引用論文;LICENSE(未確認) | 否 | 未確認(檔案託管在 GitHub Releases,推論不穩) |
| 活動日程/開賣日 | 手工整理 | 官方售票頁 | — | — | C 建 20–40 場,含公布日、開賣日、容量 | 各網站(未確認) | 否 | 未確認 |
| 自建壓測資料 | B 用 Locust/k6 打 mock 售票系統 | 自產 | — | — | 承載曲線(每 vCPU 可承載 RPS、延遲分位數) | 自有 | 否 | 可 |
- **資料拼接風險(老實評估)**:①維基瀏覽量是「讀百科的人」，不是「搶票的人」,轉換率完全未知(推論:只能當相對關注度);②Azure traces 與任何活動無關,只能當基底負載形狀,疊加活動尖峰是情境假設;③因此整題是**模擬器＋預測方法比較**,不能宣稱「預測了真實售票系統」。可驗證的部分:瀏覽量序列本身的預測誤差(真實時序)、自建壓測的承載曲線(自己量的真實資料)。
- **重要欄位**:pageviews=`article, timestamp, views`;Azure Functions=每函式每分鐘呼叫數(依 README 描述,未打開);壓測=`RPS, p50/p95/p99, 錯誤率, vCPU`。
- **EDA 可以看什麼**(待 Kenny 在非受限網路取回後驗證):分布 1=瀏覽量重尾、尖峰/中位數倍率;分布 2=Azure 呼叫量跨數量級的偏態(Serverless in the Wild 論文主題,推論)。相關 1=開賣前 N 天瀏覽量爬升 vs 事件日距(倒數日效應);相關 2=不同類型活動(體育/演唱會/節慶)的尖峰形狀差異。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 關注度/負載預測 | seasonal naive、ETS、日程特徵迴歸 | Chronos、TimesFM、Moirai 零樣本;Chronos-2 含共變數(細節未確認) | 尖峰漏報率(比平均誤差重要)、MASE |
| 擴容決策 | 固定閾值 autoscaling、全時段過度配置 | 預測式預擴容(predictive scaling)＋模擬 | SLO 違反分鐘、成本、冷啟動次數 |
| 突發偵測 | z-score/EWMA | 基礎模型預測區間 | 偵測延遲 |
| runbook/建議書 | 模板 | LLM(讀自家 runbook)＋LLM-as-judge＋A/B 審 | 步驟可執行性 |
  - 文獻:[Chronos](https://arxiv.org/abs/2403.07815)、[TimesFM](https://arxiv.org/abs/2310.10688)、[Moirai](https://arxiv.org/abs/2402.02592)、[Chronos-2: From Univariate to Universal Forecasting](https://arxiv.org/abs/2510.15821)、[LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)。
- **AT3 系統長什麼樣**:活動日曆＋預測負載曲線＋容量線;滑桿(轉換率假設、預熱分鐘);按鈕「產生擴容計畫(時間表＋成本)」「回放模擬」「產生主辦方開賣時段建議」。Demo:①選演唱會開賣,看預測尖峰與現有容量缺口;②按「回放」比較固定閾值 vs 預測式的 SLO 違反與成本,再按「產生 runbook」。
- **4 人分工**:專案管理 Kenny(備 A)｜利害關係人 C(備 A)｜方法論 Kenny(備 B)｜業務理解 A(備 C)｜軟體工程 B(備 Kenny)。Kenny=預測與 LLM 管線、整合；C=活動日程、開賣機制(抽籤/排隊/實名)、主辦方需求;**A（主場:強)**=定義 SLO、容量與成本模型、扮營運長驗收擴容建議、審 runbook;**B(主場:強)**=自建 mock 售票系統、壓測、自動擴縮與監控、部署計畫。
- **風險與備案**:①沒有真實售票流量(最大);②Wikimedia API 本環境 429、且大陸被封 → 由 Kenny 在一般網路取回後存成 CSV 共享(CC0 可分享);③做壓測需要雲端或本機資源 → 先用筆電容器，雲端額度由 B 評估;④Azure traces 授權未確認 → 可改用自製合成負載;⑤評審可能質疑「模擬≠驗證」→ 報告明寫定位為決策支援模擬器,只對可驗證部分報精度。
- **最大缺點**:缺少真實的售票/報名流量,關注度→流量的轉換是假設,模擬結果不能對外宣稱準確。

## 沒涵蓋/換掉的種子
- **種子 1(保留)**:calendar 實測無價格欄、僅單一快照 → 改用「評論量＋未來不可訂率」當需求代理;舊期快照需 Archived Data Request,未申請。
- **種子 2(換資料)**:沒找到「有日期、有星等、澳洲」且授權清楚的開放評論資料,改用 Yelp Open Dataset(美加為主);Kaggle Disneyland 頁只拿到標題,授權/大小未確認；Yelp 壓縮檔與完整條款未打開。
- **種子 3(保留)**:BTS 為主、BITRE 為輔;BITRE 只是月彙總。**種子 4(縮小)**:近期區域資料沒找到 → 降為客源市場層級;fpp3 `tourism`(R 套件資料)沒打開,僅核對 Monash 在 Zenodo 的 tourism 三個資料集記錄頁,內容未下載。**種子 5(自選)**:售票尖峰容量。
- **其他沒涵蓋**:NSW/雪梨活動開放資料與公共假期資料集、天氣資料(NOAA/Meteostat)、BITRE 國際座位容量、TRA 近期 NVS/IVS、ABS 代碼對照與 OAD_REASON 內容、Azure traces 實際大小與授權原文、TabPFN v2(Nature)DOI 與 Chronos-2 共變數細節、HuggingFace/ModelScope 模型在大陸的下載可用性、OpenAI/Claude API 在大陸的可用性(A 用 LLM 部分建議跑本地模型,未實測)。
- **適配度初判(推論)**:V5 是唯一讓 A、B 有強主場的題目但資料最不「真」;V1 資料最紮實、與眾不同度高但 A/B 弱;V3 A/B 中等、資料紮實但脈絡在美國;V4 資料可靠但分量輕;V2 距離最遠。
