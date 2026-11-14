# 查核:web_reno_setup_2026-11-14.md(雪梨裝修與佈置行情)

查閱日 2026-11-14;scope ID:IS-1114-verify-02-reno。獨立查核員,不是原筆記作者。

**一句話總結:** 筆記共 50 列,重新打開網址查了 50 列:✅ 43、⚠️ 4、❌ 0、⏸ 3、未查 0;第 7 節三種情境的加法全部算對(2,637 / 5,895 / 39,618),但「低」情境用到一列頁面打不開的數字(145)和一列幣別與國別頁面沒寫的數字(2,000),「高」情境混了 GST 含/不含與不同資料年份。

查核方法與限制:
- 用 WebFetch 重開網址,頁面內容經小模型轉成摘要後回傳,所以「頁面實際看到的值」是摘要裡的原文數字,不是我親眼逐字比對 HTML。
- Domain(403)、BuyWisely(403)、Entry Point(429,重試一次仍 429)打不開;工具上限用完,沒有改用 Chrome 分頁補查,所以這三列標 ⏸,不是「對不上」。
- 資料年份欄:多數頁面只標發布/更新日,筆記的「2026」都吻合頁面日期;筆記沒寫 GST 的來源,頁面也多半沒寫。

## 逐列判定表

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| 浴室:基本 | 11,500 / 17,250 / 23,000 AUD,Sydney,2026-11 | Basic(budget fittings)$11,500 / $17,250 / $23,000;含 GST;Sydney metro,Nov 2026 | ✅ | 吻合 | https://whatsthedamage.com.au/bathroom-renovation-cost-sydney/cost-breakdown/ |
| 浴室:標準 | 23,000 / 31,050 / 40,250 | Mid-range $23,000 / $31,050 / $40,250 | ✅ | 吻合 | 同上 |
| 浴室:高階 | 40,250 / 48,300 / 63,250 | Premium $40,250 / $48,300 / $63,250 | ✅ | 吻合;頁面另有 Luxury 63,250–92,000,筆記沒列(非錯) | 同上 |
| 浴室:簡單更新 | 8,000–15,000,NSW | Cosmetic refresh $8,000–$15,000;Published 8 Sep 2026;未標 GST | ✅ | 吻合 | https://www.thequoteyard.com.au/services/bathroom-renovation-cost-nsw |
| 浴室:標準 4–8 m² | 25,000–45,000 | $25,000–$45,000 | ✅ | 吻合 | 同上 |
| 浴室:大雪梨標準家庭 | 28,000–48,000 | $28,000–$48,000(Greater Sydney 標準家庭浴室) | ✅ | 吻合 | 同上 |
| 浴室:西雪梨標準 | 22,000–38,000 | $22,000–$38,000(Western Sydney,2026) | ✅ | 吻合 | 同上 |
| 浴室:起價 | 14,900 起,2025-04-02,全澳 | Bathroom $14,900+;Last Updated 02 April 2025;頁面未明寫地區 | ✅ | 吻合;地區「全澳」是筆記推斷(AU 站) | https://www.airtasker.com/au/costs/house-renovation/house-renovation-cost/ |
| 浴室:預算型整間(搜尋摘要) | 20,000–27,000,Domain 引述 Makeover Group | HTTP 403,打不開 | ⏸ | 筆記自己也標「搜尋摘要」、沒開過原頁;此列無法驗證 | https://www.domain.com.au/advice/bathroom-renovation-costs/ |
| 浴室:低檔帶(舊資料) | 低 4,000;中 20,001–40,000;高 40,000+;2014 | 「Low-range $4000 to $20,000」「Mid-range $20,001-$40,000s」「Luxury $40,000+」;Houzz AU 11 June 2014 | ⚠️ | 定義:筆記「低=4,000」只是低檔帶下限,低檔帶實為 4,000–20,000;「高 40,000+」頁面稱 Luxury。年份 2014 吻合 | https://www.houzz.com.au/magazine/bathroom-renovation-how-much-will-it-cost-me-stsetivw-vs~26882976 |
| 浴室磁磚人工(標準) | 65–120 AUD/m²,NSW | $65–$120/m²,標準尺寸陶瓷/瓷磚,僅人工不含磚 | ✅ | 吻合 | thequoteyard 浴室頁(同上) |
| 浴室磁磚人工(大片/石) | 100–180 AUD/m² | $100–$180/m²,大片/天然石/複雜圖案,僅人工 | ✅ | 吻合 | 同上 |
| 廚房:簡單換新(WTD) | 9,200 / 16,100 / 23,000,Sydney,2026-11 | Kitchen cosmetic refresh(reface+paint)$9,200 / $16,100 / $23,000;含 GST;Sydney Nov 2026 | ✅ | 吻合 | https://whatsthedamage.com.au/price-index/sydney/2026-11/ |
| 廚房:簡單換新(QY) | 8,000–18,000,2026-09-29 | Cosmetic refresh AUD $8,000–$18,000;Published 29 Sep 2026 | ✅ | 吻合 | https://www.thequoteyard.com.au/services/kitchen-renovation-cost-nsw |
| 廚房:平價組裝櫃 | 12,000–22,000 | $12,000–$22,000 | ✅ | 吻合 | 同上 |
| 廚房:小廚房 <10 m² | 18,000–30,000 | $18,000–$30,000 | ✅ | 吻合 | 同上 |
| 廚房:標準 10–18 m² | 30,000–55,000 | $30,000–$55,000 | ✅ | 吻合 | 同上 |
| 廚房:標準,Inner Sydney | 42,000–68,000 | $42,000–$68,000(Paddington、Surry Hills、Newtown、Balmain 區域表) | ✅ | 吻合 | 同上 |
| 廚房:起價 | 30,000 起,2025-04-02 | Kitchen $30,000+;Last Updated 02 April 2025 | ✅ | 吻合 | https://www.airtasker.com/au/costs/house-renovation/house-renovation-cost/ |
| 地毯供應+安裝 | 52 / 80 / 125 AUD/m² | Carpet supply+install per sqm $52 / $80 / $125;含 GST | ✅ | 吻合 | https://whatsthedamage.com.au/price-index/sydney/2026-11/ |
| 1 房開辦合計 | 中 5,358 | 1-bedroom AU$5,358;資料期間 2023-10 至 2024-09;範圍 Australia | ✅ | 吻合;分項(1,976+2,356+1,026)我加過 = 5,358 | https://airbtics.com/starting-an-airbnb-australia |
| 2 房開辦合計 | 中 7,539 | 頁面有寫 AU$7,539,但頁面沒給 2 房的分項;頁面文字還把 7,539 誤掛在客廳小節 | ⚠️ | 數字存在但頁面本身前後不一致、無法驗證其組成。若 2 房 = 1 房 + 多一間臥室組 1,976 → 7,334,與 7,539 差 205。此數沒被第 7 節使用 | 同上 |
| 其中:臥室家具組 | 1,976 | 臥室(每間)合計 AU$1,976(7 項加總吻合) | ✅ | 吻合;頁面明寫「per bedroom」 | 同上 |
| 其中:客廳 | 2,356 | 客廳合計 AU$2,356(6 項加總吻合) | ✅ | 吻合 | 同上 |
| 其中:其他 | 1,026 | Other AU$1,026(毛巾/枕頭/毯各 152、智慧鎖 228、攝影機 152、人工 190,加總 1,026) | ✅ | 吻合 | 同上 |
| 小型 1 房家具套裝(Minoan) | 2,000–5,000,幣別未確認,非澳洲 | 「a package might range from $2,000 to $5,000」;未註明幣別;頁面沒說公司在哪國(只有一個 pinterest.com.au 連結) | ⚠️ | 數值吻合、幣別未標吻合;但「非澳洲業者」頁面沒有證實(也沒證偽),屬筆記的推斷 | https://minoan.com/blog/airbnb-furniture-packages |
| 全套代佈置「典型單價」 | 12,000–25,000 AUD,房數未標 | 「12 000 AUD - 25 000 AUD」;AUD;無房數 | ✅ | 吻合 | https://www.houzz.se/pro/hostmybnb/airbnb-furnishing-services-by-hostmybnb |
| 攝影:基本 | 250–300 | Basic 約 10–15 張,$250–$300(AUD);Sep 17, 2026 | ✅ | 吻合;頁面摘要未直接寫「全澳」,以 AUD 計 | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth |
| 攝影:標準 | 295–500 | Standard 20–30 張,$295–$500 | ✅ | 吻合 | 同上 |
| 攝影:高階 | 500–1,000+ | Premium(空拍、黃昏、大屋)$500–$1,000+ | ✅ | 吻合 | 同上 |
| 智慧門鎖(Airbtics 單項) | 228 | Smart lock AU$228 | ✅ | 吻合 | https://airbtics.com/starting-an-airbnb-australia |
| 智慧鎖:Yale Assure(零售) | 520 特價 / 660 原價 | HTTP 429(重試一次仍 429) | ⏸ | 打不開,未驗證 | https://entry-point.com.au/products/yale-assure-keyed-electronic-deadbolt-black |
| 智慧鎖:Yale Keyless Connected | 最低零售 145 | HTTP 403 | ⏸ | 打不開;筆記標「搜尋摘要」。此數被第 7 節「低」情境使用 | https://buywisely.com.au/product/yale-keyless-connected-door-lock |
| 安全攝影機(Airbtics) | 152 | Security camera AU$152 | ✅ | 吻合 | https://airbtics.com/starting-an-airbnb-australia |
| 毛巾/枕頭/毯子 | 152 + 152 + 152 | Towels 152、Pillows 152、Blankets 152 | ✅ | 吻合 | 同上 |
| 首次深度清潔 | 242 AUD/次,Sydney,2026-10-23 | Deep clean「$ 242 /session」;Updated 23 October 2026;Sydney | ✅ | 吻合;頁面未見房型條件,不知 242 對應幾房 | https://www.maidforyou.com.au/blog/how-much-end-of-lease-clean/ |
| 退租大掃除:Studio/1 房 | 410 | Studio / 1 bedroom $410 | ✅ | 吻合 | 同上 |
| 退租大掃除:2 房 | 450 | 2 bedrooms $450 | ✅ | 吻合 | 同上 |
| 居家清潔時薪 | 40 / 63 / 92 AUD/小時 | House cleaning general per hour $40 / $63 / $92 | ✅ | 吻合 | https://whatsthedamage.com.au/price-index/sydney/2026-11/ |
| 地毯蒸氣清洗 | 34 / 52 / 69 AUD/每間房 | Carpet steam clean per room $34 / $52 / $69 | ✅ | 吻合 | 同上 |
| 油漆工 | 40 / 60 / 100 AUD/小時 | Painter per hour $40 / $60 / $100 | ✅ | 吻合 | 同上 |
| 電工 | 92 / 115 / 170 | Electrician per hour $92 / $115 / $170 | ✅ | 吻合 | 同上 |
| 水管工 | 92 / 140 / 230 | Plumber per hour $92 / $140 / $230 | ✅ | 吻合 | 同上 |
| 雜工(WTD) | 57 / 105 / 140 | Handyman per hour $57 / $105 / $140 | ✅ | 吻合 | 同上 |
| 雜工平日時薪(QY) | 80–120(多數 90–110),2026-08-24 | 平日 $80–$120/小時;「majority … $90 to $110」;Published 24 Aug 2026 | ✅ | 吻合 | https://www.thequoteyard.com.au/services/handyman-pricing-guide-nsw |
| 雜工半天 | 350–500 | $350–$500(4 小時) | ✅ | 吻合 | 同上 |
| 雜工全天 | 600–900 | $600–$900(8 小時) | ✅ | 吻合 | 同上 |
| 雜工週末/夜間 | 120–180/小時 | $120–$180/hr | ✅ | 吻合 | 同上 |
| 專業攝影使次年收入 +21% | 21%,樣本約 14,700,全球 | Airbnb 自家數據:用其專業攝影的房源次年多賺 21%;約 14,700 筆;頁面明說樣本是 global 非澳洲;未給期間與方法 | ✅ | 吻合;因果不明,筆記已提醒不要當係數 | https://www.hometime.io/blog/airbnb-professional-photography-cost-worth |
| 攝影費用一筆訂單內回本 85% | 85%(房東比例) | 頁面歸給 Airbnb:85% 的房東在「一次訂房」內回本;摘要同時出現「one night's stay」的另一種說法 | ⚠️ | 定義:「一筆訂單」vs「一晚」頁面說法不一,不確定哪個是原意;簡報若用請寫「一次訂房」並註明為 Airbnb 自述 | 同上 |

