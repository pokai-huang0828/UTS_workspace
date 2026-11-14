# 11/14 組會:外部行情總表(5 份研究檔 + 4 份查核檔合併)

整理日 2026-11-14;scope ID:IS-1114-consolidate-01。外部參考值,不是我們資料算出來的。整理員只做照表合併,沒有上網、沒有重算、沒有補數字。

## 怎麼讀這份表

- 9 個來源檔都在 `Innovation Studio/notes/raw/`,檔名都以 `_2026-11-14.md` 結尾;下面「出處」欄只寫去掉日期和副檔名的檔名,格式是「研究檔檔名:行號;查核檔檔名:行號」。例:`web_str_market:16` = `web_str_market_2026-11-14.md` 第 16 行。
- 查核判定:✅ 吻合;⚠️ 有差異(差異寫在加註);❌ 查核員在頁面看不到或與頁面不符;⏸ 頁面打不開、沒驗到;未查 = 查核員沒開;查核檔沒涵蓋 = 查核檔沒有這一列。本版沒有任何一列落在「查核檔沒涵蓋」。
- 合併規則:研究檔與查核檔不同時以查核檔為準,數值欄填查核員在頁面看到的值,加註寫「查核更正:原寫 X」;❌ 且查核員沒找到數字的列不放主表、放第 7 段;⚠️ 的加註寫出查核員指出的差異;⏸/未查的加註寫「未經獨立查核」加原因;原檔與補查檔都有的項目兩列都放、不合成;數字逐字照抄。
- 「—」= 來源沒給這一格。「(補)」= 補查檔的列;「(原)」= 原檔的列(營運成本兩份檔的列編號 W1、G1、N1、R1、I1、P3、P4、L2、T4、B3 重複,以補查檔為準並寫明檔名)。
- 欄位:項目|低|中或單一值|高|單位|資料期間|地理範圍|來源名稱|網址|來源類型|查核判定|簡報加註|出處。研究檔寫「同上」的網址已還原成完整網址。
- 所有商業網站數字都是自家演算法或報價導流網站的估計,不是官方統計;要放進簡報請標「網路公開報價/估計」。

## 0. 查核統計

| 查核檔 | 查了幾列 | ✅ | ⚠️ | ❌ | ⏸ | 未查 | 檔頭原句 | 出處 |
|---|---|---|---|---|---|---|---|---|
| 市場(web_verify_str_market) | 57 | 37 | 15 | 1 | 0 | 4 | 「共查 57 列:✅ 37、⚠️ 15、❌ 1、⏸ 0、未查 4」 | web_verify_str_market:3 |
| 裝修(web_verify_reno_setup) | 50 | 43 | 4 | 0 | 3 | 0 | 「重新打開網址查了 50 列:✅ 43、⚠️ 4、❌ 0、⏸ 3、未查 0」 | web_verify_reno_setup:5;67 |
| 裝修補查(web_verify_reno_gapfill) | 41 | 35 | 3 | 1 | 0 | 2 | 「共查 41 列(35 ✅、3 ⚠️、1 ❌、0 ⏸、2 未查)」 | web_verify_reno_gapfill:3 |
| 營運成本與房市(web_verify_opcost_housing) | 56 | 24 | 14 | 1 | 5 | 12 | 「查了 56 列,✅ 24、⚠️ 14、❌ 1、⏸ 5、未查 12」 | web_verify_opcost_housing:5 |
| 合計 | 204 | 139 | 36 | 3 | 8 | 18 | 逐欄相加 | 同上四檔 |

與你手上的數字比對:四個查核檔檔頭與你給的 57(37/15/1/0/4)、50(43/4/0/3/0)、41(35/3/1/0/2)、56(24/14/1/5/12)、合計 204(139/36/3/8/18)完全一樣,檔頭每一檔的五項相加也等於各檔的總列數。

唯一對不上的地方:裝修補查檔(web_verify_reno_gapfill)檔頭寫 41 列、✅ 35,但該檔逐列判定表我數出 42 列、✅ 36(油漆 13 + 地板 12 + ABS 4 + Hometime 5 + 智慧鎖 3 + 加總驗算 5;其中 ✅ 為油漆 13、地板 12、ABS 1、Hometime 3、智慧鎖 2、加總 5)。⚠️ 3、❌ 1、未查 2 兩邊一致。依規則以檔頭為準,上表用 41/35;差 1 列是檔頭與逐列表的落差,我沒有判斷是哪一列。

## 1. 短租市場(每晚價格、入住率、每間年收入、淡旺季、供給)

| 項目 | 低 | 中或單一值 | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 查核判定 | 簡報加註 | 出處 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.01 AirDNA 活躍房源數 | — | 16,392 | — | 間(去重,含 Airbnb/Vrbo/Booking.com) | 截至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 吻合;頁面更新日 2026-11-11。 | web_str_market:16;web_verify_str_market:13 |
| 1.02 AirDNA ADR(實際成交每晚均價) | — | $193 | — | 晚(頁面未標幣別) | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 頁面只有「$」沒標幣別,不要跟 AUD 數字直接比;定義為已訂晚實際成交均價(近 12 個月)。 | web_str_market:17;web_verify_str_market:14;109 |
| 1.03 AirDNA 入住率(平均) | — | 67% | — | %(可訂晚數中被訂走的比例) | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 吻合。 | web_str_market:18;web_verify_str_market:15 |
| 1.04 AirDNA 每間年收入(平均,典型活躍房源) | — | $40.8K | — | 年(頁面未標幣別) | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 幣別未標、不要跟 AUD 直接比;頁面定義含房價加清潔費與其他房客費用、未扣房東成本(研究檔沒提含清潔費)。 | web_str_market:19;web_verify_str_market:16;109 |
| 1.05 AirDNA RevPAR | — | $129 | — | 晚可供出租 | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 吻合(幣別同樣只有「$」)。 | web_str_market:20;web_verify_str_market:17 |
| 1.06 AirDNA 年變化(10/2025→10/2026) | — | ADR -11.5%、入住率 +7.9%、RevPAR +3.3%、活躍房源 -36.8%、營收 +99.1% | — | % | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 數字與頁面完全相同;營收 +99.1% 確實寫在頁面,但研究檔判斷與 RevPAR +3.3% 難並存而不採用(見 7.03)。 | web_str_market:21;web_verify_str_market:18 |
| 1.07 AirROI 活躍房源數 | — | 10,096(年減 22%) | — | 間 | 2025-11 至 2026-10(近 12 個月) | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合;頁面標題「12 個月至 2026-10」。 | web_str_market:22;web_verify_str_market:19 |
| 1.08 AirROI ADR(每個已訂晚) | — | AUD 399(A$399) | — | 晚 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合;頁面另有 NSW 平均 A$470(不同地理範圍,別混用)。 | web_str_market:23;web_verify_str_market:20 |
| 1.09 AirROI 入住率(佔開放天數) | — | 49.5% | — | %(分母是開放天數) | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合;分母是「開放天數」,與 AirDNA/GuestFavorites 的「可訂天數」不同;頁面也四捨五入為 50%。 | web_str_market:24;web_verify_str_market:21 |
| 1.10 AirROI 每間年收入(平均) | — | AUD 52,495(年增 12.0%) | — | 年 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:25;web_verify_str_market:22 |
| 1.11 AirROI 每間每月收入(中位數) | — | 約 AUD 4,710 | — | 月 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:26;web_verify_str_market:23 |
| 1.12 AirROI 年收入中位數:Studio / 1 房 | — | AUD 40,500 / 44,100 | — | 年 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:27;web_verify_str_market:24 |
| 1.13 AirROI 年收入中位數:2 房 / 3 房 | — | AUD 54,000 / 54,500 | — | 年 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:28;web_verify_str_market:25 |
| 1.14 AirROI 年收入中位數:4 房 / 5 房以上 | — | AUD 63,500 / 78,900 | — | 年 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:29;web_verify_str_market:26 |
| 1.15 AirROI 年收入平均:Studio / 1 / 2 / 3 / 4 / 5+ 房 | — | AUD 42,400 / 46,800 / 60,700 / 67,900 / 83,100 / 104,000 | — | 年 | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:30;web_verify_str_market:27 |
| 1.16 GuestFavorites 活躍房源數 | — | 13,051 | — | 間 | 2025-11 至 2026-10 | Greater Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 | ⚠️ | 查核更正:原寫地理範圍 Sydney,頁面是 Greater Sydney(輕微);數值吻合。 | web_str_market:31;web_verify_str_market:28 |
| 1.17 GuestFavorites ADR | — | AUD 336(A$336) | — | 晚 | 2025-11 至 2026-10 | Greater Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 | ⚠️ | 查核更正:原寫 Sydney,頁面是 Greater Sydney;數值、幣別吻合。 | web_str_market:32;web_verify_str_market:29 |
| 1.18 GuestFavorites 入住率 | — | 68% | — | % | 2025-11 至 2026-10 | Greater Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 | ⚠️ | 查核更正:原寫 Sydney,頁面是 Greater Sydney;數值吻合。 | web_str_market:33;web_verify_str_market:30 |
| 1.19 GuestFavorites 每間年收入 | — | AUD 83,094(A$83,094) | — | 年 | 2025-11 至 2026-10 | Greater Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 | ⚠️ | 查核更正:原寫「平均」;頁面自相矛盾,績效卡標 Median Annual Revenue、內文標 average,引用時不要標成平均或中位其中一個;範圍是 Greater Sydney。 | web_str_market:34;web_verify_str_market:31;110 |
| 1.20 Airbtics 追蹤房源數(有評分且近 12 個月活躍至少 90 天) | — | 13,174 | — | 間 | 2025-09 至 2026-09 | Sydney | Airbtics | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ | 商業網站 | ⚠️ | 查核更正:原寫「僅納入較高評分房源,非全市場」,頁面查不到此說法,FAQ 的納入條件是「有 Airbnb 評分資料、近 12 個月至少 90 個活躍日、有入住率資料」(評分 4.3 只是計分下限,不是納入門檻)。 | web_str_market:35;web_verify_str_market:32;111 |
| 1.21 Airbtics 入住率(中位數) | — | 75% | — | % | 2025-09 至 2026-09 | Sydney | Airbtics | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ | 商業網站 | ✅ | 數值吻合;樣本定義見 1.20(不是「高評分」)。 | web_str_market:36;web_verify_str_market:33 |
| 1.22 Airbtics ADR(中位數) | — | AUD 281(A$281) | — | 晚 | 2025-09 至 2026-09 | Sydney | Airbtics | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ | 商業網站 | ✅ | 吻合。 | web_str_market:37;web_verify_str_market:34 |
| 1.23 Airbtics 每間年收入(中位數) | — | AUD 79,355(A$79,355) | — | 年 | 2025-09 至 2026-09 | Sydney | Airbtics | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ | 商業網站 | ✅ | 吻合;頁面 FAQ 另有「只含榜單前 30 名」中位數 A$46,562,別混用。 | web_str_market:38;web_verify_str_market:35 |
| 1.24 Airbtics 2025 全年:入住率 / ADR / 年收入 | — | 78.0% / $258 / $75,205(2024 為 $69,160,+8.74%) | — | % / 晚 / 年(頁面只有「$」,未標 AUD) | 2025 日曆年 | Sydney | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 | ⚠️ | 查核更正:原寫 AUD,頁面只有「$」、未標幣別(AUD 是研究檔推定);數值吻合。 | web_str_market:39;web_verify_str_market:36;112 |
| 1.25 Airbtics 2025 全澳(46 個市場):入住率 / ADR / 每間年收入 | — | 62.20% / $317 / $71,770 | — | % / 晚 / 年(幣別未標) | 2025 日曆年 | 全澳(46 個市場) | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 | ⚠️ | 查核更正:原寫 AUD/62.2%;頁面幣別未標;同頁全澳營收 2024 對照為 $45,174、「營收變化 4.52%」,兩者對不上,全澳營收可信度低、不要用(見 7.06)。 | web_str_market:40;web_verify_str_market:37;112 |
| 1.26 Hometime 入住率(市場平均) | — | 67% | — | % | 財年 2024-25(約 2024-07 至 2025-06) | Sydney | Hometime(自家管理資料與圖表) | https://www.hometime.io/blog/market-report-short-term-rental-sydney | 部落格 | ✅ | 吻合;表名 Sydney Airbnb average occupancy。 | web_str_market:41;web_verify_str_market:38 |
| 1.27 Hometime 典型每間年收入範圍 | $50,800 | — | $97,700 | 年(頁面只有「$」,來源與期間文中未標) | 約 2025–2026(文章 2026-07-08,期間未標) | Sydney | Hometime | https://www.hometime.io/blog/market-report-short-term-rental-sydney | 部落格 | ⚠️ | 查核更正:原寫 AUD,頁面只有「$」;數值、文章日期吻合;無期間無來源,若用請寫「Hometime 文章稱」。 | web_str_market:42;web_verify_str_market:39;113 |
| 1.28 AirROI 最旺月份(每間月收入) | — | 12 月,兩年日曆月平均約 AUD 7,300/月;近 12 個月 2025-12 為 AUD 7,638 | — | 月 | 約 2024-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:54;web_verify_str_market:45 |
| 1.29 AirROI 最淡月份(每間月收入) | — | 6 月,兩年日曆月平均約 AUD 4,490/月;近 12 個月 2026-06 為 AUD 4,690 | — | 月 | 約 2024-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合。 | web_str_market:55;web_verify_str_market:46 |
| 1.30 旺淡差(研究檔用上面兩數字算出,非來源直接給) | — | 12 月約為 6 月的 1.6 倍(7,300 / 4,490) | — | 倍 | 約 2024-11 至 2026-10 | Sydney | AirROI(研究檔計算) | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 查核員重算 1.626,數字無誤;這是研究檔自算,不是來源直接給。 | web_str_market:56;web_verify_str_market:47 |
| 1.31 GuestFavorites 入住率高峰 / 平季 / 低點月份 | — | 高峰 11 月、2 月;平季 12 月、1 月;低點 5 月、6 月(只有標籤,沒有各月數字) | — | 月份 | 2025-11 至 2026-10 | Sydney | GuestFavorites | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia | 商業網站 | ✅ | 吻合;看的是入住率,AirROI 看的是收入(含價格),兩者不矛盾。 | web_str_market:57;web_verify_str_market:48 |
| 1.32 AirDNA 季節性分數 | — | 91/100(100 = 月間營收落差小);頁面未列各月數字 | — | 分 | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 頁面定義是「最低與最高月平均營收的百分比差距,差距越小分數越高」;不要解讀成「淡旺季不明顯」,它與 AirROI 12 月約為 6 月 1.6 倍並存。 | web_str_market:58;web_verify_str_market:49;117 |
| 1.33 Hometime 價格高峰 / 最淡 | — | 價格高峰 12 月至 1 月(聖誕到跨年,跨年夜最高);最淡 5–6 月 | — | 月份 | 財年 2024-25 | Sydney | Hometime | https://www.hometime.io/blog/market-report-short-term-rental-sydney | 部落格 | ⚠️ | 查核更正:原寫 5–6 月為「價格最淡」;頁面沒指明價格最淡月,只說 5、6 月是 domestic market 最軟的月份、入住率入冬放緩(是需求最軟,不是價格最淡);高峰 12–1 月、跨年夜最高吻合。 | web_str_market:59;web_verify_str_market:50;114 |
| 1.34 AirDNA 活躍房源數年變化 | — | -36.8%(2025-10 → 2026-10) | — | % | 2025-10 至 2026-10 | Sydney | AirDNA | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 商業網站 | ✅ | 吻合;研究檔另轉述搜尋摘要 -42.0%(2025-09 → 2026-09),頁面未見,不採用(見 7.04)。 | web_str_market:93;web_verify_str_market:78;119 |
| 1.35 AirROI 活躍房源數年變化 | — | -22% | — | % | 2025-11 至 2026-10 | Sydney | AirROI | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney | 商業網站 | ✅ | 吻合(10,096 間、down 22% YoY)。 | web_str_market:94;web_verify_str_market:79 |
| 1.36 Airbtics 供給年增(2025 全年) | — | +28.88%(多出 2,851 間) | — | % / 間 | 2025 日曆年 | Sydney | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 | ✅ | 吻合;期間與 1.34、1.35 不同,方向相反,只能並列、不能寫成「供給一致減少」(見 7.13)。 | web_str_market:96;web_verify_str_market:81;120 |
| 1.37 City of Sydney 市區登記狀況 | — | 5,454 間活躍短租,其中 2,468 間有依 NSW 制度登記(搜尋摘要引述市議會資料,沒讀原文) | — | 間 | 約 2025–2026 | City of Sydney(只有市區) | 搜尋摘要(smartpropertyinvestment.com.au 等) | 原檔沒寫(原檔標「未直接讀取」) | 部落格(搜尋摘要) | 未查 | 未經獨立查核:研究檔自己只看到搜尋摘要、沒讀市議會原文,查核員未開啟;不要用於簡報。 | web_str_market:97;web_verify_str_market:82;119 |
| 1.38 Airbtics 全澳供給年增 | — | +13.79% | — | % | 2025 日曆年 | 全澳 | Airbtics | https://airbtics.com/short-term-rental-market-report-2025-australia | 產業報告 | ✅ | 吻合。 | web_str_market:98;web_verify_str_market:83 |

