# 更正紀錄(2026-11-17):8 個過時的講法

> 這份記的是:我們筆記裡 8 個講法後來有更正或補了年度,以及這次改了哪些位置、哪些位置刻意沒改。scope IS-1117-FIX-A。
> 依據兩個檔:`Innovation Studio/notes/raw/teammate_download_list_check_2026-11-17.md`(表 3 列出要改的位置)與 `Innovation Studio/notes/raw/external_downloads_verify_2026-11-17.md`(14 個下載檔的開檔核對,表 2 與「和我們舊筆記不一樣的」)。
> 分法:「已核對」= 我們開了檔(有檔名加頁碼或儲存格)或開了原頁。原本只有 3 個(電費草案改最終版、ABS 雪梨建材指數 3.7%、North Sydney 市政費 970.72);2026-11-17 晚補查後增加 5 個(Airbnb 服務費頁、Inside Airbnb 申請頁、Domain 原頁、City of Sydney 議會原文、SXSW 公告),現在 8 個主題裡只剩 Blacktown 1,140 / 1,233 的年度還是「隊友查的,未核對」。補查細節見 `followup_checks_web_2026-11-17.md`(含最後一節「主腦用 Chrome 補查」)。

做法:現在還在用的檔(`data_inventory_2026-11-15.md`、`28_項目介紹簡報大綱_草稿.md`)加「〔2026-11-17 更正:…〕」,舊字不刪(只有 28 號檔第 5 頁那一句 US$500/800 改了字);11/14、11/11 當天的紀錄檔只在檔頭加一行指到這裡;11/14 組會的簡報頁、講稿、已分享的 PDF 完全沒動。

行號說明:「這次改了哪些位置」的 `data_inventory` 行號是改之前與改之後都一樣的(沒有插行)。11 個當天紀錄檔的提醒行加在**檔尾**(主腦驗收時從檔頭搬到檔尾,就是為了不讓行號移動),所以內文行號和表 3 寫的一樣,沒有位移。

