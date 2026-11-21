# 資料清單(DATA_MANIFEST)

`raw/` 和 `processed/` 不進版控(repo 公開,資料不重新發布)。要重建:把原始檔放回 `raw/`,跑 `src/01_build_dataset.py`。下面的列數、sha256 都是 2026-11-21 實跑 `01_build_dataset.py` 印出來的。

## 原始檔(raw/)

| 檔名 | 來源 | 期別 | 列數 | sha256 |
|---|---|---|---|---|
| `listings_2026-09-16.csv.gz` | Inside Airbnb 雪梨 `listings.csv.gz`(本機複本:`scratchpad/insideairbnb_sydney/2026-09-16/data/listings.csv.gz`) | 2026-09-16 | 20,833 | `06bbd629fbe93d9da1f2163e82d584a58738a53d7897d5c081f665aadc4e3c55` |
| `listings_2026-06-16.csv.gz` | 同上(`.../2026-06-16/data/listings.csv.gz`) | 2026-06-16 | 20,573 | `56c7b83723a195d6e4d0bf6d6ecd6da9b43b00cda9c9f6c08ffe11b7ee79597d` |

複製後和 scratchpad 原檔 sha256 一致。只讀這 14 欄:id、host_id、room_type、property_type、accommodates、bedrooms、beds、bathrooms_text、neighbourhood_cleansed、latitude、longitude、minimum_nights、price、amenities。不讀房東姓名、房源名稱、描述、網址、評論。

## 清洗規則(照抄 `analysis/sydney/syd_b_positioning.py`,行號見 `src/common.py`)

1. **篩選**(syd_b 第 68–72 行):room_type = Entire home/apt;bedrooms 是 1 或 2;accommodates 2–4;minimum_nights 1–7。
2. **有價**(第 98–101 行):price 不是空的;去掉 `$`、`,` 轉成數字。
3. **欄位整理**(第 102–118 行):床數缺 → 用臥室數補(另記缺值旗標);浴室文字解析成數字(half → 0.5;缺 → 1,另記旗標);設施 JSON 解析成集合、算設施數;區 = neighbourhood_cleansed(雪梨是 LGA)。
4. **去極端值**(第 45 行):每晚 > 2,000 澳元的不進模型(另存一檔)。
5. **時間外測試集**(第 643–651 行):9 月 6,615 間裡,id 沒出現在 6 月**整期** listings(不只篩選後)的。

## 每一步剩幾列

| 步驟 | 2026-09-16 | 2026-06-16 |
|---|---|---|
| 原始 | 20,833 | 20,573 |
| 篩選後 | 7,565 | 7,617 |
| 有價 | **6,639**(assert) | 6,763 |
| 去掉 > 2,000 澳元 | 去 24 → **6,615**(assert) | 去 16 → **6,747**(assert) |
| 6 月沒出現過的 id | **821**(assert) | — |

## 處理後的檔(processed/,utf-8)

| 檔名 | 用途 | 列數 | 房東數 | sha256 |
|---|---|---|---|---|
| `train_table_2026-09.csv` | 主訓練表(切 80/20、5 折、最終模型) | 6,615 | 3,689 | `b87292a063e51033b06ceebe50f0ce637532c1677f95915dce1b1f9c81b94cc1` |
| `extremes_dropped_24.csv` | 被拿掉的極端值(每晚 2,147.67–18,848) | 24 | 9 | `4e177f7289f08a802833d54cf95438333129b0e3829201b1ed55e192d68769f6` |
| `timeout_train_2026-06.csv` | 時間外驗證的訓練(6 月) | 6,747 | 3,729 | `654484efbda68f8d24a531c2cf2cea013f3dd1b673462316b4c0d85ef1e9157a` |
| `timeout_test_2026-09_new.csv` | 時間外驗證的測試(9 月新 id) | 821 | 569 | `c547a502b64d9aac56ba65954999de4e2de01f7cd3472313375a943795502b18` |

## 欄位說明(四個檔都一樣,17 欄)

| 欄 | 意思 | 進模型? |
|---|---|---|
| id | 房源編號 | 否(只用來對時間外的新舊) |
| host_id | 房東編號 | 否(只用來分組切資料) |
| nb | 區(neighbourhood_cleansed) | 是 |
| property_type | 房型細類(不足 30 間的歸 Other) | 是 |
| bedrooms | 臥室數(文字,做 B1 的組別用) | — |
| lat, lon | 緯度、經度 | 是 |
| bed_n | 臥室數(數字) | 是 |
| acc | 可住人數 | 是 |
| beds_n | 床數(缺值已用臥室數補) | 是 |
| beds_missing | 床數原本是不是缺的 | 否(syd_b 樹模型也沒用) |
| baths | 浴室數(缺值補 1) | 是 |
| baths_missing | 浴室原本是不是缺的 | 否 |
| min_n | 最少入住晚數 | 是 |
| amen_n | 設施數 | 是 |
| amenities | 設施原始 JSON 清單;模型用其中「訓練集出現比例前 40 項」做成 40 個有/沒有 | 是(轉成旗標) |
| price_num | 每晚掛牌價(澳元)— 要猜的答案,模型學的是 ln(price_num) | 答案 |

禁用欄(評論數、評分、估算入住/收入、availability、price_quote、房東經營資料)在讀檔時就沒有讀進來。
