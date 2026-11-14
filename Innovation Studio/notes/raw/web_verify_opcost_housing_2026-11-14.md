# 查核:雪梨短租營運成本與房市行情(兩份外部參考值筆記)

查核日 2026-11-14;scope ID:IS-1114-verify-03-opcost。被查檔:`web_opcost_housing_2026-11-14.md`(下稱「原檔」)、`web_opcost_housing_gapfill_2026-11-14.md`(下稱「補查檔」)。

**一句話總結:查了 56 列,✅ 24、⚠️ 14、❌ 1、⏸ 5、未查 12;換算與加總基本都對(只有甲的中位加總四捨五入差 1 元),沒有把每週、每季、每年直接相加。**

查核方式與限制:
- 用 WebFetch 重開筆記網址,內容是小模型摘要後回傳,不是我讀全文;所以「頁面實際看到的值」是摘要回報的引文。
- WebFetch 回 403 或逾時的頁,因為 26 次工具上限沒有改用 Chrome 重試,所以標 ⏸(寫明狀態),不代表頁面本身有問題。
- 沒開過頁、也沒在別頁看到數字的列,一律「未查」,不給 ✅。
- 工具用量:WebFetch 21 次、WebSearch 1 次(只用來找 P3/P4)、讀檔 2 次、載入工具 1 次、寫檔 1 次。
- 兩份檔的列 ID 有重複(W1、G1、N1、R1、I1、P3、P4、L2、T4、B3 在原檔多為「查不到」,在補查檔才有值)。下表第一欄標明哪一份。原檔裡「查不到」的空白列不計入列數。

## 逐列判定表

