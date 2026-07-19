# handoff — session 交接(append-only;新 session 只讀最後一個 entry)

---

## 2026-07-16 · fable skill 移植 + Codex 升級(本 entry 同時總結 7/06–7/16 的課程作業脈絡)

### 一、這台環境現在的樣子(實查過,可直接信)

| 項目 | 狀態 |
|------|------|
| 治理框架 | `.claude/skills/frugal-fable/`(`/frugal-fable` 可載入;2026-07-16 自 fable 改名)= VMX 移植的指揮官手冊 + Agent×Codex 兩腦驗證架構;根目錄 CLAUDE.md 已路由 |
| Codex CLI | **0.144.5,model `gpt-5.6-sol`,effort xhigh**(config `~/.codex/config.toml`,備份 `.bak.2026-07-16`)。smoke test EXIT=0(2026-07-16) |
| Codex 陷阱 | 裸名 `gpt-5.6` 在 ChatGPT 帳號下 400;5.6 系列 = `-sol`(旗艦)/`-terra`/`-luna`。駕駛配方(PowerShell tool + stdin + `-o` 落檔 + read-only)見 `.claude/skills/frugal-fable/references/codex-collab.md` |
| git | main = `6978470`,全部已 push(github.com/pokai-huang0828/UTS_workspace);Kenny 靠 push main 跨裝置追蹤,**成果完成就 commit+push** |
| Kenny 偏好 | 回覆一律繁體中文(memory 已存);交付要附證據(R-完成);發文/送出類動作 Kenny 自己做,agent 只備好內容 |

### 二、課程現況(421104 企業 AI,Session 4 2026)

- **A1(15%,7/12 截止)**:CBA 案例報告已定稿於 `Artificial Intelligence for Enterprises/Assessment1/Huang_26254793_421104_Assessment1.docx`(+PDF)。730 中文字/863 Word 計法、APA 7、目錄已更新、對齊五項 rubric「優異」要件、數字全數對過公開來源。7/11 已備妥交件;⚠️假設:Kenny 已於期限內上傳,未向我確認過。
- **接下來的截止日**:A2a **7/26**(監督式學習 coding,資料集課程提供)→ A2b **8/2**(非監督)→ A3 **8/17**(AI 路線圖)。
- **A3 重要策略**:與 A1 用**同一案例(CBA)**;A1 的三軸框架(效率/速度/風險)、IBISWorld K6221A 與 CBA FY25 數據(存於 `Foundation Studio/CBA_Report/data/`)可直接沿用擴寫。
- **Unit 1 參與狀態**(7/10 用 Chrome 逐頁實查):所有內嵌思考練習已發 ✅(1.1/1.1.1/1.1.3/1.1.4/1.2/1.3/1.3.1/1.3.2)、1.1.2 與 1.4 討論區主貼已發 ✅。**缺**:①「認識你的同學」= 必修投寄,未發(草稿已擬,只差 Kenny 填興趣愛好);②1.5 未發問(問題已擬好);③1.1.2 的「回覆兩位同學」寫在自己主貼內,建議補成真正的 threaded 回覆。三者內容都在 7/10 前後的 session 訊息裡,Kenny 說「那些不用」= 他自己決定要不要貼,**不要催**。
- **之後的必修投寄討論**(到該週要主動提醒):3.2.4 混淆矩陣、3.3.1 理解文本、4.2.1 趨勢分析、4.2.4 快速塗鴉、5.1.2 Slim Jims。
- **Zoom**:每週兩場同內容(李春平/管濟偉),北京時間 19:00;週五場擬改週三,**以 Canvas 公告為準**(行事曆不可靠)。老師明示:格式錯扣分、用 Word 不用 WPS、多用 UTS Library、遲交寬限 3 個自然日。

### 三、待辦(下個 session 的合理起點)

1. **A2a(7/26)是下一個硬截止**:先去 Canvas 讀題目與資料集、看 A3 示例一/二,規劃 Python(監督式學習)作業;Kenny 是 coder,重點在符合 rubric 與概念正確。
2. Unit 2(資料/統計/視覺化)的內嵌練習與 2.2.2、2.7 討論——照 Unit 1 模式協助擬答。
3. 若 Kenny 提「認識你的同學」:草稿在,只差興趣愛好一句。
4. fable skill 尚未在實戰任務中全流程走過(派工→Codex 複核)——A2a 是好機會(程式產出 → Codex read-only 驗證)。

