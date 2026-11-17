# 補查 5 項(本機檔,2026-11-17)

> scope IS-1117-CHK-L。接續 `external_downloads_verify_2026-11-17.md`。原檔在 `Innovation Studio/refs/external_2026-11-17/`(只讀)。腳本與暫存圖在 scratchpad `...\scratchpad\followup_1117\`(`pos.py`、`img.py`、`xl.py`、`dates.py`),不進 repo。Python 一律 `python -I`,路徑當參數。
> 頁碼 = PDF 第幾頁。引用原文都 ≤ 20 字。

## 結論

1. Vivin p.4:**確認** Standard 5,999 / 7,999 / 9,999、Designer 8,499 / 10,999 / 12,999(一/二/三房,看到床的圖示);每個價都寫「FROM」和「+GST」;頁面沒有年份。
2. Cotality p.28:**確認** Sydney 年增 4.0%(到 2026 年 10 月);但我沒有看到圖的畫面,是用文字層座標對的;「有沒有分獨棟與公寓」文字層看不出,**仍不確定**。
3. AER 3,900 kWh:**仍不確定**(檔案沒有寫「without controlled load」);間接證據傾向「1,899 是平價主費率,不含另外加的可控負載」;可控負載另有 Ausgrid 2,000 kWh(1,340 + 660)的用電量,但**文字裡沒有「可控負載客戶年費多少錢」**。
4. 瓦斯「Metro」:**更正**——不能說 Metro = Jemena 雪梨網路。同一天(2025-09-15)Metro 1,249.96 和 Jemena Coastal 1,304.05 並存且不同;檔案沒有定義 Metro,**仍不確定**它是什麼範圍。
5. 兩個 Excel 複核:**確認** ABS Data1 Q251 = 3.7(2026-09-01,Sydney All groups 年增);IPART 第 10679 列 medianBill 1,249.958、第 10682 列 1,482.799(是 **I 欄**)。

## 1. Vivin 家具型錄 p.4(`1.06_Vivin_furniture_packages_2025.pdf`)

- **上一輪**:Standard 5,999 / 7,999 / 9,999、Designer 8,499 / 10,999 / 12,999,「依文字順序」猜;臥室對應、有無年份未確認。
- **這次看到**:`pdftoppm` 沒裝、PDF Tools 又不能讀 D 槽,所以用內建瀏覽器窗格以 `file://` 唯讀打開該 PDF,捲到第 4 頁看畫面(標題「Just furniture packages」)。兩欄:「Standard Furniture Packages」「Designer Furniture package」,各寫「Available in one, two or three bedrooms」。每個價格左邊有床的圖示:1 張床、2 張床、3 張床,由上到下。Standard:$5,999 / $7,999 / $9,999;Designer:$8,499 / $10,999 / $12,999。每個價格上方都有「FROM」,後面都有「+GST」。頁面下方「Please Note」:不含 Whitegoods 與 Outdoor;「primarily for New South Wales. Melbourne and Brisbane may differ.」。整頁(含頁首頁尾)沒有看到年份。文字層座標也一致(同一頁抽出的價格順序與畫面相同)。
- **結果**:**確認**(價格與臥室對應對;「2025」只在檔名與網址,頁面上沒有)。
- **用的時候加一句**:這是「FROM」起價、不含 GST、不含白色家電與戶外;「2025 年版」只是檔名,頁面沒寫年份。

## 2. Cotality 圖表包 p.28(`1.12_Cotality_housing_chart_pack_2026-11.pdf`)

- **上一輪**:猜 Sydney 4.0%(Melbourne 4.5%、Brisbane 6.5%…),靠文字順序,沒確認。
- **這次看到**:`pdftoppm` 與 PDF Tools 都用不了,**沒有看到圖的畫面**;改用 pypdf 抽出每個字的座標(`pos.py`)。左圖標題「Annual change in rental rates to October 2026」(p.28);城市名與百分比在同一條水平線上成對:Sydney(y=64)與 4.0%(y=63),Melbourne 4.5%、Brisbane 6.5%、Adelaide 6.3%、Perth 7.5%、Hobart 8.4%、Darwin 11.4%、Canberra 3.2%;還有 Regional NSW 4.8%、Regional Vic 3.4%、Regional QLD 6.2%、Regional SA 6.2%、Regional WA 6.5%、Regional TAS 8.7%、Regional NT 8.1%;Combined capitals 5.2%、Combined regionals 5.5%、National 5.3%。右圖標題「Annual change in rental rates - National」,橫軸 Oct 21 到 Oct 26(全國時間序列)。頁首文字:「rents rising 5.3% nationally over the year to October 2026」。文字層沒有出現 house/unit(獨棟/公寓)字樣。
- **結果**:Sydney 4.0% **確認**(座標配對);期間「到 2026 年 10 月的年增」**確認**;是否分獨棟與公寓 **仍不確定**(文字層沒有,但我沒看到畫面,不能保證圖上沒有圖例;從欄位看是「Combined」整體租金)。
- **用的時候加一句**:這是 Cotality 的「租金指數」年增(整體,非掛牌價),Sydney 4.0% 對的是「到 2026-10」;別把它和 SQM 的掛牌週租(1.11)混在一起比。

