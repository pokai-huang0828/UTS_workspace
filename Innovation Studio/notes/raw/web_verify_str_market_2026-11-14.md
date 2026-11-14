# 查核:雪梨短租市場行情筆記(web_str_market_2026-11-14.md)

查核日 2026-11-14;scope ID:IS-1114-verify-01-strmarket。共查 57 列:✅ 37、⚠️ 15、❌ 1、⏸ 0、未查 4(未查的 4 列:筆記自己就標明「沒讀原文」的二手搜尋摘要)。

方法:用 WebFetch 重開筆記網址並比對數字、單位、期間、範圍;AirDNA 的 WebFetch 回 HTTP 403,改用 Chrome 擴充功能自開分頁讀取成功(已關閉自己的分頁),所以 AirDNA 不算 ⏸。WebFetch 回傳是摘要,我只對「有看到」的數字給 ✅。

## 逐列判定表

### 表 1:價格、入住率、收入

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| AirDNA 活躍房源 | 16,392(去重,三平台,截至 2026-10) | 16,392;"as of October 2026";去重跨 Airbnb/Vrbo/Booking.com | ✅ | 頁面更新日 2026-11-11 | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview |
| AirDNA ADR | $193/晚(未標幣別) | $193;定義「已訂晚實際成交均價」,近 12 個月 | ✅ | 頁面只有 "$",確實沒標幣別 | 同上 |
| AirDNA 入住率 | 67% | 67%;「可訂晚數中被訂走的比例」 | ✅ | | 同上 |
| AirDNA 每間年收入 | $40.8K/年(未標幣別) | $40.8K;近 12 個月,「含房價加清潔費與其他房客費用、未扣房東成本」 | ✅ | 筆記沒提「含清潔費」,與其他來源比較時要知道 | 同上 |
| AirDNA RevPAR | $129 | $129 | ✅ | | 同上 |
| AirDNA 年變化 | ADR -11.5%、入住率 +7.9%、RevPAR +3.3%、房源 -36.8%、營收 +99.1%(不採用) | 完全相同(2025-10 至 2026-10) | ✅ | 營收 +99.1% 確實寫在頁面,筆記不採用的處理合理 | 同上 |
| AirROI 活躍房源 | 10,096 | 10,096,年減 22% | ✅ | 頁面標題「12 個月至 2026-10」 | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney |
| AirROI ADR | AUD 399/晚 | A$399(NSW 平均 A$470) | ✅ | | 同上 |
| AirROI 入住率 | 49.5%(開放天數) | 49.5% of open nights(頁面也四捨五入為 50%) | ✅ | | 同上 |
| AirROI 每間年收入 | AUD 52,495(+12.0%) | A$52,495,年增 12.0% | ✅ | | 同上 |
| AirROI 每月收入中位數 | 約 AUD 4,710 | about A$4,710 | ✅ | | 同上 |
| AirROI 年收入中位數 Studio/1房 | 40,500 / 44,100 | 40,500 / 44,100 | ✅ | | 同上 |
| AirROI 年收入中位數 2房/3房 | 54,000 / 54,500 | 54,000 / 54,500 | ✅ | | 同上 |
| AirROI 年收入中位數 4房/5房+ | 63,500 / 78,900 | 63,500 / 78,900 | ✅ | | 同上 |
| AirROI 年收入平均 各房數 | 42,400 / 46,800 / 60,700 / 67,900 / 83,100 / 104,000 | 完全相同 | ✅ | | 同上 |
| GuestFavorites 活躍房源 | 13,051(Sydney) | 13,051;地理範圍寫 Greater Sydney | ⚠️ | 數值吻合;範圍:頁面是 Greater Sydney,筆記寫 Sydney(輕微) | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia |
| GuestFavorites ADR | AUD 336 | A$336 | ⚠️ | 數值、幣別吻合;範圍同上(Greater Sydney) | 同上 |
| GuestFavorites 入住率 | 68% | 68% | ⚠️ | 數值吻合;範圍同上 | 同上 |
| GuestFavorites 每間年收入 | AUD 83,094(平均) | A$83,094;頁面自相矛盾:績效卡標「Median Annual Revenue」、內文標 average | ⚠️ | 差在定義:平均還是中位數,頁面本身沒統一;範圍同上 | 同上 |
| Airbtics 追蹤房源數 | 13,174(僅納入較高評分房源,非全市場) | 13,174;頁面稱「Airbtics 追蹤的 Sydney 活躍房源」;FAQ 的納入條件是「有 Airbnb 評分資料、近 12 個月至少 90 個活躍日、有入住率資料」;評分 4.3 只是計分的下限、頁面明說不是納入門檻 | ⚠️ | 差在定義:筆記的「僅納入較高評分房源」頁面查不到,實際是「有評分且活躍 ≥90 天」 | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ |
| Airbtics 入住率中位數 | 75%(2025-09 至 2026-09) | 75%;資料期間 Sep 2025–Sep 2026 | ✅ | 數值吻合;樣本定義見上一列 | 同上 |
| Airbtics ADR 中位數 | AUD 281 | A$281 | ✅ | | 同上 |
| Airbtics 年收入中位數 | AUD 79,355 | A$79,355 | ✅ | 頁面 FAQ 另有「只含榜單前 30 名」中位數 A$46,562,別混用 | 同上 |
| Airbtics 2025 雪梨全年 | 78.0% / AUD 258 / AUD 75,205(2024: 69,160,+8.74%) | 78.0% / $258 / $75,205;2024 $69,160;+8.74% | ⚠️ | 數值吻合;幣別:頁面只有 "$"、未標 AUD,筆記寫 AUD 是推定 | https://airbtics.com/short-term-rental-market-report-2025-australia |
| Airbtics 2025 全澳(46 市場) | 62.2% / AUD 317 / AUD 71,770 | 62.20% / $317 / $71,770;但同頁 2024 為 $45,174、「營收變化 4.52%」,兩者互相對不上 | ⚠️ | 幣別未標;且該頁全澳營收的 2024 對照與年增率自相矛盾,全澳營收數字可信度低 | 同上 |
| Hometime 入住率 | 67%(FY24-25) | 67%,FY24-25,表名 "Sydney Airbnb average occupancy" | ✅ | | https://www.hometime.io/blog/market-report-short-term-rental-sydney |
| Hometime 典型年收入範圍 | AUD 50,800–97,700(期間未標) | $50,800–$97,700;未標期間、未標來源;文章 2026-07-08 | ⚠️ | 數值、日期吻合;幣別:頁面只有 "$",筆記寫 AUD 為推定 | 同上 |

