# -*- coding: utf-8 -*-
"""把 notes/deck_spec/pages.json 渲染成全原生形狀的 pptx。

與前兩版最大的不同:**沒有任何一張 PNG**。
每個方塊、每條線、每段文字都是 PowerPoint 原生物件,Kenny 可以直接點進去改。

用法:python scripts/render_deck.py
輸出:Huang_26254793_421104_Assessment 3.pptx
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from pptx.util import Inches

import native as N

HERE = os.path.dirname(os.path.abspath(__file__))
A3 = os.path.dirname(HERE)
SPEC = os.path.join(A3, "notes", "deck_spec", "pages.json")
OUT = os.path.join(A3, "Huang_26254793_421104_Assessment 3.pptx")

M = 0.72                       # 版心左右
TITLE_Y = 0.42
RULE_Y = 1.52
BODY_TOP = 1.76
BODY_BOT = N.H - 0.42          # 內容底線
FOOT_Y = N.H - 0.62

COVER = dict(
    title="讓機器讀懂一次事件的完整脈絡",
    subtitle="地端 AI 事件判讀 —— 六個月、三道決策門的立案提案",
    hook="今天,五個人要看完三千支影片;而客戶要的答案,兩天內。",
    scale="車隊行車影像 AI · 單一大型車隊約 3,000 筆事件/天 · 5 位專職分析人員",
    who=["Po-Kai Huang(學號 26254793)",
         "421104 Artificial Intelligence for Enterprises · Assessment 3",
         "2026 年 8 月"],
    confid="The company name has been changed for commercial in confidence reasons.　"
           "內部數字均標示為假設或推算量級,並於各頁附推算方式。",
)

REFS = [
    "Australian Human Rights Commission. (2020). Using artificial intelligence to make decisions: Addressing the problem of algorithmic bias.",
    "Department of Industry, Science and Resources. (2019). Australia's artificial intelligence ethics principles.",
    "Ensign, D., Friedler, S. A., Neville, S., Scheidegger, C., & Venkatasubramanian, S. (2018). Runaway feedback loops in predictive policing. PMLR, 81, 160–171.",
    "Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation bias: A systematic review. JAMIA, 19(1), 121–127.",
    "Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. PMLR, 70, 1321–1330.",
    "Hopp, W. J., & Spearman, M. L. (2011). Factory physics (3rd ed., chaps. 7–9). Waveland Press.",
    "National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0).",
    "Northcutt, C. G., Athalye, A., & Mueller, J. (2021). Pervasive label errors in test sets destabilize machine learning benchmarks. NeurIPS Datasets and Benchmarks Track.",
    "Parasuraman, R., & Manzey, D. H. (2010). Complacency and bias in human use of automation. Human Factors, 52(3), 381–410.",
    "Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions. Nature Machine Intelligence, 1(5), 206–215.",
    "Sambasivan, N., Kapania, S., Highfill, H., Akrong, D., Paritosh, P., & Aroyo, L. (2021). “Everyone wants to do the model work, not the data work”: Data cascades in high-stakes AI. CHI '21.",
    "Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., … Dennison, D. (2015). Hidden technical debt in machine learning systems. NeurIPS, 28.",
]

# 每種 block 的相對高度權重 —— 用來分配版心的垂直空間
WEIGHT = {"cards": 1.35, "matrix": 1.25, "compare": 1.20,
          "bar": 1.15, "rows": 1.00, "callout": 0.34}


def cover(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    N.box(s, 0, 0, 0.34, N.H, fill=N.NAVY, line=None, radius=False, who="cover-bar")
    N.text(s, 1.05, 1.30, N.W - 2.6, 1.15, COVER["title"], 40, N.NAVY, bold=True,
           who="cover-title")
    N.text(s, 1.05, 2.58, N.W - 2.6, 0.55, COVER["subtitle"], 20, N.INK,
           who="cover-sub")
    N.rule(s, 1.05, 3.30, 3.2, color=N.ORANGE)
    N.text(s, 1.05, 3.60, N.W - 2.6, 0.6, COVER["hook"], 18, N.ORANGE, bold=True,
           who="cover-hook")
    N.text(s, 1.05, 4.32, N.W - 2.6, 0.45, COVER["scale"], 13, N.GREY,
           who="cover-scale")
    N.text(s, 1.05, 5.16, N.W - 2.6 - N.SAFE_R, 1.05, "\n".join(COVER["who"]),
           15, N.INK, spacing=1.35, who="cover-who")
    N.text(s, 1.05, N.H - 0.70, N.SAFE_X - 1.10, 0.5, COVER["confid"], 12, N.GREY,
           spacing=1.2, who="cover-conf")
    return s


def refs_page(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    N.text(s, M, TITLE_Y + 0.28, 6.0, 0.6, "參考文獻", 28, N.NAVY, bold=True,
           who="ref-title")
    N.rule(s, M, RULE_Y, N.W - 2 * M)
    y = BODY_TOP
    # 文獻列會排到版面底部,兩欄都必須收在人像淨空區左緣以內
    half = (N.SAFE_X - M - 0.45) / 2
    for i, r in enumerate(REFS):
        col, row = i // 6, i % 6
        N.text(s, M + col * (half + 0.45), BODY_TOP + row * 0.80, half, 0.76,
               r, 12, N.INK, spacing=1.25, who=f"ref{i}")
    N.text(s, M, N.H - 0.52, N.SAFE_X - M, 0.34,
           "APA 7th　·　The company name has been changed for commercial in "
           "confidence reasons.", 12, N.GREY, who="ref-foot")
    return s


def content(prs, pg):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if pg.get("eyebrow"):
        N.text(s, M, TITLE_Y, 6.0, 0.30, pg["eyebrow"], 13, N.ORANGE, bold=True,
               who="eyebrow")
    N.text(s, M, TITLE_Y + 0.32, N.W - M - 0.55, 0.62, pg["title"], 27, N.NAVY,
           bold=True, who="title")
    N.text(s, M, TITLE_Y + 1.00, N.W - M - 0.55, 0.40, pg["subtitle"], 15,
           N.GREY, who="subtitle")
    N.rule(s, M, RULE_Y + 0.14, N.W - 2 * M)

    blocks = pg["blocks"]
    foot = pg.get("foot")
    bot = (FOOT_Y - 0.14) if foot else BODY_BOT
    avail = bot - (BODY_TOP + 0.16)
    gap = 0.22
    usable = avail - gap * (len(blocks) - 1)

    # 🔑 高度按**實際需要**分配,不用固定權重。
    #    固定權重的問題:某個 block 被分層縮短後,多出來的空間就空在那裡,
    #    而隔壁塞不下的 block 卻還在把內容往備註丟。
    #    callout 有天花板(它是一句話,給再多空間也只用一行高)。
    specs = [json.loads(b["spec"]) if isinstance(b["spec"], str) else b["spec"]
             for b in blocks]
    CAP = {"callout": 1.35}
    needs = []
    for b, sp in zip(blocks, specs):
        w0 = N.W - 2 * M
        nd = N.text_h(sp.get("text", ""), w0 - 0.40, 17) + 0.30 \
            if b["kind"] == "callout" else usable * WEIGHT.get(b["kind"], 1.0)
        needs.append(min(nd, CAP.get(b["kind"], 1e9)))
    tot = sum(needs) or 1.0
    heights = [usable * n / tot for n in needs]

    y = BODY_TOP + 0.16
    for b, h in zip(blocks, heights):
        spec = json.loads(b["spec"]) if isinstance(b["spec"], str) else b["spec"]
        fn = N.RENDER[b["kind"]]
        width = N.W - 2 * M
        # 底部的 block 若會伸進人像淨空區,寬度收到 SAFE_X
        if y + h > N.SAFE_Y:
            width = min(width, N.SAFE_X - M)
        if b["kind"] == "cards":
            fn(s, M, y, width, h, spec["items"])
        elif b["kind"] == "rows":
            fn(s, M, y, width, h, spec["items"])
        else:
            fn(s, M, y, width, h, spec)
        y += h + gap

    if foot:
        N.text(s, M, FOOT_Y, N.SAFE_X - M, 0.5, foot, 13, N.GREY, who="foot")

    # 版塊放不下而被截斷的完整內容 → 講者備註(內容不丟)
    notes = [f"【{k}】{v}" for k, v in N.OVERFLOW]
    N.OVERFLOW.clear()
    extra = pg.get("why")
    if extra:
        notes.append(f"【這一頁的作用】{extra}")
    if notes:
        s.notes_slide.notes_text_frame.text = chr(10).join(notes)
    return s


def main():
    pages = json.load(open(SPEC, encoding="utf-8"))
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(N.W), Inches(N.H)

    cover(prs)
    for pg in pages:
        content(prs, pg)
    refs_page(prs)

    prs.save(OUT)

    pic = sum(1 for sl in prs.slides for sh in sl.shapes if sh.shape_type == 13)
    shp = sum(len(sl.shapes) for sl in prs.slides)
    print(f"✅ {os.path.basename(OUT)}")
    print(f"   {len(prs.slides)} 頁 · {os.path.getsize(OUT)/2**20:.2f} MB")
    print(f"   形狀 {shp} 個 · 圖片 {pic} 個 {'✅ 全原生可編輯' if pic == 0 else '🔴 仍有貼圖'}")
    return OUT


if __name__ == "__main__":
    main()
