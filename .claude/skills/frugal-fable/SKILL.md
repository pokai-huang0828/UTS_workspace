---
name: frugal-fable
description: Fable 治理框架(自 MiTAC-VMX 移植)— 主模型當指揮官,派工給 Claude subagents 生產、Codex(gpt-5.6 異家族)對抗驗證的多代理協作架構。多步驟任務、批次讀檔、事實類交付、需要第二意見時使用。
---

# Fable 指揮官手冊(UTS_workspace 版)

> 移植自 `MiTAC-VMX/.claude/governance/`(Fable 撰寫,v2 2026-07-09),2026-07-16 移植並針對本機實查。
> 原始 6 檔 + VMX Codex 配方逐字保存在 [references/](references/)(見其 README 的適用性說明)。
> 讀者 = 任何等級的主模型(含 Sonnet/Haiku);規則可執行、有判準,不確定時照字面做。

## 0. 本環境實查表(2026-07-16,Win 機 `C:\Users\kenny`)

**派工報 model/參數/閘門錯誤時,第一動作 = 重查該工具 schema 並更新本表(附日期),禁止瞎猜繞過**(R-漂移,見 [02](references/02-judgment-rubrics.md))。

| 通道 | 可用值 | 備註 |
|------|--------|------|
| Agent tool `model` | `haiku` / `sonnet` / `opus` / `fable` | 無 effort 參數;subagent 預設背景執行,完成自動通知;續問同一 agent 用 SendMessage,不重派 |
| Agent tool `subagent_type` | `Explore`(只讀)/ `Plan` / `general-purpose`(全工具) | 未指定 = general-purpose;plugin agents(carta/nimble…)與本 repo 無關,不用 |
| Workflow 腳本 | `agent()` 支援 model + effort(low→max) | ⚠️ 需明確授權:Kenny 說「ultracode」或明確要求「用 workflow」才可呼叫;曖昧說法 → 改同一則訊息平行發多個 Agent |
| Codex CLI | **gpt-5.6-sol**(codex-cli 0.144.5,effort xhigh) | **2026-07-22 起(Kenny 指示)不用 sandbox:`--sandbox danger-full-access`**,可直接讀 repo 外路徑(scratchpad 等;smoke PASS)。驗證任務仍在 prompt 裡約束 read-only 行為,跑完 `git status` 驗。⚠️ ChatGPT 帳號下裸名 `gpt-5.6` 無效,5.6 系列 = `-sol`(旗艦)/`-terra`/`-luna` 三變體,三者皆實測可用。配方見 [references/codex-collab.md](references/codex-collab.md) |
| 主迴圈 | session 當下模型(不可自選) | — |

## 1. 六條鐵則

1. **指揮官不下場**:大量讀取(>2 個長檔)、掃 repo、查網頁、批次改檔 → 派 subagent,主對話只收結論。判準:正要連續 Read 第 3 個 >200 行的檔案 = 停,改派工。
2. **機械工作用最便宜的模型**:格式盤點/路徑清查/逐字抽取 → `haiku`(Explore)或 `sonnet`(要寫檔)。判準:「有沒有標準答案?」有 → 便宜模型;要權衡 → 高階。
3. **派工三件套**,缺一不派:①目標與動機 ②驗收條件(可檢查) ③回報格式。模板照抄 [03](references/03-prompt-templates.md)。
4. **回報合約**:subagent 第一行 = 一句話 TL;DR;之後只有「結論 + 檔案:行號」;長產物(>50 行)落檔回傳路徑,不回貼全文。
5. **先試跑再放量**:新型任務先派 1 個最小樣本,驗收格式與耗時 OK 才批次(實案:Codex 10 claims 一包連兩次 timeout,拆 2–3 條後一次過)。
6. **驗證不自驗**:產出者不當驗收者 — 檔案 read-back;程式實跑貼 exit code;事實類文件 → fresh agent 或 **Codex 異家族**核對;高風險判斷 → 第二意見。

## 2. 派工對照表

| 任務型態 | 派給 |
|----------|------|
| 找檔案/盤點/路徑清查 | Agent(Explore, haiku) |
| 消化長檔/逐字稿成摘要 | Agent(Explore, haiku;要取捨判斷 sonnet) |
| 逐字抽取/初稿轉換 | Agent(general-purpose, sonnet) |
| 跨檔重構/批次改檔 | Agent(general-purpose, sonnet;高風險 opus) |
| 開放式研究/多來源彙整 | Agent(general-purpose, sonnet 起步) |
| 審查/驗證(事實核對、規則打架) | fresh Agent(sonnet)或 **Codex(read-only)** |
| 主迴圈能力不足的判斷題 | 往上派:Agent(opus;不夠再 fable)— 弱指揮官可以派比自己強的專家 |
| 對外定稿/不可逆動作/裁決 | 主迴圈 + Kenny(唯一該下場的事) |

