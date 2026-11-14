# 雪梨短租營運成本與房市行情:補查(外部參考值)

查閱日 2026-11-14;外部參考值,不是我們資料算出來的;本檔是 web_opcost_housing_2026-11-14.md 的補查。scope ID:IS-1114-web-04-opcost-gapfill

用途:補上一份沒查到的項目,給方案 B(收入情境試算)當「預設參考值」,使用者可改。只列行情數字,不是理財建議。
表頭與欄位定義同上一份。「低/中(典型)/高」沒有填的格子 = 來源只給單一數字。不同期間或不同地理範圍的數字一律分列,不混成一格。
「取得方式」:
- 已開頁(Chrome)= 我用 Chrome 開該官方頁,親眼讀到頁面全文。
- 已開頁(WebFetch)= 用抓取工具開頁,內容經小模型摘要後回傳,不是我讀全文;可信度略低於 Chrome 全文。
- 搜尋摘要 = 只看到搜尋結果摘要,沒開原頁,可信度較低,正式引用前要回頭核對。
自己算的數字標「換算」。

## 1. 租金與房價

| ID | 項目 | 低 | 中(典型) | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 取得方式 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L2 | 公寓(unit)租金中位數(補上一份 L2) | | 780(「持平」) | | AUD/週 | 2026 年 9 月季 | Sydney(文內該段是雪梨段落,但這句沒重複寫 Sydney,見註) | Domain 2026 年 9 月季租金報告(經 Elite Agent 2026-10-08 文章轉述) | https://eliteagent.com/why-australian-rents-stall-despite-record-low-vacancies/ | 產業報告(轉述) | 已開頁(WebFetch) |
| L1b | 獨棟屋租金中位數(交叉對照上一份 L1) | | 835 | | AUD/週 | 2026 年 9 月季 | Sydney | 同上 | 同上 | 產業報告(轉述) | 已開頁(WebFetch) |
| V5 | 空置率(雪梨,Domain 口徑) | | 1.2(6 月季 1.1;去年同期 0.9) | | % | 2026 年 9 月季 | Sydney | Domain(經搜尋摘要) | 同上(搜尋結果頁) | 產業報告(轉述) | 搜尋摘要 |
| P3 | 公寓價值中位數(unit) | | 867,597(月 −1.0%,年 −3.8%) | | AUD | 2026 年 9 月 | Sydney(Cotality,地理口徑摘要未寫清;疑為 Greater Sydney) | Cotality(經 OpenAgent,搜尋摘要轉述) | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 產業報告(轉述) | 搜尋摘要 |
| P4 | 獨棟屋價值中位數(house) | | 1,466,060(月 −1.6%,年 −8.2%) | | AUD | 2026 年 9 月 | 同 P3 | 同上 | 同上 | 產業報告(轉述) | 搜尋摘要 |

註:
- L2:Domain 官方報告頁這次 Chrome 也沒讀到(權限提示沒人回應就逾時,沒有打開),所以 780 是第二手。支持這個數字的旁證:上一份 L5 的「2026 年 6 月季雪梨公寓 780」,與本筆「9 月季持平 780」一致。本筆的「Sydney」是依段落歸屬判斷,不是句子明寫。
- L1b 835 與上一份 L1(835,Domain 經 Time Out)一致。
- V5 的 1.2% 與上一份 V1(2.5%,Cotality)、V2(1.8%,SQM)、V3/V4(Domain 0.9/1.1)是不同供應商口徑;V5 與 V3/V4 同為 Domain,趨勢(0.9 → 1.1 → 1.2)可比。
- P3/P4:摘要自己提到與另一個來源的 8 月獨棟屋中位(約 1,494,878)有出入,且文中另有一個「雪梨公寓中位約 120 萬」的說法日期不明,我沒採用。P3/P4 的期間是 2026 年 9 月,上一份 P1(合併價 1,178,959)是 2026 年 10 月,兩者期間不同,不要拿來互相推算。拆分數字請上 Cotality 原頁核對再引用。

## 2. 水電瓦斯網路(補)

