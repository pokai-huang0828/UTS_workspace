# -*- coding: utf-8 -*-
"""原生形狀引擎 —— 用 python-pptx 的真形狀與真文字框畫圖,不出 PNG。

為什麼要有這支:
    先前兩版投影片的圖都是 matplotlib 出 PNG 再貼進去。
    在 PowerPoint 裡那就是**一張死圖** —— Kenny 一個字都改不了,
    而他要的是「可以編輯的內容,包括裡面的圖字」。

    這裡的每一個方塊、每一條線、每一段文字都是原生物件:
    點下去可以改字、拖位置、換顏色,不需要回頭找 Python。

座標一律用「吋」,原點在左上角(與 PowerPoint 一致)。
"""
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── 色票(全片鎖定,不得自行取色)────────────────────────────────
NAVY = "#1F4E79"
ORANGE = "#E8833A"
RED = "#C00000"
GREY = "#6B7885"
LIGHT = "#DCE3EA"
PALE = "#EAF1F8"
INK = "#16212E"
WHITE = "#FFFFFF"
FONT = "Microsoft JhengHei"

TONE = {"navy": NAVY, "orange": ORANGE, "red": RED, "grey": GREY,
        "chosen": NAVY, "light": LIGHT, "ink": INK}

W, H = 13.333, 7.5
SAFE_R, SAFE_B = 2.05, 1.15          # 右下人像淨空區
SAFE_X, SAFE_Y = W - SAFE_R, H - SAFE_B
MIN_PT = 12.0                        # 投影片字級下限


def rgb(h):
    return RGBColor(int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))


def _guard(x, y, w, h, who):
    assert -0.01 <= x and x + w <= W + 0.01, f"{who} 超出版面寬:{x:.2f}+{w:.2f}"
    assert -0.01 <= y and y + h <= H + 0.01, f"{who} 超出版面高:{y:.2f}+{h:.2f}"
    if x + w > SAFE_X + 1e-6 and y + h > SAFE_Y + 1e-6:
        raise AssertionError(
            f"{who} 侵入右下人像淨空區(x>{SAFE_X:.2f} 且 y>{SAFE_Y:.2f})")


# ══════════════════════════════════════════════════════════════════
# 基本元件
# ══════════════════════════════════════════════════════════════════
def text(slide, x, y, w, h, s, size=14, color=INK, bold=False,
         align="left", anchor="top", spacing=1.25, who="text"):
    """真文字框。s 可含 \\n;每一行都是一個可編輯段落。"""
    assert size >= MIN_PT - 1e-6, f"{who} 字級 {size}pt 低於下限 {MIN_PT}pt"
    _guard(x, y, w, h, who)
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    for i, line in enumerate(str(s).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                       "right": PP_ALIGN.RIGHT}[align]
        p.line_spacing = spacing
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.name = FONT
        r.font.color.rgb = rgb(color)
    return tb


def box(slide, x, y, w, h, fill=None, line=None, lw=1.6, radius=True,
        who="box", dash=False):
    """真矩形(圓角可選)。fill / line 給 None 表示不填 / 不描邊。"""
    _guard(x, y, w, h, who)
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    if radius:
        # 圓角半徑改小,預設太圓像按鈕
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(lw)
        if dash:
            from pptx.enum.dml import MSO_LINE_DASH_STYLE
            shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def rule(slide, x, y, w, color=NAVY, thick=0.035):
    """細分隔線(用扁矩形做,PowerPoint 裡好選好改)。"""
    return box(slide, x, y, w, thick, fill=color, line=None, radius=False,
               who="rule")


def arrow(slide, x, y, w, h=0.16, color=GREY):
    _guard(x, y, w, h, "arrow")
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = rgb(color)
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp


def badge(slide, x, y, w, h, s, color, size=12):
    """狀態標籤(圓角小條 + 白字)。"""
    box(slide, x, y, w, h, fill=color, line=None, who="badge")
    text(slide, x, y, w, h, s, size=size, color=WHITE, bold=True,
         align="center", anchor="middle", who="badge-text")


# ══════════════════════════════════════════════════════════════════
# 版塊 —— 六種,對應設計稿的 block kind
# ══════════════════════════════════════════════════════════════════
def blk_cards(slide, x, y, w, h, items):
    """横排卡片。items = [{title, badge, tone, lines[]}]"""
    n = len(items)
    gap = 0.16
    cw = (w - gap * (n - 1)) / n
    for i, it in enumerate(items):
        cx = x + i * (cw + gap)
        tone = TONE.get(it.get("tone", "navy"), NAVY)
        chosen = it.get("tone") == "chosen"
        box(slide, cx, y, cw, h, fill=(PALE if chosen else WHITE),
            line=tone, lw=(3.0 if chosen else 1.6), who=f"card{i}")
        text(slide, cx + 0.12, y + 0.14, cw - 0.24, 0.62, it["title"],
             size=15, color=INK, bold=True, align="center", who=f"card{i}-t")
        by = y + 0.82
        if it.get("badge"):
            bw = min(cw - 0.5, 1.35)
            badge(slide, cx + (cw - bw) / 2, by, bw, 0.30, it["badge"], tone)
            by += 0.42
        if it.get("lines"):
            text(slide, cx + 0.12, by, cw - 0.24, h - (by - y) - 0.14,
                 "\n".join(it["lines"]), size=12, color=GREY, align="center",
                 spacing=1.35, who=f"card{i}-l")


def blk_bar(slide, x, y, w, h, spec):
    """分段長條 + 括弧標註。spec = {label, segments[{name,value,weight,hot}], bracket, note}"""
    if spec.get("label"):
        text(slide, x, y, w, 0.38, spec["label"], size=17, color=INK, bold=True,
             who="bar-label")
    by = y + (0.48 if spec.get("label") else 0)
    bh = 0.62
    tot = sum(s.get("weight", 1) for s in spec["segments"])
    cx = x
    hot_x0 = hot_x1 = None
    for s in spec["segments"]:
        sw = w * s.get("weight", 1) / tot
        hot = s.get("hot")
        box(slide, cx, by, sw, bh, fill=(NAVY if hot else LIGHT), line=WHITE,
            lw=1.5, radius=False, who="seg")
        text(slide, cx, by + 0.05, sw, 0.26, s["name"], size=12,
             color=(WHITE if hot else INK), bold=True, align="center", who="seg-n")
        if s.get("value"):
            text(slide, cx, by + 0.31, sw, 0.26, s["value"], size=12,
                 color=(WHITE if hot else GREY), align="center", who="seg-v")
        if hot:
            hot_x0 = cx if hot_x0 is None else hot_x0
            hot_x1 = cx + sw
        cx += sw
    yy = by + bh + 0.10
    if spec.get("bracket") and hot_x0 is not None:
        b = spec["bracket"]
        rule(slide, hot_x0, yy, hot_x1 - hot_x0, color=NAVY, thick=0.03)
        text(slide, hot_x0, yy + 0.10, hot_x1 - hot_x0, 0.30, b["text"],
             size=14, color=NAVY, bold=True, align="center", who="brk")
        if b.get("big"):
            text(slide, hot_x0, yy + 0.44, hot_x1 - hot_x0, 0.60, b["big"],
                 size=30, color=NAVY, bold=True, align="center", who="brk-big")
        yy += 1.10
    if spec.get("note"):
        text(slide, x, min(yy, y + h - 0.30), w, 0.30, spec["note"], size=12,
             color=GREY, who="bar-note")


