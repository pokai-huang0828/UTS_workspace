# 單元四 內嵌練習與討論擬答

> 建立 2026-07-26 · 活文件(依 [`notes/README.md`](README.md) 規則不加日期前綴)
> 體例沿用 [`Unit2-3_內嵌練習擬答.md`](Unit2-3_內嵌練習擬答.md):**Kenny 自己貼**,agent 不代填 Canvas。
> 單元四共 **12 個要作答/投寄的項目**(定義 B),盤點依據見
> [`Assessment2b/A2b_單元四_知識架構與學習記錄.md`](../Assessment2b/A2b_單元四_知識架構與學習記錄.md)。

---

## ✅ 4.1.2 K 均值聚類在現實資料中的應用(必修投寄)

**題目**(raw 行 257):「請在下方討論區分享你的想法:你將如何把 K 均值聚類應用於一個假設資料集,
從而獲得與你的工作場景或任何感興趣領域(例如烹飪食材)的見解。」

### 前置活動狀態

| 步驟 | 狀態 |
|---|---|
| 1. 在 Jupyter 開啟 `clustering_song` | ✅ `notes/practice/clustering_song_updated.ipynb`(與 Canvas 版 SHA-256 相同) |
| 2. 執行程式碼跑完 K-means | ✅ **27 cells 零錯誤 + 7 張圖**,執行後副本 `clustering_song_updated_RUN_local.ipynb` |
| 3. 到討論區分享想法 | ⬜ **下面這段,Kenny 自己貼** |

> 本機執行唯一改動:Colab 掛載那格改成 `%matplotlib inline` + 本機說明。原檔未動。
> 資料 `notes/practice/nigerian_spotify_songs1.csv`(Kenny 自 Kaggle 下載,530 首 × 16 欄)。

### 貼文·中文版(**用這個直接貼**;2026-07-26 依 Kenny 指示改中文)

> ⚠️ 初版誤設為英文。回讀 [`Unit2-3_內嵌練習擬答.md`](Unit2-3_內嵌練習擬答.md) 確認:
> 3.2.4、3.3.1 兩則必修投寄的擬答**都是繁體中文**,技術詞中英並陳。本版沿用該體例。

```text
跑完 clustering_song 之後,我最大的收穫其實來自它「沒做對」的地方,所以我自己的設計是圍繞著「不要重蹈覆轍」。

一、我在課程 notebook 裡看到的問題

依 notebook 的流程篩選後剩 286 首歌,用了六個沒有標準化的特徵。popularity 的標準差是 17.73,danceability 只有 0.11,換算下來 popularity 這一個變數就佔了總距離平方和的 98.1%。所以 k=3 分出來的三群,實際上只是把人氣切成三段(1–20、21–42、43–73);三群的 danceability 質心落在 0.731 到 0.770 之間,幾乎沒有差別。曲風也沒有被分出來——全體基準是 72/21/7,偏離最大的一群也不過是 afropop 佔到 32%。silhouette 看起來還可以(k=3 為 0.5467),但 k=2 更高(0.5628),而且把資料標準化之後整體掉到 0.19–0.23。那個好看的分數,本質上只是一個變數被切成三段。

二、我會怎麼把 K-means 用到自己的資料上

我想用的是一家澳洲零售銀行的客戶資料(也是我 A1 寫的產業)。特徵我會取:每月交易筆數、平均帳戶餘額、App 對臨櫃的互動比例、持有產品數、距離上次購買產品的月數。這些都是「數值越大代表距離越遠」的個人量級指標,但單位彼此不一致,所以一定要標準化。另外餘額與交易筆數是右偏的,而 z-score 只能拉平離散程度、拉不平偏態,所以我會先取對數再標準化,否則少數大戶會重演 popularity 那一招。客戶 ID 與郵遞區號要排除;我也絕不會像 notebook 那樣把曲風用 LabelEncoder 編成 0/1/2 丟進歐氏距離——那等於替名目變數憑空製造了順序。在這份資料裡它只佔 0.1% 所以沒出事,但標準化之後就會咬人。

三、預期的分群,以及它會改變哪一個決策

如果 silhouette、肘部法(Elbow)與不同隨機種子的穩定性都指向 k=4,我預期會看到:數位優先的多產品活躍戶、依賴臨櫃的低數位客群、高餘額但只持有單一產品者,以及沉睡帳戶。k=4 是預期,不是設定值。

真正會被改變的決策,是客戶經理每月的電訪配額——目前是按帳戶餘額高低排。如果「高餘額、單一產品」那一群真的出現,配額就先給這一群,群內再依「距離該群質心的遠近」排序。因為任何一群的人數都遠大於配額,分群本身並不會告訴你該先打給誰。

我自己最沒把握的是「距離上次購買的月數」這個特徵:它衡量的是時近性而不是行為模式,而且很可能像 popularity 一樣主宰整個距離。大家覺得這個該留嗎?
```

