# TODO — 當前待辦(可覆寫,單一真相來源)

> **這份和 handoff.md 分工**:handoff 是 append-only 的**事實流水帳**(發生過什麼);TODO 是**可覆寫的當前狀態**(還沒做什麼)。
> 做完就從這裡刪掉或打勾,不要留一堆已完成項目。
> 最後更新:**2026-07-26**(A2a 過 Codex 終審 READY;repo D1 已完成)

---

## 🔴 硬截止(倒數)

### A2a — 監督式學習 · **今天 2026-07-26 23:59 雪梨 = 21:59 台北** 🔴
v3 已過 **Codex 四輪對抗終審 READY**(引用誤用全修、表五量化商業案例入 notebook、
FP 商業意義與 recall 論證依老師逐字稿補齊、五張表全部可追溯到 ipynb、字數 1,627)。
**剩下的全是 Kenny 本人要做的**:

- [ ] 在 Jupyter 開 `Assessment2a/Huang_26254793_421104_Assessment 2a.ipynb`,**Restart & Run All** 跑一次(確認自己環境能重現)
- [ ] 開 `Huang_26254793_421104_Assessment 2a.docx`,確認目錄自動更新、整體觀感
- [ ] 上傳兩檔至 Canvas(檔名已照規定,不要改)

### A2b — 非監督式(K-means)· **2026-08-02** · **權重 25%**(不是 20%,見下)
**單元四知識架構已建好** → [`Artificial Intelligence for Enterprises/Assessment2b/A2b_單元四_知識架構與學習記錄.md`](Artificial%20Intelligence%20for%20Enterprises/Assessment2b/A2b_單元四_知識架構與學習記錄.md)
(Canvas 單元四 12 項逐字落檔 + rubric 四節主表 + 資料集實查 + 偵察實跑;已過 Codex 事實軌 + fresh Claude 語意軌雙軌驗證)

- [x] ~~下載資料集~~ ✅ **2026-07-26 全部到位**:`Assessment2b/BigBlue.csv`(107 列 × 4 欄)、
      `Assessment2b/assignment_part_B_final2(1).ipynb`(**老師起手範本**)、
      `notes/practice/{clustering_song_updated,K_means_basic-1}.ipynb`
- [ ] **先跑 4.1.2 討論的 `clustering_song`**(必修投寄 + A2b 預演,見知識架構 §6)
- [ ] 建交件 notebook:排除 `EmployeeID` → silhouette 掃 k=2..9 → elbow → 質心表(照老師範本骨架 + 補 `random_state`、肘部法)
- [ ] **要裁決**:做不做標準化?老師範本**沒做**、示範 k=4;建議兩種都跑、未標準化為主線(知識架構 §4.5)
- [ ] 寫報告四節(章節骨架與 `build_report.py` 從 A2a 移植)
- [x] ~~權重 20%~~ → **實為 25%**(Canvas 作業頁原文,Codex 複核 CONFIRMED;`notes/A2b_題目與rubric.md` 已更正)
- [ ] ⚠️ 註記:rubric 文件標題寫 420104,但以 Kenny 註冊課號 **421104** 為準(Codex 抓到、已裁決)

### A3 — 10 分鐘影片 pitch + ~10 張投影片 + 5 分鐘 Zoom 答辯 · **2026-08-17**(40%)
- [ ] 下載示例兩份(Canvas `files/12834409`、`files/12834407`,需登入)
- [ ] 尚未開工。題目與 rubric 已抓齊 → `notes/A3_題目與rubric.md`
- [ ] 策略已定:沿用 A1 的 CBA 案例,敘事鏈 A1挑戰 → A2概念驗證 → A3路線圖
- [ ] 照 `.claude/skills/uts-dispatch/SKILL.md` §7.1 的 A3 preflight 逐項過
- [ ] **先做**:錄一段一分鐘試錄檔,讓 agent 跑一次 `/watch` smoke test(確認 yt-dlp / ffmpeg 這台裝得起來,不要等交件前才發現)
- [ ] ⚠️ **格式待老師釐清**:李春平(7/23)以為是「15 分鐘全線上 = 10 分鐘簡報 + 5 分鐘問答」,學生王崇說是「錄 10 分鐘影片提交 + 線上 5 分鐘問答」。**她說會確認後公告** → 看 Canvas 公告再定。我方 `notes/A3_題目與rubric.md` 目前記的是錄影版

---

## 🟡 待貼 Canvas(擬答都備好了,Kenny 自己貼)

擬答全在 `Artificial Intelligence for Enterprises/notes/Unit2-3_內嵌練習擬答.md`。

- [ ] Unit 2 五題內嵌練習(§1–6)—— 含 2.1 小測三題答案
  - [ ] ⚠️ 其中 **2.2.2 討論區那題老師點名要附箱型圖截圖**,Kenny 要自己在 Jupyter 跑一次(code 與預期輸出在擬答檔裡;跑出來應是:箱 20.5–35、中位線 25、鬚 13–52、70 為異常值圓圈)
