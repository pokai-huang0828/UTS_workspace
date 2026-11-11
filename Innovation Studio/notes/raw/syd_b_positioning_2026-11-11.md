# 雪梨 B 分支:競品定位、設施與價格、掛牌價預測(IS-1111-SYD-B)

- 資料:Inside Airbnb 雪梨 2026-09-16 期(全部 20,833 列);篩選(整套、1–2 房、2–4 人、最低 1–7 晚)後 7,565 間,其中有價 6,639 間。「區」= LGA。
- 價格是房東的「掛牌價」(澳幣/晚),不是成交價;每晚 > 2,000 的 24 間不進模型訓練與誤差。
- 模型樣本 6,615 間;固定隨機種子 42。

## 一、定位(前 10 大區,中位數 / p25–p75,括號 = 房源數)

| 區 | 1 房 | 2 房 |
|---|---|---|
| Sydney | 323 (266–389) n=1291 | 455 (366–565) n=564 |
| Waverley | 331 (272–425) n=387 | 522 (412–671) n=306 |
| North Sydney | 328 (268–396) n=234 | 446 (384–564) n=144 |
| Manly | 366 (287–442) n=237 | 575 (446–737) n=135 |
| Randwick | 310 (250–390) n=151 | 446 (366–575) n=167 |
| Auburn | 320 (282–386) n=132 | 378 (329–446) n=154 |
| Warringah | 285 (224–333) n=166 | 367 (314–479) n=108 |
| Pittwater | 308 (246–412) n=134 | 485 (404–591) n=80 |
| Woollahra | 338 (263–435) n=100 | 467 (385–698) n=92 |
| Sutherland Shire | 258 (204–333) n=113 | 350 (248–458) n=67 |

- 全市中位數:1 房 299(n=4,029),2 房 414(n=2,610);標 * = 該格不足 30 間。
- 分組:區×房間數共 76 組,93.1% 的房源在 30 間以上的組;其餘退回「最近 30 間」。

## 二、設施與價格(關聯,不是因果)

- BRAND (TBA) conditioner:同組中位數高 41.4%(迴歸控制後 48.9%,有此設施 44 間)
- Kayak:同組中位數高 31.1%(迴歸控制後 25.6%,有此設施 45 間)
- Indoor fireplace:同組中位數高 29.6%(迴歸控制後 26.9%,有此設施 94 間)
- Boat slip:同組中位數高 29.4%(迴歸控制後 20.5%,有此設施 31 間)
- River view:同組中位數高 25.3%(迴歸控制後 30.6%,有此設施 51 間)
- 負向最多(同組比較):Kitchenette -18.5%;Valley view -11.7%;Mini fridge -11.7%
- 兩種算法方向一致比例:88.7%(共 239 項可比設施)。

## 三、價格預測誤差(MAE,澳幣/晚,越低越好;5 折)

| 方法 | 依房東分組(主) | 隨機切(對照) | MdAPE% | 20% 內% |
|---|---|---|---|---|
| B0 全市中位數 | 122.5 | 122.4 | 26.0 | 40.1 |
| B1 區×房間數中位數 | 101.7 | 101.0 | 21.2 | 47.8 |
| M1 線性(Ridge) | 95.7 | 95.1 | 19.7 | 50.5 |
| M2 梯度提升樹 | 93.4 | 88.7 | 18.9 | 51.9 |
| M1 + 房東房源數(對照) | 94.7 | 94.0 | 19.5 | 51.0 |
| M2 + 房東房源數(對照) | 92.6 | 86.7 | 18.7 | 52.5 |

- 最好的是 M2(MAE 93.4),比 B0 全市中位數好 24%、比 B1 區×房間數好 8%。
- 加房東房源數(對照)後 M2 MAE 92.6(沒加 93.4),差距很小;M2 隨機切比分組切低 4.7,同房東房源互相「提示」造成偏樂觀。
- 正向設施的有此設施房源數多半只有幾十間(見上),排名容易受少數房源影響,宜看方向與迴歸是否一致。
- 時間外部檢查(用 2026-06-16 訓練、猜 821 間新出現的房源):B0 122.0;B1 103.2;M1 99.3;M2 94.1。

## 怎麼讀

- 誤差 = 猜中「別人掛多少」的能力,不是「定多少訂得出去」。
- 沒用評論、評分、可訂天數、營收等上架後才有的欄位,以免洩漏答案。
- 房東分組切法(同房東不跨訓練/測試)才接近新房東的情況,以它為主結果。

## 雪梨 vs 墨爾本

墨爾本數字取自 `Innovation Studio/notes/raw/mel_b_positioning_2026-11-11.json` 的各 key(見最右欄)。

| 項目 | 雪梨 | 墨爾本 | 墨爾本取自 key |
|---|---|---|---|
| 篩選且有價房源數 | 6,639 | 8,223 | reconciliation.rows_scope_price |
| 全部價格中位數 | 338.5 | 264.0 | price_distribution.p50 |
| 1 房中位數 | 299.0 | 230.0 | b_positioning.city_by_bedrooms.1.p50 |
| 2 房中位數 | 414.1 | 310.8 | b_positioning.city_by_bedrooms.2.p50 |
| 列入定位表的區數(≥30 間) | 33 | 27 | b_positioning.n_districts |
| 組≥30 間涵蓋的房源 % | 93.1 | 94.7 | a_grouping.pct_listings_in_groups_ge30 |
| 排除的極端值間數 | 24 | 14 | extreme_rule.n_excluded |
| MAE B0(依房東分組) | 122.5 | 87.4 | d_experiment.results_group_cv.B0.all.MAE_aud |
| MAE B1(依房東分組) | 101.7 | 78.4 | d_experiment.results_group_cv.B1.all.MAE_aud |
| MAE M1(依房東分組) | 95.7 | 75.2 | d_experiment.results_group_cv.M1.all.MAE_aud |
| MAE M2(依房東分組) | 93.4 | 75.1 | d_experiment.results_group_cv.M2.all.MAE_aud |
| M2 的 MdAPE % | 18.9 | 19.2 | d_experiment.results_group_cv.M2.all.MdAPE_pct |
| M2 的 20% 內 % | 51.9 | 51.9 | d_experiment.results_group_cv.M2.all.within20_pct |
| 最佳模型 | M2 | M2 | d_experiment.best_model |
| 時間外部檢查 M2 MAE | 94.1 | 70.9 | d_temporal_check.results.M2.MAE_aud |
| 設施數中位數 | 41.0 | 41.0 | c_amenities.amenity_count_distribution.p50 |
| 同組比較正向前 3 設施 | BRAND (TBA) conditioner、Kayak、Indoor fireplace | BBQ grill: gas、Stainless steel double oven、Indoor fireplace: gas | c_amenities.association.top10_positive[:3].amenity |
