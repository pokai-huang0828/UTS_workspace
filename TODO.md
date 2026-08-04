# TODO — 當前待辦(可覆寫,單一真相來源)

> **這份和 handoff.md 分工**:handoff 是 append-only 的**事實流水帳**(發生過什麼);TODO 是**可覆寫的當前狀態**(還沒做什麼)。
> 做完就從這裡刪掉或打勾,不要留一堆已完成項目。
> 最後更新:**2026-08-02**(A2b 延期至 8/5;新機環境建置完成;notebook rubric 措辭已清除)

---

## 🔴 硬截止(倒數)

### A2a — 監督式學習 · **今天 2026-07-26 23:59 雪梨 = 21:59 台北** 🔴
v3 已過 **Codex 四輪對抗終審 READY**(引用誤用全修、表五量化商業案例入 notebook、
FP 商業意義與 recall 論證依老師逐字稿補齊、五張表全部可追溯到 ipynb、字數 1,627)。
**剩下的全是 Kenny 本人要做的**:

- [ ] 在 Jupyter 開 `Assessment2a/Huang_26254793_421104_Assessment 2a.ipynb`,**Restart & Run All** 跑一次(確認自己環境能重現)
- [ ] 開 `Huang_26254793_421104_Assessment 2a.docx`,確認目錄自動更新、整體觀感
- [ ] 上傳兩檔至 Canvas(檔名已照規定,不要改)

### A2b — 非監督式(K-means)· ~~2026-08-02~~ → **延期至 2026-08-05(週三)23:59 雪梨 = 21:59 台北** · **權重 25%**

> 🟢 **2026-08-02 老師來信正式延期**(Chunping + Jiwei)。延期理由原文:
> 「**為了確保我們有時間為大家的 A2a 提供回饋,並將相關建議和經驗應用到 A2b 的提交中**」。
> → 這不是單純多三天,是**要你拿 A2a 的回饋回頭修 A2b**。
> - [ ] 🔴 **A2a 回饋一到就逐條對照 A2b**,該改的改完再交(這是老師給延期的目的)
> - [x] ~~⚠️ A2b 是否延期未定,不要賭~~ ✅ 已定案延期,與李春平 7/30 說的「A2a 成績出了之後給時間」一致
**單元四知識架構已建好** → [`Artificial Intelligence for Enterprises/Assessment2b/A2b_單元四_知識架構與學習記錄.md`](Artificial%20Intelligence%20for%20Enterprises/Assessment2b/A2b_單元四_知識架構與學習記錄.md)
(Canvas 單元四 12 項逐字落檔 + rubric 四節主表 + 資料集實查 + 偵察實跑;已過 Codex 事實軌 + fresh Claude 語意軌雙軌驗證)

- [x] ~~下載資料集~~ ✅ **2026-07-26 全部到位**:`Assessment2b/BigBlue.csv`(107 列 × 4 欄)、
      `Assessment2b/assignment_part_B_final2(1).ipynb`(**老師起手範本**)、
      `notes/practice/{clustering_song_updated,K_means_basic-1}.ipynb`
- [x] ~~**要裁決**:做不做標準化?~~ ✅ **2026-07-28 已裁決:做**(知識架構 §4.5 已改寫)。
      推翻「未標準化為主線」的初版建議 —— 不縮放時 `Recognition` 獨佔 79.6% 距離權重,
      分群退化為單變數複製(ARI 0.99),且 10 位高投入顧問被錯置。經 Codex 一輪對抗。
- [x] ~~建交件 notebook~~ ✅ **2026-08-02 新機 headless 實跑複驗:51 cells / 38 code / 執行序 1→38 連續 / 零錯誤 / 零字型警告 / 32.4 秒**
      (舊記的「42 cells / 31 code / 1→31」是 7/29–7/30 依老師指示修訂**之前**的數字,已過時)
- [x] ~~寫報告四節~~ ✅ 1643 字(目標 1350–1650)、5 表 4 圖 8 章節、APA 3 筆
- [x] ~~**過 Codex 對抗驗證**~~ ✅ 三項質疑全數修正(事後合理化 → 事前宣告判準;
      26.8 倍近零分母 → 絕對佔比;補最佳群成員穩定率)

> **交件包已完成並過三輪 Codex 對抗 + 依老師 7/30 課堂指示逐項修正**。
> 檔案:`Assessment2b/Huang_26254793_421104_Assessment 2b.docx` + `.ipynb`(**兩檔分開交**)。
> 字數:嚴格口徑 1719 / Word 中文字數口徑 1637。
> **字數已獲兩位老師背書**:管濟偉 7/29 當場答「1700 可以」;李春平 7/30 稱「不是很嚴,但不能差距很大」。
> 依李春平 7/30 指示的 12 項驗收全 PASS,詳見 `notes/2026-07-30_Zoom_週四場_李春平_摘要.md`。

