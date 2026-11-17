這份清單是什麼:這幾天查過的網站和資料的總清單。第一段是真的開到網頁、看到數字的;第二段是沒查到的;第三段是還缺的數據。
整理日期:2026-11-15。
三段各幾列:第一段「已經查過的資料」84 列;第二段「沒查到的」19 列(A 網頁進不去 6 列、B 只看到搜尋摘要 13 列);第三段「還缺哪些數據」32 列。

第一段最後一欄「狀態」只有這幾種:
- 有查到:開到網頁,看到的數字跟筆記一樣。
- 有查到,數字只能當大概:開到網頁,但有些地方有差(例如範圍不同、年份舊、是估計值),只能當參考範圍。
- 有查到,但網頁上的數字跟一開始記的不一樣:開到網頁,但頁面上實際的數字不是原本記的那個;「查到什麼」寫的是網頁上實際的數字。
- 有查到(只看過一次):只有一個人開過,沒有第二次核對。
沒開到網頁的(進不去、或只看到搜尋摘要)全部放在第二段。外部行情都是網路公開的報價或估計,不是官方統計。

# 第一段:已經查過的資料(一個網站一列)

## 0 我們自己用的資料(3 列)

主資料是 Inside Airbnb;街區邊界來自澳洲統計局;題目範圍看課程說明。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| Inside Airbnb(雪梨四期) | https://insideairbnb.com/get-the-data/ ;四期 listings:https://data.insideairbnb.com/australia/nsw/sydney/2025-12-12/data/listings.csv.gz  、https://data.insideairbnb.com/australia/nsw/sydney/2026-03-21/data/listings.csv.gz 、https://data.insideairbnb.com/australia/nsw/sydney/2026-06-16/data/listings.csv.gz 、https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/listings.csv.gz | 整個專題的主資料(房源、開價、設施、位置、評論、日曆) | 免費、公開、有雪梨四期 | 四期:2025-12-12 有 20,436 間(沒有價格)、2026-03-21 有 13,563 間、2026-06-16 有 20,573 間、2026-09-16 有 20,833 間(主要用這一期)。備註:四期共 28 個檔大小和檢查碼跟下載紀錄一致;晚上補查看公開頁,2026-09-16 也是 20,833 | 有查到 |
| 澳洲統計局(ABS)街區邊界 | https://geo.abs.gov.au/arcgis/rest/services/ASGS2021/SAL/MapServer | 畫地圖,把房子對到街區 | Inside Airbnb 只有 38 個大區,沒有街區邊界 | NSW 與房源範圍相交的街區 777 個(分兩頁下載,各 500、277 個);授權 CC BY 4.0。備註:只記了檔案大小和檢查碼;服務說明寫邊界不等於法定行政邊界,只供統計 | 有查到(只看過一次) |
| 課程 Canvas 的作業說明 | (要登入學校帳號,不放連結) | 確認題目和要交什麼 | 專題範圍以作業說明為準 | 作業的題目與要求。備註:學校官方說明 | 有查到(只看過一次) |

## 1 短租市場(5 列)

目的:看外面怎麼估每晚價、住滿幾成、一年收多少,給「收入試算」當參考範圍。原因:我們的資料只有房東開的價,沒有成交價,也沒有實際住了幾晚。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| airdna.co | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 看外面怎麼估每晚價、住滿幾成、一年收多少,給「收入試算」當參考範圍 | 我們的資料只有房東開的價,沒有成交價,也沒有實際住了幾晚 | 雪梨活躍房源 16,392 間;每晚價 US$193、住滿 67%、每間年收入約 US$40.8K;季節性分數 91/100 | 有查到 |
| airroi.com | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 看外面怎麼估每晚價、住滿幾成、一年收多少,給「收入試算」當參考範圍 | 我們的資料只有房東開的價,沒有成交價,也沒有實際住了幾晚 | 每晚價 AUD 399、住滿 49.5%、每間年收入 AUD 52,495;Studio 年收入中位數 AUD 40,500;12 月最旺、6 月最淡 | 有查到 |
| guestfavorites.com | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 看外面怎麼估每晚價、住滿幾成、一年收多少,給「收入試算」當參考範圍 | 我們的資料只有房東開的價,沒有成交價,也沒有實際住了幾晚 | 每晚價 AUD 336、住滿 68%、每間年收入 AUD 83,094 | 有查到,數字只能當大概 |
| airbtics.com | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ | 看外面怎麼估每晚價、住滿幾成、一年收多少,給「收入試算」當參考範圍 | 我們的資料只有房東開的價,沒有成交價,也沒有實際住了幾晚 | 中位數:住滿 75%、每晚價 AUD 281、每間年收入 AUD 79,355 | 有查到,數字只能當大概 |
| hometime.io | https://www.hometime.io/blog/market-report-short-term-rental-sydney | 看外面怎麼估每晚價、住滿幾成、一年收多少,給「收入試算」當參考範圍 | 我們的資料只有房東開的價,沒有成交價,也沒有實際住了幾晚 | 市場平均住滿 67%;典型每間年收入 $50,800–$97,700(頁面沒標幣別);價格高峰在 12–1 月 | 有查到,數字只能當大概 |

## 2 規定和平台費(6 列)