## 3. AER 電費 3,900 kWh 含不含可控負載(`1.01_AER_final_…pdf`、`1.01_AER_information_kit_…pdf`)

- **上一輪**:Table 2.1 沒寫「without controlled load」;p.14 寫基準「including the controlled load amounts」;3,900 / 4,900 / 4,600 含不含可控負載,「未確認」。
- **這次看到**(Grep 關鍵字,只讀命中處):
  - 最終版 p.16 Table 2.1:列名「Residential, flat rate」/「Residential, time of use」/「Solar Sharer Offer」;Ausgrid「DMO price $1,899」「For annual usage 3,900 kWh」。**沒有「without controlled load」字樣**(Grep `without controlled load` 在兩份 AER 檔都 0 命中)。
  - 最終版 p.14:「annual usage benchmarks … including the controlled load amounts」——講的是 DMO 的用電基準方法(基準資料有納入可控負載),沒有說 Table 2.1 的 3,900 kWh 裡含了可控負載。
  - 最終版 p.21(Figure 2.6 上方):「separate controlled load DMO tariff caps that can be included alongside」平價/分時/Solar Sharer——可控負載是**另外一組費率上限**,「加在」主費率旁邊。Figure 2.6 圖內只有一串沒有標籤的小數(如 19.3094、23.0050…,圖例有 Ausgrid CL1、CL2),**單位與逐項對應我沒有確認**,不拿來用。
  - 最終版 p.118(附錄 C「Per-customer annual usage determination」):欄位分開列——住宅平價/分時/Solar Sharer:Ausgrid 3,900;小企業 10,000;**可控負載 1+2:Ausgrid 2,000,其中 Controlled Load 1 = 1,340、Controlled Load 2 = 660**(Endeavour 2,200 = 1,474 + 726;Essential 2,000 = 1,540 + 460)。註「365 days per annum in 2026-27, expressed in kWh」。
  - p.25:列「residential customers with controlled load」為 DMO 要定的受管制費率之一。
  - 資訊包 p.4:表同最終版(Ausgrid $1,899 / 3,900 kWh;去年 $1,965),我讀的 p.4 前段(Ausgrid 到 Energex 列)沒有可控負載字樣;p.4 後半沒有逐行讀。
  - 「有可控負載的住宅客戶另外是多少錢」:**檔案文字裡沒有一個年費金額**。只有 Figure 2.6 的費率上限(圖,未確認單位)和附錄 C 的用電量。
- **結果**:**仍不確定**(檔案沒有明說)。間接證據(用電量欄位分開、可控負載費率另外列)**傾向**:1,899 / 3,900 kWh 是主費率(平價)的上限,可控負載另外加。
- **用的時候加一句**:寫「DMO 平價 1,899(3,900 kWh)」,**不要寫成「沒有可控負載的客戶」**——AER 沒用這個說法;若家裡有可控負載(熱水等),實際帳單會再加另一組費率,金額檔案沒給。

## 4. 瓦斯「Metro」是不是 Jemena 雪梨網路(`1.02_IPART_gas_data_appendix_2024-25.xlsx`)

- **上一輪**:「Metro = Jemena 雪梨網路」是從 2018 年兩者數字相同推的,檔案沒明講。
- **這次看到**(openpyxl,`xl.py`、`dates.py`):
  - 在 Contents 與其他 28 張非資料工作表搜 Metro / Jemena / Coastal / Country:**「Metro」0 命中,沒有任何定義或註解**。Jemena 相關只有:Contents D30「Retail gas offers, Jemena Coastal network」;D27「…outside the Jemena region」;工作表 4.5–4.12 的 M7/M27/M30「Jemena Country」;4.1 標題「Jemena Coastal network … ($ nominal, incl. GST)」;6.3 標題「(Jemena coastal, 24.4 GJ …)」。
  - 「Historic Data - Gas Prices」(10,688 筆資料列)`network` 欄不重複值 15 個:AGN Adelong, Gundagai and Tumut(800)、AGN Albury(792)、AGN Bombala and Cooma(800)、AGN Murray Valley(792)、AGN Temora, Culcairn, Holbrook, Henty and Walla Walla(792)、AGN Wagga Wagga(792)、Allgas(792)、Central Ranges Tamworth(792)、Evoenergy Queanbeyan(796)、Evoenergy Shoalhaven(396)、**Jemena(24)**、**Jemena Coastal(776)**、**Jemena Country(776)**、**Metro(784)**、**Regional(784)**。
  - 日期範圍:Jemena 只有 2018-06-30 到 2019-06-30;Metro、Regional 2018-06-30 到 2025-09-15;Jemena Coastal、Country 2020-06-01 到 2025-09-15。
  - 2018-06-30(住宅、單一費率市場方案、All retailers、24,400 MJ):Jemena 941.49(16 個)= Metro 941.49(16 個);Regional 980.94(67 個)。
  - **2025-09-15 同一組條件:Metro 1,249.96(29 個)、Jemena Coastal 1,304.05(22 個)、Regional 1,291.78(58 個)、Jemena Country 1,215.79(12 個)。**
