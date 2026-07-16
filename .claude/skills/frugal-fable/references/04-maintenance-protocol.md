# 04 · 維護協議 — 弱模型怎麼安全更新這套治理檔

> 讀者 = 未來 Sonnet/Haiku。照字面執行;拿不準就歸入「先問」。
> v2,2026-07-09:§1 加一列與通則、§3 追加 4 條教訓、§4 加逐台驗與門檻統一;備份慣例補保留政策與 commit 要求;§2 MEMORY 行加逐台。完整 diff 對照 v1 備份 `.claude/backups/governance-2026-07-09/`,**待 Kenny 追認**。

## 1. 權限分級

| 動作 | 授權 |
|------|------|
| [03](03-prompt-templates.md) 加新模板、`tools/` 加新只讀工具 | **可自行改**(改完 read-back + 在本檔 §3 登記) |
| [01](01-model-dispatch.md) §0 型號表(實查 schema 後更新,附實查日期) | **可自行改** |
| 規則檔內指向 repo 外的引用(memory、單機絕對路徑)= 制度 bug | **可自行改**成 git 內路徑或標「[懸空]」;若引用背後的**語義**要變(如紅線內容),先問 |
| 本檔 §3 教訓登記簿 append | **可自行改** |
| CLAUDE.md 硬約束 HC1–HC6 增/刪/改、01 鐵則、02 rubric 判準 | **先問 Kenny**(附:動機 + 原文 + 新文 + 影響) |
| AGENTS.md、audit findings 的裁決欄 | **只有 Kenny 能定**;agent 至多提案 |
| 刪除任何治理檔 | **先問 Kenny** |

備份慣例:改 CLAUDE.md 前 `cp CLAUDE.md CLAUDE.md.bak.<YYYY-MM-DD>`;治理檔整批改版前 `cp .claude/governance/*.md .claude/backups/governance-<YYYY-MM-DD>/`(先 mkdir)。備份目錄只留最近 2 個日期,更舊的靠 git history。備份與 .bak 檔要**跟著改版一起 commit**(untracked 備份在別台機器上等於不存在,= 另一種懸空指標)。

> 授權來源:01/03/tools 的預設 owner = Claude Code,依 [AGENTS.md](../../AGENTS.md) §2「知識庫維護」主責;此表其餘「先問 Kenny」條目 = AGENTS.md §1 決策權(最終定案交回 Claude+PM)的落地。本表由 Kenny 裁決後生效,agent 不得自行擴權。
>
> 通則(07-03 版原則回補):任何標記「待裁決/待追認」的修法,拿到裁決前**不執行**;先上線後補裁決 = 違規,發現就回退並記 §3。Kenny 在 session 中的明確指示 = 即時裁決,照做並在遷移紀錄留痕(例:2026-07-09 v2 重校 = 當日指示授權、已裁決,「待追認」僅為細節確認,不觸發本通則)。

## 2. 精簡門檻(超標就做精簡 pass,不要等)

| 對象 | 門檻 | 精簡規則 |
|------|------|----------|
| CLAUDE.md | **>60 行** | 加一條硬約束必同時刪/下放一條;敘事段落移治理檔,只留一行路由 |
| 本檔 §3 登記簿 | **>20 條** | 同因合併成一條 rubric 提案(進 02),原始條目移到檔尾「已吸收」區 |
| MEMORY.md(user 層,逐台各自檢查) | **全檔 >12,000 字元 或 單行 >600 字元** | ⭐區 ≤7 條;W-status 行 ≤400 字元,細節下放 weekly 檔;Active ≤8 條,結案移「近期事件」一行 |
| 01–03 任一檔 | **>120 行** | 例子移到檔尾附錄或刪重複,正文保住「判準+一正一反」 |

檢查指令(隨時可跑):`python -c "print(sum(1 for _ in open('CLAUDE.md',encoding='utf-8')))"` 期望 ≤60。

## 3. 教訓登記簿(踩坑後 5 分鐘內寫,格式固定)

格式(一條一行):`日期 | 情境 | 錯了什麼 | 改法 | 驗證方式`