### 表 2:淡旺季

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| AirROI 最旺月 | 12 月,兩年日曆月平均約 7,300;2025-12 為 7,638 | 12 月最強;兩年平均 A$7,300;2025-12 表內 A$7,638 | ✅ | | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney |
| AirROI 最淡月 | 6 月,約 4,490;2026-06 為 4,690 | 6 月最弱;A$4,490;2026-06 A$4,690 | ✅ | | 同上 |
| 旺淡差 1.6 倍 | 7,300 / 4,490 | 重算 1.626 | ✅ | 本檔計算,數字無誤 | 同上 |
| GuestFavorites 入住率月份 | 高峰 11、2 月;平季 12、1 月;低點 5、6 月 | 完全相同 | ✅ | | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia |
| AirDNA 季節性分數 | 91/100(100=月間營收落差小) | 91;定義「最低與最高月平均營收的百分比差距,差距越小分數越高」 | ✅ | 注意:AirDNA 說落差小、AirROI 算出 12 月是 6 月 1.6 倍,兩者口徑不同;不要說「淡旺季不明顯」 | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview |
| Hometime 價格高峰/最淡 | 高峰 12–1 月(跨年夜最高);最淡 5–6 月 | 高峰 12–1 月、跨年夜最高 ✔;但頁面沒指明「價格最淡月」,只說 5、6 月是「domestic market 最軟的月份」、入住率入冬放緩 | ⚠️ | 差在定義:5–6 月最淡是入住率/需求,不是「價格最淡」 | https://www.hometime.io/blog/market-report-short-term-rental-sydney |

