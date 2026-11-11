---
name: uts-dispatch
description: 指揮官派工守則(UTS_workspace)— 主腦只想、拆、寫工單、驗收;照工單做的派 sonnet high、核心派 opus high;Codex(異家族)對抗驗證。多步驟任務、批次讀檔、事實類交付、需要第二意見、開分身之前使用。派工 分工 開分身 省額度 model effort opus sonnet fable subagent.
---

# 指揮官手冊(UTS_workspace 版)

> 前身 = `frugal-fable`(移植自 MiTAC-VMX,2026-07-09)。2026-07-25 第一次改版(Opus 5 上線)。
> **2026-11-11 第二次改版**(Kenny 確認):整本跟上 `zm-dispatch`(Kenny 2026-11-08、11-11)的派工邏輯 ——
> 主腦只想不做、層級改成「模型 × effort」、不用 haiku、工單六欄、每張工單自己帶上限;同日重查 §0 全部事實。
> 這一版的獨立核對狀態寫在最下面「本版核對紀錄」。
> 原始 6 檔 + VMX Codex 配方逐字保存在 [references/](references/)。
> 讀者 = 任何等級的主模型;規則可執行、有判準,不確定時照字面做。

## 0. 本環境實查表(2026-11-11 Win 機重查)

**派工報 model/參數/閘門錯誤時,第一動作 = 重查該工具 schema 並更新本表(附日期),禁止瞎猜繞過**(R-漂移,見 [02](references/02-judgment-rubrics.md))。

| 通道 | 可用值 | 備註 |
|------|--------|------|
| Agent tool `model` | `haiku` / `sonnet` / `opus` / `fable` | **不寫 = 跟主腦同型號**(主腦是 Fable 時就是最貴那個)→ **model 一定要寫**。別名對到當代型號(Opus 5.5 / Sonnet 5.5 / Haiku 5.5)[⚠️假設:依 session 環境說明,沒有逐一實測] |
| Agent tool `effort` | `low` / `medium` / `high` / `xhigh` / `max` | **2026-11-11 schema 實查:有這個參數**(舊表寫「無 effort 參數」已過時)。工具說明要求「有明確指示才設」—— **本手冊就是那個明確指示:每次派工都照 §2 的表寫 effort** |
| Agent tool `subagent_type` | `Explore`(只讀)/ `Plan` / `general-purpose`(全工具)/ `fork` | 未指定 = general-purpose。**`fork` 一定跟主腦同模型,寫 model 也沒用** → 主腦是 Fable 時不用 fork |
| Agent 執行模式 | **一律背景**,做完才通知 | **2026-11-11 schema 實查:`run_in_background` 參數已不存在**,沒有「同步」開關。派出去就等通知:不輪詢、不自己重做同一件事、不預測結果 |
| Workflow 腳本 | `agent()` 支援 model + effort | ⚠️ 需明確授權:Kenny 說「ultracode」或明確要求「用 workflow」才可呼叫;曖昧說法 → 改同一則訊息平行發多個 Agent。每個 agent 都寫 model 與 effort,**opus 最多 1 個** |
| Codex CLI | `~/.codex/config.toml`:`model = "gpt-6.1-sol"`、`model_reasoning_effort = "high"`、`service_tier = "priority"` | **2026-11-11 實查**:PATH 上的 npm 版 `codex` = **0.162.1**,用預設設定 smoke **EXIT=0**(9/15 那次「npm 版太舊打不動」已解除)。備援 = Codex 桌面 App 內建 CLI(當日 0.167.0-alpha.3.2),路徑讀 config 的 `CODEX_CLI_PATH`,`<hash>` 會變,**每次先讀、不要寫死**。旗標 `--sandbox danger-full-access`(Kenny 2026-07-22 指示)。要更深就自己加 `-c model_reasoning_effort="xhigh"`[⚠️假設:xhigh 在 gpt-6.1-sol 上未重測]。配方與歷次踩坑見 [codex-collab.md](references/codex-collab.md) |
| Codex 三條老教訓 | (照做就好) | ① **打不動先對版本**:config 的 model 換了、CLI 沒跟上會回 400 → 改叫桌面版 CLI,不要瞎重試。② **有用量上限**:大件多輪審查別一次平行開多趟,失敗重跑的趟數也算;撞到就改派 fresh Claude agent(非產出者),交付時標明哪部分是誰驗的。③ **Win 機 prompt 用純 ASCII**;來源檔名含中文 → 先複製成 ASCII 檔名到 scratchpad(附 sha256 對賬) |
| Codex 驅動方式(依平台) | **Win = PowerShell**;Mac = Bash heredoc | Win:prompt 走 stdin、答案 `-o` 落檔。Mac(2026-07-26 實查):`cat prompt.txt \| codex exec --sandbox danger-full-access -o out.md`,中文 prompt 沒亂碼。跑完一律 `git status` 對賬。「叫不到 codex」多半是**開著的舊行程拿到舊 PATH**,不是 PATH 沒設 —— 解法見 codex-collab.md §8 |
| Canvas 抓取 | `/canvas-sync`(claude-in-chrome + Canvas API) | 頁面:同源 `fetch('/api/v1/courses/<c>/pages/<slug>')`;檔案:`/api/v1/files/<id>/public_url` → `curl -o`。⚠️ `javascript_tool` 單次回傳約 1000 字元,長內容分批(2026-07-26 Mac 實測) |
| Codex 能力邊界 | **播不了影片/音訊** | 影音驗收走 `/watch`,最後人耳留 Kenny(見 [a3-pitch-gates.md](references/a3-pitch-gates.md)) |
| 主腦(主迴圈) | Kenny 開對話時選的模型,中途不換 | **2026-11-11 = Fable 5.2**(試用,見 §2.3)。平常 = Opus |

