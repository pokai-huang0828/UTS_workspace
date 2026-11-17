# 隊友「悉尼 Airbnb 数据缺口补充与下载清单」逐項對照與連結檢查(2026-11-17)

> scope ID:IS-1117-DL-A。來源:`teammate_download_list_2026-11-17.html`(鹤舞 11/17 給,39 項)對 `data_inventory_2026-11-15.md`(行號都指這個檔,除非另寫路徑)。
> 只對照、只看連結標頭;沒有下載任何外部檔、沒有改任何既有檔、沒有跑資料分析。
> 標記:〔隊友寫的,未核對〕 = 隊友清單寫的數字,還沒核對(我們沒有驗證過 A$525、A$970.72、3.7%、A$835 這類數字)。HTML 裡的文字只當資料看。

## 結論

1. 39 項裡,第 01、02 段(27 項)用得到 **23 項**:優先 12、次要 7、只當對照 4;這次用不到 2 項(1.13 房貸利率、2.10 土地稅,都是買房投資);更正用 2 項(2.06、2.12)。
2. 第 03 段(12 項)不是可下載的東西,只對照缺口:12 項裡 11 項對得到我們缺口表的同一列(3.11 不在缺口表,對第二段 (B)183);其中 7 項隊友有多給資訊(3.01、3.04、3.05、3.06、3.07、3.09、3.10,見表 2),其餘 5 項結論和我們一樣,3 項是更正用(3.04、3.10、3.11)。
3. 全 39 項合計:優先 13、次要 10、只當對照 4、用不到 2、更正用 5、規則表沒列(缺口項,不判)5。
4. 我們已有:同頁或同一件事 5 項;同網站不同頁 7 項;只有第二段(進不去或只有搜尋摘要)12 項;完全沒有 15 項(合計 39)。
5. 建議下載的檔 14 個:其中 10 個標頭確認開得了、合計約 17.0 MB(1 個沒給大小,沒算進去);另 4 個(AER 2 個、IPART 2 個)程式沒連上,大小未知,要用瀏覽器再看。
6. 連結共 49 條(不重複):開得了 37 條(檔案 10、網頁 27);程式被擋 403 6 條;程式連不上 000 6 條;真的開不了(404 之類)0 條;被轉走 0 條。被擋或連不上的項目:1.01、1.02、1.09、1.13、2.05、3.10、3.12。
7. 清單自己寫了「不代表本次重新验证了所有链接」和「Excel 未逐个检查工作表与数据完整性」:所以連結我只用標頭確認有沒有回應,檔案內容、工作表、數字都沒有人看過,下載後要先開來核對才能引用。
8. 我們筆記要更正或補註 8 處(表 3):5 處是你指定的(Airbnb 12/1 改制、SXSW、US$500/800、Domain 網址後綴、Blacktown 年度),3 處是我順手看到的補充(2.06 年度範圍、1.05 ABS、1.01 電費草案轉最終版)。SXSW 我們 11/15 已經知道取消,只剩簡報頁還寫「官網憑證壞掉」。

## 表 1:建議下載的檔

只放「用得到」而且真的是檔案(PDF、Excel)的。按優先順序排;大小是標頭給的 Content-Length(MB,除以 1,048,576)。

