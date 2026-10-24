# BV1HK411J7Zq — 機器學習及其類型(監督／無監督／強化學習)動畫講解

## 在課程哪裡用到
- 位置:M352284#4 → 單元二 2.2「監督學習與無監督學習」(見 `notes/02_單元二_數據分析與機器學習技術概述.md` 的 `## 4.`)
- 頁面寫法:「觀看 8 分鐘」— 看監督學習與無監督學習的例子;頁面說無監督學習「從未標記數據得出結論,演算法比監督學習更複雜」。
- 嵌入網址:`https://player.bilibili.com/player.html?...&bvid=BV1HK411J7Zq&cid=213725064&p=1`

## 基本資料
| 欄位 | 內容 |
|---|---|
| 原標題(簡中) | 机器学习基础—机器学习及其类型动画演示讲解-监督学习，无监督学习和强化学习 |
| UP 主 | AI研习图书馆(轉載,copyright=2;原作是 Simplilearn,畫面右上角有 simplilearn 浮水印) |
| 長度 | 7:52(472 秒),單一分 P(P1「machine learning」) |
| 上傳日 | 2020-07-18 |
| 語言 | 英文旁白、手繪白板動畫 |
| 字幕 | 無(未登入狀態下 B 站播放器字幕清單為空) |
| 簡介重點 | 介紹什麼是機器學習、三種類型(監督／無監督／強化)、用簡單例子說明怎麼運作、各行業的應用;機器學習是 AI 的核心子領域,讓電腦不用明確寫程式也能自我學習 |

## 怎麼看的(方法與限制)
- yt-dlp 在命令列被 B 站風控擋下(API 回 412、頁面資料被清空),所以改用內建瀏覽器開影片頁,用 JS 讀頁面上的影片資料(標題、長度、分 P、字幕清單),再把播放器跳到指定秒數截圖。
- 共看了 25 張畫面(大約每 12–25 秒一張)。**沒有音訊逐字稿**(沒有字幕、也沒有語音轉文字),旁白內容是從畫面文字與動畫推得的,沒有聽到的細節不寫。

## 畫面大綱(依時間)
| 時間 | 畫面內容 |
|---|---|
| 0:12 | 開場:人在電腦前、旁邊一個機器人 —「What if humans can train the machines…」(如果人類能訓練機器?) |
| 0:45–1:35 | **聽歌例子**:一個人(Paul)聽歌,畫散布圖:x 軸 Tempo(節奏,Relaxed→Fast)、y 軸 Intensity(強度,Light→Soaring)。綠點=喜歡(Like)、紅點=不喜歡(Dislike),喜歡的歌集中在「快節奏、高強度」區,不喜歡的在「慢、輕」區。新歌 A(快節奏、高強度)落在綠群裡 → 會喜歡。 |
| 2:00 | 新歌 B(中節奏、中強度)落在兩群中間 → 大問號 →「That's where machine learning comes in」 |
| 2:25 | 用 **K-Nearest Neighbors(K 最近鄰)演算法**:看 B 周圍最近的幾個點多數是綠還是紅,來判斷 Paul 會不會喜歡 |
| 2:50 | 「MACHINE LEARNING」三張便利貼:Supervised Learning、Unsupervised Learning、(第三張是 Reinforcement Learning) |
| 3:15 | **監督學習**:硬幣例子 — 3 克、7 克、4 克三種硬幣;板書「WEIGHT : FEATURE」(重量=特徵),下一行正寫到「CUR…」(推測是 Currency 幣值=標籤) |
| 3:40 | 3 克硬幣 → 電腦 → 1 Rupee;字卡「LABELED DATA」(有標籤的資料) |
| 4:05–4:30 | **無監督學習**:一張板球選手名單(Names、Runs、Wickets 欄)→ 電腦 → 散布圖(x=Wickets 三柱門、y=Runs 跑分)自動分成兩群 → Batsmen(打擊手)與 Bowlers(投手);字卡「NO LABELED DATA」 |
| 4:55 | **強化學習**:輸入一張狗的圖 → 電腦輸出「CAT」→ 打叉、回饋箭頭(錯了就被糾正,下次改進) |
| 5:08–5:20 | **Machine Learning Model** 流程圖:Input → Model → Output,再加一條 Feedback 回饋線回到模型 |
| 5:45 | 小測驗「Supervised or Unsupervised?」:情境 1 Facebook 臉部辨識、情境 2 Netflix 電影推薦、情境 3(字還沒寫完,看不清) |
| 5:54–6:25 | 畫問號、搜尋網站(.com、放大鏡)、時鐘、資料庫圖示等過場(旁白內容無法從畫面確定) |
| 6:38 | 「APPLICATIONS OF MACHINE LEARNING」:Healthcare(醫療)、Sentiment Analysis(情緒分析)… |
| 6:50 | 汽車與手機叫車畫面 |
| 7:04 | 「Interesting machine learning model which is used by UBER」— Differential Pri(cing)(差別／動態定價) |
| 7:15 | 「It uses predictive modeling to pred(ict)…」(用預測建模來預測…) |
| 7:35 | 「Comment below some interesting everyday examples around…」(留言分享身邊的例子) |
| 7:48 | Happy Learning!(結尾) |

## 重點整理
1. **機器學習 = 讓電腦從資料學規律,而不是人寫死規則**;新資料進來,模型可以自己調整。
2. **監督學習(Supervised Learning)**:訓練資料有「標籤」(答案)。例:用硬幣重量(特徵 feature)預測幣值(標籤 label);用喜歡／不喜歡的歌訓練,判斷新歌。
3. **無監督學習(Unsupervised Learning)**:資料沒有標籤,讓電腦自己找群組。例:只給板球選手的跑分與三柱門數,電腦自己分出打擊手與投手兩群(這就是聚類 clustering)。
4. **強化學習(Reinforcement Learning)**:做出判斷 → 收到對錯回饋 → 下次修正。例:把狗認成貓被糾正。
5. **ML 模型的基本流程**:輸入 → 模型 → 輸出 → 回饋 → 再改進模型。
6. **應用**:醫療、情緒分析、Uber 動態定價(用預測模型估計需求來調價)等。

## 和課程頁面的關係
- 課程頁 2.2 只講監督／無監督兩類(含迴歸 vs 分類、對照表);影片多講了**強化學習**,是補充,不在頁面的對照表裡。
- 影片用 **KNN 做「有標籤的分類」**(喜歡／不喜歡),這是監督學習的典型用法。注意:課程頁面把「K最近鄰算法」列在**無監督學習**的例子裡,和一般教科書(KNN 屬監督式;K-means 才是無監督聚類)不同。若遇到測驗或報告要分類 KNN,建議寫「KNN 是監督式分類演算法,K-means 是無監督聚類」,必要時註明課程頁的列法。
- 影片的 Uber 動態定價例子和課程貫穿的「出租車乘客需求」案例(單元一 #24、單元二 #12)主題相近,可拿來當 AT 報告裡「預測需求」的生活化例子。