def blk_rows(slide, x, y, w, h, items):
    """左標右值的資料列。items = [{label, value, note, hot}]"""
    n = len(items)
    rh = min(0.72, h / max(n, 1))
    for i, it in enumerate(items):
        ry = y + i * rh
        c = RED if it.get("hot") else NAVY
        box(slide, x, ry + 0.04, 0.05, rh - 0.16, fill=c, line=None,
            radius=False, who=f"row{i}-tick")
        text(slide, x + 0.18, ry + 0.02, w * 0.42, rh - 0.10, it["label"],
             size=14, color=INK, bold=True, anchor="middle", who=f"row{i}-l")
        text(slide, x + w * 0.46, ry + 0.02, w * 0.30, rh - 0.10, it["value"],
             size=16, color=c, bold=True, anchor="middle", who=f"row{i}-v")
        if it.get("note"):
            text(slide, x + w * 0.78, ry + 0.02, w * 0.22, rh - 0.10, it["note"],
                 size=12, color=GREY, anchor="middle", who=f"row{i}-n")


def blk_compare(slide, x, y, w, h, spec):
    """左右兩欄對照 + 一句裁決。"""
    gap = 0.30
    cw = (w - gap) / 2
    for i, side in enumerate(("left", "right")):
        s = spec[side]
        cx = x + i * (cw + gap)
        tone = TONE.get(s.get("tone", "navy"), NAVY)
        vh = h - (0.48 if spec.get("verdict") else 0)
        box(slide, cx, y, cw, vh, fill=WHITE, line=tone, lw=2.0, who=f"cmp{i}")
        text(slide, cx + 0.16, y + 0.16, cw - 0.32, 0.42, s["title"], size=17,
             color=tone, bold=True, align="center", who=f"cmp{i}-t")
        text(slide, cx + 0.16, y + 0.70, cw - 0.32, vh - 0.86,
             "\n".join(s["lines"]), size=13, color=INK, spacing=1.5,
             align="center", who=f"cmp{i}-l")
    if spec.get("verdict"):
        text(slide, x, y + h - 0.40, w, 0.38, spec["verdict"], size=15,
             color=INK, bold=True, align="center", who="cmp-v")


def blk_matrix(slide, x, y, w, h, spec):
    """表格:cols[] + rows[{name, cells[], hot}]。用原生形狀畫,每格可編輯。"""
    cols = spec["cols"]
    rows = spec["rows"]
    name_w = w * spec.get("name_frac", 0.30)
    cw = (w - name_w) / max(len(cols), 1)
    hh = 0.40
    rh = min(0.52, (h - hh) / max(len(rows), 1))
    for j, c in enumerate(cols):
        text(slide, x + name_w + j * cw, y, cw, hh, c, size=13, color=GREY,
             bold=True, align="center", anchor="middle", who=f"col{j}")
    for i, r in enumerate(rows):
        ry = y + hh + i * rh
        if r.get("hot"):
            box(slide, x, ry, w, rh - 0.04, fill="#FBEFEF", line=None,
                radius=False, who=f"mrow{i}-bg")
        text(slide, x + 0.10, ry, name_w - 0.14, rh - 0.04, r["name"], size=13,
             color=(RED if r.get("hot") else INK), anchor="middle", who=f"mrow{i}")
        for j, cell in enumerate(r["cells"]):
            text(slide, x + name_w + j * cw, ry, cw, rh - 0.04, cell, size=12,
                 color=(RED if r.get("hot") else GREY), align="center",
                 anchor="middle", who=f"mcell{i}{j}")


def blk_callout(slide, x, y, w, h, spec):
    tone = TONE.get(spec.get("tone", "navy"), NAVY)
    box(slide, x, y, w, h, fill=tone, line=None, who="callout")
    text(slide, x + 0.20, y, w - 0.40, h, spec["text"], size=17, color=WHITE,
         bold=True, align="center", anchor="middle", who="callout-t")


RENDER = {"cards": blk_cards, "bar": blk_bar, "rows": blk_rows,
          "compare": blk_compare, "matrix": blk_matrix, "callout": blk_callout}
