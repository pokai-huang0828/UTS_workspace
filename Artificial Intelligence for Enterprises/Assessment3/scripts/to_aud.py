# -*- coding: utf-8 -*-
"""把片上所有金額從新台幣換成澳幣。

🔴 為什麼:這是交給 UTS 的作業,評分者在澳洲。用 NT$ 他沒有量感 ——
   「NT$16–20 萬」對他是一串陌生的數字,「A$7,100–8,900」他一眼知道那是多少。

🔴 匯率用 **1 A$ = NT$22.6**(2026-08 實際匯率),不是提案原本寫的 21。
   21 是 2026 年的**年均值**;2026-08-14 的實際匯率是 22.66。
   用 21 會把澳幣金額**高估約 8%** —— 而匯率是提案自己列出的三個假設之一,
   標錯等於在自己標明「這是假設」的地方出錯,最難看。

🔑 換算不影響任何比值(設備佔工程師年成本 14%–19%、佔已估成本 9%–10% …),
   已逐條驗算過。
"""
RATE = 22.6          # 1 A$ = NT$22.6(2026-08)

# 逐條列出,不做正則猜測 —— 金額換錯比沒換更糟
SUBS = [
    # 第 5 頁
    ("NT$16–20 萬/台", "A$7,100–8,900/台"),
    # 第 10 頁(KPI 業務④)
    ("省5–13人≈NT$520–1,521萬", "省5–13人≈A$23–67 萬"),
    # 第 12 頁
    ("NT$6.7–7.5 萬", "A$2,970–3,320"),
    ("匯率(1 A$≈NT$21)", "匯率(1 A$=NT$22.6,2026-08)"),
    ("1–2 台 · NT$16–40 萬", "1–2 台 · A$7,100–17,700"),
    ("NT$520–1,521 萬/年", "A$23–67 萬/年"),
    ("約 NT$50–118 萬(中案 72 萬)", "約 A$2.2–5.2 萬(中案 3.2 萬)"),
    ("NT$173–1,219 萬", "A$7.7–53.9 萬"),
    ("NT$42–47 萬", "A$18,600–20,800"),
    ("NT$158–177 萬", "A$7.0–7.9 萬"),
    ("NT$104–117 萬", "A$46,000–51,800"),
    ("初階工程師年成本(104–117 萬)", "初階工程師年成本(A$46,000–51,800)"),
]


def convert(text):
    for a, b in SUBS:
        text = text.replace(a, b)
    return text


if __name__ == "__main__":
    import json
    import os
    import re
    import sys
    HERE = os.path.dirname(os.path.abspath(__file__))
    SPEC = os.path.join(os.path.dirname(HERE), "notes", "deck_spec", "pages.json")
    P = json.load(open(SPEC, encoding="utf-8"))
    n = 0
    for pg in P:
        for f in ("title", "subtitle", "foot"):
            if pg.get(f):
                new = convert(pg[f])
                if new != pg[f]:
                    pg[f] = new
                    n += 1
        for b in pg["blocks"]:
            s = b["spec"] if isinstance(b["spec"], str) else json.dumps(b["spec"], ensure_ascii=False)
            new = convert(s)
            if new != s:
                b["spec"] = new
                n += 1
    json.dump(P, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"換了 {n} 個欄位")
    # 匯率宣告本身當然會留著 NT$,那不算漏換
    left = [(pg["n"], m.group(0)) for pg in P
            for m in re.finditer(r"NT\$[^\"]{0,26}", json.dumps(pg, ensure_ascii=False))
            if not m.group(0).startswith("NT$22.6")]
    if left:
        print("🔴 還有 NT$ 沒換掉:")
        for k, v in left:
            print(f"   第 {k} 頁 {v}")
    else:
        print("✅ 片上已無 NT$")
