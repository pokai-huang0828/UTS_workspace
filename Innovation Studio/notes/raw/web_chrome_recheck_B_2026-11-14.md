# Chrome 重查 B(8 站)— 2026-11-14

**結果統計:開到 6、要登入 0(AirDNA 每月細項在 app 內,未點開驗證)、被擋 1(SXSW Sydney 官網憑證錯誤)、找不到頁面 1(TRA,我猜的網址 404,未找到對的頁)。** 另有 B4 只開到 Airbnb 新聞室的 2025 年那一篇,2024 年那篇沒開。

方法:Claude in Chrome 自開一個新分頁(已關閉),未登入、未送表單、未下載。Google 搜尋用了 6 次(SXSW、NRL、CoStar×2、Airbnb 新聞室×2)。工具呼叫總數約 52 次(略超 50 上限,最後兩站是為了補齊)。

| 編號 | 網站 | 實際開到的網址 | 結果 | 我們原本要核對的話(來源) | 頁面上的數字、日期或原文(短) | 頁面日期 | 跟我們筆記比 |
|---|---|---|---|---|---|---|---|
| B1 | NRL 官網 | https://www.nrl.com/hospitality/grand-final/ ;https://travel.nrl.com/2027-grand-final ;nrl.com 首頁也開得到 | 開到了 | NRL Grand Final 2026 與 2027 日期(web_holidays_events:79,「被導到登入頁,沒查到」) | 2026:"Sunday 4th October 2026 at Accor Stadium, Sydney Olympic Park"(2026 NRL 與 NRLW 同日)。2027:官方旅遊頁寫 TBD、Sydney, Australia,日期未定;Google 摘要寫「暫定 2027 年 10 月」。2027 官方確定日期:看不到 | 頁面無標日期(頁尾 © 2026);2027 頁 2026 年底仍標「尚未開賣」 | 新資料(原本查不到) |
| B2 | SXSW Sydney | https://sxswsydney.com(憑證錯誤頁);https://www.sxswsydney.com 導到 https://sxsw.com/(Austin 母站首頁,無 Sydney 內容) | 被擋 | 2026 年活動日期(web_holidays_events:80,SSL 錯誤) | 官網讀不到。Google 摘要(Variety 2026-01-14、Man of Many 2026-08-26):SXSW Sydney 取消 2026 年那屆並「結束在雪梨的營運」;主辦 TEG 說 NSW 政府決定 2026、2027 都不資助 | 摘要日期 2026-01-14 / 2026-08-26(我沒開進文章全文) | 新資料(筆記以為只是打不開;實際是取消了) |
| B3a | CoStar 原頁(Eras Tour) | https://www.costar.com/products/str-benchmark/resources/press-releases/record-high-room-rates-melbourne-sydney-driven-eras | 開到了 | 2024 年 2 月雪梨旅館數字(web_price_drivers:32,hospitalitynet 轉載) | 雪梨 2024-02:入住率 86.5%(+5.9%)、ADR AUD329.05(+16.4%)、RevPAR AUD284.47(+23.2%);4 場演唱會 2/23–26,2/24 房價高點 AUD527.52;全月最高入住日 2/20 93.6%;4 天內最高 92.9%(第二天)。標「Preliminary」 | 2024-03-12 | 一樣(跟轉載逐項相同) |
| B3b | CoStar 原頁(WorldPride) | https://www.costar.com/article/789563613/str-sydney-worldpride-2023-pushed-hotel-performance-to-pre-pandemic-levels(Chrome 自動翻成中文;是 STR 稿經 Hotel News Now 刊登) | 開到了 | WorldPride + Mardi Gras 2023 17 天旅館表現(web_price_drivers:34) | 17 天;入住率比 2019 同期低 2.3%、ADR +25.7%、RevPAR +22.1%、房費收入多 A$43 百萬;3/4 95.8%、2/25 95.4%、2/25 房價高點 A$414;只有 3 天低於 80% | 頁面本身沒顯示日期(轉載為 2023-03-15) | 一樣 |
| B4 | Airbnb 新聞室 | https://news.airbnb.com/ (首頁,文字很少);https://news.airbnb.com/en-au/airbnb-proud-to-be-vivid-sydney-community-partner-once-again | 開到了(首頁內容薄;找到 Vivid 稿) | Vivid Sydney「搜尋量約兩倍、平均住 4 天」(web_price_drivers:125,頁面轉址後內容為空,日期不明) | 2025 年稿:雪梨燈光節期間搜尋預訂比 2024 年 +35% 以上;去年(2024)三週每位房東平均收入超過 1,600 美元(稿內寫 $,未標幣別);來源是 Airbnb 內部搜尋與房東調查 | 2025-05-22 | 不一樣(筆記說「約兩倍、4 天」,這篇是 +35%、沒看到「4 天」)。「約兩倍」可能在 2024-06-06 那篇「Airbnb data reveals surge in visitors flocking to Vivid Sydney」(Google 有列,我沒開到) |
| B5 | AirDNA 雪梨 | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 開到了(不登入只看到總覽) | 雪梨 STR 總覽數字(web_verify_str_market:13-18、49) | 活躍房源 16,392(截至 2026-10);年收入 $40.8K;入住率 67%;ADR $193;RevPAR $129;12 個月變化:營收 +99.1%、入住率 +7.9%、ADR -11.5%、RevPAR +3.3%、房源 -36.8%;季節性 91/100;Market Score 82。每月入住率、哪幾個月最旺、淡旺季月份:頁面只放按鈕「See in app / See peak & trough months」,數字不在頁上 | 頁面 Updated 2026-11-11 | 一樣(跟 web_verify_str_market 相同);每月數字看不到 |
| B6 | 澳洲國慶日 | https://www.australiaday.com.au/(官方活動站) | 開到了 | 2027 年雪梨 Australia Day 活動日期與內容(web_holidays_events:64、83,sydney.com 頁 404) | 全部寫 26 January 2027:Dawn Reflection 05:20–05:40(Circular Quay)、WugulOra Ceremony 07:30–08:30(Barangaroo Reserve)、Citizenship Ceremony 10:30、Harbourfest 10:30–16:00、Mega Kidz Zone 10:30–16:00、Midday Salute 11:55、Ferrython 12:10–12:30、Australia Day Live Concert 19:30–21:30(含煙火);頁面沒寫人數 | 頁面無標發布日期(標題 What's on in Sydney 2027) | 新資料(日期同 1/26;活動內容補上了) |
| B7 | Tourism Research Australia | https://www.tra.gov.au/en/regional/states-and-territories/new-south-wales(我猜的網址,404);網站本身開得到 | 找不到頁面 | 筆記沒有具體想查哪一句(web_str_market:123、meeting_1114_external_facts:395 只寫「沒查,工具次數上限」);依指示改找「雪梨/NSW 國內外過夜旅客哪幾個月最多」 | 404 頁。頁面導覽有「旅遊統計數據」「TRA Online」;TRA Online 要登入才有即時統計。沒找到月別旅客頁 | 無 | 看不到 |
| B8 | Inside Airbnb 雪梨 | https://insideairbnb.com/sydney/ | 開到了 | 我們算的 2026-09-16 那期 20,833 筆(任務說明) | 地圖頁底寫 data: September 16 2026;右側面板:Sydney 篩選 17,883,「out of 20,833 listings (85.8%)」;房型:整套 14,411(80.6%,是 17,883 的比例)、私人房 3,370(18.8%)、共用房 46(0.3%)、旅館房 56(0.3%);平均已訂 71 晚/12 個月、價格 $452/晚、平均收入 $26,367 | 2026-09-16 | 一樣(總數 20,833 吻合) |