判定統計(50 列):✅ 43、⚠️ 4(Houzz 低檔帶、Airbtics 2 房、Minoan、85% 回本)、❌ 0、⏸ 3(Domain、Entry Point、BuyWisely)、未查 0。

## 第 7 節三種情境加總驗算

**低** = 2,000(Minoan)+ 250(Hometime 基本低標)+ 145(BuyWisely)+ 242(Maid for You)
= 2,000 + 250 = 2,250;+ 145 = 2,395;+ 242 = **2,637** → 筆記「約 2,637」**對**。

**中** = 5,358(Airbtics)+ 295(Hometime 標準低標)+ 242(Maid for You)
= 5,358 + 295 = 5,653;+ 242 = **5,895** → 筆記「約 5,895」**對**。

**高** = 5,358(Airbtics)+ 500(Hometime 高階低標)+ 410(退租級 1 房)+ 17,250(WTD 浴室 Basic 典型)+ 16,100(WTD 廚房 cosmetic 典型)
= 5,358 + 500 = 5,858;+ 410 = 6,268;+ 17,250 = 23,518;+ 16,100 = **39,618** → 筆記「約 39,618」**對**。
- 只翻新浴室:6,268 + 17,250 = **23,518** → 對。
- 兩者都取高標 23,000:6,268 + 23,000 + 23,000 = **52,268** → 對。