### 表 3:NSW 法規

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| 非房東同住上限 | 180 天(days);連續 21 天以上不計;最後更新 2025-02-10;從登記日起算每 12 個月;Greater Sydney 三個城市區 | "maximum of 180 days a year"(用 days);"21 consecutive days or more" 豁免;最後更新 10 February 2025 | ⚠️ | 核心數字吻合;「從登記日起算 12 個月」「三個城市區名稱」這次回傳內容沒看到,未能證實 | https://www.planning.nsw.gov.au/STRA |
| 房東同住不限天數 | 365 天;2021-04 公告、2021-11-01 生效 | 「全年 365 天」;公告 9 April 2021;生效 1 November 2021(原訂 2021-07-30 後延) | ✅ | | https://www.planning.nsw.gov.au/news/short-term-rental-accommodation-framework-finalised |
| 登記費 | 新登記 AUD 65;續約 25;不退費 | $65 新登記、$25 年費,皆 non-refundable;更新日 10 Feb 2025 | ✅ | | https://www.planning.nsw.gov.au/STRA |
| 登記制度 | 強制登記 + 排除名單 + 最低防火 + 強制行為準則 | government-run register、exclusion register、minimum fire safety standards、mandatory Code of Conduct | ⚠️ | 差在定義:頁面只有行為準則標 mandatory,register 沒標「強制」 | 新聞稿網址同上 |
| 2024 檢討 | 2024-02-15 至 03-14;430+ 份意見、2,400+ 份問卷;天數上限列為檢討中、未列結果 | 15 Feb–14 Mar 2024;over 430 submissions、more than 2,400 survey responses | ⚠️ | 日期與數字吻合;「天數上限列為政策檢討中、未列結果」這句本次沒看到頁面有此措辭 | https://www.planning.nsw.gov.au/STRA |
| Byron Shire 60 天 | 2024-09-23 起,不適用 Greater Sydney | 2024-09-23 起,大部分 Byron LGA 的 exempt development 路徑上限 60 天;另有兩個 365 天例外區;時間軸也列 2023-09-23 | ⚠️ | 範圍:有例外區與路徑限定,筆記沒寫;與雪梨無關 | 同上 |
| City of Sydney 市議會動議 | 2026-04-28 動議(二手報導) | 未開啟(筆記自己標「未直接讀取」) | 未查 | 非官方來源,不在查核範圍 | 無 |

### 表 4:Airbnb 房東費

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| 單一房東服務費 | 15.5%(全球平均);2026-07-29 發布、2026-10-13 更新;澳洲未寫專屬日 | 「a single 15.5% service fee paid by hosts」;「based on Airbnb's global average service fees」;發布 29 July 2026、更新 13 Oct 2026;沒有澳洲專屬費率或日期;巴西與墨西哥為 16% | ✅ | 「房客不再另付」那半句本次沒逐字確認;頁面說用物業管理軟體的房東「13 October」轉換,未寫年份 | https://www.airbnb.com.au/resources/hosting-homes/a/simplifying-airbnb-service-fees-746 |
| 舊制 3% / 14.1–16.5% | 搜尋摘要引述舊版 | 未開啟 | 未查 | 筆記自己標為摘要 | 同上 |
| Hometime 說法一 | PMS 房東 2025-10-27 由 15% 調為 15.5% | "27 October 2025: PMS-connected hosts moved to the single fee",「15% to 15.5%」 | ✅ | | https://www.hometime.io/blog/what-airbnb-host-only-fee-means-for-you |
| Hometime 說法二 | 自行管理房東 2026-09-15 起轉單一費用,多為訂單小計 15.5%(文章 2026-09-08) | 15 September 2026 為 EEA 以外剩餘房東期限;多數付 15.5% of booking subtotal;文章 September 8, 2026 | ✅ | 同頁 FAQ 另寫「2025-10-27 起 Airbnb 向房東抽 15.5%」,與正文自相矛盾 | 同上 |
| 說法三 2025-12-01 | 搜尋摘要 | 未開啟 | 未查 | 筆記自己標為摘要 | 無 |