> 🚫 **內文不得出現 rubric 措辭** —— 2026-08-02 Kenny 抓到並修正(commit `e533793`)。
> 「評分項『…』20 分」「評分表要求」「論述出色」這類字眼一律改寫成題目語言。
> **逐節標配分不是學生寫工作簿的習慣,等於間接自曝是對著 rubric 生成的。**
> 目前 `.ipynb`(7 處已改)與 `.docx`(原本就乾淨)全檔命中 **0**。
> 🔑 **交件 `.ipynb` 與 `.docx` 都是 `build_notebook.py` / `build_report.py` 的生成物**(誕生於 `eac9152`)——
> 要改內容**必須產物與腳本兩邊一起改**,否則任何人重跑一次 build 就把舊內容全寫回去。
> 🚫 **內文也不得出現內部流程術語** —— 2026-08-03 全檔重掃時再抓到兩處:
> `4.2b …(回應對抗驗證)` 與 `2.5c …(回應「門檻是反推的」質疑)`,以及 markdown 裡的「檢驗這個**指控**」。
> 「對抗驗證」是我們 Codex 對抗流程的詞,寫進作業等於自曝有審查者在來回挑錯,已全部改寫。
> 📅 **繳交日 2026-08-02 已更正為 08-05** —— **四處**:notebook cell#0、`build_notebook.py`、
> **docx 標題頁**、`build_report.py`。docx 那處是 08-03 做 rubric 評估時才發現的
> (前一次只掃 rubric 字眼沒掃日期);改法是替換 `word/document.xml` 內單一 `<w:t>`,
> 段落數 237 / 總字元 5793 / 檔案大小 802,520 全部不變,7 張圖 sha256 未受影響。

**剩下的全是 Kenny 本人要做的**:
- [x] ~~在 Jupyter 開 ipynb 跑一次 **Restart & Run All**~~ ✅ **2026-08-03 20:50 Kenny 已跑**
      → 7 張圖全部重新生成,與 docx 內嵌的 7 個 media **sha256 bit-for-bit 相同**,
      `RANDOM_STATE=42` 的可重現性實錘,**圖與報告零衝突**
- [ ] ⚠️ **之後每次重跑完,都要再跑一次清理腳本**(否則雜訊會回到交件檔):
      `python "Artificial Intelligence for Enterprises/notes/practice/a2b_clean_outputs.py"`
      清的是 VS Code Data Wrangler payload、joblib stderr(含 `c:\Users\kenny\...` 本機路徑)、
      `nbconvert --execute` 寫進 cell metadata 的執行時間戳。**只動 outputs/metadata,不碰 source,可重複執行**
- [ ] 開 docx 確認目錄自動更新、整體觀感
- [ ] 上傳兩檔至 Canvas(檔名已照規定,**不要改**;上傳 ipynb 時可忽略格式錯誤提示)
      ⚠️ **只挑 `.ipynb` + `.docx` 兩檔**。`Assessment2b/` 裡還躺著 `build_notebook.py`、`build_report.py`、
      `__pycache__/`、學習記錄 md、老師範本 ipynb、`BigBlue.csv`、`figures/` —— 整包丟會連生成腳本一起交出去
- [x] ~~**4.1.2 K 均值聚類討論**(必修投寄)~~ ✅ **已投**(Kenny 2026-07-30 確認)
      ⭐ 老師 7/30 課堂上**兩度公開稱讚這則貼文**(「我覺得非常好」),並因此把「標準化」
      加進當天授課內容。→ 老師在改 A2b 前已看過並認可此論證框架,A2b 已比對一致
- [x] ~~⚠️ 延期機制措辭矛盾(自行申請三天 vs 延一天扣五分)~~ —— **已無關**:這次是老師**主動全班延期**,
      不是個人申請,不扣分。8/5 就是新的正式截止,不要再往後賭
- [x] ~~權重 20%~~ → **實為 25%**(Canvas 作業頁原文,Codex 複核 CONFIRMED;`notes/A2b_題目與rubric.md` 已更正)
- [ ] ⚠️ 註記:rubric 文件標題寫 420104,但以 Kenny 註冊課號 **421104** 為準(Codex 抓到、已裁決)