**1,050 字**(不含空白;程式實測)。所有數字**逐項比對**過下方「數字全部獨立重算過」那張表:
17 個數字全數吻合,反向檢查也未混入任何未驗證的數字。
⚠️ 中文行文本身**未經第三方語言複核**,只有數字經過機械驗證。

<details>
<summary>備用:英文版(303 words)</summary>

```text
The clustering_song notebook taught me more by failing than by working, so I built mine around not repeating it.

286 filtered tracks went in with six unscaled features. Popularity's SD is 17.73 against danceability's 0.11, so popularity alone drives 98.1% of the total squared distance. k=3 therefore just cut popularity into bands (1-20, 21-42, 43-73) whose danceability centroids sit between 0.731 and 0.770, and genre barely follows: against a 72/21/7 base rate, the largest shift is one cluster at 32% afropop. Silhouette looked fine at 0.5467; k=2 scored higher (0.5628), and standardising dropped it to 0.19-0.23. That score was one variable sliced into three.

My own dataset: customers of an Australian retail bank, the industry from my A1. Features: monthly transaction count, average balance, in-app versus branch interaction share, products held, months since last product purchase. All are per-customer magnitudes where "more" means "further away", but units are mixed, so I standardise. Balance and transactions are also right-skewed, and z-scoring equalises spread, not skew, so I'd log those two first, otherwise a few whales redo popularity's trick. ID and postcode go, and I'd never label-encode a category the way the notebook coded genre 0/1/2: that invented ordering moved only 0.1% here, but bites once scaled.

If silhouette, the elbow and seed stability agreed on k=4, I'd expect: digital-first multi-product actives, branch-reliant low-digital users, high-balance single-product holders, and dormant accounts. Four is a guess, not a setting.

The decision it changes: the bank's monthly quota of relationship-manager calls, today ordered by balance. If the high-balance single-product cluster appears, it takes those calls, ranked inside the cluster by distance to its centroid, because any cluster dwarfs the quota.

The feature I'm least sure about is months since last purchase: that's recency, not behaviour, and it could dominate the way popularity did. Would you keep it?
```

</details>

### 配圖(2026-07-26 加,本機實跑產生)

| 圖 | 檔案 | 用途 |
|---|---|---|
| **A(推薦,貼這張就夠)** | [`figures/fig_412_why_it_failed.png`](practice/figures/fig_412_why_it_failed.png) | 左:各特徵佔距離平方和比例(popularity 98.1%)· 右:課程 k=3 的散佈圖,三條垂直帶 |
| B(選用) | [`figures/fig_412_scaling_effect.png`](practice/figures/fig_412_scaling_effect.png) | 標準化前後「是什麼在分群」的對照長條 |

**圖 A 建議圖說**:
> 左:未標準化時 popularity 佔了總距離平方和的 98.1%。右:因此 k=3 的界線全落在
> popularity 上(1–20 / 21–42 / 43–73),danceability 從頭到尾沒被用到。

**圖 B 的新數據**(質心全距,z 單位 —— 這組數字圖 A 沒有,若用圖 B 才需要):

| 特徵 | 未標準化 | 標準化後 |
|---|---|---|
| popularity | **2.44** | 1.60(退到第三) |
| energy | 0.52 | **2.00** |
| loudness | 0.24 | **1.83** |
| genre(編碼) | 0.22 | 1.47 |
| acousticness | 0.08 | 0.90 |
| danceability | 0.35 | 0.66 |

⚠️ **初版圖 B 標題寫「群不再只看人氣」是過度宣稱**,已改。正確說法是:標準化後
**六個特徵全部開始起作用,popularity 從獨佔退到第三**,不是不再看人氣(它仍有 1.60)。

用圖 B 的話,第一段可加一句(可選):
> 把資料標準化之後,主導分群的變成 energy(2.00)與 loudness(1.83),popularity 退到第三(1.60)
> ——六個特徵這時才真的都在起作用。

### 一個建議(你的修訂版拿掉了結尾提問)

你刪掉了「大家覺得這個該留嗎?」。題目寫的是「與同學**分享**你的理解」,4.1.2 又是討論區,
**留一個開放問題比較容易引來回覆**,也讓貼文看起來像對話而不是報告。要不要加回去你決定。

