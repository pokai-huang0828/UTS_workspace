# 好做版題目的資料核對(2026-11-04)

> 2 個 sonnet 助手分頭打開頁面/檔案核對;指揮官另外自己驗了共享單車空值(0 個)和 NAB 檔名(GitHub API)。用在 `notes/07_第一次組會選題清單.html` 第 2 版。

| # | 資料 | 網址 | 大小 / 行列 | 答案欄 | 文字欄 | 授權 | 帳號 | 備註 |
|---|---|---|---|---|---|---|---|---|
| 1 | Hotel Booking Demand(Antonio, Almeida & Nunes 2019, Data in Brief 22:41–49) | 論文 doi.org/10.1016/j.dib.2018.11.126;CSV raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv | 16.9 MB;119,390 × 32(City 79,330、Resort 40,060);2015-07-01 到 2017-08-31 | is_canceled(37.0% 取消) | 無 | 論文「open access under CC BY」(搜尋摘要,論文頁 403 沒打開);TidyTuesday 沒另標授權 | 不用 | `reservation_status` 會洩漏答案,要刪 |
| 2 | UCI Bike Sharing(id 275) | archive.ics.uci.edu/dataset/275/bike+sharing+dataset | zip 273 KB;hour.csv 17,379 × 17、day.csv 731 × 16;2011–2012 | cnt(= casual + registered,預測時要刪這兩欄) | 無 | CC BY 4.0(原文) | 不用 | 空值 0 個(指揮官自查);天氣值已標準化 |
| 3 | Trip Advisor Hotel Reviews(Kaggle andrewmvd) | kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews | 約 15 MB;「20k reviews」;2 欄 Review、Rating(GitHub 專案說的) | Rating 1–5 | Review | CC BY-NC 4.0;要引用 Alam, Ryu & Lee (2016) Information Sciences 339:206–223 | Kaggle 登入 | 從 Tripadvisor 爬的 |
| 4 | Airline Passenger Satisfaction(Kaggle teejmahal20) | kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction | 約 15 MB;train 103,904 + test 25,976(**二手來源**) | satisfaction | 無 | 「Other (specified in description)」,說明沒寫條款 | Kaggle 登入 | 改自 johndddddd/customer-satisfaction;來源不清 |
| 5 | IT Service Ticket Classification(Kaggle adisongoh) | kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset | 約 15 MB;47,837 × 2 | Topic_group(Hardware、HR Support、Access、Miscellaneous、Storage、Purchase、Internal Project、Administrative rights…) | Document | CC0 | Kaggle 登入 | 沒寫來源,真實或生成不明 |
| 6 | Numenta Anomaly Benchmark realAWSCloudwatch | github.com/numenta/NAB | 17 檔 × 約 4,032 點(每 5 分鐘);標註 labels/combined_windows.json(這 17 檔有 30 個異常窗) | 異常窗 | 無 | repo MIT | 不用 | 17 檔 = 8 EC2 CPU、2 RDS CPU、2 磁碟寫入、2 網路流入(+1 iio NetworkIn)、1 ELB 請求數、1 grok ASG |
| 7 | UCI Online Retail II(id 502) | archive.ics.uci.edu/dataset/502/online+retail+ii | xlsx 43.5 MB;1,067,371 × 8;2009-12-01 到 2011-12-09 | 無 | Description(短商品名) | CC BY 4.0 | 不用 | 退貨是負數量;CustomerID 可能缺值 |
| ✗ | Google Play Store Apps(Kaggle lava18) | kaggle.com/datasets/lava18/google-play-store-apps | 約 9 MB;apps 10,841 × 13(二手) | Rating;評論 Sentiment(看起來是程式算的) | 評論 | CC BY-SA 4.0 | Kaggle 登入 | **沒採用**:2019 年爬的、重複和缺值多、情感標籤是演算法產生 |

- 大陸(北京)能不能打開:全部未測試。資料都很小,打不開就由 Kenny 下載後分享。
- 備選(沒採用):Hugging Face PolyAI/banking77(13,083 句、77 個意圖、CC BY 4.0),領域是銀行客服,和隊伍不對口。
