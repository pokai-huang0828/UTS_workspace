# 雪梨短租(Airbnb)市場行情:外部參考筆記

查閱日 2026-11-14;外部參考值,不是我們資料算出來的。
scope ID:IS-1114-web-01-strmarket

注意事項:
- 外部數字是各家平台對「全部或部分房源」的估計,定義、期間、幣別都不同,不能跟我們 Inside Airbnb 2026-09 快照的「掛牌價中位數 AUD 338/晚」直接相減。
- 各表的「資料期間」「地理範圍」不同,不要混成一個數字。
- 「來源類型」:官方 / 產業報告 / 商業網站 / 部落格。商業網站(AirDNA、AirROI、Airbtics、GuestFavorites)是自家演算法估計,不是政府統計。
- 本檔所有數字都是這次 session 實際讀到的頁面內容;AirDNA 內頁(supply/seasonality 子頁)讀取失敗(403),所以 AirDNA 只有 overview 頁的數字。

## 表 1:價格、入住率、收入(題 1)

| 項目 | 數值 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 |
|---|---|---|---|---|---|---|
| 活躍房源數 | 16,392 間(去重後,含 Airbnb/Vrbo/Booking.com) | 截至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 |
| ADR(實際成交每晚均價) | $193/晚(頁面未標幣別) | 2025-10 至 2026-10 | Sydney | AirDNA | 同上 | 商業網站 |
| 入住率(平均) | 67% | 2025-10 至 2026-10 | Sydney | AirDNA | 同上 | 商業網站 |
| 每間年收入(平均,典型活躍房源;頁面未標幣別) | $40.8K/年 | 2025-10 至 2026-10 | Sydney | AirDNA | 同上 | 商業網站 |
| RevPAR | $129/晚可供出租 | 2025-10 至 2026-10 | Sydney | AirDNA | 同上 | 商業網站 |
| 年變化(10/2025→10/2026) | ADR -11.5%、入住率 +7.9%、RevPAR +3.3%、活躍房源 -36.8%;頁面另寫營收 +99.1%(與 RevPAR +3.3% 難以並存,可能是定義或樣本變動,不採用) | 2025-10 至 2026-10 | Sydney | AirDNA | 同上 | 商業網站 |
| 活躍房源數 | 10,096 間 | 2025-11 至 2026-10(近 12 個月) | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 |
| ADR(每個已訂晚) | AUD 399/晚 | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 入住率(佔開放天數) | 49.5% | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 每間年收入(平均) | AUD 52,495/年(年增 12.0%) | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 每間每月收入(中位數) | 約 AUD 4,710/月 | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 年收入中位數:Studio / 1房 | AUD 40,500 / 44,100 | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 年收入中位數:2房 / 3房 | AUD 54,000 / 54,500 | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 年收入中位數:4房 / 5房以上 | AUD 63,500 / 78,900 | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 年收入平均:Studio / 1 / 2 / 3 / 4 / 5+ 房 | AUD 42,400 / 46,800 / 60,700 / 67,900 / 83,100 / 104,000 | 2025-11 至 2026-10 | Sydney | AirROI | 同上 | 商業網站 |
| 活躍房源數 | 13,051 間 | 2025-11 至 2026-10 | Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 |
| ADR | AUD 336/晚 | 2025-11 至 2026-10 | Sydney | GuestFavorites | 同上 | 商業網站 |
| 入住率 | 68% | 2025-11 至 2026-10 | Sydney | GuestFavorites | 同上 | 商業網站 |
| 每間年收入(平均) | AUD 83,094/年 | 2025-11 至 2026-10 | Sydney | GuestFavorites | 同上 | 商業網站 |
| 追蹤房源數(僅納入較高評分房源,非全市場) | 13,174 間 | 2025-09 至 2026-09 | Sydney | Airbtics | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ | 商業網站 |
| 入住率(中位數) | 75% | 2025-09 至 2026-09 | Sydney | Airbtics | 同上 | 商業網站 |
| ADR(中位數) | AUD 281/晚 | 2025-09 至 2026-09 | Sydney | Airbtics | 同上 | 商業網站 |
| 每間年收入(中位數) | AUD 79,355/年 | 2025-09 至 2026-09 | Sydney | Airbtics | 同上 | 商業網站 |
| 入住率 / ADR / 年收入(2025 全年) | 78.0% / AUD 258/晚 / AUD 75,205/年(2024 為 69,160,+8.74%) | 2025 日曆年 | Sydney | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 |
| 入住率 / ADR / 每間年收入(全澳 2025) | 62.2% / AUD 317/晚 / AUD 71,770/年 | 2025 日曆年 | 全澳(46 個市場) | Airbtics | 同上 | 產業報告 |
| 入住率(市場平均) | 67% | 財年 2024-25(約 2024-07 至 2025-06) | Sydney | Hometime(自家管理資料與圖表) | https://www.hometime.io/blog/market-report-short-term-rental-sydney | 部落格 |
| 典型每間年收入範圍 | AUD 50,800–97,700/年(來源與期間文中未標) | 約 2025–2026(文章 2026-07-08,期間未標) | Sydney | Hometime | 同上 | 部落格 |

