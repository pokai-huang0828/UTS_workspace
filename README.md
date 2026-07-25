# UTS_workspace

黃柏凱(PoKai Huang / Kenny)· 學號 26254793 · UTS 碩士課程作業與筆記工作區。

跨裝置(Windows / Mac)靠 `push origin main` 同步。

---

## 新 session 從這裡開始

| 讀什麼 | 目的 |
|--------|------|
| [handoff.md](handoff.md) **最後一個 entry** | 交接現況(append-only 事實流水帳,**不要讀全檔**,23KB+) |
| [TODO.md](TODO.md) | 當前待辦(可覆寫,單一真相來源) |
| [CLAUDE.md](CLAUDE.md) | 專案規則(繁體中文、證據要求、派工路由) |
| [.claude/skills/uts-dispatch/SKILL.md](.claude/skills/uts-dispatch/SKILL.md) | 多步驟任務前必讀:派工守則 + 驗證架構 + 成本管控 |

**handoff 記已發生的事,TODO 記還沒做的事** —— 兩者不要混。

---

## 目錄結構

| 資料夾 | 課程 | 狀態 |
|--------|------|------|
| `Artificial Intelligence for Enterprises/` | 421104 企業 AI(Session 4 2026) | **進行中** — A2a 7/26、A2b 8/2、A3 8/17 |
| `Foundation Studio/` | 231708 Foundation Studio | 已結束 |
| `Data Visualisation and Visual Analytics/` | 321146 DVVA | 已結束 |
| `Cybersecurity Analytics and Insights/` | 資安分析 | 已結束 |
| `BusnessAnalytics/` | 商業分析(⚠️ 目錄名拼字錯,應為 Business) | 已結束 |
| `PythonData/` | Python 資料處理練習 | — |

進行中課程的內部慣例:`AssessmentX/` 放交件物、`notes/` 放整理過的情報、`notes/raw/` 放一手逐字落檔、`notes/transcripts/` 放 Zoom 逐字稿、`practice/` 放練習 notebook。命名規則見 [notes/README.md](Artificial%20Intelligence%20for%20Enterprises/notes/README.md)。

---

## 協作架構

主迴圈 **Claude Opus 5** 當指揮官,派工給便宜的 subagent 生產,**Codex(gpt-5.6-sol,異家族)**做對抗驗證。

```
Kenny ── 拍板 / 花錢 / 對外送出 / 憑證
  └─ Opus 5(指揮官)
       ├─ haiku   找檔、盤點
       ├─ sonnet  抄寫、實作、初稿
       ├─ Codex   數字、引用、跨文件矛盾、交件終審
       └─ Fable 5 ⛔ 已退出常規編制(2026-07-25)
```

核心原則:**產出者不當驗收者**。交件前一定過 Codex。細節見 SKILL.md。

指令:`/uts-dispatch`(載入守則)、`/handoff`(對賬交接)、`/codex-verify`(開對抗審查)。

---

## 資料集不在版控裡

MNIST/FashionMNIST 與 DDoS 擷取檔(合計約 471 MB)已於 2026-07-25 移出 git 追蹤(見 `.gitignore` 尾段)。

**在新機器 clone 後這些檔案不存在**:MNIST 系列由 torchvision 首次執行自動下載;DDoS 資料集需自行從課程頁重抓。

---

## 外部連結

- A2 Google Doc:https://docs.google.com/document/d/1LhaZHVwcy7DfAoScwaaPPeRIuBgHoZS_xu2a4c0nb7E/edit?usp=sharing