### 四、本 session 教訓(值得延續的做法)

- 型號/工具報錯 → 照 R-漂移:實查(撈 CLI 二進位的型號表:`grep -oaE "gpt-5[a-z0-9.\-]*" codex.exe | sort -u`)、更新實查表、附日期,不瞎猜重試。
- Canvas 內嵌練習(Atomic Discussions iframe)get_page_text 讀不到,要**截圖**;頁面有影片時截圖會 timeout,等 6–8 秒重試或開新分頁。
- Canvas 模組頁(/modules)會顯示每項「已查看/投寄」完成狀態,是盤點參與度的最快入口。

---

## 2026-07-16(晚)· Zoom 答疑分析 + A1 模板核對

- **交付**:`Artificial Intelligence for Enterprises/notes/2026-07-15_Zoom_QA_摘要與模板核對.md`(週三 Zoom 逐字稿重點 + A1 vs UTS HELPS 官方模板逐項比對)。
- **核對結論**:A1 短報告規格合格(封面/真TOC/引言/編號表格/APA 7/引註 9 項全過);對照 HELPS 完整商業報告缺 Exec Summary、獨立結論、獨立建議 3 項 —— A1 已交不動,**列為 A3 長報告必備**。
- **A2 關鍵情報**(出自老師口述):feature selection 是作業二評分點;2a/2b 資料集乾淨、直接選監督/非監督不用先聚類;自選資料集去 Kaggle、要小而可控可解釋(⚠️任務編號待 Canvas 確認);疑有 presentation 成分;不需 GPU。
- **行政**:週五場改週三(以 Canvas 公告為準);春平老師場 = 週四同時段;老師會把 ML 基礎網站(對 A2 有幫助)+ LLM 安全兩連結貼 announcement,值得去撈。
- 驗證方式:模板 = WebFetch 兩次獨立實抓 HELPS 頁 + 逐字讀 2 份批註範例;A1 = python-docx 實抽(docProps Words=1,601、正文約 960–1,170 依含不含表格)。

---

## 2026-07-16(深夜)· A1 數據來源三路查核

- Kenny 問「A1 數字都有來源不是猜想吧」→ 實查結論:**33 個量化陳述無一杜撰**(逐句盤點 + 9 條抽查全數找到真實出處),但文件內 6 個數字漏掛引註、表二無表下來源註、2 處引註配對有瑕疵(1,700萬客戶掛 IBISWorld 查無支持,實為 CBA 官方口徑 15.9M–18M;「<10 分鐘核准」官方原文是中小企業貸款非房貸)。
- 完整查核表 + A3 沿用數據時的必改清單:見 notes/2026-07-15 檔 §六。A1 已交,不動;若老師追問出處,答案都備妥在該檔。

---

## 2026-07-19 · Unit 2–3 內嵌練習擬答備妥,待貼 Canvas(跨機器接手點)

### 現況一句話
五題內嵌練習擬答**全部完成並落檔**,但**尚未貼進 Canvas**——Kenny 開 remote-control 要 agent 代填時,Canvas SSO 登入態已過期,卡在 UTS 登入頁(憑證要 Kenny 本人輸入,agent 不代填)。

### 接手材料
- **全部擬答(可直接貼)**:`Artificial Intelligence for Enterprises/notes/Unit2-3_內嵌練習擬答.md`,含六項進度清單(哪頁、哪個 URL、貼了沒)、2.1 小測三題答案、五題貼文全文。
- 2.2.2 討論區那題**必附 Kenny 自己在 Anaconda/Jupyter 跑的箱型圖截圖**(老師點名);code 與預期輸出都在擬答檔裡,跑出來的圖:箱 20.5–35、中位線 25、鬚 13–52、70 = 異常值圓圈。
- 操作注意:Canvas 內嵌練習(Atomic iframe)get_page_text 讀不到,要用**截圖**定位輸入框;貼文語氣已按 Kenny 要求調過(自然但不過度口語,無語助詞)。

### 本 session 其他成果(已 commit)
- 2026-07-15 Zoom 答疑(管濟偉)分析 + A1 vs UTS HELPS 模板核對 → notes/2026-07-15 檔 §一–五。
- A1 數據來源三路查核:33 個量化陳述無一杜撰,6 個漏掛引註、表二無來源註、2 處引註配對瑕疵 → 同檔 §六(A3 沿用數據時必改清單)。