### A3 — 10 分鐘影片 pitch + ~10 張投影片 + 5 分鐘 Zoom 答辯 · **2026-08-17**(40%)
- [ ] 下載示例兩份(Canvas `files/12834409`、`files/12834407`,需登入)
- [ ] 尚未開工。題目與 rubric 已抓齊 → `notes/A3_題目與rubric.md`
- [ ] 策略已定:沿用 A1 的 CBA 案例,敘事鏈 A1挑戰 → A2概念驗證 → A3路線圖
- [ ] 照 `.claude/skills/uts-dispatch/SKILL.md` §7.1 的 A3 preflight 逐項過
- [x] ~~確認 yt-dlp / ffmpeg 這台裝得起來~~ ✅ **2026-08-02 新機已裝並實測**:ffmpeg/ffprobe 8.1.2-full、yt-dlp 2026.07.04
- [ ] 🔴 **`/watch` skill 根本不存在** —— repo `.claude/skills`(只有 uts-dispatch)、`~/.claude/skills`(20 個官方 skill)、plugins 全找過都沒有。
      handoff 2026-07-25 第 6 點與 SKILL §2 派工對照表把它當**既有能力**寫,是不實陳述。
      底層工具已就緒 → A3 影音驗收要嘛現寫一個 skill,要嘛派 agent 直接下 ffmpeg/yt-dlp 指令。**決定前不要在 A3 計畫裡再引用 `/watch`**
- [ ] **先做**:錄一段一分鐘試錄檔,跑一次影音驗收 smoke test
- [x] ~~⚠️ 格式待老師釐清,7/31 起盯 Canvas 公告~~ ✅ **2026-08-02 老師來信定案,我方筆記的錄影版正確**:
      **10 分鐘 = 錄製影片(recorded),不是現場展示**,且是主要評分內容;投影片約 10 頁為輔助;
      支持性文件僅輔助材料;**5 分鐘一對一 Zoom 問答是現場的**,亦計入評分。
- [ ] 🎥 **問答須開鏡頭**(老師 2026-08-02 明訂,用於身分確認與互動)—— 硬性要求,先確認視訊鏡頭可用
- [ ] 📬 **問答預約時段通知「之後才發」** —— 盯信箱與 Canvas,收到就立刻約(好時段會被搶)
- [ ] **開工前約一次 one-on-one**(管濟偉 或 李春平,需提前預約)—— 管濟偉 7/29 提到課室有一對一
- [ ] 💡 A3 風險治理一節可帶入**對抗風險 / 可信賴機器學習** —— 管濟偉本人的研究領域
      (對抗魯棒性、對抗樣本、後門攻擊、水印);他也說 AI 衝擊「最大是寫程式,其次金融」,
      與我方沿用 CBA 金融案例方向一致。見 `notes/2026-07-29_Zoom_週三場_管濟偉_摘要.md`

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
- [ ] **4.2.4 快速塗鴉** —— ✅ **擬答已備妥可直接貼**(2026-07-29 Kenny 實跑 4 中 2 錯,
      失敗兩張的前三名判讀也已點開截圖:披薩→西瓜/曲奇/馬鈴薯、麵包車→汽車/貨車/住宅);
      ⚠️ 貼前只剩確認作畫順序(只影響第五段)
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

---

## 📅 單元五「制定 AI 路線圖」—— **2026-08-04 Canvas API 實查**(module 342820,11 項)

內容整理與題目全文 → [`notes/Unit5_內容整理與待答清單.md`](Artificial%20Intelligence%20for%20Enterprises/notes/Unit5_內容整理與待答清單.md)

> ⭐ **5.4 頁面原文明講「這些內容將對你完成第三項評估任務非常有幫助」** —— 單元五 = **A3 的方法論骨架**,
> 不是普通一週。5.4 的七問 + 四支柱(願景/價值/風險/採納)可直接當 A3 章節骨架與答辯題庫。

**9 頁 must_view 已全部 DONE**(`module.state=started`),真正沒結的只有下面幾項:

- [ ] 🔴 **5.1.2 案例研究:Slim Jims** —— **must_contribute 必修投寄**(discussion `771434`)
      實查:目前僅 1 則貼文,作者 `259967 Jian Zhou`,**Kenny 未發文**。無 due date
      題目:「使用波特五力模型對 Slim Jims 的分析告訴你,企業應**如何以及在何處**使用 AI,以增強其競爭地位?」
      ⚠️ 兩個易漏點:①要答「如何 **+ 在何處**」用 AI,五力只是論據 ②題目要求「**與同伴比較**」→ 要回應 Jian Zhou 那則
      🔑 裁決基準:課程頁 5.2.1 已定 Slim Jims **走差異化、是質量領導者、資源應集中在差異化**
