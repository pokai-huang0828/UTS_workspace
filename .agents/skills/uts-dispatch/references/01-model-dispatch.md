# 01 · 模型調度守則(指揮官手冊)

> 讀者 = 未來任何等級的主模型(含 Sonnet/Haiku)。規則可執行、有判準;不確定時照字面做。
> v2,2026-07-09 實查更新(v1 備份 `.claude/backups/governance-2026-07-09/`)。依據:[00-diagnosis.md](00-diagnosis.md) T2/T3/E2。

## 0. 本環境實際可用的型號與通道(2026-07-09 實查)

**派工報 model/參數/閘門錯誤時,第一動作 = 重查該工具的 schema/說明並更新本表(附日期),再繼續任務;禁止瞎猜參數繞過**(見 [02](02-judgment-rubrics.md) R-漂移)。

| 通道 | 可用值 | 備註 |
|------|--------|------|
| Agent tool `model` 參數 | `haiku` / `sonnet` / `opus` / `fable` | **無 effort 參數**;effort/工具集來自 agent 定義(`.claude/agents/*.md` frontmatter)— 本 repo 目前**沒有**自訂 agent,要建先派 1 個最小樣本驗證 frontmatter 真的生效 [未實測] |
| Agent tool `subagent_type` | `Explore`(只讀搜索)/ `Plan`(規劃)/ `general-purpose`(全工具)| 未指定 = general-purpose。另有大量 plugin agents(carta/nimble…)與 VMX 無關,不用。subagent 預設**背景執行**,完成會自動通知;要追問同一個 agent 用 SendMessage 續問,不要重派新的 |
| Workflow 腳本 `agent()` | `model` 同上 + `effort`:`low`/`medium`/`high`/`xhigh`/`max` | ⚠️ **2026-07-09 起 harness 對 Workflow 加明確授權門檻**:Kenny 原話出現「ultracode」,或明確要求「用/跑 workflow」= 授權(2026-07-09 工具文件明載);曖昧說法(「多開幾個 agent」不算授權)→ 改用同一則訊息平行發多個 Agent(見 §4),拿不準就先回問一句 |
| Codex CLI | gpt-5.5(`codex exec --sandbox read-only "..."`) | 驅動配方(拆 2–3 claims/趟、prompt 純 ASCII 走 stdin、`-o` 落檔)見 `.claude/skills/weekly-ingest/references/codex-driving.md`;單趟 >10 分鐘會被 timeout 砍 → **拆小,不是換模型** |
| 主迴圈 | session 當下模型(不可自選) | effort 繼承機器設定:Win 機全域 xhigh;Mac 機未設(2026-07-09 實查 `~/.claude/settings.json`) |

## 1. 六條鐵則

1. **指揮官不下場**:大量讀取(>2 個長檔)、掃 repo、查網頁、批次改檔 → 一律派 subagent,主對話只收結論。判準:主迴圈正要連續 Read 第 3 個長檔案(>200 行)= 停,改派工(= CLAUDE.md HC6)。本 repo 大檔警示:`calibration-log.md` 1312 行 / `handoff.md` 971 行 / `changelog.md` 916 行 — 這三個檔主迴圈只讀**最後 1–2 個 entry**,全檔消化一律派工([03](03-prompt-templates.md) §摘要)。
2. **機械工作用最便宜的模型**:格式盤點/路徑清查/逐字抽取 → `haiku`(Explore)或 `sonnet`(要寫檔時)。判準:「這工作有沒有標準答案?」有 → 便宜模型;要權衡取捨 → 高階。⚠️ Agent 的 subagent 繼承 session effort,機械工也照燒思考預算;要 per-call 降 effort 只有兩條路:(a)Workflow `agent(effort:'low')` — 需 Kenny 授權(§0);(b)`.claude/agents/` 自訂 agent [未實測]。兩條都不可用時:接受繼承,省 token 靠「派 haiku + 回報行數上限」。
3. **派工三件套**,缺一不派:①目標與動機(為什麼要做,讓 agent 能自行取捨邊界)②驗收條件(可檢查的輸出要求,含數量/格式/必答欄位)③回報格式(見鐵則 4)。模板照抄 [03](03-prompt-templates.md)。
4. **回報合約**:subagent 回報第一行 = 一句話 TL;DR;之後只有「結論 + 檔案:行號」;長產物(>50 行)寫到檔案、回傳路徑,**不回貼全文**。派工 prompt 裡明寫這句。
5. **先試跑再放量**:新型任務(沒派過的工作型態/新工具/新 agent 定義)先派 1 個最小樣本,驗收格式與耗時 OK 才批次。反例(實案):Codex 一包 10 claims 連兩次吃滿 10 分鐘 timeout,拆成 2–3 條後一次過。
6. **驗證不自驗**:產出者不當自己的驗收者 —
   - 檔案落地 → read-back(重讀確認內容完整)。
   - 程式/腳本 → 實跑一次或跑測試,貼 exit code。
   - 事實類文件 → fresh-context agent 或 Codex 對源核對(兩腦:不同模型家族 = 不同失誤模式)。
   - 高風險判斷(對外措辭/裁決)→ 第二意見,或多答案評審選優。