### 表 5:供給趨勢

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| AirDNA 房源年變化 | -36.8%(2025-10→2026-10)(另一次摘要寫 -42.0%) | -36.8%;-42.0% 未見 | ✅ | -42.0% 只出現在筆記轉述的搜尋摘要,不採用即可 | https://www.airdna.co/vacation-rental-data/app/au/new-south-wales/sydney/overview |
| AirROI 房源年變化 | -22% | 10,096 間、down 22% YoY | ✅ | | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney |
| BnbCalc 較小區域 | -10%、8,379 間、2026-05 對前一年 | 頁面寫 Sydney 整個市場 12 個月至 2026-09 平均 9,083 間(標題 9.3K、結構化資料 9,316),年增 +4%、兩年 +13%;沒有 -10%、8,379 或 2026-05;頁面也沒有「Sydney/Bondi/Manly/Parramatta 合計」的資料範圍 | ❌ | 筆記數字對不上現行頁面(摘要過期或錯);方向與其他來源相反(+4% vs -22%~-37%);頁面本身 ADR/入住率也自相矛盾(369/51% vs 361/58%) | https://www.bnbcalc.com/markets/au/sydney |
| Airbtics 2025 供給年增 | +28.88%(多 2,851 間) | Supply growth +28.88%、added listings +2,851 | ✅ | | https://airbtics.com/short-term-rental-market-report-2025-australia |
| City of Sydney 登記 | 5,454 間、2,468 間登記 | 未開啟 | 未查 | 筆記自己標為摘要 | 無 |
| Airbtics 全澳供給 | +13.79% | 13.79% | ✅ | | 同 Airbtics 報告網址 |

### 檔尾情境建議值(是否取自它說的那一列)

| 項目 | 筆記寫的值 | 頁面實際看到的值 | 判定 | 說明 | 網址 |
|---|---|---|---|---|---|
| 低:入住率 50% | 取自 AirROI 49.5% | AirROI 49.5%(約 50%) | ✅ | 取自該列,四捨五入;分母是「開放天數」 | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney |
| 低:ADR 280 | 取自 Airbtics 中位數 281 | Airbtics A$281(2025-09 至 2026-09) | ✅ | 取自該列;注意低情境把 AirROI 的入住率配 Airbtics 的 ADR,是跨來源混搭 | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ |
| 中:入住率 67% | 取自 AirDNA 67%;GF 68% 也接近 | AirDNA 67%、GF 68% | ✅ | | AirDNA 與 GF 網址同上 |
| 中:ADR 336 | 取自 GuestFavorites 336;與我們掛牌價 338 接近 | GF A$336(Greater Sydney) | ⚠️ | 取自該列;範圍是 Greater Sydney;「338」是內部資料,本次未查 | https://www.guestfavorites.com/airbnb-occupancy-rates-in-sydney-australia |
| 高:入住率 75% | Airbtics 中位數 75%(僅含高評分房源) | Airbtics 75% ✔;但樣本不是「高評分」,是「有評分且活躍 ≥90 天」 | ⚠️ | 數字取自該列;括號裡的樣本描述不準確 | https://airbtics.com/top-airbnb-listings-in-sydney-australia/ |
| 高:ADR 399 | 取自 AirROI 399 | AirROI A$399 | ✅ | 取自該列 | https://www.airroi.com/airbnb-data/australia/new-south-wales/sydney |

