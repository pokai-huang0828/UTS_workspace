---
description: 用 Claude in Chrome(Kenny 已登入的 Chrome)抓 Innovation Studio Canvas 的新內容,存進 repo 並 push(只能在 Kenny 自己電腦上的 session 跑)
argument-hint: "[可選:只抓哪一塊,例如 announcements / modules / groups / assignments]"
---

抓 421048 Innovation Studio(Canvas course 42610)自上次抓取以來的新內容:$ARGUMENTS

## 0. 先確認環境(不符合就停下來告訴 Kenny)

- 這個指令**只能在 Kenny 自己電腦上的 session 跑**(`claude --chrome`,或 `claude remote-control --chrome`)。雲端 session(claude.ai/code 容器)用不了 Kenny 的 Chrome,也過不了 UTS SSO。
- 先 `git pull origin main`。
- 呼叫 `mcp__claude-in-chrome__tabs_context_mcp`;工具不存在或沒連線 → 請 Kenny 在 Claude Code 裡輸入 `/chrome` 連線,不要自己想辦法繞。
- 開**新分頁**到 `https://canvas.uts.edu.au/courses/42610`;如果跳到登入頁 → 停下來,請 Kenny 自己在 Chrome 完成 UTS 登入和 MFA。**不要碰帳號密碼。**

## 1. 抓什麼(用同源 fetch 讀 Canvas API,在 Canvas 分頁裡跑 javascript_tool)

| 項目 | API(相對網址) | 存到 |
|---|---|---|
| 公告 | `/api/v1/courses/42610/discussion_topics?only_announcements=true&per_page=50` | `Innovation Studio/notes/raw/canvas_update_<日期>.md` |
| 模組與項目(單元三到六開了沒) | `/api/v1/courses/42610/modules?include[]=items&per_page=100` | 同上 |
| 新的頁面全文 | `/api/v1/courses/42610/pages/<slug>` → `DOMParser().parseFromString(j.body,'text/html').body.innerText` | 同上(長頁可另存一檔) |
| 作業與截止日有沒有改 | `/api/v1/courses/42610/assignments?per_page=100` | 同上(只記和 `assessments/_Canvas原文_AT1-AT4_2026-10-22.md` 不同的地方) |
| 我們的小組 | `/api/v1/users/self/groups?per_page=50` | **只記**有沒有入組、組名/組號 → repo;隊友姓名 → `Innovation Studio/private/`(不進版控) |
| 討論區清單 | `/api/v1/courses/42610/discussion_topics?per_page=100` | 只記標題、編號、group_category_id |

- `javascript_tool` 一次只回約 1000 字元 → 長內容分批回傳,或寫進頁面上的 `<pre>` 再用 `get_page_text` 讀。
- 檔案要下載:`/api/v1/files/<id>/public_url` 取簽章網址 → 用 `curl -o` 存到 `Innovation Studio/notes/materials/files/`(超過 10 MB 的先問 Kenny)。
- 原文是簡體就照存簡體(逐字,不改寫),檔頭寫來源 API、抓取時間(台灣)。

## 2. 隱私(一定要守)

- **同學的討論區貼文、姓名、照片不進 repo**;需要的話整理到 `Innovation Studio/private/`(已在 .gitignore)。
- Kenny 本人和老師的名字可以留。

## 3. 整理與回報

1. 在 `canvas_update_<日期>.md` 最上面寫 5–10 行重點:新公告、新開放的單元、截止日變動、我們有沒有在同一個小組、組號。
2. 和 `Innovation Studio/README.md` §1、§5、`notes/06_第2週準備與AT1週報.md` §5「要回 Canvas 確認的事」對照:已確認的事更新回去(註明日期與出處);新的矛盾加進 README §5。
3. `git add` → commit(訊息寫清楚抓了什麼)→ `git push origin main`。
4. 回報給 Kenny(繁體中文):抓了哪些、有什麼新東西、哪些沒抓到、下一步。
