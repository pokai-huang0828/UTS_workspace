# 查核:web_price_drivers_2026-11-14.md(影響雪梨價格的時間因素)

**總結:查了 43 列(35 列表格 + 檔尾 8 項),✅ 33、⚠️ 10、❌ 0、⏸ 0;另有 3 項「只看到搜尋摘要」的說法未查(筆記自己就標了不能當證據)。** 數字大致都對得上頁面,沒有出現把旅館寫成短租、把別城市寫成雪梨的錯誤;問題集中在「基準線寫太滿」「地區標示頁面沒寫」「年份」和「結論句把不同基準的數字併在一起」。

查核日 2026-11-14;scope ID:IS-1114-verify-07-pricedrivers。
方法:用 WebFetch 重開筆記裡的每個網址,頁面內容經 WebFetch 的小模型摘出(不是我逐字讀原頁),所以「頁面實際看到的」是摘出結果;凡我追問過第二次的項目(⚠️ 那幾列)都有再確認。沒有任何頁面打不開(0 個 ⏸),所以沒用 Chrome。

## 逐列判定

| # | 項目 | 筆記寫的 | 頁面實際看到的 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|---|
| 1 | 跨年夜(2015 搜尋) | 3% 房源 12/31 可訂;市區公寓含費 A$4,303 vs 平常 A$260;Woolloomooloo A$1,640 vs A$125;遊艇 A$29,684 | 發文日 2015-11-28;3% 可訂;A$4,303 含服務費與清潔費、平常 260;Woolloomooloo 1,640、平常 125;Rozelle 遊艇 29,684 | ✅ | 「16 倍」是含費總價對平常基本價,頁面本身就不是同一基準(筆記已提醒含費)。「作者自己搜尋」這句沒另外核對 | https://www.pedestrian.tv/news/sydney-airbnb-prices-surge-up-to-4300-per-night-over-new-year-period/ |
| 2 | 跨年夜(Hometime) | 說跨年夜 ADR 最高,無數字 | 「The highest rates are on New Year's Eve」,無金額 | ✅ | 頁面日期為 2026-07-08(見 #10) | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 3 | 跨年夜(STR Specialist) | 水景房約 3 倍(FAQ 2.5–3 倍);12–2 月 1.5–2 倍;聖誕跨年最少 3–5 晚;3–4 個月前調價;港邊熱門房約 10 月被訂光 | 「up to 3x or more」、FAQ 2.5–3x;12–2 月 1.5–2x;最少 3–5 晚;提前 3–4 個月;「prime listings near the harbor book out by October」;更新日 2026-04-29;無任何引用來源;推薦 Beyond Pricing(附導購連結) | ✅ | 全是建議值。「聖誕沒有單獨倍數」也對 | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 4 | 12 月 +25%、夏季 +15%(AirDNA) | 12 月價格比「全年各月平均」高 25%;夏季比其餘月份平均高 15% | 雪梨;資料 2018-09 起一年;圖表來源 AirDNA(Airbnb 與 HomeAway 整租房源);發文 2019-12-01。夏季 15% 的基準是「其餘月份平均」(吻合)。12 月 25% 頁面只寫「nightly rates in December were 25% higher」,沒寫跟什麼比 | ⚠️ | 15% 吻合。25% 的基準頁面沒明說(句型看起來跟 15% 同一基準=「其餘月份」,但那是推論);筆記寫成「比全年各月平均」,多寫了。文章另標 MadeComfy(短租管理公司)為資料來源 | https://www.yourinvestmentpropertymag.com.au/market-analysis/signs-point-to-bumper-peak-season-for-sydneys-shortterm-rental-hosts-this-summer |
| 5 | Taylor Swift 旅館 | 2024-02 雪梨旅館入住率 86.5%(+5.9%)、ADR A$329.05(+16.4%)、RevPAR A$284.47(+23.2%);2/24 高點 A$527.52;全月最高入住 2/20 93.6%;4 場 2/23–26;轉載日 2024-03-12 | 全部相同:86.5%/+5.9%、329.05/+16.4%、284.47/+23.2%、527.52(週六 2/24)、93.6%(週二 2/20,不在演唱會日)、四場 2/23–26、2024-03-12;CoStar 旅館資料、初步數據 | ✅ | 另:頁面標題「driven by」,內文也用 boosted/pushed 歸因給巡迴,但沒有做排除其他因素的分析(筆記「有關聯不等於單獨造成」的提醒合理)。演唱會期間入住率高點 92.9%(第二天) | https://www.hospitalitynet.org/news/4120883/record-high-room-rates-in-melbourne-sydney-driven-by-the-eras-tour |
| 6 | Taylor Swift 短租(Lighthouse) | 短租標價比下一個週末高 30%;旅館 91%(前一週)/87%(下一週末);雪梨+墨爾本旅館房量剩約 10%;短租訂房率落後、雪梨 15% | 原文大意:短租「advertised prices」在東京 +6%、墨爾本 +60%、**雪梨 +30%**(對比下一個週末);旅館 91%(對前一週,重點摘要)、87%(對下一週末,內文);雪梨+墨爾本合計房量剩約 10%(截至 2/8);短租入住率「明顯落後」,雪梨 15% 是相對旅館的落差、不是絕對入住率;發文 2024-02-15 | ✅ | **這列講的是短租、是雪梨**(不是旅館、不是墨爾本),30% 吻合。注意:同一段墨爾本是 +60%,比雪梨高;15% 是「落後旅館的幅度」(筆記說單位不明,方向對);標價非成交價 | https://mylighthouse.com/resources/blog/taylor-swifts-eras-tour-hotel-room-rates-asia-pacific-leg |
| 7 | WorldPride + Mardi Gras 2023 | 17 天:入住率比 2019 同期低 2.3%、ADR 高 25.7%、RevPAR 高 22.1%、多 A$43 百萬;3/4 95.8%、2/25 遊行日 95.4%、高點 A$414;3 天低於 80% | 全部相同(+25.7%、−2.3%、+22.1%、A$43M、95.8%、95.4%、A$414 在 2/25、3 天);旅館、STR 初步數據;轉載日 2023-03-15 | ✅ | 頁面期間寫 17 天,但內文有一句引言寫「兩週」,頁面自己不一致(不影響數字) | https://www.hospitalitynet.org/news/4115445/sydney-worldpride-2023-pushed-hotel-performance-to-pre-pandemic-levels |
| 8 | Vivid 2026 年 6 月 | 6 月旅館入住率 74.1%(+1.1%),為 2019 年 6 月以來最高;最高 92.7%(6/6,國王生日長週末);同月還有演唱會與電影節;217 活動、約 4 萬張 Vivid LIVE 票;2026-07-14 | 2026 年 6 月,74.1%,「+1.1 per cent year-on-year」,「highest occupancy since June 2019」,6/6 週六 92.7%(國王生日長週末),CoStar 初步數據,無 ADR;同月提到的活動:Vivid、Al Shami Live in Sydney、雪梨電影節、長週末;217 活動、近 4 萬張;並說 6 月是雪梨「歷來最淡的月份」之一 | ⚠️ | 數字都吻合。差在:筆記寫「演唱會」,頁面只寫「Al Shami Live in Sydney」,沒說是演唱會(只能說「還有別的活動」);頁面歸功於 Vivid + 電影節 + Al Shami,不是 Vivid 單獨;+1.1 頁面寫 per cent(筆記沿用 %,OK) | https://www.destinationnsw.com.au/newsroom/vivid-sydney-drives-hotel-occupancy-surge |
| 9 | Vivid「1.3 倍需求」 | 是需求不是房價倍數;港邊;無來源 | 「can spike demand 1.3x」於 The Rocks、Circular Quay;未註明來源;同頁把 6 月列為低季 | ✅ | 吻合,筆記的限制寫得對 | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 10 | 活動泛稱(Hometime) | 只說 spike 無量化;SCG 演唱會上限每年 4 場增至 20 場;「2025 年文章」 | 活動沒有出席或營收數字;SCG 場域上限「從 4 場升到 20 場/年」;**頁面日期 2026-07-08**,圖表為 FY24-25,訪客數到 2025-03 | ⚠️ | 內容吻合;年份標錯(筆記寫 2025 年文章,頁面是 2026-07-08)。#30 同樣問題 | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 11 | 學校假期、大型賽事(PriceLabs) | 學校假期/大賽可在 2–4 週前引發訂房高峰;全國層級,無金額 | 「2–4 weeks out」,沒有佐證數據 | ✅ | 吻合 | https://hello.pricelabs.co/australia-airbnb-market-trends/?amp=1 |
| 12 | 季節(PriceLabs 2024) | 全澳:7 月 59.4%、8 月 56.8%、9 月 61.1%、10 月 62.4%、11 月 63.8%;ADR 7 月 US$170、8 月 162.8、9 月 170.4、10 月 182.7(最高)、11 月約 180;只有 7–11 月;雪梨 ADR A$258、78%(引 Airbtics) | 月份數字全相同(2024);ADR 同(另附 AUD 值);10 月在「報告期間」最高;不含 12 月、5 月,6 月只出現在冬季定義;更新日 2026-10-16。但頁面**沒有明確標示這些月份數字是全國或哪個城市**(7、10 月出現在全國總覽,7–11 月逐月出現在「Regional Performance」標題下,無地理標籤);雪梨 A$258/78% 在 FAQ 沒寫來源,只有 Airbtics 的圖表圖片 | ⚠️ | 數字吻合。「澳洲(全國)」是筆記的推定(頁面有「Australian market」的免責語),不是頁面明說;「10 月房價最高」只限於 7–11 月這個窗口。雪梨那兩個數字,筆記寫「引 Airbtics」,頁面 FAQ 沒標來源,不可直接當 Airbtics 的數字 | https://hello.pricelabs.co/australia-airbnb-market-trends/?amp=1 |
| 13 | 季節倍數(STR Specialist) | 12–2 月 1.5–2;3–4 月與 9–11 月 1.2–1.4;5、8 月 1.0–1.1;6–7 月 0.8–0.9 | 相同(頁面以 Peak/High/Shoulder/Low 分季,沒有表格) | ✅ | 建議值,不是量到的 | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 14 | 季節(夏季對全年)(重複 #4) | 12 月比全年各月平均高 25%、夏季高 15%;約 2018–2019 | 同 #4 | ⚠️ | 同 #4:25% 的基準頁面沒寫 | 同 #4 |
| 15 | 季節無數字(Hometime) | 12–1 月價格高點 | 「peak around Christmas and New Year's, December–January」 | ✅ | 吻合 | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 16 | 學校假期與停留天數(PriceLabs) | 平均住 4–5 晚(冬)、5–6 晚(春) | 「4-5 nights in winter; 5-6 nights in spring」,在 2024-25 季節段;冬=6–8 月、春=9–11 月;無來源 | ✅ | 筆記標「澳洲(全國)」同 #12 的標示問題 | https://hello.pricelabs.co/australia-airbnb-market-trends/?amp=1 |
| 17 | 週末加價(STR Specialist) | 週五到週日 1.2–1.4 倍 | 「Friday–Sunday 1.2x–1.4x weekday base」(檢核表只寫 1.2x) | ✅ | 建議值 | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 18 | 週末定義(Airbnb) | 週末夜=週五、週六;週末價是基本價加百分比;無百分比 | 「Friday and Saturday nights」,週末價是基本價上的百分比加成;沒有數字 | ✅ | 吻合(兩頁都寫週五週六) | https://www.airbnb.com/resources/hosting-homes/a/understanding-pricing-on-airbnb-370 |
| 19 | 平日需求(PriceLabs) | 商務旅客與活動拉高平日入住率;無數字 | 「business travel and events lift weekday occupancy in Sydney and Melbourne」,無數字 | ✅ | 頁面其實點名雪梨和墨爾本(筆記標「都會區泛稱」,偏保守) | https://hello.pricelabs.co/australia-airbnb-market-trends/?amp=1 |
| 20 | 提前訂(PriceLabs) | 不少訂單落在入住前 14–30 天,疫情前常見 60 天以上 | 「within 14-30 days of arrival」,「60-plus pre-pandemic」 | ✅ | 吻合 | https://hello.pricelabs.co/australia-airbnb-market-trends/?amp=1 |
| 21 | 早鳥/最後一刻(Airbnb) | 早鳥 1–24 個月、最後一刻 1–28 天,百分比房東自訂 | 1–24 個月、1–28 天 | ✅ | 吻合 | https://www.airbnb.com/resources/hosting-homes/a/using-airbnb-pricing-tools-707 |
| 22 | 最少住幾晚(STR) | 聖誕跨年 3–5 晚 | 3–5 晚 | ✅ | 吻合 | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 23 | 長住折扣(Airbnb) | 每週折扣 7 晚以上、每月 28 晚以上;折扣 10% 以上有標示 | 7 晚、28 晚、「10% or more」有標示(僅限週/月折扣) | ✅ | 吻合 | https://www.airbnb.com/resources/hosting-homes/a/using-airbnb-pricing-tools-707 |
| 24 | 長住折扣(STR) | 週 10–20%、月 25–40% | 相同 | ✅ | 建議值 | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 25 | 新房源促銷(Airbnb) | 前 3 筆訂單折 20%;較低起始價可能幫助吸引首批房客與評價 | 20% off first 3 bookings(視資格才看得到);370 頁:低基本價可幫新房源吸引第一批房客與評價 | ✅ | 吻合 | https://www.airbnb.com/resources/hosting-homes/a/using-airbnb-pricing-tools-707 |
| 26 | 新房源(STR) | 比目標價低 20–30%,維持 2–4 週 | 20–30% 低於目標價 2–4 週,之後在至少 5 筆評價後逐步調高 | ✅ | 吻合(筆記沒寫「5 筆評價後調高」) | https://strspecialist.com/set-the-perfect-price-for-your-airbnb-in-sydney |
| 27 | 清潔費(Airbnb) | 清潔費等費用算入房客總價 | 「cleaning fees count toward total price guests pay」,無數字(頁面 2022-07-14 發、2025-07-14 更新) | ✅ | 吻合 | https://www.airbnb.com/resources/hosting-homes/a/understanding-pricing-on-airbnb-370 |
| 28 | 裝潢(Hometime) | 「裝潢好的房子可賺到相近房源的最多 2 倍」 | 「well-styled properties can earn up to 2x more than comparable」;頁面沒提「renovation」 | ✅ | 說的是 styled(佈置/風格),筆記標題「照片/裝潢」略寬;行銷說法,筆記已標 | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 29 | Hometime 入住率 | 自家 83% vs 市場 67%(FY24-25);「高 16%」是 16 個百分點 | 83% vs 67%,標「+16%」=16 個百分點(相對約高 24%) | ✅ | 吻合 | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 30 | 規定限制(Hometime) | 大雪梨非房東自住每年上限 180 晚;連續超過 21 晚不計入;「2025 年文章」 | 頁面:greater Sydney 等地非自住短租有上限,連續超過 21 晚豁免;頁面「180-day」與「180-night」兩種寫法並用;**日期 2026-07-08** | ⚠️ | 內容吻合;年份標錯(同 #10);頁面自己兩種用詞,引用前要對官方法規 | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 31 | 到訪人次(Hometime) | 國際 360 萬、國內 320 萬,截至 2025-03 | 3.6M 國際、3.2M 國內,year to March 2025 | ✅ | 吻合 | https://hometime.io/blog/how-events-sydney-boost-property-investments |
| 32 | Smart Pricing 名稱與因素 | 仍叫 Smart Pricing;「數百個」因素;房東設最低/最高價;頁面沒列季節、週末、活動為輸入因素 | 全部吻合(「hundreds of factors about your listing and your area」;未列季節/活動/週末為因素) | ✅ | 吻合 | https://www.airbnb.com/help/article/1168 |
| 33 | 週末價與 Smart Pricing | 用週末價必須先關 Smart Pricing;遇天災、緊急事件、政治動盪可能暫停 | 兩點都吻合(「temporarily turn off ... to prevent extreme price changes」) | ✅ | 吻合 | https://www.airbnb.com/help/article/1168 |
| 34 | 季節與活動(Airbnb 370) | 自訂價可針對日期/季節/活動;日曆上有價格建議;週末夜五六;三種價格 | 「3 types of prices: base, weekend, custom」;自訂價可覆蓋;price tips 針對不同日/季/特殊活動;無具體數字 | ✅ | 吻合 | https://www.airbnb.com/resources/hosting-homes/a/understanding-pricing-on-airbnb-370 |
| 35 | 價格建議(Airbnb 707) | 價格建議可用魔杖顯示/隱藏;用 Smart Pricing 看不到;該頁沒講季節與活動 | 用 Smart Pricing 的房東看不到價格建議(吻合);「魔杖」操作細節我沒單獨核對 | ✅ | 小細節(魔杖)未核對,不影響用途 | https://www.airbnb.com/resources/hosting-homes/a/using-airbnb-pricing-tools-707 |

## 檔尾「比較可靠的說法(a)」與結論句

| # | 項目 | 筆記寫的 | 實際 | 判定 | 說明 |
|---|---|---|---|---|---|
| a1 | Taylor Swift 旅館 | A$329.05(+16.4%)、86.5%(+5.9%)、2/24 高點 A$527.52;旅館 | 吻合(見 #5) | ✅ | 標了旅館、單一活動單一年份 |
| a2 | WorldPride 2023 | 房價比 2019 同期高 25.7%、入住率低 2.3%;遊行日 95.4%、高點 A$414 | 吻合(見 #7) | ✅ | 標了旅館、比對 2019 |
| a3 | Vivid 2026 6 月 | 74.1%(+1.1%)、6/6 高點 92.7%;限制:混有長週末、演唱會、電影節 | 數字吻合;「演唱會」頁面沒這樣寫(見 #8) | ⚠️ | 限制寫得對,只有「演唱會」該改成「其他活動(Al Shami Live)」 |
| a4 | 12 月 +25%、夏季 +15% | 雪梨短租 12 月比「全年各月平均」高 25% | 基準頁面沒寫(見 #4) | ⚠️ | 它被放在「來源比較可靠」那組,但是檔裡基準最模糊的一個;資料 2018–19 |
| a5 | PriceLabs 全國季節 | 「澳洲全國(非雪梨)」;10 月房價最高;窗口縮短到 14–30 天 | 數字吻合;但「全國」是推定,且「10 月最高」只在 7–11 月內比較(見 #12) | ⚠️ | 句子需補「7–11 月內」 |
| a6 | 短租標價比下一個週末高 30% | Lighthouse,2024-02,中低可信度 | 吻合,講的是雪梨短租標價(見 #6) | ✅ | 筆記自己把它放在「中低可信度」,合理 |
| a7 | Airbnb 工具設定 | 7 晚、28 晚、1–24 個月、1–28 天、前 3 筆 20%、週五六 | 全吻合 | ✅ | |
| 結論句 | 一句話參考 | 「大型活動(Taylor Swift、WorldPride)會把雪梨旅館房價推高約 16–26%」 | TS 的 +16.4% 是「2024 年 2 月整月 vs 2023 年 2 月整月」;WorldPride 的 +25.7% 是「17 天 vs 2019 同期」;兩個基準不同(年份、期間長度都不同);「推高」是因果語氣,兩篇新聞稿雖用 driven by / pushed,但都沒有排除其他因素 | ⚠️ | 把兩個不同基準的數字併成一個範圍、再寫成因果,簡報上不要用;各說各的才安全 |

## 未查項目(3)

- Airbnb 新聞室「Vivid 搜尋量約兩倍」、學術文獻方向不一致、2022/2024 Vivid 入住率:筆記自己標「只看到搜尋摘要」,沒有網址可重開,我也沒查(未查,3 項)。
- 筆記說 AirDNA seasonality、CoStar 原頁 403:我沒有重試。

## 簡報上可以直接用的說法

每條都標類型、年份、城市:

1. **旅館|2024 年 2 月|雪梨**:Taylor Swift 4 場期間,整個 2 月旅館入住率 86.5%(比去年同月高 5.9%)、平均房價 A$329(比去年同月高 16.4%);2/24 單日房價高點 A$527。來源:CoStar 初步數據(經 Hospitality Net,2024-03-12)。記得講「旅館」。
2. **旅館|2023 年 2 月底到 3 月初|雪梨**:WorldPride + Mardi Gras 17 天,旅館房價比 2019 同期高 25.7%、入住率低 2.3%;遊行日 2/25 入住率 95.4%。來源:STR/CoStar(2023-03-15)。
3. **旅館|2026 年 6 月|雪梨**:整個 6 月旅館入住率 74.1%(比去年高 1.1%),頁面說是 2019 年 6 月以來最高;單日高點 92.7% 在 6/6 國王生日長週末。來源:Destination NSW 引 CoStar 初步數據。可說「6 月有 Vivid、雪梨電影節等活動加上長週末」。
4. **短租(Airbnb 標價)|2024 年 2 月|雪梨**:Lighthouse 觀察到演唱會週末的短租標價比下一個週末高約 30%(同一份分析中,墨爾本 +60%)。只能講「標價」「單一廠商」。
5. **Airbnb 官方規則|現行|全球**:週末夜=週五、週六;週折扣 7 晚起、月折扣 28 晚起;用 Smart Pricing 就不能設週末價;Smart Pricing 依「數百個」因素調價,官方沒列出季節或活動為輸入因素。
6. **短租(AirDNA 資料)|約 2018–2019|雪梨**:夏季每晚價格比其餘月份平均高 15%(同篇說 12 月高 25%,見下)。

## 要加註或不要用的說法

1. **12 月 +25%**(短租,2018–19,雪梨,AirDNA 整租房源):頁面沒說比什麼;不要說「比全年各月平均高」,要用就說「12 月比平常高約 25%(2018–19 年資料,基準未明)」。
2. **PriceLabs 月份入住率與房價**(短租,2024 年 7–11 月,澳洲,非雪梨):頁面沒明標全國或城市;說「澳洲 2024 年 7–11 月」並註明「10 月是這 5 個月裡房價最高」;不能當雪梨數字,也不能說 12 月或 5–6 月。
3. **雪梨 ADR A$258、入住率 78%**(PriceLabs FAQ,短租,期間不明):FAQ 沒寫來源,不要說這是 Airbtics 的數字。
4. **「大型活動把雪梨旅館房價推高 16–26%」**:不要用。兩個數字基準不同(整月對去年同月 vs 17 天對 2019 同期),又是因果語氣。改成分開講:「Taylor Swift 那個月旅館房價比去年同月高 16%;WorldPride 那 17 天比 2019 年同期高 26%」。
5. **Vivid 當月數字**:不要寫成「Vivid 讓入住率變 74.1%」;改「Vivid 那個月入住率 74.1%,同月還有電影節與長週末」。不要說同月有「演唱會」。
6. **Taylor Swift 與 WorldPride 數字**:一律講「旅館」,不要說成 Airbnb 或短租;「有關聯」不要寫成「造成」(新聞稿標題雖寫 driven by,沒有排除其他因素)。
7. **STR Specialist 的倍數表(跨年約 3 倍、季節 0.8–2 倍、週末 1.2–1.4 倍、Vivid 需求 1.3 倍)**:廠商建議值,無來源且有導購連結;不要當證據,最多說「廠商建議」。
8. **跨年夜 2015 年 Pedestrian.TV 例子**(短租,2015,雪梨):挑選過的個別房源、含費用、已 11 年;不要說「跨年夜貴 16 倍」,最多說「舉例」。
9. **Hometime 的文章年份**:頁面日期是 2026-07-08(筆記寫 2025),180 晚上限、SCG 場次要引用前另找官方來源;「+16%」是 16 個百分點。
10. **Lighthouse 的「訂房率 15%」**:是短租落後旅館的幅度,不是絕對入住率;不要寫成「雪梨短租入住率 15%」。