| 哪一份檔 | 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|---|
| 原檔 | E1 Ausgrid 2025-26 | 1,965 AUD/年 | 表「Draft flat rate electricity price changes: 2026-27」,Ausgrid「Current price」$1,965 | ⚠️ | 數字、單一費率、無受控負載(controlled load)都吻合;但頁面欄名只寫 Current price,沒寫 2025-26,期間是推論。頁面沒給用電度數(筆記的「標準用電量」是沿用「AER 平均家戶」說法)。 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ |
| 原檔 | E2 Ausgrid 2026-27 草案 | 1,875 AUD/年 | Draft price $1,875(−$90,−4.6%) | ✅ | 吻合,頁面也標為草案。 | 同上 |
| 原檔 | E3 Endeavour 2025-26 | 2,411 | Current price $2,411 | ⚠️ | 同 E1:期間欄名是 Current price。 | 同上 |
| 原檔 | E4 Endeavour 2026-27 草案 | 2,347 | Draft price $2,347(−$64,−2.7%) | ✅ | 吻合。 | 同上 |
| 原檔 | E5 Essential 2025-26 | 2,741 | Current price $2,741 | ⚠️ | 同 E1。 | 同上 |
| 原檔 | E6 Essential 2026-27 草案 | 2,515 | Draft price $2,515(−$226,−8.2%) | ✅ | 吻合。 | 同上 |
| 原檔 | E7 AER 草案資訊頁 | 只記網址 | WebFetch 逾時(60 秒) | ⏸ | 官方原件沒打開,E2/E4/E6 仍只有 Canstar 轉述。 | https://www.aer.gov.au/system/files/2026-03/Draft%20Default%20Market%20Offer%202026-27%20-%20Information%20sheet.pdf |
| 原檔 | C1 清潔費 | 低 50 / 中 65 / 高 105 AUD/次;2026-11-13;全澳 | 平均 $50–$80;自己打掃約 $65;大房找清潔公司約 $105;文章日期 Nov 13, 2026;沒提雪梨;幣別頁面沒明寫 AUD | ⚠️ | 數字與日期吻合。差在:「低 50」是頁面「平均 50–80」的下緣,不是獨立的「低檔」;高 105 超出該平均區間;幣別是推定 AUD。 | https://hospitable.com/airbnb-cleaning-fee-australia |
| 原檔 | F1 平台抽成 | 15.5%(訂房小計);2026-05;全澳 | 「Since December 2025, Airbnb charges all Australian hosts a single 15.5% service fee on the booking subtotal」;Updated May 11, 2026 | ✅ | 吻合。補充:頁面說 subtotal 含清潔費、額外房客費、寵物費,不含稅與押金,所以 15.5% 也會抽到清潔費。筆記說的「取代舊制 3%+14%」這次沒驗。 | https://www.houst.com/blog/airbnb-hosting-fees-australia |
| 原檔 | M1 代管抽成 | 15 / 20–22 / 25 %;2026-05;全澳 | 「typically range from 15% to 25% of rental income」「most sitting around 20-22%」;Updated May 11, 2026 | ✅ | 吻合。頁面提到 Houst 在 Sydney 有服務,但費率沒有單獨列雪梨;而且是代管商自己的行銷文。 | 同上 |
| 原檔 | M2 雪梨/墨爾本代管抽成 | 15–22 % | 頁面沒有「15% 到 22%」,也沒出現 22%;只有「Houst starts from 12% in London, Paris and Dubai and from 14% in its other locations」;頁面日期 Updated Oct 21, 2026 | ❌ | 這個數字在該頁查不到。原檔註裡「M2 上限比 M1 低 3 個百分點」的推論也跟著站不住。可能來自搜尋摘要誤抄。 | https://www.houst.com/blog/airbnb-management-fees-guide |
| 原檔 | M3 共同房東抽成 | 10–15(只溝通)/ 20(最常見)/ 25;% 總訂房收入;2026;全澳 | 整體「15-25% of gross booking revenue」,20% 最常見;「Communication-only roles run 10-15%」;full-service 是「25%+」,頁面 FAQ 又寫 20–25%;文章 2026-03-16 | ⚠️ | 低、中、基礎(gross booking revenue)吻合。差在「高 25」:頁面 25% 是 full-service 的下限(25%+),不是上限,頁面本身前後也不一致。 | https://www.rakidzich.com/articles/airbnb-co-hosting-australia |
| 原檔 | S1 公寓管理費 | 854 AUD/季;Sydney | 句子「the typical Sydney (NSW) apartment costs $854 per quarter」;表「National coverage」NSW 列:24,064 筆、854/季、年化 3,416;資料 2019 至 2026 年初 | ⚠️ | 數字與單位吻合。地理範圍:表格標 NSW、句子標 Sydney (NSW),頁面沒說是否只含雪梨,原檔寫「Sydney」過度確定。854×4=3,416,與頁面年化吻合。 | https://www.microburbs.com.au/research/strata-levies-whitepaper |
| 原檔 | S2 Flat Chat 約 850/季 | 約 850 AUD/季 | 沒開 | 未查 | 論壇頁沒重開(工具次數)。 | https://www.flatchat.com.au/topic/how-do-you-guesstimate-levies/ |
| 原檔 | S3 小棟無電梯 | 600–1,200 AUD/季;NSW | 「Small building,6–12 lots,No lift,$600–$1,200」「a rough guide for NSW」 | ✅ | 吻合;頁面標明是粗略參考,只有 NSW,沒有雪梨細分。 | https://stratachecks.com.au/blog/beginners-guide-strata-levies |
| 原檔 | S4 中型有電梯 | 1,000–2,500 | 「Mid-size,30–60 lots,With lift,$1,000–$2,500」 | ✅ | 吻合。 | 同上 |
| 原檔 | S5 大型設施齊全 | 1,500–4,000 以上 | 「Large,100+ lots,Full amenities,$1,500–$4,000+」 | ✅ | 吻合。 | 同上 |
| 原檔 | S6 標準兩房 | 1,500–3,000;單位未註明(推測每季);2026;Sydney | 「average quarterly strata fees are: Sydney $1,500 to $3,000 for a standard two-bedroom apartment」,2026 粗估;豪華大樓可超過 $5,000/季 | ✅ | 吻合,而且單位確認是每季,原檔的「推測」成立。要注意:這個值是 S1 的約 1.8–3.5 倍,原檔「不採用」的理由(單位不明)已不成立,剩下的理由只有「兩房、粗估」。 | https://savingsmate.com.au/blog/strata-fees-explained-australia |
| 原檔 | L1 獨棟租金中位數 | 835 AUD/週(單季 −5,約 −0.6%);2026 年 9 月季;Sydney | Time Out:「fell 0.6 per cent ($5) to $835 per week」,歸屬 Domain September Quarter 2026 | ✅ | 吻合。頁面沒寫是 median;Elite Agent 那頁寫 median asking(開價中位)。 | https://www.timeout.com/australia/news/australias-rental-market-has-officially-stalled-despite-capital-city-shortages-100726 |
| 原檔 | L3 公寓 2025-09 季 750 | 750 AUD/週(年增 4.9%) | HTTP 403 | ⏸ | Domain 頁 WebFetch 403,Chrome 未試。 | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ |
| 原檔 | L4 獨棟 2025-09 季 780 | 780 | 同上 403 | ⏸ | 同上。 | 同上 |
| 原檔 | L5 公寓 2026-06 季 780 | 780 | 沒開 | 未查 | The New Daily 原檔已記 403,我沒重試。旁證:Elite Agent 說 9 月季公寓 780「steady」(持平),方向一致但不是同一頁。 | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices |
| 原檔 | L6 獨棟 2026-06 季 850 | 850 | 沒開 | 未查 | 但已開的兩頁(Time Out、Elite Agent)都寫 9 月季「−$5 到 835」,代表 6 月季應為 840,不是 850;L6 與已驗證頁面矛盾,見矛盾段。 | 同 L5 |
| 原檔 | V1 空置率 Cotality | 2.5%(去年同期 1.8);2026 年 9 月季;Sydney | 「In Sydney, the vacancy rate was 2.5 per cent」,與「1.8 per cent a year earlier」比較;該句沒標季別 | ⚠️ | 數字吻合;期間「9 月季」是推論(頁面該句沒標,同文有標 9 月季的是租金 −0.4%)。 | https://thenightly.com.au/australia/nsw/sydney-rents-fall-despite-fears-of-a-post-budget-spike-c-22990976 |
| 原檔 | V2 空置率 SQM | 1.8%;2026 年 9 月;Sydney | 「Sydney led the rise, with its vacancy rate climbing to 1.8 per cent」,SQM Research,September | ✅ | 吻合。 | https://www.openagent.com.au/news/national-property-market-update-october-2026 |
| 原檔 | V3 空置率 Domain 2025-09 | 0.9% | 403 | ⏸ | 原頁打不開。間接旁證:Elite Agent 說雪梨 9 月季 1.2%,「0.9% a year earlier」,與 V3 一致。 | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ |
| 原檔 | V4 空置率 Domain 2026-06 | 1.1% | 沒開 | 未查 | 間接旁證:Elite Agent 說「up from 1.1% in June」。 | 同 L5 |
| 原檔 | L7 租金季變動 | −0.4%;2026 年 9 月季;Sydney | 「Sydney rents fell 0.4 per cent in the September quarter」,Cotality,10/9 報導 | ✅ | 吻合。 | 同 V1 |
| 原檔 | P1 合併價值中位數 | 1,178,959 AUD(月 −1.6%、三個月 −4.7%、較 2 月高點低逾 10%);2026-10;Greater Sydney(Cotality) | CommBank:$1,178,959、月 −1.6%、較 2 月高點低逾 10%;地理只寫「In Sydney」;沒有三個月變動;沒有房型拆分 | ⚠️ | 價位、月變動、高點吻合。差在:「Greater Sydney」頁面沒寫;「三個月 −4.7%」不在這頁,在 P2 的 OpenAgent 頁。 | https://www.commbank.com.au/articles/newsroom/2026/11/sydney-home-prices-fall-more-than-10-percent-from-peak.html |
| 原檔 | P2 同上交叉 | 1,178,959 | OpenAgent:$1,178,959、月 −1.6%、季 −4.7%、年 −9.4%;表內標籤只寫「Sydney」 | ⚠️ | 數字吻合;地理一樣沒有「Greater Sydney」字樣。 | https://www.openagent.com.au/news/national-property-market-update-october-2026 |
| 原檔 | B1 RBA 現金利率 | 4.85%(11/3 升 0.25,前值 4.60);「2026-11-03 起」 | RBA 頁最新列:4 Nov 2026,+0.25,4.85;前一列 30 Sep 2026,+0.25,4.60 | ⚠️ | 利率與前值吻合;「11/3 起」不對,頁面生效日是 11/4(11/3 是公布日,補查檔已更正)。 | https://www.rba.gov.au/statistics/cash-rate/ |
| 原檔 | B2 自住房貸平均利率 | 約 6.75% | 沒開(原檔就沒有出處頁) | 未查 | 無網址可查。 | |
| 原檔 | T1 NSW 土地稅一般門檻 | 1,075,000 AUD 土地價值;2026 | 「General Threshold of $1,075,000」,2026 | ✅ | 吻合。 | https://www.revenue.nsw.gov.au/news-media-releases/preparing-for-the-2026-land-tax-year |
| 原檔 | T2 優質門檻 | 6,571,000 | 「Premium Threshold of $6,571,000」 | ✅ | 吻合。 | 同上 |
| 原檔 | T3 稅率「100 加超額部分 1.6%」 | 100 + 1.6% | 該頁沒有任何稅率,只連到另一頁 | 未查 | 原檔自己已註明頁內沒給稅率;我也沒開稅率頁。這個數字目前沒有已開頁面支持。 | 同上 |
| 補查檔 | L2 公寓租金 | 780 AUD/週(持平);2026 年 9 月季;Sydney | Elite Agent:「Sydney unit rent $780 a week, remained steady」;該句沒寫 Sydney,是接在雪梨句子之後;頁面標 median asking | ⚠️ | 數字吻合,地理靠上下文判斷(補查檔自己也有註明)。Time Out 那頁沒有雪梨公寓值。是「開價中位」。 | https://eliteagent.com/why-australian-rents-stall-despite-record-low-vacancies/ |
| 補查檔 | L1b 獨棟 | 835 | 「Sydney house rent $835 a week, down 0.6% ($5)」,2026 年 9 月季 | ✅ | 吻合,且與原檔 L1 一致。 | 同上 |
| 補查檔 | V5 空置率 Domain | 1.2%(6 月季 1.1;去年同期 0.9);2026 年 9 月季 | 「Sydney vacancy rate 1.2% in September, combined for houses and units; up from 1.1% in June and 0.9% a year earlier」 | ✅ | 吻合,而且是開頁讀到的,可從「搜尋摘要」升級成「已開頁(WebFetch)」。 | 同上 |
| 補查檔 | P3 公寓價值中位數 | 867,597(月 −1.0%,年 −3.8%);2026 年 9 月;Sydney | OpenAgent 10 月頁:兩段(0–10 萬字、10 萬字後)都找不到 867,597。WebSearch 摘要回報這是 Cotality 2026 年 9 月雪梨公寓中位,月 −1.0%、季 −3.0%、年 −3.8%,ProperEasy 表格也列同值 | ⚠️ | 數字與期間(9 月)有第二來源旁證,但補查檔指定的網址頁面上看不到,我沒有開到原頁。引用要換成 Cotality 原頁(搜尋結果有 discover.cotality.com 的 HVI SEP 2026 PDF)。 | https://www.openagent.com.au/news/national-property-market-update-october-2026 |
| 補查檔 | P4 獨棟價值中位數 | 1,466,060(月 −1.6%,年 −8.2%);2026 年 9 月 | 同上:指定網址頁面找不到;搜尋摘要:$1,466,060,月 −1.6%、季 −5.6%、年 −8.2% | ⚠️ | 同 P3。另:同一摘要給 9 月全住宅中位 1,198,596(月 −1.4%)。 | 同上 |
| 補查檔 | W1 供水固定費 | 26.65 AUD/季(最大);2026-27 | 「Water service (metered) $26.65 per quarter (maximum)」 | ✅ | 吻合。括號內 2025-26 的 29.73 在摘要沒顯示,沒驗。原網址是 301 轉址到 sydneywater.com.au/residential/accounts-billing/residential-pricing.html。 | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html |
| 補查檔 | W2 污水處理固定費 | 189.88 AUD/季 | 「Wastewater service $189.88 per quarter (maximum)」 | ✅ | 吻合(174.40 舊價沒驗)。 | 同上 |
| 補查檔 | W3 雨水排水費 | 公寓 9.67、獨棟 30.26 AUD/季 | 「Stormwater, houses $30.26;units or low-impact $9.67 per quarter」 | ✅ | 吻合。 | 同上 |
| 補查檔 | W4 用水單價 | 3.41 AUD/kL | 「Drinking water usage $3.41 per kilolitre」 | ✅ | 吻合(3.17 舊價沒驗)。 | 同上 |
| 補查檔 | W5 乾旱費率 | 3.84 AUD/kL;水庫低於 60% 適用,回升到 70% 以上取消 | 「Drought drinking water usage $3.84 per kilolitre」;Greater Sydney 水庫低於 60% 適用,回升超過 70% 取消 | ✅ | 吻合。 | 同上 |
| 補查檔 | W6 官方典型帳單 | 387.03 AUD/季(獨棟、50 kL、供水+污水、92 天) | 「Typical house bill (50 kL) $387.03 per 92-day quarter」 | ✅ | 吻合;頁面摘要也指出它不含雨水費。 | 同上 |
| 補查檔 | W7 公寓 396.70/季 | 396.70(換算) | 見下方「換算與加總的驗算」 | ✅ | 算式正確;但前提是有水表、位於雨水排水區、用水 50 kL(獨棟典型量)。 | 同上 |
| 補查檔 | G1 瓦斯 | 730 / 964 / 1,320 AUD/年 | 沒開 | 未查 | 工具次數用完。 | https://www.finder.com.au/energy/gas-nsw |
| 補查檔 | N1 NBN 50 | 50 / 約 86 / 100 AUD/月 | 沒開 | 未查 | 同上。 | https://www.canstar.com.au/internet/average-internet-bill/ |
| 補查檔 | N2 NBN 100 | 70 / / 110 | 沒開 | 未查 | 同上。 | https://www.mozo.com.au/broadband.html |
| 補查檔 | S1b 公寓管理費(確認 S1) | 854 AUD/季;NSW 全州,不是只有雪梨 | 同 S1:表格標 NSW(24,064 筆,佔高信心樣本約 49%);句子稱「Sydney (NSW)」;頁面「doesn't say whether the table figure covers only Sydney or the whole state」 | ⚠️ | 數值吻合、樣本數吻合(全澳 49,234 筆、19,270 棟、NSW 24,064)。差在:補查檔斷言「涵蓋 NSW 全州」比頁面說得更肯定,頁面只說表格標 NSW、句子標 Sydney (NSW),沒說是否只含雪梨。建議寫「NSW(頁面句子稱 Sydney (NSW))」。 | https://www.microburbs.com.au/research/strata-levies-whitepaper |
| 補查檔 | R1 North Sydney 最低費率 | 970.72 AUD/年(2026-27) | 沒開 | 未查 | IPART PDF 沒重開。 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Minimum-Rates-Instrument-2026-27-North-Sydney-Council.PDF |
| 補查檔 | R2 Blacktown | 1,140 / 1,233 AUD/年 | 沒開 | 未查 | 同上。 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Blacktown-City-Council-Attachment-Other-Attachment-2.5-Special-Rate-Variation-FAQs-and-Factsheets.PDF |
| 補查檔 | I1 房東/短租保險 | 500–700 AUD/年 | 沒開 | 未查 | 同上。 | https://www.rakidzich.com/articles/airbnb-insurance-australia |
| 補查檔 | B1b RBA 現金利率 | 4.85%(+0.25;前值 4.60);2026-11-04 生效;共 5 次升息 | 最新列「4 Nov 2026 / +0.25 / 4.85」,前一列「30 Sep 2026 / +0.25 / 4.60」;2026 全年:2/4→3.85、3/18→4.10、5/6→4.35、6/17 與 8/12 維持 4.35、9/30→4.60、11/4→4.85 | ✅ | 全部吻合;升息 5 次(2/4、3/18、5/6、9/30、11/4)也數對。 | https://www.rba.gov.au/statistics/cash-rate/ |
| 補查檔 | T4 ATO 短租申報重點 | 見補查檔 §5 | WebFetch HTTP 403 | ⏸ | 只用 WebFetch 試過,Chrome 因工具上限沒試。補查檔寫的 5 點(毛額申報、取消訂單訂金、共有人按比例、仲介代收時點、填報欄位)與「最後更新 2026-05-21」我都沒驗到。 | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare |

## 換算與加總的驗算

**⑤ Sydney Water 公寓 396.70/季(補查檔 W7)**
- 頁面上的項目(2026-27,每季最大值,92 天):供水(有水表)26.65;污水 189.88;雨水(公寓/低衝擊)9.67;用水 3.41/kL。
- 用水:50 × 3.41 = 170.50
- 固定費:26.65 + 189.88 + 9.67 = 226.20
- 合計:226.20 + 170.50 = **396.70** ✅ 與補查檔相同
- 對照官方典型獨棟 387.03:26.65 + 189.88 + 170.50 = **387.03** ✅(與頁面一致,且不含雨水費)
- 兩者差 396.70 − 387.03 = 9.67 = 公寓雨水費 ✅
- 年化:396.70 × 4 = 1,586.80 ≈ 1,587 ✅(補查檔已註明是粗略,最長季乘 4)
- 注意:92 天是最大值,90、91 天的季較低;50 kL 是官方獨棟典型量,小公寓可能遠少。

**⑪ 原檔檔尾「三種新房東每月固定成本」**
- 電費 ÷12(每年轉每月):
  - 低 1,875 ÷ 12 = 156.25 → 約 156 ✅
  - 中 1,965 ÷ 12 = 163.75 → 約 164 ✅
  - 高 2,411 ÷ 12 = 200.92 → 約 201 ✅