### 0.1 費率表(排相對貴度用,不用來算錢)

來源:`claude-api` skill 內建價目(快取日 2026-11-03),與 `zm-dispatch` 2026-11-11 所記一致。

| 模型 | input / output(每百萬 token) | 相對 |
|------|------|------|
| Fable 5.2 | $8 / $40 | Opus 的 **2 倍**、Sonnet 的 **4 倍** |
| Opus 5.5 | $4 / $20 | 基準 |
| Sonnet 5.5 | $2 / $10 | 0.5× |
| Haiku 5.5 | $0.10 / $0.50 | **不在編制**(Kenny 2026-11-11:最低用 sonnet low) |

讀快取:Fable、Opus 都是 $0.20,Sonnet $0.10。**快取每個模型各一份** —— 中途換模型,整段要用新模型的價錢重寫。

**⚠️ 換不成錢**:Agent tool 只回一個 `subagent_tokens` 總數,拆不出 input / output / 快取(2026-07-25 實查,11-11 未重查)。所以帳本**以總 token 記**,費率表只用來排「誰比較貴」。

## 1. 七條鐵則

1. **主腦只做四件事:想清楚、拆工作、寫工單、驗收。** 不做長執行。主對話「**5 個工具呼叫內,而且輸出很小**」才自己做(主腦是 Fable 時改 **3 個**)。讀長檔、掃 repo、查網頁、批次改檔一律派分身 —— 網頁全文和長檔留在主對話裡,之後每一回合都要再算一次錢。
2. **現成的腳本和 skill 做得到,就不派模型。** `/canvas-sync`、`/handoff`、`/codex-verify`、`/watch`、repo 裡的 `build_*.py`、`analysis/*.py` 先用。
3. **預設 sonnet high;核心用 opus high;最低 sonnet low。** 不用 haiku,不用 opus low(只少想一點,價錢沒少多少)。**拿不準就升一級** —— 便宜的做錯重來更貴,而且抄漏的內容下游會當成「不存在」。
4. **工單六欄缺一不派**(§2.4):單/範圍/先讀/禁止/上限/回報。**model 和 effort 一定要寫。**
5. **回報合約**:分身第一行 = 一句話 TL;DR;之後只有「結論 + 檔案:行號」;長產物(>50 行)落檔回傳路徑,不回貼全文。
6. **先試跑再放量**:新型任務先派 1 個最小樣本,驗收格式與耗時 OK 才批次。
7. **驗證不自驗**:產出者不當驗收者。**自檢可以提供客觀完成證據(命令輸出、檔案 read-back、對賬數字),但永遠不滿足「需要獨立驗證」的要求 —— 這是兩件事**(§6 R-獨立)。事實類文件 → fresh agent 或 **Codex 異家族**核對;高風險判斷 → 第二意見。

## 2. 層級與派工表

