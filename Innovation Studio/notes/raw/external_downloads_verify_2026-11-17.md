# 外部下載檔核對(2026-11-17)

> scope IS-1117-VF-A。對象:`Innovation Studio/refs/external_2026-11-17/` 的 14 個檔(12 PDF、2 Excel,只讀)。方法:pypdf 逐頁抽字 + openpyxl 讀 Excel,再用關鍵字找頁、只讀命中的頁。抽字腳本與文字檔在 scratchpad(不進 repo):`C:\Users\kenny\AppData\Local\Temp\claude\476d15717a45c1e6\9b28e753-2dfd-40bc-8f43-9ccda1bb6ccb\scratchpad\verify_1117\`(`extract.py`、`abs_tail.py`、`gas_tail.py`、`txt\`)。
> 頁碼 = PDF 檔的第幾頁(不是文件印的頁碼;AER 最終版 PDF 第 16 頁 = 文件印的第 7 頁)。隊友講法取自這次任務清單,沒有逐項回頭對他的 HTML 原文。

## 結論

- 13 項裡:**對 12 項、部分對 1 項(1.06)、不對 0 項、找不到或抽不到 0 項**。
- 部分對的 1.06:Standard/Designer、一到三房、另加 GST 都對;但「2025 年版」只在網址與檔名,PDF 內文沒寫年份。
- 電費最終版對舊筆記草案:**有變**(Ausgrid +24、Endeavour −19;Essential 的 2,515 舊筆記沒寫是哪一種費率,最終版平價 2,604、分時 2,530,對不上)。
- 兩個要留意:1.14 TRA 完全沒有雪梨層級數字;1.12 Cotality 的雪梨租金年增靠文字順序推,要人眼看第 28 頁。

## 表 1 逐項核對

| 編號 | 隊友的講法 | 檔案裡的依據 | 結果 | 差在哪 |
|---|---|---|---|---|
| 1.01 | 兩個 AER PDF 是 2026–27 最終版(非草案);DMO 是照規定用電量算的基準,不是實際平均電費 | 最終版 `1.01_AER_final_…pdf` p.1 封面「Final determination … May 2026」;p.16 Table 2.1(標 inc. GST);資訊包 `1.01_AER_information_kit_…pdf` p.2「if they had an average annual level of household … consumption」、p.4 表 | 對 | 資訊包 p.10–11 還留有「in the draft determination」字樣,是文件殘留,不影響。資訊包 p.1 寫只有約 8% 家戶留在 DMO |
| 1.02 | IPART 瓦斯 Excel 有按地區與客戶類型的估算年度帳單時間序列 | `1.02_IPART_gas_data_appendix_2024-25.xlsx` 工作表 Contents B8–B9「time series data on estimated annual bills … by region and customer type」;29 張工作表,資料在「Historic Data - Gas Prices」(10,688 列) | 對 | 報告標題在 Contents B8 打成「2024-45」(原檔筆誤)。工作表名單見下方備註 |
| 1.03 | Archicentre 2026 年版;維修、裝修、擴建成本參考 | `1.03_Archicentre_CostGuide_2026.pdf` p.1「CostGuide 2026」;p.2–3「REPAIRS & MAINTENANCE」;p.4「RENOVATIONS & ADDITIONS」 | 對 | 沒標明是雪梨價,是全國通用指引;p.4 寫含 GST |
| 1.04 | Martina Hayes 基礎廚房 28,000–45,000;基礎浴室 25,000–30,000;分基礎、中檔、高檔 | `1.04_MartinaHayes_…pdf` p.1 表「Kitchen 28 to 45K / Bathroom 25 to 30K」,欄為 BASIC / MID-RANGE / HIGH END | 對 | 檔案寫「28 to 45K」(單位 AUD,見 p.1);廚房不含家電(p.3–4)、浴室含磁磚與配件(p.4) |
| 1.05 | ABS Table 18:2026 年 9 月季雪梨住宅建築材料投入價格指數,年增 3.7% | `1.05_ABS_PPI_Table18_sep_2026.xlsx` 工作表 Data1,序列「Percentage change from corresponding quarter of previous year ; All groups ; Sydney」(ID A2390419X)Q251 = 3.7,日期欄 2026-09-01;Index 表 B6 標題 | 對 | 準確名稱是「Input to the House construction industry」(房屋建築業的投入),「All groups」= 全部材料合計,不是單一建材。指數值 C251 = 169.9,季增 J251 = 0.9% |
| 1.06 | Vivin:不同臥室數、Standard 與 Designer 套裝與標價;2025 年版;另加 GST | `1.06_Vivin_…pdf` p.4「Standard Furniture Packages」「Designer Furniture package」「Available in one, two or three bedrooms」「FROM $ 5,999 +GST」等 | 部分對 | 年份:PDF 內文沒寫,只有網址路徑與檔名有 2025。臥室數與價格的對應靠文字順序(第 1 個價 = 一房),p.4 要人眼確認。其餘對 |
| 1.07 | Terri Scheer:NSW 新業務保費 A$525;註明價格可能調整 | `1.07_TerriScheer_…pdf` p.2「New Business Policy Premiums」表 New South Wales $525;「Pricing subject to change」 | 對 | 檔案另寫「新業務保費適用 2025-11-14 以後出單、2026-01-19 以後生效的保單」(p.2),這是 Holiday Rental(短租)保單。含不含 GST 檔案沒寫 |
| 1.08 | amaysim:2026-02-25 起有效;NBN 50 月費 A$85;NBN 100 是 A$90;另有入門優惠 | `1.08_amaysim_…pdf` p.1「Valid from 25/02/2026」;p.1 表 Minimum Monthly Charge NBN 50 = $85、NBN 100 = $90;入門價 $75 / $80 前 6 個月;p.2「$10 off for your first 6 months」 | 對 | 表頭叫「Minimum Monthly Charge」,不是「標準月費」。檔案寫該摘要不含促銷;含不含 GST 沒寫 |
| 1.09 | IPART North Sydney:2026–27 最低住宅費率 A$970.72 | `1.09_IPART_North_Sydney_…pdf` p.8 Figure 1.2「APROVED PATHWAY / Minimum rates」2026-27 Residential $970.72 | 對 | 這是核准的「路徑」數字;同表 2025-26 現行 $743.85。只適用 North Sydney 市議會 |
| 1.11 | SQM:含截至 2026-11-12 雪梨獨棟、公寓、合計「掛牌」週租 | `1.11_SQM_…pdf` p.3「Advertised Rents Analysis」Sydney 段;p.1 日期 12 November 2026;p.4 標題「Advertised Rents — Week Ending 12 November 2026」 | 對 | 是廣告掛牌租金(advertised),不是成交租金。p.3 寫「over the 30 days to 12 November」 |
| 1.12 | Cotality:2026 年 11 月 Housing Chart Pack;原始資料要聯絡機構;有雪梨租金/年增就抽出 | `1.12_Cotality_…pdf` p.1「Monthly Housing Chart Pack November 2026」;p.38「For access to the data, contact us.」;p.28「Annual change in rental rates to October 2026」 | 對 | 雪梨租金年增數字在圖裡,文字抽出來是一串無標籤的百分比,對應靠順序推(見第 5 節),沒放進表 2 |
| 1.14 | TRA:2026 年 10 月旅遊儀表板;(請寫清楚有無雪梨層級) | `1.14_TRA_ATDD_october_2026.pdf` p.1–6 每頁標題「Australian Tourism Data Dashboard - October 2026」 | 對 | **沒有雪梨層級數字。** 只有全國合計、州別(p.3「Stopovers by state」圖,NSW 在內)、首都市對區域的比例(p.3、p.6)。全是季或 12 個月滾動,沒有雪梨月別或淡旺季 |
| 1.15 | NSW STRA FAQ:大雪梨適用;房東不同住短租每年上限 180 天;連續 21 天以上訂單不計;2024 年版 | `1.15_NSW_STRA_FAQ.pdf` p.4「Non-hosted STRA is restricted to a maximum of 180 days per 365-day annual period」「the Greater Sydney region (not including the Central Coast)」;p.5「21 or more consecutive days … will not count」;p.1「Updated May 2024」 | 對 | 「不含 Central Coast」要一起講。年度是「從註冊日起算的 365 天」不是日曆年(p.5)。p.4 另列 Byron Shire 60 天(2024-09-23 起) |

備註 1.02 工作表(共 29 張):Contents、Historic Data - Gas Prices、3 Market overview & barriers to entry and expansion >、3.3-3.4 Gas demand、3.5-3.6 Connections、3.7-3.8 Number of retailers、3.9-3.10 Market share、3.11 Number of retailers、4 Trends in retail gas prices >、4.1-4.2 Prices 2020-25、4.3-4.4 Price changes 2020-25、4.5-4.6 Price changes_Regional、4.7-4.8 Gas offers_Regional、4.9-4.10 Price spread 2020-25、4.11-4.12 Price spread_Region、5 Changes in gas supply costs >、5.1 Total gas supply costs、5.2-5.3 Wholesale gas prices、6 Customer engagement, switching and complaints >、6.1 Customers on market offers、6.2 Switching numbers and rates、6.3-6.5 Savings、6.6 Reasons not review plan、6.7 EWON complaint numbers、7 Affordability, hardship and disconnections >、7.1 Concerned customers、7.2 Bill to income ratio、7.3-7.4 Hardship program、7.5 Rebate。(工作表實際名稱中的逗號、頓號以檔案為準;上表為節錄顯示。)

## 表 2 可以拿來用的數字

只收我在抽出的文字或儲存格裡親眼看到、且有頁碼或儲存格的數字。

| 項目 | 數字 | 單位 | 年度或生效日 | 適用範圍 | 含 GST? | 出處 | 提醒 |
|---|---|---|---|---|---|---|---|
| DMO 住宅平價(flat rate)Ausgrid | 1,899;年用電 3,900 kWh | A$/年;kWh | 2026-27,2026-07-01 起 | NSW,Ausgrid 配電區,住宅;價格是 DMO 基準用電量算出來的 | 含(Table 2.1 標 inc. GST) | 最終版 PDF p.16;資訊包 p.4 | 是規定基準用電量算的上限參考價,不是家戶實際平均電費 |
| 同上,分時(TOU) | 1,893 | A$/年 | 同上 | 同上,3,900 kWh | 含 | 最終版 p.16;資訊包 p.4 | 需有智慧電表 |
| DMO 住宅平價 Endeavour | 2,328;4,900 kWh | A$/年;kWh | 同上 | NSW,Endeavour 配電區,住宅 | 含 | 最終版 p.16;資訊包 p.4 | 同上 |
| 同上,分時 | 2,320 | A$/年 | 同上 | 4,900 kWh | 含 | 最終版 p.16 | 同上 |
| DMO 住宅平價 Essential | 2,604;4,600 kWh | A$/年;kWh | 同上 | NSW,Essential 配電區,住宅 | 含 | 最終版 p.16;資訊包 p.4 | 同上 |
| 同上,分時 | 2,530 | A$/年 | 同上 | 4,600 kWh | 含 | 最終版 p.16 | 同上 |
| 2025-26 同區前一年平價 | Ausgrid 1,965;Endeavour 2,411;Essential 2,741 | A$/年 | 2025-26 | 同上 | 含 | 資訊包 p.4 | 用來算年變化:Ausgrid −3.4%、Endeavour −3.4%、Essential −5.0%(資訊包 p.4) |
| 雪梨住宅瓦斯 市場方案中位數(Metro,即 Jemena 雪梨網路) | 1,249.96(29 個方案) | A$/年 | 2025-09-15 快照(報告為 2024-25) | 住宅、單一費率、用量 24,400 MJ、all retailers | 工作表沒寫;4.1 表標題寫 incl. GST | `1.02` 工作表 Historic Data - Gas Prices,第 10679 列 I 欄 | 「Metro」= Jemena 雪梨網路是我從 2018 年兩者數字完全相同推的(同表第 91、93 列),檔案沒明講 |
| 同上,待機(standing)方案中位數 | 1,482.80(13 個方案) | A$/年 | 2025-09-15 | 同上 | 同上 | 同工作表第 10682 列 I 欄 | 同上 |
| Jemena Coastal 住宅瓦斯 2025 年 6 月 | 10 百分位 1,065.41;市場中位 1,195.42;待機中位 1,523.74 | A$/年 | 2025-06-19 | Jemena Coastal 網路、住宅 | 含(表標題「$ nominal, incl. GST」) | `1.02` 工作表 4.1, 4.2 Prices 2020-25,第 54 列 C、D、E 欄 | 這張表沒寫用量;和上面 Metro 數字是不同日期、不同分組,不要混在一起比 |
| 廚房/浴室基礎價(Martina Hayes) | 廚房 28,000–45,000;浴室 25,000–30,000;(中檔:廚房 45–75K、浴室 30–45K) | A$ | 2026 | 雪梨,持牌建商施工 | 含(p.3) | `1.04` p.1 表;p.3 GST | 廚房不含家電(p.3–4);建議加 20% 預備金(p.4) |
| 浴室、廚房、油漆(Archicentre) | 浴室/套房 17,500–35,000;廚房 23,000–49,000;洗衣間 10,000–19,000;室內粉刷(一底漆二面漆)20–40/m²;外牆木作狀況好 25–60/m²、差 45–80/m² | A$;A$/m² | 2026 | 全國通用指引,假設標準建材、可順利施工 | 含(p.4) | `1.03` p.4(濕區)、p.3(PAINTING) | 白色家電另加(p.4);不是雪梨專屬價 |
| 雪梨建材投入價格指數 | 年增 3.7%;指數 169.9;季增 0.9% | %;指數 | 2026 年 9 月季 | 雪梨,房屋建築業投入,All groups | 不適用(指數) | `1.05` Data1 Q251、C251、J251 | 前幾季:2026-06 年增 3.5、2026-03 年增 2.6、2025-12 年增 2.0(Data1 Q250、Q249、Q248) |
| 家具套裝標價(Vivin) | Standard:5,999 / 7,999 / 9,999;Designer:8,499 / 10,999 / 12,999(一/二/三房,依文字順序) | A$,「FROM」起價 | 小冊(網址年份 2025) | 主要 NSW;不含白色家電與戶外;Premium Luxury 另詢價 | 不含,另加 GST | `1.06` p.4、p.25 | 一房、二房標價 = 5,999、7,999(Standard);8,499、10,999(Designer),**臥室對應要人眼看 p.4** |
| 短租保險(Terri Scheer) | NSW 525;其他州:SA 405、WA 405、VIC 415、ACT 429、TAS 375、NT 395、QLD 459 | A$/年(新業務保費) | 2025-11-14 後出單且 2026-01-19 後生效的保單 | Holiday Rental 保單;新業務,不是續保 | 檔案沒寫 | `1.07` p.2 | 「Pricing subject to change」;理賠自負額:租金損失無、房客損壞 500、寵物/灼傷 250(p.2) |
| 網路月費(amaysim) | NBN 25:70;NBN 50:85;NBN 100:90;入門價前 6 個月 75(NBN 50)、80(NBN 100) | A$/月 | 2026-02-25 起 | 家用 NBN,月對月無合約,自備數據機 | 檔案沒寫 | `1.08` p.1 | 摘要寫不含促銷;NBN 新開發區啟用費 $300(p.2) |
| 市政最低費率 | 2026-27:970.72(住宅與商業相同);2025-26 現行 743.85;2027-28:1,116.32;2028-29:1,216.79 | A$/年 | 2026-27 起 | 僅 North Sydney Council | 不適用 | `1.09` p.8 Figure 1.2 | 是核准路徑,別的市議會不同 |
| 雪梨掛牌週租 | 合計 918.95;獨棟 1,175.11;公寓 743.95 | A$/週 | 截至 2026-11-12 | 雪梨,SQM 網路掛牌租金 | 租金不適用 | `1.11` p.3 | 掛牌價 ≠ 成交價。公寓年增 2.0%(p.3);雪梨空置率 1.8%,13,872 戶(p.1 表) |
| 全國租金年增(Cotality) | 全國 5.3%;首都市合計 5.2%;區域 5.5% | % | 到 2026 年 10 月的年增 | 全國(含雪梨在內) | 不適用 | `1.12` p.28 | 雪梨單獨的數字見第 5 節 |
| 短租日數規定(NSW) | 180 天/365 天;21 連續天以上不計 | 天 | 2024 年 5 月更新版 | 大雪梨(不含 Central Coast),房東不同住(non-hosted) | 不適用 | `1.15` p.4、p.5 | 房東同住(hosted)無日數限制(p.4) |
| TRA 全國旅遊(只在需要大環境數字時用) | 12 個月到 2026 年 6 月:總旅客消費 200.6bn;國內過夜消費 108.1bn;國際 40.5bn | A$ | 到 2026-06 | 全國 | 不適用 | `1.14` p.3 | **無雪梨數字**,不要當成雪梨用 |

## 和我們舊筆記不一樣的

只列差異與位置,沒有改舊筆記。

| 舊筆記位置 | 舊筆記寫的 | 檔案裡的 | 差 |
|---|---|---|---|
| `data_inventory_2026-11-15.md` 第 75 行 | Ausgrid 單一費率住宅 2025-26 年電費 1,965;2026-27 **草案 1,875** | 最終版 Ausgrid 平價 **1,899**(3,900 kWh);2025-26 前一年 1,965 與舊筆記一致(資訊包 p.4) | 草案 → 最終 **+24** |
| 同第 75 行 | Endeavour 2,411;**草案 2,347** | 最終版 Endeavour 平價 **2,328**(4,900 kWh);2,411 一致 | 草案 → 最終 **−19** |
| 同第 167 行 | Essential **2,515**(沒寫是哪種費率、也沒寫用電量) | 最終版 Essential 平價 **2,604**(4,600 kWh)、分時 2,530;2025-26 前一年 2,741 | 2,515 對不上任一種。若當成分時比,差 +15;若當成平價比,差 +89。舊筆記沒說清楚,**不能判斷是哪種**。這一區也不在第 75 行(Canstar)裡,第 167 行是在列「要核對的」 |
| 同第 75 行對費率的種類 | 「單一費率」 | 最終版有平價/分時/Solar Sharer 三種;「單一費率」對應平價 | 舊筆記講的對得上最終版的平價欄 |
| 同第 167 行 | 「最終版新聞稿沒有 Ausgrid 年電費和用電量」 | 最終版 PDF p.16 與資訊包 p.4 有 | 現在補上了(用電量 3,900 / 4,900 / 4,600 kWh) |

「沒有可控負載」:最終版 Table 2.1(p.16)沒有寫「without controlled load」字樣;可控負載(CL1、CL2)在另外的費率上限(p.21 Figure 2.6,「separate controlled load DMO tariff caps」),所以平價欄應是不含可控負載的主費率。但 p.14 另寫用電量基準「including the controlled load amounts」,指基準資料的處理;表 2.1 的 3,900 / 4,900 / 4,600 kWh 到底含不含可控負載,檔案文字沒有直接講,**這點未確認**。

## 沒做的/要人眼看的

1. 1.06 Vivin p.4:價格與臥室數的對應靠文字順序,要看圖確認;其餘頁(p.5–31)是圖片頁,抽不到字(沒有價格文字,不是漏抽)。
2. 1.12 Cotality p.28:圖的文字是一串沒有標籤對應的百分比(順序似乎是 Sydney 4.0%、Melbourne 4.5%、Brisbane 6.5%、Adelaide 6.3%、Perth 7.5%、Hobart 8.4%、Darwin 11.4%、Canberra 3.2%),但這是我從城市名單順序推的,沒有確認,**所以沒放進表 2**。要人眼看第 28 頁。
3. 1.14 TRA:沒有雪梨層級數字,也沒有月別或淡旺季資料(只有季和 12 個月滾動)。若要雪梨淡旺季得改找別的資料(隊友清單提到的 DoTS 入口,這次沒抓)。
4. 1.01 最終版共 152 頁,只用關鍵字讀了 p.1、p.14、p.16、p.21;沒讀其他頁的成本明細。Excel 轉文字只倒前 60 列;1.02 與 1.05 的最新列用另外的小腳本(`gas_tail.py`、`abs_tail.py`)讀,不在 repo。
5. 1.02 Metro 與 Jemena 是同一網路的推論(見表 2);GST 標示只有 4.1 表標題,歷史工作表表頭沒寫。
6. 1.07 保費含不含 GST、1.08 月費含不含 GST,檔案沒寫,表 2 已標「檔案沒寫」。
7. 隊友 HTML 原文這次沒逐項回頭 Grep;核對用的是任務清單裡抄的講法。