- 管理費 ÷3(每季轉每月):
  - 低 600 ÷ 3 = 200 ✅
  - 中 854 ÷ 3 = 284.67 → 約 285 ✅
  - 高 1,500 ÷ 3 = 500 ✅
- 甲的加總(只含電費+管理費):
  - 低 156.25 + 200 = 356.25 → 約 356 ✅
  - 中 163.75 + 284.67 = 448.42 → 筆記寫約 449;差 1 元是先四捨五入再加(164 + 285 = 449),精確值約 448。⚠️ 無實質影響。
  - 高 200.92 + 500 = 700.92 → 約 701 ✅
- 乙的租金(每週 × 52 ÷ 12):
  - 835 × 52 = 43,420;÷ 12 = 3,618.33 → 約 3,618 ✅
  - 750 × 52 = 39,000;÷ 12 = 3,250 ✅
  - 780 × 52 = 40,560;÷ 12 = 3,380 ✅
- 乙的範例:3,250 + 156.25 = 3,406.25;3,250 + 200.92 = 3,450.92 → 約 3,406–3,451 ✅
- 丙的利息:1,000,000 × 1% = 10,000/年;÷ 12 = 833.33 → 約 833 ✅
- 是否有把每週、每季、每年直接相加:沒有。每週租金都先 ×52÷12;每季管理費先 ÷3;每年電費先 ÷12。
- 仍要留意的口徑問題(不是算錯):
  1. 電費三檔混了供電區與年度(低 = Ausgrid 2026-27 草案,中 = Ausgrid 2025-26,高 = Endeavour 2025-26),原檔自己有註明。
  2. 管理費的低(S3 下限 600)、高(S5 下限 1,500)是不同樓型的下限,中位 854 是 NSW 表(見 S1)。
  3. 乙的租金範例混了不同年度,原檔有註明「僅示範算法」。
  4. 甲、乙都沒有水、瓦斯、網路、市政費、保險,總和是「只含兩列」的下限,不是完整月成本;補查檔現在已有水費(W)、瓦斯 G1、網路 N1 的候選值,但這份原檔的加總沒有更新。