(BnbCalc 供給列 web_str_market:95 查核為 ❌,查核員沒有找到研究檔的數字,不放主表,見 7.01。)

## 2. 法規與平台費(180 天、登記費、15.5%、報稅、土地稅)

| 項目 | 低 | 中或單一值 | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 查核判定 | 簡報加註 | 出處 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.01 非房東同住(non-hosted)上限 | — | 每年 180 天(頁面用 days 不是 nights);從初次登記日起算每 12 個月;單筆連續 21 天以上的訂單不計入上限 | — | 天/年 | 官方頁最後更新 2025-02-10 | Greater Sydney(Eastern Harbour / Central River / Western Parkland 三個城市區) | NSW Department of Planning, Housing and Infrastructure | https://www.planning.nsw.gov.au/STRA | 官方 | ⚠️ | 核心數字(180 days、21 consecutive days、更新日 2025-02-10)吻合;「從登記日起算 12 個月」「三個城市區名稱」查核員沒看到、未能證實;對外前再開 planning.nsw.gov.au 確認有無 2025–2026 修法。 | web_str_market:67;web_verify_str_market:56;115 |
| 2.02 房東同住(hosted) | — | 不限天數(全年 365 天可出租) | — | 天/年 | 2021-04 公告(9 April 2021),2021-11-01 生效 | NSW 適用地區 | NSW Planning(新聞稿) | https://www.planning.nsw.gov.au/news/short-term-rental-accommodation-framework-finalised | 官方 | ✅ | 吻合;生效日原訂 2021-07-30、後延至 2021-11-01。 | web_str_market:68;web_verify_str_market:57 |
| 2.03 登記費 | — | 新登記 AUD 65;每年續約 AUD 25;皆不退費 | — | AUD | 官方頁最後更新 2025-02-10 | NSW | NSW Planning | https://www.planning.nsw.gov.au/STRA | 官方 | ✅ | 吻合(non-refundable);官方頁最後更新 2025-02-10。 | web_str_market:69;web_verify_str_market:58;115 |
| 2.04 登記制度 | — | 政府營運的登記(register)與排除名單(exclusion register)、最低防火安全標準、行為準則 | — | — | 2021-11-01 起 | NSW | NSW Planning(新聞稿) | https://www.planning.nsw.gov.au/news/short-term-rental-accommodation-framework-finalised | 官方 | ⚠️ | 查核更正:原寫「強制登記」「強制行為準則」;頁面只有行為準則標 mandatory,register 沒標強制;簡報改寫「政府營運登記制度」。 | web_str_market:70;web_verify_str_market:59;116 |
| 2.05 2024 檢討 | — | 2024-02-15 至 03-14 公開討論文件,430+ 份意見、2,400+ 份問卷;非房東天數上限「列為政策檢討中」,官方頁未列結果 | — | 份 | 2024 | NSW | NSW Planning | https://www.planning.nsw.gov.au/STRA | 官方 | ⚠️ | 日期與數字吻合(over 430 submissions、more than 2,400 survey responses);「天數上限列為政策檢討中、未列結果」這句查核員沒看到頁面有此措辭。 | web_str_market:71;web_verify_str_market:60 |
| 2.06 Byron Shire 另訂 60 天上限(不適用 Greater Sydney) | — | 60 天(2024-09-23 起) | — | 天/年 | 2024-09 | Byron Shire | NSW Planning | https://www.planning.nsw.gov.au/STRA | 官方 | ⚠️ | 範圍:頁面是大部分 Byron LGA 的 exempt development 路徑上限 60 天,另有兩個 365 天例外區,研究檔沒寫;與雪梨無關。 | web_str_market:72;web_verify_str_market:61 |
| 2.07 City of Sydney 市議會動議 | — | 2026-04-28 動議要求研究限制部分內城區「非主要居所」短租;是市議會行動,不是州法修改 | — | — | 2026-04 | City of Sydney | 二手報導(搜尋摘要,wboc.com 新聞稿頁,品質低) | 原檔沒寫(原檔標「未直接讀取」,只提 wboc.com) | 部落格(搜尋摘要) | 未查 | 未經獨立查核:非官方來源,不在查核範圍,查核員未開啟;研究檔自己也只有二手報導。 | web_str_market:73;web_verify_str_market:62 |
| 2.08 Airbnb 單一房東服務費(host-only fee) | — | 15.5%(房客不再另付服務費;依 Airbnb 頁面,15.5% 為全球平均) | — | % | 頁面 2026-07-29 發布、2026-10-13 更新 | Airbnb 澳洲站(頁面未寫澳洲專屬生效日) | Airbnb 官方資源頁 | https://www.airbnb.com.au/resources/hosting-homes/a/simplifying-airbnb-service-fees-746 | 官方(平台自述) | ✅ | 頁面寫明是全球平均、沒有澳洲專屬費率或日期;「房客不再另付」半句查核員未逐字確認;頁面說用物業管理軟體的房東「13 October」轉換,未寫年份。 | web_str_market:81;web_verify_str_market:68 |
| 2.09 Airbnb 舊制(分攤費) | — | 房東約 3%、房客另付約 14.1%–16.5% | — | % | 2025 以前(搜尋摘要引述舊版) | 澳洲 | Airbnb 澳洲頁(舊版,經搜尋摘要) | https://www.airbnb.com.au/resources/hosting-homes/a/simplifying-airbnb-service-fees-746 | 官方(平台自述;搜尋摘要) | 未查 | 未經獨立查核:研究檔自己標為搜尋摘要,查核員未開啟;不要用於簡報。 | web_str_market:82;web_verify_str_market:69;119 |
| 2.10 澳洲改制日(說法一):PMS 連線房東 | — | 2025-10-27 轉為單一 15.5%(由 15% 調為 15.5%) | — | % | 2025-10 | 澳洲 | Hometime | https://www.hometime.io/blog/what-airbnb-host-only-fee-means-for-you | 部落格 | ✅ | 吻合(27 October 2025: PMS-connected hosts moved to the single fee)。 | web_str_market:83;web_verify_str_market:70 |
| 2.11 澳洲改制日(說法二):自行管理、仍在舊制的房東 | — | 2026-09-15 起全部轉為單一費用,多數為訂單小計的 15.5% | — | % | 2026-09(文章 2026-09-08) | 澳洲 | Hometime | https://www.hometime.io/blog/what-airbnb-host-only-fee-means-for-you | 部落格 | ✅ | 吻合(15 September 2026 為 EEA 以外剩餘房東期限);同頁 FAQ 另寫「2025-10-27 起 Airbnb 向房東抽 15.5%」,與正文自相矛盾。 | web_str_market:84;web_verify_str_market:71 |
| 2.12 澳洲改制日(說法三) | — | 搜尋摘要有網站寫 2025-12-01 全部轉換;沒有直接讀到原文,只供參考 | — | — | 2025-12 | 澳洲 | 搜尋摘要(houst.com / hostaway 類指南) | 原檔沒寫(原檔標「未直接讀取」) | 部落格(搜尋摘要) | 未查 | 未經獨立查核:研究檔自己標為搜尋摘要,查核員未開啟;不要用於簡報(另見 2.13 Houst 頁寫 Since December 2025)。 | web_str_market:85;web_verify_str_market:72;119 |
| 2.13 F1 Airbnb 平台對房東抽成(原檔) | — | 15.5% | — | % 訂房小計 | 2026-05 更新(頁面 Updated May 11, 2026) | 全澳 | Houst | https://www.houst.com/blog/airbnb-hosting-fees-australia | 商業網站(短租代管商) | ✅ | 吻合;頁面寫「Since December 2025, Airbnb charges all Australian hosts a single 15.5% service fee on the booking subtotal」,subtotal 含清潔費、額外房客費、寵物費、不含稅與押金,所以 15.5% 也會抽到清潔費;「取代舊制 3%+14%」未驗;改制日各頁說法不同見 2.10–2.12。 | web_opcost_housing:37;web_verify_opcost_housing:26;146 |
| 2.14 T1 NSW 土地稅起徵點(一般) | — | 1,075,000 | — | AUD 土地價值 | 2026 土地稅年度 | NSW | Revenue NSW | https://www.revenue.nsw.gov.au/news-media-releases/preparing-for-the-2026-land-tax-year | 官方 | ✅ | 吻合(General Threshold of $1,075,000);土地稅看土地價值,不是房價。 | web_opcost_housing:108;web_verify_opcost_housing:50;129 |
| 2.15 T2 NSW 土地稅「優質」門檻 | — | 6,571,000 | — | AUD 土地價值 | 2026 土地稅年度 | NSW | Revenue NSW | https://www.revenue.nsw.gov.au/news-media-releases/preparing-for-the-2026-land-tax-year | 官方 | ✅ | 吻合(Premium Threshold of $6,571,000)。 | web_opcost_housing:109;web_verify_opcost_housing:51;129 |
| 2.16 T3 超過一般門檻的稅率 | — | 100 加超額部分的 1.6 | — | AUD 加 % | 2026 | NSW | 搜尋摘要引用 Revenue NSW 資料 | https://www.revenue.nsw.gov.au/news-media-releases/preparing-for-the-2026-land-tax-year | 官方(轉述;搜尋摘要) | 未查 | 未經獨立查核:該頁沒有任何稅率、只連到另一頁,研究檔自己也註明頁內沒給稅率,查核員沒開稅率頁;目前沒有已開頁面支持,不要用。 | web_opcost_housing:110;web_verify_opcost_housing:52;153 |
| 2.17 T4(補)ATO:短租收入申報重點 | — | 短租、透過平台出租、出租自己住家的一部分或全部,都要申報租金收入;要申報的是扣除平台費、代管費之前的毛額,還包括被取消訂單你留下的訂金/預訂費、保證金、損害保險金等;按法定持有比例分報;仲介代收的以房客付給仲介的年度為準;個人報稅表填在「澳洲利息或其他澳洲投資/財產收入」那一項 | — | 無數值(文字重點) | 頁面「最後更新 2026-05-21」 | 全澳 | ATO「Rental income you must declare」 | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare | 官方 | ⏸ | 未經獨立查核:查核員用 WebFetch 開 ATO 頁回 HTTP 403,沒用 Chrome 重試;5 點重點與「最後更新 2026-05-21」都沒驗到;研究檔註明費用怎麼扣本檔不寫、不構成報稅建議。 | web_opcost_housing_gapfill:80;web_verify_opcost_housing:73 |

## 3. 裝修與佈置(浴室、廚房、油漆、地板、家具佈置、開辦小項、工資、營造成本指數)