### 2.1 層級(Kenny 2026-11-08 定,2026-11-11 套用到 UTS)

| 層級 | 什麼時候 |
|---|---|
| **opus high**(核心,短單) | 會直接被評分的東西的**論證和數字**:交件報告、notebook、投影片的內容;方法論或統計設計;跨文件數字要對賬的改寫;評分預估;兩個定案互相衝突時出裁決草稿 |
| **主腦**(Opus medium;Fable 見 §2.3) | 想清楚、拆工作、寫工單、驗收、跟 Kenny 定方向。在主對話做,不派分身 |
| **sonnet high**(預設) | 照工單做:逐字稿和 Canvas 內容落檔、摘要、筆記、初稿轉換、查證、盤點、獨立核對(語意面)。**邏輯由主腦先想好寫進工單** |
| **sonnet low**(最低) | 三條**都**符合才用:①主腦已把確切內容寫進工單(照抄、照表)②完全不用判斷 ③做完驗得出對錯。例:照清單批次改字、跑指令回報結果、關鍵字和格式都寫死的盤點 |

**選的順序**:現成腳本/skill 做得到 → 不派模型。否則對照上表**由上往下**,第一個符合的就用。

### 2.2 派工表(上限 = 工具呼叫次數／讀進來的量)

上限是**起始值**(由 zm-dispatch 換算,加上本 repo 歷次實耗),每次照 handoff 記的實耗往回修。

| 工作 | 做法 | model · effort | 分身 | 上限 | 回報行數 |
|---|---|---|---|---|---|
| 跟 Kenny 定方向、裁決 | 主對話自己做:一次一題、最多 2 個選項、推薦的放 A | 主腦 | — | — | ≤ 5 |
| 抓 Canvas 新內容 | skill `/canvas-sync` | — | — | — | 5 |
| 補交接紀錄 | skill `/handoff` | — | — | — | 3 |
| 影片/音訊 QA | skill `/watch` + ffmpeg;人耳最後確認留 Kenny | — | — | — | 5 |
| 找檔、盤點、路徑清查 | Agent | sonnet low(關鍵字和格式都寫死);否則 sonnet high | Explore | 10／8 萬 | 10 |
| 逐字稿、長檔 → 落檔與摘要 | Agent | sonnet high | general-purpose | 25／12 萬 | 8 |
| 筆記、初稿轉換、資料整理 | Agent | sonnet high | general-purpose | 30／12 萬 | 8 |
| 交件檔本體(報告、notebook、投影片內容) | Agent,一項一單 | **opus high** | general-purpose | 40／15 萬 | 8 |
| 方法論、統計設計、評分預估 | Agent,短單,只出設計不做長實作 | **opus high** | general-purpose | 20／8 萬 | 10 |
| 開放式研究、多來源、查網路 | Agent,**工單一定寫搜尋次數上限**(這類最燒錢,見 §8.4) | sonnet high | general-purpose | 25／12 萬,搜尋 ≤ 8 次 | 10 |
| 批次改字(同一個字多處) | 先 grep 列位置;同一個字用一支腳本取代。只有要看上下文的幾處才派 | sonnet low | general-purpose | 10／8 萬 | 5 |
| 語意/rubric 覆蓋審查(驗證軌 ①) | fresh Agent,**非產出者** | sonnet high | general-purpose | 20／10 萬 | 10 |
| 數字再推導、跨文件矛盾、引用實在性、方法論(驗證軌 ②) | **Codex(read-only)**,`/codex-verify`;與軌 ① 同一則訊息發 | Codex | — | 單趟 < 8 分鐘 | 逐條 verdict |
| 口試、答辯對抗演練 | fresh Agent 扮評分者,嚴格計時,追問決策/替代方案/風險 | sonnet high | general-purpose | 20／10 萬 | 10 |
| workflow、大型分析 | **先問 Kenny**;每個 agent 寫 model 與 effort;opus 最多 1 個 | — | — | — | 30 |
| 對外定稿、不可逆動作、裁決 | 主腦 + Kenny(唯一該下場的事) | — | — | — | — |

影片/投影片/口試型作業的專用閘門(渲染稽核、片長、音訊)已存檔在 [a3-pitch-gates.md](references/a3-pitch-gates.md),再遇到時拿來用。