目的:確認一年最多能租幾天、平台抽多少。原因:收入試算要用;工具不能建議違規的做法。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| planning.nsw.gov.au | https://www.planning.nsw.gov.au/STRA | 確認一年最多能租幾天、平台抽多少 | 收入試算要用;工具不能建議違規的做法 | 非房東同住每年最多 180 天;房東同住不限天數;新登記費 AUD 65(官方頁最後更新 2025-02-10) | 有查到,數字只能當大概 |
| airbnb.com.au | https://www.airbnb.com.au/resources/hosting-homes/a/simplifying-airbnb-service-fees-746 | 確認一年最多能租幾天、平台抽多少 | 收入試算要用;工具不能建議違規的做法 | 房東單一服務費 15.5%,房客不再另付;舊制是房東約 3%、房客另付(沒開原頁)。另有 1 個數字沒有人開過原頁(見第二段 B) | 有查到 |
| hometime.io | https://www.hometime.io/blog/what-airbnb-host-only-fee-means-for-you | 確認一年最多能租幾天、平台抽多少 | 收入試算要用;工具不能建議違規的做法 | 改制日有兩種說法:2025-10-27(用管理軟體連線的房東)、2026-09-15(自己管理、仍在舊制的房東) | 有查到 |
| houst.com | https://www.houst.com/blog/airbnb-hosting-fees-australia | 確認一年最多能租幾天、平台抽多少 | 收入試算要用;工具不能建議違規的做法 | 平台對房東抽成 15.5%(訂房小計) | 有查到 |
| revenue.nsw.gov.au | https://www.revenue.nsw.gov.au/news-media-releases/preparing-for-the-2026-land-tax-year | 看持有房子要不要付土地稅(屬買房投資那一類,現在不在範圍,只留紀錄) | 收入試算要用;工具不能建議違規的做法 | 2026 土地稅年度起徵點 AUD 1,075,000(土地價值);優質門檻 AUD 6,571,000;超過起徵點的稅率沒開原頁。另有 1 個數字沒有人開過原頁(見第二段 B) | 有查到 |
| ato.gov.au | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare | 確認短租收入要不要報稅(收入試算只做提醒,不算稅) | 收入試算要用;工具不能建議違規的做法 | 短租、透過平台出租、出租自己住家的收入都要申報(文字重點,沒有數字;另一人打不開頁面,沒有第二次核對) | 有查到(只看過一次) |

## 3 裝修和佈置(13 列)

目的:給「裝修、開辦費」一個參考範圍。原因:我們的資料沒有裝修費;這一格由使用者自己填。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| whatsthedamage.com.au | https://whatsthedamage.com.au/bathroom-renovation-cost-sydney/cost-breakdown/ | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 浴室翻新中間值:基本 AUD 17,250、標準 31,050、高階 48,300;廚房簡單換新 16,100;地板每平方公尺約 AUD 75–230 | 有查到 |
| thequoteyard.com.au | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 浴室簡單更新 AUD 8,000–15,000、標準 25,000–45,000;廚房標準 30,000–55,000;整間臥室油漆 450–750 | 有查到 |
| airtasker.com | https://www.airtasker.com/au/costs/house-renovation/house-renovation-cost/ | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 浴室翻新起價 AUD 14,900、廚房起價 30,000;智慧鎖安裝師傅報價中位數 AUD 276 | 有查到 |
| domain.com.au | https://www.domain.com.au/advice/bathroom-renovation-costs/ | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 預算型整間浴室翻新 AUD 20,000–27,000(頁面沒標幣別,推定 AUD) | 有查到 |
| houzz.com.au | https://www.houzz.com.au/magazine/bathroom-renovation-how-much-will-it-cost-me-stsetivw-vs~26882976 | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 浴室低檔帶 AUD 4,000–20,000(2014 年舊資料,只拿來對照) | 有查到,數字只能當大概 |
| airbtics.com | https://airbtics.com/starting-an-airbnb-australia | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 1 個臥室的 Airbnb 開辦合計 AUD 5,358、2 個臥室 AUD 7,539(含家具、智慧鎖、攝影機等)。另有 1 個數字沒有人開過原頁(見第二段 B) | 有查到,數字只能當大概 |
| minoan.com | https://minoan.com/blog/airbnb-furniture-packages | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 小型 1 個臥室家具套裝 2,000–5,000(搜尋摘要;來源是非澳洲業者,幣別沒確認) | 有查到,數字只能當大概 |
| houzz.se | https://www.houzz.se/pro/hostmybnb/airbnb-furnishing-services-by-hostmybnb | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 全套代佈置服務 AUD 12,000–25,000(搜尋摘要,沒標房數) | 有查到 |
| hometime.io | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 專業攝影 AUD 250–1,000+;1 個臥室「寬裕但不奢華」開辦約 AUD 5,000–7,000;轉述 Airbnb:用專業攝影的房源次年收入多 21% | 有查到,數字只能當大概 |
| entry-point.com.au | https://entry-point.com.au/products/yale-assure-keyed-electronic-deadbolt-black | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | Yale 智慧門鎖舊筆記記 AUD 520(特價)/660(原價);晚上補查看到頁面資料是 550/787.07,不一樣 | 有查到,但網頁上的數字跟一開始記的不一樣 |
| buywisely.com.au | https://buywisely.com.au/product/yale-keyless-connected-door-lock | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | Yale 智慧門鎖舊筆記記最低價 AUD 145;頁面沒有 145(比價範圍 157.21–315.17) | 有查到,但網頁上的數字跟一開始記的不一樣 |
| maidforyou.com.au | https://www.maidforyou.com.au/blog/how-much-end-of-lease-clean/ | 給「裝修、開辦費」一個參考範圍 | 我們的資料沒有裝修費;這一格由使用者自己填 | 首次深度清潔 AUD 242;退租級大掃除 Studio/1 個臥室 410、2 個臥室 450 | 有查到 |
| abs.gov.au | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026 | 看營造成本漲多少,判斷裝修費會不會變貴 | 我們的資料沒有裝修費;這一格由使用者自己填 | 2026 年 9 月季:建築營造季增 +1.3%、住宅營造季增 +1.1%;全澳最終需求年增 +3.6%(不是營造專屬)。有 1 個數字頁面上不一樣 | 有查到,數字只能當大概 |

## 4 每月成本(10 列)

