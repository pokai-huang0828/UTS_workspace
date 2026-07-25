---
name: uts-dispatch
description: 指揮官派工守則(UTS_workspace)— 主模型當指揮官,派工給 Claude subagents 生產、Codex(gpt-5.6 異家族)對抗驗證。多步驟任務、批次讀檔、事實類交付、需要第二意見時使用。
---

# 指揮官手冊(UTS_workspace 版)

> 前身 = `frugal-fable`(移植自 MiTAC-VMX,Fable 撰寫 v2 2026-07-09)。
> **2026-07-25 改版**:Opus 5 上線,經 Fable 5 立場書 + Codex gpt-5.6-sol 四輪對抗(最終 READY)後改寫 §0/§2/§3/§5/§6/§7,新增 §8。
> 原始 6 檔 + VMX Codex 配方逐字保存在 [references/](references/)。
> 讀者 = 任何等級的主模型;規則可執行、有判準,不確定時照字面做。

## 0. 本環境實查表

**派工報 model/參數/閘門錯誤時,第一動作 = 重查該工具 schema 並更新本表(附日期),禁止瞎猜繞過**(R-漂移,見 [02](references/02-judgment-rubrics.md))。

| 通道 | 可用值 | 備註 |
|------|--------|------|
| Agent tool `model` | `haiku` / `sonnet` / `opus` / `fable` | 無 effort 參數。**2026-07-25 實查:`opus` = `claude-opus-5`,與主迴圈同型號**,派它不是「比較強」,是 context 乾淨 / 可平行 / 可 worktree 隔離 |
| Agent tool `subagent_type` | `Explore`(只讀)/ `Plan` / `general-purpose`(全工具) | 未指定 = general-purpose |
| Agent 執行模式 | 預設背景執行;`run_in_background: false` 同步 | **2026-07-25 實測**:要收結論才能繼續的派工用同步,比背景+通知少一次往返 |
| Workflow 腳本 | `agent()` 支援 model + effort(low→max) | ⚠️ 需明確授權:Kenny 說「ultracode」或明確要求「用 workflow」才可呼叫;曖昧說法 → 改同一則訊息平行發多個 Agent |
| Codex CLI | **gpt-5.6-sol**(codex-cli 0.144.5,effort xhigh) | `--sandbox danger-full-access`(2026-07-22 起,Kenny 指示)。**2026-07-25 實測:一趟吃 5 個複合命題 + 讀 3 個檔案,EXIT=0 未 timeout** —— 舊表「每趟 2–3 claims」是 gpt-5.5 時代的數字,已放寬。配方見 [codex-collab.md](references/codex-collab.md) |
| Codex 能力邊界 | **播不了影片/音訊** | A3 影音驗收不可外包給 Codex,見 §6 R-A3 |
| 主迴圈 | session 當下模型(不可自選) | 2026-07-25 起 = Claude Opus 5 |

### 0.1 費率表(排相對貴度用,不用來算錢)

| 模型 | input / output(每百萬 token) | 相對 |
|------|------|------|
| Fable 5 | $10 / $50 | Opus 5 的 **2 倍** |
| Opus 5 | $5 / $25 | 基準 |
| Sonnet 5 | $3 / $15 | 0.6× |
| Haiku 4.5 | $1 / $5 | 0.2× |

**⚠️ 換不成錢**:Agent tool 只回一個 `subagent_tokens` 總數,拆不出 input / output / cache-read / cache-write。因此 §8 預算一律**以總 token 計價**,費率表只用來排「誰比較貴」——Fable 對 Opus 是雙向兩倍,這個排序不受拆分方式影響。

## 1. 六條鐵則

