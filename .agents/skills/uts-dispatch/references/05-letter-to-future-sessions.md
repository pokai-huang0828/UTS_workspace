# 05 · 給未來 session 的信

> v2,寫於 2026-07-09,作者 = 當日主模型(Fable),讀者 = 之後任何等級的主模型(多數時候是 Sonnet/Opus/Haiku)。
> 前信(2026-07-03,同為 Fable 所寫,備份 `.claude/backups/governance-2026-07-09/`)的三件事**全部仍成立**,一行各濃縮如下;本版加上只有 2026-07-09 這個 session 才看得到的三件新事。

## 〇、前信三件事(仍有效,濃縮保留)

1. **頭號日常風險是「表面不同步」**:一個事實活在 .md → mirror → 三索引 → MEMORY → handoff 五個地方;build.py 吃掉中間三個,MEMORY/handoff 靠自律。改完任何事實,問「MEMORY.md 有沒有一句話現在變成錯的?」
2. **Kenny 的打斷是 steering,不是否定**(37 次/81 sessions):停手 → 一句話確認新方向 → HC3 給 ≤3 行計畫;不要解釋剛剛為什麼那樣做,不要硬塞半成品。
3. **兩腦驗證有實錘**:Codex(異家族)抓到的錯全是「Claude 沿用自己舊筆記」型,自驗永遠抓不到。事實類交付 ≥10 條 claims 開 Codex;小事 fresh sonnet 就夠。

## 一、三件 Kenny 沒問、但對這個環境最重要的事(2026-07-09 版)

**1. 這個 repo 是 public 的,裡面是真的內部資料 — 這是全環境最高優先的未決事項。**
2026-07-09 `gh repo view` 實查 = **PUBLIC**(`github.com/pokai-huang0828/MiTAC-VMX`)。repo 內有 357 張 Jira 票的 snapshot(2026-07-07 快照)、客戶案件(Honeywell/Azuga/Mapon…)、會議紀錄;而 HC5 卻在小心翼翼防止 Jira key 洩進「對外 email」— 前門上鎖、後門敞開,威脅模型自相矛盾。memory 早在 23 天前就標了 open item,至今未裁決。**每個接手 session 該做的**:①寫入任何新內容前,當作陌生人看得到(已入 CLAUDE.md 公開倉注意行);②在合適時機(週會/weekly-ingest 收尾)把這題端給 Kenny 裁決:轉 private(最簡),或留 public + 系統性去識別化(工程大,不建議)。裁決前不催第二次,但別讓它掉出視野。

**2. 這套制度只在 git 裡活得下去 — 機器本地層的一切終將漂移。**
本 session 實錘三件:C1 plugin 修在 Win、Mac 復發(~57 個 plugin 家族的開場稅);01/HC5 引用的 memory 檔在 Mac 不存在(懸空指標 ×2);A1 hook 退役漏了 `.codex/hooks.json`。歸納成一條判準:**寫規則時引用了 repo 外的東西,這條規則在別台機器就是死的**;機器層修法沒有逐台驗過就不算結案(04 §4 第 5 點)。你接手時若發現「治理檔說的」和「機器上看到的」不一致 → 照 02 R-漂移:實查、更新、附日期,別默默繞過。

**3. 資料層的下一步是「結構化 spine」,不是更多散文。**(回 Kenny 被中斷的那個問題:repo 還能怎麼優化 — 資料庫/流程/儲存)
現況已經對:md = SSOT、build.py 7-gate、jira_data 有 JSON snapshot、validate-meta 47/0。按 Kenny「治本(可重跑工具)優於治標」的偏好,價值排序後的三個方向(都是**方向**,動工前照 HC3 先給計畫):
①**case 狀態機進 front-matter**:case-learning 檔的 meta 補 `status(open/monitoring/closed) + owner + next_review`,讓 W28 那種 lifecycle-close 候選掃描(mapon-qa17/honeywell/connectsource)從「Explore 建議」變成腳本輸出;
②**Jira audit-diff 固化成 repo script**:兩份 JSON snapshot 的 diff 邏輯目前每次由 Codex 重推,W26/W28 兩次 removed-membership regex 誤抓就是根源(04 §3 已記)— 寫成 `.claude/scripts/` 可重跑工具 + cross-ref 排除,兩腦驗證改驗「script 輸出」而非「重算」;
③**append-only 長檔做季度歸檔**:handoff.md(971 行)與 changelog(916 行)是唯二只增不縮的檔,沿用各內容夾 `archive/` 慣例,每季把舊 entry 移 `archive/`,主檔保最近一季(handoff 歸檔 = 修訂 AGENTS.md §3「只能 append」條款,屬 only-Kenny 級:先拿裁決、同步改 AGENTS.md、知會 Codex,三者缺一不動工)。