目的:看電、水、瓦斯、網路、管理費、保險的每月參考數字。原因:我們的資料沒有成本。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| canstar.com.au | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | Ausgrid 供電區單一費率住宅年電費 AUD 1,965(2025-26)、2026-27 草案 1,875;Endeavour 2,411、草案 2,347。另有 2 個數字沒有人開過原頁(見第二段 B)〔2026-11-17 更正:最終版已出(AER 最終決定 PDF p.16,含 GST):Ausgrid 平價 1,899(年用電 3,900 kWh)、Endeavour 平價 2,328(4,900 kWh)。草案的 1,875 / 2,347 不要再用〕 | 有查到,數字只能當大概 |
| hospitable.com | https://hospitable.com/airbnb-cleaning-fee-australia | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 每次退房向房客收的清潔費 AUD 50–105(65 是房東自己打掃) | 有查到,數字只能當大概 |
| houst.com | https://www.houst.com/blog/airbnb-hosting-fees-australia | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 短租代管公司抽成 15–25%,多數落在 20–22% | 有查到 |
| rakidzich.com | https://www.rakidzich.com/articles/airbnb-co-hosting-australia | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 共同房東抽成 10–25%(最常見 20%);短租保險 AUD 500–700/年(只有單一業者的行銷文)。另有 1 個數字沒有人開過原頁(見第二段 B) | 有查到,數字只能當大概 |
| microburbs.com.au | https://www.microburbs.com.au/research/strata-levies-whitepaper | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 公寓管理費典型約 AUD 854/季 | 有查到,數字只能當大概 |
| flatchat.com.au | https://www.flatchat.com.au/topic/how-do-you-guesstimate-levies/ | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 中位價公寓管理費約 AUD 850/季(論壇估算;晚上補查看到是 2024-06-09 的貼文,不是統計) | 有查到,數字只能當大概 |
| stratachecks.com.au | https://stratachecks.com.au/blog/beginners-guide-strata-levies | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 管理費(AUD/季):小棟無電梯 600–1,200、中型有電梯 1,000–2,500、大型設施齊全 1,500–4,000 以上 | 有查到 |
| savingsmate.com.au | https://savingsmate.com.au/blog/strata-fees-explained-australia | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 標準兩房公寓管理費 AUD 1,500–3,000/季 | 有查到 |
| sydneywater.com.au | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 2026-27 用水單價 AUD 3.41/kL;官方典型季帳單(獨棟、50 kL)AUD 387.03 | 有查到 |
| 研究檔自己算(換算;用到的數字來自 Sydney Water 官方頁) | (筆記沒記網址) | 看電、水、瓦斯、網路、管理費、保險的每月參考數字 | 我們的資料沒有成本 | 公寓(有水表)用水 50 kL/季的季帳單 AUD 396.70(用 Sydney Water 官方頁的數字算的) | 有查到 |

## 5 房市(租金、房價、利率)(9 列)

目的:當時在評估「二房東」和「買房投資」兩種人。原因:他們要用租金、房價、利率。這兩種人現在不在題目範圍,這一類只留紀錄。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| timeout.com | https://www.timeout.com/australia/news/australias-rental-market-has-officially-stalled-despite-capital-city-shortages-100726 | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 雪梨每週租金中位數 AUD 835(單季 −5) | 有查到 |
| eliteagent.com | https://eliteagent.com/why-australian-rents-stall-despite-record-low-vacancies/ | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 雪梨公寓每週租金中位數 AUD 780(持平);空置率 1.2%(2026 年 9 月季) | 有查到,數字只能當大概 |
| insight.domain.com.au | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 2025 年 9 月季雪梨公寓每週 AUD 750(年增 4.9%)、獨棟 780;空置率 0.9% | 有查到 |
| thenewdaily.com.au | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 舊筆記記公寓 780、獨棟 850、空置率 1.1%;晚上補查開原頁,雪梨只有 835 一個數字 | 有查到,但網頁上的數字跟一開始記的不一樣 |
| thenightly.com.au | https://thenightly.com.au/australia/nsw/sydney-rents-fall-despite-fears-of-a-post-budget-spike-c-22990976 | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 雪梨租金單季 −0.4%;空置率 2.5%(去年同期 1.8%);數字出自 Cotality | 有查到,數字只能當大概 |
| openagent.com.au | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 雪梨空置率 1.8%;全住宅價值中位數 AUD 1,178,959;舊筆記記的公寓 867,597、獨棟 1,466,060 頁面沒有 | 有查到,數字只能當大概 |
| commbank.com.au | https://www.commbank.com.au/articles/newsroom/2026/11/sydney-home-prices-fall-more-than-10-percent-from-peak.html | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 雪梨住宅價值中位數 AUD 1,178,959(月 −1.6%);數字出自 Cotality | 有查到,數字只能當大概 |
| investinglive.com | https://investinglive.com/central-banks/more-rba-lifts-cash-rate-to-4-85-in-split-6-3-vote-sees-inflation-above-3-until-late-2027/ | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | 央行(RBA)現金利率 4.85%(2026-11-04 升 0.25 個百分點) | 有查到,數字只能當大概 |
| rba.gov.au | https://www.rba.gov.au/statistics/cash-rate/ | 當時在評估「二房東」和「買房投資」兩種人 | 他們要用租金、房價、利率 | RBA 現金利率 4.85%(官方頁確認) | 有查到 |

## 6 假期和活動日期的官方網站(13 列)