- 2026-07-03 | Codex 驗證派工 | 10 claims 一包 → 連兩次 10min timeout 全損 | 拆 2–3 claims/趟 + 指示程式化比對 | 單趟 <8min 完成、exit 0
- 2026-07-03 | SessionStart hook | 用 `pwsh` 但機器只有 `powershell` → 8 個月靜默不跑 | hook 命令寫進 repo 前先在目標機實跑一次 | `Get-Command <runner>` 有解 + 手跑 exit 0
- 2026-07-03 | 同上的第一版修法 | 提議 `pwsh`→`powershell` 忘了 repo 要跑 Mac(powershell 在 macOS 不存在)= 修法自己犯跨平台錯 | committed 檔裡**不寫死任何 per-OS runner**;per-OS 差異照 launch.json 慣例走 setup-agents.sh 生成進 gitignored local 檔 | 檢視 settings.json:`grep -c "pwsh\|powershell" .claude/settings.json` 目標 0
- 2026-07-03 | 靜態頁 regex 檢查 | 頁面改版後檢查 pattern 0 命中 = 永遠綠燈 | 檢查器要驗「pattern 至少命中一次」的自檢(deadman switch) | grep 計數 >0 才算檢查有效
- 2026-07-03 | md-lint 首跑 | 把 list 縮排續行誤判為違規(presentation-workflow.md:65)| **新檢查器首跑必 report-only 過人眼**再 enforce;SAFE_PREV 補縮排續行 | 首跑 45 檔 2 hits → 1 真 1 誤,修後 0 violations
- 2026-07-06 | weekly audit regex | removed-membership 誤抓 cross-ref(VMX-7404;與 W26 同款,第 2 次) | **同款 gotcha 第 2 次出現 = 把檢查寫進工具**(候選:audit diff 邏輯固化成 repo script + cross-ref 區排除),不再靠人記 | 下次 weekly 的 removed 表 0 誤抓
- 2026-07-09 | 治理引用 | 01 檔與 HC5 指向 memory 檔,Mac 機的 memory 沒有這些檔(懸空指標 ×2,照做 = 死路) | 規則依據只准指向 git 內路徑(已入 CLAUDE.md 定位段);兩處已改 | `grep -rnE "(見|照|依|參)[ ]?memory|durable[ ]rules" CLAUDE.md .claude/governance/0[1-4]*.md` 期望 0 hit(00/05 是歷史敘述檔,引述舊病灶不在偵測範圍)
- 2026-07-09 | harness 漂移 | Workflow 工具新增 ultracode 授權門檻,照 01 v1 教法直接呼叫 = 違反工具閘門 | 01 §0 更新(附實查日期)+ 02 新增 R-漂移:報錯第一動作 = 實查 schema 更新表,不是瞎猜繞過 | 01 §0 表頭含「2026-07-09 實查」
- 2026-07-09 | 機器層修法 | C1 plugin 修在 Win、Mac 未做而復發;A1 hook 退役清了 `.claude/settings.json` 漏了 `.codex/hooks.json` | 機器層修法**逐台驗**(見 §4 第 5 點);`.codex/hooks.json` 是 gitignored 機器本地檔(`.gitignore:2`),Mac 側已清空(備份 `.claude/backups/governance-2026-07-09/codex-hooks.json.bak`),**Win 側同檔待清** | `grep -c "pwsh" .codex/hooks.json` 期望 0(逐台各跑);Mac 開場可見 plugin 家族 ≤10

- 2026-07-09 | Codex 複核 Run A | 全 repo 文件寫 `python`,Mac 只有 `python3` → HC4 照抄 = command not found | 不逐檔寫死 per-OS runner(沿 07-03 教訓 3),CLAUDE.md HC4 加一句全域代換規則(Win=`python`/Mac=`python3`) | Mac 跑 `python3 .claude/scripts/build.py --check` exit 0
- 2026-07-09 | Codex 複核 Run B | 工具 `--dir` 缺值 IndexError;deadman 只驗檔案存在、不驗可讀內容(空 jsonl = 假綠燈) | `--dir` 缺值/接 flag → exit 2;有檔但 0 可讀 user 訊息 → 印 WARN + exit 1 | `--dir` 無值實跑 exit 2;空內容目錄實跑 exit 1;正常跑仍 exit 0

> 新教訓 append 在上方清單末尾(勿寫死條數)。屬於「判斷類」的教訓,同時到 [02](02-judgment-rubrics.md) 開提案(先問 Kenny)。

## 4. 每季維護(或大改版後;掛在某次 weekly-ingest 順跑)

1. 重跑 [audit-findings-2026-07-03.md](audit-findings-2026-07-03.md) 全部驗證指令 → 期望值變了就更新該檔 + [00](00-diagnosis.md)(含 §四落地對照表)。注意:user 層指令(C1/C2/丁段)要在**對應機器**跑 — 基線量測於 Win 機,在 Mac 跑出的 0 不是綠燈。
2. 重跑 `python .claude/governance/tools/mine-session-pain.py`(2026-07-09 起 log 目錄自動推導 + deadman:零檔案 exit 1)→ md-render 季增 ≥5、其餘 pattern 季增 >10 = 對應規則沒生效,開檢討(門檻定義以 [00](00-diagnosis.md) F3 為唯一真相;基線逐台各自累積,不跨機比對)。
3. 實查 Agent tool schema 與工具閘門 → 更新 01 §0(附日期)。
4. 檢查 §2 門檻全表。
5. **逐台機器驗**:機器層設定(plugin 數、effort、hooks)在每台工作機各驗一次;目前工作機 = Win(`C:\Users\pokai.huang`)+ Mac(`/Users/pokaihuang`)。單台修完 ≠ 結案。

## 5. 裁決時效

audit findings 的 ☐ 條目,**30 天無裁決 = 視為「暫不修」**,由當值 agent 把該條移到 findings 檔尾「未裁決歸檔」區(內容原封不動,可隨時復活)— 防裁決積壓變殭屍清單。
