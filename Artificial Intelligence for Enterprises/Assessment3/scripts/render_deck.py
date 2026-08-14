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
BODY_BOT = N.H - 0.38          # 內容底線(0.42→0.38:第 9 頁差 0.12" 才裝得下八條 KPI)
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


def narration():
    """從 notes/_v2_parts 取出十二個單元的口白逐字。

    順序:鉤子 → P1…P10 → 參考文獻,正好對上投影片 1…12。
    舞台指示(整段被括號包住的錄影標記)剝掉 —— 那是給錄影用的,不唸出聲。
    """
    import glob
    H1 = re.compile(r"(?m)^#\s+(.+)$")
    NARR = re.compile(r"(?m)^##\s*口白逐字\s*$")
    NXT = re.compile(r"(?m)^#{1,2}\s+")
    STAGE = re.compile(r"(?ms)^[ \t]*[*_]{0,2}[(（].*?[)）][*_]{0,2}[ \t]*$")
    out = []
    for f in sorted(glob.glob(os.path.join(A3, "notes", "_v2_parts", "*.md"))):
        t = open(f, encoding="utf-8").read()
        hs = list(H1.finditer(t))
        for i, m in enumerate(hs):
            if i == 0:
                continue                      # 分段標題(甲/乙/丙段),不是單元
            e = hs[i + 1].start() if i + 1 < len(hs) else len(t)
            u = t[m.start():e]
            nm = NARR.search(u)
            if not nm:
                out.append((m.group(1).strip(), "", []))
                continue
            rest = u[nm.end():]
            nx = NXT.search(rest)
            raw = rest[:nx.start()] if nx else rest
            # 舞台指示不唸出聲,但它是**錄影提示**(哪裡停、哪裡切全螢幕人像),
            # 所以要留下來放在講稿下方,不是丟掉。
            cues = [re.sub(r"[*_`~]", "", c).strip("()（） \n")
                    for c in STAGE.findall(raw)]
            blk = STAGE.sub("", raw)
            body = "\n".join(l for l in blk.split("\n")
                             if not l.lstrip().startswith(">")).strip()
            out.append((m.group(1).strip(), re.sub(r"[*_`~]", "", body), cues))
    return out


NARR_CACHE = None


RATE = 4.4          # 字/秒(全片配時基準)
CJK = re.compile(r"[一-鿿A-Za-z0-9]")


def put_notes(slide, idx, extra_lines):
    """講者備註 = **提詞稿**。

    結構刻意固定,錄影時眼睛只掃第一行就知道這頁該講多久:
        【第 N 頁 · 約 XX 秒 · 累計 X:XX】
        ── 講稿 ──
        <照著唸的字>
        ── 錄影提示 ──
        <哪裡停、哪裡切全螢幕人像>
        → 換下一頁
        ── 備查(不唸)──
        <被收起來的細節>
    """
    global NARR_CACHE
    if NARR_CACHE is None:
        NARR_CACHE = narration()
    parts = []
    if idx < len(NARR_CACHE) and NARR_CACHE[idx][1]:
        title, body, cues = NARR_CACHE[idx]
        n = len(CJK.findall(body))
        secs = n / RATE
        cum = sum(len(CJK.findall(NARR_CACHE[k][1])) for k in range(idx + 1)) / RATE
        parts.append(f"【第 {idx + 1} 頁 · {title}】"
                     f"　約 {secs:.0f} 秒 · {n} 字 · 累計 {int(cum // 60)}:{int(cum % 60):02d}")
        parts.append("── 講稿(照著唸)──")
        parts.append(body)
        if cues:
            parts.append("── 錄影提示(不唸)──")
            parts.extend(f"· {c}" for c in cues)
        parts.append("→ 換下一頁")
        if extra_lines:
            parts.append("── 備查(不唸,答辯用)──")
    parts.extend(extra_lines)
    if parts:
        slide.notes_slide.notes_text_frame.text = chr(10).join(parts)


