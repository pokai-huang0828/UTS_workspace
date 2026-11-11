# 雪梨分支 A 市場概況(IS-1111-SYD-A,2026-11-11)

主體 2026-09-16 一期;calendar 用四期。資料 scratchpad/insideairbnb_sydney(唯讀)。腳本 analysis/sydney/syd_a_market.py;數字全部來自同名 .json。
掛牌價是掛牌(每晚),不是成交價;推算入住與日曆可訂天數都是需求代理,不是真實入住。

## 對賬

| 項目 | 數 |
|---|---|
| 全體列數 | 20,833 |
| 篩選樣本(整套房、1-2 房、2-4 人、最低 1-7 晚) | 7,565 |
| 篩選且有價 | 6,639 |
| 全體有價(price 非空) | 17,721 |

## a 供給長相

| 房型 | 房源數 | 占比 |
|---|---|---|
| 整套房 | 16,445 | 78.9% |
| 獨立房間 | 4,282 | 20.5% |
| 飯店房間 | 58 | 0.3% |
| 合住房間 | 48 | 0.2% |

| 房東規模(以房源為分母) | 房源數 | 占比 |
|---|---|---|
| 名下 1 間 | 7,634 | 36.6% |
| 名下 2-4 間 | 3,764 | 18.1% |
| 名下 5 間以上 | 9,435 | 45.3% |

| 前 8 種 property_type | 房源數 | 占比 |
|---|---|---|
| Entire rental unit | 9,806 | 47.1% |
| Entire home | 4,413 | 21.2% |
| Private room in home | 2,234 | 10.7% |
| Private room in rental unit | 1,037 | 5.0% |
| Entire guesthouse | 482 | 2.3% |
| Entire condo | 379 | 1.8% |
| Entire guest suite | 373 | 1.8% |
| Entire townhouse | 252 | 1.2% |

## b 掛牌價

| 範圍 | n | p25 | p50 | p75 | p90 |
|---|---|---|---|---|---|
| 全體有價 | 17,721 | $209 | $338 | $514 | $874 |
| 房型:整套房 | 13,899 | $284 | $394 | $583 | $1,008 |
| 房型:飯店房間 | 53 | $228 | $291 | $351 | $406 |
| 房型:獨立房間 | 3,726 | $91 | $125 | $179 | $260 |
| 房型:合住房間 | 43 | $58 | $66 | $78 | $158 |
| 整套房 1 房 | 4,557 | $230 | $293 | $373 | $468 |
| 整套房 2 房 | 4,553 | $319 | $408 | $525 | $704 |
| 整套房 3 房 | 2,123 | $422 | $567 | $824 | $1,224 |
| 整套房 4 房 | 1,207 | $559 | $850 | $1,468 | $2,323 |
| 整套房 5以上 房 | 1,439 | $255 | $421 | $1,014 | $2,277 |
| 整套房 缺值 房 | 20 | $173 | $214 | $290 | $356 |

p99 = $3,482;高於 p99 共 178 間;最高掛牌價 $96,888。直方圖只畫到 p99。

## c/d 分區與地圖(區 = neighbourhoods.geojson 的 LGA)

| 區 | 房源數 | 篩選且有價 | 價格中位數 | 評分中位數 |
|---|---|---|---|---|
| Sydney | 5,024 | 1855 | $355 | 4.80 |
| Waverley | 1,796 | 693 | $407 | 4.88 |
| Randwick | 1,115 | 318 | $373 | 4.88 |
| Manly | 935 | 372 | $414 | 4.89 |
| Pittwater | 931 | 214 | $373 | 4.95 |
| Warringah | 890 | 274 | $315 | 4.94 |
| North Sydney | 791 | 378 | $375 | 4.86 |
| Auburn | 720 | 286 | $350 | 4.78 |
| Woollahra | 629 | 192 | $404 | 4.88 |
| Sutherland Shire | 517 | 180 | $287 | 4.91 |

共 38 區;樣本少於 10 間不報中位數的區 2 個(Hunters Hill、Hurstville)。價格中位數最低 Fairfield $216、最高 Manly $414。

## e 需求代理

推算近一年入住晚數(篩選且有價 6,639 間):中位數 60、平均 85.0;0 晚占 12.4%;達上限 255 占 6.4%。

| 窗口 | 可訂天數 p50 | 占窗口 | 可訂天數 = 窗口全部(完全沒被擋)占比 | 可訂天數 = 0(完全不可訂)占比 |
|---|---|---|---|---|
| 未來 30 天 | 10.0 | 33% | 2.4% | 14.7% |
| 未來 90 天 | 45.0 | 50% | 1.9% | 6.0% |
| 未來 365 天 | 164.0 | 45% | 0.2% | 0.0% |

| 期別 | 季節 | calendar 房源數 | 後 30 天不可訂 | 後 60 天不可訂 | 後 90 天不可訂 |
|---|---|---|---|---|---|
| 2025-12-12 | 12月(夏) | 20,436 | 62.6% | 53.4% | 51.0% |
| 2026-03-21 | 3月(秋) | 13,563 | 55.0% | 44.2% | 38.3% |
| 2026-06-16 | 6月(冬) | 20,573 | 48.7% | 44.1% | 42.0% |
| 2026-09-16 | 9月(春) | 20,833 | 58.5% | 53.0% | 49.3% |

不可訂 = 被訂走或房東自己關閉,分不出來。

## f 評分