### 2.3 主腦是 Fable 時(Kenny 2026-11-11 試用;主腦是 Opus 時整段不看)

Fable 寫字比 Opus 貴一倍、比 Sonnet 貴四倍,所以:

- 主對話「**3 個工具呼叫內,而且輸出很小**」才自己做(取代 §1 的 5 個)。主腦只想、拆、寫工單、驗收。
- **effort**:派工、驗收用 medium;定方向、難題才 high;不用 xhigh、max。
- **升級多一層**:opus high 新單還是沒好 → `fable` high **短單**,≤ 20 回／8 萬,只出原因和做法,不做長實作;實作再派回 sonnet high 或 opus high。**這是唯一可以用 fable 分身的地方。**
- 其他分身照 §2.2 不變。**model 一定要寫**(沒寫會跟著主腦用 Fable);**不用 `fork`**(一定跟主腦同模型)。
- 要用 Fable 就**開新對話、一開始就選 Fable**。中途換模型,整段快取要用新模型的價錢重寫;隔太久回來重寫也貴 → 用 `/handoff` 收尾,換新對話。
- 這是試用:做完一個大題目,跟平常比額度,**留不留由 Kenny 決定**。
- 舊版 §2.1「Fable 5 退出常規編制」的依據是 2026-07 的 Fable 5 對 Opus 5 外部評測,型號已換兩代、價格也變了 → **那段結論作廢,不再引用**。現行規則就是本節。

### 2.4 工單(照抄填空;六欄缺一不派)

呼叫:`Agent(subagent_type, model, effort, description, prompt)`。

```
【單】一件事。做完的樣子:…(可檢查的驗收條件)
【範圍】只改:…　不碰:…
【先讀】最多 5 項,寫明檔名和節名或行段
【禁止】整檔讀任何超過 20 KB 的檔(handoff.md、TODO.md、各課 README、91_上課紀錄 都是;用 grep + offset);
       改交件檔(*_交件/、已上傳的 docx/pdf/ipynb);對外送出任何東西;等超過 5 分鐘的事(交回主對話)
【上限】工具呼叫 N 次(查網路另寫搜尋 ≤ M 次),到了就停,回報進度和沒涵蓋的部分。scope ID:…
【回報】≤ K 行繁體中文:第一行一句話結論/做了什麼(檔案:行號)/沒做的。不貼全文、不貼 log
```

舊的六型派工模板(搜尋/實作/審查…)仍在 [03](references/03-prompt-templates.md),要長一點的寫法時參考;欄位以這一份為準。

## 3. 升級與降級

- **sonnet low 錯 1 次** → sonnet high。
- **sonnet high 同一張單被打回 2 次** → opus high **新單**,只帶失敗摘要(不把整段對話丟過去)。
- **opus high 還是沒好** → 主腦是 Fable:照 §2.3 開 fable high 短單。主腦是 Opus:收回主對話;仍無解 → 照 R-問人 交 Kenny。
- **水平換家族(盲點型錯)**:沿用舊 context、跨文件矛盾、數字抄自己算過的、自驗盲點 → **不是升級,是開 Codex**。升級解決不了盲點。
- **到上限**:分身停下回報進度;主腦問 Kenny「**A 繼續(推薦)/ B 停**」。
- **降級**:高階解出模式 → 整理成可照抄的步驟 → 批次改派 sonnet high 或 sonnet low。
- 同一件事最多重試 2 輪;第 3 輪 = 換方法或升級(R-換路)。不第三次原樣重派。
- Codex timeout = 拆小任務,不是換模型。
- 「錯」的定義:驗收未過、缺必答欄位、引用不存在的路徑/ID、或驗收者打回。格式醜但內容對 ≠ 錯。

## 4. 並行紀律

- 互不依賴的派工在**同一則訊息**一起發;有依賴的等結果再派。
- 已委派的事,主腦不自己再做一次(雙倍燒 token)。
- 同時在跑的分身 ≤ 3。
- 兩個分身不碰同一批檔案;會碰 → 串行,或 `isolation: "worktree"`。
- 分身一律背景跑(§0):派完就做不依賴它的事,或等通知;**不輪詢、不猜結果**。

## 5. Agent × Codex 兩腦協作架構

核心:**Claude 生產、Codex(異家族)驗證** —— Codex 抓到的錯多是「Claude 沿用自己舊筆記」型,自驗有共同盲點。完整配方見 [references/codex-collab.md](references/codex-collab.md)。