| ID | 項目 | 低 | 中(典型) | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 取得方式 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1 | 水:供水固定費(有水表) | | 26.65(2025-26 為 29.73) | | AUD/季(最大值,以 92 天季計) | 2026-27(2026-07-01 至 2027-06-30) | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | 已開頁(Chrome) |
| W2 | 水:污水處理固定費 | | 189.88(2025-26 為 174.40) | | AUD/季(最大值) | 2026-27 | 同上 | 同上 | 同上 | 官方 | 已開頁(Chrome) |
| W3 | 水:雨水排水費(公寓/低衝擊) | | 9.67(獨棟屋 30.26) | | AUD/季(最大值,只在雨水排水區才收) | 2026-27 | 同上 | 同上 | 同上 | 官方 | 已開頁(Chrome) |
| W4 | 水:用水量單價 | | 3.41(2025-10 至 2026-06 為 3.17) | | AUD/千公升(kL) | 2026-07-01 至 2027-06-30 | 同上 | 同上 | 同上 | 官方 | 已開頁(Chrome) |
| W5 | 水:乾旱費率用水單價 | | 3.84 | | AUD/kL | 水庫低於 60% 時才適用,回升到 70% 以上取消 | 同上 | 同上 | 同上 | 官方 | 已開頁(Chrome) |
| W6 | 水:官方給的典型季帳單(獨棟屋,用水 50 kL,供水+污水,92 天) | | 387.03 | | AUD/季 | 2026-27 | 同上 | 同上 | 同上 | 官方 | 已開頁(Chrome) |
| W7 | 水:公寓(有水表)用水 50 kL/季的季帳單(換算) | | 396.70 | | AUD/季 | 2026-27 | 同上 | 自己算 | | 換算 | 換算 |
| G1 | 瓦斯:NSW 家戶年均 | 730 | 964(241/季 × 4,換算) | 1,320 | AUD/年 | 日期多數沒標(2026 搜尋結果) | NSW(非雪梨專屬) | Mozo 引 Finder(730);Finder 州別表(241/季);Energy Plans(1,320) | https://www.mozo.com.au/best/energy/gas.html ; https://www.finder.com.au/energy/gas-nsw ; https://www.energyplans.com.au/average-gas-bill-australia | 商業網站(比價站) | 搜尋摘要 |
| N1 | 網路:NBN 50 一般方案月費 | 50(Mozo 最便宜無限量,NSW) | 約 86(Canstar 2026 全速率平均月帳單) | 100(Canstar 區間上限;Telstra NBN 50 為 99、Optus 97,2026-07 漲價後) | AUD/月 | 2026(7 月起 NBN 批發價上調) | 全澳,Mozo 列表為 NSW | Canstar、Mozo、Finder(搜尋摘要) | https://www.canstar.com.au/internet/average-internet-bill/ ; https://www.mozo.com.au/broadband.html ; https://www.finder.com.au/news/optus-telstra-nbn-price-hikes-locked-in-for-july-2026 | 商業網站(比價站) | 搜尋摘要 |
| N2 | 網路:NBN 100 方案月費 | 70(Mozo 最便宜無限量) | | 110(Canstar 區間上限;Telstra/Optus 同為 99) | AUD/月 | 2026 | 同 N1 | 同 N1 | 同 N1 | 商業網站(比價站) | 搜尋摘要 |

註:
- W1–W6 都是官方頁 2026-27 年度,「最大季費」以最長季(92 天)計;Sydney Water 說固定費按日計算,所以 90、91 天的季會略少。
- W7 換算:供水 26.65 + 污水 189.88 + 雨水(公寓)9.67 + 用水 50 kL × 3.41(=170.50)= 396.70。官方給的獨棟屋 387.03 = 26.65 + 189.88 + 170.50,不含雨水費;所以公寓這一列是我加雨水費 9.67 的結果,而且只在位於雨水排水區才有。「50 kL/季」是官方典型獨棟屋的用水量,不代表小公寓,用水量請使用者自填。以 4 季粗乘 = 約 1,587 AUD/年(粗略,未扣短季)。
- 公寓是否另有「由管理委員會統一繳水費、以 strata 管理費分攤」的情況:這次沒查到,不寫。使用者若住的大樓水費已含在管理費,不要重複計入。
- G1 三個數字差距大(730 對 1,320),來源是比價站、方法不同、日期沒標,只能當粗略帶狀,不能當中位。AER 摘要有說明 Jemena(雪梨瓦斯網)家庭換到最便宜市場方案每年可省 377,這個是節省額不是帳單,不採用。
- N1/N2:搜尋摘要自己標出有些來源是聯盟行銷或 SEO 頁(ShopBack、kalinino.pages.dev),它們的數字我沒採用。方案有促銷價與正常價之分,上列「低」是促銷或最便宜無限量方案,不一定是長期價。

## 3. 持有成本(補)

| ID | 項目 | 低 | 中(典型) | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 取得方式 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1b | 公寓管理費(strata)典型值(確認上一份 S1) | | 854 | | AUD/季 | 2026(白皮書年份;分析 2019 至 2026 年初的房源描述) | **NSW 全州**,不是只有雪梨(見註) | Microburbs strata levies whitepaper | https://www.microburbs.com.au/research/strata-levies-whitepaper | 商業網站(資料公司) | 已開頁(WebFetch) |
| R1 | 市政費(council rates):North Sydney 住宅最低費率(minimum rate) | | 970.72(2027-28 核准 1,116.32;2028-29 為 1,216.79) | | AUD/年 | 2026-27 | North Sydney 市政區 | IPART「Minimum Rates Instrument 2026-27 North Sydney Council」 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Minimum-Rates-Instrument-2026-27-North-Sydney-Council.PDF | 官方(NSW 州政府機構) | 搜尋摘要 |
| R2 | 市政費:Blacktown 住宅最低費率與平均住宅費 | 1,140(最低費率) | 1,233(平均住宅費) | | AUD/年 | 年度摘要沒寫清 | Blacktown(雪梨西部) | Blacktown 市政廳 Special Rate Variation 說明(放在 IPART 資料庫) | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Blacktown-City-Council-Attachment-Other-Attachment-2.5-Special-Rate-Variation-FAQs-and-Factsheets.PDF | 官方(轉述) | 搜尋摘要 |
| I1 | 房東/短租專用保險 | 500 | | 700 | AUD/年 | 2026 | 全澳(沒分雪梨,沒分房型) | Rakidzich(短租代管商部落格) | https://www.rakidzich.com/articles/airbnb-insurance-australia | 商業網站(代管商行銷文) | 搜尋摘要 |