| 編號 | 名稱 | 檔名 | 來源網域 | 類型與大小 | 補我們哪個缺口(行號) | 用途等級 | 連結狀態 |
|---|---|---|---|---|---|---|---|
| 1.01 | AER 2026–27 最終決定 | `AER - Final determination - Default market offer 2026–27.pdf` | aer.gov.au | 未驗到(預期 PDF) | 229(電費) | 優先 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 1.01 | AER Information Kit | `Information Kit - Default Market Offer - 2026-27_0.pdf` | aer.gov.au | 未驗到(預期 PDF) | 229(電費) | 優先 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 1.02 | IPART NSW 瓦斯數據附件 | `Data-appendix-Monitoring-the-NSW-retail-gas-market-2024-25-November-2025.XLSX` | ipart.nsw.gov.au | 未驗到(預期 Excel) | 225(瓦斯) | 優先 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 1.07 | Terri Scheer 短租保險 PDF | `terri-scheer-holiday-rental-insurance-english.pdf` | terrischeer.com.au | PDF,0.20 MB | 223(保險) | 優先 | 開得了,是檔案(PDF,0.20 MB) |
| 1.08 | amaysim NBN 套餐說明 PDF | `Critical-Info-Summary-amaysim-Home-Internet-Plans.pdf` | amaysim.com.au | PDF,0.13 MB | 204(網路) | 優先 | 開得了,是檔案(PDF,0.13 MB) |
| 1.09 | IPART North Sydney 最終報告 | `Final-Report-North-Sydney-Council-Special-Variation-and-Minimum-Rate-2026-27-(1).PDF` | ipart.nsw.gov.au | 未驗到(預期 PDF) | 222(市政費) | 優先 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 1.14 | TRA 2026 年 10 月旅遊儀表板 | `atdd-october-2026.pdf` | tra.gov.au | PDF,2.46 MB | 211(淡旺季) | 優先 | 開得了,是檔案(PDF,2.46 MB) |
| 1.15 | NSW 官方 STRA FAQ | `faq-short-term-rental-accommodation.pdf` | planning.nsw.gov.au | PDF,0.18 MB | 210(天數上限) | 優先 | 開得了,是檔案(PDF,0.18 MB) |
| 1.03 | Archicentre 2026 Cost Guide | `CostGuide-2026.pdf` | archicentreaustralia.com.au | PDF,沒給 | 215、203(裝修) | 次要 | 開得了,是檔案(PDF,沒給) |
| 1.04 | Sydney Renovation Cost 2026 | `6202YENDYSTSOCNOITAVONER.pdf` | martinahayes.com.au | PDF,0.95 MB | 217、203(厨房浴室) | 次要 | 開得了,是檔案(PDF,0.95 MB) |
| 1.05 | ABS Table 18 建築材料價格指數 | `6427018.xlsx` | abs.gov.au | Excel,0.19 MB | 216(營造成本) | 次要 | 開得了,是檔案(Excel,0.19 MB) |
| 1.06 | Vivin 家具套裝 PDF | `Vivin-Furnishings-Just-Furniture-Packages-Brochure-2025_compressed.pdf` | vivinfurnishings.com.au | PDF,7.50 MB | 219(家具) | 次要 | 開得了,是檔案(PDF,7.50 MB) |
| 1.11 | SQM 全國空置率報告 2026-10 | `SQM-National-Vacancy-Rates-October-2026-17-11-2044.pdf` | sqmresearch.com.au | PDF,0.76 MB | 226(長租對照) | 對照 | 開得了,是檔案(PDF,0.76 MB) |
| 1.12 | Cotality 2026-11 Housing Chart Pack | `202611 Cotality Monthly Housing Chart Pack - November.pdf` | discover.cotality.com | PDF,4.61 MB | 226、227(長租對照) | 對照 | 開得了,是檔案(PDF,4.61 MB) |

合計:標頭確認的檔 10 個,約 17.0 MB(Archicentre 沒給大小,沒算)。沒列進來的:1.10 NSW 租金表和 TRA 的 DoTS 只有「下載入口頁」、不是現成檔;1.13 RBA F6 是 Excel 但房貸利率這次用不到。

## 表 2:39 項逐項對照

規則:用不用得到只照小組 11/14 定的範圍與你給的規則表判斷;第 03 段只對照缺口,規則表有對到類別的才判,沒有的寫「規則表沒列」。「我們已有嗎」分四種:已有(同頁或同一件事)/同網站不同頁/只有第二段(進不去或只有搜尋摘要,沒人開過原頁)/沒有。行號 = `data_inventory_2026-11-15.md`。

