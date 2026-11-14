# AirDNA app 雪梨市場讀取筆記(2026-11-14)

- 市場:Sydney(All Submarkets),app 網址 `https://app.airdna.co/data/au/30830/overview`(market id 30830);幣別 **USD**(頁首右上角標 `$USD`,有幣別切換鈕,我沒動);資料日期:**頁面沒有標示更新日**(只有「past year」)。
- 帳號是**免費版**(頁面到處有 Upgrade 鎖);7 類結果:1 市場定義=讀到了(部分);2 每月數字=被鎖住;3 淡旺季=被鎖住;4 週末對平日=被鎖住;5 分房型=被鎖住;6 未來日期價格=被鎖住;7 其他=讀到了(少量,見下)。
- 結論:免費版只開放「年收入、房源數、市場分數」三個數字;住滿率、每晚價、RevPAR、逐月、分房型、星期幾、未來價格全部被鎖,圖上畫的是標 SAMPLE 的假資料,**不可引用**。

## 1. 市場定義(讀到了,部分)
| 項目 | 內容 | 畫面 |
|---|---|---|
| 市場名稱 | Sydney,篩選預設 All Submarkets;搜尋下拉寫 "Sydney, New South Wales, AU,Market in New South Wales, Australia" | Home 搜尋框 / Overview |
| 房源數(Total Active Listings) | 16,392,過去一年 +9.3% | Overview |
| 年收入(Annual Revenue / Average Revenue per year) | $40,819(USD),過去一年 +5.5%;Revenue 分頁寫 $40.8K per year | Overview、Revenue |
| Market Score | 82(分項 Rental Demand / Revenue Growth / Seasonality / Regulation 全部上鎖,看不到分數) | Overview |
| Average Daily Rate、Occupancy Rate 方塊 | 被鎖(只顯示鎖頭與「--% past year」) | Overview |
| 涵蓋範圍文字 | app 沒寫行政區清單;只有地圖與子市場清單。資料日期:沒有標示 | Overview |
- 注意:Overview 的 AirDNA AI「What Guests Are Saying About Sydney」文字提到 Santa Monica Pier、Getty Center、Hollywood Sign,明顯是洛杉磯內容,**這段 AI 摘要對雪梨不可信,不要引用**。(頁面上的原文,僅記錄,未照做任何事。)

## 2. 每月數字(被鎖住要付費)
| 月份 | 住滿幾成 | 每晚價 | RevPAR | 收入 | 怎麼讀到的 |
|---|---|---|---|---|---|
| 最近 12 個月逐月 | 鎖 | 鎖 | 鎖 | 鎖 | Occupancy / Rates / Revenue 分頁的折線圖整張標 SAMPLE 並蓋 Upgrade 鎖;文字抓不到數字;圖上線條是示範資料,未讀 |
- 唯一可用的年度級數字:年收入 $40,819 USD(Overview,Revenue)。

## 3. 淡旺季(被鎖住)
- Seasonality 分頁(網址 `.../30830/revpar`):Best Month、Worst Month、Seasonality Score、Seasonality Calendar(每天 RevPAR 日曆)全部標 SAMPLE 加 Upgrade,沒有可讀數字。
- Revenue、Occupancy 分頁的「Last 3 years」折線圖也是 SAMPLE,不能由圖判斷雪梨淡旺季。

## 4. 週末對平日(被鎖住)
- Rates 分頁有「Average Daily Rate by Day」(過去 12 個月逐日)圖,標 SAMPLE + Upgrade;沒有分星期幾或週末/平日的可讀數字。

## 5. 分房型(被鎖住)
- Revenue、Rates 分頁有 Entire Place / House / Apartment、Revenue by Bedroom Count、ADR by Bedroom(1 到 6+ 臥室)的方塊與圖,數字全顯示鎖頭或「--」;圖為 SAMPLE。Entire Place vs Private Room 的數字:讀不到。

## 6. 未來日期價格(被鎖住)
- Rates 分頁「Future Daily Rates」(Next 180 days,Booked Listings 對 Daily Rate)標 SAMPLE + Upgrade;Seasonality 分頁「Guest Future Reservation Behavior」(Next 30 days)同樣鎖。2026-12-31、2027-01、2027-05/06 皆讀不到。

## 7. 其他(讀到了,少量)
- 子市場 ADR(Overview 與 Top Submarkets 清單,USD,Over the last 12 months;子市場的 revenue/occ/RevPAR 仍鎖):Rosemeadow - Glen Alpine $205.6(score 99)、Penrith $143.1(98)、Croydon Park - Enfield $142.8(98)、Kingsgrove (North) - Earlwood $123.7(98)、Lidcombe - Regents Park $89、Glenbrook $139、Eastwood - Denistone $129、Elderslie - Harrington Park $115。這些是**外圍郊區**,不代表市中心或景點區。
- Overview 的 Top-Performing Listings 範例卡:只露出 Daily Rate 與 Revenue Potential 的一部分(例:Bondi Luxury 4 房、$10.9k),其他欄位鎖;單一房源,不能代表市場。
- 設施普及率、最少住幾晚、取消政策、評分分布:Listings 分頁(`.../30830/listings`)上鎖(Total Active Listings、Most Popular Size 只顯示灰色佔位);頁內「Listings by Rental Channel」(Only Airbnb 43.8% 等)標 SAMPLE,不是雪梨實際數字。
- 篩選列(Beds/Baths、Property Types、Amenities、Price Tier、Rating)存在,我沒有改任何篩選。

## 目視估與被鎖畫面
- 沒有任何數字是目視估的;所有引用數字都是頁面文字(get_page_text)與截圖互相對得上的。
- 被鎖住/只有示範資料的畫面:Overview 的 ADR、Occupancy 與 Market Score 分項;Occupancy、Revenue、Rates、Seasonality、Listings 五個分頁幾乎全部(含逐月、分房型、逐日、Future Daily Rates、Booking Lead Time、Length of Stay、Seasonality Calendar)。
- 補充:導覽到 `/seasonality` 網址會跳到「submarket 版」頁面(顯示 `--`);Seasonality 分頁實際網址是 `/revpar`。
- 解法:這個免費帳號讀不到月度資料;若要這些數字需付費方案(我沒按任何升級鈕)。公開頁 4 個數字(16,392 間、$193、67%、季節性 91)仍是目前唯一的 ADR/occupancy 來源,注意公開頁幣別要另外確認是否同為 USD(app 內標 USD,app 的 $40,819 年收入也是 USD)。