### 待辦
1. Kenny 登入 Canvas → 把五題擬答貼上(自己貼或叫 agent 用 remote-control 代填皆可)。
2. 2.2.2 的 Jupyter 截圖要 Kenny 自己跑一次。
3. **A2a(7/26)仍是下一個硬截止**:去 Canvas 讀題目與資料集;Zoom 情報:feature selection 是評分點、資料集乾淨不用先聚類、自選資料集去 Kaggle 挑小而可控的。

## 2026-07-19(午)· 7/16 週四場 Zoom(李春平)逐字稿分析落檔

### 交付(已驗證)
- **逐字稿原檔**:`Artificial Intelligence for Enterprises/notes/transcripts/2026-07-16_Zoom_週四場_李春平_逐字稿.md`(語音+聊天室逐字保存;Kenny 可整檔上傳 NotebookLM 作 source)。
- **課程情報摘要**:`notes/2026-07-16_Zoom_週四場_李春平_摘要.md`(§一–§五 可直接貼 Google Doc)。重點:A1 評分目標 7/20–21 批完;APA 7 只看引用格式(文內=作者+年份、reference list 懸掛縮排),排版不看;Kenny 問 docx 獲答「Word 可以」;**A2a 滿分寫法 = feature importance 三層論證(模型輸出→案例解釋→外部佐證)**;feature importance≠因果;交跑完帶 output 的 .ipynb(Colab 可);churn 案例鎖定 false negative + 量化商業價值;週四場 19:30、8/6 那週可能改時間;企業落地素材(安全/治理/澳洲保守環境)可進 A3 風險章節。
- **驗證(R-完成)**:雙線——fresh sonnet agent 全量核對(抓 5 處輕度過度推論,已逐條修正:Unit 3 標記為推斷、interval/ratio 註明課上未展開、A2 獨立性歸屬 Tao Wang、刪 sklearn 具體化、docx/PDF 留分寸)+ Codex gpt-5.6-sol read-only 抽查 3 條時間/格式類 claims 全數支持。
- 環境註記:**這台 Mac 的 codex-cli = 0.144.6**,`codex exec --sandbox read-only` 直接可用(SKILL §0 實查表是 Win 機 0.144.5,配方通用)。

### 待辦(不變+新增)
1. **A2a(7/26)硬截止**:去 Canvas 讀題目+rubric 逐條對照「優異」欄;notebook 按摘要 §三寫。
2. 週一(7/20)看 Canvas 公告:A1 成績可能發布、老師答應的 ML 基礎網站連結。
3. Kenny 自報進度:Canvas 讀到 3.2.1,續讀後自己更新 Google Doc + NotebookLM(agent 只備內容,不代登)。
4. 前一 entry 的五題內嵌練習擬答仍待貼 Canvas(SSO 要 Kenny 登入)。

## 2026-07-19(午後)· 三個外部來源實查補課

Kenny 問「其他資料來源有一起看嗎」→ 誠實回答:先前只分析逐字稿本文。隨即用本機 Chrome(Kenny 登入態)三個都實開:
- **Google Doc「单元三 | 概述」**:Kenny 的 Unit 3 筆記,大綱到 3.2.1 決策樹,與自報進度一致。
- **Canvas modules**:登入態有效、整頁可讀。證實 Unit 3 = 機器學習實操第一部分(3.1 思維/監督/k-NN/評估、3.2 分類實操含 SVM、3.3 理解文本),A2a 掛 Unit 3 末;**Unit 3 週兩個必修投寄 = 3.2.4 混淆矩陣 + 3.3.1 理解文本練習**。已回寫進 7/16 摘要(⚠️推斷解除)。
- **NotebookLM**:11 來源(7/03 建),缺單元三筆記與兩份 Zoom 逐字稿;有一個「Just a moment...」疑似壞來源可刪。建議 Kenny 補傳 `notes/transcripts/` 兩份逐字稿。

## 2026-07-19(晚)· Unit 3.2 實作三頁分析 + notebook + 3.2.4 必修投寄定稿

