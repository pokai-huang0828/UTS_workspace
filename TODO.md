# TODO — 當前待辦(可覆寫,單一真相來源)

> **這份和 handoff.md 分工**:handoff 是 append-only 的**事實流水帳**(發生過什麼);TODO 是**可覆寫的當前狀態**(還沒做什麼)。
> 做完就從這裡刪掉或打勾,不要留一堆已完成項目。
> 最後更新:**2026-07-25**(建檔;來源 = handoff.md 全檔盤點)

---

## 🔴 硬截止(倒數)

### A2a — 監督式學習 · **2026-07-26 23:59 雪梨**(剩 1 天)
交付物兩個都已完成並過 Codex 三輪稽核(READY),**剩下的全是 Kenny 本人要做的**:

- [ ] 在 Jupyter 開 `Assessment2a/Huang_26254793_421104_Assessment 2a.ipynb`,**Restart & Run All** 跑一次(確認自己環境能重現)
- [ ] 開 `Huang_26254793_421104_Assessment 2a.docx`,確認目錄自動更新、整體觀感
- [ ] 上傳兩檔至 Canvas(檔名已照規定,不要改)

### A2b — 非監督式(K-means)· **2026-08-02**
- [ ] 下載資料集(Canvas `files/12834401`,需登入)
- [ ] 尚未開工。題目與 rubric 已抓齊 → `notes/A2b_題目與rubric.md`
- [ ] ⚠️ 註記:rubric 文件標題寫 420104,但以 Kenny 註冊課號 **421104** 為準(Codex 抓到、已裁決)

### A3 — 10 分鐘影片 pitch + ~10 張投影片 + 5 分鐘 Zoom 答辯 · **2026-08-17**(40%)
- [ ] 下載示例兩份(Canvas `files/12834409`、`files/12834407`,需登入)
- [ ] 尚未開工。題目與 rubric 已抓齊 → `notes/A3_題目與rubric.md`
- [ ] 策略已定:沿用 A1 的 CBA 案例,敘事鏈 A1挑戰 → A2概念驗證 → A3路線圖
- [ ] 照 `.claude/skills/uts-dispatch/SKILL.md` §7.1 的 A3 preflight 逐項過
- [ ] **先做**:錄一段一分鐘試錄檔,讓 agent 跑一次 `/watch` smoke test(確認 yt-dlp / ffmpeg 這台裝得起來,不要等交件前才發現)

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

## 📅 未來要主動提醒的必修投寄

到該週再提:**4.2.1 趨勢分析** → **4.2.4 快速塗鴉** → **5.1.2 Slim Jims**

---

## 🔧 Repo 工程債

- [ ] **repo 體積**:`.git` 959 MB / 工作區 798 MB。2026-07-25 已做 D1 止血(大檔移出追蹤 + .gitignore),但**歷史沒洗,`.git` 不會縮**。要真的瘦身得改寫歷史 + force push + 兩台機器重 clone —— **不可逆,待 Kenny 決定**
- [ ] `BusnessAnalytics` 拼字錯(應為 `BusinessAnalytics`),改名要同步兩台機器
- [ ] `Data Visualisation and Visual Analytics/` 有 `26254793_A2.pdf` 與 `26254793_A2_FINAL_preview.pdf` 並存,確認哪個是定稿
- [ ] `Foundation Studio/Quarterly ... (2).xlsx` 檔名帶 `(2)`,疑重複下載