目的:做「淡旺季和假期提醒」的日曆。原因:我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子。晚上補查新開到的 NRL、澳洲國慶日官方站放在第 8 組。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| NSW Government 公眾假期 | https://www.nsw.gov.au/about-nsw/public-holidays | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2026-12-25、12-26、12-28 和 2027 年,共 17 天公眾假期(含補假);2027-08-02 銀行假日不算公眾假期。備註:18 列都對 | 有查到 |
| NSW Department of Education 學校假期 | https://education.nsw.gov.au/schooling/calendars/2026 、https://education.nsw.gov.au/schooling/calendars/2027 | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 東部分區暑假 2026-12-18 至 2027-01-27;2027 冬假 07-05 至 07-16。備註:7 列都對);頁面沒寫「雪梨 = 東部」,引用要註明「NSW 東部分區」 | 有查到 |
| Sydney New Year's Eve 跨年煙火 | https://www.sydneynewyearseve.com/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 煙火 9pm 與午夜;頁面沒寫「12 月 31 日」,日期由「跨年夜」推出。備註:日期是推的 | 有查到,數字只能當大概 |
| Sydney Festival 雪梨藝術節 | https://www.sydneyfestival.org.au/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027 年 1 月;頁面節目最早 1/7、最晚 1/25(筆記寫到 1/24,差一天)。備註:只寫「2027 年 1 月」最安全 | 有查到,數字只能當大概 |
| City of Sydney 農曆新年慶典(Lunar Festival) | https://www.cityofsydney.nsw.gov.au/sydney-lunar-festival | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 官方頁只有 2026 馬年版,沒有 2027 日期。備註:確認「沒有日期」 | 有查到 |
| Sydney Mardi Gras | https://www.mardigras.org.au/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027-02-12 至 03-07(節慶期間;大遊行當天頁面沒寫) | 有查到 |
| Sydney Royal Easter Show | https://www.eastershow.com.au/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027-03-19 至 03-30 | 有查到 |
| Vivid Sydney | https://www.vividsydney.com/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027-05-28 至 06-19 | 有查到 |
| Sydney Olympic Park(State of Origin) | (筆記記的網址不完整,不放連結) | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2026-05-27 在 Accor Stadium,預期約 8 萬人;2027 場次未公布;筆記記的網址不完整,沒放連結。備註:2026 場次,沒有當成 2027 用 | 有查到 |
| City2Surf | https://www.city2surf.com.au/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027-08-08;2026 版連續第 3 年額滿 | 有查到 |
| TCS Sydney Marathon | https://www.tcssydneymarathon.com/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027-08-29;2026 版官方寫 40,000+ 跑者 | 有查到 |
| Sculpture by the Sea(Bondi) | https://sculpturebythesea.com/bondi | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2027-10-22 至 11-08 | 有查到 |
| Rolex Sydney Hobart 帆船賽 | https://www.rolexsydneyhobart.com/ | 做「淡旺季和假期提醒」的日曆 | 我們的資料看得出哪幾天特別滿,但看不出那幾天是什麼日子 | 2026-12-26;2027 未公布。備註:頁面沒明寫「開賽日」 | 有查到,數字只能當大概 |

## 7 假期、活動對價格的影響(10 列)

目的:找外面有沒有「假期會漲多少」的數字。原因:我們的資料沒有每天的價格。結論:只有旅館的數字和少數短租的說法,所以延伸 2 只做提醒、不說漲多少。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| PEDESTRIAN.TV | https://www.pedestrian.tv/news/sydney-airbnb-prices-surge-up-to-4300-per-night-over-new-year-period/ | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 2015 年跨年夜:市區一間公寓 12/31 含費用 AUD 4,303,平常約 260。備註:只有 2015 一年 | 有查到 |
| Hometime 部落格(活動與跨年) | https://hometime.io/blog/how-events-sydney-boost-property-investments | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 說跨年夜每晚價最高、12–1 月是高點,沒有金額;說佈置好的房子最多賺 2 倍。備註:頁面日期是 2026-07-08,筆記寫成 2025 | 有查到,數字只能當大概 |
| STR Specialist | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 建議值:12–2 月約基本價 1.5–2 倍,週末 1.2–1.4 倍(不是量到的)。備註:都是建議值,沒有來源 | 有查到 |
| PriceLabs | https://hello.pricelabs.co/australia-airbnb-market-trends/?amp=1 | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 全澳(不是雪梨)2024 年 7–11 月住滿 56.8%–63.8%;10 月每晚價最高 US$182.7。備註:「10 月最高」只在 7–11 月內比 | 有查到,數字只能當大概 |
| Your Investment Property 雜誌 | https://www.yourinvestmentpropertymag.com.au/market-analysis/signs-point-to-bumper-peak-season-for-sydneys-shortterm-rental-hosts-this-summer | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 雪梨 12 月每晚價比全年各月平均高 25%、夏季高 15%(約 2018–2019 資料,引 AirDNA)。備註:25% 比較的對象頁面沒寫;資料很舊 | 有查到,數字只能當大概 |
| Hospitality Net | https://www.hospitalitynet.org/news/4120883/record-high-room-rates-in-melbourne-sydney-driven-by-the-eras-tour 、https://www.hospitalitynet.org/news/4115445/sydney-worldpride-2023-pushed-hotel-performance-to-pre-pandemic-levels | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 旅館(不是短租):2024-02 雪梨入住率 86.5%、每晚均價 AUD 329.05(+16.4%) | 有查到 |
| CoStar | https://www.costar.com/products/str-benchmark/resources/press-releases/record-high-room-rates-melbourne-sydney-driven-eras 、https://www.costar.com/article/789563613/str-sydney-worldpride-2023-pushed-hotel-performance-to-pre-pandemic-levels | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 旅館:2023 年 WorldPride + Mardi Gras 17 天,每晚均價比 2019 同期高 25.7%。備註:晚上補查開原頁,數字跟轉載一樣 | 有查到 |
| Destination NSW | https://www.destinationnsw.com.au/newsroom/vivid-sydney-drives-hotel-occupancy-surge | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 旅館:2026 年 6 月入住率 74.1%,6/6 最高 92.7%。備註:「演唱會」頁面沒這樣寫 | 有查到,數字只能當大概 |
| Lighthouse | https://mylighthouse.com/resources/blog/taylor-swifts-eras-tour-hotel-room-rates-asia-pacific-leg | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 2024-02 雪梨短租開價比下一個週末高 30%(是開價,不是成交價)。備註:筆記自己標中低可信度 | 有查到 |
| Airbnb 說明頁(Resource Center / Help Center) | https://www.airbnb.com/resources/hosting-homes/a/understanding-pricing-on-airbnb-370 、https://www.airbnb.com/resources/hosting-homes/a/using-airbnb-pricing-tools-707 、https://www.airbnb.com/help/article/1168 | 找外面有沒有「假期會漲多少」的數字 | 我們的資料沒有每天的價格 | 週末夜 = 週五、週六;每週折扣用於 7 晚以上、每月折扣 28 晚以上;沒有「漲多少」的數字 | 有查到 |