1. **指揮官不下場**:大量讀取(>2 個長檔)、掃 repo、查網頁、批次改檔 → 派 subagent,主對話只收結論。判準:正要連續 Read 第 3 個 >200 行的檔案 = 停,改派工。
2. **機械工作用最便宜的模型**:格式盤點/路徑清查/逐字抽取 → `haiku`(Explore)或 `sonnet`(要寫檔)。判準:「有沒有標準答案?」有 → 便宜模型;要權衡 → 高階。
3. **派工三件套**,缺一不派:①目標與動機 ②驗收條件(可檢查) ③回報格式。**再加 §8 的 scope 上限。** 模板照抄 [03](references/03-prompt-templates.md)。
4. **回報合約**:subagent 第一行 = 一句話 TL;DR;之後只有「結論 + 檔案:行號」;長產物(>50 行)落檔回傳路徑,不回貼全文。
5. **先試跑再放量**:新型任務先派 1 個最小樣本,驗收格式與耗時 OK 才批次。
6. **驗證不自驗**:產出者不當驗收者。**自檢可以提供客觀完成證據(命令輸出、檔案 read-back、對賬數字),但永遠不滿足「需要獨立驗證」的要求 —— 這是兩件事**(見 §6 R-獨立)。事實類文件 → fresh agent 或 **Codex 異家族**核對;高風險判斷 → 第二意見。

## 2. 派工對照表

| 任務型態 | 派給 |
|----------|------|
| 找檔案/盤點/路徑清查 | Agent(Explore, haiku) |
| 消化長檔/逐字稿成摘要 | Agent(Explore, haiku;要取捨判斷 sonnet) |
| 逐字抽取/初稿轉換 | Agent(general-purpose, sonnet) |
| 跨檔重構/批次改檔 | Agent(general-purpose, sonnet;高風險 opus —— 理由是 context 乾淨可隔離,不是比較強) |
| 開放式研究/多來源彙整 | Agent(general-purpose, sonnet 起步)+ **必附 §8 scope 上限**(這類是本框架最大燒錢點) |
| 語意/rubric 覆蓋審查 | fresh Agent(sonnet,非產出者)—— 驗證軌 ① |
| 數字再推導/跨文件矛盾/引用實在性/方法論 | **Codex(read-only)** —— 驗證軌 ②,與軌 ① 同一則訊息並行發 |
| 需要獨立第二腦的判斷題 | 換家族(Codex)優先;家族內要乾淨 context → Agent(opus)。**「往上派」概念已廢除** |
| **A3 投影片視覺設計 / rubric 覆蓋** | sonnet 生產;fresh sonnet **或 Codex** 只看**渲染後的 PDF/逐頁圖**驗收,不得以原始投影片檔自驗 |
| **A3 影片 / 音訊 / 字幕 QA** | `/watch` skill(yt-dlp + ffmpeg + 逐字稿)可查:片長、逐頁可讀性、旁白↔投影片同步、逐字稿→主張追溯、字幕數字一致;ffmpeg `volumedetect` 可查爆音/削波。**只有「口說清晰度與聽感」留給 Kenny 本人** |
| **A3 5 分鐘 Zoom 對抗演練** | fresh Agent(sonnet)扮演 senior technical marker,嚴格計時 5 分鐘,追問決策、替代方案、風險、KPI、資源 |
| 對外定稿/不可逆動作/裁決 | 主迴圈 + Kenny(唯一該下場的事) |

### 2.1 Fable 5 已退出常規編制(2026-07-25)

**證據**:知識工作 GDPval-AA Opus 5 = 1861 vs Fable 5 ≈1761;Frontier-Bench agentic coding 43.3% vs 33.7%;綜合智力指數 61 vs 60(平手);價格 2 倍;Fable 安全分類器約 5% 對話誤擋。Fable 唯一領先項是 SWE-bench Pro(80.0 vs 79.2,差 0.8),**不是本 repo 的工作型態**。官方建議亦為「先用 Opus 5,需要最高能力上限才用 Fable」。

⚠️ 以上全為**外部評測**,本 repo 無本地 A/B(Kenny 2026-07-25 裁定不做,直接轉移)。

