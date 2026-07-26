# A2b 學習記錄 — 單元四:非監督式學習(2026-07-26 由 Canvas 實抓)

> 抓取範圍:單元四(Module 4)全部 11 個子項目,逐頁 `get_page_text` + 關鍵頁面截圖覆核。未下載任何檔案、未在 Canvas 發文/送出/點提交。

## 一、單元四頁面地圖

| 頁面 | URL | 一句話重點 | 必修投寄? |
|---|---|---|---|
| 單元四概述 | https://canvas.uts.edu.au/courses/42198/pages/dan-yuan-si-gai-shu?module_item_id=2783601 | 本週兩大主題:①聚類基礎概念 ②互動演示與系統;目標為定義ML、區分監督/非監督學習、概述ML技術範圍與局限 | 否 |
| 4.1 聚類(clustering)基礎(無監督學習) | https://canvas.uts.edu.au/courses/42198/pages/4-dot-1-ju-lei-clustering-ji-chu-wu-jian-du-xue-xi?module_item_id=2783603 | 聚類=不用預定義標籤分組;可降低資料複雜度、支援分類/預處理/異常偵測;實務案例含市場細分、隱私保護(用聚類編號取代個資) | 否 |
| 4.1.1 進行聚類分析 | https://canvas.uts.edu.au/courses/42198/pages/4-dot-1-1-jin-xing-ju-lei-fen-xi?module_item_id=2783605 | K-means 三步驟流程圖(初始中心→分配最近中心→重算均值,重複至不再移動);附下載練習檔 `K_means_basic`(30分鐘,未下載) | 否(僅練習活動) |
| 4.1.2 K均值聚類在現實資料中的應用(討論主題) | https://canvas.uts.edu.au/courses/42198/discussion_topics/771448?module_item_id=2783607 | 用 Kaggle Nigerian Spotify 歌曲資料(16特徵)實作,notebook 檔名 `clustering_song`;要求討論如何把K-means用到自己感興趣的假設情境 | 否(模組頁無「投寄」標記,對照3.2.4/4.2.1「已投寄」字樣可確認;Kenny 尚未回覆) |
| 4.2 互動演示與系統 | https://canvas.uts.edu.au/courses/42198/pages/4-dot-2-hu-dong-yan-shi-yu-xi-tong?module_item_id=2783609 | 介紹「數據分析翻譯師」(analytics translator)角色定義,導覽NLP/電腦視覺互動demo清單 | 否 |
| 4.2.1 趨勢分析工具(討論主題) | https://canvas.uts.edu.au/courses/42198/discussion_topics/771442?module_item_id=2783611 | Google Trends/百度指數等;需回答2題+回覆1位同學 | **是,目前未完成**(模組頁顯示「投寄 必須完成此單元項目」,非「已投寄」) |
| 4.2.2 語言理解實戰 | https://canvas.uts.edu.au/courses/42198/pages/4-dot-2-2-yu-yan-li-jie-shi-zhan?module_item_id=2783613 | Microsoft LUIS 意圖辨識demo;比較生成式AI聊天機器人與LUIS/Siri | 否 |
| 4.2.3 圖像分類[Teachable Machine] | https://canvas.uts.edu.au/courses/42198/pages/4-dot-2-3-tu-xiang-fen-lei-google-teachable-machine?module_item_id=2783615 | 用Teachable Machine訓練"生氣臉vs微笑臉"分類器;快速任務嘗試讓模型誤判 | 否 |
| 4.2.4 人工智能的趣味應用:快速塗鴉!(討論主題) | https://canvas.uts.edu.au/courses/42198/discussion_topics/771450?module_item_id=2783617 | Quick,Draw!神經網路猜圖遊戲;玩6次記錄成功/失敗,討論後再玩2次比較 | **是,目前未完成** |
| 4.2.5 圖像生成 | https://canvas.uts.edu.au/courses/42198/pages/4-dot-2-5-tu-xiang-sheng-cheng?module_item_id=2783619 | ModelScope/Stable Diffusion/ToonCrafter demo;討論生成式AI幻覺問題+提示詞工程 | 否 |
| 4.3 第四週總結與問題(討論主題) | https://canvas.uts.edu.au/courses/42198/discussion_topics/771446?module_item_id=2783621 | 總結單元二~四(監督式vs非監督式學習全貌);開放問答 | 否(頁尾另有「模組4參考文獻列表」連結,受12頁上限未展開,見六節) |

## 二、核心概念(白話 + 為什麼重要)