## 兩份互相矛盾的地方

1. **S1 管理費地理範圍**:原檔寫 Sydney;補查檔改成「NSW 全州」。頁面兩邊都有字(句子 Sydney (NSW)、表格 NSW),沒說是否只含雪梨。兩份都說得太肯定,建議寫「NSW(句子稱 Sydney (NSW))」。
2. **RBA 利率生效日**:原檔「11/3 起」;補查檔「11/4 生效、11/3 公布」。RBA 頁面寫 4 Nov 2026,補查檔正確,原檔 B1 應改。
3. **P1 與 P3/P4 期間不同**:P1 是 2026-10(合併 1,178,959),P3/P4 是 2026-09(公寓 867,597、獨棟 1,466,060)。補查檔已提醒不要互推。我另外確認 9 月全住宅中位是 1,198,596(搜尋摘要),10 月 1,178,959 比 9 月低 1.64%,與「月 −1.6%」一致,所以 P1 與 P3/P4 沒有互相打架,只是不同月份。
4. **L6(850)與 L1/L1b(835)**:原檔 L6 說 2026 年 6 月季獨棟 850;但 Time Out 與 Elite Agent 兩頁都寫 9 月季「−$5 到 835」,代表 6 月季是 840,不是 850。原檔已自己標出「對不上」,我這邊兩個已開頁面都站在 835/840 這邊,所以 L6 應視為轉述有誤。
5. **S6 與 S1/S2**:原檔不採 S6(1,500–3,000)是因為「單位沒寫清楚」,頁面確認單位是每季,理由要改成「兩房、粗估、約 S1 的兩倍」。
6. **M1 與 M2**:原檔推論「M2 雪梨 15–22%,上限比 M1 低 3 點」;M2 頁面並沒有這個數字(見表 ❌),所以兩者其實沒有衝突,是 M2 本身需要刪掉。
7. **V5 取得方式**:補查檔把 V5 標為搜尋摘要;其實 Elite Agent 頁面就寫了 1.2 / 1.1 / 0.9,可以升級。
8. **ID 重複**:兩份檔的 W1、G1、N1、R1、I1、P3、P4、L2、T4 在原檔是「查不到」、在補查檔有值,引用時要以補查檔為準,並寫明檔名。