### 貼之前 Kenny 自己決定的三件事

1. **要不要點名 CBA。** 現在寫 "an Australian retail bank"(不具名但屬實 —— `notes/raw/A1_body_extract.txt` 出現 CBA ×14、Commonwealth Bank ×8)。想點名就自己改。
2. **"the bank's monthly quota"** 已從草稿的 "our" 改掉,避免暗示你在該銀行任職。要改回 "our" 是你的選擇。
3. **想換成自己真實的工作領域**:只需替換第 3、5 段的特徵與決策,**第 2 段的診斷可以原封不動**(那段是這則貼文的價值所在)。

### 數字全部獨立重算過(R-獨立)

產出者是工作流的合成 agent;下列數字由主迴圈**用原始 CSV 重跑一次**核對,非採信 agent 回報:

| 主張 | 重算值 |
|---|---|
| 286 tracks | 286 |
| popularity SD 17.73 / danceability 0.11 | 17.7326 / 0.1122 |
| popularity 佔距離平方和 98.1% | 98.06% |
| bands 1-20 / 21-42 / 43-73(n=110/111/65) | 完全吻合 |
| danceability 質心 0.731–0.770 | 0.731 / 0.746 / 0.770 |
| silhouette 原始 k=2 0.5628 / k=3 0.5467 | 相同 |
| 標準化後 0.19–0.23 | 0.2238(k=2)/ 0.1912(k=3) |
| label-encoded genre 只佔 0.1% | 0.112% |
| 曲風基準 72/21/7 | 72.0 / 21.3 / 6.6 |
| 「最大偏離為某群 32% afropop」 | 各群 17.1 / 19.1 / **32.3** |

⚠️ **主迴圈推翻合成 agent 的一處裁決**:原句寫 `every mix stays near the 72/21/7 base rate`,
但第三群是 61.5/32.3/6.2,afropop 為基準的 1.5 倍,**「stays near」是事實誇大**。
已改為指名最大偏離值。合成 agent 自己標出了這條缺陷卻因字數預算選擇不改 —— 公開貼文不接受這種取捨。

---

## ⬜ 4.1 內嵌問答(H5P,頁內提交)

**題目**(頁內 H5P 元件,**純文字抓取看不到**,2026-07-26 瀏覽器實查):

> 聚类也有助于异常值检测。你能想到一个例子吗?

有作答框 + **提交**鈕,目前空白。課程依據:raw 行 45「聚类通常用于支持…异常值检测」。

⬜ **待擬答**。方向:銀行/電信的異常交易或異常用量偵測 —— 把絕大多數樣本聚成少數大群後,
落在所有質心都很遠的點即為候選異常;優點是不需要標籤(承接 raw 行 41 的無監督定義)。

---

## ✅ 4.2 思考與分享(Atomic Discussions 頁內回覆框)

**題目**(raw 行 131–132):「在熟悉這些工具之前,請思考真實的人工智慧專案,它們的優勢與劣勢。
這將幫助你在資料分析翻譯師這一角色中取得成功。請在下方文字框中分享你的想法。」

**課程脈絡**(raw 行 111–118):Henke, Levine & McInerney (2018) HBR;分析翻譯師 =
AI 團隊與其他職能之間的**中介**,需要**領域知識(domain knowledge)**
+ **一般技術理解能力(general technical fluency)**。

### 貼文(直接貼這段,463 字)

```text
我最大的體會是:AI 專案最危險的失敗,是「安靜地失敗」。

剛做完的 4.1.2 K-means 分群就是活例:課程 notebook 的 27 個 cell 全跑完、零錯誤,輪廓係數(silhouette)0.5467 也很體面。但六個特徵沒有標準化(standardisation),popularity 的標準差 17.73、danceability 只有 0.11,光 popularity 就吃掉總距離平方和的 98.1%。k=3 的三群其實只是把人氣切成 1–20、21–42、43–73,三群 danceability 質心落在 0.731–0.770 幾乎無差,曲風完全沒被分出來;更諷刺的是 k=2 的 silhouette 反而更高(0.5628),標準化後整體掉到 0.19–0.23。

優勢我一樣有感,而且同樣有數字。A2a 電信流失預測的流失率只有 14.49%,代表挽留名單本來就不該全打;模型讓名單從憑印象挑人變成可排序、可事後驗證,最佳模型在測試集的偽陽性(False Positive)是 24 個,把這 24 通白打的電話乘上單通成本,就是能拿去跟業務單位談的語言。

但同一個 14.49% 也是陷阱:全部猜「不會流失」就有 85.5% 的準確率(accuracy)。這種不平衡技術端查得到,查不到的是「漏掉一個真流失客戶(偽陰性,False Negative)值多少錢」;K-means 那種更徹底,連錯誤訊息都沒有,預設指標不會亮紅燈。兩種都要有人問「這在回答哪個商業問題」才會浮上來。

我 A1 案例研究(一家澳洲零售銀行)失分也是同一病因:寫「成本收入比下行」卻沒給基準值、目標值與期間,也沒做跨方案的成本比較,AI 能力只拿 18.75/25。Henke、Levine 與 McInerney(2018)講的資料分析翻譯師(analytics translator),就是站在 AI 團隊與其他職能中間的人,用領域知識(domain knowledge)加一般技術理解能力(general technical fluency),讓洞察真的在組織裡變成大規模的實際影響——而那份影響,最後是寫成有基準值、有期間、有負責人的交付物。
```