表 1 不一致處(兩個都列、不取平均):
- ADR:AirDNA 193(未標幣別,可能是美元;AirROI 自述由 USD 以 1.44 換成 AUD,AirDNA 若同為美元約等於 AUD 278,與 Airbtics 281 接近,但這是我的推算,頁面未證實)、Airbtics 281、GuestFavorites 336、AirROI 399。差在定義與樣本(全部房源 vs. 高評分房源、中位數 vs. 平均、已訂晚 vs. 掛牌價、幣別),不是同一把尺。
- 入住率:AirROI 49.5% 用「開放天數」當分母,AirDNA 67%、GuestFavorites 68% 用「可訂天數」,Airbtics 75% 是高評分房源中位數;分母定義不同。
- 年收入:AirDNA 40.8K(未標幣別)與 GuestFavorites 83K、Airbtics 79K 差一倍,原因多半是樣本(全部活躍房源含很少出租的 vs. 篩過的房源)與平均 vs. 中位數;AirROI 52.5K 在中間。這個落差是這次最大的不確定點,不要只拿其中一個當事實。
- 我們自己的 338/晚是「掛牌價」,通常高於「已訂晚的成交均價」,對照時請用 GuestFavorites 336 / AirROI 399 這類較高的一組,而不是 AirDNA 193。

## 表 2:淡旺季(題 2)

| 項目 | 數值 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 |
|---|---|---|---|---|---|---|
| 最旺月份(每間月收入) | 12 月,兩年日曆月平均約 AUD 7,300/月;近 12 個月 2025-12 為 AUD 7,638 | 約 2024-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 |
| 最淡月份(每間月收入) | 6 月,兩年日曆月平均約 AUD 4,490/月;近 12 個月 2026-06 為 AUD 4,690 | 同上 | Sydney | AirROI | 同上 | 商業網站 |
| 旺淡差(由上面兩個數字算出,非來源直接給) | 12 月約為 6 月的 1.6 倍(7,300 / 4,490) | 同上 | Sydney | AirROI(本檔計算) | 同上 | 商業網站 |
| 入住率高峰 / 平季 / 低點月份 | 高峰 11 月、2 月;平季 12 月、1 月;低點 5 月、6 月(只有標籤,沒有各月數字) | 2025-11 至 2026-10 | Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 |
| 季節性分數 | 91/100(100 = 月間營收落差小);頁面未列各月數字 | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 |
| 價格高峰 | 12 月至 1 月(聖誕到跨年,跨年夜最高);最淡 5–6 月 | 財年 2024-25 | Sydney | Hometime | https://www.hometime.io/blog/market-report-short-term-rental-sydney | 部落格 |

表 2 一致處與差異:三個來源都說 5–6 月最淡;旺季 AirROI/Hometime 說 12 月(1 月),GuestFavorites 的入住率高峰標成 11 月與 2 月、12–1 月反而只算平季。差在 GuestFavorites 看的是「入住率」、AirROI 看的是「收入」(含價格),12–1 月價格高但入住率不是最高,兩者不矛盾。AirDNA 的季節性分數 91 也表示整體月間落差不大。

## 表 3:NSW 短租法規(題 3;以官方頁為準)

