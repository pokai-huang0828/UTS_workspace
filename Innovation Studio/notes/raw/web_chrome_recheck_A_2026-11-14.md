# Chrome 重查 A 組(10 個之前打不開的網站)— 2026-11-14

**結果:開到 6 個、要登入 2 個、被擋 0 個、找不到頁面 1 個、沒做(工具次數用完)1 個。**
(開到:A1、A3、A4、A5、A6、A9;要登入:A7、A8;找不到頁面:A2;沒做:A10。)

做法:Claude in Chrome,自己開的分頁,沒登入、沒送表單、沒下載。A6 的 PDF 是直接在 Chrome 內建檢視器顯示,沒有跳下載。

| 編號 | 網站 | 實際開到的網址 | 結果 | 我們原本要核對的話(來源筆記) | 頁面上的數字或原文(短) | 頁面日期 | 跟我們筆記比 |
|---|---|---|---|---|---|---|---|
| A1a | hipages 浴室 | https://hipages.com.au/article/how_much_does_bathroom_renovation_cost (原猜的 bathroom_renovation_cost 是 404;正確網址從 Google site: 搜尋點進去) | 開到了 | 搜尋摘要:全澳預算型 8,000–15,000、標準 15,000–35,000、高階 35,000+,但沒網址與年份(web_reno_setup_gapfill:89) | 頁首「From $8,000 To $35,000」(全澳平均);預算 8,000–15,000、標準 15,000–35,000、高階 35,000+;另引 HIA 2023 全澳平均 26,000;每平方公尺 2,300–4,600 | Last Updated on 21 Jan 2026 | 一樣(摘要的三檔數字全部對上),新資料:有原頁網址、日期、HIA 2023 平均 26,000 |
| A1b | hipages 廚房 | https://hipages.com.au/article/how_much_does_kitchen_renovation_cost (我猜的 how_much_does_a_kitchen_renovation_cost 沒開到內容,改點 Google 結果進去) | 開到了 | 之前沒有廚房數字(web_reno_setup 系列沒收) | 頁首「From $30,000 To $50,000」(全澳);文內「basic reno around $30,000 - $50,000」;預算 10,000 可做換門板/地板/benchtop 等不動水電的小改;建議另加 15%–20% 預備金 | Last Updated on 2 Jan 2026 | 新資料 |
| A2 | Domain 2026 年 9 月季租金報告 | 我試的 .../rental-report/september-2026-rental/ 回「Page not found」;.../reports/rental-report 也是 Page not found;Google site: 搜尋沒有 2026 年的季報(最新只到 Rental Report - December 2025)。改開 September 2025 頁當對照:https://insight.domain.com.au/research-insights/reports/rental-report/september-2025-rental/ | 找不到頁面(2026 年 9 月季那頁) | L3 雪梨公寓 750(年增 4.9%)、L4 獨棟 780、V3 空置率 0.9%(皆 2025 年 9 月季,web_opcost_housing:69,70,75);原本要找 2026 年同一季 | 2026 年那頁沒開到。對照的 2025 年 9 月頁:雪梨 Houses $780(季 0%、年 1.3%)、Units $750(季 1.4%、年 4.9%)、vacancy 0.9%;Google 摘要:2025 年 12 月季雪梨獨棟 $800(+1.3%) | 頁面只標「September 2025」(無發布日);另一頁標題為 December 2025 | 2025 年 9 月數字一樣(L3、L4、V3 都對上);2026 年 9 月季:看不到 |
| A3 | The New Daily | https://www.thenewdaily.com.au/news/2026/10/08/domain-rent-prices | 開到了 | L5 雪梨公寓 780、L6 獨棟 850(標 2026 年 6 月季,web_opcost_housing:71–72);meeting_1114_external_facts 5.06/5.07 | 頁面標題「Rents stall in most cities as tenants hit affordability wall」。雪梨只有一個數字:「fell $5 to $835」(6 月到 9 月);其他城市:墨爾本 600、布里斯本 700、阿得雷德 650、伯斯 750、荷巴特 625、達爾文 760→800;全國獨棟持平、公寓 +1.5%。頁面沒有雪梨公寓的單獨數字,也沒有空置率 1.1 | Oct 08, 2026,updated Oct 09, 2026 | 不一樣:L6 850 與頁面 835(9 月)/840(6 月)對不上;L5 公寓 780 在此頁看不到;V4 空置率 1.1 看不到 |
| A4 | OpenAgent | https://www.openagent.com.au/news/national-property-market-update-october-2026(頁面標題「Values slip again as buyers wait out higher rates」) | 開到了 | P3 雪梨公寓 867,597(年 −3.8%)、P4 獨棟 1,466,060(年 −8.2%)(web_opcost_housing_gapfill:20;meeting_1114_external_facts 5.16、5.17) | 頁面全文搜尋:867,597 沒有、1,466,060 沒有。頁面上寫的是雪梨全住宅中位 $1,178,959(月 −1.6%、季 −4.7%、年 −9.4%);「Sydney led the rise, with its vacancy rate climbing to 1.8 per cent」(SQM,9 月;全國 1.4%) | Last updated on Nov 4, 2026 | 不一樣:兩個指定數字頁面上都沒有(頁面只給全住宅 1,178,959);P2 與 V2 一樣 |
| A5 | Flat Chat | https://www.flatchat.com.au/flat-chat-forum/topic/how-do-you-guesstimate-levies/ (輸入舊網址後自動轉到這個) | 開到了 | S2 雪梨中位價公寓管理費約 850/季,日期沒確認(web_opcost_housing:53) | 站長 Jimmy-T 寫:雪梨公寓中位價約 $850,000、平均管理費約 $850 一季,約為房價 0.4%/年;他的「quick search」,沒附來源;另有網友:雪梨 8 戶、各約 80 萬、管理費 $3,200/年(0.4%);站長收斂的合理基準 0.4%–0.6% | 貼文 09/06/2024(2024 年 6 月 9 日) | 一樣(850/季對上);新資料:日期是 2024 年 6 月,不是現在的行情;且是論壇隨手估算,不是統計 |
| A6 | Master Builders NSW PDF | https://www.mbansw.asn.au/sites/default/files/datapack_-_building_input_and_output_costs_-_sept_2025_qtr.pdf | 開到了(Chrome 內建檢視器,19 頁,只讀了第 1 頁截圖) | 想找雪梨層級的營造/裝修成本年增(web_reno_setup_gapfill:60);原本只有全澳最終需求年增 3.6%,沒有雪梨 | 第 1 頁「房屋營造用料投入成本,截至 2025 年 9 月的年增」:All materials used in house building 全澳 +2.1%、雪梨 +2.0%(墨爾本 2.3%、布里斯本 1.8%);雪梨分項:木料 +2.2%、陶瓷 −1.5%、水泥混凝土 +1.0%、鋼 −5.8%、電氣設備 +2.6%、其他 +4.6%;註明資料來源為 Master Builders Australia 分析 ABS 生產者物價指數 | 頁尾 October 2025 | 新資料:有雪梨數字,但只是「材料投入成本」,不是工資或整體裝修價;第 2–19 頁(季變化、產出成本)沒讀 |
| A7 | AER 草案預設市場價 2026-27 資訊頁 PDF | 輸入的網址被轉到 https://www.aer.gov.au/user/login?destination=/system/files... (AER 網站的登入頁,文字寫給 AER 網站編輯/技術支援人員) | 要登入(登入網域 aer.gov.au) | E2 Ausgrid 1,875、E4 Endeavour 2,347、E6 Essential 2,515(AUD/年,2026-27 草案),目前只有 Canstar 轉述(web_opcost_housing:15–19;meeting_1114_external_facts 4.07) | 沒拿到 PDF,沒有數字;年用電量 kWh 假設也沒看到 | 看不到 | 看不到(沒開到官方原件,E2/E4/E6 仍待核對) |
| A8 | Entry Point Yale Assure 智慧門鎖(黑) | https://www.entry-point.com.au/products/yale-assure-keyed-electronic-deadbolt-black | 要登入(頁面開得到,但價格被遮;登入網域 entry-point.com.au) | 零售價 520 特價 / 660 原價(web_reno_setup:61;meeting_1114_external_facts 3.32) | 頁面文字:「Prices are shown once you log in」、「Log in to see your pricing」、標籤「Save 30%」;頁面原始資料(不是畫面上看得到的價格):product:price:amount 550.00 AUD、另一欄 787.07 | 頁面沒標日期 | 不一樣:原始資料 550 / 787.07(折 30%)與筆記 520 / 660 對不上;畫面上的價格要登入才看得到,沒登入 |
| A9 | ATO | https://www.ato.gov.au/individuals-and-families/investments-and-assets/property-and-land/residential-rental-properties/rental-income-you-must-declare | 開到了 | T4 短租收入申報 5 點與「最後更新 2026-05-21」(web_opcost_housing_gapfill:80) | 頁面:要申報「short-term rentals」「renting your property through a sharing platform」「renting part or all of your home」;bond 留下代替租金、取消訂房留下的訂金/booking fee、保險賠償(含租金損失)都列為租金收入;範例寫「report the gross rent … before it's reduced by property management fees」;依法定持有比例申報(50% 就報 50%);經仲介的以房客付給仲介的年度為準;填在「You had Australian interest, or other Australian income or losses from investments or property」 | Last updated 21 May 2026 | 一樣(日期 2026-05-21 與 5 點都對上);小差異:頁面講的是扣除「代管費」之前的毛額,沒有明寫「平台費」 |
| A10 | HIA、Archicentre 裝修費用指南 | 沒開 | 沒做(工具次數用完) | HIA、Archicentre 費用指南數字(web_reno_setup:105;meeting_1114_external_facts 8.08) | 沒搜尋 | — | 看不到 |

