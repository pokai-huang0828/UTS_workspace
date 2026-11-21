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


---

## 追加(2026-11-21,工單 IS-1121-TRAIN-B):另外兩群房源的訓練表

組長要求「房源資料全部都要訓練」。上面是第一次訓練(整套、1–2 臥、可住 2–4 人、最少 1–7 晚)的表,下面是另外兩群。只用 2026-09-16 期(`listings_2026-09-16.csv.gz`,20,833 列,sha256 前 16 碼 `06bbd629fbe93d9d`)。產生指令:`python "Innovation Studio/model_training/src/01_build_dataset.py" --group private_room`(或 `entire_home_all`);不加 `--group` = 第一次訓練那群,行為不變。

### 02 獨立房間(`private_room`)每一步剩幾列

| 步驟 | 條件 | 剩幾列 |
|---|---|---|
| 0 | 2026-09 期原始 | 20,833 |
| 1 | `room_type == 'Private room'` | 4,282(其中 price 非空 3,726,和主腦給的參考值相同) |
| 2 | `accommodates` 純數字且 1–4 | 4,163(沒有非純數字的) |
| 3 | `minimum_nights` 純數字且 1–7 | 3,213(另有 6 列非純數字,被排除) |
| 4 | `price` 非空 | 2,916 |
| 5 | 去掉每晚 > 2,000 澳元的 1 列(價格 3,000) | **2,915**(房東 1,057 位) |

- 臥室數原始值(步驟 3 之後):1 間 3,028、2 間 97、0 間 59、3 間 21、4 間 5、5 間 2、空 1。空的補 1 並加旗標 `bed_missing`(只有 1 列是空的);0 照原值 0(57 間在有價的 2,915 間裡)。
- 可住人數、最少入住晚數在這個範圍內沒有缺值(`acc_missing`、`min_missing` 全為 0,不進模型)。
- 價格:中位數 130、平均 154.4、最低 28、最高 1,258。
- `bathrooms_text` 含 "shared"(共用衛浴)的比例 59.3%(步驟 3 之後的 3,213 列);模型沒有這個欄(沿用第一次訓練的浴室數解析,只取數字)。

### 03 全部整套房(`entire_home_all`)每一步剩幾列

| 步驟 | 條件 | 剩幾列 |
|---|---|---|
| 0 | 2026-09 期原始 | 20,833 |
| 1 | `room_type == 'Entire home/apt'` | 16,445 |
| 2 | `price` 非空 | 13,899(和主腦給的數字相同;**包含**第一次訓練的 6,639 間) |
| 3 | 去掉每晚 > 3,000 澳元的 214 列(價格 3,008–96,887.58) | **13,685**(房東 6,737 位) |

- 其中屬於第一次訓練那 6,615 間的:6,615(以 id 對,已核對恰好 6,615);在 6,615 之外的:7,070。表內 `in_run01` 欄 = 1 表示屬於那 6,615 間。
- `bedrooms`、`accommodates`、`minimum_nights` 不設範圍;空的或非純數字的補中位數並各加旗標(用有價的 13,899 列的中位數:臥室 2、可住人數 4、最少晚數 2):臥室缺 20 列、可住人數缺 0 列、最少晚數缺 5 列。
- 臥室數(補值後):0 間 733、1 間 4,543、2 間 4,560、3 間 2,100、4 間 1,134、5 間 497、6 間以上 118。可住人數 1–16;最少入住晚數 1–365(中位數 2)。價格:中位數 390、平均 509.2、最低 56.1、最高 3,000。
- 補值的中位數用該群全部列算(只看特徵,沒看價格;包含之後會被切進測試集的列),影響極小,但嚴格說不是「只用訓練集」。

| 檔名 | 用途 | 列數 | 房東數 | sha256 |
|---|---|---|---|---|
| `train_table_2026-09_private_room.csv` | 02 獨立房間主訓練表 | 2,915 | 1,057 | `9bde612cb8138b21e468afacd8ef54398dfcfe9020212e42131bbea6a52e310b` |
| `extremes_dropped_private_room.csv` | 02 被拿掉的極端值(每晚 3,000) | 1 | 1 | `1bad2b65d60427247835c20085ef757e3c6ac745cf2697d6dcdf4a7021d3e544` |
| `train_table_2026-09_entire_home_all.csv` | 03 全部整套房主訓練表 | 13,685 | 6,737 | `2d92e57e9d6fb84b71a69c2ecd282b7a017640b01878d209edc40ba326439ee7` |
| `extremes_dropped_entire_home_all.csv` | 03 被拿掉的極端值(每晚 3,008–96,887.58) | 214 | 84 | `e4c85ed0d54566945f6e74e928d285334523ecc407de9e373249112209c0b2ca` |

欄位:同上面 17 欄,再加 4 欄:`bed_missing`、`acc_missing`、`min_missing`(原本是不是缺的,1 = 缺)和 `in_run01`(是否屬於第一次訓練的 6,615 間;02 獨立房間全為 0)。這兩群的 `bedrooms` 欄是補值後的臥室數(文字),B1 基準用它分組。進模型的缺值旗標:02 只有 `bed_missing`;03 有三個(`acc_missing` 全為 0,是常數欄,對預測沒作用)。