| 項目 | 數值 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 |
|---|---|---|---|---|---|---|
| 非房東同住(non-hosted)上限 | 每年 180 天(頁面用「days」不是 nights);從初次登記日起算每 12 個月;單筆連續 21 天以上的訂單不計入上限 | 官方頁最後更新 2025-02-10 | Greater Sydney(Eastern Harbour / Central River / Western Parkland 三個城市區) | NSW Department of Planning, Housing and Infrastructure | https://www.planning.nsw.gov.au/STRA | 官方 |
| 房東同住(hosted) | 不限天數(全年 365 天可出租) | 2021-04 公告,2021-11-01 生效 | NSW 適用地區 | NSW Planning(新聞稿) | https://www.planning.nsw.gov.au/news/short-term-rental-accommodation-framework-finalised | 官方 |
| 登記費 | 新登記 AUD 65;每年續約 AUD 25;皆不退費 | 官方頁最後更新 2025-02-10 | NSW | NSW Planning | https://www.planning.nsw.gov.au/STRA | 官方 |
| 登記制度 | 政府營運的強制登記(register)與排除名單(exclusion register)、最低防火安全標準、強制行為準則 | 2021-11-01 起 | NSW | NSW Planning(新聞稿) | https://www.planning.nsw.gov.au/news/short-term-rental-accommodation-framework-finalised | 官方 |
| 2024 檢討 | 2024-02-15 至 03-14 公開討論文件,430+ 份意見、2,400+ 份問卷;非房東天數上限「列為政策檢討中」,官方頁未列結果 | 2024 | NSW | NSW Planning | https://www.planning.nsw.gov.au/STRA | 官方 |
| Byron Shire 另訂 60 天上限(不適用 Greater Sydney) | 2024-09-23 起 | 2024-09 | Byron Shire | NSW Planning | https://www.planning.nsw.gov.au/STRA | 官方 |
| City of Sydney 市議會動議 | 2026-04-28 動議要求研究限制部分內城區「非主要居所」短租;是市議會行動,不是州法修改(只有二手報導,我沒讀到議會原文) | 2026-04 | City of Sydney | 二手報導(來自搜尋摘要,網址見搜尋結果:wboc.com 新聞稿頁,品質低) | 未直接讀取 | 部落格 |

表 3 說明:官方頁在 2025-02-10 後沒有更新,所以我查到的官方資料是「Greater Sydney 仍是 180 天、AUD 65/25」,沒有找到官方公布的 2025–2026 修法結果。有些二手文章猜測上限可能降到 90 天,那是猜測,不是決定;使用前請在 planning.nsw.gov.au 再確認一次。

## 表 4:Airbnb 對房東的平台抽成(題 4)

| 項目 | 數值 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 |
|---|---|---|---|---|---|---|
| 單一房東服務費(host-only fee) | 15.5%,房客不再另付服務費(依 Airbnb 頁面,15.5% 為全球平均) | 頁面 2026-07-29 發布、2026-10-13 更新 | Airbnb 澳洲站(頁面未寫澳洲專屬生效日) | Airbnb 官方資源頁 | https://www.airbnb.com.au/resources/hosting-homes/a/simplifying-airbnb-service-fees-746 | 官方(平台自述) |
| 舊制(分攤費) | 房東約 3%、房客另付約 14.1%–16.5% | 2025 以前(搜尋摘要引述 Airbnb 澳洲頁舊版) | 澳洲 | Airbnb 澳洲頁(舊版,經搜尋摘要) | 同上 | 官方(平台自述) |
| 澳洲改制日(說法一) | 透過 PMS(物業管理軟體)連線的房東 2025-10-27 轉為單一 15.5%(由 15% 調為 15.5%) | 2025-10 | 澳洲 | Hometime | https://www.hometime.io/blog/what-airbnb-host-only-fee-means-for-you | 部落格 |
| 澳洲改制日(說法二) | 自行管理、仍在舊制的房東 2026-09-15 起全部轉為單一費用,多數為訂單小計的 15.5% | 2026-09(文章 2026-09-08) | 澳洲 | Hometime | 同上 | 部落格 |
| 澳洲改制日(說法三) | 搜尋摘要有網站寫 2025-12-01 全部轉換;沒有直接讀到原文,只供參考 | 2025-12 | 澳洲 | 搜尋摘要(houst.com / hostaway 類指南) | 未直接讀取 | 部落格 |

表 4 不一致處:改制日期各家說法不同(2025-10-27 / 2025-12-01 / 2026-09-15 / Airbnb 頁的 10-13),原因是「PMS 連線房東」與「自行管理房東」分批轉換。Airbnb 自己的頁面只確認最終是 15.5% 單一費用。建議模型直接用 15.5%(對自行管理的新房東),不用再算 3% 舊制。

## 表 5:供給趨勢(題 5)