## 8 晚上補查開到的(15 列)

18 個網站裡開到 13 個(以核對那份為準);已經在第 1–7 組出現過的,這裡只補晚上的新結果,不重複算成新網站。新網站 5 個:hipages、Master Builders NSW、NRL、Airbnb 新聞室、澳洲國慶日官方站。另加 AirDNA app、Variety 兩列(不在那 18 個裡)。

| 名稱 | 網址 | 查它的目的 | 為什麼要查 | 查到什麼 | 狀態 |
|---|---|---|---|---|---|
| hipages(新網站) | https://hipages.com.au/article/how_much_does_bathroom_renovation_cost 、https://hipages.com.au/article/how_much_does_kitchen_renovation_cost | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 浴室全澳平均 AUD 8,000–35,000、廚房 30,000–50,000(2026-01 更新;不是雪梨專屬) | 有查到 |
| The New Daily(第 5 組) | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 雪梨租金中位數只有一個數字:掉 AUD 5 到 835;舊筆記的公寓 780、獨棟 850 頁面沒有。備註:頁面確實是 835;舊的 780/850 不一樣 | 有查到,但網頁上的數字跟一開始記的不一樣 |
| OpenAgent(第 5 組) | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 雪梨全住宅價值中位數 AUD 1,178,959(年 −9.4%)、空置率 1.8%;公寓 867,597、獨棟 1,466,060 頁面沒有 | 有查到,但網頁上的數字跟一開始記的不一樣 |
| Flat Chat(第 4 組) | https://www.flatchat.com.au/flat-chat-forum/topic/how-do-you-guesstimate-levies/ | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 850/季對上,但是 2024-06-09 站長自己隨手估的,不是統計 | 有查到,數字只能當大概 |
| Master Builders NSW(新網站) | https://www.mbansw.asn.au/sites/default/files/datapack_-_building_input_and_output_costs_-_sept_2025_qtr.pdf | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 房屋營造材料成本到 2025-09 止一年:雪梨 +2.0%、全澳 +2.1%(只有材料,只讀第 1 頁) | 有查到 |
| ATO(第 2 組) | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 短租、平台出租都要申報;取消訂房留下的訂金也算租金收入。備註:獨立查核打不開頁面 | 有查到(只看過一次) |
| NRL(新網站) | https://www.nrl.com/hospitality/grand-final/ 、https://travel.nrl.com/2027-grand-final | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 2026 總決賽 10/4 在 Accor Stadium;2027 日期官方寫 TBD | 有查到 |
| CoStar 原頁(第 7 組) | https://www.costar.com/products/str-benchmark/resources/press-releases/record-high-room-rates-melbourne-sydney-driven-eras | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 2024-02 雪梨旅館入住率 86.5%、每晚均價 AUD 329.05、2/24 最高 AUD 527.52;跟轉載逐項一樣 | 有查到 |
| Airbnb 新聞室(新網站) | https://news.airbnb.com/en-au/airbnb-data-reveals-surge-in-visitors-flocking-to-vivid-sydney 、https://news.airbnb.com/en-au/airbnb-proud-to-be-vivid-sydney-community-partner-once-again | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 2024-06-06 稿:Vivid 期間搜尋晚數成長近 100%、前一年平均住約 4 天;2025-05-22 稿:搜尋預訂 +35% 以上。備註:舊句出自 2024 那篇;「約兩倍」是搜尋晚數,不是訂房量 | 有查到 |
| AirDNA 雪梨公開頁(第 1 組) | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 跟之前一樣:16,392 間、住滿 67%、每晚價 US$193;每月數字不在頁面上 | 有查到 |
| AirDNA app(另加) | https://app.airdna.co/data/au/30830/overview | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 只開放年收入 US$40,819、房源 16,392、Market Score 82;每月數字、淡旺季、分房型、未來價格全部要付費。備註:跟公開頁數字相符 | 有查到 |
| 澳洲國慶日官方站(新網站) | https://www.australiaday.com.au/ | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 2027-01-26 活動:日出儀式 05:20、午間禮砲 11:55、晚上 7:30 演唱會(含煙火)。備註:煙火沒有單獨時間 | 有查到 |
| Inside Airbnb 雪梨頁(第 0 組) | https://insideairbnb.com/sydney/ | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 2026-09-16 那期共 20,833 筆;選「Sydney」並只看短租是 17,883 筆 | 有查到 |
| Entry Point(第 3 組) | https://www.entry-point.com.au/products/yale-assure-keyed-electronic-deadbolt-black | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | 畫面價格 AUD 550(劃線原價 787.07);舊筆記的 520/660 不一樣。備註:原記要登入才看得到價格;沒登入的人看到什麼沒驗 | 有查到,但網頁上的數字跟一開始記的不一樣 |
| Variety(核對時開到) | https://au.variety.com/2026/biz/news/sxsw-sydney-cancels-2026-edition-and-future-events-31939/ | 把前面打不開、或只有搜尋摘要的頁面再開一次,核對舊數字 | 前面查核時沒開到原頁 | SXSW Sydney 2026-01-14 公告取消 2026 那屆;NSW 政府說 2026、2027 都不辦 | 有查到 |

# 第二段:沒查到的

## (A) 網頁進不去(6 列)

