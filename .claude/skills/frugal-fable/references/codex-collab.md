# Agent × Codex 兩腦協作架構(UTS_workspace・Kenny 個人 Win 機)

> 2026-07-16 本機實測撰寫;母本 = VMX `codex-driving.md`(公司機版,見 [codex-driving-vmx-machine.md](codex-driving-vmx-machine.md))。
> 本機環境:codex-cli **0.144.5**,model **gpt-5.6-sol**,已 `codex login`,reasoning effort xhigh(config:`~/.codex/config.toml`)。
> ⚠️ 型號命名(2026-07-16 實查):ChatGPT 帳號下裸名 `gpt-5.6` 會 400;5.6 系列實際名稱 = `gpt-5.6-sol`(旗艦,官方描述「most ambitious work」)/ `gpt-5.6-terra` / `gpt-5.6-luna`,三者皆實測 EXIT=0。可用型號清單可從 CLI 二進位撈:`grep -oaE "gpt-5[a-z0-9.\-]*" <codex.exe> | sort -u`。

## 1. 為什麼要兩腦

Codex(OpenAI 家族)與 Claude 的**失誤模式不同**。VMX 實錘:Codex 抓到的錯全是「Claude 沿用自己舊筆記/舊 context」型——這類錯 Claude 自驗(包括 fresh Claude agent)有共同盲點。因此:

- **事實類交付 ≥10 條 claims**(數字、日期、路徑、引用)→ 必開 Codex 複核。
- 小事(<10 claims、格式類)→ fresh Claude agent(sonnet)就夠。
- 品味/模糊判斷(對外語氣、要不要做)→ 兩腦都補不了,照 R-問人 交 Kenny。

## 2. 角色分工(架構圖)

```text
┌─ 指揮官:主迴圈(session 模型)──────────────────────────┐
│  拆解任務、選模型、發派工三件套、收 TL;DR、整合裁決          │
└──────────────┬───────────────────────────┬───────────────┘
               │ 生產線(Claude 家族)         │ 驗證線(異家族)
   ┌───────────▼───────────┐   ┌───────────▼───────────┐
   │ Explore(haiku)搜索/盤點 │   │ fresh Claude agent      │
   │ general-purpose(sonnet) │   │  對抗審查(03 §審查)      │
   │  實作/轉換/研究           │   │ Codex(gpt-5.6, read-only)│
   │ opus / fable 判斷題往上派  │   │  事實核對 2–3 claims/趟   │
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
$prompt | codex exec --sandbox read-only -o $out
Write-Output "EXIT=$LASTEXITCODE"
Get-Content $out
```

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

1. **拆小**:每趟 2–3 條 claims;10 條一包 = 連兩次 10 分鐘 timeout 全損(VMX 2026-07-03 實案)。單趟目標 <8 分鐘。
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

## 6. Fallbacks

- Codex 連兩趟異常(非 timeout)→ 停,實查 `codex --version`/登入狀態,更新 SKILL §0 表,不瞎猜重試。
- Codex 不可用 → 第二意見降級:fresh opus/fable agent(往上派);再不行 → 明說「未經異家族核對」。
- 互動式備援:Kenny 自己跑 `codex`(TUI)貼 prompt。
