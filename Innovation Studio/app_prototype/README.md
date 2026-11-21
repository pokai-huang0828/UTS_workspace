# app_prototype:民宿營運助手的「計算核心」原型

這個資料夾是報告裡那個 App 的**計算部分**,能真的跑。輸入一間房的條件,它會算出同類房源、價格位置、設施差距、收入情景、淡旺季參考,然後寫成一頁網頁(HTML)。

它**不是**正式的 App:沒有網頁伺服器、沒有登入、不能線上用。七個功能裡 T1、T2、T3、T6、T7 能算;T4、T5(讀評論)接上的是「示範」:拿已讀過評論的 10 間房之一來演,不是你輸入的那間房。每個功能做到哪,看 [STATUS.md](STATUS.md)。

## 怎麼跑(在 repo 根目錄)

```
# 報告附錄 B 的例子:Sydney 區、1 臥、可住 2 人、1 床、1 浴,已有 Kitchen、Washer、Wifi,打算開 300 澳元/晚
python "Innovation Studio/app_prototype/demo.py" --nb Sydney --bedrooms 1 --acc 2 --beds 1 --baths 1 --amen "Kitchen,Washer,Wifi" --price 300

# T4、T5 示範要用哪一間已讀過評論的房(房源A–J,預設 房源C):加 --review-demo 房源A

# 煙霧測試(50 項,全過會印「共 50 項,過 50 項」)
python "Innovation Studio/app_prototype/tests/smoke_test.py"
```

其他可填的:`--cost`(一年的成本,收入會扣掉)、`--lat/--lon`(房子位置;不填就用該區房源的中間位置)、`--threshold`(設施差距門檻,預設 0.80)、`--year`(列哪一年的公眾假期)、`--name`(輸出檔名)、`--review-demo`(T4、T5 示範哪一間)。設施要用資料裡的英文名稱(不分大小寫);對不到的會列出「沒有算進去」。臥室數只支援 1 或 2、可住人數 2–4、區名要在資料裡,不符會印中文錯誤訊息。

跑完會在 `outputs/` 寫出兩份:
- `*_public.html`:可以給別人看。同類清單只列區、臥室、可住人數、設施數、相似度。
- `*_local.html`:多列房源 id 和匹配理由,**只留本機,不進版控**。

## 資料夾裡有什麼

| 檔案 | 做什麼 |
|---|---|
| `core/data_access.py` | 讀資料。房源從 `model_training/data/` 讀;評論檔只讀「房源 id、日期」兩欄;日曆只讀「房源 id、日期、可不可訂」 |
| `core/peers.py` | T1 找同類 |
| `core/pricing.py` | T2 價格位置 + 模型參考價(用 `model_training/runs/run_2026-11-21_01/` 存好的模型) |
| `core/amenities.py` | T3 設施差距 |
| `core/income.py` | T6 年收入情景(排除估計 0 晚的同類房源) |
| `core/season.py` | T7 淡旺季參考 |
| `core/reviews.py` | T4、T5 示範:讀 `review_analysis/runs/run_2026-11-21_listing10/` 的彙總檔(summary.json、listing_summary_*.csv;不讀評論原文)。公開版只讀只有代號的那份 |
| `core/report.py` | 把結果組起來、寫成一頁 HTML |
| `demo.py` | 命令列入口 |
| `tests/smoke_test.py` | 煙霧測試 |
| `data/` | 第一次跑時從評論檔、日曆檔算出的彙總表(每間房每月幾則評論、每月幾天不可訂)。**不進版控** |
| `outputs/` | 範例頁 |
| `reference/` | 另一個人在用,這裡的程式不碰它 |

## 需要什麼

- python 3.11,和 `model_training/` 一樣的套件(pandas、numpy、xgboost、joblib)。不用網路。
- 本機要有這些資料(都不進版控):`model_training/data/raw/listings_2026-09-16.csv.gz`、`model_training/data/processed/` 的兩個表、`scratchpad/insideairbnb_sydney/2026-09-16/data/` 的 `reviews.csv.gz` 和 `calendar.csv.gz`。
- 第一次跑要讀評論檔和日曆檔,幾秒到幾十秒;之後直接讀 `data/` 的彙總表。

## 數字的口徑

- 比較範圍:2026-09-16 期,整套、1–2 臥、可住 2–4 人、最少 1–7 晚、有掛牌價的 **6,639 間**。模型是用其中去掉每晚 > 2,000 澳元後的 6,615 間訓練的。
- 價格都是**掛牌價**(房東標的價),不是成交價。收入都是**估算**。