**① K-means 運作原理(質心、迭代、收斂)—— 課程有教**
出處:4.1.1。三步驟:(1) 隨機選幾個初始聚類中心 (2) 把每個樣本分配給距離最近的中心 (3) 重新計算每個聚類的均值當新中心;重複(2)(3)直到中心不再移動(收斂)。白話:K-means 就是「猜中心→分組→修正中心」不斷循環,直到分組穩定。為什麼重要:這是 A2b notebook 要跑出來的核心演算法,也是 rubric 第3、4條「解釋聚類特徵」「用質心表論證」的技術基礎。

**② 聚類的用途與定位 —— 課程有教**
出處:4.1。聚類常用來:降低資料複雜度(用n個聚類中心代表大量個體記錄)、輔助分類/預處理/異常偵測、保護隱私(用聚類編號取代個人識別)。為什麼重要:呼應A2b題目本身(IBM用聚類把顧問員工分組發獎金,而非逐一分析每個員工)。

**③ 如何選 k:elbow method 與 silhouette score —— ⚠️讀不到,課程單元四文字頁面完全沒出現這兩個詞**
我逐字讀過 4.1、4.1.1、4.1.2 三頁全文,搜尋不到「elbow」「肘部」「silhouette」「轮廓系数」等字樣。A2b題目原文(raw檔第43行)明確要求用轮廓系数(silhouette score)找最優k,並提示「有時需要肘部法(Elbow method)輔以確認」——但單元四的Canvas頁面文字本身沒有教這兩個方法,只給了K-means三步驟的原理說明。判斷:這兩個方法應該是寫在兩個下載練習檔(`K_means_basic`、`clustering_song`)的Jupyter notebook程式碼裡,而不是頁面文字內,尚未下載確認。
⚠️ 非課程內容(補充一般知識,供理解用,實際寫法仍需以下載後的notebook為準):elbow method是畫「k值 vs 群內平方和(inertia/WCSS)」的折線圈,找曲線彎折像手肘的點;silhouette score則是量化「每個點離自己群近、離別群遠」的程度,分數愈接近1愈好。

**④ 排除變量的理由 —— ⚠️讀不到,課程單元四文字頁面沒有教「哪些變量該排除」的判斷原則**
4.1 只講了聚類的一般用途與案例,沒有出現「不應考慮的變量」「ID類欄位」等特徵工程判斷語言。這正是A2b rubric第1條(20分)的核心,但目前找不到課程原文依據。

**⑤ 質心表怎麼解讀、如何反標準化回原始單位 —— ⚠️讀不到,課程單元四文字頁面沒出現「質心表」「Centroid Table」「反標準化」等字樣**
4.1 只提到「聚類中心可作為該聚類的代表性觀察」這個概念層次的說明,沒有示範具體的質心表格長什麼樣、標準化後的質心值如何換算回原始單位(usage rate/recognition/leader 的實際數值)。這是A2b rubric第4條(25分)最大的技術缺口。

**⑥ 標準化(scaling)為何必要 —— ⚠️讀不到,課程單元四文字頁面沒有討論標準化**
K-means用歐式距離計算相似度,若三個變量(使用率、認可度、領導角色)尺度不同,量綱大的變量會主導距離計算。這是統計/機器學習的一般常識(⚠️非課程內容,單元四頁面文字沒有明確教這點),但單元二(2.2/2.3)有教統計描述與資料轉換,可能是伏筆,惟本次抓取範圍限定單元四,未回頭核對單元二頁面。

## 三、課程給的程式碼片段