### 本段成果(全部已 commit+push,最新 `2c6dc48`)
- **3.2.1 決策樹**:實跑抓到頁面筆誤((0.6,0.75) 實為 1 非 0);Q2 評論框擬答 + 四個實驗(補象限 1a/1b、閾值漂移、XOR、雜訊+max_depth)入擬答檔 §7,含用字修正(原規則未定義左上象限)。
- **3.2.2 最近鄰**:頁面三處不一致(NearestCentroid 非 k-NN、代碼 [0.6,0.1]×2 vs 表格 (0.6,1)、兩半範例各對應不同資料);無需貼文,筆記入 §8。
- **3.2.4 混淆矩陣(必修投寄)**:定稿 v2 在 §9——第 1 點答本頁示範 SVM(0.2857/0.2857/0.4444、[[0 5],[0 2]]),第 2 點答決策樹([[5 0],[0 2]]、全 1.0),附「Decision tree」藍圖。**Kenny 尚未貼**。同儕 Chong Wang 的 [[3 0],[0 2]] = 只用前 5 測試點(Codex gpt-5.6-sol 獨立驗算確認我方 7 點版正確);Kenny 決定不回覆他。題目本身有缺陷(第 1 點未指明分類器、「上一节…决策树」矛盾)→ v2 兩種讀法都覆蓋。
- **practice/ 資料夾**新建:`practice/Unit3_2_實作練習.ipynb`(22 格,headless 驗證零錯誤;Kenny 已在 VS Code 跑過,輸出已入 repo)。
- **Mac 環境**:repo 根目錄 `.venv`(sklearn 1.9.0 + matplotlib 3.11.1 + ipykernel,kernel 名「Python (UTS AI)」,已加 .gitignore)。這台 Mac 無 Anaconda(在 Win 機),之後課程 Python 都用此 venv。scratchpad 另有驗證用 skv venv(session 結束即失效,不可依賴)。

### 教訓
- Canvas wiki 頁摺疊步驟(步骤一/二/三):主文件用 JS 過濾 `textContent==步骤X` 可抽;討論區(React)則走 **Canvas API** `/api/v1/courses/42198/discussion_topics/<id>` 拿 message HTML,再抽 `<pre>/<code>`。
- 課程頁面代碼/表格/示範輸出**經常互相不一致**(3.2.1、3.2.2、3.2.4 三頁全中),擬答一律以本機實跑為準,貼文前 Kenny 自跑對數字。

### 待辦(下個 session 起點)
1. Kenny 續讀 3.2.3(SVM)→ 3.2.5(真實資料)→ 3.3.x;到 **3.3.1 理解文本練習 = 另一個必修投寄**,照本輪模式協助擬答。
2. 待貼清單:3.2.1 評論框(§7)、3.2.4 討論區(§9 v2 + 藍圖);連同 Unit 2 的五題(§1–6)都還沒貼。
3. **A2a 7/26 硬截止**(下週日):讀完 3.2.x 後去 Canvas 讀 A2a 題目+rubric 對照「優異」欄。
4. Kenny 持續更新 Google Doc(單元三筆記,已到 3.2.1)+ NotebookLM(建議補傳 notes/transcripts/ 兩份 Zoom 逐字稿)。

## 2026-07-19(深夜)· 3.3.1 定稿 + A2a 題目/rubric 已抓,進入 A2a 準備

- **3.3.1 理解文本(必修投寄)定稿**:擬答檔 §10 + `practice/Unit3_3_理解文本.ipynb`(headless 零錯誤;含 macOS SSL 修正)。答案:詞頻「措施」×6(「表示」若不濾亦 6,最高頻率必為 6);VADER 句1 compound -0.3412 負面、句2 +0.6364 正面。**未貼**。
- **A2a 情報已全抓**(Canvas API):見 `notes/A2a_題目與rubric.md` —— 電信 churn、六模型比較、報告四節=rubric 四條(20/20/25/25+形式10)、檔名規定、給高管的獨立報告。附件(資料集 file 12834685、課程筆記本 file 12834727)**尚未下載**(需登入,留給 Kenny 或下個 session 經瀏覽器抓)。
- 待貼清單不變:Unit2 五題 + 3.2.1 §7 + 3.2.4 §9v2 + 3.3.1 §10。
- **下個 session 起點 = A2a**:下載附件 → 開 `practice/A2a/` → 照 A2a 檔「下一步」順序做。7/26 截止。
