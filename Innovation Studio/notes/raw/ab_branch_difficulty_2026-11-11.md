# A/B 方案難度分析(IS-1111-BR-DIFF,2026-11-11)

**結論:A(新房東競品分析)難度 4/5,資料全在手上;B(投資報酬測算)難度 2/5,要補 6 類外部資料且多數粒度對不上、關鍵輸入(成交價、營運成本)沒有。**

> 標記:「repo 既有,2026-11-07」= 引用 `15_Airbnb_2024起雙城與ROI_研究範圍.md`、`airbnb_sources_2026-11-07.md`,今天沒重查。「今天打開」= 本次用 WebFetch 實際取得頁面內容。

## 1. 難度分數(5 = 最好做,1 = 最難)

| 方案 | 分數 | 理由 1 | 理由 2 | 理由 3 |
|---|---|---|---|---|
| A 新房東競品分析 | **4** | 主線只用 listings:20,833 列 × 90 欄(Sydney 9 月快照),room_type、accommodates、bedrooms、amenities、price、評分、`neighbourhood_cleansed` 都在(repo 既有,2026-11-07) | 沒有「對不對」的真值要驗證:輸出是分位數比較與定位建議,不必宣稱預測準確 | 要處理的髒點可控:price 空 14.94%、評分空 15.41%、bathrooms 整欄空、amenities 要文字解析;「同類」定義有主觀性 |
| B 投資報酬測算 | **2** | 6 類外部資料(買價、租金、利率、平台費、營運成本、法規稅費)要自己找、對齊,其中營運成本沒有官方來源 | 收入端全是估計:`price`=掛牌價、`estimated_occupancy_l365d` / `estimated_revenue_l365d` 是 Inside Airbnb 估計值,整條 ROI 沒有任何一個真實成交輸入 | 地區粒度對不上:買價/租金公開資料多為 suburb 或 LGA、且「中位數」≠該房源;兩州法規不同(NSW 180 天 vs VIC 7.5% levy)要分開建模 |

## 2. 技術工作項

| 方案 | 工作項 | 類別 | 大小 |
|---|---|---|---|
| A | 讀 listings、型別轉換、`price` 去 `$`/逗號、缺值標記 | 資料清洗 | 小 |
| A | amenities 字串解析成 0/1 設備欄(挑 20–30 個常見項) | 資料清洗 | 中 |
| A | 定義「同類」分群(room_type × accommodates × bedrooms × 區) | 分析建模 | 中 |
| A | 各群價格/評分/設備普及率分位數(P25/P50/P75) | 分析建模 | 中 |
| A | 新房東定位建議:輸入自己房況 → 輸出同類區間與設備缺口 | 分析建模 | 中 |
| A | 雙城(雪梨、墨爾本)套同一流程 | 資料清洗 | 小 |
| A | 互動展示(篩選地區/房型、顯示同類分布) | 系統展示 | 中 |
| B | 同 A 的 listings 清洗,另加 estimated_* 欄稽核 | 資料清洗 | 小 |
| B | 找、下載、讀 6 類外部資料(見 §3) | 資料清洗 | 大 |
| B | `neighbourhood_cleansed` ↔ LGA/suburb 對照表(空間疊合或名稱對照) | 資料清洗 | 中 |
| B | 季度中位租金 vs 移動年度中位租金口徑統一(repo 既有) | 資料清洗 | 中 |
| B | ROI 公式實作(NOI、無槓桿收益率、融資現金回報,repo 既有公式) | 分析建模 | 中 |
| B | 入住率 × 夜價 × 可售夜數(NSW 180 天)情境矩陣、敏感度、損益平衡 | 分析建模 | 大 |
| B | 兩州稅費規則分開處理(VIC levy 平台繳,不重複扣) | 分析建模 | 中 |
| B | 互動展示:選地區 → 低/中/高情境 ROI 與短租 vs 長租 | 系統展示 | 大 |

## 3. B 要補的外部資料

欄位順序:來源與網址 → 免費 → 最細層 → 格式 → 涵蓋時間 → 對得上 `neighbourhood_cleansed`? → 今天打開

