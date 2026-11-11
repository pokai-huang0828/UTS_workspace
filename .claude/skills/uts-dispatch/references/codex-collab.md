# Agent × Codex 兩腦協作架構(UTS_workspace・Kenny 個人 Win 機)

> 2026-07-16 本機實測撰寫;母本 = VMX `codex-driving.md`(公司機版,見 [codex-driving-vmx-machine.md](codex-driving-vmx-machine.md))。
> **現況(2026-11-11 Win 實查)**:npm 版 codex-cli **0.162.1**,`~/.codex/config.toml` = `model = "gpt-6.1-sol"`、`model_reasoning_effort = "high"`、`service_tier = "priority"`,預設設定 smoke EXIT=0。**型號和版本會一直變 —— 每次以 config.toml 和 `codex --version` 為準,SKILL §0 是最新紀錄,歷次變動在本檔 §8。**
> 以下第 4–5 行是 2026-07-16 的原始紀錄,留作歷史:
> 本機環境:codex-cli **0.144.5**,model **gpt-5.6-sol**,已 `codex login`,reasoning effort xhigh(config:`~/.codex/config.toml`)。
> ⚠️ 型號命名(2026-07-16 實查):ChatGPT 帳號下裸名 `gpt-5.6` 會 400;5.6 系列實際名稱 = `gpt-5.6-sol`(旗艦,官方描述「most ambitious work」)/ `gpt-5.6-terra` / `gpt-5.6-luna`,三者皆實測 EXIT=0。可用型號清單可從 CLI 二進位撈:`grep -oaE "gpt-5[a-z0-9.\-]*" <codex.exe> | sort -u`。

## 1. 為什麼要兩腦

Codex(OpenAI 家族)與 Claude 的**失誤模式不同**。VMX 實錘:Codex 抓到的錯全是「Claude 沿用自己舊筆記/舊 context」型——這類錯 Claude 自驗(包括 fresh Claude agent)有共同盲點。因此:

- **什麼時候必開 Codex,以 SKILL §5 的「風險 × 獨立性」為準**(2026-07-25 起不再看 claim 數):慣性型的錯(抄自己舊數字、跨檔矛盾、引用不存在)、或直接面對評分者/不可逆的交付 → 必開。
- 小事(格式類、中間產物)→ fresh Claude agent(sonnet high,非產出者)就夠。
- 品味/模糊判斷(對外語氣、要不要做)→ 兩腦都補不了,照 R-問人 交 Kenny。

## 2. 角色分工(架構圖)

```text
┌─ 指揮官:主迴圈(session 模型)──────────────────────────┐
│  拆解任務、選模型、發派工三件套、收 TL;DR、整合裁決          │
└──────────────┬───────────────────────────┬───────────────┘
               │ 生產線(Claude 家族)         │ 驗證線(異家族)
   ┌───────────▼───────────┐   ┌───────────▼───────────┐
   │ sonnet low 照抄/盤點     │   │ fresh Claude agent      │
   │ sonnet high 照工單做     │   │  (sonnet high)語意審查   │
   │  落檔/摘要/轉換/查證      │   │ Codex(read-only)        │
   │ opus high 核心論證與數字  │   │  事實核對,逐條 verdict   │
   └───────────────────────┘   └───────────────────────┘
               │                           │
               └────────► Kenny:對外定稿/不可逆/裁決 ◄────┘
```

**流程**:產出(Claude)→ read-back 自檢 → fresh Claude 審查 → 事實類加開 Codex → 主迴圈整合 → 需要時 Kenny 裁決。產出者永遠不當自己的驗收者。

## 3. 本機駕駛配方(2026-07-16 實測 EXIT=0)

用 **PowerShell tool**(非 Bash [⚠️假設:Bash 未實測,VMX 公司機 Bash 會炸 CLM;本機沒驗過前照用 PowerShell]),prompt 走 **stdin**,答案用 **`-o` 落檔**:

```powershell
$out = "<scratchpad>\codex-out.md"
$prompt = @'
...pure ASCII English prompt (multi-line OK)...
'@
$prompt | codex exec --sandbox danger-full-access -o $out
Write-Output "EXIT=$LASTEXITCODE"
Get-Content $out
```

> **2026-07-22 更新(Kenny 指示:不用 sandbox)**:旗標改 `--sandbox danger-full-access`(smoke PASS,EXIT=0,可讀 repo 外路徑)。背景:07-22 實測發現 `--sandbox read-only` 只能讀 workdir(repo)內檔案,scratchpad 等外部路徑 Access denied,得先把材料複製進 repo 才能比對;Kenny 裁定直接放行。**紀律不變**:驗證任務在 prompt 裡明寫 "read-only; do not modify or create any file",跑完 `git status` 對賬;要 Codex 寫檔的任務仍先問 Kenny。

與 VMX 公司機的差異(實測):