說明:裝修類來源多半是商業/報價導流網站(What's The Damage、The Quote Yard 等),不是官方統計,也不是成交價;請標「網路公開報價」。幣別全部 AUD。GST 以來源原文為準,沒寫的沒有補。3.01–3.50 來自 web_reno_setup(原檔),3.51–3.85 來自 web_reno_setup_gapfill(補查檔)。

| 項目 | 低 | 中或單一值 | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 查核判定 | 簡報加註 | 出處 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.01 浴室翻新:基本(來源標 Basic;含 GST) | 11,500 | 17,250 | 23,000 | AUD/每項 | 2026(頁面標 2026-11) | Sydney | What's The Damage | https://whatsthedamage.com.au/bathroom-renovation-cost-sydney/cost-breakdown/ | 商業網站 | ✅ | 吻合;Basic(budget fittings),含 GST,Sydney metro,Nov 2026。 | web_reno_setup:18;web_verify_reno_setup:16 |
| 3.02 浴室翻新:標準(來源標 Mid-range) | 23,000 | 31,050 | 40,250 | AUD/每項 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/bathroom-renovation-cost-sydney/cost-breakdown/ | 商業網站 | ✅ | 吻合。 | web_reno_setup:19;web_verify_reno_setup:17 |
| 3.03 浴室翻新:高階 | 40,250 | 48,300 | 63,250 | AUD/每項 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/bathroom-renovation-cost-sydney/cost-breakdown/ | 商業網站 | ✅ | 吻合;頁面另有 Luxury 63,250–92,000,研究檔沒列(非錯)。 | web_reno_setup:20;web_verify_reno_setup:18 |
| 3.04 浴室翻新:簡單更新(cosmetic refresh) | 8,000 | — | 15,000 | AUD/每項 | 2026(頁面 2026-09-08) | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 商業網站 | ✅ | 吻合;頁面 Published 8 Sep 2026,未標 GST。 | web_reno_setup:21;web_verify_reno_setup:19 |
| 3.05 浴室翻新:標準(4–8 m²) | 25,000 | — | 45,000 | AUD/每項 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:22;web_verify_reno_setup:20 |
| 3.06 浴室翻新:大雪梨標準家庭浴室 | 28,000 | — | 48,000 | AUD/每項 | 2026 | Sydney | The Quote Yard | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 商業網站 | ✅ | 吻合(Greater Sydney 標準家庭浴室)。 | web_reno_setup:23;web_verify_reno_setup:21 |
| 3.07 浴室翻新:西雪梨標準浴室 | 22,000 | — | 38,000 | AUD/每項 | 2026 | Sydney(西區) | The Quote Yard | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 商業網站 | ✅ | 吻合(Western Sydney,2026)。 | web_reno_setup:24;web_verify_reno_setup:22 |
| 3.08 浴室翻新:起價 | 14,900 | — | — | AUD/每項(起價) | 2025(頁面 2025-04-02) | 全澳(頁面未分地區) | Airtasker | https://www.airtasker.com/au/costs/house-renovation/house-renovation-cost/ | 商業網站 | ✅ | 吻合(Last Updated 02 April 2025);地區「全澳」是研究檔推斷(AU 站),頁面未明寫地區。 | web_reno_setup:25;web_verify_reno_setup:23 |
| 3.09 浴室翻新:預算型整間(搜尋摘要) | 20,000 | — | 27,000 | AUD/每項 | 2025 | 全澳 | Domain(引述 The Makeover Group 負責人) | https://www.domain.com.au/advice/bathroom-renovation-costs/ | 商業網站(搜尋摘要) | ⏸ | 未經獨立查核:Domain 頁 HTTP 403 打不開,研究檔自己也只有搜尋摘要、沒開過原頁;補查前不要用(見 7.21)。 | web_reno_setup:26;web_verify_reno_setup:24;110 |
| 3.10 浴室翻新:低檔帶(舊資料,僅供對照) | 4,000–20,000(低檔帶) | 20,001–40,000(中檔帶) | 40,000+(頁面稱 Luxury) | AUD/每項 | 2014(Houzz AU 2014-06-11) | 全澳 | Houzz Australia | https://www.houzz.com.au/magazine/bathroom-renovation-how-much-will-it-cost-me-stsetivw-vs~26882976 | 商業網站 | ⚠️ | 查核更正:原寫「低 4,000」,只是低檔帶下限,低檔帶實為 4,000–20,000;原寫「高 40,000+」頁面稱 Luxury;2014 年舊資料不要放簡報(見 7.20)。 | web_reno_setup:27;web_verify_reno_setup:25;107 |
| 3.11 浴室磁磚鋪貼人工(標準磁磚) | 65 | — | 120 | AUD/每平方公尺 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 商業網站 | ✅ | 吻合;標準尺寸陶瓷/瓷磚,僅人工不含磚。 | web_reno_setup:28;web_verify_reno_setup:26 |
| 3.12 浴室磁磚鋪貼人工(大片/天然石) | 100 | — | 180 | AUD/每平方公尺 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw | 商業網站 | ✅ | 吻合;大片/天然石/複雜圖案,僅人工。 | web_reno_setup:29;web_verify_reno_setup:27 |
| 3.13 廚房翻新:簡單換新(cosmetic refresh) | 9,200 | 16,100 | 23,000 | AUD/每項 | 2026(Nov 2026 price index) | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合;Kitchen cosmetic refresh(reface+paint),含 GST,Sydney Nov 2026。 | web_reno_setup:30;web_verify_reno_setup:28 |
| 3.14 廚房翻新:簡單換新(cosmetic refresh) | 8,000 | — | 18,000 | AUD/每項 | 2026(頁面 2026-09-29) | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/kitchen-renovation-cost-nsw | 商業網站 | ✅ | 吻合(Published 29 Sep 2026)。 | web_reno_setup:31;web_verify_reno_setup:29 |
| 3.15 廚房翻新:平價組裝櫃(flat pack) | 12,000 | — | 22,000 | AUD/每項 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/kitchen-renovation-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:32;web_verify_reno_setup:30 |
| 3.16 廚房翻新:小廚房(<10 m²) | 18,000 | — | 30,000 | AUD/每項 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/kitchen-renovation-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:33;web_verify_reno_setup:31 |
| 3.17 廚房翻新:標準(10–18 m²) | 30,000 | — | 55,000 | AUD/每項 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/kitchen-renovation-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:34;web_verify_reno_setup:32 |
| 3.18 廚房翻新:標準,雪梨市區(Inner Sydney) | 42,000 | — | 68,000 | AUD/每項 | 2026 | Sydney(市區) | The Quote Yard | https://www.thequoteyard.com.au/services/kitchen-renovation-cost-nsw | 商業網站 | ✅ | 吻合(Paddington、Surry Hills、Newtown、Balmain 區域表)。 | web_reno_setup:35;web_verify_reno_setup:33 |
| 3.19 廚房翻新:起價 | 30,000 | — | — | AUD/每項(起價) | 2025(頁面 2025-04-02) | 全澳(頁面未分地區) | Airtasker | https://www.airtasker.com/au/costs/house-renovation/house-renovation-cost/ | 商業網站 | ✅ | 吻合(Last Updated 02 April 2025)。 | web_reno_setup:36;web_verify_reno_setup:34 |
| 3.20 地毯供應+安裝(最接近的地板項目) | 52 | 80 | 125 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup:37;web_verify_reno_setup:35 |
| 3.21 1 房 Airbnb 開辦合計(含臥室組、客廳、智慧鎖、攝影機、毛巾枕頭毯、人工) | — | 5,358 | — | AUD/每項 | 資料期間 2023-10 至 2024-09;頁面 © 2026 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(AU$5,358);分項 1,976 + 2,356 + 1,026 查核員加過吻合;資料是 2023-10 至 2024-09,與其他 2026 報價不同年。 | web_reno_setup:43;web_verify_reno_setup:36 |
| 3.22 2 房 Airbnb 開辦合計(同上口徑) | — | 7,539 | — | AUD/每項 | 資料期間 2023-10 至 2024-09;頁面 © 2026 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ⚠️ | 頁面有寫 AU$7,539,但沒給 2 房分項,頁面文字還把 7,539 誤掛在客廳小節,前後不一致、無法驗證組成;查核員試算 2 房 = 1 房 + 多一間臥室組 1,976 → 7,334,與 7,539 差 205;不建議用(見 7.19)。 | web_reno_setup:44;web_verify_reno_setup:37;104 |
| 3.23 其中:臥室家具組 | — | 1,976 | — | AUD/每項 | 資料期間 2023-10 至 2024-09;頁面 © 2026 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(7 項加總吻合);頁面明寫 per bedroom。 | web_reno_setup:45;web_verify_reno_setup:38 |
| 3.24 其中:客廳 | — | 2,356 | — | AUD/每項 | 資料期間 2023-10 至 2024-09;頁面 © 2026 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(6 項加總吻合)。 | web_reno_setup:46;web_verify_reno_setup:39 |
| 3.25 其中:其他(鎖、攝影機、人工、毛巾枕頭毯) | — | 1,026 | — | AUD/每項 | 資料期間 2023-10 至 2024-09;頁面 © 2026 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(毛巾/枕頭/毯各 152、智慧鎖 228、攝影機 152、人工 190,加總 1,026)。 | web_reno_setup:47;web_verify_reno_setup:40 |
| 3.26 小型 1 房家具套裝(搜尋摘要;來源為非澳洲業者) | 2,000 | — | 5,000 | AUD/每項(原文幣別未確認) | 未標示 | 非澳洲(研究檔推斷;不當澳洲數字用,只當低標對照) | Minoan | https://minoan.com/blog/airbnb-furniture-packages | 商業網站(搜尋摘要) | ⚠️ | 數值吻合、幣別頁面未標吻合;但「非澳洲業者」頁面沒有證實也沒證偽,是研究檔推斷(頁面沒說公司在哪國);不要寫成澳洲價(見 7.24)。 | web_reno_setup:48;web_verify_reno_setup:41;111 |
| 3.27 全套代佈置服務「典型單價」(搜尋摘要;房數未標) | 12,000 | — | 25,000 | AUD/每項 | 未標示 | 全澳(業者列在 Houzz) | Hostmybnb(Houzz 商家頁) | https://www.houzz.se/pro/hostmybnb/airbnb-furnishing-services-by-hostmybnb | 商業網站(搜尋摘要) | ✅ | 吻合(12 000 AUD - 25 000 AUD);頁面無房數。 | web_reno_setup:49;web_verify_reno_setup:42 |
| 3.28 專業攝影:基本(10–15 張精修) | 250 | — | 300 | AUD/每項 | 2026(頁面 2026-09-17) | 全澳 | Hometime | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth | 商業網站 | ✅ | 吻合(Sep 17, 2026);頁面摘要未直接寫「全澳」,以 AUD 計。 | web_reno_setup:57;web_verify_reno_setup:43 |
| 3.29 專業攝影:標準(20–30 張) | 295 | — | 500 | AUD/每項 | 2026 | 全澳 | Hometime | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth | 商業網站 | ✅ | 吻合。 | web_reno_setup:58;web_verify_reno_setup:44 |
| 3.30 專業攝影:高階(空拍、黃昏、大屋) | 500 | — | 1,000+ | AUD/每項 | 2026 | 全澳 | Hometime | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth | 商業網站 | ✅ | 吻合。 | web_reno_setup:59;web_verify_reno_setup:45 |
| 3.31 智慧門鎖(Airbtics 開辦清單內的單項) | — | 228 | — | AUD/每項 | 2023-10 至 2024-09 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(Smart lock AU$228)。 | web_reno_setup:60;web_verify_reno_setup:46 |
| 3.32 智慧門鎖:Yale Assure 電子門閂(零售價,特價/原價) | 520 | — | 660 | AUD/每項(不含安裝) | 頁面未標年份 | 全澳(零售) | Entry Point(零售商) | https://entry-point.com.au/products/yale-assure-keyed-electronic-deadbolt-black | 商業網站 | ⏸ | 未經獨立查核:查核員開頁回 HTTP 429(重試一次仍 429);補查前不要用(見 7.22)。【晚上補查 2026-11-14】Chrome 開到商品頁;在已登入的 Chrome 看到標價 550.00、原價 787.07(Save 30%);頁面另寫登入才顯示價格,未登入看到什麼沒驗;520、660 不要再引用。 | web_reno_setup:61;web_verify_reno_setup:47;110 |
| 3.33 智慧門鎖:Yale Keyless Connected(最低零售價,搜尋摘要) | 145 | — | — | AUD/每項(不含安裝) | 頁面未標年份 | 全澳(零售) | BuyWisely(比價站) | https://buywisely.com.au/product/yale-keyless-connected-door-lock | 商業網站(搜尋摘要) | ⏸ | 未經獨立查核:查核員開頁回 HTTP 403;此數被原檔 7 節「低」情境使用(見 6(i)、7.23)。 | web_reno_setup:62;web_verify_reno_setup:48;110 |
| 3.34 安全攝影機(Airbtics 清單單項) | — | 152 | — | AUD/每項 | 2023-10 至 2024-09 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(Security camera AU$152)。 | web_reno_setup:63;web_verify_reno_setup:49 |
| 3.35 毛巾 / 枕頭 / 毯子(三類各一筆) | — | 152 + 152 + 152 | — | AUD/每類 | 2023-10 至 2024-09 | 全澳 | Airbtics | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | ✅ | 吻合(Towels 152、Pillows 152、Blankets 152)。 | web_reno_setup:64;web_verify_reno_setup:50 |
| 3.36 首次深度清潔(單次) | — | 242 | — | AUD/每次 | 2026(頁面 2026-10-23) | Sydney | Maid for You | https://www.maidforyou.com.au/blog/how-much-end-of-lease-clean/ | 商業網站 | ✅ | 吻合(Deep clean $242/session,Updated 23 October 2026);頁面未見房型條件,不知 242 對應幾房;研究檔另記同業者另一頁搜尋摘要寫深度清潔 223、退租 390,取本頁。 | web_reno_setup:65,73;web_verify_reno_setup:51 |
| 3.37 退租級大掃除:Studio / 1 房 | — | 410 | — | AUD/每次 | 2026 | Sydney | Maid for You | https://www.maidforyou.com.au/blog/how-much-end-of-lease-clean/ | 商業網站 | ✅ | 吻合(Studio / 1 bedroom $410)。 | web_reno_setup:66;web_verify_reno_setup:52 |
| 3.38 退租級大掃除:2 房 | — | 450 | — | AUD/每次 | 2026 | Sydney | Maid for You | https://www.maidforyou.com.au/blog/how-much-end-of-lease-clean/ | 商業網站 | ✅ | 吻合(2 bedrooms $450)。 | web_reno_setup:67;web_verify_reno_setup:53 |
| 3.39 居家清潔時薪 | 40 | 63 | 92 | AUD/每小時 | 2026(Nov 2026) | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合(House cleaning general per hour)。 | web_reno_setup:68;web_verify_reno_setup:54 |
| 3.40 地毯蒸氣清洗 | 34 | 52 | 69 | AUD/每間房 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合(Carpet steam clean per room)。 | web_reno_setup:69;web_verify_reno_setup:55 |
| 3.41 油漆工(時薪) | 40 | 60 | 100 | AUD/每小時 | 2026(Nov 2026) | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合(Painter per hour)。 | web_reno_setup:80;web_verify_reno_setup:56 |
| 3.42 水電工:電工 | 92 | 115 | 170 | AUD/每小時 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合(Electrician per hour)。 | web_reno_setup:81;web_verify_reno_setup:57 |
| 3.43 水電工:水管工 | 92 | 140 | 230 | AUD/每小時 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合(Plumber per hour)。 | web_reno_setup:82;web_verify_reno_setup:58 |
| 3.44 雜工(handyman) | 57 | 105 | 140 | AUD/每小時 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/price-index/sydney/2026-11/ | 商業網站 | ✅ | 吻合(Handyman per hour)。 | web_reno_setup:83;web_verify_reno_setup:59 |
| 3.45 雜工(handyman)平日時薪(多數落在 90–110) | 80 | — | 120 | AUD/每小時 | 2026(頁面 2026-08-24) | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/handyman-pricing-guide-nsw | 商業網站 | ✅ | 吻合(majority $90 to $110;Published 24 Aug 2026)。 | web_reno_setup:84;web_verify_reno_setup:60 |
| 3.46 雜工:半天(4 小時) | 350 | — | 500 | AUD/每半天 | 2026 | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/handyman-pricing-guide-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:85;web_verify_reno_setup:61 |
| 3.47 雜工:全天(8 小時) | 600 | — | 900 | AUD/每天 | 2026 | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/handyman-pricing-guide-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:86;web_verify_reno_setup:62 |
| 3.48 雜工:週末/夜間時薪 | 120 | — | 180 | AUD/每小時 | 2026 | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/handyman-pricing-guide-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup:87;web_verify_reno_setup:63 |
| 3.49 用 Airbnb 專業攝影的房源,之後一年收入多出的比例 | — | 21 | — | %(次年收入) | 2026 頁面轉述(樣本約 14,700 筆) | 全球(不是澳洲) | Hometime 轉述 Airbnb 自家數據 | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth | 商業網站(轉述平台官方資料) | ✅ | 吻合;Airbnb 自家全球樣本(約 14,700 筆)、非澳洲、未給期間與方法、因果不明,只能當背景敘述,不要當係數乘進試算(見 7.26)。 | web_reno_setup:95,98;web_verify_reno_setup:64;109 |
| 3.50 攝影費用能在一筆訂單內回本的房東比例 | — | 85 | — | %(房東比例) | 2026 頁面轉述 | 全球 | Hometime 轉述 Airbnb 自家數據 | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth | 商業網站(轉述平台官方資料) | ⚠️ | 定義:頁面歸給 Airbnb「85% 的房東在一次訂房內回本」,摘要同時出現「one night's stay」另一種說法,不確定哪個是原意;若用請寫「一次訂房」並註明為 Airbnb 自述(見 7.25)。 | web_reno_setup:96;web_verify_reno_setup:65;108 |
| 3.51(補)室內牆面油漆(多數落在 18–30) | 15 | — | 45 | AUD/每平方公尺 | 2026 | NSW(頁面以 Sydney 為主) | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合(most straightforward work $18 to $30);油漆頁沒標 GST。 | web_reno_setup_gapfill:19;web_verify_reno_gapfill:17;124 |
| 3.52(補)天花板油漆 | 20 | — | 40 | AUD/每平方公尺 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup_gapfill:20;web_verify_reno_gapfill:18 |
| 3.53(補)標準臥室整間(約 3×3.5 m、2.4 m 天花板,含天花板與全部木作) | 450 | — | 750 | AUD/每房 | 2026 | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合;同頁「At a Glance」表另給 Sydney 臥室整間 $500–$900,與 450–750 不一致,簡報請標「來源頁內有 500–900 的另一組臥室價」。 | web_reno_setup_gapfill:21;web_verify_reno_gapfill:19;103 |
| 3.54(補)臥室(3 m 天花板、兩窗、有衣櫃、牆況差) | 900 | — | 1,200 | AUD/每房 | 2026 | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup_gapfill:22;web_verify_reno_gapfill:20 |
| 3.55(補)客餐廳合併(約 30 m² 樓地板、標準天花板) | 700 | — | 1,400 | AUD/每區 | 2026 | Sydney | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合;若屋型是開放式客餐廚,不能與 3.57 廚房牆面同時加(重複計算),應改用 3.56。 | web_reno_setup_gapfill:23;web_verify_reno_gapfill:21;104 |
| 3.56(補)開放式客餐廚(天花板 >2.7 m 或複雜格局) | 1,500 | — | 2,500 | AUD/每區 | 2026 | Sydney / NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合(頁面標 Sydney)。 | web_reno_setup_gapfill:24;web_verify_reno_gapfill:22 |
| 3.57(補)廚房牆面 | 400 | — | 800 | AUD/每間 | 2026 | Sydney | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合(per kitchen)。 | web_reno_setup_gapfill:25;web_verify_reno_gapfill:23 |
| 3.58(補)浴室(防潮漆) | 300 | — | 650 | AUD/每間 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合;頁面是「浴室或洗衣間」。 | web_reno_setup_gapfill:26;web_verify_reno_gapfill:24 |
| 3.59(補)室內門(雙面、四邊、含門框) | 80 | — | 150 | AUD/每扇 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合。 | web_reno_setup_gapfill:27;web_verify_reno_gapfill:25 |
| 3.60(補)踢腳板(油漆) | 8 | — | 15 | AUD/每公尺(線性) | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合(per linear metre)。 | web_reno_setup_gapfill:28;web_verify_reno_gapfill:26 |
| 3.61(補)3 房獨棟整戶室內(對照用,不是公寓) | 4,500 | — | 9,000 | AUD/每戶 | 2026 | Sydney | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合;頁面沒有 1 房/2 房公寓整戶價(查核員確認,見 6(i))。 | web_reno_setup_gapfill:29;web_verify_reno_gapfill:27,29 |
| 3.62(補)3 房出租屋整戶室內(中階漆,對照用) | 3,500 | — | 6,000 | AUD/每戶 | 2026 | Sydney | The Quote Yard | https://www.thequoteyard.com.au/services/interior-painting-cost-nsw | 商業網站 | ✅ | 吻合;同頁另有業主自住高階漆 $5,500–$9,000,研究檔沒列(沒錯,只是沒拿)。 | web_reno_setup_gapfill:30;web_verify_reno_gapfill:28 |
| 3.63(補)複合木地板 laminate(含材料+安裝;含 GST) | 57 | 75 | 115 | AUD/每平方公尺 | 2026(頁面標 2026-11) | Sydney 都會區 | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;頁面標 updated and last verified November 2026、價格含 GST、Sydney 都會區(外圍可能不同)。 | web_reno_setup_gapfill:38;web_verify_reno_gapfill:37,33 |
| 3.64(補)乙烯塑膠板 vinyl plank(含材料+安裝) | 57 | 86 | 115 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:39;web_verify_reno_gapfill:38 |
| 3.65(補)Hybrid / SPC(含材料+安裝) | 63 | 92 | 140 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:40;web_verify_reno_gapfill:39 |
| 3.66(補)海島型/工程木地板 engineered timber(含材料+安裝) | 125 | 160 | 230 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:41;web_verify_reno_gapfill:40 |
| 3.67(補)實木地板 solid hardwood(含材料+安裝) | 170 | 230 | 320 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:42;web_verify_reno_gapfill:41 |
| 3.68(補)浮動式地板僅人工(材料自備) | 29 | 40 | 63 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:43;web_verify_reno_gapfill:42 |
| 3.69(補)舊地板拆除與清運 | 9 | 17 | 29 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:44;web_verify_reno_gapfill:43 |
| 3.70(補)地基整平/備料 | 23 | 46 | 105 | AUD/每平方公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合;含 GST。 | web_reno_setup_gapfill:45;web_verify_reno_gapfill:44 |
| 3.71(補)踢腳板(供應+安裝) | 12 | 21 | 34 | AUD/每公尺 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合(per linear metre);含 GST。 | web_reno_setup_gapfill:46;web_verify_reno_gapfill:45 |
| 3.72(補)該頁自己的例子:40 m² 鋪 hybrid(未含拆舊與踢腳板) | — | 3,680 | — | AUD/每項 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合(roughly $3,680 = 40 × $92,before removal and trims);40 m² 是該頁範例面積,不是我們 1 房的實際坪數。 | web_reno_setup_gapfill:47;web_verify_reno_gapfill:46,106 |
| 3.73(補)該頁自己的例子:55 m² 兩房單位鋪 hybrid(未含拆舊) | 3,465 | — | 7,700 | AUD/每項 | 2026 | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合(55×63 到 55×140);拆舊另加 $495–$1,595。 | web_reno_setup_gapfill:48;web_verify_reno_gapfill:47 |
| 3.74(補)Sydney 地板費用過去一年上漲(該站自己的說法,「對照 90+ 來源」,不是官方統計) | — | 約 3.4 | — | %(年增) | 過去一年(頁面標 2026-11) | Sydney | What's The Damage | https://whatsthedamage.com.au/flooring-cost-sydney/ | 商業網站 | ✅ | 吻合(up around 3.4% over the past year);是商業站說法,不是官方統計。 | web_reno_setup_gapfill:50;web_verify_reno_gapfill:48 |
| 3.75(補)建築營造(Building construction)產出價格指數,季增 | — | +1.3 | — | %(季增,2026 年 9 月季對 6 月季) | 2026 Q3(2026-10-30 發布) | 全澳(非雪梨) | 澳洲統計局 ABS,Producer Price Indexes | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026 | 官方 | ⚠️ | 查核更正:原寫「主因非住宅營造」,頁面沒這麼寫(非住宅只是分類中漲最多:非住宅 +1.7、其他住宅 +1.3、房屋營造 +1.0),頁面把原因歸給中東衝突與燃料、運費、技術工短缺;1.3%、季別、全澳都對(見 7.29)。 | web_reno_setup_gapfill:56;web_verify_reno_gapfill:56,121 |
| 3.76(補)住宅營造(Residential building construction)季增 | — | +1.1 | — | %(季增;頁面文字寫主因是技術工短缺推高工資、運費與進口材料) | 2026 Q3 | 全澳 | 澳洲統計局 ABS | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026 | 官方 | ⚠️ | 查核更正:原寫「對最終需求指數的貢獻」;頁面只在最終需求季增的主要貢獻項清單寫 Residential building construction (+1.1%),查核檔寫工具判斷 +1.1% 較可能是該類價格自己的季變動、頁面沒明說,且與最終需求整體季增同為 1.1%、易混淆;同頁房屋營造 +1.0%、其他住宅 +1.3%(見 7.28)。 | web_reno_setup_gapfill:57;web_verify_reno_gapfill:57,120 |
| 3.77(補)所有最終需求(Final demand,整體經濟,不是只有營造)年增 | — | +3.6 | — | %(年增,2025 Q3 起算至 2026 Q3) | 2026 Q3 | 全澳 | 澳洲統計局 ABS | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026 | 官方 | ✅ | 吻合(Final demand rose 1.1% this quarter and 3.6% throughout the year);這是整體經濟,不是營造。 | web_reno_setup_gapfill:58;web_verify_reno_gapfill:58 |
| 3.78(補)ABS 營造專屬年增(查核員在頁面文字與表格看到;研究檔原寫沒有) | — | 建築營造 4.9;房屋營造 5.7;其他住宅營造 4.1;非住宅營造 4.8 | — | %(年增) | 至 2026 年 9 月季 | 全澳(雪梨層級頁面沒有) | 澳洲統計局 ABS(查核員補看到) | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026 | 官方 | ❌ | 查核更正:原寫「頁面只有營造季增、沒看到房屋/住宅營造年增,官方給不出年增」「年增只能引最終需求 3.6%」;頁面文字與表格都有營造專屬年增(表列房屋營造 AUST 季增 1.0、年增 5.7;NSW +1.7% 為房屋營造季增貢獻最大的州),比 3.6% 高 1.3–2.1 個百分點;若放「成本近一年漲多少」用營造 4.9%、註明全澳不是雪梨,並先人工複看原頁(見 7.30)。 | web_reno_setup_gapfill:60;web_verify_reno_gapfill:59,113,122 |
| 3.79(補)1 房 Airbnb「寬裕但不奢華」開辦整體(WebFetch 摘要;項目細節未列) | 5,000 | — | 7,000 | AUD/每項 | 2026(頁面日期 2026-05-07) | 澳洲(頁面寫給澳洲房東,未分城市) | Hometime | https://www.hometime.io/blog/airbnb-renovate-vs-redecorate | 商業網站(代管公司) | ⚠️ | 查核更正:原寫「寬裕但不奢華」,頁面是「modest(簡樸/適中)」,簡報請寫「適中的 1 房開辦」;數字、幣別、日期、範圍都對;頁面沒列細項,不能與 Airbtics 5,358 逐項比(見 7.31)。 | web_reno_setup_gapfill:66;web_verify_reno_gapfill:65,123 |
| 3.80(補)較大/高階房源開辦(沒分房數;不能當 2 房數字) | 8,000 | — | 15,000 | AUD/每項 | 2026(2026-05-07) | 澳洲 | Hometime | https://www.hometime.io/blog/airbnb-renovate-vs-redecorate | 商業網站 | ✅ | 吻合(larger homes or luxury properties);「不能當 2 房數字」的提醒正確。 | web_reno_setup_gapfill:67;web_verify_reno_gapfill:66 |
| 3.81(補)找外部佈置公司全套代辦 | 25,000+ | — | — | AUD/每項(起價) | 2026(頁面日期 2026-07-15) | 澳洲 | Hometime | https://www.hometime.io/blog/airbnb-setup-guide-costs-timelines | 商業網站 | ✅ | 吻合(often $25K+)。 | web_reno_setup_gapfill:68;web_verify_reno_gapfill:67 |
| 3.82(補)代管公司的上線費(首次清潔、攝影、鑰匙盒或智慧鎖安裝、刊登費) | 600 | — | 1,000 | AUD/每項 | 2026(2026-07-15) | 澳洲 | Hometime | https://www.hometime.io/blog/airbnb-setup-guide-costs-timelines | 商業網站 | ✅ | 吻合;是 Hometime 自己的收費(Typical onboarding costs range from $600–$1,000 at Hometime),不是通用行情。 | web_reno_setup_gapfill:69;web_verify_reno_gapfill:68 |
| 3.83(補)2 房 Airbnb 開辦合計(上一份檔已有的 Airbtics 數字,仍是唯一的 2 房澳洲數字) | — | 7,539 | — | AUD/每項 | 2023-10 至 2024-09 | 全澳 | Airbtics(上一份檔) | https://airbtics.com/starting-an-airbnb-australia | 商業網站 | 未查 | 未經獨立查核:補查檔查核員未重開此頁(超出本次範圍);同一數字在原檔查核(3.22)已判 ⚠️,頁面前後不一致、不建議用(見 7.19)。 | web_reno_setup_gapfill:70;web_verify_reno_gapfill:69 |
| 3.84(補)智慧鎖安裝師傅報價(搜尋摘要;自填的案件價,有些只含人工) | 202 | 276(中位數) | 375 | AUD/每把 | 頁面未標年份(查核員看到頁面「Last updated on 7th Nov 2026」) | Sydney | Airtasker | https://www.airtasker.com/au/services/smart-lock-installation/sydney/ | 商業網站(搜尋摘要) | ✅ | 查核員已打開原頁,吻合;價格本身沒另標年份;未說含不含鎖本體,研究檔「有些只含人工」頁面沒寫。 | web_reno_setup_gapfill:78;web_verify_reno_gapfill:75 |
| 3.85(補)智慧鎖每扇門追加費用(搜尋摘要;含不含鎖本體未確認) | 200 | — | 600 | AUD/每扇 | 2026 | NSW | The Quote Yard | https://www.thequoteyard.com.au/services/home-security-nsw | 商業網站(搜尋摘要) | ✅ | 查核員已打開原頁,吻合(smart locks add $200 to $600 for each door;indicative 2026 NSW estimates);未說含不含鎖或人工。 | web_reno_setup_gapfill:79;web_verify_reno_gapfill:76 |

(研究檔自己排除、沒列表的數字:What's The Damage 鎖匠頁「智慧鎖含安裝 17–57」web_reno_setup_gapfill:81、Payscale 雪梨油漆工約 34/小時 web_reno_setup:89;前者查核員未查,見 7.32。)

## 4. 營運成本(電、水、瓦斯、網路、清潔、代管、管理費、市政費、保險)

說明:列編號沿用營運成本研究檔的 ID;「(原)」= web_opcost_housing,「(補)」= web_opcost_housing_gapfill。平台抽成 15.5% 放在第 2 段 2.13。電費 E 系列是 AER「預設市場價」(standing offer 價格上限,典型家戶用電量,來源沒寫度數),像「上限型」參考值,不是小套房實際帳單;草案與最終版可能不同(研究檔註)。

| 項目 | 低 | 中或單一值 | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 查核判定 | 簡報加註 | 出處 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4.01 E1 電費:Ausgrid 供電區,單一費率住宅,標準用電量(上限價) | — | 1,965 | — | AUD/年 | 2025-26 年度(2025/7–2026/6) | NSW(Ausgrid 供電網路區) | Canstar 引用 AER 預設市場價 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 商業網站(轉述官方) | ⚠️ | 數字、單一費率、無受控負載吻合;頁面欄名只寫 Current price,期間 2025-26 是推論;頁面沒給用電度數(「標準用電量」沿用 AER 平均家戶說法);小公寓實際帳單通常較低。 | web_opcost_housing:14;web_verify_opcost_housing:18,139 |
| 4.02 E2 電費:Ausgrid,2026-27 草案 | — | 1,875 | — | AUD/年 | 2026-27 年度(草案,非最終) | NSW(Ausgrid) | Canstar 引用 AER 預設市場價 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 商業網站(轉述官方) | ✅ | 吻合(Draft price $1,875,−$90,−4.6%),頁面也標為草案;不是最終版。 | web_opcost_housing:15;web_verify_opcost_housing:19,139 |
| 4.03 E3 電費:Endeavour Energy 供電區 | — | 2,411 | — | AUD/年 | 2025-26 年度 | NSW(Endeavour,雪梨西/南部一帶) | Canstar 引用 AER 預設市場價 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 商業網站(轉述官方) | ⚠️ | 同 4.01:頁面欄名只寫 Current price,期間 2025-26 是推論。 | web_opcost_housing:16;web_verify_opcost_housing:20 |
| 4.04 E4 電費:Endeavour,2026-27 草案 | — | 2,347 | — | AUD/年 | 2026-27 年度(草案) | NSW(Endeavour) | Canstar 引用 AER 預設市場價 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 商業網站(轉述官方) | ✅ | 吻合(Draft price $2,347,−$64,−2.7%);草案。 | web_opcost_housing:17;web_verify_opcost_housing:21 |
| 4.05 E5 電費:Essential Energy 供電區(非雪梨市區,供參考) | — | 2,741 | — | AUD/年 | 2025-26 年度 | NSW(Essential,多為郊區/外圍) | Canstar 引用 AER 預設市場價 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 商業網站(轉述官方) | ⚠️ | 同 4.01:期間 2025-26 是推論。 | web_opcost_housing:18;web_verify_opcost_housing:22 |
| 4.06 E6 電費:Essential,2026-27 草案 | — | 2,515 | — | AUD/年 | 2026-27 年度(草案) | NSW(Essential) | Canstar 引用 AER 預設市場價 | https://www.canstar.com.au/news/regulator-to-shift-electricity-prices-in-reverse-march-2026/ | 商業網站(轉述官方) | ✅ | 吻合(Draft price $2,515,−$226,−8.2%);草案。 | web_opcost_housing:19;web_verify_opcost_housing:23 |
| 4.07 E7 官方原件(待核對 E2/E4/E6 草案與最終版) | — | (只有網址,無數值) | — | — | 2026-27 草案資訊頁 | NSW | AER Draft Default Market Offer 2026-27 information sheet | https://www.aer.gov.au/system/files/2026-03/Draft%20Default%20Market%20Offer%202026-27%20-%20Information%20sheet.pdf | 官方 | ⏸ | 未經獨立查核:查核員 WebFetch 逾時(60 秒),官方原件沒打開,E2/E4/E6 仍只有 Canstar 轉述;研究檔也只在搜尋結果看到網址、沒開。【晚上補查 2026-11-14】Chrome 開這份 PDF 被轉到 AER 登入頁(Access denied),沒拿到;AER 最終版新聞稿(2026-05-26)只寫 NSW 住宅降 3.4% 到 5.0%,沒有 Ausgrid 年電費和年用電量;final determination PDF 與 information kit 頁還沒開。 | web_opcost_housing:20;web_verify_opcost_housing:24,139 |
| 4.08 C1 每次退房清潔「向房客收的清潔費」 | 50 | 65(房東自己打掃) | 105(大房、找清潔公司) | AUD/次 | 文章日期 2026-11-13 | 全澳(沒分雪梨) | Hospitable | https://hospitable.com/airbnb-cleaning-fee-australia | 商業網站(短租軟體商部落格) | ⚠️ | 數字與日期吻合;「低 50」是頁面「平均 $50–$80」的下緣、不是獨立低檔,高 105 超出該平均區間;幣別頁面沒明寫(AUD 為推定);是向房客收的行情,不是房東實際付給清潔人員的成本。 | web_opcost_housing:35,43;web_verify_opcost_housing:25,133,147 |
| 4.09 M1 短租代管公司抽成(全澳範圍,多數落點) | 15 | 20–22 | 25 | % 租金收入 | 2026-05 更新(Updated May 11, 2026) | 全澳(文內沒單獨列雪梨) | Houst | https://www.houst.com/blog/airbnb-hosting-fees-australia | 商業網站(代管商) | ✅ | 吻合(typically 15% to 25% of rental income,most 20-22%);是代管商自己的行銷文,頁面提到 Houst 在 Sydney 有服務但費率沒有單獨列雪梨;抽成基礎不一(總收入或扣費後淨額),填抽成前要先確認。 | web_opcost_housing:38,45;web_verify_opcost_housing:27,132 |
| 4.10 M3 澳洲共同房東(co-host)抽成 | 10–15(只負責溝通) | 20(最常見) | 25(頁面為 full-service 的 25%+) | % 總訂房收入 | 2026(文章 2026-03-16) | 全澳 | Rakidzich | https://www.rakidzich.com/articles/airbnb-co-hosting-australia | 部落格(搜尋摘要) | ⚠️ | 查核更正:原寫「高 25」當上限;頁面 25% 是 full-service 的下限(25%+)、不是上限,頁面 FAQ 又寫 20–25%,前後不一致;低、中、基礎(gross booking revenue)吻合(見 7.45)。 | web_opcost_housing:40;web_verify_opcost_housing:29,145 |
| 4.11 S1(原)公寓管理費(strata levies),典型公寓 | — | 854 | — | AUD/季 | 約 2025–2026(研究檔:白皮書日期沒確認);查核員:資料 2019 至 2026 年初 | NSW(頁面句子稱 Sydney (NSW)) | Microburbs | https://www.microburbs.com.au/research/strata-levies-whitepaper | 商業網站(資料公司;搜尋摘要) | ⚠️ | 查核更正:原寫地理範圍 Sydney;表格標 NSW(24,064 筆、854/季、年化 3,416)、句子標 Sydney (NSW),頁面沒說是否只含雪梨;數字與單位吻合(854×4=3,416 與頁面年化吻合);簡報寫「NSW(頁面句子稱 Sydney (NSW))」,不要寫成雪梨公寓;S6 兩房 1,500–3,000/季要一起看。 | web_opcost_housing:52,61;web_verify_opcost_housing:30,115,143 |
| 4.12 S2 中位價公寓管理費(估計值) | — | 約 850 | — | AUD/季 | 日期沒確認 | Sydney | Flat Chat 論壇 | https://www.flatchat.com.au/topic/how-do-you-guesstimate-levies/ | 部落格/論壇(搜尋摘要) | 未查 | 未經獨立查核:查核員沒重開論壇頁(工具次數用完),仍是搜尋摘要狀態。【晚上補查 2026-11-14】Chrome 開到原帖(網址轉到 flatchat.com.au/flat-chat-forum/topic/how-do-you-guesstimate-levies/):約 850/季是站長 2024-06-09 自己快查估的(房價約 85 萬、每年約 0.4%),沒附來源,不是統計。 | web_opcost_housing:53;web_verify_opcost_housing:31,153 |
| 4.13 S3 管理費:小棟、無電梯 | 600 | — | 1,200 | AUD/季 | 日期沒確認 | NSW | Stratachecks | https://stratachecks.com.au/blog/beginners-guide-strata-levies | 商業網站(搜尋摘要) | ✅ | 吻合(Small building,6–12 lots,No lift);頁面標明是 NSW 粗略參考,沒有雪梨細分。 | web_opcost_housing:54;web_verify_opcost_housing:32,134 |
| 4.14 S4 管理費:中型、有電梯 | 1,000 | — | 2,500 | AUD/季 | 日期沒確認 | NSW | Stratachecks | https://stratachecks.com.au/blog/beginners-guide-strata-levies | 商業網站(搜尋摘要) | ✅ | 吻合(Mid-size,30–60 lots,With lift)。 | web_opcost_housing:55;web_verify_opcost_housing:33,134 |
| 4.15 S5 管理費:大型、設施齊全(泳池/健身房) | 1,500 | — | 4,000 以上 | AUD/季 | 日期沒確認 | NSW | Stratachecks | https://stratachecks.com.au/blog/beginners-guide-strata-levies | 商業網站(搜尋摘要) | ✅ | 吻合(Large,100+ lots,Full amenities,$1,500–$4,000+)。 | web_opcost_housing:56;web_verify_opcost_housing:34,134 |
| 4.16 S6 管理費:標準兩房公寓 | 1,500 | — | 3,000 | AUD/季(查核員確認每季) | 2026 | Sydney | SavingsMate | https://savingsmate.com.au/blog/strata-fees-explained-australia | 商業網站(搜尋摘要) | ✅ | 查核更正:原寫「單位沒寫清楚(推測每季)」,頁面確認是每季(average quarterly strata fees: Sydney $1,500 to $3,000 for a standard two-bedroom apartment,2026 粗估;豪華大樓可超過 $5,000/季);此值是 S1 的約 1.8–3.5 倍,研究檔「不採用」的理由(單位不明)已不成立,剩下的理由只有「兩房、粗估」。 | web_opcost_housing:57,61;web_verify_opcost_housing:35,119,143 |
| 4.17 S1b(補)公寓管理費(strata)典型值(確認上一份 S1) | — | 854 | — | AUD/季 | 2026(白皮書年份;分析 2019 至 2026 年初的房源描述) | NSW(表格標 NSW、句子標 Sydney (NSW),頁面沒說是否只含雪梨) | Microburbs strata levies whitepaper | https://www.microburbs.com.au/research/strata-levies-whitepaper | 商業網站(資料公司) | ⚠️ | 查核更正:補查檔寫「NSW 全州,不是只有雪梨」比頁面說得更肯定,頁面 doesn't say whether the table figure covers only Sydney or the whole state;數值、樣本數吻合(全澳 49,234 筆、19,270 棟、NSW 24,064);建議寫「NSW(頁面句子稱 Sydney (NSW))」。 | web_opcost_housing_gapfill:55,61;web_verify_opcost_housing:68,115,143 |
| 4.18 W1(補)水:供水固定費(有水表) | — | 26.65(2025-26 為 29.73) | — | AUD/季(最大值,以 92 天季計) | 2026-27(2026-07-01 至 2027-06-30) | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | ✅ | 吻合(Water service (metered) $26.65 per quarter (maximum));括號內 2025-26 的 29.73 查核員摘要沒顯示、沒驗;固定費是最長季(92 天)上限,要寫「最多」;原網址 301 轉址到 sydneywater.com.au/residential/accounts-billing/residential-pricing.html。 | web_opcost_housing_gapfill:33,45;web_verify_opcost_housing:58,127 |
| 4.19 W2(補)水:污水處理固定費 | — | 189.88(2025-26 為 174.40) | — | AUD/季(最大值) | 2026-27 | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | ✅ | 吻合(Wastewater service $189.88 per quarter (maximum));174.40 舊價沒驗。 | web_opcost_housing_gapfill:34;web_verify_opcost_housing:59 |
| 4.20 W3(補)水:雨水排水費(公寓/低衝擊) | — | 9.67(獨棟屋 30.26) | — | AUD/季(最大值,只在雨水排水區才收) | 2026-27 | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | ✅ | 吻合(Stormwater, houses $30.26;units or low-impact $9.67 per quarter)。 | web_opcost_housing_gapfill:35;web_verify_opcost_housing:60 |
| 4.21 W4(補)水:用水量單價 | — | 3.41(2025-10 至 2026-06 為 3.17) | — | AUD/千公升(kL) | 2026-07-01 至 2027-06-30 | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | ✅ | 吻合(Drinking water usage $3.41 per kilolitre);3.17 舊價沒驗。 | web_opcost_housing_gapfill:36;web_verify_opcost_housing:61 |
| 4.22 W5(補)水:乾旱費率用水單價 | — | 3.84 | — | AUD/kL | 水庫低於 60% 時才適用,回升到 70% 以上取消 | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | ✅ | 吻合(Drought drinking water usage $3.84 per kilolitre;Greater Sydney 水庫低於 60% 適用、回升超過 70% 取消)。 | web_opcost_housing_gapfill:37;web_verify_opcost_housing:62 |
| 4.23 W6(補)水:官方給的典型季帳單(獨棟屋,用水 50 kL,供水+污水,92 天) | — | 387.03 | — | AUD/季 | 2026-27 | Sydney Water 服務範圍 | Sydney Water | https://www.sydneywater.com.au/accounts-billing/paying-your-bill/our-prices/residential-pricing.html | 官方 | ✅ | 吻合(Typical house bill (50 kL) $387.03 per 92-day quarter);不含雨水費。 | web_opcost_housing_gapfill:38;web_verify_opcost_housing:63,82 |
| 4.24 W7(補)水:公寓(有水表)用水 50 kL/季的季帳單(換算) | — | 396.70 | — | AUD/季 | 2026-27 | Sydney Water 服務範圍 | 研究檔自己算(換算;用到的數字來自 Sydney Water 官方頁) | 原檔沒寫(換算列,無網址;數字來自 4.18–4.22 同一官方頁) | 換算 | ✅ | 查核員重算:26.65 + 189.88 + 9.67 + 50 × 3.41(=170.50)= 396.70,算式正確;前提是有水表、位於雨水排水區、用水 50 kL(官方獨棟典型量,小公寓可能遠少,請使用者自填);4 季粗乘約 1,587 AUD/年(最長季乘 4,粗略);大樓水費若已含在管理費,不要重複計入。 | web_opcost_housing_gapfill:39,46,47;web_verify_opcost_housing:64,77–85 |
| 4.25 G1(補)瓦斯:NSW 家戶年均 | 730 | 964(241/季 × 4,研究檔換算) | 1,320 | AUD/年 | 日期多數沒標(2026 搜尋結果) | NSW(非雪梨專屬) | Mozo 引 Finder(730);Finder 州別表(241/季);Energy Plans(1,320) | https://www.mozo.com.au/best/energy/gas.html ; https://www.finder.com.au/energy/gas-nsw ; https://www.energyplans.com.au/average-gas-bill-australia | 商業網站(比價站;搜尋摘要) | 未查 | 未經獨立查核:查核員工具次數用完、沒開頁;三個數字差距大(730 對 1,320),來源是比價站、方法不同、日期沒標,只能當粗略帶狀、不能當中位;研究檔說沒有 AER 或政府的雪梨瓦斯年均帳單。 | web_opcost_housing_gapfill:40,48;web_verify_opcost_housing:65,153 |
| 4.26 N1(補)網路:NBN 50 一般方案月費 | 50(Mozo 最便宜無限量,NSW) | 約 86(Canstar 2026 全速率平均月帳單) | 100(Canstar 區間上限;Telstra NBN 50 為 99、Optus 97,2026-07 漲價後) | AUD/月 | 2026(7 月起 NBN 批發價上調) | 全澳,Mozo 列表為 NSW | Canstar、Mozo、Finder | https://www.canstar.com.au/internet/average-internet-bill/ ; https://www.mozo.com.au/broadband.html ; https://www.finder.com.au/news/optus-telstra-nbn-price-hikes-locked-in-for-july-2026 | 商業網站(比價站;搜尋摘要) | 未查 | 未經獨立查核:查核員工具次數用完、沒開頁;「低」是促銷或最便宜無限量方案,不一定是長期價;研究檔已排除聯盟行銷/SEO 頁的數字。 | web_opcost_housing_gapfill:41,49;web_verify_opcost_housing:66,153 |
| 4.27 N2(補)網路:NBN 100 方案月費 | 70(Mozo 最便宜無限量) | — | 110(Canstar 區間上限;Telstra/Optus 同為 99) | AUD/月 | 2026 | 全澳,Mozo 列表為 NSW | Canstar、Mozo、Finder | https://www.canstar.com.au/internet/average-internet-bill/ ; https://www.mozo.com.au/broadband.html ; https://www.finder.com.au/news/optus-telstra-nbn-price-hikes-locked-in-for-july-2026 | 商業網站(比價站;搜尋摘要) | 未查 | 未經獨立查核:查核員工具次數用完、沒開頁;同 4.26 的促銷價提醒。 | web_opcost_housing_gapfill:42,49;web_verify_opcost_housing:67,153 |
| 4.28 R1(補)市政費(council rates):North Sydney 住宅最低費率(minimum rate) | — | 970.72(2027-28 核准 1,116.32;2028-29 為 1,216.79) | — | AUD/年 | 2026-27 | North Sydney 市政區 | IPART「Minimum Rates Instrument 2026-27 North Sydney Council」 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Minimum-Rates-Instrument-2026-27-North-Sydney-Council.PDF | 官方(NSW 州政府機構;搜尋摘要) | 未查 | 未經獨立查核:查核員沒重開 IPART PDF;這是「最低費率」(下限概念),不是雪梨一般公寓的典型年度市政費;City of Sydney、Inner West 等官方頁沒開。 | web_opcost_housing_gapfill:56,62,90;web_verify_opcost_housing:69,153 |
| 4.29 R2(補)市政費:Blacktown 住宅最低費率與平均住宅費 | 1,140(最低費率) | 1,233(平均住宅費) | — | AUD/年 | 年度摘要沒寫清 | Blacktown(雪梨西部) | Blacktown 市政廳 Special Rate Variation 說明(放在 IPART 資料庫) | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Blacktown-City-Council-Attachment-Other-Attachment-2.5-Special-Rate-Variation-FAQs-and-Factsheets.PDF | 官方(轉述;搜尋摘要) | 未查 | 未經獨立查核:查核員沒重開 PDF;1,233 是平均住宅費(不分房型、年度不明);R1/R2 都不是雪梨一般公寓的典型值,只能顯示量級約 1,000–1,250 AUD/年。 | web_opcost_housing_gapfill:57,62;web_verify_opcost_housing:70,153 |
| 4.30 I1(補)房東/短租專用保險 | 500 | — | 700 | AUD/年 | 2026 | 全澳(沒分雪梨,沒分房型) | Rakidzich(短租代管商部落格) | https://www.rakidzich.com/articles/airbnb-insurance-australia | 商業網站(代管商行銷文;搜尋摘要) | 未查 | 未經獨立查核:查核員沒開頁(工具次數用完);廠商行銷文的單一區間,不是保險公司公布費率;一般房東保險常不涵蓋短租,要問保險公司。 | web_opcost_housing_gapfill:58,63;web_verify_opcost_housing:71,153 |

(M2 Houst「雪梨/墨爾本代管抽成 15–22%」web_opcost_housing:39 查核為 ❌,頁面查不到,不放主表,見 7.02。)

## 5. 房市(租金、空置率、房價、利率)

說明:租金、空置率、房價、利率四種各列各的期間與供應商,不同供應商(Cotality / SQM / Domain)口徑與區域不同,同一供應商的趨勢才可比較,不要跨家直接比(研究檔註)。2026 年房價下跌、利率連升五次,引用務必帶日期。

| 項目 | 低 | 中或單一值 | 高 | 單位 | 資料期間 | 地理範圍 | 來源名稱 | 網址 | 來源類型 | 查核判定 | 簡報加註 | 出處 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5.01 L1(原)獨棟屋租金中位數 | — | 835(單季 −5,約 −0.6%) | — | AUD/週 | 2026 年 9 月季 | Sydney(Domain 的雪梨首都圈口徑) | Domain(經 Time Out 轉述) | https://www.timeout.com/australia/news/australias-rental-market-has-officially-stalled-despite-capital-city-shortages-100726 | 產業報告(轉述) | ✅ | 吻合(fell 0.6 per cent ($5) to $835 per week,歸屬 Domain September Quarter 2026);頁面沒寫是 median,Elite Agent 那頁寫 median asking(開價中位);簡報標「開價中位」。 | web_opcost_housing:67;web_verify_opcost_housing:36,130 |
| 5.02 L2(補)公寓(unit)租金中位數(補上一份 L2) | — | 780(「持平」) | — | AUD/週 | 2026 年 9 月季 | Sydney(文內該段是雪梨段落,但這句沒重複寫 Sydney) | Domain 2026 年 9 月季租金報告(經 Elite Agent 2026-10-08 文章轉述) | https://eliteagent.com/why-australian-rents-stall-despite-record-low-vacancies/ | 產業報告(轉述) | ⚠️ | 數字吻合(Sydney unit rent $780 a week, remained steady);地理靠上下文判斷、句子沒寫 Sydney;是第二手轉述、Domain 原頁沒開到;是「開價中位」(median asking);Time Out 那頁沒有雪梨公寓值。 | web_opcost_housing_gapfill:17,24;web_verify_opcost_housing:53,140 |
| 5.03 L1b(補)獨棟屋租金中位數(交叉對照上一份 L1) | — | 835 | — | AUD/週 | 2026 年 9 月季 | Sydney | Domain 2026 年 9 月季租金報告(經 Elite Agent 2026-10-08 文章轉述) | https://eliteagent.com/why-australian-rents-stall-despite-record-low-vacancies/ | 產業報告(轉述) | ✅ | 吻合(Sydney house rent $835 a week, down 0.6% ($5)),與 5.01 一致。 | web_opcost_housing_gapfill:18,25;web_verify_opcost_housing:54 |
| 5.04 L3 公寓租金中位數(較舊) | — | 750(年增 4.9%) | — | AUD/週 | 2025 年 9 月季 | Sydney | Domain September 2025 rental report | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ | 產業報告(搜尋摘要) | ⏸ | 未經獨立查核:Domain 頁 WebFetch 回 403、Chrome 未試;待原頁,補查前不要用(見 7.35)。 | web_opcost_housing:69;web_verify_opcost_housing:37,152 |
| 5.05 L4 獨棟屋租金中位數(較舊) | — | 780 | — | AUD/週 | 2025 年 9 月季 | Sydney | Domain September 2025 rental report | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ | 產業報告(搜尋摘要) | ⏸ | 未經獨立查核:同 5.04,頁面 403;待原頁(見 7.36)。 | web_opcost_housing:70;web_verify_opcost_housing:38,152 |
| 5.06 L5 公寓租金(較新但可信度低) | — | 780 | — | AUD/週 | 2026 年 6 月季 | Sydney | 某新聞報導引用(Domain 口徑)The New Daily | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices | 商業網站(新聞;搜尋摘要,頁面 403) | 未查 | 未經獨立查核:The New Daily 原檔已記 403,查核員沒重試;旁證:Elite Agent 說 9 月季公寓 780 steady,方向一致但不是同一頁;研究檔註明 L5/L6 不當預設值,只供旁證(見 7.38)。【晚上補查 2026-11-14】Chrome 開到 The New Daily 原頁:雪梨只寫「fell $5 to $835」,沒分公寓或獨棟,頁上沒有 780;這一列不要再當這頁的數字引用。 | web_opcost_housing:71,82;web_verify_opcost_housing:39,152 |
| 5.07 L6 獨棟屋租金(較新但可信度低) | — | 850 | — | AUD/週 | 2026 年 6 月季 | Sydney | 某新聞報導引用(Domain 口徑)The New Daily | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices | 商業網站(新聞;搜尋摘要) | 未查 | 未經獨立查核:查核員沒開;已開的 Time Out、Elite Agent 兩頁都寫 9 月季「−$5 到 835」,代表 6 月季應為 840、不是 850,L6 與已驗證頁面矛盾,應視為轉述有誤,不要用(見 7.34)。【晚上補查 2026-11-14】Chrome 開到 The New Daily 原頁:雪梨只寫「fell $5 to $835」,沒分公寓或獨棟,頁上沒有 850;不要引用。 | web_opcost_housing:72,82;web_verify_opcost_housing:40,118,151 |
| 5.08 L7 租金季變動 | — | −0.4 | — | % 單季 | 2026 年 9 月季 | Sydney | Cotality(經 The Nightly) | https://thenightly.com.au/australia/nsw/sydney-rents-fall-despite-fears-of-a-post-budget-spike-c-22990976 | 產業報告(轉述) | ✅ | 吻合(Sydney rents fell 0.4 per cent in the September quarter,Cotality,10/9 報導)。 | web_opcost_housing:77;web_verify_opcost_housing:45,131 |
| 5.09 V1 空置率 | — | 2.5(去年同期 1.8) | — | % | 2026 年 9 月季 | Sydney | Cotality(經 The Nightly) | https://thenightly.com.au/australia/nsw/sydney-rents-fall-despite-fears-of-a-post-budget-spike-c-22990976 | 產業報告(轉述) | ⚠️ | 數字吻合;期間「9 月季」是推論(頁面該句沒標季別,同文有標 9 月季的是租金 −0.4%);三個供應商(Cotality 2.5、SQM 1.8、Domain 1.2)口徑不同,不要放同一條線;「去年同期 1.8%」與 5.10 的 1.8% 只是數字巧合相同。 | web_opcost_housing:73,80,81;web_verify_opcost_housing:41,144 |
| 5.10 V2 空置率 | — | 1.8 | — | % | 2026 年 9 月 | Sydney(口徑:SQM) | SQM Research(經 OpenAgent) | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 產業報告(轉述) | ✅ | 吻合(Sydney led the rise, with its vacancy rate climbing to 1.8 per cent,SQM Research,September)。 | web_opcost_housing:74;web_verify_opcost_housing:42,131 |
| 5.11 V3 空置率 | — | 0.9 | — | % | 2025 年 9 月季 | Sydney | Domain | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ | 產業報告(搜尋摘要) | ⏸ | 未經獨立查核:原頁 403 打不開;間接旁證:Elite Agent 說雪梨 9 月季 1.2%、「0.9% a year earlier」,與 V3 一致,仍待原頁(見 7.37)。 | web_opcost_housing:75;web_verify_opcost_housing:43,152 |
| 5.12 V4 空置率 | — | 1.1 | — | % | 2026 年 6 月季 | Sydney | 某新聞引用 Domain(The New Daily) | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices | 商業網站(搜尋摘要) | 未查 | 未經獨立查核:查核員沒開;間接旁證:Elite Agent 說「up from 1.1% in June」,仍待原頁(見 7.39)。【晚上補查 2026-11-14】Chrome 開到 The New Daily 原頁:頁上沒有空置率 1.1。 | web_opcost_housing:76;web_verify_opcost_housing:44,152 |
| 5.13 V5(補)空置率(雪梨,Domain 口徑) | — | 1.2(6 月季 1.1;去年同期 0.9) | — | % | 2026 年 9 月季 | Sydney | Domain(經 Elite Agent;研究檔原標搜尋摘要) | https://eliteagent.com/why-australian-rents-stall-despite-record-low-vacancies/ | 產業報告(轉述) | ✅ | 吻合(Sydney vacancy rate 1.2% in September, combined for houses and units;up from 1.1% in June and 0.9% a year earlier);查核員在 Elite Agent 頁讀到,可從「搜尋摘要」升級為已開頁(WebFetch);與 V3/V4 同為 Domain,趨勢 0.9→1.1→1.2 可比。 | web_opcost_housing_gapfill:19,26;web_verify_opcost_housing:55,121,131 |
| 5.14 P1 住宅價值中位數(公寓+獨棟合併) | — | 1,178,959(月 −1.6%,三個月 −4.7%,較 2 月高點低逾 10%) | — | AUD | 2026 年 10 月 | Sydney(頁面只寫 In Sydney) | Cotality(經 CommBank 新聞室) | https://www.commbank.com.au/articles/newsroom/2026/11/sydney-home-prices-fall-more-than-10-percent-from-peak.html | 產業報告(轉述) | ⚠️ | 查核更正:原寫 Greater Sydney,頁面沒寫、只寫 In Sydney,不要寫成 Greater Sydney;價位、月變動、較 2 月高點低逾 10% 吻合;「三個月 −4.7%」不在這頁、在 5.15 的 OpenAgent 頁;沒有房型拆分,不能代表公寓或獨棟。 | web_opcost_housing:90,99;web_verify_opcost_housing:46,141 |
| 5.15 P2 住宅價值中位數(交叉) | — | 1,178,959(查核員所見:月 −1.6%、季 −4.7%、年 −9.4%) | — | AUD | 2026 年 10 月 | Sydney(表內標籤只寫 Sydney) | Cotality(經 OpenAgent) | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 產業報告(轉述) | ⚠️ | 數字吻合;地理一樣沒有「Greater Sydney」字樣(原寫 Greater Sydney 口徑);三個月 −4.7% 在此頁。 | web_opcost_housing:91;web_verify_opcost_housing:47,141 |
| 5.16 P3(補)公寓價值中位數(unit) | — | 867,597(月 −1.0%,年 −3.8%) | — | AUD | 2026 年 9 月 | Sydney(Cotality,地理口徑摘要未寫清;疑為 Greater Sydney) | Cotality(經 OpenAgent,搜尋摘要轉述) | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 產業報告(轉述;搜尋摘要) | ⚠️ | 數字與期間(9 月)有第二來源旁證(搜尋摘要:月 −1.0%、季 −3.0%、年 −3.8%;ProperEasy 表格同值),但補查檔指定的 OpenAgent 頁面上查核員兩段都找不到 867,597;引用要換成 Cotality 原頁(discover.cotality.com 的 HVI SEP 2026 PDF);期間 2026-09 與 5.14 的 2026-10 不同月,不要互相推算(見 7.42)。【晚上補查 2026-11-14】Chrome 開到 OpenAgent 頁(Last updated Nov 4, 2026),全文沒有 867,597;頁上只有雪梨全部住宅中位 1,178,959(年 −9.4%);這個分項不要引用。 | web_opcost_housing_gapfill:20,27;web_verify_opcost_housing:56,142 |
| 5.17 P4(補)獨棟屋價值中位數(house) | — | 1,466,060(月 −1.6%,年 −8.2%) | — | AUD | 2026 年 9 月 | 同 5.16 | Cotality(經 OpenAgent,搜尋摘要轉述) | https://www.openagent.com.au/news/national-property-market-update-october-2026 | 產業報告(轉述;搜尋摘要) | ⚠️ | 同 5.16;查核員的搜尋摘要為 $1,466,060、月 −1.6%、季 −5.6%、年 −8.2%,另給 9 月全住宅中位 1,198,596(月 −1.4%);研究檔自己註明摘要與另一來源 8 月獨棟約 1,494,878 有出入、另有日期不明的「雪梨公寓約 120 萬」說法未採用(見 7.43)。【晚上補查 2026-11-14】Chrome 開到 OpenAgent 頁(Last updated Nov 4, 2026),全文沒有 1,466,060;頁上只有雪梨全部住宅中位 1,178,959(年 −9.4%);這個分項不要引用。 | web_opcost_housing_gapfill:21,27;web_verify_opcost_housing:57,142 |
| 5.18 B1(原)央行(RBA)現金利率目標 | — | 4.85(升 0.25 個百分點,前值 4.60;2026 年第 5 次升息) | — | % 年利率 | 2026-11-04 生效(2026-11-03 公布) | 全澳 | investinglive 等(搜尋摘要;RBA 的 SMP 頁也出現在搜尋結果) | https://investinglive.com/central-banks/more-rba-lifts-cash-rate-to-4-85-in-split-6-3-vote-sees-inflation-above-3-until-late-2027/ | 商業網站(轉述官方;搜尋摘要) | ⚠️ | 查核更正:原寫「2026-11-03 起」;RBA 頁面生效日是 11/4(11/3 是公布日),補查檔 5.19 正確;利率 4.85 與前值 4.60 吻合。 | web_opcost_housing:94,102;web_verify_opcost_housing:48,116 |
| 5.19 B1b(補)RBA 現金利率目標(確認上一份 B1) | — | 4.85(+0.25;前值 4.60) | — | % 年利率 | 2026-11-04 生效(2026-11-03 公布,頁面說調整於公布後隔日生效) | 全澳 | 澳洲央行 RBA「Cash Rate Target」頁 | https://www.rba.gov.au/statistics/cash-rate/ | 官方 | ✅ | 全部吻合;2026 年調整:2/4→3.85、3/18→4.10、5/6→4.35、6/17 與 8/12 維持 4.35、9/30→4.60、11/4→4.85,共 5 次升息;原檔 B1 的「11/3」是公布日。 | web_opcost_housing_gapfill:69,73;web_verify_opcost_housing:72,116,128 |
| 5.20 B2 新承作自住房貸平均利率(升息前估計,非投資客利率) | — | 約 6.75 | — | % 年利率 | 2026-11 升息前後的估計 | 全澳 | 搜尋摘要沒標明出處頁 | 原檔沒寫 | 不明(搜尋摘要,可信度低) | 未查 | 未經獨立查核:原檔就沒有出處頁、查核員無網址可查;研究檔自己標低可信度;不要用(見 7.40)。 | web_opcost_housing:95;web_verify_opcost_housing:49,153 |

## 6. 情境表(照抄研究檔與補查檔已算好的情境,附查核檔驗算結論;整理員沒有重算)

### 6(i) 一間 1 房公寓從空屋到可上架的開辦成本

研究檔提醒:下面加總只用表內的列,不含我們資料算出的值;三個情境口徑不同,「低」用非澳洲來源、可信度最低;預設放「中」,「高」情境有沒有翻新要做成可勾選項目,因為翻新金額是佈置金額的數倍,且沒有證據顯示翻新能帶來多少價差(web_reno_setup:118)。

#### 6(i)-A 原檔版本(web_reno_setup 第 7 節)

| 情境 | 加了哪幾列(括號 = 主表編號) | 研究檔寫的總和 | 查核員驗算 | 查核員指出的問題 | 出處 |
|---|---|---|---|---|---|
| 低(只佈置、不翻新、能省則省) | 小型 1 房家具套裝低標 2,000(Minoan,非澳洲;3.26)+ 專業攝影基本低標 250(Hometime;3.28)+ 智慧鎖最低零售 145(BuyWisely;3.33)+ 首次深度清潔 242(Maid for You;3.36);未含毛巾床單,因 Minoan 套裝是否含備品不明 | 約 2,637 AUD | 2,000 + 250 = 2,250;+ 145 = 2,395;+ 242 = 2,637 → 對 | 2,000 是 ⚠️(幣別頁面未標、國別未證實、無年份),145 是 ⏸(頁面打不開,無法確認),250 與 242 是 ✅;Minoan 與 BuyWisely 都沒有年份,與 2026 的 Hometime、Maid for You 混加;若 Minoan 真的非澳洲,就是把非澳洲的家具價加到澳洲的清潔與攝影價上(研究檔已自註可信度最低);不要當主數字,要用加註「含兩個未驗證加項」 | web_reno_setup:112;web_verify_reno_setup:71,83,87,103 |
| 中(只佈置、不翻新、用澳洲整包估算) | 1 房開辦合計 5,358(Airbtics,已含鎖、攝影機、毛巾枕頭毯、人工;3.21)+ 專業攝影標準低標 295(Hometime;3.29)+ 首次深度清潔 242(Maid for You;3.36);Airbtics 已含智慧鎖與備品,所以不再另加 | 約 5,895 AUD | 5,358 + 295 = 5,653;+ 242 = 5,895 → 對 | 三項全 ✅;但資料年份不同:Airbtics 是 2023-10 至 2024-09,Hometime 是 2026-09、Maid for You 是 2026-10,等於把約 2 年前的整包加上 2026 年報價;國家都是澳洲,沒有跨國混加;簡報加註「Airbtics 為 2023–24 資料,其餘為 2026 報價」 | web_reno_setup:114;web_verify_reno_setup:74,75,84,106 |
| 高(佈置 + 簡單翻新浴室與廚房) | 1 房開辦合計 5,358(Airbtics;3.21)+ 專業攝影高階低標 500(Hometime;3.30)+ 退租級大掃除 410(Maid for You;3.37)+ 浴室翻新「基本」典型值 17,250(What's The Damage,Sydney;3.01)+ 廚房「簡單換新」典型值 16,100(What's The Damage,Sydney;3.13) | 約 39,618 AUD;若只翻新浴室不動廚房約 23,518;若兩者都取該來源的高標 23,000,總額約 52,268 | 5,358 + 500 = 5,858;+ 410 = 6,268;+ 17,250 = 23,518;+ 16,100 = 39,618 → 對;只翻浴室 6,268 + 17,250 = 23,518 → 對;6,268 + 23,000 + 23,000 = 52,268 → 對 | 五項全 ✅,但:(1) 標籤:「高」稱「簡單翻新浴室」,用的 17,250 是 What's The Damage 的 Basic renovation(budget fittings,整間基本翻新),不是簡單更新(cosmetic refresh;Quote Yard 的簡單更新是 8,000–15,000,見 3.04),廚房 16,100 才是真的 cosmetic refresh,簡報請改稱「基本翻新(budget fittings)」;(2) 混了不同年份:Airbtics 2023–24 + 其他 2026;(3) GST 標示不一致:What's The Damage 兩項頁面明寫含 GST,Airbtics、Hometime、Maid for You 頁面沒寫含不含;(4) 範圍混:Airbtics 全澳,What's The Damage 與 Maid for You 是 Sydney | web_reno_setup:116;web_verify_reno_setup:77–80,85,86,105,106 |

#### 6(i)-B 補查後版本(web_reno_setup_gapfill 第 8 節;原檔不改)

| 情境 | 加了哪幾列(括號 = 主表編號) | 研究檔寫的總和 | 查核員驗算 | 查核員指出的問題 | 出處 |
|---|---|---|---|---|---|
| 低(研究檔:建議改,原 2,637 偏低) | 把原本非澳洲的 Minoan 2,000 換成澳洲來源 Hometime(2026-05)1 房開辦低標 5,000(3.79)+ 攝影基本低標 250(3.28)+ 智慧鎖最低零售 145(BuyWisely;3.33)+ 首次深度清潔 242(3.36) | 5,637 AUD;若 Hometime 的 5,000 已含鎖,扣掉 145 為 5,492。研究檔結論:澳洲來源下「低」不會比 5,000 多低 | 5,000 + 250 + 145 + 242 = 5,637 → 對;5,637 − 145 = 5,492 → 對 | 加總算式全對;Hometime 5,000 的細項(含不含鎖、攝影、備品)頁面沒列,頁面形容詞是 modest(簡樸/適中),不是研究檔寫的「寬裕」(見 3.79);145 仍是原檔查核的 ⏸(頁面 403,未驗證) | web_reno_setup_gapfill:100;web_verify_reno_gapfill:93–95,65,123;web_verify_reno_setup:48 |
| 中(研究檔:可不改,或換成 Hometime 範圍) | 原 5,895 可保留(Airbtics 5,358 落在 Hometime 2026 的 1 房區間 5,000–7,000 內);若改用較新來源,取 Hometime 範圍算術中點 6,000 + 攝影標準低標 295 + 深度清潔 242 | 6,537 AUD(與原 5,895 差約 640);研究檔建議保留 5,895、把 6,537 當上緣 | 6,000 + 295 + 242 = 6,537 → 對;6,537 − 5,895 = 642(研究檔寫約 640,對);5,358 落在 5,000–7,000 內 → 對 | 6,000 是研究檔取的算術中點、不是來源給的;Hometime 細項不明,不能與 Airbtics 5,358 逐項比 | web_reno_setup_gapfill:102;web_verify_reno_gapfill:95,106 |
| 高(研究檔:主體不改,可加兩個選項列) | 原 39,618 不改(hipages 沒取得,無法對照),可加:(a) 室內油漆(1 房各區加總 = 臥室 + 客餐廳 + 廚房牆 + 浴室:低 450 + 700 + 400 + 300、高 750 + 1,400 + 800 + 650;3.53/3.55/3.57/3.58)(b) 地板(40 m² hybrid,不含拆舊與踢腳板:低 63×40、典型 3,680、高 140×40;3.65/3.72) | 油漆 +1,850 至 +3,600;地板低 2,520、典型 3,680、高 5,600;兩項都加:43,988(低端)至 48,818(高端);另:鎖 228 換 Airtasker 中位數 276 只差 48,可忽略、不建議改 | 1,850 與 3,600 算式對;63 × 40 = 2,520、140 × 40 = 5,600、92 × 40 = 3,680 對;39,618 + 1,850 + 2,520 = 43,988 對;39,618 + 3,600 + 5,600 = 48,818 對 | 口徑提醒(不是算錯):(1) 同頁 At a Glance 表給 Sydney 臥室整間 $500–$900,研究檔用的 450–750 是正文另一句,若改用 500–900 加總為 1,900–3,750,簡報請寫「約 1,850–3,600」並標另有 500–900 一組;(2) 「客餐廳合併」與「廚房牆」若屋型是開放式客餐廚,應改用「開放式 1,500–2,500」,兩者不能同時加,否則重複計算;(3) GST 口徑不一致:地板含 GST(頁面明寫)、油漆頁沒寫,卻相加;(4) 地板 40 m² 是該頁範例面積、不是我們 1 房的實際坪數,要等比例調整;(5) 「成本近一年漲多少」要用 ABS 修正版(見 3.78);另 1 房油漆加總是研究檔作者自己加的、不含門與踢腳板;39,618 主體的標籤、年份、GST 問題見上一張表;研究檔建議油漆與地板做成可勾選選項列、預設不勾 | web_reno_setup_gapfill:32,104–110;web_verify_reno_gapfill:96–100,103–107,125 |

### 6(ii) 三種新房東的每月固定成本清單(只做加總,不做收益預測)

研究檔說明:每月固定成本與「跟營收/訂單連動」的變動成本分開看;下面「低/中/高」是研究檔從表格挑的(取法寫在欄內);沒查到的列,試算工具請預設為空白或讓使用者自填(web_opcost_housing:117–118)。查核員確認:沒有把每週、每季、每年直接相加(每週租金先 ×52÷12、每季管理費先 ÷3、每年電費先 ÷12;web_verify_opcost_housing:106)。

共通變動項目(三種人都有,不是固定月成本;web_opcost_housing:119–124):平台抽成 F1 15.5%(訂房小計;2.13);清潔 C1 每次退房 50 / 65 / 105 AUD(向房客收的費行情;4.08)× 每月退房次數(使用者自填);代管/共同房東抽成(若有)15% / 20% / 25% 的收入(4.09;共同房東溝通型 10–15%,4.10);床單洗滌 C2 查不到,自填(見 8.14)。

#### 甲、已有房(自有房,貸款或已還清;web_opcost_housing:125–131)

| 列 | 低 | 中 | 高 | 取法(研究檔) | 查核員驗算(web_verify_opcost_housing:87–111) |
|---|---|---|---|---|---|
| 電費(AUD/月,年 ÷ 12) | 約 156 | 約 164 | 約 201 | 低 = E2 Ausgrid 2026-27 草案 1,875;中 = E1 Ausgrid 2025-26 1,965;高 = E3 Endeavour 2025-26 2,411;三個數字不同年度或供電區,只是粗略帶狀 | 1,875 ÷ 12 = 156.25;1,965 ÷ 12 = 163.75;2,411 ÷ 12 = 200.92 → 約 156 / 164 / 201,對 |
| 管理費(AUD/月,季 ÷ 3) | 200 | 約 285 | 500 | 低 = S3 下限 600/季;中 = S1 854/季;高 = S5 下限 1,500/季(大樓或設施多);獨棟屋此列為 0 | 600 ÷ 3 = 200;854 ÷ 3 = 284.67;1,500 ÷ 3 = 500 → 對 |
| 水、瓦斯、網路、市政費、保險 | 空 | 空 | 空 | 原檔查不到,三欄皆空(補查檔後來有候選值,見 4.18–4.30,但原檔加總沒有更新) | 查核員:這兩列加總是「只含兩列」的下限,不是完整月成本 |
| 已有的列加總(只含電費 + 管理費) | 約 356 | 約 449 | 約 701 | 若有房貸,貸款月付由使用者自填(見丙) | 低 156.25 + 200 = 356.25 → 約 356 對;中 163.75 + 284.67 = 448.42 → 研究檔寫約 449,差 1 元是先四捨五入再加(164 + 285 = 449),精確值約 448(⚠️ 無實質影響);高 200.92 + 500 = 700.92 → 約 701 對 |

查核員口徑提醒(不是算錯):電費三檔混了供電區與年度(原檔有註明);管理費低(S3 下限 600)、高(S5 下限 1,500)是不同樓型的下限,中位 854 是 NSW 表(見 4.11/4.17)。

#### 乙、二房東(租來再轉短租;web_opcost_housing:132–141)

| 列 | 數字 | 取法(研究檔) | 查核員驗算(web_verify_opcost_housing:101–104) |
|---|---|---|---|
| 租金:獨棟屋 L1 835/週(2026 年 9 月季) | 約 3,618 AUD/月 | 週租 × 52 ÷ 12 | 835 × 52 = 43,420;÷ 12 = 3,618.33 → 約 3,618,對 |
| 租金:公寓 L3 750/週(2025 年 9 月季,舊一年) | 3,250 AUD/月 | 同上 | 750 × 52 = 39,000;÷ 12 = 3,250 → 對(輸入 L3 的原頁是 ⏸,見 5.04) |
| 租金:公寓 L5 780/週(2026 年 6 月季,可信度低) | 3,380 AUD/月 | 同上 | 780 × 52 = 40,560;÷ 12 = 3,380 → 對(輸入 L5 查核為未查,見 5.06) |
| 電費 | 約 156 / 164 / 201 AUD/月 | 同甲 | 同甲 |
| 水、瓦斯、網路、保險 | 查不到(原檔) | 房東保險不需要,租客/短租責任險查不到;通常沒有管理費與市政費,視租約由使用者填 | — |
| 範例加總:公寓 750/週 + 電費 156–201 | 約 3,406–3,451 AUD/月 | 研究檔註:每個數字期間不同,僅示範算法;三個租金期間或口徑不同,不併成低/中/高,請在預設值旁標日期 | 3,250 + 156.25 = 3,406.25;3,250 + 200.92 = 3,450.92 → 對 |

補查檔另有 L2 公寓 780/週(2026 年 9 月季,5.02,⚠️);總表沒有把它換算成每月(整理員不重算)。

#### 丙、想買房(新購置;web_opcost_housing:143–150)

| 列 | 內容 | 查核員驗算(web_verify_opcost_housing:105) |
|---|---|---|
| 買價參考 | P1 住宅價值中位數 1,178,959 AUD(公寓與獨棟合併,2026-10;5.14);公寓/獨棟分開的中位價原檔沒查到(補查檔 P3/P4 另有 867,597 / 1,466,060,2026-09,⚠️,見 5.16/5.17) | P1 查核 ⚠️(頁面只寫 Sydney,見 5.14) |
| 利率參考 | RBA 現金利率 4.85%(B1;5.18/5.19);房貸實際利率比它高,新承作自住房貸平均約 6.75%(B2,低可信度估計;5.20);投資客利率沒查到(8.17) | B2 查核為未查(無出處頁) |
| 利息換算(純算術) | 每借 100 萬 AUD、每 1 個百分點年利率,只付息的利息約 833 AUD/月;實際貸款額、利率、是否還本都由使用者填 | 1,000,000 × 1% = 10,000/年;÷ 12 = 833.33 → 約 833,對 |
| 管理費、電費 | 同甲 | 同甲 |
| 土地稅 | 起徵點見 T1(1,075,000 土地價值,2.14);是否適用、金額取決於土地價值,本檔不試算 | T1 查核 ✅ |
| 水、瓦斯、網路、市政費、保險 | 查不到(原檔) | — |

### 6(iii) 短租市場的入住率、每晚價格低/中/高建議值

研究檔提醒(web_str_market:102–116):三組值全部是外部商業網站估計,不是我們資料算出來的,也不是政府統計;使用前要在試算工具的假設欄標示來源。三組入住率分母不同,情境間的差距主要是「定義差」,不是同一市場在不同狀況下的差;年收入都是營收,未扣平台費 15.5%、清潔費、管理費、水電、稅;AirDNA 的 ADR 193 與年收入 40.8K 沒列進情境(幣別未標)。

| 情境 | 入住率 | 入住率取自 | 每晚價格(ADR) | 每晚價格取自 | 查核員加註(web_verify_str_market:85–96) |
|---|---|---|---|---|---|
| 低 | 50% | AirROI 49.5%(2025-11 至 2026-10,Sydney;1.09) | AUD 280 | Airbtics 中位數 281(2025-09 至 2026-09,Sydney;1.22) | 入住率 ✅:取自該列、四捨五入,分母是「開放天數」;ADR ✅:取自該列;注意低情境把 AirROI 的入住率配 Airbtics 的 ADR,是跨來源混搭 |
| 中 | 67% | AirDNA 67%(2025-10 至 2026-10;1.03);GuestFavorites 68% 也接近(1.18) | AUD 336 | GuestFavorites 336(2025-11 至 2026-10;1.17);研究檔寫也與我們掛牌價中位數 338 接近 | 入住率 ✅(AirDNA 67%、GF 68%);ADR ⚠️:取自該列,但範圍是 Greater Sydney;「338」是內部資料,查核員本次未查 |
| 高 | 75% | Airbtics 中位數 75%(僅含高評分房源,2025-09 至 2026-09;1.21) | AUD 399 | AirROI 399(2025-11 至 2026-10;1.08) | 入住率 ⚠️:數字取自該列,但括號裡的樣本描述不準確(實際是「有評分且近 12 個月活躍 ≥90 天」,不是高評分),簡報註解同步改;ADR ✅:取自該列 |

年收入交叉檢查(研究檔用上面數字乘出來的,不是來源直接給的;web_str_market:114):低 ≈ 280 × 50% × 365 ≈ AUD 51,100(與 AirROI 平均年收入 52,495 接近);中 ≈ 336 × 67% × 365 ≈ AUD 82,200(與 GuestFavorites 83,094 接近);高 ≈ 399 × 75% × 365 ≈ AUD 109,200(高於所有來源的年收入,屬上界,偏樂觀)。查核員重算(web_verify_str_market:96):280×50%×365 = 51,100;336×67%×365 = 82,171(筆記寫 82,200);399×75%×365 = 109,226(筆記寫 109,200);三個乘積無誤。

研究檔另提醒(web_str_market:113):要做真正的低/中/高,建議低情境再套用 180 天上限(只有非房東同住房源適用):180 / 365 = 49.3% 最高入住率,與 AirROI 49.5% 巧合接近、意義不同(此算式查核檔沒涵蓋)。

## 7. 不採用或要小心的數字

「是否在主表」欄:7.01 與 7.02 不放主表(規則 b);其餘主表也有該列,主表加註已寫差異,這裡集中列出供簡報時避開。

| 項目 | 原寫的值 | 為什麼不用 | 是否在主表 | 出處 |
|---|---|---|---|---|
| 7.01 BnbCalc 較小區域供給年變化 | -10%、8,379 間(Sydney、Bondi Beach、Manly、Parramatta 合計,2026-05 對前一年;搜尋摘要,研究檔沒讀原頁) | ❌ 查核員在現行頁面看不到這些數字:頁面寫 Sydney 整個市場 12 個月至 2026-09 平均 9,083 間(標題 9.3K、結構化資料 9,316)、年增 +4%、兩年 +13%,沒有 -10%、8,379、2026-05,也沒有四區合計;方向與 AirDNA/AirROI 相反;頁面自己的 ADR/入住率也自相矛盾(369/51% 對 361/58%) | 否 | web_str_market:95;web_verify_str_market:80,118 |
| 7.02 Houst 雪梨/墨爾本代管抽成(M2) | 15–22%(原檔 M2;搜尋摘要;研究檔註「上限比 M1 低 3 個百分點」) | ❌ 該頁(Updated Oct 21, 2026)沒有「15% 到 22%」、也沒出現 22%,只有「Houst starts from 12% in London, Paris and Dubai and from 14% in its other locations」;可能來自搜尋摘要誤抄;研究檔的 M1/M2 差距推論跟著站不住(兩者其實沒有衝突) | 否 | web_opcost_housing:39,44;web_verify_opcost_housing:28,120,150 |
| 7.03 AirDNA 年變化裡的「營收 +99.1%」 | +99.1% | 研究檔判斷與 RevPAR +3.3% 難以並存、可能是定義或樣本變動而不採用;查核員確認頁面確實寫了 +99.1%,不採用的處理合理 | 是(1.06) | web_str_market:21;web_verify_str_market:18 |
| 7.04 AirDNA 活躍房源年變化 -42.0% | -42.0%(2025-09 → 2026-09) | 只出現在研究檔轉述的搜尋摘要,查核員在頁面看不到;採用頁面的 -36.8%(1.34) | 否(只在 1.34 加註) | web_str_market:93;web_verify_str_market:78,119 |
| 7.05 AirDNA ADR $193、年收入 $40.8K | $193/晚;$40.8K/年 | 頁面只有「$」沒標幣別,年收入含清潔費與其他房客費用;不要與 AUD 數字直接比,引用要加註「幣別未標」;研究檔也沒把它們列進三個情境 | 是(1.02、1.04) | web_str_market:116,17,19;web_verify_str_market:109 |
| 7.06 Airbtics 2025 全澳營收(及全澳組數字) | 62.2% / AUD 317 / AUD 71,770 | 頁面只有「$」(AUD 是推定);同頁全澳 2024 為 $45,174、「營收變化 4.52%」,兩者對不上,全澳營收可信度低、不要用 | 是(1.25) | web_str_market:40;web_verify_str_market:37,112 |
| 7.07 Airbtics 13,174 / 75% 的「僅含高評分房源」說法 | 僅納入較高評分房源 | 頁面查不到此說法;實際是「有評分且近 12 個月活躍 ≥90 天」;改寫成該說法,高情境 75% 的註解同步改 | 是(1.20、1.21) | web_str_market:35,110;web_verify_str_market:32,93,111 |
| 7.08 GuestFavorites 年收入 83,094 標成「平均」 | AUD 83,094(平均) | 頁面自己同時把它叫作平均與中位數;不要標成其中一個;全組範圍是 Greater Sydney | 是(1.19) | web_str_market:34;web_verify_str_market:31,110 |
| 7.09 Hometime 典型年收入範圍 | AUD 50,800–97,700(期間未標) | 無期間、無來源、頁面只有「$」;若用請寫「Hometime 文章稱」,不要標 AUD | 是(1.27) | web_str_market:42;web_verify_str_market:39,113 |
| 7.10 Hometime「最淡 5–6 月」寫成價格最淡 | 價格最淡 5–6 月 | 頁面是需求最軟、不是價格最淡;改寫「5–6 月需求最軟」 | 是(1.33) | web_str_market:59;web_verify_str_market:50,114 |
| 7.11 AirDNA 季節性分數 91 的解讀 | 91/100 | 不要解讀成「淡旺季不明顯」:它量最低與最高月營收的差距,與 AirROI 12 月約為 6 月 1.6 倍並存 | 是(1.32) | web_str_market:58,61;web_verify_str_market:49,117 |
| 7.12 「強制登記」措辭 | 政府營運的強制登記 | 頁面沒標 register 為 mandatory(只有行為準則標 mandatory);簡報改寫「政府營運登記制度」,或另找官方頁佐證「強制」 | 是(2.04) | web_str_market:70;web_verify_str_market:59,116 |
| 7.13 「供給方向一致減少」的說法 | 各家商業來源對 2026 年的方向一致是「減少」,幅度 10%–37% | 查核員:AirDNA -36.8%、AirROI -22% 是減少;Airbtics 2025 是 +28.88%;BnbCalc 現行頁是 +4%(見 7.01);期間與口徑不同,只能並列 | 是(1.34–1.36) | web_str_market:100;web_verify_str_market:80,120 |
| 7.14 City of Sydney 市議會動議 | 2026-04-28 動議 | 未查:二手報導、非官方,查核員未開啟,不要用於簡報 | 是(2.07) | web_str_market:73;web_verify_str_market:62,119 |
| 7.15 City of Sydney 登記狀況 | 5,454 間活躍短租、2,468 間有登記 | 未查:研究檔自己標為搜尋摘要,查核員未開啟,不要用於簡報 | 是(1.37) | web_str_market:97;web_verify_str_market:82,119 |
| 7.16 Airbnb 舊制 | 房東約 3%、房客另付約 14.1%–16.5% | 未查:研究檔自己標為搜尋摘要,查核員未開啟,不要用於簡報 | 是(2.09) | web_str_market:82;web_verify_str_market:69,119 |
| 7.17 2025-12-01 全部轉換說法 | 2025-12-01 | 未查:研究檔自己標為搜尋摘要,查核員未開啟,不要用於簡報 | 是(2.12) | web_str_market:85;web_verify_str_market:72,119 |
| 7.18 低情境 2,637 | 約 2,637 AUD | 含 Minoan 2,000(幣別、國別未證實)和 BuyWisely 145(頁面 403 未驗證);不要當主數字,要用就加註「含兩個未驗證加項」 | 否(情境表 6(i)-A) | web_reno_setup:112;web_verify_reno_setup:83,103 |
| 7.19 2 房 Airbnb 開辦合計 | 7,539 AUD(Airbtics) | 頁面前後不一致、無法驗證組成(補查檔查核員另未重開);要用 2 房請改用「1 房 5,358 + 多一間臥室組 1,976」自行推估並註明是推估 | 是(3.22、3.83) | web_reno_setup:44;web_verify_reno_setup:37,104;web_reno_setup_gapfill:70;web_verify_reno_gapfill:69,126 |
| 7.20 Houzz 浴室翻新 | 4,000 / 20,001–40,000 / 40,000+(2014) | 2014 年舊資料,不要放簡報;若引用,低檔帶要寫 4,000–20,000 | 是(3.10) | web_reno_setup:27;web_verify_reno_setup:25,107 |
| 7.21 Domain 預算型浴室整間 | 20,000–27,000 | 頁面 403 打不開,本輪沒驗到,補查前不要用 | 是(3.09) | web_reno_setup:26;web_verify_reno_setup:24,110 |
| 7.22 Yale Assure 電子門閂 | 520 特價 / 660 原價 | 頁面 HTTP 429 打不開,補查前不要用 | 是(3.32) | web_reno_setup:61;web_verify_reno_setup:47,110 |
| 7.23 Yale Keyless Connected | 最低零售 145 | 頁面 HTTP 403 打不開,補查前不要用(也被 6(i) 低情境使用) | 是(3.33) | web_reno_setup:62;web_verify_reno_setup:48,110 |
| 7.24 Minoan 小型 1 房家具套裝 | 2,000–5,000(幣別未確認) | 幣別與國別未證實,只能當低標對照,不要寫成澳洲價 | 是(3.26) | web_reno_setup:48;web_verify_reno_setup:41,111 |
| 7.25 攝影費用「一筆訂單內回本」85% | 85% 的房東 | Airbnb 自述,且「一次訂房」與「一晚」兩種說法不一,建議不用或註明 | 是(3.50) | web_reno_setup:96;web_verify_reno_setup:65,108 |
| 7.26 專業攝影使次年收入 +21% | 21% | Airbnb 自家全球樣本(約 14,700)、非澳洲、因果不明,只能當背景敘述,不要當係數乘進試算 | 是(3.49) | web_reno_setup:95,98;web_verify_reno_setup:64,109 |
| 7.27 「簡單翻新浴室」的標籤(用於「高」情境) | 簡單翻新浴室 17,250 | 17,250 是 What's The Damage 的 Basic renovation(budget fittings,整間基本翻新),不是 cosmetic refresh(Quote Yard 簡單更新 8,000–15,000);請改稱「基本翻新(budget fittings)」 | 是(3.01、3.04) | web_reno_setup:116;web_verify_reno_setup:86,105 |
| 7.28 ABS 住宅營造「對最終需求指數的貢獻 +1.1%」 | +1.1%(對最終需求指數的貢獻,季增) | 不要用:頁面只說住宅營造是最終需求季增的主要貢獻項之一,+1.1% 較可能是該類價格自己的季增(頁面沒明說),且與最終需求整體季增同為 1.1%、易誤讀;要用寫「住宅營造價格季增約 1.1%(ABS 2026 Q3,全澳)」並先人工看原頁 | 是(3.76) | web_reno_setup_gapfill:57;web_verify_reno_gapfill:57,120 |
| 7.29 ABS「建築營造季增 1.3% 主因非住宅營造」 | 主因非住宅營造 | 不要用;改寫「建築營造價格季增 1.3%;ABS 歸因於中東衝突推高燃料與運費,以及技術工短缺」 | 是(3.75) | web_reno_setup_gapfill:56;web_verify_reno_gapfill:56,121 |
| 7.30 「近一年成本只能引最終需求年增 3.6%」 | 官方給不出營造年增、只能引 3.6% | 不要用:ABS 同頁有營造專屬年增(營造 4.9%、房屋營造 5.7%,全澳),比 3.6% 高;要放一句話用營造 4.9% 並註明是全澳不是雪梨 | 是(3.77、3.78) | web_reno_setup_gapfill:60,110;web_verify_reno_gapfill:59,122 |
| 7.31 Hometime 5,000–7,000 稱「寬裕但不奢華」 | 寬裕但不奢華 | 頁面是 modest;簡報寫「適中(modest)的 1 房開辦」;頁面沒列細項,不能與 Airbtics 5,358 逐項相比 | 是(3.79) | web_reno_setup_gapfill:66,72;web_verify_reno_gapfill:65,123 |
| 7.32 What's The Damage 鎖匠頁「智慧鎖含安裝」 | 17–57(搜尋摘要) | 研究檔自己排除、不列表(明顯偏低、與其他兩個差一個量級);查核員未查;不要放進簡報 | 否 | web_reno_setup_gapfill:81;web_verify_reno_gapfill:77,126 |
| 7.33 1 房各區油漆加總 | 1,850–3,600 AUD | 研究檔作者自己用同一頁各列加的算術,不是來源直接給的,且不含門與踢腳板;簡報寫「約 1,850–3,600」並標來源頁內有臥室 500–900 的另一組價 | 否(情境表 6(i)-B) | web_reno_setup_gapfill:32;web_verify_reno_gapfill:87,103,125 |
| 7.34 L6 獨棟屋租金(2026 年 6 月季) | 850 AUD/週 | 與已驗證頁面矛盾:Time Out、Elite Agent 兩頁都寫 9 月季「−$5 到 835」,代表 6 月季應為 840、不是 850;原頁沒開;研究檔自己也註明 L5/L6 不當預設值 | 是(5.07) | web_opcost_housing:72,82;web_verify_opcost_housing:40,118,151 |
| 7.35 L3 公寓租金(2025 年 9 月季) | 750 AUD/週(年增 4.9%) | Domain 原頁 HTTP 403,未驗證 | 是(5.04) | web_opcost_housing:69;web_verify_opcost_housing:37,152 |
| 7.36 L4 獨棟屋租金(2025 年 9 月季) | 780 AUD/週 | Domain 原頁 HTTP 403,未驗證 | 是(5.05) | web_opcost_housing:70;web_verify_opcost_housing:38,152 |
| 7.37 V3 空置率(Domain,2025 年 9 月季) | 0.9% | 原頁 HTTP 403;雖有 Elite Agent 旁證(「0.9% a year earlier」)仍待原頁 | 是(5.11) | web_opcost_housing:75;web_verify_opcost_housing:43,152 |
| 7.38 L5 公寓租金(2026 年 6 月季) | 780 AUD/週 | 原頁沒開(The New Daily 403);Elite Agent 旁證方向一致但不是同一頁 | 是(5.06) | web_opcost_housing:71;web_verify_opcost_housing:39,152 |
| 7.39 V4 空置率(2026 年 6 月季) | 1.1% | 原頁沒開;Elite Agent 旁證(「up from 1.1% in June」)仍待原頁 | 是(5.12) | web_opcost_housing:76;web_verify_opcost_housing:44,152 |
| 7.40 B2 新承作自住房貸平均利率 | 約 6.75% | 原檔沒有出處頁、查核員無網址可查;研究檔自己標低可信度 | 是(5.20) | web_opcost_housing:95;web_verify_opcost_housing:49,153 |
| 7.41 T3 土地稅率 | 100 加超額部分的 1.6% | 該頁沒有任何稅率、只連到另一頁;目前沒有已開頁面支持 | 是(2.16) | web_opcost_housing:110;web_verify_opcost_housing:52,153 |
| 7.42 P3 公寓價值中位數 | 867,597(2026 年 9 月) | 在補查檔指定的網址頁面上查核員看不到,只有搜尋摘要與 ProperEasy 表格旁證;月份(2026-09)與合併值(2026-10)不同月;引用請先換成 Cotality 原頁 | 是(5.16) | web_opcost_housing_gapfill:20,27,89;web_verify_opcost_housing:56,142 |
| 7.43 P4 獨棟屋價值中位數 | 1,466,060(2026 年 9 月) | 同 7.42 | 是(5.17) | web_opcost_housing_gapfill:21,27,89;web_verify_opcost_housing:57,142 |
| 7.44 Cotality 空置率 2.5% 與其他供應商放同一條線 | 2.5%(Cotality) | 頁面該句沒標季別;Cotality 2.5、SQM 1.8、Domain 1.2 三個供應商口徑不同,不要放同一條線 | 是(5.09) | web_opcost_housing:73,80;web_verify_opcost_housing:41,144 |
| 7.45 M3 共同房東抽成「高 25%」當上限 | 25% | 頁面 25% 是 full-service 的下限(25%+),不是上限 | 是(4.10) | web_opcost_housing:40;web_verify_opcost_housing:29,145 |

## 8. 還沒查到的項目

合併自 9 個檔的「沒查到/沒涵蓋/還是查不到」段,已去掉補查檔後來補到的(去掉的列在 8-B)。

### 8-A 仍然沒有

| 項目 | 狀態 | 出處 |
|---|---|---|
| 8.01 按「房型」(整套房/單間)的價格與收入 | 查不到,只有 AirROI 的臥房數分組(1.12–1.15) | web_str_market:120 |
| 8.02 AirDNA 季節性各月數字、供給子頁 | 研究檔:內頁讀取失敗(403),只有 overview;查核員改用 Chrome 讀到 overview(季節性分數 91),各月數字仍沒有 | web_str_market:10,121;web_verify_str_market:5 |
| 8.03 NSW 2025–2026 修法結果 | 官方頁沒有列;官方頁最後更新 2025-02-10;二手文章猜上限可能降到 90 天是猜測、不是決定,使用前要在 planning.nsw.gov.au 再確認 | web_str_market:75,122;web_verify_str_market:115 |
| 8.04 Tourism Research Australia 與 Inside Airbnb 摘要頁 | 這次沒查(工具呼叫上限)【晚上補查 2026-11-14】Inside Airbnb 雪梨頁開到(資料 2026-09-16、20,833 筆,一樣);TRA 猜的網址 404,沒找到每月旅客頁(TRA Online 要登入)。 | web_str_market:123 |
| 8.05 1 房/2 房整戶公寓油漆的來源價 | 補查檔也沒有,只有各區加總的算術(見 7.33、6(i)-B) | web_reno_setup:102;web_reno_setup_gapfill:91;web_verify_reno_gapfill:29 |
| 8.06 木地板翻新(原檔字樣) | 原檔寫「木地板翻新、層板、乙烯地板:查不到」;補查檔補了層板、乙烯、工程木、實木的供應+安裝價(3.63–3.67),沒有「翻新」 | web_reno_setup:103;web_reno_setup_gapfill:34–48 |
| 8.07 浴室「整間每平方公尺」單價 | 未取得可驗證的值(搜尋摘要有不具名的 3,000–5,000/m² 說法,沒對到可開的頁面,不列);補查檔沒處理 | web_reno_setup:104 |
| 8.08 官方/產業協會費用指南(HIA、Archicentre、Cordell、Rawlinsons、Canstar、Master Builders) | 沒取得數字;hipages 被抓取工具擋掉、Domain 403;補查檔仍沒有 HIA、Master Builders、Archicentre 費用指南數字【晚上補查 2026-11-14】hipages 原頁開到(浴室 8,000–35,000、廚房 30,000–50,000,全澳平均);Master Builders NSW 資料包第 1 頁開到(只有材料成本,見 8.09);HIA、Archicentre 還是沒去查。 | web_reno_setup:105;web_reno_setup_gapfill:90 |
| 8.09 ABS 雪梨層級年增 / Master Builders NSW 資料包 | ABS 全澳年增已由查核員補到(3.78),雪梨層級頁面沒有;Master Builders NSW 2025 年 9 月季資料包可能有雪梨層級值,本輪沒開【晚上補查 2026-11-14】Master Builders NSW 2025 年 9 月季資料包第 1 頁開到:房屋營造材料截至 2025 年 9 月一年全澳 +2.1%、雪梨 +2.0%(只是材料,不含工資;第 2–19 頁沒讀)。 | web_reno_setup_gapfill:60,90;web_verify_reno_gapfill:59 |
| 8.10 hipages 浴室/廚房費用指南 | 猜的網址回 404、搜尋工具不給搜 hipages 網域、Chrome 分頁群組中斷;搜尋摘要有說全澳浴室預算型 8,000–15,000、標準 15,000–35,000、高階 35,000 以上,但沒附原頁網址與年份,不放表,僅當線索【晚上補查 2026-11-14】Chrome 開到原頁:浴室 8,000–35,000(2026-01-21 更新)、廚房 30,000–50,000(2026-01-02 更新),都是全澳平均;網址 hipages.com.au/article/how_much_does_bathroom_renovation_cost 與 how_much_does_kitchen_renovation_cost。 | web_reno_setup_gapfill:89 |
| 8.11 雪梨家具租賃(月租)實價 | 查不到雪梨數字 | web_reno_setup:106 |
| 8.12 澳洲業者的 1 房/2 房家具套裝標價 | 沒找到(FurnishX 等出現在搜尋結果但沒標價) | web_reno_setup_gapfill:72,92 |
| 8.13 澳洲裝修或設施升級對價格/訂房率影響的研究 | 原檔與補查檔都沒找到(21% 是 Airbnb 自己的數字、因果不明) | web_reno_setup:98;web_reno_setup_gapfill:85,94 |
| 8.14 床單洗滌費(C2) | 原檔查不到;補查檔本輪沒查(工具次數用完) | web_opcost_housing:36,153;web_opcost_housing_gapfill:93 |
| 8.15 雪梨一般公寓的年度市政費 | 補查檔只有 North Sydney 最低費率、Blacktown 平均費(4.28、4.29,未查);City of Sydney、Inner West 等官方頁沒開 | web_opcost_housing_gapfill:62,90 |
| 8.16 保險公司公布的房東/短租保險費率 | 補查檔只有單一廠商行銷文(4.30,未查) | web_opcost_housing_gapfill:63,91 |
| 8.17 投資客房貸利率(B3) | 原檔與補查檔都查不到(補查檔:抓取工具被 RateCity 轉址到 Canstar,沒有後續工具次數) | web_opcost_housing:96;web_opcost_housing_gapfill:70,74,92 |
| 8.18 雪梨瓦斯年均帳單(AER 或政府來源) | 補查檔只有比價站數字(4.25,未查) | web_opcost_housing_gapfill:48,95 |
| 8.19 NSW 政府租金報告、SQM 的雪梨週租中位數、Cotality 的租金水準(AUD) | 原檔本次沒查到,補查檔沒補 | web_opcost_housing:84 |
| 8.20 L2、P3/P4 的官方原頁(Domain 租金報告、Cotality 或 Domain 房價頁) | 補查檔的值是第二手或搜尋摘要;原頁沒讀到(Chrome 權限提示逾時、頁面 403) | web_opcost_housing:154;web_opcost_housing_gapfill:24,88,89 |
| 8.21 S2(Flat Chat 約 850/季)原頁 | 沒重開,仍是搜尋摘要狀態【晚上補查 2026-11-14】原帖開到:850/季對得上,但那是 2024-06-09 站長自己估的,不是統計(見 4.12)。 | web_opcost_housing_gapfill:94;web_verify_opcost_housing:31 |
| 8.22 2026-27 電費最終版與 AER 官方原件 | 原檔只有草案(最終版沒查);AER 2025-26 決定頁逾時,2026-27 草案資訊頁查核員也逾時【晚上補查 2026-11-14】草案資訊頁 PDF 被轉到 AER 登入頁;最終版新聞稿開到但沒有 Ausgrid 年電費(見 4.07)。 | web_opcost_housing:20,27,154;web_verify_opcost_housing:24 |
| 8.23 ATO 短租報稅重點的獨立查核 | 補查檔的 Chrome 讀到頁面(見 2.17);獨立查核員 WebFetch 403、沒驗到 | web_opcost_housing_gapfill:80;web_verify_opcost_housing:73 |
| 8.24 搜尋摘要來源的列的原頁 | 未開原頁,正式引用前需回頭核對(原檔與補查檔都這樣寫) | web_opcost_housing:155;web_opcost_housing_gapfill:96 |

### 8-B 已去掉(後來補查到;主表有值,查核狀態以主表為準)

| 項目 | 補到的位置 | 出處(原「沒查到」位置) |
|---|---|---|
| 室內油漆每房/每平方公尺價格 | 3.51–3.62(查核 ✅) | web_reno_setup:102;web_reno_setup_gapfill:19–30 |
| 地板:層板、乙烯、工程木、實木的供應+安裝價 | 3.63–3.71(查核 ✅) | web_reno_setup:103;web_reno_setup_gapfill:38–46 |
| 官方成本指數(ABS) | 3.75–3.78(⚠️/⚠️/✅/❌) | web_reno_setup_gapfill:56–60 |
| 智慧鎖安裝工資 | 3.84–3.85(查核員已開原頁 ✅) | web_reno_setup:106;web_reno_setup_gapfill:78–79 |
| 水費(Sydney Water) | 4.18–4.24(✅) | web_opcost_housing:21;web_opcost_housing_gapfill:33–39 |
| 瓦斯、網路 | 4.25–4.27(有值但未查) | web_opcost_housing:22,23;web_opcost_housing_gapfill:40–42 |
| 市政費、保險(單點) | 4.28–4.30(有值但未查;一般公寓與保險公司費率仍沒有,見 8.15、8.16) | web_opcost_housing:58,59;web_opcost_housing_gapfill:56–58 |
| ATO 報稅重點 | 2.17(⏸) | web_opcost_housing:111;web_opcost_housing_gapfill:80 |
| 2026 年 9 月季雪梨公寓租金 | 5.02(⚠️) | web_opcost_housing:68;web_opcost_housing_gapfill:17 |
| 雪梨公寓與獨棟分開的房價中位 | 5.16–5.17(⚠️) | web_opcost_housing:92,93;web_opcost_housing_gapfill:20,21 |

### 8-C 研究檔表格中「值為查不到」的列去向(這些列沒有數值,不計入總表列數)

| 研究檔列 | 去向 | 出處 |
|---|---|---|
| 原檔 W1 水費 | 補查檔補到,見 4.18–4.23 | web_opcost_housing:21 |
| 原檔 G1 瓦斯 | 補查檔有值,見 4.25(未查) | web_opcost_housing:22 |
| 原檔 N1 網路 | 補查檔有值,見 4.26–4.27(未查) | web_opcost_housing:23 |
| 原檔 C2 床單洗滌費 | 仍沒有,見 8.14 | web_opcost_housing:36 |
| 原檔 R1 市政費 | 補查檔有單點值,見 4.28–4.29(未查);一般公寓仍沒有,見 8.15 | web_opcost_housing:58 |
| 原檔 I1 房東/短租保險 | 補查檔有單一區間,見 4.30(未查);保險公司費率仍沒有,見 8.16 | web_opcost_housing:59 |
| 原檔 L2 公寓租金 | 補查檔補到,見 5.02(⚠️) | web_opcost_housing:68 |
| 原檔 P3 公寓中位價 | 補查檔有搜尋摘要值,見 5.16(⚠️) | web_opcost_housing:92 |
| 原檔 P4 獨棟中位價 | 補查檔有搜尋摘要值,見 5.17(⚠️) | web_opcost_housing:93 |
| 原檔 B3 投資客房貸利率 | 仍沒有,見 8.17 | web_opcost_housing:96 |
| 原檔 T4 ATO 報稅重點 | 補查檔補到,見 2.17(⏸) | web_opcost_housing:111 |
| 補查檔 B3 投資客房貸利率 | 仍沒有,見 8.17 | web_opcost_housing_gapfill:70 |

總表共 190 列,其中 ✅ 130、⚠️ 34、⏸/未查/沒涵蓋 25(⏸ 8、未查 17、查核檔沒涵蓋 0),不採用 45(含不放主表的 2 筆);另有 ❌ 1 列(3.78,查核員在頁面看到正確值,照規則 a 更正後放入主表)。