- [ ] 3.2.1 決策樹 · 評論框(§7)
- [ ] 3.2.4 混淆矩陣 · 討論區 **必修投寄**(§9 v2 + 「Decision tree」藍圖)
- [ ] 3.3.1 理解文本 · 討論區 **必修投寄**(§10)

> 上次卡住原因:Canvas SSO 登入態過期,憑證只有 Kenny 有,agent 不代填。

---

## 🟢 課程進度 / 外部工具

- [ ] Kenny 續讀 Canvas:3.2.3(SVM)→ 3.2.5(真實資料)→ 3.3.x
- [ ] Google Doc「單元三概述」更新(自報進度到 3.2.1)
- [ ] NotebookLM:補傳 `notes/transcripts/` 兩份 Zoom 逐字稿;刪掉一個「Just a moment...」壞來源

---

## ⚪ Kenny 已決定不做 — **不要催**

Unit 1 三項缺漏,Kenny 2026-07-10 明示「那些不用」:
- 「認識你的同學」必修投寄(草稿在,只差興趣愛好一句)
- 1.5 未發問(問題已擬好)
- 1.1.2 的「回覆兩位同學」寫在自己主貼內,未補成 threaded

> 只有 Kenny 主動提起才處理。

---

## 📅 單元四待作答 —— 共 **12 個**(2026-07-26 實查,含瀏覽器挖出的頁內元件)

擬答與題目全在 [`Artificial Intelligence for Enterprises/notes/Unit4_內嵌練習擬答.md`](Artificial%20Intelligence%20for%20Enterprises/notes/Unit4_內嵌練習擬答.md)。

**Canvas 討論(必修投寄,modules 頁列完成條件)**
- [ ] **4.1.2 K 均值聚類** —— ✅ **擬答已備妥可直接貼**(前置 notebook 已跑完,27 cells 零錯誤 + 7 圖)
- [ ] **4.2.1 趨勢分析工具** —— ✅ **主文擬答已備妥**;⚠️ 第 3 點「評論一位同學」仍要 Kenny 自己做
- [ ] **4.2.4 快速塗鴉** —— ⚠️ 要 Kenny 本人玩 6 次並記錄成敗,agent 產不出
- [ ] 4.3 第四週總結與問題 —— 提問/回覆同學

**⚠️ 頁內作答元件(純文字抓取看不到,2026-07-26 瀏覽器實查才發現,四個框全空)**
- [ ] **4.1 H5P 問答**「聚类也有助于异常值检测。你能想到一个例子吗?」有作答框 + 提交鈕
- [ ] **4.2 思考與分享**(Atomic Discussions 回覆框)—— ✅ **擬答已備妥可直接貼**
- [ ] **4.2.2 思考與分享**(Atomic Discussions 回覆框,兩問)
- [ ] **4.2.3 快速任務**(Atomic Discussions 回覆框)⚠️ 要先真的訓練一個 Teachable Machine 模型

**要動手但不用投寄**
- [ ] 4.1.1 `K_means_basic` 活動(含 Task 1 / Task 2 兩個留白格)
- [ ] 4.2.2 操作 Microsoft LUIS 演示 · 4.2.3 訓練 Teachable Machine · 4.2.5 試用 ModelScope
- [ ] **4.2.5 圖像生成頁面未查看**(單元四唯一未讀頁)

到該週再提:**5.1.2 Slim Jims**

---

## 🔧 Repo 工程債

- [x] ~~D1 止血:大檔移出追蹤~~ **2026-07-25 完成**(追蹤中 >5MB 檔案 524.9 → 53.9 MB)。⚠️ **Mac 下次 pull 時那 27 個檔會被刪掉**,要用先自行備份或重抓
- [ ] **repo 體積**:`.git` 仍 959 MB(**歷史沒洗**)。要真的瘦身得改寫歷史 + force push + 兩台機器重 clone —— **不可逆,Kenny 2026-07-25 表示先不做**
- [ ] **關掉用不到的 plugin**:MCP 工具定義佔 context 約 214k,且 Desktop Commander 載兩次、pdf-viewer 載三份。可在 `.claude/settings.json` 加 `enabledPlugins` 只留 claude-in-chrome / ccd_session / visualize,估可省 150k+
- [ ] `BusnessAnalytics` 拼字錯(應為 `BusinessAnalytics`),改名要同步兩台機器
- [ ] `Data Visualisation and Visual Analytics/` 有 `26254793_A2.pdf` 與 `26254793_A2_FINAL_preview.pdf` 並存,確認哪個是定稿
- [ ] `Foundation Studio/Quarterly ... (2).xlsx` 檔名帶 `(2)`,疑重複下載