def need_h(kind, sp, w):
    """這個版塊**真正需要**多少高度(吋)。

    🔴 為什麼要有這個函式:
       版心高度原本按 WEIGHT 這張跟內容無關的固定權重分配,
       於是「三張卡片、每張三行長句」跟「三張卡片、每張一個詞」拿到一樣的高度。
       實際後果是第 6 頁那張〈這 85% 到底是什麼(三層,一層都不可省)〉——
       標題印出來了,**三層本身被 clamp 吃掉**,片上只剩一句半。
       那是全案最重要的一句話,而它是被一個猜出來的高度砍掉的。

    這裡的估算刻意跟各 blk_* 的實際幾何對齊(卡片標題 0.62 + 徽章 0.42、
    表格表頭 0.36、rows 的 PAD 0.10 …),數值不必精準到吋,
    但**必須隨內容單調成長** —— 分配是按比例正規化的,重要的是相對大小。
    """
    if kind == "callout":
        return N.text_h(sp.get("text", ""), w - 0.40, 17) + 0.30

    if kind == "matrix":
        rows, cols = sp.get("rows", []), sp.get("cols", [])
        name_w = w * sp.get("name_frac", 0.30)
        cw = (w - name_w) / max(len(cols), 1)
        # 每格允許到 2 行時的高度 —— 壓到 1 行雖然放得下,但那是降級不是需求
        return 0.36 + sum(
            max([min(N.text_h(str(r["name"]), name_w - 0.16, 12,
                              safety=N.PINNED_SAFETY), 2 * 0.345)]
                + [min(N.text_h(str(c), cw - 0.16, 12,
                                safety=N.PINNED_SAFETY), 2 * 0.345)
                   for c in r["cells"]]) + 0.06
            for r in rows)

    if kind == "cards":
        items = sp["items"]
        cw = (w - 0.16 * (len(items) - 1)) / max(len(items), 1)
        return max(0.82 + (0.42 if it.get("badge") else 0) + 0.14
                   + sum(N.text_h(ln, cw - 0.24, 12, 1.35)
                         for ln in it.get("lines", []))
                   for it in items)

    if kind == "compare":
        cw = (w - 0.30) / 2
        return 0.90 + (0.48 if sp.get("verdict") else 0) + max(
            sum(N.text_h(ln, cw - 0.32, 13, 1.5) for ln in sp[s]["lines"])
            for s in ("left", "right"))

    if kind == "rows":
        LW, VW, NW = w * 0.24, w * 0.30, w * 0.40
        return sum(max(N.text_h(it["label"], LW - 0.24, 14),
                       N.text_h(it["value"], VW - 0.14, 15),
                       min(N.text_h(it.get("note", ""), NW - 0.14, 12),
                           3 * 0.30)) + 0.20
                   for it in sp["items"])

    if kind == "bar":
        h = (0.48 if sp.get("label") else 0) + 0.72
        if sp.get("bracket"):
            h += 1.24 if isinstance(sp["bracket"].get("big"), str) else 0.62
        return h + (0.30 if sp.get("note") else 0)

    return 2.0


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
    put_notes(s, 0, [])
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
    put_notes(s, 11, [])
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
    gap = 0.14
    usable = avail - gap * (len(blocks) - 1)

    # 🔑 高度按**實際需要**分配,不用固定權重。
    #    固定權重的問題:某個 block 被分層縮短後,多出來的空間就空在那裡,
    #    而隔壁塞不下的 block 卻還在把內容往備註丟。
    #    callout 有天花板(它是一句話,給再多空間也只用一行高)。
    specs = [json.loads(b["spec"]) if isinstance(b["spec"], str) else b["spec"]
             for b in blocks]
    CAP = {"callout": 1.35}
    needs = [min(need_h(b["kind"], sp, N.W - 2 * M), CAP.get(b["kind"], 1e9))
             for b, sp in zip(blocks, specs)]

    # 🔴 表格先拿到**保證下限**,剩下的空間才按需求比例分。
    #    理由是兩種版塊掉東西的後果不一樣:
    #      · cards / rows 少印一行,是說明變短 —— 難看,但沒有自相矛盾;
    #      · matrix 少印一列,是**標題承諾「十條風險」而片上只有六條** ——
    #        那是投影片自己跟自己打架,而且看的人一數就知道。
    #    所以表格的最小高度(每格壓到 1 行)不參與競爭,直接扣下來。
    #    callout 也給一條下限 —— 第 9 頁那條被分到 **0.00"**,等於這個版塊不存在。
    FLOOR = {"callout": 0.62}
    floors = [(0.36 + len(sp.get("rows", [])) * 0.32) if b["kind"] == "matrix"
              else FLOOR.get(b["kind"], 0.0)
              for b, sp in zip(blocks, specs)]
    # 下限加總可能就已經超過版心(第 9 頁:兩張表 + callout)。
    # 這時要縮下限,否則 slack 變負數、版塊會被排到版面外(實測掉出底部 0.74")。
    # 🔑 縮的順序有先後:**先縮 callout,表格的下限最後才動** ——
    #    callout 短一句只是話變短,表格少一列是投影片自打嘴巴。
    if sum(floors) > usable:
        over = sum(floors) - usable
        for i, b in enumerate(blocks):
            if over <= 1e-9:
                break
            if b["kind"] != "matrix":
                cut = min(floors[i], over)
                floors[i] -= cut
                over -= cut
        if over > 1e-9:                       # 光表格的下限就塞不下,只好等比縮
            k = usable / sum(floors)
            floors = [f * k for f in floors]
    slack = max(usable - sum(floors), 0.0)
    extra = [max(n - f, 0.0) for n, f in zip(needs, floors)]
    tot = sum(extra) or 1.0
    heights = [f + slack * e / tot for f, e in zip(floors, extra)]

    # 🔴 每種版塊都有一個「再少就畫不出來」的高度。低於它會產生**零高或負高的形狀**,
    #    python-pptx 照寫、zip 也合法,但 PowerPoint 會拒絕開啟整個檔案。
    #    不足的部分一律向最高的那個版塊借。
    MIN = {"callout": 0.36, "cards": 1.75, "rows": 0.70,
           "compare": 0.95, "bar": 0.80, "matrix": 0.70}
    for _ in range(len(heights)):
        i = min(range(len(heights)),
                key=lambda k: heights[k] - MIN.get(blocks[k]["kind"], 0.3))
        gap_i = MIN.get(blocks[i]["kind"], 0.3) - heights[i]
        if gap_i <= 1e-6:
            break
        # 向**餘裕最多**的版塊借,不是向最高的借 —— 最高的那個可能自己就剛好卡在下限
        # (第 10 頁 cards 1.69" 既是最矮也是最高,迴圈當場空轉)。
        j = max(range(len(heights)),
                key=lambda k: heights[k] - max(MIN.get(blocks[k]["kind"], 0.3),
                                               floors[k]))
        if j == i:
            break
        # 借的時候不能借到低於對方的 floor —— 否則剛保住的表格列又被借走
        # (實測第 10 頁四臂表就是這樣從 1.64" 被扣到 1.58",少印一臂)。
        take = min(gap_i,
                   heights[j] - max(MIN.get(blocks[j]["kind"], 0.3), floors[j]))
        if take <= 1e-6:
            break
        heights[j] -= take
        heights[i] += take
    assert all(h > MIN.get(b["kind"], 0.3) - 1e-6 for h, b in zip(heights, blocks)), \
        f"第 {pg['n']} 頁塞不下:" + "、".join(
            f'{b["kind"]}={h:.2f}"' for b, h in zip(blocks, heights))

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
    extra = [f"【{k}】{v}" for k, v in N.OVERFLOW]
    N.OVERFLOW.clear()
    if pg.get("why"):
        extra.append(f"【這一頁的作用】{pg['why']}")
    put_notes(s, pg["n"] - 1, extra)      # 投影片 n → 單元索引 n-1
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
