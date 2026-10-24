# 單元二 #12｜案例研究:乘客需求 — 「上車點 × 出租車區域」genial.ly 地圖

> 位置:M352284#12(單元二 → 案例研究:乘客需求 [數據與分析解決方案],小節「將上車地點聚合到區域中」)｜Canvas 頁:<https://canvas.uts.edu.au/courses/42610/pages/an-li-yan-jiu-cheng-ke-xu-qiu-shu-ju-yu-fen-xi-jie-jue-fang-an>
> 工具:genial.ly(標題「420048 Passenger Demand」)<https://view.genial.ly/62217da315825c00179d8f53>
> 內容:**單頁、單張靜態圖片(原圖 2000×1310)**,唯一的按鈕是右下角「Full screen(全螢幕)」;沒有熱點、沒有翻頁、沒有文字層。抓取:2026-10-24
> 性質:**閱讀素材,不是活動,沒有作答也沒有計分**
> 截圖:[img/M352284_12_genially_上車點與區域地圖.jpg](img/M352284_12_genially_上車點與區域地圖.jpg)

## 頁面怎麼介紹這張圖(Canvas 頁原文重點)

> 下圖展示了上車地點(綠色點)和出租車區域(藍色多邊形)。由於行程數據中的每個上車地點都是一個包含緯度和經度信息的 GPS 點,因此,數據預處理任務中的一個主要挑戰是識別包含某個特定上車地點的出租車區域。

接著說明用 **點落在多邊形內(Point-in-Polygon)疊加分析** 解決:把上車 GPS 點疊到區域多邊形上,判斷每個點落在哪一區 → 行程數據多一個「出租車區域 ID」欄位。

## 圖的內容描述

- **底圖**:Google 地圖風格的街道圖。從地標判斷是**美國紐約曼哈頓中城(Midtown Manhattan)**:Times Square、Rockefeller Center(洛克斐勒中心)、St. Patrick's Cathedral、Grand Central Terminal(中央車站)、Bryant Park、Port Authority Bus Terminal、MetLife Building、Madison Ave、Lexington Ave 等。(課程頁沒有明講城市,這是我從地圖判斷的。)
- **粗藍線**:出租車區域(taxi zone)的多邊形邊界。區域沿著曼哈頓斜向的街廓切成長方形/不規則多邊形。
- **大量小綠點**:每一點 = 一筆行程的上車 GPS 位置。
- **肉眼可見的分布**:綠點大多落在街道上、常沿著大道排成線,在 Times Square、Grand Central、Rockefeller Center 一帶特別密;Bryant Park 公園內比較稀疏(仍有零星幾點)。有些點剛好壓在藍色邊界線附近 → 這正是 Point-in-Polygon 要處理的「這點到底算哪一區」。
- 圖上沒有任何文字說明、圖例或數字。

## 老師想讓你學的事

- **原始 GPS 點不能直接拿來做區域需求分析**,要先做空間聚合(spatial aggregation):點 → 區域 ID。這是數據預處理(2.3)的一個具體例子。
- 聚合之後才能做頁面接著講的:**趨勢分析**(每區按小時/星期幾/每月日期/月份的需求)、**熱點分析**(高需求區域)、**監督學習預測模型**(行程數據有標註 → 監督式;可用線性模型或深度學習)。
- 頁面兩個「提示」是在暗示作業:**依專案目標與數據可用性慎選數據集**、**你可能需要設計自己的分析解決方案**(AT2 計畫、AT3 分析報告)。
- 這張圖也可當 AT3 視覺化的參考:地圖疊點＋區域邊界,能一眼看出「點落在哪一區」。

## 補充(我的理解,非課程原文)

- 實作上常用 GeoPandas 的 `sjoin`(spatial join)或 Shapely 的 `contains` 來做 Point-in-Polygon;區域檔就是頁面說的 shapefile。
- 紐約市計程車委員會(NYC TLC)有公開的行程紀錄與 taxi zone shapefile,與本案例的欄位描述高度相似;若 AT 要找公開數據可參考(課程頁沒有指定這個來源)。
