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

### 貼文(直接貼這段,303 words)

```text
The clustering_song notebook taught me more by failing than by working, so I built mine around not repeating it.

286 filtered tracks went in with six unscaled features. Popularity's SD is 17.73 against danceability's 0.11, so popularity alone drives 98.1% of the total squared distance. k=3 therefore just cut popularity into bands (1-20, 21-42, 43-73) whose danceability centroids sit between 0.731 and 0.770, and genre barely follows: against a 72/21/7 base rate, the largest shift is one cluster at 32% afropop. Silhouette looked fine at 0.5467; k=2 scored higher (0.5628), and standardising dropped it to 0.19-0.23. That score was one variable sliced into three.

My own dataset: customers of an Australian retail bank, the industry from my A1. Features: monthly transaction count, average balance, in-app versus branch interaction share, products held, months since last product purchase. All are per-customer magnitudes where "more" means "further away", but units are mixed, so I standardise. Balance and transactions are also right-skewed, and z-scoring equalises spread, not skew, so I'd log those two first, otherwise a few whales redo popularity's trick. ID and postcode go, and I'd never label-encode a category the way the notebook coded genre 0/1/2: that invented ordering moved only 0.1% here, but bites once scaled.

If silhouette, the elbow and seed stability agreed on k=4, I'd expect: digital-first multi-product actives, branch-reliant low-digital users, high-balance single-product holders, and dormant accounts. Four is a guess, not a setting.

The decision it changes: the bank's monthly quota of relationship-manager calls, today ordered by balance. If the high-balance single-product cluster appears, it takes those calls, ranked inside the cluster by distance to its centroid, because any cluster dwarfs the quota.

The feature I'm least sure about is months since last purchase: that's recency, not behaviour, and it could dominate the way popularity did. Would you keep it?
```

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

## ⬜ 4.2 思考與分享(Atomic Discussions 頁內回覆框)

**題目**(raw 行 131–132):思考真實 AI 專案的優勢與劣勢,在下方文字框分享。
可接 raw 行 111–118 的「分析翻譯師」框架。⬜ **待擬答**。

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
