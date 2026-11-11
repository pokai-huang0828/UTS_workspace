**結論:資料完整度 A = 3 分、B = 2 分;A 的競品欄位夠用但「新房東」只能用首評年份代理,B 的收入欄是由評論數推算出來的估計值,而且缺成本欄,撐不起「投資報酬」。**

範圍:雪梨(全體 20,833 / 篩選 7,565 / 篩選且有價 6,639)、墨爾本(25,715 / 10,940 / 8,223),Inside Airbnb 2026-09-16 批次。
篩選 = 整套、1–2 房、2–4 人、最低 1–7 晚。程式 `Innovation Studio/analysis/airbnb_ab_quality_checks.py`,彙總 `airbnb_ab_quality_checks_2026-11-11.json`。
下面數字預設是「篩選且有價」;JSON 路徑 = `cities.<sydney|melbourne>.scope_price.<鍵>`(全體在 `.all`、篩選含無價在 `.scope`)。
格式「雪 / 墨」。

## 方案 A(新房東競品分析):3 / 5

1. **新房東沒有直接欄位,只能用首評代理,而且「新房源」不等於「新手房東」**
   - `host_since` 缺 100%(`h_host.host_since_missing_pct`)。
   - 首評在批次前 12 個月內:2,028 筆(30.55%)/ 2,056 筆(25.0%)(`e_first_review_years.first_review_within_12m_before_batch`,`within_12m_pct_of_rows`)。
   - 首評年份分布(`e_first_review_years.bins`):2022 以前 1,638 / 2,200;2023 718 / 1,033;2024 943 / 1,192;2025 1,324 / 1,534;2026 1,428 / 1,448;無評論 588 / 816。
   - 多房源房東(`calculated_host_listings_count` ≥ 2)佔 61.64% / 62.71%(`h_host.calculated_host_listings_ge2_pct`)。新上架的房源有六成機率屬於已經有多間房的房東,抓不出真正第一次當房東的人。
2. **競品池的量夠,但小區偏薄**
   - 篩選樣本價格 100% 有值(`a_price.price_missing` = 0)。
   - 區數 38 / 30(`f_neighbourhoods.sample_priced.n_neighbourhoods`)。
   - 每區筆數 min / 中位 / max:6 / 80 / 1,855(雪),22 / 86.5 / 3,487(墨)(`sample_priced.min/median/max`)。
   - ≥ 30 筆的區 33 / 27 個,< 30 筆的區 5 / 3 個(`n_ge_30`、`n_lt_30`)。
   - 若限「近 12 個月有評論」,≥ 30 筆的區剩 29 / 25 個(`sample_priced_and_reviews_ltm_gt0.n_ge_30`)。
   - 再切成「新房源 × 區」(2,028 / 2,056 筆分到 38 / 30 區)這次沒算,預期多數區會 < 30。
3. **設備與房型欄位可解析,價格要截尾**
   - `amenities` 能當 JSON 清單解析 100%(`g_amenities.parse_ok_pct_of_rows`),設備數中位 41 / 41(`n_amenities_median`),最常見是 Smoke alarm、Kitchen、Wifi(`top10`)。
   - `bathrooms_text` 缺 0%,能抓出數字 99.83%(`j_bathrooms_text.parse_digit_ok_pct_of_rows`),含 half-bath 為 100%。
   - 價格 p50 / p99:338.5 / 1,198(雪),264 / 937(墨);最大值 18,848 / 90,000(`a_price.p50`、`p99`、`max`)。≥ 5,000 的只有 11 / 6 筆(`n_ge_5000`),但會拉歪平均,要截尾或用中位數。

## 方案 B(投資報酬測算):2 / 5

1. **收入欄是推算出來的,不是另外觀察到的**
   - `estimated_revenue_l365d` ÷ (`price` × `estimated_occupancy_l365d`) 落在 0.99–1.01 的比例是 100%:5,815 / 5,815(雪)、6,885 / 6,885(墨)(`b_revenue_vs_price_x_occ.ratio_within_0.99_1.01_pct`;全體也是 100%)。
   - 入住晚數大約是「近一年評論數 × 6 晚」(`c_occupancy.occ_per_review_ltm_p50` = 6),Spearman 0.9938 / 0.9969(`spearman_vs_reviews_ltm`)。
   - 評論 = 0 時入住一定 = 0,反過來也成立,兩個方向例外都是 0 筆(`n_reviews_ltm_eq_0_and_occ_gt0`、`n_reviews_ltm_gt0_and_occ_eq_0`)。
   - 所以收入 = 標價 × 由評論數換算的晚數,不含實收、折扣、清潔費或空置,拿它當「報酬」是在把模型輸出當觀察值。
2. **推算值有天花板與地板,新房源只有部分年**
   - 入住晚數最大值 255,頂到最大值的 423 筆(6.37%)/ 594 筆(7.22%)(`c_occupancy.max`、`at_max_pct`)。
   - 入住 = 0 的 824 筆(12.41%)/ 1,338 筆(16.27%)(`eq_0_pct`);近 12 個月沒評論的比例相同(`d_activity.reviews_ltm_eq_0_pct`)。
   - 首評在 12 個月內的 2,028 / 2,056 筆,其 l365d 不是整年,收入會被低估(`e_first_review_years.first_review_within_12m_before_batch`)。
3. **有價才有收入,缺價的多是封鎖日曆,成本與買價欄也不在這批資料裡**
   - 篩選樣本裡沒價格的有 926 筆(12.24%)/ 2,717 筆(24.84%)(`scope.a_price.price_missing`)。其中 `availability_365` = 0 的 791 / 2,532 筆(`price_missing_and_availability_365_eq_0`),多半是房東關日曆。
   - 收入欄只在有價者有值(全體 17,721 / 19,004 筆,`all.b_revenue_vs_price_x_occ.n_revenue_numeric`),所以估計只看得到有開放訂房的房源,對 B 偏樂觀。
   - 清潔費、押金、買價、租金等欄位,前一份盤點的關鍵字掃描沒有找到(見 `airbnb_ab_field_inventory_2026-11-11.json` 的 `keyword_scan`),本次沒重查。投資報酬的成本端要靠外部假設。

## 這次沒查到/不能下結論的事

- **新房東**:`host_since` 全空,無法驗證「首評年份」能不能代表新房東;重新上架、換房東的情況看不出來。
- **新房源 × 區**的筆數沒算,所以 A 能不能做到區級分析沒有答案。
- **`review_scores_*`**(A 的品質比較會用到)這次只有前一份盤點的缺值 %,沒查分布與是否集中在高分。
- **入住推算準不準**:本機沒有 calendar 檔,無法用實際訂房驗證 `estimated_occupancy_l365d`,只知道它是評論數的函數。
- **價格**是單日標價(不是實收);沒跟 calendar 價格比,也沒逐筆檢查最大值(18,848 / 90,000)是不是輸入錯誤。
- 檔內 `last_scraped` 是雪梨 2026-09-17、墨爾本 2026-09-17 至 09-18(JSON `last_scraped_min_max`),與「09-16 批次」差一天,不影響結論;首評「12 個月內」以檔內最後抓取日往前推(JSON `cutoff_date`)。
- 沒有跨批次比較(例如 2024 批次),看不出欄位品質有沒有隨時間變差。
- `bathrooms`(數字欄)全空(`j_bathrooms_text.bathrooms_numeric_missing_pct` = 100),浴室數只能靠 `bathrooms_text`。