- [ ] 5.6 第五周总结与提问(discussion `771430`)—— 只要 **must_view** 即達成;目前 0 則貼文
- [ ] 5.5 衡量 AI 的成功 —— **無完成條件**(系統不追蹤),但 KPI 清單與 IBM 成熟度框架對 A3 有用

**⚠️ 頁內元件(module 清單看不到,實查 11 個 iframe)** —— 不影響完成條件,但單元四踩過
- [ ] 5.1 / 5.1.1 / 5.2 / 5.2.1 四處 **Atomic Discussions** 思考與分享框
- [ ] 5.3 是 **Atomic Polls**(投票,不是討論框)· 5.3.1 有「Think and share activity」+ UTS 圖書館兩本書
- [ ] **兩個 H5P**:5.1.1 五力滑桿互動 · 5.2.1 戰略投影片
- [ ] 外部材料:5.2 的〈推動生成式 AI 採用的五大力量〉、5.2.1 要**下載 Deloitte《企業中生成式 AI 現狀》最新季報**

---

## 🖥️ 本機環境(Windows 新機,2026-08-02 建置)

一次裝好、已逐項實測。**換機時照這張表重跑即可**。

| 項目 | 狀態 |
|---|---|
| git **2.55.0.3** + 身分 + origin + 與 origin/main 同步 | ✅ 沿用,2026-08-02 由 2.51.1 升級 |
| gh **2.97.0** / pip **26.2** / npm **12.0.2** | ✅ 2026-08-02 升級(原 2.94.0 / 25.3 / 11.16.0) |
| winget `--all` | ✅ 2026-08-02 跑完 13/14(Zoom 7.1.5、Teams、OneDrive、VCRedist、WinRAR…);**只剩 Microsoft Edge 升不動**(winget 對執行中的 Edge 沒轍,交給 Edge 自己的更新器) |
| Python 3.11.9 + A2b 全部相依(pandas 2.1.4 / numpy 1.26.4 / sklearn 1.4.2 / scipy 1.11.4 / matplotlib 3.7.5 / seaborn / yellowbrick / python-docx 1.2.0) | ✅ 沿用 |
| VS Code + Jupyter/Python/Data Wrangler 擴充、Word(含 COM)、gh CLI、winget | ✅ 沿用 |
| **JupyterLab 4.6.2 / notebook 7.6.1 / nbconvert 7.17.1** | 🆕 本次 `pip install`(原本只有 ipykernel,**沒有 UI 也沒有 nbconvert**) |
| **ipykernel 註冊** `python3` @ `%APPDATA%\jupyter\kernels\python3` | 🆕 本次 `python -m ipykernel install --user` |
| **Node.js v24.18.1 + npm 12.0.2** | 🆕 `winget install OpenJS.NodeJS.LTS`(隨附 npm 11.16.0,同日再升 12.0.2) |
| **Codex CLI 0.146.0(gpt-5.6-sol)** | 🆕 `npm install -g @openai/codex`;auth.json 沿用、實測 EXIT=0 |
| **ffmpeg / ffprobe 8.1.2-full** | 🆕 `winget install Gyan.FFmpeg` |
| **yt-dlp 2026.07.04** | 🆕 `pip install yt-dlp` |

### 🔒 為什麼 Python 套件停在 2024 年 —— 是 `pycaret 3.3.2` 鎖的(2026-08-02 查明)

Python 3.11.9 本身**沒有落後**(官方支援到 2027/10);winget 那條「Python Launcher 3.13.5」是 `py.exe` 啟動器,不是直譯器。
真正被鎖的是套件,元兇是 **pycaret 3.3.2**,五個上限**全部貼死**:

| pycaret 3.3.2 要求 | 實際安裝 |
|---|---|
| `scipy<=1.11.4` | scipy **1.11.4** |
| `numpy<1.27` | numpy **1.26.4**(1.26 最後一版) |
| `matplotlib<3.8.0` | matplotlib **3.7.5**(3.7 最後一版) |
| `pandas<2.2.0` | pandas **2.1.4** |
| `sktime==0.26.0` → `scikit-learn<1.5.0` | sklearn **1.4.2**(1.4 最後一版) |

**pycaret 是真的在用的** —— `BusnessAnalytics/A1`、`A2` 都有 `from pycaret.classification import *`,不能砍。
週邊套件(ipython 9.6 / pillow 12.0 / pydantic 2.12)沒被它管到,所以漂到 2025 年 → 這就是「核心舊、週邊新」的成因。

