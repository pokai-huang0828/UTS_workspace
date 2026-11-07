TL;DR：Inside Airbnb 可做房源供給、刊登價格與評論分析；沒有可供驗證的訂單取消結果，不能直接做 Airbnb 訂單取消預測。價格模型須先處理報價日期不一致與缺值，且只代表刊登／報價，不代表成交或最優價格。

# Airbnb 公開資料與專案可行性實查（2026-11-07）

> 範圍 IS-1107-AIR；2 次搜尋查詢、官方頁面與資料字典核對、Sydney 一份 listings 全量下載；calendar／reviews 只串流讀表頭。未跑模型，以下專案設計均為建議。原始房源資料只留 scratchpad，不進版控。

## 1. 一手資料來源與使用界線

| 來源 | 本次實查 | 對作業的意義 |
|---|---|---|
| [Inside Airbnb 下載入口](https://insideairbnb.com/get-the-data/) | Sydney 顯示 2026-09-16；提供 listings、calendar、reviews、neighbourhoods；公開資料通常為近 12 個月的季度快照 | 不是每日訂單串流；歷史快照範圍有限，舊檔需另申請 |
| [Data Assumptions](https://insideairbnb.com/data-assumptions/) | 非 Airbnb 官方資料；日曆無法區分已預訂與房東封鎖；位置經模糊化 | 不可訂不等於成交、入住或取消；精確地址與極近距離分析有誤差 |
| [Data Policies](https://insideairbnb.com/data-policies/)＋下載入口 | 下載入口標 CC BY 4.0、要求註明來源；站方另請求不要重新發布整份資料、不要反覆下載或爬站 | 報告正式引用資料集；repo 留腳本、彙總與來源，不放原始姓名／評論全文資料庫；「不要重發布」是站方社群請求，勿誤寫成 CC BY 禁止重發布 |
| [官方連結的資料字典](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit) | 顯示 v4.3、2022-08；描述 price 為當地幣別日價、availability 為未來可訂天數 | 現場檔已增欄，字典不是完整的當前 schema；分析前須核實實檔 |

## 2. Sydney 實際下載與品質

- [listings 全量原檔](https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/listings.csv.gz)：HTTP 200、12,747,164 bytes；解壓為 **20,833 列 × 90 欄**；20,833 個唯一 id、9,769 個 host_id。
- SHA-256：`06bbd629fbe93d9da1f2163e82d584a58738a53d7897d5c081f665aadc4e3c55`。
- **日期必須分開記**：下載目錄與入口是 **2026-09-16**，全部列的 `last_scraped` 卻是 **2026-09-17**；兩者均保留，不自行修成同一天。這是 9 月快照，不能稱 11 月即時市場。
- 房型：Entire home/apt 16,445；Private room 4,282；Hotel room 58；Shared room 48；合計 20,833。

| 欄位／現象 | 實算結果 | 影響與最小處理 |
|---|---:|---|
| price 空白 | 3,112／20,833＝14.94% | 有價樣本 17,721；先比較缺價／有價房源的地區與房型，不用平均數補目標值 |
| review_scores_rating 空白 | 3,210／20,833＝15.41% | 不可把無評論當零分；僅對有評分房源做評分分析並標分母 |
| bathrooms 空白 | 20,833／20,833＝100% | 不可承諾直接使用數值浴室欄；bathrooms_text 僅缺 24，可另訂簡單文字解析規則 |
| bedrooms 空白 | 22 | 可保留缺值指標或使用訓練集統計填補 |
| price_quote_price_per_night 空白 | 3,113 | 不是每列均有可用報價；其與 price 的實際關係尚未檢查 |
| price_quote_checkin_date／checkout_date | 各缺 2,725；非空值跨多個日期 | 房源間報價不一定是同一入住日或住宿晚數，混合比較有偏差；報價日期須控制或限定同一區間 |
| estimated_occupancy_l365d | 欄位存在、0 空白 | 名稱即標估計；不可當真實入住標籤 |
| estimated_revenue_l365d | 欄位存在、3,112 空白 | 不可當真實帳務收入；避免用其做「收益預測」再以同來源估計評分 |
| 含 cancel 的欄名 | 0 | 此房源檔無取消結果欄；也沒有一列一訂單的記錄結構 |

注意：缺值以上以 CSV 空字串計算，未完成所有數值欄的零值、異常值與語意稽核；不應把它說成已清理好的訓練資料。

官方 Data Assumptions 有以評論推估入住與收入的模型說明；本次未找到能逐項追溯這版兩個 `estimated_*_l365d` 欄位的完整生成規格，不把頁面的舊模型直接當作這版精確公式，也不把完整非空視為結果真實性的證明。

## 3. 三份表能支持什麼

| 表 | 實檔粒度與已確認欄位 | 可以做 | 不能直接推斷 |
|---|---|---|---|
| listings | 一列一房源；id、host_id、neighbourhood_cleansed、room_type、accommodates、bedrooms、amenities、price、評分、availability、price_quote_*、estimated_* | 房型／地區供給比較、刊登價比較、房源屬性與刊登價關聯 | 一列一訂單、訂單是否取消、實際成交價、價格調整的因果效果 |
| [calendar](https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/calendar.csv.gz) | 本次表頭：listing_id、date、available、minimum_nights、maximum_nights；HTTP 200 | 未來可訂狀態與最少入住晚數分布 | **這版沒有 price**，不能承諾逐日價格曲線；不可訂也不是已售出 |
| [reviews](https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/reviews.csv.gz) | 本次表頭：listing_id、id、date、reviewer_id、reviewer_name、comments；HTTP 200 | 評論量、文字面向、抱怨內容分析 | **沒有逐則星等**；不能把房源平均評分複製到每則評論當人工真值 |

calendar／reviews 僅確認表頭，未驗總列數、日期範圍、主鍵唯一性與缺值；不把官方「未來 365 天」描述當成這份檔案已逐列驗收的結果。

## 4. 取消預測的 go／no-go

**以本次公開 Inside Airbnb 檔案作 Airbnb 取消預測：no-go。** 理由是沒有真實預訂與取消結果，不是資料列數不足。

只有取得有權使用、已去識別的訂單資料，並同時滿足以下條件，才值得改判：

1. 一列一筆預訂，有穩定 booking_id、建立時間、入住日期與最終取消／完成結果；能說清楚 no-show 如何標記。
2. 有可重建的「預測當時」特徵版本；不能拿取消後才更新的欄位預測取消。
3. 有足夠的成熟結果與連續時間，能把未來時段留作測試；足夠樣本須看取消數與分段穩定性，不預先編造最低筆數。
4. 業務可明確說出誰使用預測、何時採取何種行動，並取得資料使用同意。

**不可替代做法**：把 calendar 從 f 變 t 當成取消、把房源消失當取消、把 estimated occupancy 當訂單、把合成訂單訓練分數當真實成效。這些可做情境演示，不能驗證 Airbnb 真實取消預測。

酒店取消資料可支持「酒店」模型；無 Airbnb 訂單測試集時，不可將其重新命名為已驗證的 Airbnb 模型（方法論推論）。

## 5. 若隊伍偏好 Airbnb，最小可做題目

**建議題名：Sydney Airbnb 房源市場比較與刊登價估計。** 業務對象是房源營運者／分析人員；輸入地區、房型、容量等條件，顯示相似房源的刊登價分布、可訂狀態與簡單估計。主張限於「公開市場比較」，不承諾提高收益。

- **核心交付（可直接開始）**：一座城市、一個快照、供給與房型分布、分組刊登價分布、資料限制卡；不用先接外部付費 API。
- **ML 子任務（有條件）**：先確認 price／price_quote_price_per_night 的語意與日期可比性，再選一種目標；基準為訓練集的「地區×房型中位數」，比較一個樹模型。若日期混雜無法說清楚，降為描述性價格比較，不硬湊預測。
- **分割**：同一 host_id 的房源歸同一折，減少同營運者資訊滲漏；前處理只用訓練集估計。有另一快照時再加時間外測試，單快照不能宣稱預測未來定價。
- **特徵**：地區、房型、容量、臥室、設施；若目標為具日期報價，納入其入住日與晚數。禁用同列其他價格欄、estimated_revenue、price_quote_raw 或由目標推算的欄位預測該目標。
- **驗收**：固定留出樣本上的 MAE 與分房型誤差，對照中位數基準；展示實際誤差與樣本量，不先承諾某個準確率。價格模型可輸出估計範圍，不稱「最佳價格」。
- **介面**：篩選地區／房型→顯示同類房源分布→輸入屬性→刊登價估計＋限制；最多加一頁評論主題，避免地圖、活動預測、收益最佳化同時開工。
- **創新點（建議）**：把可解釋的比較、報價日期限制、人工覆核連成決策流程；單純做房價迴歸較普通，不能靠套 LLM 名稱補分。

若改做「評論改善助手」，另需人工標註一批評論的面向與情感；房源平均星等不是逐則標籤，且評論有選擇偏差與多語言清理成本。可做，但比現成標籤的酒店取消更耗人工（可行性判斷）。

## 6. 四人分工與範圍

| 既有職責 | 可獨立驗收的成果 |
|---|---|
| 項目負責 | 明定資料使用範圍、研究問題、時程與驗收；維護來源與風險表 |
| 開發 | 固定快照載入、資料版本／快取、篩選介面與模型呼叫；先做本機離線展示 |
| Kenny：數據分析＋開發 | 缺值／異常與價格語意稽核、基準與模型、host 分組評估、誤差分析 |
| 報告呈現／業務理解／利害關係人 | 相似房源定義、人工評估展示案例、解讀結果、報告與簡報；不把關聯講成因果 |

**選題判斷**：有現成資料且能落地，但「取消預測」無標籤；作業若要求可靠監督式預測，酒店取消更直接。Airbnb 題需願意把問題改成房源／刊登價分析，且接受日期可比性稽核後可能縮小 ML 範圍。

## 7. 可重算證據

本機留存 `scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz` 及不含個人文字的 `profile.json`。全量 listings 已以 Python csv/gzip 計算，calendar/reviews 僅讀首列。

```python
import csv, gzip, hashlib
from pathlib import Path
p = Path('scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz')
with gzip.open(p, 'rt', encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == len({r['id'] for r in rows}) == 20833
assert len(rows[0]) == 90
assert sum(not r['price'] for r in rows) == 3112
assert {r['last_scraped'] for r in rows} == {'2026-09-17'}
assert not any('cancel' in c.lower() for c in rows[0])
assert hashlib.sha256(p.read_bytes()).hexdigest() == '06bbd629fbe93d9da1f2163e82d584a58738a53d7897d5c081f665aadc4e3c55'
```

未做：calendar／reviews 全量稽核、模型實驗、商用資料供應商授權審查、中國大陸網路實測。主要風險是把估計或公開可訂狀態誤當交易真值，以及報價日期混雜。