| 名稱 | 網址 | 卡在哪 | 本來想拿它做什麼 |
|---|---|---|---|
| AER 電費原始 PDF(2026-27 草案資訊頁) | https://www.aer.gov.au/system/files/2026-03/Draft%20Default%20Market%20Offer%202026-27%20-%20Information%20sheet.pdf | 要登入(被轉到 AER 的登入頁) | 核對 Ausgrid、Endeavour、Essential 三區 2026-27 年電費(1,875、2,347、2,515 AUD)。最終版新聞稿開到了,但沒有 Ausgrid 年電費和用電量〔2026-11-17 更正:最終版 PDF 已下載並開檔核對,裡面有年電費與用電量(p.16)。Essential 平價 2,604、分時 2,530(4,600 kWh);這裡的 2,515 對不上最終版任何一種,不要再用〕 |
| SXSW Sydney 官網 | https://sxswsydney.com | 憑證壞掉 | 查活動日期和人數。後來從 Variety 報導知道 2026 那屆取消、NSW 政府說 2026、2027 都不辦〔2026-11-17 已核對:主辦方 2026-01-14 公告 2026 不辦(abea.org.au)〕 |
| Domain 2026 年 9 月季租金報告 | (筆記只記到 …/rental-report/september-2026-rental/,前段沒記全,不放)〔2026-11-17 已核對(Chrome 開原頁):獨棟 835、公寓 780、空置率 1.2%;網址 https://www.domain.com.au/research/rental-report/september-2026/ 沒有 -rental 後綴〕 | 找不到頁面(猜的網址和報告列表都 404) | 核對雪梨公寓、獨棟每週租金和空置率(公寓 780 目前只有 Elite Agent 轉述) |
| Tourism Research Australia 每月旅客頁 | https://www.tra.gov.au/en/regional/states-and-territories/new-south-wales | 找不到頁面(猜的網址 404;TRA Online 要登入) | 看雪梨或 NSW 各月旅客多寡,對照淡旺季 |
| HIA 與 Archicentre 裝修費用指南 | (筆記沒記網址) | 沒去查 | 拿協會的費用指南校「裝修、開辦費」的範圍 |
| AirDNA app 的每月數字 | https://app.airdna.co/data/au/30830/overview | 要付費方案(每月住滿幾成、每晚價、淡旺季、週末對平日、分房型、未來價格都被鎖,圖上是標 SAMPLE 的示範資料) | 看雪梨每個月的住滿率和每晚價,做淡旺季 |

## (B) 只看到搜尋摘要,沒開到原始網頁(13 列)

這些數字只是搜尋結果裡的摘要,沒有人開過原頁,不能當成查到的數字。

| 想查的數字 | 目前手上只有(摘要寫的數字) | 網址(有才放) |
|---|---|---|
| City of Sydney 市區登記的短租有幾間 | 5,454 間活躍短租,有 2,468 間依 NSW 制度登記(搜尋摘要引述市議會資料)〔2026-11-17 已核對(Chrome 開議會原文):2,468 是 NSW 政府 2023 年資料(有登記且活躍)、5,454 是獨立資料(活躍);議會 2025-02-17;只含 City of Sydney;不能寫成 2026 年現況〕 | (筆記沒記網址) |
| City of Sydney 市議會對短租的動議 | 2026-04-28 動議要求研究限制部分內城區「非主要居所」短租;是市議會行動,不是州法修改(來源是 wboc.com 新聞稿頁,品質低) | (筆記沒記網址) |
| Airbnb 舊制服務費(分攤費) | 房東約 3%、房客另付約 14.1%–16.5%(舊版頁面的搜尋摘要) | https://www.airbnb.com.au/resources/hosting-homes/a/simplifying-airbnb-service-fees-746 |
| 澳洲 Airbnb 改單一服務費的改制日(說法三) | 有網站寫 2025-12-01 全部轉換(搜尋摘要,只供參考)〔2026-11-17 已核對:Airbnb 官方服務費頁沒有寫任何統一改制日期;這句整句不用。官方頁寫分攤制多數房東 3%、房客 14.1%–16.5%,單一服務費多數房東 15.5%〕 | (筆記沒記網址) |
| NSW 土地稅超過一般門檻的稅率 | AUD 100 加超額部分的 1.6%(搜尋摘要引用 Revenue NSW 資料) | https://www.revenue.nsw.gov.au/news-media-releases/preparing-for-the-2026-land-tax-year |
| 2 個臥室 Airbnb 開辦合計 | AUD 7,539(Airbtics 的數字,資料期間 2023-10 至 2024-09;上一份筆記就有,這次沒再開頁) | https://airbtics.com/starting-an-airbnb-australia |
| NSW 家戶瓦斯年均 | AUD 730–1,320/年:Mozo 引 Finder 730;Finder 州別表每季 241(換算約 964);Energy Plans 1,320 | https://www.mozo.com.au/best/energy/gas.html 、https://www.finder.com.au/energy/gas-nsw 、https://www.energyplans.com.au/average-gas-bill-australia |
| NBN 50 方案月費 | AUD 50(Mozo 最便宜無限量)、約 86(Canstar 2026 全速率平均月帳單)、100(Canstar 區間上限) | https://www.canstar.com.au/internet/average-internet-bill/ 、https://www.mozo.com.au/broadband.html 、https://www.finder.com.au/news/optus-telstra-nbn-price-hikes-locked-in-for-july-2026 |
| NBN 100 方案月費 | AUD 70(Mozo 最便宜無限量)、110(Canstar 區間上限) | https://www.canstar.com.au/internet/average-internet-bill/ 、https://www.mozo.com.au/broadband.html 、https://www.finder.com.au/news/optus-telstra-nbn-price-hikes-locked-in-for-july-2026 |
| North Sydney 住宅市政費最低費率 | AUD 970.72/年(2026-27;2027-28 核准 1,116.32) | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Minimum-Rates-Instrument-2026-27-North-Sydney-Council.PDF |
| Blacktown 住宅最低費率與平均住宅費 | 最低費率 AUD 1,140、平均住宅費 1,233(每年;年度摘要沒寫清)〔2026-11-17:隊友查原始申請 PDF,A$1,140 屬 2025–26,不是 2026–27 的最終費用;1,233 是哪一年仍不清楚。這是隊友查的,我們沒核對;11/17 晚再查,申請 PDF 太大開不了、預算新聞頁沒有這兩個數字〕 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Blacktown-City-Council-Attachment-Other-Attachment-2.5-Special-Rate-Variation-FAQs-and-Factsheets.PDF |
| 房東 / 短租專用保險 | AUD 500–700/年(單一業者 Rakidzich 的文章) | https://www.rakidzich.com/articles/airbnb-insurance-australia |
| 新承作自住房貸平均利率 | 約 6.75%(升息前後的估計,不是投資客利率;沒標出處頁) | (筆記沒記網址) |

