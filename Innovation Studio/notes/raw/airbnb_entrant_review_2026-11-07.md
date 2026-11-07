# AIR-NOV07-REVIEW：雪梨新房東研究工作稿獨立核對

- 日期：2026-11-07。核對者為非產出者的 fresh Codex subagent；未另派代理。
- 結論：本次範圍通過，未發現會改變研究方向的數字錯誤或因果誤用；適用於研究工作稿，並非課程提交終審。
- 核對對象：`../14_Airbnb新房東_資料範圍與業務方向.md`、`../../analysis/airbnb_entrant_eda.py`、`airbnb_entrant_eda_2026-11-07.json`、本機原始 `scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz`。
- 方法：另寫短程式，僅用標準庫 `csv/gzip/Decimal/Counter/statistics/hashlib` 直接讀原檔；未匯入或執行產出者的分析函式。數值條件以 Decimal 比較，避免直接照抄字串篩選。

| 獨立重算項目 | 結果／與主稿、JSON對賬 |
|---|---|
| 原檔SHA256 | `06bbd629fbe93d9da1f2163e82d584a58738a53d7897d5c081f665aadc4e3c55`，一致 |
| 全量／欄位／唯一ID | 20,833／90／20,833，一致 |
| last_scraped | 僅2026-09-17，一致 |
| 整套房／全量有價 | 16,445／17,721，一致 |
| 整套＋臥室1–2＋容納2–4＋最低晚數1–7 | 7,565；缺值排除，一致 |
| 範圍內有價 | 6,639，一致 |
| 有價且入住／退房日期齊全 | 6,639，分873組，一致 |
| 最大同日期組 | 2026-09-17入住、09-18退房，375列，中位報價AUD333.00，一致 |
| 兩價格欄均有值 | 17,720列；Decimal逐列最大差AUD0.00，全數小於AUD0.011，一致 |
| 最低晚數缺值／至少90晚 | 13／2,846，一致 |
| 範圍內Wifi／Kitchen | 6,881／7,103，一致 |

主稿第22–45行的上述數字均通過；獨立計算 assert 驗證 `(範圍,有價,日期組,最大組,雙價列,差小於0.011列) == (7565,6639,873,375,17720,17720)`，程序EXIT=0。

- 直接HTTP串流重讀[同版calendar](https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/calendar.csv.gz)：HTTP200；解壓表頭為 `listing_id,date,available,minimum_nights,maximum_nights`，確實無price。僅驗表頭，未全量讀取。
- [官方下載頁](https://insideairbnb.com/get-the-data/)確認Sydney列2026-09-16、約近12個月季度檔與CC BY4.0；目錄日期和實檔抓取日不同，主稿有清楚區分。
- [官方Data Assumptions](https://insideairbnb.com/data-assumptions/)確認不可訂無法區分已訂或房東封鎖、座標經模糊及收益／入住率為模型估計；主稿未當作實際交易或帳務。
- [NSW官方STRA概述](https://www.planning.nsw.gov.au/the-planning-system/housing/short-term-rental-accommodation)確認Greater Sydney的非hosted豁免開發途徑180日限制及21天以上連續住宿例外；主稿未套用到所有房源，亦未作個別物業合規判定。
- 方法界線：375列僅對齊日期，未對齊臥室、容量、客人數與費用；主稿已揭露，AUD333沒有寫成建議售價。不同日期酒店價未與9月Airbnb直接比價。
- 裝修／收益：設備與評分沒有被寫成因果溢價、裝修ROI或最佳投資；營運式為假設試算，清潔成本以訂單數扣除，長租機會成本未重複扣除。
- 程式最新回讀已有原檔SHA256 assert，固定快照圖標籤的適用邊界明確；本次未修改主稿、JSON或程式。

未驗：其餘補充API的即時配額／穩定性、GeoJSON全量、逐則評論、圖的視覺品質、模型分數、活動／裝修因果及收益實現；這些不在本次通過範圍。
風險：原始報價客人數／費用尚未釐清，資料仍為單次快照；開始價格推薦前，須先完成同條件競品定義。