```text
主腦(Opus medium;試用期 Fable medium)— 想、拆、寫工單、驗收
 ├─ 生產線:sonnet high 照工單做 → opus high 做核心(論證、數字、方法)
 ├─ 驗證線【並行,同一則訊息發出,不排隊】
 │   ├─ 軌①語意面:fresh Claude(sonnet high,非產出者)— 有沒有漏講、rubric 有沒有蓋到、論證缺口
 │   └─ 軌②事實面:Codex(read-only)— 數字、跨文件矛盾、引用實在性、方法論
 └─ 裁決:主腦整合 → 對外/不可逆 → Kenny
```

**兩軌查的維度不重疊,所以並行不犧牲覆蓋 —— 省的是等待時間。**

**什麼時候一定要開 Codex(看「風險 × 獨立性」,不是看有幾條 claim):**
- 這個錯若存在,是**能力型**(方法錯、論證漏)還是**慣性型**(抄自己舊數字、跨檔矛盾、引用不存在)?慣性型 → 必 Codex。
- 交付**直接面對評分者或不可逆**?是 → Codex 終審閘門不可省。中間產物 → 抽查即可。
- **Codex 不可用**(額度滿、打不動)→ 改派 fresh Claude agent(非產出者),交付時**寫明哪部分只有 Claude 驗過**。

**多輪稽核的範圍:**
- R1 全件
- R2 = 缺陷清單 + 改動鄰域 + **凡涉數字的修正一律三邊對賬**(notebook ↔ 報告 ↔ results.json)。理由:表四 759→767 那次是跨產物傳遞依賴,只看鄰域會漏。
- R3 全件兜底,終審

**自檢指令:**
| 對象 | 做法 |
|---|---|
| opus / fable 分身 | **刪掉**多餘的「再檢查一次 / 回答前再驗一遍」—— 它本來就會自檢。要獨立驗證就另派 fresh verifier |
| sonnet 分身 | 工單照 §2.4 原樣寫,不加不減 |

## 6. 判準速查(完整版見 [02](references/02-judgment-rubrics.md))

- **R-完成**:交付必附證據四選一(命令輸出/read-back/對賬數字/第二意見),沒有證據不得說「完成」。
- **R-獨立**:**產出者的自檢可以提供 R-完成 的客觀證據,但永遠不滿足「需要獨立驗證」的要求。** 主腦覺得自己查過了,不算查過。
- **R-問人**:只有四類該問 —— 花錢/對外/不可逆、架構級分歧、指示互相矛盾、憑證只有 Kenny 有;其餘選預設 + 標「⚠️假設」。問的時候:一次一題、最多 2 個選項、推薦的放 A。
- **R-換路**:被打斷 ≥2 次且是重定向、同一錯誤重現 2 次、第 3 個 edge case 補丁、驗證過但不是要的 → 停手換路。
- **R-回讀**:用 Kenny 給的日期/ID/數字前,第一句先回讀關鍵值。
- **R-漂移**:工具與規則打架 → 實查 schema、更新 §0、附日期,才繼續。
- **R-A3(影音交付閘門)**:已存檔 → [a3-pitch-gates.md](references/a3-pitch-gates.md)。

## 7. 交付前 60 秒 checklist

```text
□ 列舉型 → 來源 N = 輸出 N?差額有解釋?
□ 關鍵數字/日期/ID 與來源逐字對過?
□ 完成宣稱:有 R-完成 四種證據之一?
□ 需要「獨立驗證」的項目,證據來自非產出者?(R-獨立)
□ 每個新檔 read-back 過?
□ 對外內容:個資已 strip?語言 = 繁體中文(台灣用語)?
□ 每張工單的 model、effort、上限都有寫?
□ handoff 已記:本 session 按模型分列的 subagent token?(§8.3)
```

## 8. 成本管控(2026-11-11 改寫)

### 8.1 每張工單自己帶上限

上限寫在工單【上限】欄(§2.4):工具呼叫次數、查網路的搜尋次數、回報行數、一個不重複的 scope ID。
**到上限的分身必須停下來回報「做到哪、哪些沒涵蓋」,不得自己續跑。** 主腦再問 Kenny「A 繼續(推薦)/ B 停」。

