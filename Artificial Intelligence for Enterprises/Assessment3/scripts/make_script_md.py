# -*- coding: utf-8 -*-
"""產生 notes/22_演講稿_逐頁提詞.md —— 印出來或放第二螢幕用的講稿。

與投影片備註同一份骨架(scripts/pitch.py),所以兩邊永遠不會不一致。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_deck as R
import pitch as PITCH

N = R.narration()
OUT = os.path.join(R.A3, "notes", "22_演講稿_逐頁提詞.md")

L = []
w = L.append
w("# A3 講稿 —— 十分鐘錄製影片(骨架版)")
w("")
w("> 🔴 **這不是逐字稿,不要照著唸。**")
w("> Jiwei Guan 的作業說明:「视频不是简单地『念 PPT』，而是一个 Selling Pitch」、")
w("> 「如果完全照读 AI 生成的稿件，往往会显得不自然，也难以体现个人的说服力」。")
w("> 每頁只要做三件事:**把 ★ 那句話講出來** → 用 · 那三個支點把它撐起來 → 數字照著唸。")
w("> 中間怎麼串,用你自己的話。逐字版在每頁最下面,忘詞才看。")
w("")
w("> ⚠️ **表上那個秒數是「逐字備援」的長度,不是你會講的長度。**")
w("> 你要講的是 ★ 那一句 + 三個支點 + 數字 —— 那比逐字稿短。")
w("> 所以**先錄一次、把真實秒數填進最後一欄**,再決定要砍哪裡。")
w("> 🚫 不要照著推估值先砍 —— 砍完可能還是超,或砍過頭。")
w("")
w("> 🎬 錄製前確認:①人像疊在**右下角**(overlay,不是側欄)②按 **F5** 全螢幕放映再分享")
w("> ③用微軟 PowerPoint,不要 WPS 或 Keynote(老師明講他的系統打不開)")
w("> ④多錄幾遍挑最好的一版(老師建議)")
w("")

tot = 0
w("| 頁 | 這一頁要落地的那句話 | 逐字秒 | 累計 | **實測** |")
w("|---|---|---:|---:|---|")
for i, sk in enumerate(PITCH.SKELETON):
    body = R.unit(i)[1]
    n = len(R.CJK.findall(body)); tot += n
    w(f"| {i+1} | {sk['one'][:34]} | {n/R.RATE:.0f} | "
      f"{int(tot/R.RATE//60)}:{int(tot/R.RATE%60):02d} | ____ |")
w(f"| **合計** | | **{tot/R.RATE:.0f}** | "
  f"**{int(tot/R.RATE//60)}:{int(tot/R.RATE%60):02d}** | ____ |")
w("")
w(f"逐字備援全長 **{tot/R.RATE:.0f} 秒**(4.4 字/秒推估),硬上限 **600 秒**;")
w(f"換頁換氣十二次約 12 秒要另外算。")
w("")
w("> 🔴 **照逐字唸一定超時。** 但你不會照逐字唸 —— 逐字版是忘詞才看的。")
w("> 用 ★ + 三個支點 + 數字去講,實際長度通常落在逐字版的七到九成。")
w("> **先錄一次拿到真實秒數,再照那個數字砍。**")
w("")
w("> ⏱️ 錄的時候每換一頁看一次碼表,把秒數寫進上表最後一欄。")
w("> 錄完把那一欄給我,我照真實數字給逐句刪法 —— 砍的會是")
w("> 「片上已經印著、你又唸一遍」的句子,不是論證。")
w("")
w("---")
w("")

for i, sk in enumerate(PITCH.SKELETON):
    title, body, cues = R.unit(i)
    n = len(R.CJK.findall(body))
    w(f"## 第 {i+1} 頁 · {title}")
    w(f"`目標 {n/R.RATE:.0f} 秒`")
    w("")
    w(f"### ★ {sk['one']}")
    if sk.get("keys"):
        w("")
        for k in sk["keys"]:
            w(f"- {k}")
    if sk.get("nums"):
        w("")
        w("**照著唸的數字**")
        for x in sk["nums"]:
            w(f"- `{x}`")
    if sk.get("red"):
        w("")
        for x in sk["red"]:
            w(f"> ⚠️ {x}")
    if sk.get("cut"):
        w("")
        w(f"> ✂️ **超時砍這裡** —— {sk['cut']}")
    allcues = list(cues)
    if sk.get("cue") and not any(sk["cue"][:12] in c for c in allcues):
        allcues.append(sk["cue"])
    if allcues:
        w("")
        w("**錄影提示(不唸)**")
        for c in allcues:
            w(f"- {c}")
    if body:
        w("")
        w(f"<details><summary>逐字備援 · {n} 字(忘詞才看)</summary>")
        w("")
        w(body)
        w("")
        w("</details>")
    w("")
    w("→ 換下一頁")
    w("")

doc = chr(10).join(L)
open(OUT, "w", encoding="utf-8").write(doc)
print("✅ " + os.path.relpath(OUT, R.A3) + f"  ({len(doc)} 字元)")
print(f"   合計 {tot} 字 = {tot/R.RATE:.0f} 秒 = {int(tot/R.RATE//60)}:{int(tot/R.RATE%60):02d}")