## 簡報上可以直接用的數字

(都是這次在頁面上親眼看到,仍要標來源與期間)
- Sydney Water 2026-27(官方):供水固定費 26.65/季、污水 189.88/季、雨水(公寓)9.67/季(獨棟 30.26)、用水 3.41/kL、官方典型獨棟帳單 387.03/季(50 kL,92 天季);固定費是最長季上限,要寫「最多」。
- RBA 現金利率目標 4.85%,2026-11-04 生效(官方頁)。
- NSW 土地稅 2026:一般門檻 1,075,000、優質門檻 6,571,000,單位是土地價值(Revenue NSW)。
- 雪梨獨棟屋租金中位 835 AUD/週,2026 年 9 月季,較上季 −0.6%(−5)(Domain 經 Time Out、Elite Agent;標「開價中位」)。
- 雪梨租金季變動 −0.4%(Cotality,2026 年 9 月季);SQM 雪梨空置率 1.8%(2026 年 9 月);Domain 雪梨空置率 1.2%(9 月季,6 月季 1.1,去年同期 0.9)。
- Airbnb 平台費 15.5%(訂房小計,2025-12 起,全澳,Houst 頁,2026-05 更新);代管抽成「多數 20–22%、範圍 15–25%」(Houst,全澳,代管商自己的說法)。
- 清潔費行情 50–80 AUD/次、自己打掃約 65、大房找清潔公司約 105(Hospitable,2026-11-13,全澳;是向房客收的行情,不是實際成本)。
- 管理費區間(Stratachecks,NSW 粗略參考,每季):小棟無電梯 600–1,200;中型有電梯 1,000–2,500;大型設施齊全 1,500–4,000 以上。