## 3. 升降級路徑

- haiku 錯 1 次 → 直接升 sonnet(不給第二次)。
- sonnet 同一子任務連錯 2 次 → 帶完整失敗軌跡升 opus 或收回主迴圈;不第三次原樣重派。
- 高階解出模式後 → 整理成「可照抄步驟」降級批次套用。
- 同一件事最多重試 2 輪;第 3 輪 = 換方法或升級。
- Codex timeout(~10 分鐘)= 拆小任務,不是換模型。
- 「錯」的定義:驗收未過、缺必答欄位、引用不存在的路徑/ID、或驗收者打回。格式醜但內容對 ≠ 錯。

## 4. 並行紀律

- 互不依賴的派工在**同一則訊息**一起發;有依賴的等結果再派。
- 已委派的搜尋,主迴圈不自己再做一次(雙倍燒 token)。
- 同時在跑的 background agent ≤3。
- 兩個 agent 不碰同一批檔案;會碰 → 串行或 `isolation: "worktree"`。

## 5. Agent × Codex 兩腦協作架構

核心:**Claude 生產、Codex(異家族)驗證** — Codex 抓到的錯全是「Claude 沿用自己舊筆記」型,自驗永遠抓不到(VMX 實錘)。完整配方與模板見 [references/codex-collab.md](references/codex-collab.md)。

```text
指揮官(主迴圈)
 ├─ 生產線:Explore(haiku)搜 → general-purpose(sonnet)寫 → opus/fable 判斷題
 ├─ 驗證線:fresh Claude agent 對抗審查(03 §審查)
 │          └─ 事實類 ≥10 claims → 加開 Codex 異家族複核(2–3 claims/趟)
 └─ 裁決:主迴圈整合 → 對外/不可逆 → Kenny
```

第二意見管道排序:**Codex(異家族)> fresh opus/fable agent > 明說「這題需要 Kenny/高階模型」**。

## 6. 判準速查(完整版見 [02](references/02-judgment-rubrics.md))

- **R-完成**:交付必附證據四選一(命令輸出/read-back/對賬數字/第二意見),沒有證據不得說「完成」。
- **R-問人**:只有四類該問 — 花錢/對外/不可逆、架構級分歧、指示互相矛盾、憑證只有 Kenny 有;其餘選預設+標「⚠️假設」。
- **R-換路**:被打斷 ≥2 次且是重定向、同一錯誤重現 2 次、第 3 個 edge case 補丁、驗證過但不是要的 → 停手換路。
- **R-回讀**:用 Kenny 給的日期/ID/數字前,第一句先回讀關鍵值。
- **R-漂移**:工具與規則打架 → 實查 schema、更新本檔 §0、附日期,才繼續。

## 7. 交付前 60 秒 checklist

```text
□ 列舉型 → 來源 N = 輸出 N?差額有解釋?
□ 關鍵數字/日期/ID 與來源逐字對過?
□ 完成宣稱:有 R-完成 四種證據之一?
□ 每個新檔 read-back 過?
□ 對外內容:個資已 strip?語言 = 繁體中文(Kenny 偏好)?
```

## references/ 清單

| 檔案 | 內容 |
|------|------|
| [README.md](references/README.md) | 移植來源與適用性(哪些 VMX 條目在本 repo 不適用) |
| [00-diagnosis.md](references/00-diagnosis.md) | VMX 原檔:harness 漏 token/失焦/出錯 前三名診斷 |
| [01-model-dispatch.md](references/01-model-dispatch.md) | VMX 原檔:模型調度守則(本 SKILL §0–§4 的母本) |
| [02-judgment-rubrics.md](references/02-judgment-rubrics.md) | VMX 原檔:R-升級/完成/問人/換路/回讀/新開/漂移 全文 |
| [03-prompt-templates.md](references/03-prompt-templates.md) | VMX 原檔:六型派工模板(搜尋/摘要/實作/重構/研究/審查) |
| [04-maintenance-protocol.md](references/04-maintenance-protocol.md) | VMX 原檔:治理檔維護權限與教訓登記簿 |
| [05-letter-to-future-sessions.md](references/05-letter-to-future-sessions.md) | VMX 原檔:給未來 session 的信(制度退化模式與預防) |
| [codex-collab.md](references/codex-collab.md) | **本機版** Agent×Codex 協作架構 + 已實測駕駛配方 |
| [codex-driving-vmx-machine.md](references/codex-driving-vmx-machine.md) | VMX 公司機原版配方(CLM 三陷阱;本機不適用,留作對照) |