用到的每一列在第 7 節以前的驗證狀態與混用問題:
- 「低」:2,000 是 ⚠️(幣別頁面未標、國別未證實、無年份);145 是 ⏸(頁面打不開,無法確認);250、242 是 ✅。所以「低」有兩個數字不是穩的,而且 Minoan 與 BuyWisely 都沒有年份,與 2026 的 Hometime、Maid for You 混加。
- 「中」:5,358、295、242 全 ✅,但資料年份不同:Airbtics 是 2023-10 至 2024-09,Hometime 是 2026-09、Maid for You 是 2026-10,等於把約 2 年前的整包加上 2026 年報價。國家都是澳洲,沒有跨國混加。
- 「高」:五項全 ✅。年份同樣混(Airbtics 2023–24 + 其他 2026)。GST 口徑混:WTD 兩項頁面明寫含 GST,Airbtics、Hometime、Maid for You 頁面沒寫含不含。範圍混:Airbtics 全澳、WTD 與 Maid for You 是 Sydney。
- 標籤問題:「高」情境稱「簡單翻新浴室」,但用的 17,250 是 WTD 的 Basic renovation(budget fittings,整間基本翻新),不是 cosmetic refresh;同一份筆記裡 Quote Yard 的「簡單更新」是 8,000–15,000。廚房用的 16,100 才是真的 cosmetic refresh。
- 跨國混加:「低」情境若 Minoan 真的非澳洲(頁面未證實),就是把非澳洲的家具價加到澳洲的清潔與攝影價上;筆記已自己註明可信度最低。