| 資料 | 內容 |
|---|---|
| **買房價格 NSW** | NSW Valuer General / NSW 政府「How to find property sales information」<br>https://www.nsw.gov.au/housing-and-construction/land-values-nsw/how-to-find-property-sales-information<br>→ 頁面沒說收費;網站資料限非商業(CC BY-NC-ND 4.0),商業用途要 PSI 授權(頁面所見)→ 逐筆交易可依 suburb/街道查;頁面未說逐筆欄位是否含 postcode → bulk 格式頁面未說(搜尋摘要稱 .DAT,**未確認**)→ bulk 自 1990 年;查詢工具自 2001 年 → 要自行 suburb→LGA 對照,**未確認**可對上 → **有(該說明頁);bulk 下載頁 valuation.property.nsw.gov.au 回 403,沒打開**。彙總中位價:此頁沒有 |
| **買房價格 VIC** | VIC Dept of Transport and Planning「Victorian Property Sales Report – Median House by Suburb」<br>https://discover.data.vic.gov.au/dataset/victorian-property-sales-report-median-house-by-suburb<br>→ CC BY 4.0,公開(頁面所見)→ suburb(另有大都會/郊區整體)→ XLS → 季度;今天頁面只看到 March 2026 Quarter,完整起訖**未確認**(另有 2011–2021 時間序列,為搜尋摘要,**未打開**)→ suburb≠LGA,要對照,**未確認** → **有(資料集頁)**。只有 house;unit 資料集頁面沒給連結,**未確認**。land.vic.gov.au 年報頁回 403,沒打開 |
| **長租租金(機會成本)** | NSW:DCJ Rent and Sales report<br>https://dcj.nsw.gov.au/about-us/families-and-communities-statistics/housing-rent-and-sales/rent-and-sales-report.html<br>VIC:DFFH 歷史租金報告 https://www.dffh.vic.gov.au/publications/past-rental-reports<br>→ NSW 頁面未見收費,可直接下載(頁面所見);VIC 見 repo 既有 → NSW:頁面未明寫 LGA/postcode,只說依 ASGS 彙整,**未確認**;VIC:LGA 季度中位(repo 既有,2026-11-07)→ NSW XLSX(租金表 3.3 MB,今年 6 月季);VIC Excel → NSW 租金最新 June 2026 quarter,自 2017-09 起走儀表板、之前為舊報告;VIC 2024 四季 LGA(repo 既有)→ 若為 LGA 則較容易對;**未確認** → **NSW 有;VIC 今天兩次 WebFetch(past-rental-reports、rental-report)逾時,且 Excel 連結再試逾時,沒打開成功**(repo 2026-11-07 稱已確認) |
| **房貸利率** | RBA 統計表 F5 Indicator Lending Rates、F6 Housing Lending Rates<br>https://www.rba.gov.au/statistics/tables/<br>→ 頁面未見收費,有直接下載;版權聲明內容未檢視 → 全國(無地區)→ f05hist.xlsx、f06hist.xlsx、CSV(f5-data.csv、f6-data.csv)→ 頁面未說起始年份與頻率,**未確認** → 不需對地區(全市/全國同一參數)→ **有(表格索引頁);xlsx 本體沒打開** |
| **平台服務費** | Airbnb 說明中心「Service fees」<br>https://www.airbnb.com.au/help/article/1857<br>→ 公開免費 → 全平台費率(無地區)→ 網頁 → 現行費率,無歷史 → 不需對地區 → **有**。所見:split fee 房東約 3%;單一式(host-only)多數 15.5%,範圍 14–16%;費基含每晚價與房東加收費用(清潔費是否計入為頁面推論,非明文);頁面無澳洲專屬規定 |
| **清潔等營運成本** | **沒找到官方來源**。Airbnb listings 無清潔費欄。可能的替代:自設參數(每單清潔費、水電網路、保險、管理費),或另找 ABS/產業報告 → 無 → 無 → 無 → 無 → 無 → **沒查(本次工具額度用完,未做搜尋),全部「未確認」** |
| **短租法規與稅費 NSW** | NSW Planning「Short-term rental accommodation」<br>https://www.planning.nsw.gov.au/the-planning-system/housing/short-term-rental-accommodation<br>→ 公開;STRA 新登記 $65、年續 $25;頁面未提稅費 → 規則層級:Greater Sydney(Eastern Harbour/Central River/Western Parkland)、Ballina、部分 Clarence Valley/Muswellbrook 非 hosted 年上限 180 天;Byron 60 天;21 天以上連住不計入 → 網頁 → 頁面 2025-02-10 更新,政府仍在檢討 → 頁面**沒列 LGA 名稱**,Greater Sydney 的 LGA 清單要另查,**未確認** → **有** |
| **短租法規與稅費 VIC** | VIC SRO「Understanding the short stay levy」<br>https://www.sro.vic.gov.au/owning-property/short-stay-levy/understanding-short-stay-levy<br>→ 公開 → 全州規則 → 網頁 → 2025-01-01 起,總預訂費 7.5%;<28 天算短租;費基含住宿費、清潔費、GST、延遲退房費;經平台預訂由平台繳;主要住所等排除 → 全州適用;council 層級登記/地方稅此頁沒提,**未確認** → **有** |

## 4. A 要補的外部資料

**主線不需要外部資料。** 原因:A 回答的是「跟我同類的房源,定價、評分、設備長怎樣」,三者(`price`、`review_scores_rating`、`amenities`)與分群欄位(room_type、accommodates、bedrooms、`neighbourhood_cleansed`)都在 listings 內(repo 既有,2026-11-07)。選配(非主線):地區平均所得或景點距離做加分,但這會引入對照表工作,建議不做。

