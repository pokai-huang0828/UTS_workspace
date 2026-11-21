# 雪梨可比房源:相關係數矩陣與掛牌價分布(IS-1121-REPORT-FIG-A)

## 1. 怎麼跑、樣本與規則

- 重跑:`python "Innovation Studio/analysis/sydney/syd_r_report_figures.py"`(repo 根目錄下執行;不加 `-I`)。
- 資料(唯讀):`scratchpad/insideairbnb_sydney/2026-09-16/data/listings.csv.gz`,20,833 列,`dtype=str, keep_default_na=False` 讀入。
- 樣本規則(照抄 `syd_b_positioning.py` 的 `scope()` 第 68–72 行與 `parse_amen()` 第 85–89 行):`room_type == Entire home/apt`、`bedrooms` 為 1 或 2、`accommodates` 2–4、`minimum_nights` 1–7、`price` 非空。篩完 6,639 列(程式內 assert 檢查為 6,639)。
- 11 個變數:price(去 `$`、`,` 轉數字)、bedrooms、accommodates、amenities_n(設施 JSON 解析後去重去空白的個數)、rating / accuracy / cleanliness / checkin / communication / location / value(各 `review_scores_*`)。評分欄空字串視為缺值,不補。
- 相關:Spearman(成對刪除缺值);JSON 內另附 price 取自然對數後的 Pearson(`pearson_logprice`)與每對的有效筆數(`pair_n`)。
- 輸出:`notes/raw/syd_r_report_figures_2026-11-21.json`、`notes/figures/report_fig_corr_heatmap_2026-11-21.png`、`notes/figures/report_fig_price_dist_2026-11-21.png`。

## 2. 描述統計(11 個變數)

| 變數 | 中文 | 有效筆數 | 缺值 | 平均 | 標準差 | 最小 | P25 | 中位數 | P75 | 最大 | 偏態 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| price | 掛牌價 | 6,639 | 0 | 397.28 | 472.49 | 79 | 260.33 | 338.50 | 442.39 | 18848 | 21.99 |
| bedrooms | 臥室數 | 6,639 | 0 | 1.39 | 0.49 | 1 | 1.00 | 1.00 | 2.00 | 2 | 0.44 |
| accommodates | 可住人數 | 6,639 | 0 | 3.08 | 0.94 | 2 | 2.00 | 3.00 | 4.00 | 4 | -0.16 |
| amenities_n | 設施數 | 6,639 | 0 | 40.06 | 13.26 | 0 | 32.00 | 41.00 | 49.00 | 96 | -0.35 |
| rating | 總評分 | 6,051 | 588 | 4.77 | 0.33 | 1 | 4.70 | 4.86 | 4.96 | 5 | -5.34 |
| accuracy | 描述相符 | 6,051 | 588 | 4.81 | 0.31 | 1 | 4.75 | 4.88 | 4.98 | 5 | -5.89 |
| cleanliness | 清潔 | 6,051 | 588 | 4.75 | 0.34 | 1 | 4.66 | 4.83 | 4.96 | 5 | -4.49 |
| checkin | 入住 | 6,051 | 588 | 4.83 | 0.30 | 1 | 4.80 | 4.91 | 5.00 | 5 | -6.07 |
| communication | 溝通 | 6,051 | 588 | 4.87 | 0.27 | 1 | 4.86 | 4.95 | 5.00 | 5 | -7.46 |
| location | 位置 | 6,051 | 588 | 4.87 | 0.21 | 1 | 4.82 | 4.92 | 5.00 | 5 | -6.30 |
| value | 性價比 | 6,051 | 588 | 4.68 | 0.35 | 1 | 4.59 | 4.75 | 4.88 | 5.04 | -4.55 |

## 3. Spearman 相關矩陣(兩位小數)