# 第三段:還缺哪些數據

前 8 列是我們自己資料的缺口;後面是外部行情還沒查到的。 **2026-11-17 更新**:隊友鹤舞給的清單裡 14 個檔已下載並開檔核對。下面這些缺口現在有檔案可以補(數字、頁碼、適用範圍在 `external_downloads_verify_2026-11-17.md` 表 2):電費最終版(229)、瓦斯(225;IPART 表的 Metro 分組,範圍檔案沒定義,不要寫成雪梨)、短租保險(223)、網路月費(204)、市政費(222,只有 North Sydney)、裝修(215、217)、建材價格指數(216)、家具套裝(219)、長租掛牌租金(226)。短租天數(210):現行規定有官方 FAQ(2024 年 5 月版:180 天、連續 21 天以上不計),但 2025–2026 修法結果仍未查到;現行政策頁(更新日 2025-02-10)仍寫 180 天,沒提 2025–2026 新規定。**還是缺的**:淡旺季(211)—— NSW 租金頁、TRA、Destination NSW 三個入口頁都沒有雪梨按月資料。

| 缺什麼 | 為什麼需要 | 現在怎麼處理 |
|---|---|---|
| 實際成交價 | 收入試算要用成交價;我們只有房東開的價,清潔費、折扣也看不到 | 外部行情給參考範圍(第 1 組);每晚價由使用者自己填 |
| 實際住了幾晚 | 算一年收入要知道住滿幾成;日曆的「不能訂」分不出是被訂走,還是房東自己關 | 外部行情給參考範圍(AirDNA 67%、AirROI 49.5%、Airbtics 75% 等);由使用者自己填 |
| 日曆沒有每天的價格 | 淡旺季要看哪天漲多少 | 延伸 2 只做提醒(假期、活動日期),不說漲多少 |
| 裝修費 | 開辦費、裝修費要有範圍 | 由使用者自己填;外部行情(第 3 組)只當參考範圍 |
| 成本(電、水、瓦斯、網路、管理費、保險) | 算每月淨收入要用 | 由使用者自己填;外部行情(第 4 組)只當參考範圍 |
| 看不出房東是自住還是投資 | 想分自住、二房東、買房三種人 | 不做(兩種人不在題目範圍);資料只看得出當房東多久 |
| 2025-12 那期沒有價格(整欄是空的) | 想多一期有價格的資料 | 價格只用 2026-03、06、09 三期 |
| 沒有 2025-09 那一期 | 想要滿一年的對照 | 免費最早從 2025-12-12 開始;更早的要向官方申請,參考價 US$500 或 US$800,還沒申請〔2026-11-17 已核對(官方申請頁,工具摘要,把握中):500 = 2 城且用途與站方使命相符(1 城商業也是 500);800 = 2 城商業用途;這是舊價表,新價 2026-11-01 起,2026-11-30 前送出的申請照舊價;不是固定報價,要向站方問〕 |
| 按房型(整套出租 / 只租一個房間)的價格與收入 | 同類比較和收入範圍要分整套出租、只租一個房間 | 外部只有 AirROI 按臥室數分組;整套/單間的開價用我們自己的房型欄算 |
| AirDNA 每月數字、供給子頁 | 做淡旺季每月住滿幾成 | 晚上補查:app 裡全部被鎖,要付費方案才看得到;不買,延伸 2 只做提醒 |
| NSW 2025–2026 修法結果 | 一年最多能租幾天會不會改 | 目前用官方頁寫的 180 天,並註明官方頁最後更新 2025-02-10;有沒有改要另外查 |
| Tourism Research Australia 每月旅客頁 | 看雪梨各月旅客多寡對照淡旺季 | 晚上補查:猜的網址 404,TRA Online 要登入;延伸 2 只做提醒 |
| 1 房 / 2 房整戶公寓油漆的來源價 | 裝修費的範圍 | 補查檔也沒有,只有各區油漆價(每平方公尺、每房)可加總;由使用者自己填 |
| 木地板翻新(磨砂上漆)價 | 裝修費的範圍 | 已補到層板、乙烯、工程木、實木的供應加安裝價,翻新沒有;由使用者自己填 |
| 浴室「整間每平方公尺」單價 | 裝修費的範圍 | 沒有可驗證的值;只用整間浴室價的範圍 |
| HIA、Archicentre、Cordell、Rawlinsons 的費用指南 | 官方或協會的裝修費用對照 | 晚上補查拿到 hipages(全澳平均)和 Master Builders NSW 第 1 頁;HIA、Archicentre 沒去查;由使用者自己填 |
| 雪梨層級的營造成本年增(ABS) | 判斷裝修費會不會變貴 | 晚上補到 Master Builders NSW:雪梨房屋營造材料 +2.0%(到 2025-09 止一年,只有材料);ABS 雪梨層級沒有〔2026-11-17 更正:ABS 有雪梨層級。Producer Price Indexes Table 18「Input to the House construction industry」,雪梨 2026 年 9 月季年增 3.7%(工作表 Data1 儲存格 Q251,已開檔核對)。這是房屋建築業的材料投入價格,不含人工,不能直接叫「裝修成本漲幅」〕 |
| 雪梨專屬的浴室、廚房費用指南(hipages 以外) | 裝修費的範圍 | 晚上補到 hipages 全澳平均:浴室 AUD 8,000–35,000、廚房 30,000–50,000;雪梨專屬的沒有 |
| 雪梨家具租賃(月租)實價 | 不買家具時的開辦費 | 查不到;由使用者自己填 |
| 澳洲業者 1 個臥室 / 2 個臥室家具套裝標價 | 開辦費裡的家具 | 只有 Airbtics 合計(1 個臥室 AUD 5,358、2 個臥室 7,539);由使用者自己填 |
| 澳洲裝修或設施升級對價格、住滿率影響的研究 | 告訴房東「缺哪些設施」值不值得補 | 沒找到(21% 是 Airbnb 自己的數字,因果不明);設施只列出同類有、自己沒有的,不寫補了能多賺多少 |
| 床單洗滌費 | 每月成本 | 查不到;由使用者自己填 |
| 雪梨一般公寓的年度市政費 | 每月成本 | 只有 North Sydney 最低費率、Blacktown 平均費,都沒有人開過原頁〔2026-11-17 已補到一部分:North Sydney 2026–27 最低住宅費率 970.72(IPART 最終報告 p.8,已開檔核對;只適用 North Sydney Council)。Blacktown 的 1,140 屬 2025–26(隊友查的,未核對;11/17 晚再查,申請 PDF 太大開不了、預算新聞頁沒有這兩個數字)〕;由使用者自己填 |
| 保險公司公布的房東 / 短租保險費率 | 每月成本的保險 | 只有單一業者的行銷文(AUD 500–700/年),沒有人開過原頁;由使用者自己填 |
| 投資客房貸利率 | 當時評估買房投資 | 查不到;買房投資不在題目範圍,不做 |
| 雪梨瓦斯年均帳單(AER 或政府來源) | 每月成本 | 只有比價站數字(AUD 730–1,320/年),沒有人開過原頁;由使用者自己填 |
| NSW 政府租金報告、SQM 的雪梨週租中位數、Cotality 的租金水準 | 當時評估二房東 | 沒查到;二房東不在題目範圍,只留紀錄 |
| Domain 租金報告、Cotality 或 Domain 房價頁的官方原頁 | 當時評估二房東、買房投資 | 晚上補查:Domain 2026 年 9 月季打不開(404),公寓 780 只剩 Elite Agent 轉述〔2026-11-17:公寓 780 已在 Domain 原頁確認(見第 169 行)〕;不在題目範圍,只留紀錄 |
| 有統計來源的雪梨公寓管理費 | 每月成本的管理費 | 晚上補到 Flat Chat 原帖(850/季,是 2024 年論壇估算);另有 Microburbs 854/季、Stratachecks 範圍,都沒有人開過原頁;由使用者自己填 |
| 2026-27 電費最終版與 AER 官方原件 | 每月成本的電費 | 晚上補查:PDF 被轉到登入頁;最終版新聞稿沒有 Ausgrid 年電費與用電量(可能在 information kit 或 final determination PDF,沒再開);目前用 Canstar 轉述,標「網路公開報價」,由使用者自己填〔2026-11-17 已補到:AER 最終決定 PDF 與資訊包已下載,數字見 `external_downloads_verify_2026-11-17.md` 表 2〕 |
| ATO 短租報稅重點的獨立查核 | 收入試算提醒要報稅 | 頁面開到(要申報短租收入),獨立查核打不開;只做提醒,不算稅 |
| 搜尋摘要來源那幾列的原頁 | 正式引用前要核對 | 沒開原頁;第二段 (B) 列了 13 列只看到搜尋摘要的項目 |

