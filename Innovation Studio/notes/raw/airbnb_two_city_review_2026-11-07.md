TL;DR：未發現會改變研究主線的錯誤；獨立CSV重算墨爾本25,715／10,940／8,223及雙城逐年評論均與JSON、主稿一致，2024起完整市場面板仍未取得。

- Scope：AIR-TWOCITY-REVIEW；2026-11-07；核對者非主稿／profile程式產出者，未另派工。
- 硬上限50,000 tokens；正文輸入6檔、官方來源3頁，未擴查其餘引用。
- 6檔：主稿15、profile JSON、profile程式、墨爾本listings.gz、兩城市reviews_summary.csv；handoff／技能屬執行規則。
- 核對方式：另用Python標準csv／gzip與Decimal篩選，未呼叫原profile函式；assert與對賬命令EXIT=0。

數字證據：

- 主稿15:33–36：墨爾本25,715列×90欄、25,715個唯一ID；價格非空19,004；整套1–2房／2–4人／最低1–7晚10,940，其中有價8,223；全與JSON相符。
- 墨爾本SHA256獨立重算為`7d09b7124bfc26bdb5c8a2a66efe0b9a48e4e1d7cc2e11242e9d52ee3f17985b`，與JSON相符；last_scraped為2026-09-17及09-18。
- 主稿15:37–39：雪梨評論829,163列，2024年134,978，2024起474,233；墨爾本1,042,226／174,079／546,972；逐年Counter也全與JSON相符。
- 雪梨日期2009-12-05至2026-09-17；墨爾本2010-08-04至2026-09-18；兩城日期空白均0，表頭均只有listing_id,date。
- 墨爾本評論涉及的listing_id全部存在本次listings；沒有評論全文、訂單或真實收入欄，評論列數不能當成訂單量。
- 主稿表格與JSON逐項對賬一致；雪梨listings的20,833／7,565／6,639僅核對兩份產物相符，本輪未重讀該原始檔。

會影響結論的邊界：

- 主稿15:22–25、51已清楚區分2024起目標與2026橫斷面；現存房源附帶的歷史評論有存活／選樣偏差，不能補成2024全市場面板。JSON的historical_snapshots_2024_acquired=false一致。
- 主稿15:80–87的回報公式區分可售夜入住率、全年利用率、NOI、增量投入、總購置成本與自有現金分母；融資現金流含本金，未見會推翻情境比較的內部矛盾。
- 上述是公式與口徑審查，沒有物業實收、成本、融資或報酬案例可驗；不能提升為真實投資回報預測或裝修因果ROI。
- 主稿15:98–103將墨爾本直接遷移、少量校準及本地訓練基準分開，第三城調參後不稱未見測試，並排除目標價格／估計收入偷讀；設計方向未見明確漏洩。
- 尚無模型／split／評分實作，故不能證明實驗沒有漏洩；實作時中位數、前處理與調參須只用對應訓練資料，保留測試標籤不得參與，否則分數失效。

官方來源（2026-11-07開啟，限此3頁）：

- [Inside Airbnb Data Requests](https://insideairbnb.com/data-requests/)：旅遊／定價研究屬non-mission-aligned類，兩城US$800為歷史資料資金指南；不是本組報價或2024檔取得證明。主稿15:18限定正確。
- [VIC SRO Understanding the short stay levy](https://www.sro.vic.gov.au/owning-property/short-stay-levy/understanding-short-stay-levy)：2025-01-01起、少於28連續日、7.5%總booking fee含清潔及GST；主要住所等可排除，平台訂單由平台負申報繳付責任。主稿15:92未套成NSW180日，亦提醒避免重扣。
- [NSW STRA](https://www.planning.nsw.gov.au/the-planning-system/housing/short-term-rental-accommodation)：Greater Sydney非hosted豁免開發途徑180日限制，計數為登記年度，連續21日以上訂單有計數例外；不能無條件套所有房源。主稿15:91的條件性描述相符。

未驗：

- 未重新下載原始檔，未獨立讀雪梨listings、兩城calendar串流或詳細reviews；calendar無價格目前只有程式／JSON／主稿一致性證據。
- 未查兩州長租Excel、估值／購置成本、地方政府／公寓條件、逐物業法律稅務適用、模型、第三城或真實營運結果；未驗圖像。
- 本輪僅為資料數字／研究範圍／方法與3頁概述的獨立抽核，不是完整投資或法律驗收；無須修改主稿才能維持目前有限結論。