附帶重算:280×50%×365=51,100;336×67%×365=82,171(筆記寫 82,200);399×75%×365=109,226(筆記寫 109,200)。三個乘積無誤。

## 簡報上可以直接用的數字(頁面親眼看到,數值、單位、期間、範圍都吻合)

- AirROI(Sydney,AUD,2025-11 至 2026-10):活躍房源 10,096(年減 22%)、ADR 399、入住率 49.5%(分母是開放天數)、每間年收入平均 52,495、月收入中位數約 4,710、各房數年收入中位數/平均、12 月最旺約 7,300/月、6 月最淡約 4,490/月。
- AirDNA(Sydney,2025-10 至 2026-10):活躍房源 16,392、入住率 67%、RevPAR 129、房源年變化 -36.8%、季節性分數 91。(只有金額欄位要加註,見下。)
- Airbtics 追蹤榜(A$,2025-09 至 2026-09):入住率中位數 75%、ADR 中位數 281、年收入中位數 79,355。
- Airbtics 2025 供給年增 +28.88%(雪梨)。
- NSW 官方:非房東同住 180 天/年、連續 21 天以上不計;房東同住 365 天;登記費新登記 AUD 65、續約 AUD 25(官方頁最後更新 2025-02-10)。
- Airbnb 房東單一服務費 15.5%(頁面寫明是全球平均;Hometime 文章寫澳洲自行管理房東 2026-09-15 起轉換)。

## 簡報上要加註或不要用的數字

- AirDNA ADR $193、年收入 $40.8K:頁面只有 "$"、沒標幣別;年收入含清潔費與其他房客費用。加註「幣別未標」,不要跟 AUD 數字直接比。
- GuestFavorites 全組(13,051 / 336 / 68% / 83,094):範圍是 Greater Sydney;83,094 頁面自己同時叫它平均與中位數。引用時寫「GuestFavorites 估計,Greater Sydney」,年收入不要標成平均或中位數其中一個。
- Airbtics 13,174 與 75%:別寫「僅含高評分房源」,改寫「有評分且近 12 個月活躍 ≥90 天的追蹤房源」;高情境 75% 的註解同步改。
- Airbtics 2025 全年報告(78.0% / 258 / 75,205 與全澳數字):頁面只有 "$",筆記寫 AUD 是推定;全澳營收的 2024 對照與年增率自相矛盾,全澳營收不要用。
- Hometime 年收入範圍 50,800–97,700:無期間、無來源、只有 "$",若用請寫「Hometime 文章稱」,不要標 AUD。
- Hometime「最淡 5–6 月」:改寫成「5–6 月需求最軟」,不要寫成價格最淡。
- 180 天與登記費:官方頁最後更新 2025-02-10;「從登記日起算 12 個月」「三個城市區」這次沒親眼看到;對外前再開 planning.nsw.gov.au 確認有無 2025–2026 修法。
- 登記制度的「強制登記」:頁面沒標 register 為 mandatory;簡報改寫「政府營運登記制度」,或另找官方頁佐證「強制」。
- AirDNA 季節性 91 不要解讀成「淡旺季不明顯」:它量的是月營收最高最低差,與 AirROI 12 月/6 月約 1.6 倍並存。
- BnbCalc -10%、8,379 間:對不上現行頁面(頁面是 +4%、約 9,083 間),不要用。
- 未查、不要用於簡報:City of Sydney 動議與登記 5,454/2,468、Airbnb 舊制 3%/14.1–16.5%、2025-12-01 改制說法、AirDNA -42.0%。
- 供給方向不能寫成「一致減少」:AirDNA -36.8%、AirROI -22% 是減少;Airbtics 2025 是 +28.88%;BnbCalc 現行頁是 +4%。期間與口徑不同,只能並列。