## 2. 派工對照表(照抄即可)

| 任務型態 | 派給 | 模板 |
|----------|------|------|
| 找檔案/盤點格式/路徑清查 | Agent(Explore, model=haiku) | [03](03-prompt-templates.md) §搜尋 |
| 消化長檔/email thread/會議逐字稿成摘要 | Agent(Explore 或 general-purpose, model=haiku;要判斷取捨時 sonnet) | 03 §摘要 |
| 逐字抽取/初稿轉換(來源已給定) | Agent(general-purpose, model=sonnet) | 03 §實作 |
| 跨檔重構/批次改檔(會動 git 檔案) | Agent(general-purpose, model=sonnet;高風險改 opus) | 03 §重構 |
| 開放式研究/多來源彙整 | Agent(general-purpose, model=sonnet 起步) | 03 §研究 |
| 審查/驗證(事實核對、規則打架) | fresh Agent(sonnet)或 Codex(read-only) | 03 §審查 |
| 主迴圈能力不足的判斷題(權衡/裁決/對外措辭初稿) | **往上派**:Agent(general-purpose, model=opus;不夠再 fable)— 弱指揮官可以派比自己強的專家 [首次使用先驗 model 可用性] | 03 §研究 或 §審查 改裝 |
| 對外措辭定稿/SSOT 裁決/風險簽核 | 主迴圈 + Kenny(這是唯一該下場的事) | — |

## 3. 升降級路徑(照字面執行)

- **haiku 錯 1 次** → 同一子任務直接升 sonnet 重派(不給 haiku 第二次)。
- **sonnet 同一子任務連錯 2 次** → 帶完整失敗軌跡(兩次的 prompt+輸出+哪裡錯)升 opus 或收回主迴圈;**不要**第三次原樣重派。
- **解出模式後降級**:高階模型解出的做法,整理成「可照抄的步驟+範例」後,批次套用改派便宜模型。
- **同一件事最多重試 2 輪**;第 3 輪 = 換方法或升級,見 [02](02-judgment-rubrics.md) R-換路。
- **「錯」的定義**(可判):驗收條件未過、回報缺必答欄位、引用了不存在的路徑/ID(幻覺)、或驗收者(鐵則 6)打回。格式醜但內容對 ≠ 錯,主迴圈自己整理即可。
- **Codex timeout(10 分鐘)** = 拆小任務,不是換模型。

## 4. 並行紀律

- 互不依賴的派工在**同一則訊息**一起發(省 round-trip);有依賴的等結果再派。
- 已委派出去的搜尋/讀取,主迴圈**不要自己同步再做一次**(雙倍燒 token,還會撞檔)。
- 同時在跑的 background agent ≤3,超過就先收成果再派新的(context 追蹤成本)。
- 兩個 agent 不碰同一批檔案;會碰 → 串行或 worktree 隔離(Agent tool `isolation: "worktree"`)。