**回鍋只有兩個具名觸發條件**,不是判斷題:
- (a) Opus 5 **同一子任務連錯 2 次**,且已記錄完整失敗軌跡
- (b) Codex 不可用 **且** 不可逆送出前需要獨立第二意見 —— 此時 Fable 的角色是**同家族、乾淨 context、非產出者的 fallback**,不等同 Codex

## 3. 升降級路徑

- **垂直升級(能力不足型錯)**:haiku 錯 1 次 → sonnet;sonnet 同一子任務連錯 2 次 → 帶完整失敗軌跡升 opus;不第三次原樣重派。
- **水平換家族(視角/盲點型錯)**:升級解決不了盲點。沿用舊 context、跨文件矛盾、數字沿用自己算過的、自驗盲點 → **不升級,開 Codex**。
- opus 也錯 → 收回主迴圈;主迴圈仍無解 → 照 R-問人 交 Kenny。**不存在「再往上」。**
- **降級**:高階解出模式 → 整理成可照抄步驟 → 批次改派 sonnet/haiku。
- 同一件事最多重試 2 輪;第 3 輪 = 換方法或升級(R-換路)。
- Codex timeout = 拆小任務,不是換模型。
- 「錯」的定義:驗收未過、缺必答欄位、引用不存在的路徑/ID、或驗收者打回。格式醜但內容對 ≠ 錯。

## 4. 並行紀律

- 互不依賴的派工在**同一則訊息**一起發;有依賴的等結果再派。
- 已委派的搜尋,主迴圈不自己再做一次(雙倍燒 token)。
- 同時在跑的 background agent ≤3。
- 兩個 agent 不碰同一批檔案;會碰 → 串行或 `isolation: "worktree"`。
- 要收結論才能往下走的派工 → `run_in_background: false`(同步),省一次往返。

## 5. Agent × Codex 兩腦協作架構

核心:**Claude 生產、Codex(異家族)驗證** —— Codex 抓到的錯多是「Claude 沿用自己舊筆記」型,自驗有共同盲點。完整配方見 [references/codex-collab.md](references/codex-collab.md)。

```text
指揮官(主迴圈 = Opus 5)
 ├─ 生產線:Explore(haiku)搜 → general-purpose(sonnet)寫 → opus(乾淨 context)判斷題
 ├─ 驗證線【並行,同一則訊息發出,不排隊】
 │   ├─ 軌①語意面:fresh Claude(sonnet)— 有沒有漏講、rubric 有沒有蓋到、論證缺口
 │   └─ 軌②事實面:Codex(read-only)— 數字、跨文件矛盾、引用實在性、方法論
 └─ 裁決:主迴圈整合 → 對外/不可逆 → Kenny
```

**兩軌查的維度不重疊,所以並行不犧牲覆蓋 —— 省的是 wall-clock。**

**觸發判準改為「風險 × 獨立性」,不是 claim 數:**
- 這個錯若存在,是**能力型**(方法錯、論證漏)還是**慣性型**(抄自己舊數字、跨檔矛盾、引用不存在)?慣性型 → 必 Codex。
- 交付**直接面對評分者或不可逆**?是 → Codex 終審閘門不可省。中間產物 → 抽查即可。

**多輪稽核的範圍(2026-07-25 修訂):**
- R1 全件
- R2 = 缺陷清單 + 改動鄰域 + **凡涉數字的修正一律三邊對賬**(notebook ↔ 報告 ↔ results.json)。理由:表四 759→767 那次是跨產物傳遞依賴,只看鄰域會漏。
- R3 全件兜底,終審

**自檢指令三分法:**
| 對象 | 做法 |
|---|---|
| Opus subagent | **刪掉**多餘的「再檢查一次 / 回答前再驗一遍」—— Opus 5 本來就會自檢,叫它檢查反而過度 |
| Fable 長任務(若回鍋) | **保留** read-back + 明確的獨立 fresh-context verifier 指令(官方對 Fable 長跑的建議) |
| haiku / sonnet | **完全不動**,派工三件套照原樣 |

