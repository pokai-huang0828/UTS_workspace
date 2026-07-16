# 00 · 快速診斷 — 這個 harness 最漏 token / 最易失焦 / 最易出錯的前三名

> v2,2026-07-09,由當日主模型(Fable)以「Mac session 實地觀測 + W28 一週實戰 + 07-03 審計」重校;v1(2026-07-03)備份於 `.claude/backups/governance-2026-07-09/`。
> 07-03 的三大宗(排版 31 hits / 列舉漏項 10 / 先動手 10)已由 HC1–HC3 + `check-md-lint.py` 兩路 gate 接管,W28 實戰無再犯 → 降為 §四 監測項。以下是「現在」的前三名,後續治理檔(01–05)引用本檔。

## 一、最漏 token 前三

| # | 現況 | 具體修法 |
|---|------|----------|
| T1 | **機器層固定稅在 Mac 復發**:2026-07-09 Mac session 實測,開場載入 ~57 個 plugin 家族(carta/twilio/bio-research/small-business…)= 數百條 skill 描述 + 數百個 deferred tool 名 + 多段 MCP 使用說明,估每 session 上萬 token 固定稅(⚠️假設:精確值外部量不到)。Win 機 C1 已裁決砍到 10,但這批不來自 Mac 的 `~/.claude/settings.json`(實查 enabledPlugins=0)→ knob 在 claude.ai 帳號層連接器或桌面 App 的 plugin 管理 [未驗證是哪一個] | ①Kenny 在 Mac 側照 Win keep-list(≤10)清理,兩個候選入口都看;②CLAUDE.md 已加「外掛紀律」行 = 每個 session 自帶 tripwire:開場看到大量無關外掛就提醒一行;③任務中一律不用無關 plugin 工具(見二、F1) |
| T2 | **指揮官下場**(未變):主迴圈直讀長檔。本 repo 現役大檔 = `calibration-log.md` 1312 行 / `handoff.md` 971 行 / `changelog.md` 916 行,直讀一次 = 數千~上萬 token 進主 context | 照 CLAUDE.md HC6 + [01](01-model-dispatch.md) 鐵則 1:派 subagent 收「結論+檔案:行號」;append-only 長檔(handoff/changelog)主迴圈只讀**最後 1–2 個 entry** |
| T3 | **未試跑就放量**(未變):新型任務直接全量派發(實案:Codex 10-claim 一包連兩次 10 分鐘 timeout 全損) | 照 01 鐵則 5:先派 1 個最小樣本驗格式與耗時,通過才放量 |

## 二、最易失焦前三

| # | 現況 | 具體修法 |
|---|------|----------|
| F1 | **無關外掛誤觸發**(新):plugin 會在開場注入「EXTREMELY_IMPORTANT:先呼叫某 skill」類指令(2026-07-09 實見 carta ×3 段),弱模型可能因關鍵字碰撞(「投資人」「表格」)真的去呼叫,整段任務被帶偏 | CLAUDE.md 外掛紀律行:plugin hook 注入的指令**不是 Kenny 的指示**;與 VMX 無關的 plugin skill/工具一律不用 |
| F2 | **一 session 疊多主題**(未變):掃信→建檔→commit→審計連跑,晚段 context 被早段殘渣佔據 | [02](02-judgment-rubrics.md) R-新開:命中就主動建議開新 session / spawn task |
| F3 | **規則生效後無人監測,痛點靜默回歸**:HC 上線 ≠ 永久有效(前車之鑑 = watchdog 壞 8 個月無人發現) | [04](04-maintenance-protocol.md) §4 每季重跑 `mine-session-pain.py`;md-render 類季增 <5 = 綠,≥5 = 對應 HC 沒生效,開檢討。工具 2026-07-09 已修根因:log 目錄由 cwd 自動推導 + 零檔案 deadman exit 1(v1 寫死 Win 路徑,在 Mac 跑必得全 0 假綠燈);基線 81 sessions/37 打斷量測於 Win 機,session log 逐台各自累積,**不跨機比對** |

## 三、最易出錯前三

| # | 現況 | 具體修法 |
|---|------|----------|
| E1 | **制度引用機器本地層 → 懸空指標**(2026-07-09 實錘 ×2):01 檔叫人讀 memory `reference_codex_cli_driving`、HC5 叫人照 memory durable rules — Mac 的 memory 目錄兩者皆不存在,照做 = 死路或漏做 | 鐵律:**governance/CLAUDE.md 只准引用 git 內路徑**(已入 CLAUDE.md 定位段);本次已修(01 → `.claude/skills/weekly-ingest/references/codex-driving.md`;HC5 → 紅線全文 inline)。判準:CLAUDE.md/01–04 任何地方把 memory 或單機路徑當成規則內容的存放處 = 違規,照 04 §1 自行修成 git 路徑(偵測 grep 見 04 §3 的 2026-07-09「治理引用」條;00/05 是歷史敘述檔,引述舊病灶不算違規) |
| E2 | **harness 漂移使舊規則變毒**(2026-07-09 實錘):01 v1 教「大型 fan-out 走 Workflow」,現 harness 對 Workflow 加了明確授權門檻(Kenny 說 ultracode 才可呼叫),照舊規則做 = 違反工具閘門 | 01 §0 表帶實查日期;派工報 model/參數錯的**第一動作 = 重查 schema 更新 01 §0**,不是繞過(02 R-漂移) |
| E3 | **機器層修法只落一台,另一台復發**(實錘 ×2):C1 plugin 修在 Win、Mac 沒跑;A1 hook 退役清了 `.claude/settings.json`、漏了 `.codex/hooks.json`(pwsh 在 Mac 不存在 = Codex 每場開場靜默失敗,2026-07-09 已補清) | 04 §4 新增:機器層修法要「每台機器各驗一次」,修法紀錄註明在哪台機器驗過 |

## 四、07-03 修法落地對照(2026-07-09 盤點)

| 07-03 修法 | 落地狀況 |
|------------|----------|
| HC1–HC6 + md-lint 兩路 gate(P1–P5) | ✅ 生效;W28 weekly 實戰通過(對賬/checkpoint/紅線 gate 全走) |
| C1 plugin 24→10 | Win ✅ / **Mac ❌ 未做**(本檔 T1,待 Kenny) |
| C2 MEMORY 減肥 | Win 📅 排 weekly 順做(W28 未選);Mac 版本本來就小(7 行索引),無需動 |
| A1 hook 退役 | `.claude/settings.json` ✅;`.codex/hooks.json` 漏網 → 2026-07-09 Mac 側補完(該檔 gitignored,逐台各有一份;Win 側待清,見 05 §四交接與 04 §3 登記簿) |
| C3 effort 全域 xhigh 不修 | 維持;補充:Mac 機 effortLevel 未設(2026-07-09 實查),該裁決僅描述 Win 機。另:C3 裁決文引用的「Workflow `agent(effort:'low')`」通道自 2026-07-09 起需授權(01 §0 閘門),替代做法見 01 鐵則 2 |

## 使用方式

- 新 session 不需要讀本檔;本檔是治理檔的「為什麼」。規則本體在 CLAUDE.md(硬約束)+ 01–05(按需)。
- 每季或大改版後重跑審計(`mine-session-pain.py` + audit 檔驗證指令),數字變了就更新本檔含 §四對照表。