| 項目 | VMX 公司機 | 本機(kenny Win) |
|------|-----------|------------------|
| sandbox 旗標 | 必須 `--dangerously-bypass-approvals-and-sandbox`(CLM 擋 wrapper) | **`--sandbox read-only` 直接可用**,不需要 bypass ✅ |
| prompt 通道 | stdin(arg 會被拆爆) | 同 — 照用 stdin |
| prompt 編碼 | 純 ASCII(中文經 PowerShell 會亂碼) | [⚠️假設:未實測中文,照用純 ASCII 最穩] |
| stdout 重導 | 禁止(`1>` 觸發 encoding bootstrap exit 2) | 照禁 — 用 `-o` 落檔 |
| 驅動工具 | PowerShell tool | 同 |

**跑完必做**:`git status` 確認 Codex 只動了該動的(read-only 任務理論上不動檔,仍要驗)。

## 4. 任務紀律(承 VMX 教訓登記簿)

1. **拆小**:單趟目標 <8 分鐘。舊數字「每趟 2–3 條 claims」是 gpt-5.5 時代的(VMX 2026-07-03:10 條一包連兩次 timeout 全損);2026-07-26 實測一趟 6 個複合 claim + 讀 3 個檔 EXIT=0,已放寬。timeout 了再拆。
2. **先試跑再放量**:新型 Codex 任務先 1 條 smoke(本檔配方已是驗過的 smoke),格式/耗時 OK 才批次。
3. **timeout = 拆小,不是換模型**。
4. **輸出合約寫進 prompt**:要求 Codex 逐條回 verdict,禁散文。

## 5. 驗證派工模板(ASCII,填空即用)

```text
You are an independent fact-checker. Default stance: skeptical.
Verify the following claims against the repository files. For each claim:
- Re-derive the fact from the source file(s) yourself; do NOT trust the claim text.
- Reply with: CLAIM <n>: CONFIRMED | REFUTED | CANNOT-VERIFY, then one line of evidence (file path + line or quoted value).

CLAIM 1: <e.g. file X section Y states value Z>
CLAIM 2: <...>
CLAIM 3: <...>

Rules: read-only; do not modify any file; no prose outside the per-claim verdicts;
if a file is missing, say CANNOT-VERIFY and name the path you tried.
```

其他可派給 Codex 的型態(同樣 read-only):規則互相打架掃描(兩份文件矛盾)、路徑/命令實在性抽查、diff 對賬。**不要**派給 Codex:要寫檔的任務(在本 repo 一律由 Claude agent 寫,Codex 只驗)[⚠️假設:如需 Codex 寫檔,先問 Kenny 開 sandbox 等級]。

## 5.1 對抗審查/設計評審模板(2026-07-25 新增,實測有效)

事實核對用 §5。**要 Codex 評審一個設計、計畫、或立場書時用這一份** —— 差別是它被強制提出替代方案,不能只挑毛病。

> **問題背景**:舊合約只逼 Codex 給 verdict。實測結果是它會回「§2 缺投影片派工路徑、§6 缺影音閘門」這種純清單,零實作。同一題目換成下面的合約後,回來的是可直接貼進 SKILL.md 的條文 + 分數曝險量化 + 它自己方案的代價 + 它自己最弱環節的自我攻擊。

```text
NEW OUTPUT CONTRACT - for each finding:
  Fn: the gap or defect, one line
  SEVERITY: HIGH | MEDIUM | LOW - and what it concretely costs if unfixed
  ALT: MANDATORY. The concrete replacement text or rule, written so it can be
       pasted in as-is. Name where it goes. If you cannot write a usable rule,
       you MUST downgrade the finding to a QUESTION and say what you are unsure
       about - you are NOT permitted to leave a gap open with no proposal.
  COST: what YOUR OWN proposal costs - tokens, wall-clock, added process burden,
        or what it trades away. Be honest about the downside of your own idea.
Then:
  SELFCHECK: 2 lines. Which of your own ALT proposals is weakest, and why a
             reviewer should push back on it.
```

附加規則,寫進 prompt:

```text
If you REJECT something but cannot offer an executable alternative, downgrade to
CHALLENGE and state what you are uncertain about.
```

### ⚠️ 副作用:Codex 提方案就變成產出者

一旦 Codex 出方案,**它就不能當那個方案的驗收者**(SKILL §1 鐵則 7「驗證不自驗」/ §6 R-獨立)。配套:

- Codex 提的方案被採用 → 另派一個乾淨的 Claude agent 查一遍;
- 或在交付時明說「這條未經獨立核對」。

**目前未驗清單**:(空)。原本列的「SKILL §8 預先扣額度機制」(Codex 第四輪自己提的,2026-07-25)已在 2026-11-11 隨 1.5M 總預算一起作廢。

## 6. Codex 能力邊界(必讀,2026-07-25 實查)