## 6. 判準速查(完整版見 [02](references/02-judgment-rubrics.md))

- **R-完成**:交付必附證據四選一(命令輸出/read-back/對賬數字/第二意見),沒有證據不得說「完成」。
- **R-獨立**(2026-07-25 新增):**產出者的自檢可以提供 R-完成 的客觀證據,但永遠不滿足「需要獨立驗證」的要求。** 兩者是不同的東西 —— 主迴圈覺得自己查過了,不算查過。
- **R-A3 影音交付閘門**(2026-07-25 新增):A3 不得只憑投影片原檔或講稿宣稱完成,以下四項證據任一未過即不得交付:
  1. **渲染稽核** —— 投影片匯出 PDF/逐頁圖,按實際播放尺寸逐頁檢查裁切、字級、對比、圖例、引用、可讀性;建立 rubric(25/30/30/15)→ 頁碼/時間戳對照表。兩個 30 分項各須有一個可判讀的專業視覺化。
  2. **逐字稿 → 主張追溯** —— 每個外部數字、日期、benchmark、比較、因果主張都要對到來源;估計值標明假設與算法;無來源者刪除或降格表述。
  3. **完整計時播放** —— 從實際要提交的檔案播一次;**片長 ≤ 10:00**;確認權限、畫面、聲音、投影片與旁白同步。
  4. **音訊/可及性** —— ffmpeg 讀峰值查爆音削波;圖表不得只靠顏色傳意;文字須在一般筆電尺寸可讀;字幕與旁白的專有名詞/數字/姓名一致。**最後一次人耳確認由 Kenny 本人做。**
- **R-問人**:只有四類該問 —— 花錢/對外/不可逆、架構級分歧、指示互相矛盾、憑證只有 Kenny 有;其餘選預設+標「⚠️假設」。
- **R-換路**:被打斷 ≥2 次且是重定向、同一錯誤重現 2 次、第 3 個 edge case 補丁、驗證過但不是要的 → 停手換路。
- **R-回讀**:用 Kenny 給的日期/ID/數字前,第一句先回讀關鍵值。
- **R-漂移**:工具與規則打架 → 實查 schema、更新 §0、附日期,才繼續。

## 7. 交付前 60 秒 checklist

```text
□ 列舉型 → 來源 N = 輸出 N?差額有解釋?
□ 關鍵數字/日期/ID 與來源逐字對過?
□ 完成宣稱:有 R-完成 四種證據之一?
□ 需要「獨立驗證」的項目,證據來自非產出者?(R-獨立)
□ 每個新檔 read-back 過?
□ 對外內容:個資已 strip?語言 = 繁體中文(Kenny 偏好)?
□ §8 帳本已更新?本 session 總 token 已記入 handoff?
```

### 7.1 A3 pitch preflight(2026-08-17 截止)

```text
□ A3:截止 2026-08-17 23:59 Sydney、規定檔名、上傳候選檔與影片權限已逐項回讀?
□ A3:約 10 張投影片?若不是,每張都能對到官方五段或 rubric,且差異有一句理由?
□ A3:25/30/30/15 四項皆有頁碼/時間戳對照?兩個 30 分項各有一個通過渲染稽核的視覺化?
□ A3:最終影片已從提交候選檔完整播放並實測 ≤10:00?音訊、同步、字幕、對比、筆電尺寸可讀性皆過?
□ A3 Zoom:Canvas 預約、Sydney↔Taipei 時區、Zoom 連結、麥克風/鏡頭、備援網路、耳機、本機投影片副本皆確認?
□ A3 Q&A:8 題有來源的 defence bank —— 選案/戰略契合、可行性、ROI/成本、風險緩解、倫理、KPI、計畫資源、替代方案;每答 20–40 秒,含證據+限制+決策理由(記骨架不背逐字)?
□ A3 Q&A:已由 fresh reviewer 完成一次嚴格計時 5 分鐘對抗演練,未答出的問題已補回 defence bank?
```

