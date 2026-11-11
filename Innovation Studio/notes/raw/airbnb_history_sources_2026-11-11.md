結論:不花錢最多能拿到「2025-12-12 起、約每季一期、共 4 期」的雪梨與墨爾本房源快照(listings/calendar/reviews),2024 到 2025-11 沒有免費快照;2024 年以來只能靠現有評論日期看月度活躍度,或付費申請、或用標示清楚的模擬資料補。

# Airbnb 2024–2026 資料取得途徑查證(2026-11-11)

查證方式:今天用 curl 讀官方頁與其頁面資料檔、對 listings 檔只發 HEAD(只看狀態碼與 Content-Length,未下載資料本體)、WebFetch 讀官方文字頁、WebSearch 2 次(Kaggle、Zenodo 各一)。

## 1. 官方免費頁現況([Get the Data,今天已開](https://insideairbnb.com/get-the-data/))
- 每個城市頁面只直接顯示最新一期;其餘期別藏在「show archived data」(點擊才展開,靜態 HTML 裡沒有)。我沒有點開渲染後的區塊;改讀該頁自己載入的資料檔([page-data/sq/d/3176684073.json](https://insideairbnb.com/page-data/sq/d/3176684073.json),今天已開),裡面雪梨、墨爾本各 4 筆期別,且 8 個 listings 網址 HEAD 全部 200,所以這 4 期確實存在。
- 頁面說明:封存區「大致是最近 12 個月的季度資料」,要更多請走 [data request](https://insideairbnb.com/data-requests/)。
- 每期提供檔案:data/ 下 listings.csv.gz、calendar.csv.gz、reviews.csv.gz(詳細版);visualisations/ 下 listings.csv、reviews.csv、neighbourhoods.csv、neighbourhoods.geojson(摘要版)。最新期(2026-09-16)這 7 種檔的網址我是從頁面 HTML 讀到(repo 的 official_links.json 亦同);其餘三期的 calendar/reviews 網址未逐一確認(只對 listings 發 HEAD)。

| 城市 | 期別 | listings HEAD(狀態 / Content-Length) | 網址 |
|---|---|---|---|
| 雪梨 | 2026-09-16 | 200 / 12,747,164 | [listings.csv.gz](https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/listings.csv.gz) |
| 雪梨 | 2026-06-16 | 200 / 12,633,389 | [listings.csv.gz](https://data.insideairbnb.com/australia/nsw/sydney/2026-06-16/data/listings.csv.gz) |
| 雪梨 | 2026-03-21 | 200 / 9,036,609 | [listings.csv.gz](https://data.insideairbnb.com/australia/nsw/sydney/2026-03-21/data/listings.csv.gz) |
| 雪梨 | 2025-12-12 | 200 / 11,627,165 | [listings.csv.gz](https://data.insideairbnb.com/australia/nsw/sydney/2025-12-12/data/listings.csv.gz) |
| 墨爾本 | 2026-09-16 | 200 / 15,409,076 | [listings.csv.gz](https://data.insideairbnb.com/australia/vic/melbourne/2026-09-16/data/listings.csv.gz) |
| 墨爾本 | 2026-06-16 | 200 / 15,270,041 | [listings.csv.gz](https://data.insideairbnb.com/australia/vic/melbourne/2026-06-16/data/listings.csv.gz) |
| 墨爾本 | 2026-03-21 | 200 / 11,071,408 | [listings.csv.gz](https://data.insideairbnb.com/australia/vic/melbourne/2026-03-21/data/listings.csv.gz) |
| 墨爾本 | 2025-12-12 | 200 / 13,972,316 | [listings.csv.gz](https://data.insideairbnb.com/australia/vic/melbourne/2025-12-12/data/listings.csv.gz) |

- 同學截圖問題:(1) 兩城各列 4 期(上表);(2) HEAD 見上表,8 條皆 200;(3) 最早一期 2025-12-12,所以免費最遠只到 2025-12-12;(4) 網址樣式對:`data.insideairbnb.com/australia/<州>/<城市>/<YYYY-MM-DD>/data/listings.csv.gz`,日期格式是 YYYY-MM-DD,但日期不規律(09-16、06-16、03-21、12-12),不能自己推算。
- 試過的日期只有頁面資料檔列出的 8 筆,沒有猜測日期。
- 各期內容(欄位數、列數)今天沒有下載,不得從檔案大小推論房源數變化。

## 2. 歷史資料申請(今天頁面:[Data Requests](https://insideairbnb.com/data-requests/),今天已開;11/07 的紀錄見 [notes/15](../15_Airbnb_2024起雙城與ROI_研究範圍.md))
- 誰能申請:任何人填封存資料申請;站方依「是否符合其使命、申請人身分、要的資料、用途」排優先順序。活動人士、記者、居民的使命相符申請最優先、通常免費;政府機關高優先、通常要資助;研究者(個人或機構)做使命相符研究為中優先、要付費;商業或非使命相符研究最低優先、要付費。
- 計價:依「城市數」不是指名城市。非使命相符/商業:1 城 US$500、2 城 US$800、3 城 US$1,100。使命相符研究:1 城 US$300、2 城 US$500、3 城 US$700。另有依世界銀行所得分類的 10% / 25% 折扣(國際或資金充裕機構不適用)。
- 學術用途:頁面沒有「學生」或「課堂作業」類別;學術研究若符合使命(例如住房管制、士紳化、旅遊化)算使命相符研究。
- 與 11/07 紀錄比較:US$800(2 城、非使命相符)吻合;今天另看到使命相符研究 2 城 US$500 這一檔。11/07 紀錄把「旅遊/定價策略」歸為非使命相符,我今天的頁面摘要沒看到這個歸類句子,未確認。頁面未寫交付內容、時效、交付資料的授權。
- 我沒有填表、沒送出、沒聯絡站方;一個課堂專題會被歸哪一類,頁面沒寫,須由站方判定。

## 3. 資料字典(官方連結的[資料字典試算表](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing),今天已開)
- 今天開到的內容只有 listings 詳細檔的欄位說明,版本 v4.3(2022-08);price 說明為「當地幣別日價」。試算表頁面載入不完整,calendar 欄位的分頁今天讀不到,所以「官方字典對 calendar 有沒有價格欄」今天無法由字典回答。
- [Data Assumptions](https://insideairbnb.com/data-assumptions/)(今天已開):只說日曆涵蓋未來 365 天、無法分辨「已訂」與「房東封鎖」(兩者都算不可訂);沒有列 calendar 欄位。
- repo 11/07 紀錄([airbnb_sources_2026-11-07.md](airbnb_sources_2026-11-07.md))寫:2026-09-16 雪梨 calendar 表頭為 listing_id、date、available、minimum_nights、maximum_nights,沒有 price。這是 11/07 實讀表頭,今天未重開。

## 4. 授權([Data Policies](https://insideairbnb.com/data-policies/),今天已開)
- 公開下載資料為 CC BY 4.0,須署名 Inside Airbnb、寫明地點與收集日期並附連結,學術文章要正式資料集引用;站方請求不要重新發布整份資料、不要爬站,腳本分析請下載一次即可。

## 5. 其他公開資料集(各搜尋 1 次;只看搜尋結果與資料集頁,未下載)
- Kaggle 有雪梨/墨爾本的舊期別,都早於 2024 起,對「2024 以來」沒有幫助:
  - [Sydney Airbnb Open Data](https://www.kaggle.com/datasets/tylerx/sydney-airbnb-open-data):搜尋結果摘要稱檔案標示 2018-12。授權:資料集頁今天讀不到授權標示。
  - [Melbourne Airbnb Open Data](https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data):搜尋摘要稱 2018-12-07 編製。授權:未開頁確認。
  - [Melbourne Airbnb | September 2023](https://www.kaggle.com/datasets/tauanoliveira/melbourne-airbnb-september-2023-dataset):標題為 2023-09;授權頁面讀不到。
  - [Airbnb: Melbourne 2023-03-13](https://www.kaggle.com/datasets/samibrahim/airbnb-melbourne):2023-03-13;授權頁面讀不到。
  - 結論:今天沒找到涵蓋 2024 年到 2025-11 的雪梨/墨爾本 Kaggle 資料集;各頁授權標示我都沒讀到,不能當作可轉用。
- Zenodo:沒有查到雪梨或墨爾本的 Inside Airbnb 舊期別資料集(結果多是別的城市、AirDNA 或不含原始資料的程式碼存檔)。

## 6. 途徑總表
| 途徑 | 拿得到什麼 | 涵蓋期間 | 花費 | 限制 | 今天有沒有實際確認 | 連結 |
|---|---|---|---|---|---|---|
| 官方免費各期 | 兩城 listings/calendar/reviews 快照 | 2025-12-12、2026-03-21、2026-06-16、2026-09-16 | 0 | 只有 4 期;無 2024–2025-11;calendar 11/07 紀錄無 price | 有:8 條 listings HEAD 皆 200;期別來自頁面資料檔 | [Get the Data](https://insideairbnb.com/get-the-data/) |
| 官方歷史申請 | 站方依申請提供舊期別 | 申請時談(未知) | 指南:2 城 US$500(使命相符)或 US$800(非使命相符) | 優先順序與歸類由站方判定;交付內容與時效未寫 | 有讀價格頁;未送出申請 | [Data Requests](https://insideairbnb.com/data-requests/) |
| 現有評論日期看月度活躍度 | 現存房源的每月評論數(repo 已算:2024 起雪梨 474,233、墨爾本 546,972 則) | 2024 起至 2026-09 | 0 | 看不到當時價格、看不到已下架房源;評論日不是入住日 | 筆數為 repo 既有計算,今天未重算 | [reviews.csv.gz(雪梨 2026-09-16)](https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/reviews.csv.gz) |
| 其他公開資料集 | Kaggle 舊期別(2018、2023);Zenodo 無 | 皆早於 2024 | 0 | 授權未讀到;不涵蓋 2024 起 | 有搜尋,未下載 | [Kaggle 雪梨](https://www.kaggle.com/datasets/tylerx/sydney-airbnb-open-data)、[Kaggle 墨爾本 2023-09](https://www.kaggle.com/datasets/tauanoliveira/melbourne-airbnb-september-2023-dataset) |
| 模擬資料(老師允許) | 自行產生的價格/入住序列 | 任意 | 0 | 不是觀測值,圖表與結論須標「模擬」 | 老師允許為 repo 既有紀錄,今天未重驗 | 無外部來源 |

## 7. 三個組合(題目目標句「不要這樣寫 → 改這樣寫」)
- 零成本(官方 4 期 + 現有評論日期):拿到 2025-12 起每季房源快照與 2024 起評論月度活動;缺 2024–2025-11 的房源與價格面板、當時價格、已下架房源。
  不要這樣寫 → 改這樣寫:「分析 2024 年以來雪梨與墨爾本的市場變化」→「以 2025-12 至 2026-09 四期快照做近一年比較,並以現存房源的評論日期觀察 2024 年以來的評論活躍度」。
- 零成本加模擬:同上,再加分開標示的模擬資料(用來演示方法或補價格序列);缺的仍是真實的 2024–2025 價格與供給。
  不要這樣寫 → 改這樣寫:「用 2024–2026 資料預測價格」→「以真實近一年快照訓練/驗證;2024 以前的情境由模擬資料示範,結果不代表真實市場」。
- 付費申請(約 US$500–800,2 城):有機會取得 2024 起舊期別,但是否核准、涵蓋哪幾期、何時交付未知。
  不要這樣寫 → 改這樣寫:「已取得 2024 年起完整資料」→「已向 Inside Airbnb 申請 2024 年起舊期別;拿到前,結論只用免費四期」(拿到後再列實際期別)。

## 8. 沒查到的事
- 渲染後的「show archived data」區塊我沒有點開看;期別是讀頁面載入的資料檔。
- 其餘三期(2026-06-16、2026-03-21、2025-12-12)的 calendar/reviews 網址與欄位,今天沒對檔案發請求。
- 官方字典的 calendar 分頁今天讀不到,calendar 是否有 price 欄以 11/07 實讀表頭為準(無)。
- 申請的交付內容、時效、授權、學生專題的歸類;Kaggle 各頁授權標示;Kaggle 是否另有 2024 起的雪梨/墨爾本資料集(只搜一次,可能漏)。