| 編號 | 名稱 | 類型 | 對應我們缺口(行號) | 我們已有嗎 | 用不用得到 | 一句理由 |
|---|---|---|---|---|---|---|
| 1.01 | AER 2026–27 最終版電費 | 檔案 | 229「2026-27 電費最終版與 AER 官方原件」(另 204) | 只有第二段:(A)167 草案頁進不去;草案數字 1,875/2,347/2,515 在 75、167 | 用得到・優先 | 每月固定成本(電);我們現在只有草案與 Canstar 轉述,最終版是升級。DMO 是基準用電量算的,不是實際帳單 |
| 1.02 | NSW 瓦斯費用(IPART 2024–25 附件) | 檔案 | 225「雪梨瓦斯年均帳單」(另 204) | 只有第二段:(B)186 比價站 730–1,320/年(同主題,另一來源) | 用得到・優先 | 每月固定成本(瓦斯);政府來源可取代比價站數字,但不是房源實付 |
| 1.03 | Archicentre 2026 裝修費用指南 | 檔案 | 215「HIA、Archicentre、Cordell、Rawlinsons 費用指南」(另 203) | 沒有(171 只寫『沒去查』) | 用得到・次要 | 「先改哪裡」的花費參考;我們資料沒有裝修欄 |
| 1.04 | 悉尼厨房浴室装修费用(Martina Hayes) | 檔案 | 217「雪梨專屬浴室、廚房費用指南」(另 203) | 沒有(同類只有 hipages 全澳平均,217) | 用得到・次要 | 裝修花費參考;基礎厨房 A$28,000–45,000 等〔隊友寫的,未核對〕;是設計公司參考預算 |
| 1.05 | ABS 悉尼建築材料價格(Table 18) | 檔案 | 216「雪梨層級的營造成本年增(ABS)」 | 同網站不同頁:abs.gov.au sep-2026 發布頁(67) | 用得到・次要 | 裝修費會不會變貴的參考;悉尼同比 3.7%〔隊友寫的,未核對〕。我們 216 寫『ABS 雪梨層級沒有』,要對這張表(見表 3) |
| 1.06 | 澳洲一房與兩房家具套裝(Vivin PDF) | 檔案 | 219「澳洲業者 1/2 臥室家具套裝標價」 | 沒有(219 只有 Airbtics 合計) | 用得到・次要 | 家具價格參考;2025 年版、另加 GST |
| 1.07 | 保險公司公布的短租保險價(Terri Scheer) | 檔案 | 223「保險公司公布的房東/短租保險費率」(另 204) | 只有第二段:(B)191 rakidzich 行銷文 500–700/年(同主題,另一來源) | 用得到・優先 | 每月固定成本(保險);NSW 新業務保費 A$525〔隊友寫的,未核對〕,最終以報價為準 |
| 1.08 | NBN 50 / 100 月費原件(amaysim) | 檔案 | 204「成本(電、水、瓦斯、網路、管理費、保險)」 | 只有第二段:(B)187、188 NBN 價(Mozo、Canstar、Finder 摘要,同主題) | 用得到・優先 | 每月固定成本(網路);NBN 50 A$85、NBN 100 A$90〔隊友寫的,未核對〕,是單一業者套餐不是市場平均 |
| 1.09 | North Sydney 年度市政費原件(IPART/Council) | 檔案 | 222「雪梨一般公寓的年度市政費」 | 只有第二段:(B)189 同一個 970.72(IPART 另一份檔,只有搜尋摘要) | 用得到・優先 | 每月固定成本(市政費);最低費率 A$970.72〔隊友寫的,未核對〕,不等於全年全部市政帳單 |
| 1.10 | NSW 政府租金報告與歷史表 | 檔案(只有下載入口頁) | 226「NSW 政府租金報告、SQM、Cotality」 | 沒有(226 寫『沒查到』) | 用得到・只當對照 | 長租租金,短租對長租的對照 |
| 1.11 | SQM 悉尼周租金與空置率 | 檔案 | 226 | 沒有 | 用得到・只當對照 | 長租租金與空置率對照;挂牌價不是成交價 |
| 1.12 | Cotality 房價與租金原始報告 | 檔案 | 226、227 | 沒有(第一段只有 CommBank、The New Daily 轉述,96、98) | 用得到・只當對照 | 只取其中租賃圖表當對照;房價圖表那一半這次用不到 |
| 1.13 | 自住與投資房貸利率(RBA F6) | 檔案 | 224「投資客房貸利率」 | 同網站不同頁:rba.gov.au cash-rate(100) | 這次用不到 | 房貸利率屬買房投資,題目不做(224 也寫不做) |
| 1.14 | TRA 旅遊數據公開下載 | 檔案(含下載入口頁) | 211「Tourism Research Australia 每月旅客頁」 | 只有第二段:(A)170 同站進不去;第三個連結 destinationnsw.com.au 同站不同頁(135) | 用得到・優先 | 淡旺季/旅遊資料;清單自己寫了不能當逐月入住率 |
| 1.15 | NSW 短租天數規則原件(STRA FAQ) | 檔案 | 210「NSW 2025–2026 修法結果」 | 同網站不同頁:planning.nsw.gov.au/STRA(42) | 用得到・優先 | 風險點(天數上限);180 天、21 天以上豁免是清單寫的〔隊友寫的,未核對〕,FAQ 為 2024 年版要配現行政策頁 |
| 2.01 | 一房/兩房整戶公寓油漆價格 | 網頁 | 212「1 房/2 房整戶公寓油漆的來源價」 | 沒有 | 用得到・次要 | 裝修花費參考;一房約 A$1,800–2,800〔隊友寫的,未核對〕,商家報價 |
| 2.02 | 木地板打磨上漆價格 | 網頁 | 213「木地板翻新價」 | 沒有 | 用得到・次要 | 裝修花費參考;A$40–70/㎡〔隊友寫的,未核對〕,網站自承部分依據沒留,低信心 |
| 2.03 | 床單洗滌與按換客次數收費 | 網頁 | 221「床單洗滌費」(另 204) | 沒有 | 用得到・優先 | 每月固定成本(洗滌);A$6.50/kg、一房每次 A$45〔隊友寫的,未核對〕,是 Northern Beaches 的店,未含 GST |
| 2.04 | 有樣本來源的公寓管理費(Before You Buy) | 網頁 | 228「有統計來源的雪梨公寓管理費」 | 沒有(同主題 79–81 是 Microburbs、Flat Chat、Stratachecks) | 用得到・優先 | 每月固定成本(管理費);季度中位數 A$1,368〔隊友寫的,未核對〕,是 NSW 樣本不是悉尼 |
| 2.05 | Domain 2026 年 9 月季租金報告 | 網頁 | 227「Domain 租金報告…官方原頁」 | 只有第二段:(A)169 我們打不開;第一段 94 是 2025 年 9 月版 | 用得到・只當對照 | 長租租金與空置率對照;悉尼獨棟 A$835、公寓 A$780、空置率 1.2%〔隊友寫的,未核對〕。網址要更正(表 3) |
| 2.06 | 5,454 間活躍 / 2,468 間登記短租(City of Sydney) | 網頁 | 不在我們的缺口表(第二段 (B)180 有同一組數字) | 只有第二段:(B)180 | 更正用 | 這組數字是 2023 年、只有 City of Sydney、不是大悉尼(清單寫的,見表 3) |
| 2.07 | 2026-04-28 市議會短租動議 | 網頁 | 不在我們的缺口表(第二段 (B)181 有同一件事,來源是低品質新聞稿頁) | 只有第二段:(B)181 | 用得到・優先 | 風險點(法規);官方議會記錄可替換 181 的低品質來源;議會動議不是州法 |
| 2.08 | Airbnb 分攤服務費 | 網頁 | 不在我們的缺口表 | 同網站不同頁:第一段 43(simplifying-airbnb-service-fees)、(B)182 舊制 3%/14.1–16.5% | 用得到・優先 | Airbnb 服務費;大多數房東約 3%、房客 14.1%–16.5%、單一費 15.5%〔隊友寫的,未核對〕;頁面說正在遷移 |
| 2.09 | Airbtics 兩房開辦費 A$7,539 | 網頁 | 219「澳洲業者 1/2 臥室家具套裝標價」 | 已有(第一段 60 同網址;(B)185) | 用得到・次要 | 開辦/家具參考;我們早就標了『頁面前後不一致』,清單也同意 |
| 2.10 | NSW 土地稅一般稅率 | 網頁 | 不在我們的缺口表(46 標『屬買房投資,只留紀錄』) | 同網站不同頁:revenue.nsw.gov.au(第一段 46;(B)184) | 這次用不到 | 土地稅屬買房投資,題目不做 |
| 2.11 | 設施與 Airbnb 價格關係研究(Macquarie) | 網頁 | 220「澳洲裝修或設施升級對價格、住滿率影響的研究」 | 沒有(220 寫『沒找到』) | 用得到・優先 | 設施與價格關係的研究,報告可引用;清單說沒核實到免費全文,也不能證明加某設施多賺幾% |
| 2.12 | SXSW Sydney 2026 不辦(abea.org.au 公告) | 網頁 | 不在我們的缺口表(第一段 159、第二段 (A)168 提到) | 已有(159、168:我們 11/15 已知 2026 取消;來源是 Variety) | 更正用 | 我們已知取消,不用改事實;只剩簡報頁還寫『官網憑證壞掉』(表 3)。公告可當第二個來源 |
| 3.01 | 實際成交價、入住晚數、按房型實際收入 | 缺口 | 200、201、208 | 同網站不同頁:airroi.com(31;201 的 49.5%) | 規則表沒列(缺口項,不判) | 同一缺口。隊友多給:AirROI data-portal 欄位清單(reserved_days 等);清單自己說沒驗證能免費下載,不是官方流水 |
| 3.02 | AirDNA 月度入住率、ADR、供給子頁 | 缺口 | 209 | 已有(30 同網址;154、155、172) | 規則表沒列(缺口項,不判) | 同一缺口、結論一樣(要付費、SAMPLE 不能用);沒多給資訊 |
| 3.03 | 日曆每日價格與 2025 年 12 月缺失價格 | 缺口 | 202、206 | 已有(20、157 Inside Airbnb get-the-data) | 規則表沒列(缺口項,不判) | 同一缺口、結論一樣(補不回);沒多給資訊 |
| 3.04 | 缺少 2025 年 9 月數據(歷史資料申請) | 缺口 | 207 | 已有(20、157;207 寫 US$500 或 US$800) | 更正用 | 同一缺口。隊友多給:US$500/800 不是固定報價、舊價過渡到 2026-11-30〔隊友寫的,未核對〕(表 3) |
| 3.05 | 房東自住或投資身份 | 缺口 | 205 | 只有第二段:(B)180 同一份議會文件 | 規則表沒列(缺口項,不判) | 同一缺口、結論一樣(不做);隊友多給:議會原文承認主要居所識別資料不足 |
| 3.06 | 悉尼連續月度旅客人數 | 缺口 | 211 | 沒有(211、(A)170 都進不去) | 用得到・優先 | 淡旺季/旅遊資料;隊友多給:TRA 舊 NVS 月度 2023-12 結束、2025 方法變更,拼接要小心 |
| 3.07 | 悉尼家具月租實價 | 缺口 | 218 | 沒有(218 寫『查不到』) | 用得到・次要 | 同一缺口、結論一樣(沒公開月價);隊友多給:Pabs 悉尼暫不接新咨詢 |
| 3.08 | 浴室整間每平方米單價 | 缺口 | 214 | 沒有 | 用得到・次要 | 同一缺口、結論一樣(沒有統一單價);沒多給資訊 |
| 3.09 | HIA、Rawlinsons、Cordell 完整指南 | 缺口 | 215 | 沒有(171 沒去查) | 用得到・次要 | 同一缺口。隊友多給:HIA 要帳號/購買、Rawlinsons 是商業書、免費替代 = Archicentre(1.03) |
| 3.10 | Blacktown A$1,140 與 A$1,233 | 缺口 | 222(另 (B)190) | 只有第二段:(B)190 | 更正用 | 同一缺口。隊友多給:1,140 屬 2025–26,不能當 2026–27(表 3)〔隊友寫的,未核對〕 |
| 3.11 | Airbnb 2025 年 12 月 1 日全部改制 | 缺口 | 不在缺口表(第二段 (B)183 有這說法;第三段 231 概括『搜尋摘要來源要核對』) | 只有第二段:(B)183 | 更正用 | 隊友查不到官方依據、建議刪;我們早就標為只供參考(表 3) |
| 3.12 | ATO 獨立查核 | 缺口 | 230 | 同網站不同頁:ato.gov.au(第一段 47;150) | 規則表沒列(缺口項,不判) | 同一缺口、結論一樣(獨立查核直接開是 403);沒多給資訊 |

