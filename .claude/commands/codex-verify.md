---
description: 用 Codex(gpt-5.6-sol 異家族)對抗審查指定產物,強制它提出替代方案
argument-hint: "<檔案路徑或要審查的主題> [round1|round2|round3]"
---

開 Codex 異家族線審查:$ARGUMENTS

## 先判斷是哪一種審查

| 類型 | 用哪份合約 |
|---|---|
| **事實核對**(數字、日期、引用、路徑是否真實) | `references/codex-collab.md` §5 |
| **設計/計畫/立場書評審**(要它挑毛病並提方案) | `references/codex-collab.md` **§5.1** — 強制 `ALT`/`COST`/`SELFCHECK` |

不確定就用 §5.1,它涵蓋比較廣。

## 駕駛配方(照抄,不要改)

用 **PowerShell tool**,prompt 走 **stdin**,答案用 **`-o` 落檔**,prompt 一律**純 ASCII 英文**:

```powershell
$out = "<scratchpad>\codex_<主題>_r<N>.md"
$prompt = @'
...pure ASCII English prompt...
'@
$prompt | codex exec --sandbox danger-full-access -o $out
Write-Output "EXIT=$LASTEXITCODE"
```

然後 Read `$out`(不要直接看 stdout,那包含整段 transcript 會爆)。

## 分輪紀律(SKILL §5)

- **R1** 全件審查
- **R2** = R1 缺陷清單 + 改動鄰域 + **凡涉數字的修正一律三邊對賬**(notebook ↔ 報告 ↔ results.json)
- **R3** 全件兜底終審,必須拿到 READY 才可交付

## 每輪跑完必做

1. `git status` 對賬 —— 確認 Codex 沒動檔(prompt 裡已約束 read-only,但仍要驗)
2. 把 verdict 摘要給我,**被 REJECT 的要照實說**,不要只報過關的
3. Codex 自己提的方案被採用 → 標記「未經獨立核對」或另派 fresh Claude agent 查(§5.1 副作用)

## 能力邊界(不要浪費趟次)

Codex **播不了影片/音訊**,也看不出原始 `.pptx` 的實際播放效果。這類驗收走 `/watch` skill + ffmpeg,最後人耳確認留 Kenny。

## timeout

單趟目標 <8 分鐘。timeout = **拆小任務**,不是換模型。
(2026-07-25 實測:一趟 5 個複合命題 + 讀 3 個檔案 EXIT=0,舊表「每趟 2–3 claims」已過時。)