## 簡報上要加註或不要用的數字

要加註:
- 電費 1,965 / 2,411 / 2,741(2025-26)與 1,875 / 2,347 / 2,515(2026-27 草案):數字吻合 Canstar 轉述的 AER 預設價,但頁面只寫「Current price」(2025-26 是推論),2026-27 是草案、不是最終版;單一費率、無受控負載、沒給度數;小公寓實際帳單通常較低。AER 原件這次打不開(逾時)。
- 雪梨公寓租金 780 AUD/週(2026 年 9 月季):句子沒寫 Sydney(靠上下文),是第二手轉述,Domain 原頁沒開到。
- 雪梨房價中位 1,178,959(2026-10):頁面只寫「Sydney」,不要寫成「Greater Sydney」;那頁有「較 2 月高點低逾 10%」,「三個月 −4.7%」要引 OpenAgent 頁。
- 公寓 867,597 / 獨棟 1,466,060(2026-09):在指定網址沒看到,只有搜尋摘要與 ProperEasy 表格旁證;月份和合併值(10 月)不同,要引用請先換成 Cotality 原頁。
- 管理費 854 AUD/季:寫「NSW(頁面句子稱 Sydney (NSW))」,不要寫成「雪梨公寓」。另 S6 標準兩房 1,500–3,000/季(每季,2026 粗估)比 854 高很多,兩個要一起看。
- Cotality 空置率 2.5%:頁面該句沒標季別;三個供應商(Cotality 2.5、SQM 1.8、Domain 1.2)口徑不同,不要放同一條線。
- 共同房東抽成 M3 的「高 25%」:頁面 25% 是 full-service 的下限(25%+),不是上限。
- 平台費 15.5% 是以訂房小計計算,含清潔費。
- 清潔費「低 50」是平均區間 50–80 的下緣,幣別頁面沒明寫。

不要用:
- M2「雪梨/墨爾本代管抽成 15–22%」:Houst 該頁沒有這個數字(只有「其他地區 14% 起」)。
- L6「2026 年 6 月季獨棟 850」:與已驗證頁面推出的 840 矛盾,而且沒開原頁。
- L3 / L4 / V3(Domain 2025-09 季)與 L5 / V4:原頁打不開或沒開(L3/L4/V3 HTTP 403),雖有 Elite Agent 的旁證(V3 的 0.9、V4 的 1.1),仍待原頁。
- 沒查的列:S2、B2(6.75% 自住房貸利率,原檔就沒有出處頁)、T3(稅率 100 + 1.6%,頁面沒給)、G1 / N1 / N2(瓦斯與網路)、R1 / R2(市政費)、I1(保險)、E7(AER 原件,逾時)、T4(ATO,403)。這些要引用前先回頭開頁。