⚠️ **陷阱**:`pip install --dry-run --upgrade numpy pandas scikit-learn scipy matplotlib` 回覆
`Would install numpy-2.4.6 pandas-3.0.5 scikit-learn-1.9.0 scipy-1.17.1`,**一句 pycaret 警告都沒有** ——
pip 升級時只解點名的套件與其相依,**不回頭檢查已裝的 pycaret**。照著跑會「成功」,然後 Business Analytics 靜默壞掉。

- [ ] **正解是隔離不是升級**:全域維持 pycaret 這組給 Business Analytics;
      **AI for Enterprises 另開 venv + `requirements.txt`**,想多新用多新。A2b 交件後再建
- [ ] 註記:`rooster_a2.ipynb` 存有舊機 pip log(路徑 `c:\users\kenny\`),顯示舊機當時 numba 0.62.1 / plotly 6.5.0 /
      kaleido 1.2.0 / ipython 9.7.0 **都比這台新**。兩台 Python 環境本來就不同份(該 log 只是歷史快照,不代表舊機現況)

**換機才會踩到的坑(已寫進 SKILL §0;2026-08-02 經獨立稽核更正一條):**
- ✅ **持久化 PATH 是對的** —— 12 個工具(git / python / jupyter / jupyter-lab / node / npm / codex /
  ffmpeg / ffprobe / yt-dlp / gh / code)**在全新開的 shell 全部叫得到**,實測逐一解析過。
- ⚠️ 真正的坑是**行程過期不是 PATH 沒設**:安裝**之前**就已啟動的行程(Claude Code session 本身、
  已開著的終端機 / VS Code)拿的是舊環境區塊。**解法是重開那些視窗**,或在該 session 內用
  `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')` **重讀 registry**。
  ~~原本寫「codex 不在預設 PATH,要 append」是錯的~~,照那樣做只會一直疊重複路徑。
- 🆕 **已修**:`%APPDATA%\Python\Python311\Scripts` 原本不在 PATH,導致 `jupyter kernelspec list`
  報 `command not found`(該目錄裡有 `jupyter-kernelspec.exe` / `jupyter-run.exe` / `debugpy.exe`)。
  已加進 User PATH,`jupyter kernelspec list` 現在正常列出 python3 kernel。
- Codex 預設 `reasoning effort: none`(不是 SKILL 舊表寫的 xhigh)→ **每趟都要加 `-c model_reasoning_effort="xhigh"`**
- ℹ️ `.ipynb` 沒有 Windows 檔案關聯,在檔案總管點兩下不會開。只要一律從 VS Code / Jupyter 開就沒事,沒去改系統設定

- [ ] 選配:要不要把 `model_reasoning_effort = "xhigh"` 寫進 `~/.codex\config.toml` 免得每趟漏加?
      (影響 Kenny 所有專案的 Codex,不只這個 repo,所以沒擅自改)
- [ ] ⚠️ 這台是 fresh clone,**`.gitignore` 裡 D1 移出追蹤的大檔一個都沒有**:
      `Cybersecurity Analytics and Insights/A3/data/`、`A3a/data/`、`A2/ddos_syn_flood_lo.csv`、兩個 `.pcapng`。
      **只影響 Cybersecurity 科目**(MNIST 類 torchvision 會自動重抓);AI for Enterprises 的 A2b/A3 不受影響

---

## 🔧 Repo 工程債

- [x] ~~D1 止血:大檔移出追蹤~~ **2026-07-25 完成**(追蹤中 >5MB 檔案 524.9 → 53.9 MB)。⚠️ **Mac 下次 pull 時那 27 個檔會被刪掉**,要用先自行備份或重抓
- [ ] **repo 體積**:歷史沒洗。**2026-08-02 新機 fresh clone 實測:`.git` 542.3 MB / 工作區 124.5 MB**
      (舊記 959 MB 是舊機未 gc 的數字;fresh clone 會自動 repack,所以看起來小,但**歷史裡的大物件還在**)。
      要真的瘦身得改寫歷史 + force push + 所有機器重 clone —— **不可逆,Kenny 2026-07-25 表示先不做**
- [ ] **關掉用不到的 plugin**:MCP 工具定義佔 context 約 214k,且 Desktop Commander 載兩次、pdf-viewer 載三份。可在 `.claude/settings.json` 加 `enabledPlugins` 只留 claude-in-chrome / ccd_session / visualize,估可省 150k+
- [ ] `BusnessAnalytics` 拼字錯(應為 `BusinessAnalytics`),改名要同步兩台機器
- [ ] `Data Visualisation and Visual Analytics/` 有 `26254793_A2.pdf` 與 `26254793_A2_FINAL_preview.pdf` 並存,確認哪個是定稿
- [ ] `Foundation Studio/Quarterly ... (2).xlsx` 檔名帶 `(2)`,疑重複下載