## 不一樣或新資料的說明

- **B1 新資料**:2026 總決賽是 10/4(Accor Stadium),2027 總決賽官方還沒定日期(只知在雪梨、暫定 10 月)。簡報裡的總決賽只能寫「2027 日期未公布」。
- **B2 新資料**:SXSW Sydney 不是打不開而已,是主辦宣布不辦 2026 也不辦 2027(NSW 政府不再出錢)。這個活動不該再當作「2026/2027 雪梨九、十月的需求來源」;此判斷來自 Google 摘要,我沒開 Variety 全文,對外引用前建議再開一次原文。
- **B4 不一樣**:我開到的 Airbnb 稿(2025-05-22)寫搜尋量比 2024 年多 35% 以上,不是「約兩倍」,也沒有「平均住 4 天」。筆記那句很可能來自另一篇(2024-06-06,我沒開),在確認前不要拿「約兩倍」當事實。
- **B6 新資料**:國慶日官方站列出 2027 年 8 項活動與時段(煙火在晚上 7:30 的演唱會),日期都是 1/26,與筆記一致,只是多了內容。
- **B7 沒完成**:沒找到 TRA 的月別旅客頁,建議下次用 Google site:tra.gov.au 找(這次 Google 次數已用完)。
- **B5 看不到**:每月入住率、價格、最旺月份 AirDNA 首頁沒放數字(要進 app),不登入就拿不到。

其他:B3 兩份原頁與轉載數字完全相同;B8 面板數字是「Sydney 篩選後 17,883」,不要把它當成總數,總數是 20,833。
