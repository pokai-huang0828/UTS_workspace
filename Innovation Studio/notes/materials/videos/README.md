# B 站影片素材索引(Innovation Studio 421048)

整理日期:2026-10-24。來源清單:`notes/raw/inventory_2026-10-24.tsv` 裡所有 `player.bilibili.com` 嵌入列與 `link-video` 列。

> 盤點表實際是 **7 筆嵌入(iframe)+ 3 筆連結(link-video)= 10 列、10 支不重複影片**(M352284#11 一頁有 2 支)。派工說明寫「8 筆 iframe／11 支」,和盤點表對不上;已用 `grep` 全檔搜尋 `bilibili`、`BV1`,課程筆記 00/01/02 裡也只出現這 10 個 BV 號。

## 一覽表
| 位置 | 課程頁 | 影片 | 長度 | 必看? | 筆記 |
|---|---|---|---|---|---|
| M352280#5 | 課程導學・團隊組建(教學資源 2) | 5 Dysfunctions of a Team(團隊的 5 個障礙,Blinkist) | 1:38 | 第 1 週會議前要看 | [BV1mqqLYWEj5_團隊的五大障礙.md](BV1mqqLYWEj5_團隊的五大障礙.md) |
| M352282#4 | 單元一 1.2 大數據 | What Is Big Data?(5V、Hadoop,Simplilearn) | 5:12 | 頁內影片 | [BV1KU411F76G_什麼是大數據.md](BV1KU411F76G_什麼是大數據.md) |
| M352282#5 | 單元一 1.3 數據類型 | 結構化 vs 非結構化數據(365 Data Science 動畫) | 1:48 | 頁內影片 | [BV1Fqjb6bEuT_結構化與非結構化數據.md](BV1Fqjb6bEuT_結構化與非結構化數據.md) |
| M352282#23 | 單元一 1.17 風險考量 | The Error of Our Ways(Kevlin Henney) | 54:23 | 延伸 | [BV1f54y1w7tz_我們行徑中的謬誤_KevlinHenney.md](BV1f54y1w7tz_我們行徑中的謬誤_KevlinHenney.md) |
| M352282#23 | 單元一 1.17 風險考量 | Seven Ineffective Coding Habits(Kevlin Henney) | 54:28 | 延伸 | [BV1vj411P7cT_程式設計師的七種低效習慣_KevlinHenney.md](BV1vj411P7cT_程式設計師的七種低效習慣_KevlinHenney.md) |
| M352284#4 | 單元二 2.2 監督與無監督學習 | 機器學習及其類型(Simplilearn 動畫) | 7:52 | 頁內影片 | [BV1HK411J7Zq_監督與無監督學習.md](BV1HK411J7Zq_監督與無監督學習.md) |
| M352284#8 | 單元二 2.6 圖形與圖表 | 合集 P7「Which is the best chart? Part I」(365 Data Science) | 12:08 | 頁內影片 | [BV1dZ4y1N7jw_P7_如何選擇合適的圖表.md](BV1dZ4y1N7jw_P7_如何選擇合適的圖表.md) |
| M352284#11 | 單元二 2.9 良好的數據可視化 | David McCandless:數據可視化之美(TED) | 18:18 | 延伸 | [BV1fJ411m7ZZ_McCandless數據可視化之美.md](BV1fJ411m7ZZ_McCandless數據可視化之美.md) |
| M352284#11 | 單元二 2.9 良好的數據可視化 | 1500–2020 世界人口最多的 20 個城市(動態長條圖) | 5:41 | 延伸 | [BV17p4y1Q719_1500至2020世界最大城市.md](BV17p4y1Q719_1500至2020世界最大城市.md) |
| M352284#18 | 單元二 2.13 集成 | Bagging and Random Forests(Bloomberg ML,David Rosenberg) | 33:48 | 延伸 | [BV1zE411D7w2_Bagging與隨機森林_Bloomberg.md](BV1zE411D7w2_Bagging與隨機森林_Bloomberg.md) |

## 怎麼看的(全部影片共通)
- **命令列抓不到**:yt-dlp(不帶 cookie)對 B 站全部失敗 — API 回 412(風控)、影片頁伺服器端資料被清空(`Unable to extract initial state`),Bash 沙箱的 DNS 也時好時壞,curl 下載影片串流同樣失敗。依規定不使用瀏覽器 cookie。
- **改用內建瀏覽器正常觀看**(未登入):讀影片頁上的公開資料(標題、UP 主、長度、分 P、簡介、標籤、字幕清單),再把播放器跳到指定秒數截圖,逐張看畫面。沒有解任何驗證碼、沒有登入、沒有留言或互動。
- **字幕**:10 支在未登入狀態下平台字幕清單都是空的。其中 2 支畫面有燒錄英文字幕(團隊 5 障礙、McCandless),可直接讀。其餘 8 支**沒有音訊逐字稿**(沒有語音轉文字工具),內容依畫面／投影片整理,每份筆記都有註明。
- 未登入只能看到 360p,小字偶爾看不清,筆記裡有標出。

## 給後續整合的重點提示
- **KNN 歸類差異**:2.2 課程頁把「K 最近鄰」列在無監督學習,但影片(與一般教科書)用 KNN 做有標籤的分類 = 監督式。測驗／報告遇到要小心(詳見 BV1HK411J7Zq 筆記)。
- **p=7&t=1706 的意思**:合集 P1–P6 長度加總剛好 1706 秒,所以就是「從 P7 開頭看」,P7 全長 12:08 = 課程頁寫的 12 分鐘。
- **選圖速查表**(長條／圓餅／甜甜圈／折線／面積各自什麼時候用、什麼時候避免)在 BV1dZ4y1N7jw 筆記,可直接用於 AT 報告選圖。
- **風險案例庫**(Reinhart–Rogoff 試算表錯誤、Knight Capital、left-pad、「簡單測試能預防多數重大故障」)在 BV1f54y1w7tz 筆記,可用於 AT 報告的風險段落。
- **團隊經營**:Lencioni 5 障礙(信任 → 衝突 → 承諾 → 當責 → 結果)可搭配 Tuckman 階段,用在團隊章程或團隊反思。