| 能做 | 做不到 |
|------|--------|
| 讀 repo 內外任何文字檔(danger-full-access) | **播放影片 / 聽音訊** |
| 逐字核對數字、日期、ID、引用 | 判斷圖表美感、口說聽感 |
| 跨文件矛盾掃描 | 寫檔(政策上禁止,非能力限制) |
| 重新推導統計方法有效性 | 驗收自己提出的方案(見 §5.1) |
| 讀渲染後的 PDF / 逐頁圖 | 從原始 .pptx 判斷實際播放效果 |

**影音驗收因此不能外包給 Codex。** 走 `/watch` skill(yt-dlp + ffmpeg + 逐字稿)+ ffmpeg `volumedetect`,最後人耳確認留 Kenny —— 見 [a3-pitch-gates.md](a3-pitch-gates.md)。

## 7. Fallbacks

- Codex 連兩趟異常(非 timeout)→ 停,實查 `codex --version`、config.toml 的 model、登入狀態,更新 SKILL §0 表,不瞎猜重試。
- npm 版打不動(400「requires a newer version」)→ 改叫 Codex 桌面 App 內建 CLI:路徑讀 config.toml 的 `CODEX_CLI_PATH`(`<hash>` 會變,不要寫死),寫法 `$prompt | & $cli exec ...`。
- Codex 不可用(額度滿等)→ 改派 fresh Claude agent(非產出者;sonnet high,核心內容用 opus high);交付時**寫明哪部分只有 Claude 驗過**、「未經異家族核對」。
- 互動式備援:Kenny 自己跑 `codex`(TUI)貼 prompt。

## 8. 環境漂移紀錄(由新到舊;原本擠在 SKILL §0 的表格裡,2026-11-11 搬來)

- **2026-11-11 Win**:config = `gpt-6.1-sol` / effort `high` / `priority`。npm 版 `codex` **0.162.1**,預設設定 smoke EXIT=0。桌面版 CLI 0.167.0-alpha.3.2(`CODEX_CLI_PATH` = `...\Codex\bin\f71a721e0e6193a9\codex.exe`)。xhigh 在這個型號上沒重測。
- **2026-09-16**:額度恢復後平行重跑 R2/R3,兩趟跑到 70,454 / 92,948 token 又滿(重置 9/17 00:40)→ 改派 fresh Claude agent(非產出者)當驗收者,交付時標明哪些部分只有 Codex 驗過、哪些只有 Claude agent 驗過。
- **2026-09-15 Win**:config 預設模型變 `gpt-6-astra`(effort `xhigh`、`priority`)。PATH 上的 npm 版 `codex` = 0.147.0,打 `gpt-6-astra` 回 **400「requires a newer version of Codex」→ 背景兩趟全損**。解法(不安裝、不改設定):改叫桌面 App 內建 CLI(當日 `...\Codex\bin\12219cbfbcbddde7\codex.exe`,0.154.0-alpha.6.2,smoke EXIT=0)。npm 最新版當日為 0.154.0。來源檔名含中文時先複製成 ASCII 檔名到 scratchpad(附 sha256 對賬)再交給 Codex。
- **2026-09-15 同日撞用量上限**:xhigh 共 4 趟(R1 兩趟完成,各 82,875 / 90,320 token;R2、R3 平行跑到 45,498 / 32,086 token 時中斷),回「You've hit your usage limit」,重置 2026-09-16 02:41 —— **大件多輪審查別一次平行開太多趟,R1 失敗重跑的趟數也要算進去**。
- **2026-08-02 Win**:codex-cli 0.146.0,gpt-5.6-sol。當時 config 只有 sandbox 與 trust_level、**沒設 effort,預設 `reasoning effort: none`** → 每趟要自己加 `-c model_reasoning_effort="xhigh"`(實測生效,EXIT=0)。**之後 config 已有 effort 設定,這條改成:開跑前看一眼 config 的 effort 是不是你要的。**
- **2026-08-02 Win(PATH,經獨立稽核更正)**:codex 裝在 `%APPDATA%\npm\codex.cmd`,該路徑本來就在持久化的 User PATH 裡,全新開的 shell 直接叫得到。真正的坑是**安裝之前就已啟動的行程**(Claude Code session、開著的終端機 / VS Code)拿的是舊環境區塊。在那種 session 裡用 `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')` **重讀 registry**,不要再 append 一次 —— 這是「行程過期」不是「PATH 沒設」。
- **2026-07-26 Mac**:`/opt/homebrew/bin/codex`(0.144.6),`cat prompt.txt | codex exec --sandbox danger-full-access -o out.md`,**中文 prompt 無亂碼**;一趟 6 個複合 CLAIM + 讀 3 個檔(744 行)EXIT=0 未 timeout。§3 的「必須 PowerShell / 純 ASCII」是 Win 機專屬限制,Mac 不適用。
- **2026-07-22**:旗標改 `--sandbox danger-full-access`(Kenny 指示,見 §3)。