| | price | bedrooms | accommodates | amenities_n | rating | accuracy | cleanliness | checkin | communication | location | value |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **price** | 1.00 | 0.41 | 0.35 | 0.20 | 0.14 | 0.13 | 0.10 | 0.06 | 0.09 | 0.28 | 0.01 |
| **bedrooms** | 0.41 | 1.00 | 0.73 | 0.05 | -0.01 | 0.02 | -0.03 | -0.01 | -0.01 | 0.04 | -0.03 |
| **accommodates** | 0.35 | 0.73 | 1.00 | 0.11 | -0.03 | -0.01 | -0.05 | -0.05 | -0.02 | 0.02 | -0.03 |
| **amenities_n** | 0.20 | 0.05 | 0.11 | 1.00 | 0.17 | 0.13 | 0.14 | 0.08 | 0.10 | 0.07 | 0.14 |
| **rating** | 0.14 | -0.01 | -0.03 | 0.17 | 1.00 | 0.82 | 0.76 | 0.63 | 0.67 | 0.52 | 0.78 |
| **accuracy** | 0.13 | 0.02 | -0.01 | 0.13 | 0.82 | 1.00 | 0.72 | 0.60 | 0.65 | 0.51 | 0.75 |
| **cleanliness** | 0.10 | -0.03 | -0.05 | 0.14 | 0.76 | 0.72 | 1.00 | 0.53 | 0.57 | 0.43 | 0.68 |
| **checkin** | 0.06 | -0.01 | -0.05 | 0.08 | 0.63 | 0.60 | 0.53 | 1.00 | 0.62 | 0.44 | 0.56 |
| **communication** | 0.09 | -0.01 | -0.02 | 0.10 | 0.67 | 0.65 | 0.57 | 0.62 | 1.00 | 0.46 | 0.60 |
| **location** | 0.28 | 0.04 | 0.02 | 0.07 | 0.52 | 0.51 | 0.43 | 0.44 | 0.46 | 1.00 | 0.46 |
| **value** | 0.01 | -0.03 | -0.03 | 0.14 | 0.78 | 0.75 | 0.68 | 0.56 | 0.60 | 0.46 | 1.00 |

## 4. 看得出什麼(只講數字顯示的事)

1. 相關最高的三對(依絕對值):rating–accuracy = 0.82;rating–value = 0.78;rating–cleanliness = 0.76。
2. 掛牌價與其他 10 個變數的 Spearman:bedrooms 0.41、accommodates 0.35、amenities_n 0.20、rating 0.14、accuracy 0.13、cleanliness 0.10、checkin 0.06、communication 0.09、location 0.28、value 0.01。
3. 掛牌價與 7 個評分類變數的相關介於 0.01 到 0.28;與 accommodates 0.35、bedrooms 0.41、amenities_n 0.20。
4. 6 個分項評分(不含總評分)與總評分的相關介於 0.52 到 0.82;7 個評分變數彼此的相關最低 0.43(cleanliness–location)、最高 0.82(rating–accuracy)。
5. 掛牌價偏態 21.99(平均 397、中位數 338);1 臥室中位數 299(n=4,029,P25–P75 為 238–376),2 臥室中位數 414(n=2,610,P25–P75 為 326–538.9);超過 1,000 澳元的 116 套、超過 2,000 澳元的 24 套。
6. price 取自然對數後的 Pearson:與 bedrooms 0.38、accommodates 0.33、amenities_n 0.16、rating 0.08(對照 Spearman 依序 0.41、0.35、0.20、0.14)。

## 5. 限制

- 篩選把範圍壓窄:bedrooms 只有 1 和 2、accommodates 只有 2–4,所以這兩個變數的相關係數只反映這段範圍內的關係,不能外推到更大的房子。
- 評分擠在接近滿分:總評分中位數 4.86、P25 4.70(滿分 5),分項評分也類似;變異小、並列值多,Spearman 係數對此類資料較敏感。
- price 是掛牌價,不是成交價;沒有看到實際訂房價格。
- 評分缺值(沒有評論或沒有評分的房源):rating 588、accuracy 588、cleanliness 588、checkin 588、communication 588、location 588、value 588(共 6,639 套);涉及評分的係數用的是成對有效樣本(筆數見 JSON `pair_n`),有評分的房源不一定等於全體房源的縮影。
- 本表只描述相關,不含因果推論,也沒有做模型或分群。