- **結果**:**更正**。2018 年 Metro 與 Jemena 相同,但 2020 年後 Jemena 被拆成 Coastal/Country,2025 年 Metro 與 Jemena Coastal 在同一天數字不同、方案數也不同(29 vs 22),所以**不能把 Metro 當成 Jemena Coastal(雪梨沿海網路)**。Metro 實際涵蓋哪些供氣網路,檔案沒寫,**仍不確定**。
- **用的時候加一句**:表 2 的「雪梨瓦斯 Metro 1,249.96」要改叫「IPART 資料裡的 Metro 區(範圍檔案沒定義)」,不要寫成 Jemena 雪梨網路;若要講雪梨沿海,有明講的是 Jemena Coastal(4.1 表 2025-06:市場中位 1,195.42;Historic 2025-09-15:1,304.05),兩個日期的數字不同,別混。

## 5. 兩個 Excel 儲存格複核

**5a. `1.05_ABS_PPI_Table18_sep_2026.xlsx` 工作表 Data1,Q 欄**
- **上一輪**:Q251 = 3.7;日期 2026-09-01。
- **這次看到**:Q 欄表頭:Q1「Percentage change from corresponding quarter of previous year ; All groups ; Sydney ;」;Unit = Percent;Series Type = Original;Data Type = PERCENT;Frequency = Quarter;Series Start 1967-09-01;Series End 2026-09-01;No. Obs 237;**Series ID = A2390419X**。A251 = 2026-09-01;**Q251 = 3.7**(251 為最後一列);A250 = 2026-06-01,Q250 = 3.5。工作表三張:Index、Data1、Enquiries。
- **結果**:**確認**。
- **用的時候加一句**:3.7% 是「雪梨、房屋建築業投入、All groups、2026 年 9 月季對去年同季」的年增(原始、未季調),不是單一建材價。

**5b. `1.02_IPART_gas_data_appendix_2024-25.xlsx`「Historic Data - Gas Prices」第 10679、10682 列**
- 表頭(第 1 列,A 到 P):date、customer_type、offer_type、network、usage、retailer_group、minBill、q1Bill、medianBill、q3Bill、maxBill、number_of_offers、p05Bill、p10Bill、p15Bill、p20Bill。(**medianBill 是 I 欄**。)
- 第 10679 列:2025-09-15|Residential|Single rate - Market offer|Metro|24400 MJ|All retailers|min 1070.37|q1 1143.59|**median 1249.95805**|q3 1435.52|max 1639.51|offers 29|p05 1085.25|p10 1120.06|p15 1128.18|p20 1132.45。
- 第 10682 列:2025-09-15|Residential|Single rate - Standing offer|Metro|24400 MJ|All retailers|min 1377.82|q1 1408.66|**median 1482.798848**|q3 1559.90|max 2066.22|offers 13|p05 1380.42|p10 1382.78|p15 1384.66|p20 1394.63。
- **結果**:**確認**(1,249.96 與 1,482.80;29 與 13 個方案)。
- **用的時候加一句**:歷史工作表表頭沒寫含不含 GST、也沒寫單位(只有 usage 欄寫 24400 MJ);「Metro」範圍見第 4 節,別當雪梨沿海。

## 沒做的

1. 沒有親眼看到 Cotality p.28 的圖(`pdftoppm` 沒裝,PDF Tools 限制在 Documents/Downloads/Desktop,而且我只對 Vivin 用了內建瀏覽器窗格);Sydney 4.0% 與「是否分獨棟/公寓」要人眼再看一次。
2. AER Figure 2.6(p.21)可控負載費率的單位與逐項對應沒有確認;資訊包 p.4 後半沒逐行讀;其他 150 頁沒讀。
3. Metro 的實際範圍沒查(檔案內沒有定義;IPART 報告本文不在這個 Excel 裡,沒查)。
4. 沒查表 2 的其他數字;沒改任何既有檔(包含 `external_downloads_verify_2026-11-17.md` 與表 2 裡的 Metro 說法);沒 commit。