### 數字全部獨立重算過(R-獨立)

產出者是工作流的合成 agent;下列由主迴圈**回到原始資料重算**,非採信 agent 回報:

| 主張 | 驗證來源 | 結果 |
|---|---|---|
| 流失率 14.49% | `Assessment 2a Cellphone-1.csv`(3,333 列)`Churn` 欄重算 | **14.4914%** ✅ |
| 全猜不流失 accuracy 85.5% | 100 − 14.4914 | **85.51%** ✅ |
| **最佳模型測試集 FP = 24** | `a2a_results.json`:`winner = XGBoost`,`test_table[5].fp = 24` | ✅ |
| A1「AI 能力」18.75/25 | `A1_成績復盤與優化清單.md` §一 | ✅ |
| K-means 那組全部數字(8 項) | `nigerian_spotify_songs1.csv` 重跑 | ✅ 見上方 4.1.2 節對照表 |
| Henke, Levine & McInerney (2018) | `raw/Unit4_canvas_raw.txt` 行 340 參考文獻 | ✅ |

⚠️ **查核時發現的陷阱**:`test_table` 六個模型的 FP 分別是 15 / 25 / 62 / 118 / 201 / **24**,
`24` 只有在「最佳模型 = XGBoost」成立時才是對的。已從 `a2a_results.json` 的
`winner` 欄確認為 XGBoost。附帶確認選模邏輯正確 —— XGBoost 是靠交叉驗證勝出,
測試集上 RandomForest 的 F1 其實略高(0.7451 vs 0.7148),**測試集只用一次**,
沒有挑分數最好看的。

18 個事實 token 以腳本逐項比對,零缺漏;反向檢查未混入未驗證數字。
⚠️ 中文行文本身**未經第三方語言複核**。

---

## ⬜ 4.2.1 趨勢分析工具(Canvas 討論,必修投寄)

**題目**(raw 行 289–296)三問:
1. 趨勢分析工具會如何被生成式 AI 提升?
2. 假設你是澳洲某大學的市場分析師,你會怎麼用趨勢分析工具?
3. **對另一位同學的回答留言並給建設性回饋。**

⬜ **待擬答**。⚠️ 第 3 點是額外動作,別漏。

---

## ⬜ 4.2.2 思考與分享(Atomic Discussions 頁內回覆框)

**題目**(raw 行 148–153)兩問:生成式聊天機器人 vs Microsoft LUIS / Siri 有何不同?
這類工具未來的優勢與挑戰?⬜ **待擬答**。

---

## ⬜ 4.2.3 快速任務(Atomic Discussions 頁內回覆框)

**題目**(raw 行 192–195):想辦法讓你訓練的 Teachable Machine 模型**分類失敗**,並分享給同學。
頁面自己給了範例(青蘋果貼上手寫 "iPod" 標籤 → 模型從 Granny Smith 85.6% 翻成 iPod 99.7%)。

⬜ **待擬答**。⚠️ 這題要先真的去 teachablemachine.withgoogle.com 訓練一個模型並截圖,
不能純文字作答。

---

## ⬜ 4.2.4 快速塗鴉(Canvas 討論,必修投寄)

**題目**(raw 行 318–321):玩 6 次 Quick, Draw!,**記錄每次畫的物件與成功/失敗**,
前 4 次後與同學討論發現,再玩 2 次看有沒有進步。

⬜ **待擬答**。⚠️ 需要 Kenny 本人實際去玩並記錄,agent 產不出這個資料。

---

## 📌 4.2.5 圖像生成(非投寄,但頁面未讀)

單元四唯一未查看的頁面。內容:ModelScope、Stable Diffusion、ToonCrafter、
生成式 AI 的幻覺問題、提示詞工程。無作答框。