| 主題 | 舊講法 | 現在的講法 | 依據 | 這次改了哪些位置 | 沒改的位置與原因 |
|---|---|---|---|---|---|
| 1. Airbnb「2025-12-01 全部改制」 | 有網站寫 2025-12-01 全部轉換(搜尋摘要,只供參考) | 整句不要用,不是改日期。以 Airbnb 官方服務費說明頁和房東自己收到的通知為準 | 已核對(2026-11-17,分身用 WebFetch 開 Airbnb 官方服務費頁 https://www.airbnb.com.au/help/article/1857;工具摘要):頁面沒有寫任何統一改制日期,整句不用。官方頁寫分攤制多數房東 3%、房客 14.1%–16.5%,單一服務費多數房東 15.5%,頁面說正在遷移 | `data_inventory_2026-11-15.md:183` 加更正;檔頭加提示:`meeting_1114_external_facts.md`(原 88、354)、`web_str_market_2026-11-14.md`(原 85、87)、`web_verify_str_market_2026-11-14.md`(原 72、119) | `meeting_1114/index.html:1533`(+ share)的 ext-data 2.12 列:當天頁面;該列備註本來就寫「不要用於簡報」,沒有當成事實 |
| 2. SXSW Sydney 2026 | 官網「憑證壞掉」/「被擋(憑證錯誤)」的舊狀態 | 2026 那屆取消(2026-01-14 公告);NSW 政府說 2026、2027 都不辦。這是我們 11/15 已經知道的事,只剩簡報頁還寫舊狀態 | Variety 報導,見 `data_inventory_2026-11-15.md:159`;abea.org.au 公告已核對(2026-11-17 晚,主腦用使用者 Chrome 開原頁:公告日 2026-01-14,原文 "will not proceed in 2026") | `data_inventory:159、168` 已經寫取消,不用改。檔頭加提示:`web_holidays_events_2026-11-14.md`(原 80)、`page_reconcile_v4_2026-11-14.md`(原 56) | `meeting_1114/index.html:1155、1514`(+ share):當天頁面,見下一節 |
| 3. Inside Airbnb 歷史資料 US$500 / US$800 | 「參考價 US$500 或 US$800」,像是二選一的報價 | 不是固定報價:價格按城市數和用途分類,要向站方問;另有到 2026-11-30 的舊價過渡安排。依隊友清單表 3 的備註,兩個數字是不同分類的 2 城價,不是二選一(已核對,見依據) | 已核對(2026-11-17,分身用 WebFetch 開官方申請頁 https://insideairbnb.com/data-requests/;是工具摘要,把握中):500 = 2 個城市且用途與站方使命相符(1 個城市、商業用途也是 500);800 = 2 個城市、商業用途;這是舊價表,新價 2026-11-01 起,2026-11-30 前送出的申請仍照舊價 | `data_inventory:207` 加更正;`28_項目介紹簡報大綱_草稿.md:65` 改字(這是唯一改了舊字的位置);檔頭加提示:`meeting_1114_internal_facts.md`(原 143)、`airbnb_history_sources_2026-11-11.md`(原 29、31、55、65)、`21_1111組會錄音整理.md`(原 79) | `meeting_1114/talk_script.md:106`、`index.html:824、1294`(+ share):當天簡報與講稿。`notes/15_…:18`、`notes/16_…:386` 本來就寫「指南、不是本組報價」,不用改 |
| 4. Domain 2026 年 9 月季報告網址與公寓 780 | 網址記到 `…/rental-report/september-2026-rental/`(404);公寓 780 只有 Elite Agent 轉述 | 隊友給的網址是 `https://www.domain.com.au/research/rental-report/september-2026/`(沒有 -rental 後綴);他寫原頁有獨棟 835、公寓 780、空置率 1.2%。2026-11-17 晚主腦用 Chrome 開原頁,看到雪梨中位週租 獨棟 $835、公寓 $780、空置率 1.2%,所以 780 已在原頁確認 | 已核對(2026-11-17 晚,主腦用使用者 Chrome 開 https://www.domain.com.au/research/rental-report/september-2026/ 原頁:獨棟 $835(季 −0.6%、年 +5.7%)、公寓 $780(季 0%)、空置率 1.2%) | `data_inventory:169` 加更正;`data_inventory:227` 加「新網址見第 169 行」;檔頭加提示:`web_chrome_recheck_A_2026-11-14.md`(原 12) | 無 |
| 5. Blacktown 1,140 / 1,233 與 North Sydney 市政費 | Blacktown 最低費率 1,140、平均 1,233「年度摘要沒寫清」;市政費「只有 North Sydney 最低費率、Blacktown 平均費,都沒有人開過原頁」 | Blacktown 1,140 屬 2025–26,不是 2026–27 最終費用;1,233 是哪一年仍不清楚(隊友查的,未核對)。North Sydney 2026–27 最低住宅費率 970.72 已開檔核對,只適用 North Sydney Council;2025–26 現行 743.85 | 970.72(已核對):`external_downloads_verify_2026-11-17.md` 表 1 的 1.09 與表 2「市政最低費率」;檔案 `1.09_IPART_North_Sydney_…pdf` p.8 Figure 1.2。Blacktown 年度:隊友清單 3.10,隊友查的,未核對(11/17 晚再查仍開不了:申請 PDF 太大開不了,預算新聞頁 2026-07-13 沒有 1,140、1,233,只寫一般費率收入總增幅 11.54%) | `data_inventory:190、222` 加更正;檔頭加提示:`web_opcost_housing_gapfill_2026-11-14.md`(原 57、62)、`web_verify_opcost_housing_2026-11-14.md`(原 70)、`meeting_1114_external_facts.md`(原 223) | `index.html:1533`(+ share)的 ext-data 4.28、4.29 列:當天頁面。4.28 的 970.72 本來就對;4.29 沒寫 1,140 屬 2025–26 |
| 6. City of Sydney 5,454 間 / 2,468 間 | 5,454 間活躍短租、2,468 間依 NSW 制度登記(沒寫年度,頁面寫「約 2025–2026」) | 這組數字指 2023 年,決議日期 2025-02-17,範圍只有 City of Sydney;不能寫成 2026 年的現況,也不是整個大悉尼 | 已核對(2026-11-17 晚,主腦用使用者 Chrome 開議會原文 https://meetings.cityofsydney.nsw.gov.au/mgDecisionDetails.aspx?IId=32031&Opt=1):原文 "according to NSW Government data, in 2023, there were 2,468 active and registered" 短租;同一句接著寫獨立資料有 5,454 間活躍;會議日期 17/02/2025;範圍 City of Sydney | `data_inventory:180` 加更正;檔頭加提示:`meeting_1114_external_facts.md`(原 68、352)、`web_str_market_2026-11-14.md`(原 97) | `index.html:1533`(+ share)的 ext-data 1.37 列:當天頁面,period 寫「約 2025–2026」 |
| 7. ABS 雪梨營造成本 | 「ABS 雪梨層級沒有」,只有 Master Builders NSW 雪梨材料 +2.0% | ABS 有雪梨層級:Producer Price Indexes Table 18「Input to the House construction industry」,雪梨 2026 年 9 月季年增 3.7%(指數 169.9、季增 0.9%)。這是房屋建築業的材料投入價格,不含人工,不能直接叫「裝修成本漲幅」 | 已核對:`1.05_ABS_PPI_Table18_sep_2026.xlsx` 工作表 Data1 儲存格 Q251(指數 C251、季增 J251);見 `external_downloads_verify_2026-11-17.md` 表 1 的 1.05 與表 2 | `data_inventory:216` 加更正 | 無(表 3 沒列到簡報頁或當天紀錄檔) |
| 8. 電費草案改最終版 | 2026-27 草案:Ausgrid 1,875、Endeavour 2,347、Essential 2,515;「最終版新聞稿沒有 Ausgrid 年電費和用電量」 | 最終版(含 GST):Ausgrid 平價 1,899(3,900 kWh)、Endeavour 平價 2,328(4,900 kWh)、Essential 平價 2,604、分時 2,530(4,600 kWh)。草案的 1,875 / 2,347 不要再用;2,515 對不上最終版任何一種。這是 DMO 基準用電量算的上限參考價,不是家戶實際平均電費 | 已核對:AER 最終決定 PDF p.16 Table 2.1;資訊包 p.4;見 `external_downloads_verify_2026-11-17.md` 表 2 與「和我們舊筆記不一樣的」 | `data_inventory:75、167、229` 加更正;檔頭加提示:`meeting_1114_external_facts.md`(原 196、287) | `index.html:1533`(ext-data 4.02、4.04、4.06、4.07)、`index.html:1712`(+ share):當天頁面,見下一節 |

## 之後如果要重用 11/14 的簡報頁,要先改這幾行

> **2026-11-17 晚:下表列的位置都已經改完**(`meeting_1114/index.html` 與分享版 HTML;手動改字,沒有重建)。另外主腦補改了同一段裡的 Domain、AER、Archicentre、旅遊局四個狀態,並在統計那一行下面加「11/17 更新」(11/14 當晚的統計數字保留原樣)。
> ⚠️ **不要直接跑 `build_page.py` 重建**:它會從 `notes/raw/meeting_1114_external_facts.md`(當天紀錄,沒改)重產那一段,把這些手改蓋回去。要重建,先把這些字改進來源。
> 沒改的:`share/` 裡 11/14 那份 PDF(當時的版本);頁面上用草案電費 1,875 算出來的每月粗估沒有重算(旁邊已加說明,一個月約差 2 元)。

下面這些位置這次完全沒動(11/14 組會當天的簡報頁、講稿、已分享的檔)。`share` 指 `Innovation Studio/meeting_1114/share/雪梨Airbnb房東定位助手_1114組會.html`,行號與 `meeting_1114/index.html` 相同(兩份內容一樣)。

| 位置 | 現在寫的 | 重用前要改成 |
|---|---|---|
| `index.html:824`(+ share) | 「…更早的要付錢跟官方申請,參考價 US$500 或 US$800,還沒申請。」 | 「…更早的要向官方申請;US$500、US$800 是之前看到的參考價,不是固定報價,要向站方問,還沒申請。」 |
| `talk_script.md:106` | 「更早的要付錢申請,參考價 US$500 或 US$800,還沒申請(B 段)」 | 同上口氣:「…不是固定報價,要向站方問,還沒申請(B 段)」 |
| `index.html:1155`(+ share) | chip「SXSW Sydney 官網(憑證壞掉)」;同一行的「AER 電費原始文件(要登入)」也過時 | 「SXSW Sydney:2026 取消(NSW 政府說 2026、2027 都不辦)」;AER 那個改成「最終版 PDF 已下載核對」 |
| `index.html:1294`(+ share) | 行尾「歷史資料申請:兩城 US$500 或 US$800,沒送出」 | 「歷史資料申請:價格按城市數和用途分類,US$500、US$800 不是固定報價,要向站方問;沒送出」 |
| `index.html:1514`(+ share) | 「SXSW Sydney · 被擋(憑證錯誤)」 | 「SXSW Sydney · 2026 取消」 |
| `index.html:1533`(+ share) | ext-data 的 JSON:1.37(City of Sydney 5,454 / 2,468,period「約 2025–2026」)、2.12(Airbnb 2025-12-01 改制)、4.02 / 4.04 / 4.06(電費草案 1,875 / 2,347 / 2,515)、4.07(官方原件待核對)、4.29(Blacktown 1,140) | 1.37 改成「指 2023 年,決議日期 2025-02-17,只有 City of Sydney」;2.12 整列拿掉;4.02 / 4.04 改成最終版 1,899 / 2,328,4.06 改成 Essential 2,604(平價);4.07 改成「最終版 PDF 已核對」;4.29 補「1,140 屬 2025–26(隊友查的,未核對)」。改完要重算同一段 JSON 的 stats 與 verdict 數量 |
| `index.html:1712`(+ share) | calc-r9「甲 已有房 · 電費(每月)」val「約 156 / 164 / 201」,f「1,875 ÷ 12;…」,chk「156.25」 | Ausgrid 改最終版:val 第一個數字改 158,f 改「1,899 ÷ 12」,chk 改「158.25」(3,900 kWh 平價,含 GST);另兩個(1,965、2,411)是 2025-26,維持 |
| `share/雪梨Airbnb房東定位助手_查過的資料清單_2026-11-15.pdf` | 11/15 版的資料清單,內容等於改之前的 `data_inventory` 對應列 | 要重做才會更新;重做時用現在加了更正的 `data_inventory_2026-11-15.md` |

## 沒做的

1. 沒 commit、沒 push,沒上網,沒重新開任何 PDF 或 Excel;已核對的 3 項完全沿用 `external_downloads_verify_2026-11-17.md` 的結果。
2. 沒改 D 列的 4 個位置群(簡報頁、share 版、講稿、11/15 版 PDF),沒重做 PDF、沒重建簡報頁;`handoff.md`、`TODO.md`、`Innovation Studio/refs/`、腳本都沒碰。
3. 〔2026-11-17 晚更新〕原本隊友查的 5 項裡,Airbnb 12/1、US$500/800 分類、Domain 網址與 780、City of Sydney 年度已核對(見上表依據欄);只剩 Blacktown 年度沒核對(11/17 晚再查仍開不了)。
4. 事件日曆有沒有還放著 SXSW,這次沒查。
5. 第三段「還缺哪些數據」的 2026-11-17 更新,為了不讓後面的行號往下移,接在該段開頭那一句的後面(同一行),沒有另起一個引言區塊;`data_inventory` 的行號(含 28 號檔第 5 頁「③ 依據」引用的 207、196、243 等)因此都沒變。
6. 11 個當天紀錄檔的提醒行在檔尾(最後一行),內文行號沒有變;別的筆記引用這些檔的行號照舊可用。
7. `data_inventory` 末段「數量對照」沒重算(沒新增或刪除列)。
8. Essential 2,515 是哪一種費率、Blacktown 1,233 是哪一年,都還沒解決(Domain 網址已解決,見上表第 4 列)。