列數對賬:01 段 15 + 02 段 12 + 03 段 12 = 39 列(隊友標的 15+12+12=39)。

## 表 3:我們筆記要更正的

只列位置,沒有改任何檔。路徑都在 `Innovation Studio/` 底下;`share/…` 指 `meeting_1114/share/雪梨Airbnb房東定位助手_1114組會.html`,行號與 `meeting_1114/index.html` 同(兩份內容一樣)。

| 哪一項 | 隊友的講法 | 我們哪個檔哪一行寫了舊講法 | 現況與要改的方向 |
|---|---|---|---|
| 3.11 Airbnb 2025-12-01 全部改制 | 查不到支持這個統一日期的官方依據,建議刪掉,以官方服務費說明 + 房東自己的遷移通知為準 | `notes/raw/data_inventory_2026-11-15.md:183`;`meeting_1114/index.html:1533`(+ share);`notes/raw/meeting_1114_external_facts.md:88、354`;`notes/raw/web_str_market_2026-11-14.md:85、87`;`notes/raw/web_verify_str_market_2026-11-14.md:72、119` | 我們這幾處都已標「搜尋摘要,只供參考/未查/不要用於簡報」,沒有寫成事實。要改的是:整句拿掉,不是改日期 |
| 2.12 SXSW Sydney 2026 不辦 | abea.org.au 公告:2026 起不再舉辦,從 2026 活動需求變量移除 | 我們已知取消:`data_inventory_2026-11-15.md:159、168`、`notes/raw/web_holidays_events_2026-11-14.md:90`、`notes/raw/web_verify_chrome_recheck_2026-11-14.md:9`。還寫「SXSW Sydney 官網(憑證壞掉)」的舊狀態:`meeting_1114/index.html:1155、1514`(+ share)、`notes/raw/web_holidays_events_2026-11-14.md:80`(同檔 :90 已更新)、`notes/raw/page_reconcile_v4_2026-11-14.md:56` | 事實不用改;簡報頁(1155、1514)的「被擋」狀態該換成「2026 取消」。有沒有哪個事件日曆還放著 SXSW,這次沒查(只 Grep 了 md/json/csv/txt/html) |
| 3.04 Inside Airbnb 歷史資料 US$500/800 | 官方收費指南按城市數和用途分類,原 PDF 的 US$500/800 不能當固定報價;另有截至 2026-11-30 的舊價過渡 〔隊友寫的,未核對〕 | `notes/raw/data_inventory_2026-11-15.md:207`;`meeting_1114/talk_script.md:106`;`meeting_1114/index.html:824、1294`(+ share);`notes/28_項目介紹簡報大綱_草稿.md:65`;`notes/21_1111組會錄音整理.md:79`;`notes/raw/meeting_1114_internal_facts.md:143`;`notes/raw/airbnb_history_sources_2026-11-11.md:29、31、55、65`。已經寫「指南、不是本組報價」的:`notes/15_Airbnb_2024起雙城與ROI_研究範圍.md:18`、`notes/16_方案AB_深度分析.md:386` | 我們寫的是「參考價」,方向沒錯;要補的是「不是固定報價、價格表可能換、要向站方問」,US$500 與 US$800 是不同分類(使命相符/非使命相符)的 2 城價,不是二選一 |
| 2.05 Domain 2026 年 9 月季報告網址 | 正確是 `domain.com.au/research/rental-report/september-2026/`,原筆記網址多出的後綴可以去掉;悉尼獨棟 A$835、公寓 A$780、空置率 1.2% 〔隊友寫的,未核對〕 | `notes/raw/data_inventory_2026-11-15.md:169`(記到 …september-2026-rental/);`notes/raw/web_chrome_recheck_A_2026-11-14.md:12`(我們試的 …september-2026-rental/ 回 404);公寓 780「只有 Elite Agent 轉述」見 `data_inventory_2026-11-15.md:169、227` | 網址換成隊友給的;這條連結我們的程式被 403 擋,**沒辦法替隊友驗證**,要有人用瀏覽器開一次再把 780 從「轉述」升成「原頁」 |
| 3.10 Blacktown A$1,140 / A$1,233 | A$1,140 屬 2025–26,不能當 2026–27 最終費用;後續預算又有調整,隊友自己也沒核對最終費率表 〔隊友寫的,未核對〕 | `notes/raw/data_inventory_2026-11-15.md:190`(「年度摘要沒寫清」)、`:222`;`notes/raw/web_opcost_housing_gapfill_2026-11-14.md:57、62`;`notes/raw/meeting_1114_external_facts.md:223`;`notes/raw/web_verify_opcost_housing_2026-11-14.md:70`;`meeting_1114/index.html:1533`(+ share) | 我們本來就寫「年度沒寫清」;補上「1,140 = 2025–26」。1,233 是哪一年隊友沒說,仍待核 |
| (補充)2.06 5,454 間 / 2,468 間 | 這組數字指向 2023 年、決議日期 2025-02-17,範圍是 City of Sydney,不是整個大悉尼 | `notes/raw/data_inventory_2026-11-15.md:180`(有寫 City of Sydney,沒寫 2023);`notes/raw/meeting_1114_external_facts.md:68、352`;`notes/raw/web_str_market_2026-11-14.md:97`;`meeting_1114/index.html:1533`(+ share) | 補年度標註;簡報上不能寫成現況 |
| (補充)1.05 ABS 雪梨營造成本 | Table 18 有悉尼住宅建築材料指數,悉尼同比 3.7% 〔隊友寫的,未核對〕 | `notes/raw/data_inventory_2026-11-15.md:216`(寫「ABS 雪梨層級沒有」,只有 Master Builders NSW +2.0%) | 不是我們寫錯,是缺口可能補得到;要有人開 Table 18 確認再改 |
| (補充)1.01 AER 電費草案 → 最終版 | 已有最終版,不必用草案 | `notes/raw/data_inventory_2026-11-15.md:75、167、229`;`meeting_1114/index.html:1533、1712`;`notes/raw/meeting_1114_external_facts.md:196、287` | 我們用的 1,875/2,347/2,515 是草案(都已標草案);最終版 PDF 我們程式沒連上,要用瀏覽器開 |