## 簡報上可以直接用的數字

(頁面上親眼看到、單位年份範圍都吻合;仍請標「網路公開報價,非成交價」)
- 雪梨浴室翻新(What's The Damage,Sydney metro,2026-11,含 GST):基本 11,500–23,000(典型 17,250)、標準 23,000–40,250(典型 31,050)、高階 40,250–63,250(典型 48,300)。
- 浴室(Quote Yard,2026):簡單更新 8,000–15,000(NSW);大雪梨標準家庭 28,000–48,000;西雪梨 22,000–38,000。
- 廚房(2026):簡單換新 Sydney 9,200–23,000(典型 16,100,含 GST);NSW 8,000–18,000;Inner Sydney 標準 42,000–68,000。
- 澳洲 1 房 Airbnb 開辦合計 5,358(Airbtics,資料期間 2023-10 至 2024-09;組成加總吻合 1,976 + 2,356 + 1,026)。
- 攝影:基本 250–300、標準 295–500、高階 500–1,000+(Hometime,2026)。
- 退租級大掃除 Sydney:1 房 410、2 房 450;深度清潔 242/次(Maid for You,2026-10)。
- Sydney 時薪(What's The Damage,2026-11,含 GST):油漆 40–100、電工 92–170、水管 92–230、雜工 57–140、居家清潔 40–92。
- 三個情境的加總算術是對的:約 2,637 / 5,895 / 39,618(中與高的每個加項都查過)。

## 簡報上要加註或不要用的數字

- 「低」情境 2,637:不要當主數字。含 Minoan 2,000(幣別、國別未證實)和 BuyWisely 145(頁面 403 未驗證),要用就加註「含兩個未驗證加項」。
- 2 房開辦合計 7,539:頁面前後不一致,不建議用;要用 2 房,請改用「1 房 5,358 + 多一間臥室組 1,976」自行推估並註明是推估。
- 浴室「高階」「中」情境:「簡單翻新浴室」請改稱「基本翻新(budget fittings)」,避免與 8,000–15,000 的 cosmetic refresh 混淆。
- 「中」「高」加總:加註「Airbtics 為 2023–24 資料,其餘為 2026 報價;WTD 含 GST,其餘來源未標」。
- Houzz 浴室 4,000 / 20,001–40,000 / 40,000+:2014 年舊資料,不要放簡報;若引用,低檔帶要寫 4,000–20,000。
- 85% 房東一筆訂單內回本:Airbnb 自述且「一次訂房」與「一晚」說法不一,建議不用或註明。
- 21% 收入增幅:頁面確認是 Airbnb 自家全球樣本(約 14,700)、非澳洲、因果不明,只能當背景敘述,不要當係數乘進試算。
- Domain 20,000–27,000、Yale Assure 520/660、Yale Keyless 145:本輪都打不開(403/429/403),在補查前不要用。
- Minoan 2,000–5,000:幣別與國別未證實,只能當低標對照,不要寫成澳洲價。
- 通則:所有裝修價來源都是商業報價網站,不是官方統計;資料頁面抓取經摘要工具,若要放進正式簡報,關鍵數字(浴室 17,250、廚房 16,100、5,358)建議再人工開頁面對一次。