## 5. 假設清單

### A(6 條)
1. **「同類」= room_type × accommodates × bedrooms × 地區** → 錯了:群太小或混入不可比房源,分位數失真 → 交代:公開分群規則、每群標樣本數,樣本 < 30 的群不下結論。
2. **`price` 掛牌價可代表市場價位** → 錯了:實際成交價可能更低/有折扣 → 交代:明講是「掛牌價定位」,不是成交價分析。
3. **評分只分析有評分的房源** → 錯了:新房源無評分被排除,偏向老牌房源 → 交代:標分母(約 85%),不把空值當 0。
4. **amenities 文字出現 = 有該設備** → 錯了:房東可能亂填/漏填 → 交代:只談「刊登的設備」,不談實際。
5. **2026-09-16 快照可代表「2024 年以來」的現況** → 錯了:季節性、價格變動被忽略 → 交代:明講單一時點;若要時間趨勢需另取歷史檔(repo 既有:歷史資料參考價 US$800 為站方指南,本組未申請)。
6. **定位建議用分位數(如 P25/P50/P75)而非因果** → 錯了:被誤讀成「裝了這設備價格就會漲」 → 交代:只講相關,不講因果(repo 既有立場)。

### B(10 條)
1. **入住率用 `estimated_occupancy_l365d` 當基準情境** → 錯了:這是估計值,可能系統性高/低估 → 交代:改以低/中/高三情境,加敏感度表。
2. **夜價用 `price` 掛牌價** → 錯了:收入高估(折扣、旺季調整未反映) → 交代:加「實收/掛牌」折扣參數情境。
3. **買價用 suburb/LGA 中位數代表一間房** → 錯了:與該房源實際價差大;VIC 只有 house 中位(今天所見) → 交代:標為「假設物業」,不是個別房源 ROI。
4. **長租機會成本用 LGA 中位租金 × 52 週** → 錯了:房型/臥室數口徑可能對不上;季度 vs 移動年度中位口徑不同 → 交代:公開口徑,限定可比房型。
5. **平台費用 15.5% 單一式(或 3% split)** → 錯了:房東實際設定不同 → 交代:兩種都跑,引用 Airbnb 說明頁。
6. **清潔/營運成本用自設參數** → 錯了:無官方依據,可能偏離現實 → 交代:列為「待驗證參數」,做敏感度,不聲稱預測。
7. **利率與貸款成數自設** → 錯了:實際房貸條件因人而異 → 交代:用 RBA F6 作為利率背景,貸款成數當情境。
8. **NSW 以 180 天上限(Greater Sydney 非 hosted)計可售夜數;VIC 7.5% levy 由平台繳、不重複扣** → 錯了:房源可能是 hosted、有 21 天以上連住例外,或屬 VIC 主要住所排除 → 交代:按州分開、限定「非 hosted 整套」情境。
9. **不計房價上漲、所得稅、折舊** → 錯了:真實報酬不同 → 交代:公式本來就定為稅前、無增值(repo 既有);結果只叫「情境回報率」。
10. **`neighbourhood_cleansed` 可映射到 LGA/suburb** → 錯了:對不上則買價、租金無法接 → 交代:先做對照表並報對應率,對不上的區域剔除。

**統計:A = 6 條,B = 10 條。**

## 6. 沒查到的事

- 清潔、水電、保險、管理費等營運成本:沒找到官方來源,本次也沒搜尋(額度用完)。
- VIC DFFH 租金報告:今天 3 次 WebFetch 逾時,沒打開成功;只有 repo 2026-11-07 的紀錄,今天無法獨立確認。
- NSW 租金表的地理層級(LGA/postcode)與房型/臥室分組:頁面沒寫,檔案沒下載。
- NSW 逐筆買賣 bulk 檔的格式、欄位、授權細節:bulk 頁 403;.DAT、1990 年起這兩點只來自搜尋摘要與說明頁,bulk 本體沒打開。
- VIC 年報(land.vic.gov.au)403,沒打開;VIC unit(公寓)中位價資料集沒找到連結。
- RBA F5/F6 的頻率與起始年份:沒打開 xlsx。
- `neighbourhood_cleansed` 實際值(是 LGA 名稱還是別的劃分)與 Inside Airbnb 雪梨/墨爾本 neighbourhoods 檔:沒打開,對應關係**未確認**。本地欄位盤點檔未列出該欄的值。
- Greater Sydney 涵蓋哪些 LGA:NSW 頁面沒列,需看 Planning Portal 地圖。
- Council 層級短租規定(墨爾本市、雪梨各 council 的附加限制):兩個州頁面都沒提。
- 墨爾本整體資料量與品質:本次只用 repo 既有的 Sydney 數字,沒看 Melbourne 檔。