### 8.2 沒有 session 總預算

舊版的「預設 1.5M、70% 停派、預先扣額度」**已作廢**。Kenny 在 2026-08-05~07 那次 session 明確否決:那是手冊自己寫的數字,不是任何系統額度,**不得再拿它擋派工**。
取代它的只有兩道閘:

- **第 9 個分身之前**:先報一次本 session 累計 subagent token,問 Kenny「A 繼續(推薦)/ B 停」。
- **workflow 和大型分析**:開跑前先問 Kenny(§2.2)。

其餘 spawn 上限照舊:同時在跑 ≤ 3;每個開放問題 ≤ 2 個研究 agent;每個產物每輪 ≤ 1 個驗證 agent。

### 8.3 帳本(記實耗,用來校準 §2.2 的上限)

- 派工時記:scope ID、model、effort、上限。
- 回來後記:實耗 token、工具呼叫次數、有沒有超上限。
- **沒回報用量的分身,寫「未回報」,不得當成 0。**
- 每個 session 的 handoff entry 記**按模型分列的 subagent 總 token**;Codex 另記趟數。

### 8.4 錢最容易燒在哪(本 repo 實測)

- **沒設界線的研究型 agent**:2026-07-25,兩個查網路的 agent 各約 44 萬 token,是同場立場書 agent(8.6 萬)的 5 倍。
- **workflow**:單次 200 萬到 700 萬 token(2026-09-23、10-08 實測)。
- **主腦是 Fable 時的主對話本身**:長讀取、長輸出都在最貴的模型上 → 所以門檻降到 3 個工具呼叫。

### 8.5 殘餘風險(直接告知,不假裝解決)

**寫在工單裡的上限擋不住真的失控的分身**,除非執行環境會強制終止它。本框架只能在**派工前**攔,攔不住已經開跑的。

## 本版核對紀錄(2026-11-11)

- §0 的事實來自當日命令輸出與工具 schema(R-完成 證據);標 [⚠️假設] 的沒有實測。
- 派工邏輯移植自 `~/.claude/skills/zm-dispatch/SKILL.md`(2026-11-08、11-11 版),「改多大」與「最低層模型」兩項由 Kenny 當日選定。
- **沒有獨立核對。** 原本開了一趟 Codex 唯讀審查,Kenny 當場說「不用了,都由你來負責」,已中途停掉、沒有產出。所以這一版只有產出者(主腦)自檢:舊字眼掃描、節號與 CLAUDE.md 的引用對得上、references 連結 10 個全部存在、A3 三段原文搬進存檔檔。**照 R-獨立,這不算獨立驗證** —— 之後用起來發現規則互相打架,照 R-漂移 當場修並記日期。

## references/ 清單

| 檔案 | 內容 |
|------|------|
| [README.md](references/README.md) | 移植來源與適用性 |
| [00-diagnosis.md](references/00-diagnosis.md) | VMX 原檔:harness 漏 token/失焦/出錯 前三名診斷 |
| [01-model-dispatch.md](references/01-model-dispatch.md) | VMX 原檔:模型調度守則(舊版 §0–§4 的母本;**haiku 階梯已不適用**,以本檔 §2 為準) |
| [02-judgment-rubrics.md](references/02-judgment-rubrics.md) | VMX 原檔:R-升級/完成/問人/換路/回讀/新開/漂移 全文 |
| [03-prompt-templates.md](references/03-prompt-templates.md) | VMX 原檔:六型派工模板(欄位以本檔 §2.4 為準) |
| [04-maintenance-protocol.md](references/04-maintenance-protocol.md) | VMX 原檔:治理檔維護權限與教訓登記簿 |
| [05-letter-to-future-sessions.md](references/05-letter-to-future-sessions.md) | VMX 原檔:給未來 session 的信 |
| [codex-collab.md](references/codex-collab.md) | **本機版** Agent×Codex 協作架構 + 駕駛配方 + 輸出合約 + 環境漂移紀錄(§8) |
| [codex-driving-vmx-machine.md](references/codex-driving-vmx-machine.md) | VMX 公司機原版配方(本機不適用,留作對照) |
| [a3-pitch-gates.md](references/a3-pitch-gates.md) | 存檔:影片 pitch / 投影片 / 口試型作業的交付閘門與 preflight(原 §2、§6 R-A3、§7.1) |