**單元四的頁面文字裡沒有任何內嵌可直接複製貼上的程式碼。** K-means相關的實際程式碼都封裝在兩個「下載後用Anaconda/Jupyter開啟」的notebook檔案裡,頁面本身只給操作說明:
- `K_means_basic`(出自 4.1.1,https://canvas.uts.edu.au/courses/42198/pages/4-dot-1-1-jin-xing-ju-lei-fen-xi?module_item_id=2783605):操作指南是「用Anaconda『打開筆記本』開啟下載的檔案,依前面流程圖跑K-means三步驟」,無逐字程式碼。
- `Clustering song`(出自 4.1.2,https://canvas.uts.edu.au/courses/42198/discussion_topics/771448?module_item_id=2783607):資料來源Kaggle「Nigerian songs Spotify data」(16個特徵,含danceability/acousticness/loudness/speechiness/popularity/energy等),操作指南同上,無逐字程式碼。

兩個檔案均**尚未下載**(不在本次≤4個本機讀檔額度內,且下載檔案需另外向 Kenny 確認),故無法核對其中是否已內建 elbow/silhouette/標準化/質心表的範例程式碼——這點強烈建議列為下一步優先動作(見第六節)。

## 四、內嵌練習與必修投寄

| 項目 | 題目原文摘要 | 目前狀態 |
|---|---|---|
| 4.1.1 K均值聚類活動 | 下載`K_means_basic`,用Anaconda跑K-means三步驟,預估30分鐘 | 練習性質,非必修投寄;未做 |
| 4.1.2 K均值聚類在現實資料中的應用 | 下載`clustering_song`跑K-means於Spotify資料,並在討論區分享「如何把K-means用到你的工作場景或興趣領域(如烹飪食材)」的想法,預估30分鐘 | 非必修投寄(模組頁無「投寄」標記);Kenny尚未回覆 |
| **4.2.1 趨勢分析工具** | 討論區回答:①生成式AI會如何提升趨勢分析工具?②身為澳洲大學市場分析師會如何用趨勢分析工具?另需回覆1位同學 | **必修投寄,目前未完成** |
| 4.2 互動演示與系統(頁尾反思) | 「思考與分享」文字框,反思真實AI專案的優劣勢 | 非必修投寄形式的自由填答;未做但非強制 |
| 4.2.3 圖像分類快速任務 | 嘗試讓Teachable Machine訓練出的模型誤判,並分享給同學 | 非必修投寄;未做 |
| **4.2.4 快速塗鴉** | 玩6次Quick,Draw!,記錄物品名+成功/失敗,與同學討論後再玩2次比較進步 | **必修投寄,目前未完成** |
| 4.3 第四週總結與問題 | 開放問答,未解決問題留到下次Zoom | 非必修投寄 |

**兩個必修投寄(4.2.1、4.2.4)目前皆未完成**,與 handoff 記載一致。

## 五、A2b 四條 rubric 對應到單元四哪裡

| rubric 條(分) | 單元四哪一頁/哪個概念 | 目前缺什麼 |
|---|---|---|
| 不應考慮的變量識別(20分) | 4.1 聚類基礎(僅講聚類一般用途,未教特徵篩選判斷原則) | 課程文字頁**沒有**教「哪些變量不該進聚類」的判斷方法;需查 `K_means_basic`/`clustering_song` notebook 是否有範例,或自行以統計常識論證(如ID類標稱變量無距離意義) |
| 最佳聚類數的識別(20分) | 4.1.1 進行聚類分析(只給K-means三步驟流程圖) | **elbow method、silhouette score 兩個關鍵方法,單元四頁面文字完全沒出現**,是本次抓取最大缺口,必須另外查兩個下載notebook或自學補上 |
| 對聚類的語言學解釋(25分) | 4.1 聚類基礎(提到「聚類中心可作代表性觀察」的概念) | 沒有課程示範「如何用商業語言描述一個cluster的整體特徵」的寫法範例 |
| 最佳表現聚類的識別(25分) | 4.1 聚類基礎(僅提及聚類中心作為代表值) | 沒有出現「質心表/Centroid Table」字樣或具體解讀/反標準化示範 |

## 六、開工前待辦

1. **下載A2b資料集**(https://canvas.uts.edu.au/courses/42198/files/12834401/download,檔名"Big Blue"/"IBM")——尚未下載。
2. **下載並打開兩個課程練習notebook**(`K_means_basic`〔4.1.1〕、`clustering_song`〔4.1.2〕),確認裡面是否已包含 elbow method、silhouette score、標準化(StandardScaler)、質心表(Centroid Table)反標準化的範例程式碼——本次Canvas頁面文字完全沒教這四項,是目前最大知識缺口,務必在寫報告前確認清楚,不要等到動筆才發現缺口。
3. **完成2個必修投寄**:4.2.1 趨勢分析工具討論、4.2.4 快速塗鴉討論(目前皆未完成,單元四無法勾選「完成所有項目」)。
4. 若下載後notebook仍未涵蓋 elbow/silhouette/標準化/質心表反標準化,需另外自學(sklearn `KMeans`、`sklearn.metrics.silhouette_score`、`StandardScaler`等),確保能在報告第1、2、4節提供「notebook中的證據」。
5. 對照A2a報告模板(封面+目錄+APA7+獨立結論)套用到A2b四節結構,四節嚴格對齊四條rubric。
6. (次要,未涵蓋)4.3頁尾「模組4參考文獻列表」連結因12頁額度已用完未展開,若報告需要單元四的官方參考文獻,之後應補讀。