| 項目 | 數值 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 |
|---|---|---|---|---|---|---|
| 活躍房源數年變化 | -36.8%(2025-10 → 2026-10;AirDNA 另一次搜尋摘要寫 -42.0%,期間 2025-09 → 2026-09) | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 |
| 活躍房源數年變化 | -22% | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 |
| 活躍房源數年變化(較小區域:Sydney、Bondi Beach、Manly、Parramatta 合計) | -10%,8,379 間 | 2026-05 對前一年 | 雪梨部分區域 | BnbCalc(搜尋摘要,沒讀原頁) | https://www.bnbcalc.com/markets/au/sydney | 商業網站 |
| 供給年增(2025 全年) | +28.88%(多出 2,851 間) | 2025 日曆年 | Sydney | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 |
| City of Sydney 市區登記狀況 | 5,454 間活躍短租,其中 2,468 間有依 NSW 制度登記(搜尋摘要引述市議會資料,沒讀原文) | 約 2025–2026 | City of Sydney(只有市區) | 搜尋摘要(smartpropertyinvestment.com.au 等) | 未直接讀取 | 部落格 |
| 全澳供給年增 | +13.79% | 2025 日曆年 | 全澳 | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 |

表 5 不一致處:2025 日曆年 Airbtics 說雪梨供給增加 28.88%,2025-10 至 2026-10 AirDNA/AirROI 說減少 22%–37%,兩邊期間不同(前者到 2025 年底,後者是 2026 年一整年);方向也可能反映平台對「活躍」定義與去重方式不同(AirDNA 去重跨平台,Airbtics 沒說明)。能確定的只有:各家商業來源對 2026 年的方向一致是「減少」,幅度 10%–37% 不等。我們自己的 Inside Airbnb 2026-09 快照有 20,833 間,比 AirDNA 活躍數 16,392 與 AirROI 10,096 都多——因為 Inside Airbnb 是掛牌快照,含不活躍房源;對照時要用同一尺。

## 可以當低/中/高情境的建議值(外部參考值,給方案 B 的情境假設用)

重要:三組值全部是「外部商業網站估計」,不是我們資料算出來的,也不是政府統計;使用前要在試算工具的假設欄標示來源。

| 情境 | 入住率 | 入住率取自 | 每晚價格(ADR) | 每晚價格取自 |
|---|---|---|---|---|
| 低 | 50% | AirROI 49.5%(2025-11 至 2026-10,Sydney) | AUD 280 | Airbtics 中位數 281(2025-09 至 2026-09,Sydney) |
| 中 | 67% | AirDNA 67%(2025-10 至 2026-10);GuestFavorites 68% 也接近 | AUD 336 | GuestFavorites 336(2025-11 至 2026-10);也與我們掛牌價中位數 338 接近 |
| 高 | 75% | Airbtics 中位數 75%(僅含高評分房源,2025-09 至 2026-09) | AUD 399 | AirROI 399(2025-11 至 2026-10) |

使用提醒:
- 三組入住率用的分母不同(見表 1 下說明);情境之間的差距主要是「定義差」,不是同一個市場在不同狀況下的差。要做真正的低/中/高,建議低情境再套用 180 天上限(只有非房東同住房源適用):180 / 365 = 49.3% 最高入住率,和 AirROI 49.5% 巧合接近,但意義不同。
- 年收入若要交叉檢查:低 ≈ 280 × 50% × 365 ≈ AUD 51,100(與 AirROI 平均年收入 52,495 接近);中 ≈ 336 × 67% × 365 ≈ AUD 82,200(與 GuestFavorites 83,094 接近);高 ≈ 399 × 75% × 365 ≈ AUD 109,200(高於所有來源的年收入,屬上界,偏樂觀)。這些是本檔用上面數字乘出來的,不是來源直接給的。
- 這些年收入都是營收,未扣平台費 15.5%、清潔費、管理費、水電、稅;方案 B 讓使用者自己填成本。
- AirDNA 的 ADR 193 與年收入 40.8K 沒有被列進三個情境,因為頁面沒標幣別,也無法確認可否與 AUD 直接比較;若組員要用,請先確認幣別。

## 沒涵蓋或證據弱的部分

- 按「房型」(整套房 / 單間)的價格與收入:查不到。只有 AirROI 的臥房數分組。
- AirDNA 的季節性各月數字、供給子頁:頁面讀取失敗,只拿到 overview。
- NSW 2025–2026 修法結果:官方頁沒有列,查不到官方公布的改動。
- Tourism Research Australia 與 Inside Airbnb 摘要頁:這次沒查(工具呼叫上限)。