# 數量對照

- 五類不重複網站:我用 build_page.py 的同一套解析(沒有執行它,沒改任何檔)算出 48 個;它的 site_stats 算出 48 個;要求 48。一致。
  - 五類各自的網站數(重排前):短租市場 6、規定和平台費 8、裝修和佈置 13、每月成本 15、房市 10,加起來 52。
  - 加起來是 52 而不是 48:hometime.io 出現在 3 類、airbtics.com 與 houst.com 各出現在 2 類,各算一個網站,所以 52 − 2 − 1 − 1 = 48。
  - 這 48 個裡有 5 個是筆記沒記網址的來源(搜尋摘要、二手報導、研究檔自己算),有網址的網站是 43 個。mozo.com.au、finder.com.au、energyplans.com.au 在同一列的來源欄一起出現,分開算 3 個。
  - 第一段現在只列有開到網頁的,所以第 1–5 組是 43 列、39 個不重複網站,比 48 少 9 個。少的這些在第二段 (B):aer.gov.au、energyplans.com.au、finder.com.au、ipart.nsw.gov.au、mozo.com.au、二手報導(搜尋摘要,wboc.com 新聞稿頁,品質低)、搜尋摘要(houst.com / hostaway 類指南)、搜尋摘要(smartpropertyinvestment.com.au 等)、搜尋摘要沒標明出處頁;aer.gov.au 同時在第二段 (A)(網頁進不去)。
- 總表 190 列的查核結果(套用晚上補查的 8 列更新後):✅134 ⚠️34 ❌3 ⏸2 未查17;要求 ✅134 ⚠️34 ❌3 ⏸2 未查17。一致。更新前是 ✅130 ⚠️34 ❌1 ⏸8 未查17(晚上補查動到 8 列:6 列改變結果、2 列維持 ⏸)。
- 晚上補查 18 個:開到 13(hipages、The New Daily、OpenAgent、Flat Chat、Master Builders NSW、ATO、NRL、CoStar、Airbnb 新聞室、AirDNA 雪梨、澳洲國慶日官方站、Inside Airbnb、Entry Point)、要登入 1(AER)、被擋 1(SXSW Sydney)、找不到頁面 2(Domain 2026 年 9 月季報告、Tourism Research Australia)、沒去查 1(HIA 與 Archicentre)。13+1+1+2+1 = 18,一致。
  - 差在哪:Entry Point 原本記「要登入」,核對時開到頁面也看到價格,所以以核對為準算開到(原本記 12 個開到、2 個要登入)。
- 第一段各組列數:0 組 3、1 組 5、2 組 6、3 組 13、4 組 10、5 組 9、6 組 13、7 組 10、8 組 15,合計 84 列。第 8 組 15 列 = 13 個晚上開到的 + AirDNA app + Variety。第二段:(A) 6 列、(B) 13 列。第三段 32 列。
- 狀態的出處:第 6、7 組取自各自的核對檔(假期 37 列:✅34 ⚠️3;價格影響 43 列:✅33 ⚠️10);第 0 組的 Inside Airbnb 取自下載紀錄和晚上補查。