有評分 17,623 間(占 84.6%);中位數 4.84;5.0 占 25.0%;4.5 以上占 85.5%;低於 4 占 3.5%。

| 價格分組(篩選且有價) | 價格範圍 | 評分中位數 |
|---|---|---|
| Q1(最便宜 25%) | $79–$260 | 4.83 |
| Q2 | $260–$338 | 4.83 |
| Q3 | $339–$442 | 4.85 |
| Q4(最貴 25%) | $442–$18,848 | 4.90 |

## 圖

syd_a_calendar_blocked.png、syd_a_demand_proxy.png、syd_a_map_listing_count.png、syd_a_map_price_median.png、syd_a_price_hist.png、syd_a_rating.png、syd_a_supply.png

## 雪梨 vs 墨爾本

墨爾本數字取自 `notes/raw/mel_a_market_2026-11-11.json`,最右欄為該檔的 key 路徑(同一路徑雪梨 JSON 也有)。兩城篩選與 price 解析定義相同;兩城都在南半球,季節標籤同。

| 指標 | 雪梨 | 墨爾本 | 墨爾本 key |
|---|---|---|---|
| 全體房源數 | 20,833 | 25,715 | `meta.recon.listings_rows` |
| 篩選樣本數 | 7,565 | 10,940 | `meta.recon.scope_rows` |
| 篩選且有價數 | 6,639 | 8,223 | `meta.recon.scope_with_price_rows` |
| 整套房占全體 | 78.9% | 73.7% | `a_supply.room_type.Entire home/apt.share` |
| 私人房間占全體 | 20.5% | 25.2% | `a_supply.room_type.Private room.share` |
| 房源屬名下 1 間房東 | 36.6% | 43.6% | `a_supply.host_concentration.1.share` |
| 房源屬名下 5 間以上房東 | 45.3% | 35.8% | `a_supply.host_concentration.5_plus.share` |
| 有價房源數 | 17,721 | 19,004 | `b_price.n_priced_all` |
| 全體有價 掛牌價中位數 | $338 | $263 | `b_price.all_priced.p50` |
| 整套房 1 房 掛牌價中位數 | $293 | $229 | `b_price.entire_by_bedrooms.1.p50` |
| 整套房 2 房 掛牌價中位數 | $408 | $309 | `b_price.entire_by_bedrooms.2.p50` |
| 篩選且有價 掛牌價中位數 | $338 | $264 | `f_rating.scope_priced_price_quartile_cuts.1` |
| 推算入住晚數中位數(篩選且有價) | 60 | 60 | `e_demand.occupancy_proxy.median` |
| 推算入住 0 晚占比 | 12.4% | 16.3% | `e_demand.occupancy_proxy.share_zero` |
| 推算入住達上限 255 占比 | 6.4% | 7.2% | `e_demand.occupancy_proxy.share_at_cap` |
| 未來 30 天可訂占比中位 | 33.3% | 40.0% | `e_demand.availability_proxy.by_window.30.pct_of_window.p50` |
| 未來 90 天可訂占比中位 | 50.0% | 61.1% | `e_demand.availability_proxy.by_window.90.pct_of_window.p50` |
| 2025-12-12 日曆後 30 天不可訂占比 | 62.6% | 65.6% | `e_demand.calendar_blocked.periods.2025-12-12.all.30.blocked_share` |
| 2025-12-12 日曆後 90 天不可訂占比 | 51.0% | 56.6% | `e_demand.calendar_blocked.periods.2025-12-12.all.90.blocked_share` |
| 2026-03-21 日曆後 30 天不可訂占比 | 55.0% | 47.5% | `e_demand.calendar_blocked.periods.2026-03-21.all.30.blocked_share` |
| 2026-03-21 日曆後 90 天不可訂占比 | 38.3% | 31.3% | `e_demand.calendar_blocked.periods.2026-03-21.all.90.blocked_share` |
| 2026-06-16 日曆後 30 天不可訂占比 | 48.7% | 51.9% | `e_demand.calendar_blocked.periods.2026-06-16.all.30.blocked_share` |
| 2026-06-16 日曆後 90 天不可訂占比 | 42.0% | 46.3% | `e_demand.calendar_blocked.periods.2026-06-16.all.90.blocked_share` |
| 2026-09-16 日曆後 30 天不可訂占比 | 58.5% | 62.8% | `e_demand.calendar_blocked.periods.2026-09-16.all.30.blocked_share` |
| 2026-09-16 日曆後 90 天不可訂占比 | 49.3% | 52.5% | `e_demand.calendar_blocked.periods.2026-09-16.all.90.blocked_share` |
| 有評分占全體 | 84.6% | 82.2% | `f_rating.all_rated.share_rated` |
| 評分中位數 | 4.84 | 4.86 | `f_rating.all_rated.p50` |
| 評分 5.0 占比 | 25.0% | 25.7% | `f_rating.all_rated.share_5_0` |
| 房源數最多的區(個數) | 5,024 | 8,422 | `d_maps.top8_by_listings.0.n_listings` |

房源數最多的區:雪梨 Sydney(5,024 間,占全體 24.1%);墨爾本 Melbourne(8,422 間,占全體 32.8%),取自 `c_districts.districts.<區>.n_listings`。

注意:兩城有價比例不同(有價占全體:雪梨 85.1%、墨爾本 73.9%),價格是掛牌價,單位為資料原值($),未做任何調整。