## 「不一樣」或「新資料」白話說明

- A1 hipages(新資料):浴室翻新的三檔數字之前只有搜尋摘要,現在原頁(2026-01-21 更新)全部對上,而且頁面自己引用 HIA 2023 年全澳浴室平均 26,000。廚房是新的:全澳基本翻新約 30,000–50,000(2026-01-02 更新)。這些是全澳平均,不是雪梨專屬。
- A2 Domain:2026 年 9 月季那頁打不開(猜的網址 404、列表頁也 404、Google 也沒收),所以雪梨最新的季度租金還是只有 2025 年 9 月(獨棟 780、公寓 750)與 2025 年 12 月(獨棟 800)可用。
- A3 The New Daily(不一樣):頁面只說雪梨「掉 5 塊到 835」,沒有分公寓/獨棟。筆記的 L6 獨棟 850 對不上(頁面 9 月是 835),L5 公寓 780 在這頁看不到。所以 L5、L6 不要當這頁的數字引用。
- A4 OpenAgent(不一樣):筆記說的雪梨公寓 867,597、獨棟 1,466,060 這頁都沒有;頁面只有雪梨全住宅中位 1,178,959。要用這兩個數字得換 Cotality 原頁。
- A5 Flat Chat(新資料):850/季對得上,但那是 2024 年 6 月站長自己「快查」的估算,同時代的房價假設是 85 萬(2024),不是現在的行情,也不是統計。
- A6 Master Builders(新資料):雪梨房屋營造用料成本到 2025 年 9 月止一年漲 2.0%(全澳 2.1%)。注意這是材料,不含工資。
- A7 AER:官方原件沒拿到(轉到 AER 的登入頁,文字是寫給 AER 站務人員的),E2/E4/E6 仍然只有 Canstar 轉述。可能是草案檔已下架或搬位置,這點我沒查證。
- A8 Entry Point(不一樣):畫面價格要登入;頁面原始資料寫 550 與 787.07,和筆記的 520/660 不同。筆記的 520/660 不要再引用。

## 沒涵蓋

- A10(HIA、Archicentre)沒做。
- A7 沒有去找 AER 草案的新網址(Google 搜尋也沒用)。
- A6 只讀第 1 頁,其他頁沒讀。
- A2 沒找到 2026 年 9 月季。

## 工具呼叫次數

- Chrome 工具約 49 次(含幾次因網域變動被擋的重試),加上 Skill、ToolSearch、Grep 共約 54 次,超過上限 50 一點,所以 A10 沒做。Google 搜尋 3 次(Domain 2 次、hipages 1 次)。
