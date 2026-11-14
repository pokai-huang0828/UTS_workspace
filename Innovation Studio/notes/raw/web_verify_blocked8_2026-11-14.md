# 補查 8 列(原本因 403/429/逾時標 ⏸)+ 1 列加查,2026-11-14

**一句話總結:8 列加 1 列加查共 9 列,✅ 4、⚠️ 0、❌ 2、⏸ 3;Domain 三列與浴室預算在 Chrome 打開且數字吻合,兩個智慧鎖價格對不上;AER 原件、ATO、加查的 Domain 2026 年 9 月季 780 因工具呼叫上限(24 次)用完沒有查,維持 ⏸。**

scope ID:IS-1114-verify-05-blocked8。查核員:獨立查核(非筆記作者)。Chrome 權限提示:Domain 第一次開頁時需要使用者允許,允許後重新開同一網址就讀得到;之後的網站沒有再卡權限。

## 逐列判定

| 原查核檔與代號 | 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 | 這次用什麼工具打開 |
|---|---|---|---|---|---|---|---|
| web_verify_opcost_housing / E7 | AER 預設市場價 2026-27 草案資訊頁(官方原件) | 只記網址,用來核對 E2 1,875 / E4 2,347 / E6 2,515(AUD/年,2026-27 草案) | 沒打開 | ⏸ | 工具呼叫上限用完,這次沒試;E2/E4/E6 仍只有 Canstar 轉述 | https://www.aer.gov.au/system/files/2026-03/Draft%20Default%20Market%20Offer%202026-27%20-%20Information%20sheet.pdf | 未開 |
| web_verify_opcost_housing / L3 | 雪梨公寓租金中位數,2025 年 9 月季 | 750 AUD/週(年增 4.9%) | 雪梨 Units:「record of $750 per week」,季增 1.4%,年增 4.9%($35) | ✅ | 數值、單位(每週)、期間(Sep-25 季)、地區(Sydney)全吻合 | https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ | Chrome(navigate + get_page_text) |
| web_verify_opcost_housing / L4 | 雪梨獨棟屋租金中位數,2025 年 9 月季 | 780 AUD/週 | 雪梨 Houses:「record high of $780 per week」,季增 0%,年增 1.3%;總表 Sydney Sep-25 $780 | ✅ | 數值、單位、期間、地區吻合 | 同上 | Chrome(同一頁) |
| web_verify_opcost_housing / V3 | 雪梨空置率,2025 年 9 月 | 0.9% | 「Vacancy rates fell to 0.9% in September」(雪梨段落,「lowest September figure since 2023」) | ✅ | 吻合;頁面把 0.9% 放在雪梨段落,期間為 2025 年 9 月 | 同上 | Chrome(同一頁) |
| web_verify_opcost_housing / T4 | ATO 短租收入申報重點(補查檔 §5 的 5 點與「最後更新 2026-05-21」) | 見補查檔 §5 | 沒打開 | ⏸ | 工具呼叫上限用完,這次沒試 | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare | 未開 |
| web_verify_reno_setup / 浴室預算型整間 | 浴室翻新「預算型整間」,Domain 引述 Makeover Group | 20,000–27,000 AUD(2025,全澳) | The Makeover Group 負責人 Richard Armstrong:「a full budget renovation will set you back between $20,000 and $27,000」;頁面年份 2025(內文「in 2025」) | ✅ | 數值與出處人物吻合。注意頁面小標「The budget bathroom: $5,000 – $27,000」,整段預算級下限是 5,000(基本翻新 5,000–10,000),20,000–27,000 只是「整間預算翻新」那一句;頁面未標幣別字樣,以澳洲網站推定 AUD | https://www.domain.com.au/advice/bathroom-renovation-costs/ | Chrome(get_page_text 只抓到無關文字,改用 javascript_tool 讀 body 文字) |
| web_verify_reno_setup / Yale Assure | Entry Point 的 Yale Assure Keyed Electronic Deadbolt(Black,零售) | 520 特價 / 660 原價 | 頁面可見文字寫「Prices are shown once you log in」,價格被登入牆遮住,標籤只有「Save 30%」;頁面結構化資料(meta/JSON)為 price 550.00 AUD、compare_at_price 787.07 | ❌ | 頁面資料與筆記的 520/660 對不上(550 / 787.07,折扣 30%,不是 520/660 的約 21%)。價格顯示在頁面上要登入才看得到(我沒有登入),所以只憑頁面原始資料判定;520/660 可能來自舊快取或搜尋摘要,不能再引用 | https://entry-point.com.au/products/yale-assure-keyed-electronic-deadbolt-black | Chrome(javascript_tool 讀頁面文字與 meta) |
| web_verify_reno_setup / Yale Keyless | BuyWisely 的 Yale Keyless Connected,最低零售 | 145(此數被第 7 節「低」情境使用) | 比價範圍 $157.21–$315.17(10 家,最近一次見價 2026-11-03);頁面當日價 $199.99;歷史最低 $115.40(2025-02-04);近期區間最低 $192.00(2026-07-23) | ❌ | 頁面上沒有 145;現價最低 157.21,歷史最低 115.40,兩個都不是 145。第 7 節「低」情境用 145 要改用頁面有的數(例如現價最低 157.21,並註明日期 2026-11-03) | https://buywisely.com.au/product/yale-keyless-connected-door-lock | Chrome(javascript_tool 讀頁面文字) |
| web_opcost_housing_gapfill / L2(加查) | 雪梨公寓每週租金中位數 780(Domain 2026 年 9 月季,經 Elite Agent 轉述) | 780 AUD/週(2026 年 9 月季,持平) | 沒打開 Domain 2026 年 9 月季報告頁 | ⏸ | 工具呼叫上限用完。旁證(不算驗證):這次讀到的 2025 年 9 月季頁面,雪梨公寓是 750、獨棟是 780;所以 780 在 2025 年 9 月季是獨棟的數字,筆記 L2「公寓 780」要特別確認不是把獨棟與公寓混了 | 待查 Domain 2026 年 9 月季租金報告頁 | 未開 |

## 備註

- 判定方法:Chrome 開頁後用頁面文字比對筆記值;沒有登入、沒有下載、沒有填表。
- 加查那列的旁證提醒值得優先處理:2025 年 9 月季同一份 Domain 報告裡,雪梨 780 是獨棟(House),公寓(Unit)是 750。
- 仍待查:E7、T4、加查 L2(上限用完)。

這份的判定取代原查核檔裡這幾列的 ⏸