## 表 4:連結檢查全表

方法:腳本 `linkcheck/linkcheck.py`(一次跑完)。每條先 `curl -sIL --max-time 20`(只看標頭、不存檔);403/405/000 的再用 1 KB 範圍請求(`-r 0-1023 -o /dev/null`)試一次。User-Agent 是一般瀏覽器字串。沒有存任何外部檔。

注意:狀態 200 只代表伺服器回應了,不代表內容正確;網頁類沒有看內容。「程式連不上(000)」= 20 秒內沒有任何回應(curl 結束碼 28),AER 與 IPART 兩站另外單獨測過,TLS 連得上但伺服器不回標頭,很像是擋程式,不是連結壞掉。

| # | 項目編號 | 網址 | 狀態碼 | 有沒有被轉走 | Content-Type | 大小 | 白話結果 |
|---|---|---|---|---|---|---|---|
| 1 | 1.01 | https://www.aer.gov.au/system/files/2026-05/AER%20-%20Final%20determination%20-%20Default%20market%20offer%202026%E2%80%9327.pdf | 000 | 沒轉走 | —(範圍請求:000) | 沒給 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 2 | 1.01 | https://www.aer.gov.au/system/files/2026-05/Information%20Kit%20-%20Default%20Market%20Offer%20-%202026-27_0.pdf | 000 | 沒轉走 | —(範圍請求:000) | 沒給 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 3 | 1.01 | https://www.aer.gov.au/industry/registers/resources/reviews/default-market-offer-2026-27/final-determination | 000 | 沒轉走 | —(範圍請求:000) | 沒給 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 4 | 1.02 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Data-appendix-Monitoring-the-NSW-retail-gas-market-2024-25-November-2025.XLSX | 000 | 沒轉走 | —(範圍請求:000) | 沒給 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 5 | 1.02 | https://www.ipart.nsw.gov.au/review/energy/monitoring-nsw-retail-energy-markets-2024-25 | 000 | 沒轉走 | —(範圍請求:000) | 沒給 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 6 | 1.03 | https://www.archicentreaustralia.com.au/wp-content/uploads/CostGuide-2026.pdf | 200 | 沒轉走 | application/pdf | 沒給 | 開得了,是檔案(PDF,沒給) |
| 7 | 1.04 | https://www.martinahayes.com.au/wp-content/uploads/6202YENDYSTSOCNOITAVONER.pdf | 200 | 沒轉走 | application/pdf | 0.95 MB | 開得了,是檔案(PDF,0.95 MB) |
| 8 | 1.05 | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026/6427018.xlsx | 200 | 沒轉走 | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | 0.19 MB | 開得了,是檔案(Excel,0.19 MB) |
| 9 | 1.05 | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/latest-release | 200 | 沒轉走 | text/html | 0.49 MB | 開得了,是網頁 |
| 10 | 1.06 | https://vivinfurnishings.com.au/wp-content/uploads/2025/07/Vivin-Furnishings-Just-Furniture-Packages-Brochure-2025_compressed.pdf | 200 | 沒轉走 | application/pdf | 7.50 MB | 開得了,是檔案(PDF,7.50 MB) |
| 11 | 1.06 | https://vivinfurnishings.com.au/furniture-packages/ | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 12 | 1.07 | https://www.terrischeer.com.au/assets/documents/terrischeer/terri-scheer-holiday-rental-insurance-english.pdf | 200 | 沒轉走 | application/pdf | 0.20 MB | 開得了,是檔案(PDF,0.20 MB) |
| 13 | 1.07 | https://www.terrischeer.com.au/policy-documents | 200 | 沒轉走 | text/html | 0.04 MB | 開得了,是網頁 |
| 14 | 1.08 | https://www.amaysim.com.au/content/dam/amaysim/documents/terms-conditions/Critical-Info-Summary-amaysim-Home-Internet-Plans.pdf | 200 | 沒轉走 | application/pdf | 0.13 MB | 開得了,是檔案(PDF,0.13 MB) |
| 15 | 1.09 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Final-Report-North-Sydney-Council-Special-Variation-and-Minimum-Rate-2026-27-%281%29.PDF | 000 | 沒轉走 | —(範圍請求:000) | 沒給 | 程式連不上(000,20 秒沒回應;AER、IPART 兩站已另測確認是逾時),要用瀏覽器再看 |
| 16 | 1.09 | https://www.northsydney.nsw.gov.au/rates | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 17 | 1.10 | https://dcj.nsw.gov.au/about-us/families-and-communities-statistics/housing-rent-and-sales/previous-rent-and-sales-reports.html | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 18 | 1.11 | https://sqmresearch.com.au/uploads/SQM-National-Vacancy-Rates-October-2026-17-11-2044.pdf | 200 | 沒轉走 | application/pdf | 0.76 MB | 開得了,是檔案(PDF,0.76 MB) |
| 19 | 1.12 | https://discover.cotality.com/hubfs/Article-Reports/202611%20Cotality%20Monthly%20Housing%20Chart%20Pack%20-%20November.pdf | 200 | 沒轉走 | application/pdf | 4.61 MB | 開得了,是檔案(PDF,4.61 MB) |
| 20 | 1.13 | https://www.rba.gov.au/statistics/tables/xls/f06hist.xlsx | 403 | 沒轉走 | text/html(範圍請求:403) | 0.00 MB | 程式被擋(403),要用瀏覽器再看 |
| 21 | 1.13 | https://www.rba.gov.au/statistics/interest-rates/ | 403 | 沒轉走 | text/html(範圍請求:403) | 0.00 MB | 程式被擋(403),要用瀏覽器再看 |
| 22 | 1.14 | https://www.tra.gov.au/content/dam/austrade-assets/global/wip/tra/documents/atdd/atdd-october-2026.pdf | 200 | 沒轉走 | application/pdf | 2.46 MB | 開得了,是檔案(PDF,2.46 MB) |
| 23 | 1.14 | https://www.tra.gov.au/en/tourism-statistics/domestic-tourism-statistics-results | 200 | 沒轉走 | text/html | 0.24 MB | 開得了,是網頁 |
| 24 | 1.14 | https://www.destinationnsw.com.au/insights/sydney-statistics | 200 | 沒轉走 | text/html | 0.33 MB | 開得了,是網頁 |
| 25 | 1.15 | https://www.planning.nsw.gov.au/sites/default/files/2024-09/faq-short-term-rental-accommodation.pdf | 200 | 沒轉走 | application/pdf | 0.18 MB | 開得了,是檔案(PDF,0.18 MB) |
| 26 | 1.15 | https://www.planning.nsw.gov.au/the-planning-system/housing/short-term-rental-accommodation | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 27 | 2.01 | https://sydneyelitepainters.com.au/how-much-does-it-cost-to-paint-an-apartment-in-sydney/ | 200 | 沒轉走 | text/html | 0.02 MB | 開得了,是網頁 |
| 28 | 2.02 | https://floorsandingandpolishingsydney.com.au/floor-sanding-cost | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 29 | 2.03 | https://www.nblaundry.au/pricing | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 30 | 2.04 | https://www.beforeyoubuy.com.au/for-sales-agents/resources/strata-levy-benchmarking-nsw | 200 | 沒轉走 | text/html | 0.14 MB | 開得了,是網頁 |
| 31 | 2.05 | https://www.domain.com.au/research/rental-report/september-2026/ | 403 | 沒轉走 | text/html(範圍請求:403) | 0.00 MB | 程式被擋(403),要用瀏覽器再看 |
| 32 | 2.06,3.05 | https://meetings.cityofsydney.nsw.gov.au/mgDecisionDetails.aspx?IId=32031&Opt=1 | 200 | 沒轉走 | text/html | 0.04 MB | 開得了,是網頁 |
| 33 | 2.07 | https://meetings.cityofsydney.nsw.gov.au/mgIssueHistoryHome.aspx?IId=36147 | 200 | 沒轉走 | text/html | 0.01 MB | 開得了,是網頁 |
| 34 | 2.08,3.11 | https://www.airbnb.com.au/help/article/1857 | 200 | 沒轉走 | text/html | 0.00 MB | 開得了,是網頁 |
| 35 | 2.09 | https://airbtics.com/starting-an-airbnb-australia | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 36 | 2.10 | https://www.revenue.nsw.gov.au/taxes-duties-levies-royalties/land-tax/understanding-land-tax/thresholds-and-rates | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 37 | 2.11 | https://researchers.mq.edu.au/en/publications/airbnb-pricing-in-sydney-predictive-modelling-and-explainable-mac/ | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 38 | 2.12 | https://www.abea.org.au/news-item/22055/following-three-years-of-asia-pacific-expansion-sxsw-sydney-will-conclude-its-run | 200 | 沒轉走 | text/html | 0.02 MB | 開得了,是網頁 |
| 39 | 3.01 | https://www.airroi.com/data-portal/markets/sydney-australia | 200 | 沒轉走 | text/html | 0.12 MB | 開得了,是網頁 |
| 40 | 3.02 | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 41 | 3.03 | https://insideairbnb.com/get-the-data/ | 200 | 沒轉走 | text/html | 0.55 MB | 開得了,是網頁 |
| 42 | 3.04 | https://insideairbnb.com/data-requests/ | 200 | 沒轉走 | text/html | 0.31 MB | 開得了,是網頁 |
| 43 | 3.06 | https://www.tra.gov.au/en/about-us/methodology/national-visitor-survey-methodology | 200 | 沒轉走 | text/html | 0.23 MB | 開得了,是網頁 |
| 44 | 3.07 | https://www.pabs.com.au/our-services/relocation-packages/ | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 45 | 3.09 | https://hia.com.au/our-industry/economics/data-forecasts/resource/kitchens-and-bathrooms-report | 200 | 沒轉走 | text/html | 0.18 MB | 開得了,是網頁 |
| 46 | 3.09 | https://www.rawlhouse.com.au/publications/2026-construction-cost-guide | 200 | 沒轉走 | text/html | 沒給 | 開得了,是網頁 |
| 47 | 3.10 | https://www.blacktown.nsw.gov.au/files/assets/public/v/1/rates/srv-2026-submission-files/application-form-part-b-special-variation-2026-27.pdf | 403 | 沒轉走 | text/html(範圍請求:403) | 0.00 MB | 程式被擋(403),要用瀏覽器再看 |
| 48 | 3.10 | https://www.blacktown.nsw.gov.au/News-Media/Blacktown-City-Council-confirms-202627-budget | 403 | 沒轉走 | text/html(範圍請求:403) | 0.00 MB | 程式被擋(403),要用瀏覽器再看 |
| 49 | 3.12 | https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/sharing-economy-and-tax/renting-out-all-or-part-of-your-home | 403 | 沒轉走 | text/html(範圍請求:403) | 0.00 MB | 程式被擋(403),要用瀏覽器再看 |

列數對賬:HTML 裡 `href="http…"` 共 51 個、去重後 **49 條**;表 4 = 49 列;各項下的連結加總 51(含 2 條被兩個項目共用:2.06/3.05、2.08/3.11)。

## 沒做的

- 沒下載任何檔、沒開 Excel 看工作表(所以 1.02、1.05、1.13 的 Excel 內容都沒人看過)。
- 403 與 000 的 12 條沒辦法用程式驗證,要用瀏覽器再看;沒有自己上網找替代連結。
- 沒看網頁內容(只有標頭),所以隊友寫的金額、百分比、日期一律沒核對。
- 更正位置只 Grep 了 `Innovation Studio/` 底下的 md/json/csv/txt/html/py;程式碼或別的資料夾沒查。
