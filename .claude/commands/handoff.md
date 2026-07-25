---
description: 對賬 git log 與 handoff.md,補上漏記的成果並 append 本 session entry
argument-hint: "[可選:本 session 的一句話重點]"
---

把 `handoff.md` 補到與 git 現況一致,然後 append 本 session 的 entry。

## 步驟(照順序做,不要跳)

1. **實查現況**,一次跑完:
   - `git log --oneline -15`
   - `git status --short`
   - `git rev-list --left-right --count origin/main...main`(是否落後/超前遠端)
   - 讀 `handoff.md` 的**最後 3 個 entry 標題**(用 tail,不要讀全檔 —— 23KB+)

2. **對賬**:找出「已 commit 但 handoff 沒寫」的成果。逐筆列出 commit hash + 訊息,先給我看,**不要直接寫檔**。

3. **等我確認後**再 append。格式照既有 entry:
   ```
   ## YYYY-MM-DD(時段)· 一句話標題

   ### 交付(已驗證)
   - 產物路徑 + 一句話 + 證據(命令輸出 / read-back / 對賬數字 / 第二意見)

   ### 待辦變化
   - 關閉了什麼、新增了什麼(**待辦本體寫在 TODO.md,這裡只記變化**)

   ### 教訓 / 環境註記
   - 只寫「下個 session 不知道會踩坑」的事
   ```

4. **同步 TODO.md**:這個 session 關掉的待辦要從 TODO.md 移除或打勾,新出現的要加進去。

5. **記成本**(SKILL §8.4):本 session 的 subagent 總 token,按模型分列,寫進 entry。

## 硬規則

- `handoff.md` 是 **append-only**。**只在檔尾加**,絕對不改既有 entry(歷史 entry 的路徑就算已失效也不動,改了會破壞可追溯性)。
- 待辦不要寫進 handoff —— 那是 `TODO.md` 的事。handoff 只記**已發生的事實**。
- 每個宣稱「完成」的項目都要附證據(R-完成)。沒證據的寫「⚠️未驗證」。
- 寫完 read-back 確認。

$ARGUMENTS