## 二、這套制度最可能的退化方式(+預防)

| # | 退化模式 | 早期症狀 | 預防(已內建) |
|---|----------|----------|----------------|
| 1 | **硬約束通脹**:每踩一坑加一條,弱模型全部略讀 = 形同沒有 | CLAUDE.md 出現第 8 條 HC 或 >60 行 | 行數上限([04](04-maintenance-protocol.md) §2);加一條必刪/下放一條 |
| 2 | **治理檔變擺設**:寫完沒人執行(前車之鑑:watchdog 壞 8 個月無人發現) | 連續 3 個 session 沒人引用 HC 編號;audit 驗證指令超過一季沒重跑 | 04 §4 每季重跑;檢查器必須有 deadman 自檢 |
| 3 | **裁決積壓**:待決清單變殭屍 | audit 檔超過 30 天無變動 | 04 §5:30 天未裁決自動歸檔「暫不修」 |
| 4 | **假設漂移**:型號表/工具閘門過時,照表派工報錯(**已兌現一次**:Workflow ultracode 門檻,2026-07-09 修) | 派工報 model/參數/授權錯誤 | 表格帶實查日期;02 R-漂移:報錯第一動作 = 重查更新,不是繞過 |
| 5 | **登記簿只寫不吸收** | 04 §3 超過 20 條 | 04 §2 門檻:同因合併、提案進 02 |
| 6 | **機器層漂移**(新):修法只落一台,另一台悄悄復發 | 同一個問題在換機後重現;開場外掛數又爆 | 04 §4 逐台驗 + CLAUDE.md 外掛紀律 tripwire;修法紀錄註明驗於哪台 |

## 三、誠實條款(harness 極限,別假裝)

- 這套制度補得了:**執行品質**(拆解、對賬、驗證、格式、成本紀律)— 靠 HC + 01 派工 + 02 rubric + 03 模板 + fresh-context 驗收,Sonnet 等級可完整執行。
- 補不了:**品味與模糊判斷**(對外語氣、政治敏感度、「這個要不要做」)。遇到 → 02「Harness 極限」的三步:R-問人 → 第二意見管道(Codex > 往上派 opus/fable > 明說做不到)→ 標註「未經人核」。
- 前信警告「未經時間考驗」— 一週後部分兌現:漂移真的發生了(Workflow 閘門、機器層復發),但 HC1–HC3 在 W28 實戰撐住了。**制度活性靠 04 §4 季檢,不靠信仰。**

## 四、交接 — 本次(2026-07-09)未完成、留給之後的 session

- **C1-Mac**:Mac 側 plugin 清理待 Kenny 手動(knob 在 claude.ai 連接器設定或桌面 App plugin 管理,[未驗證是哪個];keep-list 參考 Win 裁決 ≤10)。每個 session 的 tripwire 已入 CLAUDE.md。
- **C2-Win**:Win 機 MEMORY.md 減肥,仍排 weekly-ingest 順做(W28 未選)。
- **A1-Win 殘尾**:`.codex/hooks.json` 是 gitignored 機器本地檔;Mac 側 2026-07-09 已清空,Win 機同檔大概率仍掛 pwsh watchdog(A1 同款)→ 下次在 Win 機跑 `grep -c "pwsh" .codex/hooks.json`,非 0 就照 Mac 做法清成 `{"hooks": {}}`。
- **public repo 裁決**:見本信第一件事,Kenny 決策。
- **`.agents/skills/vmx-hub-freshness-audit/`** 疑似 `.claude/skills/` 的重複鏡像 [未確認用途,可能供 Codex 讀] → 下次遇到再查清,別直接刪。
- 本版治理檔經雙重對抗審查:fresh-context Claude agent(初判 FAIL+14,已逐條修正,含季檢工具假綠燈根因修復)+ Codex 異家族兩輪複核(抓到 python/python3 runner 陷阱與工具邊界 bug,處置見 handoff.md 2026-07-09 NOTE)。HC5 指標修復、CLAUDE.md 新增三句、01/02/03 措辭微調 **待 Kenny 追認**(清單在 CLAUDE.md 遷移紀錄)。