註:
- S1b:頁面寫「the typical Sydney (NSW) apartment costs $854 per quarter」,但這個數字出現在全國表格的 NSW 那一列,涵蓋 NSW 全州(分析樣本:全澳 49,234 筆、19,270 棟大樓,其中 NSW 24,064 筆)。所以上一份把它標成「地理範圍 Sydney」要改成「NSW(措辭寫 Sydney (NSW))」。
- R1/R2:City of Sydney 與其他市區的「一般公寓一年大概多少」沒有查到。R1 是「最低費率」,是下限的概念,不是公寓典型帳單;R2 的 1,233 是 Blacktown 的平均住宅費(不分房型、年度不明)。兩個都不是雪梨一般公寓的典型值,只能顯示量級約 1,000–1,250 AUD/年。NSW 全州 2026-27 的 rate peg(上限)為 2.5% 至 4.2%(IPART,搜尋摘要)。
- I1:這是廠商行銷文的單一區間,不是保險公司的公布費率。搜尋摘要還說:一般房東保險常不涵蓋短租(多被視為商業用途),要問保險公司;Houst 文章說 NSW 短租規定要有第三方傷亡責任險,但我沒對到 NSW 官方頁,沒採用。

## 4. 利率

| ID | 項目 | 低 | 中(典型) | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 取得方式 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B1b | RBA 現金利率目標(確認上一份 B1) | | 4.85(+0.25;前值 4.60) | | % 年利率 | 2026-11-04 生效(2026-11-03 公布,頁面說調整於公布後隔日生效) | 全澳 | 澳洲央行 RBA「Cash Rate Target」頁 | https://www.rba.gov.au/statistics/cash-rate/ | 官方 | 已開頁(Chrome) |
| B3 | 投資客房貸利率 | 查不到 | 查不到 | 查不到 | % | | | | | | 沒查到 |

註:
- B1b:上一份 B1 的 4.85% 確認無誤。RBA 頁面列出 2026 年的調整:2/4 升到 3.85、3/18 升到 4.10、5/6 升到 4.35、9/30 升到 4.60、11/4 升到 4.85,共 5 次升息(間隔的 6/17 與 8/12 維持 4.35),與上一份「第 5 次升息」一致。上一份寫「11/3 升」是公布日,生效日是 11/4。
- B3:抓取工具被 RateCity 轉址到 Canstar,沒有後續工具次數可再抓,所以沒查到。

## 5. 報稅

| ID | 項目 | 重點(我的話) | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 取得方式 |
|---|---|---|---|---|---|---|---|---|
| T4 | ATO:短租收入申報 | 短租、透過平台出租、出租自己住家的一部分或全部,都要申報租金收入;要申報的是扣除平台費、代管費之前的毛額,還包括被取消訂單你留下的訂金/預訂費、保證金、損害保險金等。按法定持有比例分報(共有人各報自己那份);仲介代收的,以房客付給仲介的年度為準,不是你收到的日期。個人報稅表填在「澳洲利息或其他澳洲投資/財產收入」那一項。 | 頁面「最後更新 2026-05-21」 | 全澳 | ATO「Rental income you must declare」 | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare | 官方 | 已開頁(Chrome) |

註:
- 費用怎麼扣(含只出租部分空間或部分天數的分攤)這頁只列出相關文件名稱(TR 2026/1、PCG 2026/2、PCG 2026/3),沒展開內文,我沒開,所以扣除規則本檔不寫。
- 本列只說明申報範圍,不構成報稅建議。

## 6. 還是查不到的項目

- L2 官方原頁:Domain 租金報告頁沒讀到(Chrome 權限提示逾時),780 是 Elite Agent 轉述。
- P3/P4 官方原頁:Cotality 或 Domain 房價頁沒讀到,867,597 與 1,466,060 是搜尋摘要;期間為 2026 年 9 月,不是 10 月。
- R1/R2 的目標:雪梨「一般公寓」的年度市政費沒有查到,只有 North Sydney 最低費率與 Blacktown 平均費。City of Sydney、Inner West 等官方頁沒開(搜尋次數用完)。
- I1:保險公司公布的房東保險/短租保險費率沒有,只有單一廠商文章。
- B3:投資客房貸利率沒查到。
- C2:床單洗滌外包每次或每公斤價格:沒查(本輪工具次數用完)。
- S2(Flat Chat 論壇約 850/季):沒重開原頁,仍是上一份的搜尋摘要狀態。
- G1:沒有 AER 或政府的雪梨瓦斯年均帳單,只有比價站數字。
- 搜尋摘要來源的列未開原頁,正式引用前需回頭核對。