## 8. 成本管控(2026-07-25 新增,經 Codex 四輪對抗定案)

**背景實測**:本框架最大燒錢點不是模型選擇,是**沒設界線的研究型 agent**。2026-07-25 session 實測:Fable 立場書 agent = 86,499 tokens;兩個查網路 agent = 440,503 / 427,108 tokens(各約 5 倍)。

### 8.1 派工必附 scope 上限

派工三件套之外,**每次派工都要宣告**:
- 讀檔上限(N 個檔)或搜尋上限(N 次查詢)
- 輸出長度上限
- 一個不重複的 scope ID

**超出上限的 agent 必須停下來回報「哪些沒涵蓋」,不得自行續跑。**

### 8.2 預先扣額度(不是事後記帳)

**派工前**必須算:

```
已花掉 + 在途保留 + 這次宣告的硬上限  ≤  70% × session 預算
```

- 超過 → **不准發**。自己在主迴圈做完,或問 Kenny 要不要加額度。
- 每次派工的 scope ID + 硬上限,**開跑前先寫進帳本**。
- agent 回來後,保留額度釋放為實際值。
- **沒回來或沒記錄的 agent,按宣告上限全額計,不得按零計。**
- spawn 上限對照**帳本**,不對照計數器。

> 為什麼不能事後記帳:錢已經花完了才知道超支。這是 Codex R2/R3 兩次打回的原因。

### 8.3 spawn 上限

- 同時在跑 ≤3(§4 原規則)
- 每個開放問題 ≤2 個研究 agent
- 每個產物每輪 ≤1 個驗證 agent
- 每 session ≤8 個 subagent,超過必須停下來向 Kenny 報告

### 8.4 預算單位與記錄

- 預算**以總 token 計**,session 開始由 Kenny 宣告,預設 **1.5M subagent tokens**(依 8.0 實測校準)。
- 70% 停止派工、100% 硬停,不經明確同意不得再派。
- 每個 session 的 handoff entry 記錄**按模型分列的 subagent 總 token**,讓預設值能用真實數據重新校準。

### 8.5 殘餘風險(直接告知,不工程化)

**宣告的上限擋不住真的失控的 agent**,除非執行環境會強制終止它。本框架只能在**派工前**攔,攔不住已經開跑的。Codex 明確要求把這一點揭露而不是假裝解決了。

## references/ 清單

| 檔案 | 內容 |
|------|------|
| [README.md](references/README.md) | 移植來源與適用性 |
| [00-diagnosis.md](references/00-diagnosis.md) | VMX 原檔:harness 漏 token/失焦/出錯 前三名診斷 |
| [01-model-dispatch.md](references/01-model-dispatch.md) | VMX 原檔:模型調度守則(本 SKILL §0–§4 的母本) |
| [02-judgment-rubrics.md](references/02-judgment-rubrics.md) | VMX 原檔:R-升級/完成/問人/換路/回讀/新開/漂移 全文 |
| [03-prompt-templates.md](references/03-prompt-templates.md) | VMX 原檔:六型派工模板 |
| [04-maintenance-protocol.md](references/04-maintenance-protocol.md) | VMX 原檔:治理檔維護權限與教訓登記簿 |
| [05-letter-to-future-sessions.md](references/05-letter-to-future-sessions.md) | VMX 原檔:給未來 session 的信 |
| [codex-collab.md](references/codex-collab.md) | **本機版** Agent×Codex 協作架構 + 駕駛配方 + 輸出合約 |
| [codex-driving-vmx-machine.md](references/codex-driving-vmx-machine.md) | VMX 公司機原版配方(本機不適用,留作對照) |
