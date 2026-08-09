# -*- coding: utf-8 -*-
"""第 1 段:封面 + P1-P4(page_idx 0, 1, 2, 3, 4)。

只准動這個檔,不要動 build_deck_v4.py,也不要動另外兩個分段模組。

怎麼填
------
    def build(prs, ctx):
        s = ctx["new_slide"](prs, 1, ctx=ctx)              # 開頁 + 標題 + 五段導軌
        ctx["place_fig"](s, "fig_v4_01.png", top=ctx["TOP"])   # 100% 原尺寸,不縮放
        ctx["place_slide_text"](s, [
            dict(id="P1-T01", x=0.55, y=6.30, w=10.6, h=0.5,
                 text="……", size=12, color=ctx["NAVY"], bold=True),
        ])

ctx 有什麼(三段共用,照這個用,不要自己重造)
--------------------------------------------
  helper   new_slide(prs, idx, sub=None, title=None, ctx=ctx) · blank_slide ·
           page_header · place_slide_text(slide, blocks) · place_fig(slide, name,
           left=None, top=TOP, center=True) · fig_inches(name) ·
           speaker_notes(slide, text) · txt / header / picture / note / card ·
           rgb("#1F4E79") · assert_clear_of_safe(x, y, w, h, who)
  色票     NAVY(#1F4E79)· ORANGE(#E8833A)· DEEP_ORANGE(#B45F1F)·
           RED · GREY · DARK · WHITE · LIGHT · FONT
  版面     W H TOP BOT SAFE_R SAFE_B SAFE_X SAFE_Y MIN_PT CARD_W CARD_GAP CARD_X0
  頁序     SECTIONS · PAGE_TITLES · PAGE_SECTION · PAGE_FIG · FIG_INCHES · FIG · V4
  emitted  框架用來對頁號;開頁時把 ctx 傳進 new_slide 就會自動記,別自己改。

規則(踩到就是內容出錯,不是風格問題)
--------------------------------------
  1. 標題只由 new_slide / page_header 放,**不要再加標題文字框**;圖裡也沒有標題。
  2. 文字框一律走 place_slide_text —— 它會擋掉 <12pt 與落進右下淨空區的框。
  3. 圖 100% 原尺寸置入,絕不縮放。
  4. 移出圖的文字一個字都不能少;P2 的來源是 `figs.fig_v4_02.SLIDE_TEXT`
     (該常數已取代 notes/14 的「區塊 1」,後者的數字整組作廢),本檔一律 import,不手抄。
  5. 內容以 notes/04_十頁內容_v2.md 的「投影片文字」節為準,不得自行改寫或加料。

本段負責的頁
------------
  0  封面(無 header:PAGE_TITLES[0] 是 None,new_slide 會自動略過標題)
  1  P1 用例:兩階段推論,與它下游那道人工防線        圖 fig_v4_01.png(12.20 x 5.70)
  2  P2 為什麼是現在:工作量沒變多,客戶要的時效變了  圖 fig_v4_02.png(11.95 x 2.81)
  3  P3 發現過程:兩種病,兩個缺口                    圖 fig_v4_03.png(9.69 x 4.93)
  4  P4 我們看不見的那一半:有資料,沒有習慣          圖 fig_v4_04.png(10.07 x 5.62)

圖的墨跡範圍(文字框只放在圖外的留白,不疊墨跡)
------------------------------------------------
  fig_01 12.20 x 5.70 滿版,四邊無白邊 → 文字框只能放在圖下緣(y >= 6.78)。
  fig_02 11.95 x 2.81 → 圖上、圖下兩條帶都是空的,移出的 14 塊全放這兩條帶。
  fig_03  9.69 x 4.93 → 置中後圖下緣 5.98,下方整條空。
  fig_04 10.07 x 5.62 → 置中後圖下緣 6.67,下方整條空。
"""
import unicodedata

from pptx.util import Inches

from figs.fig_v4_02 import SLIDE_TEXT as P2T

# ------------------------------------------------------------------
# 版面常數(本檔自用)
# ------------------------------------------------------------------
X0 = 0.55                 # 內容左緣
W_FULL = 12.20            # 全寬(0.55 -> 12.75)
W_SAFE = 10.70            # 避開右下淨空區的寬度(0.55 -> 11.25)
Y_SAFE = 6.35             # 淨空區上緣;超過這條線的框寬度只能到 W_SAFE
Y_BOTTOM = 7.44           # 底緣硬上限(版面 7.5 減 0.06 安全邊)

# 🔴 高度算法(本檔唯一一套,四頁共用)
#    1. 用 PIL 載入 Microsoft JhengHei,以 getlength() 逐字模擬換行 -> 實際行數 n
#    2. h = n × (size/72) × LS + 2 × PAD
#    3. 框與框之間至少 GAP;算完由 _audit() 用程式 assert 兩兩不重疊、底緣 <= Y_BOTTOM
#
#    LS 是「每行佔幾個字級」。PowerPoint 的 line_spacing 倍數是乘在字型自然行高
#    (Microsoft JhengHei = ascent+descent = 1.4375 em)上,所以送進 pptx 的倍數
#    必須是 LS / LINE_EM,才會真的排成 LS × 字級。
LINE_EM = 1.4375          # msjh.ttc:(ascent 18 + descent 5) / 16px em
LS_DENSE = 1.20           # 密排頁(P2):12pt × 1.20 = 每行 0.20 吋
LS_LOOSE = 1.45           # 有餘裕的頁(P1/P3/P4),看起來鬆一點
PAD = 0.03                # 文字框上下內距,各 0.03 吋(同步寫進 tIns/bIns)
GAP = 0.04                # 框與框最小間距
_EPS = 1e-9

_FONTS = {}


def _font(size, bold):
    """量測用的字面。取不到系統字型就回 None,改走全形字寬估算。"""
    key = (round(size, 1), bool(bold))
    if key not in _FONTS:
        try:
            from PIL import ImageFont
            path = "C:/Windows/Fonts/msjhbd.ttc" if bold else "C:/Windows/Fonts/msjh.ttc"
            _FONTS[key] = ImageFont.truetype(path, int(round(size * 96.0 / 72.0)))
        except Exception:
            _FONTS[key] = None
    return _FONTS[key]


def _u(s):
    """字串的「全形字寬」單位:全形 1、半形 0.5(量不到字型時的退路)。"""
    n = 0.0
    for ch in s:
        n += 1.0 if unicodedata.east_asian_width(ch) in ("W", "F") else 0.5
    return n


def _w(s, size, bold=False):
    """字串實寬(吋)。"""
    f = _font(size, bold)
    if f is None:
        return _u(s) * size / 72.0
    return f.getlength(s) / 96.0


# 不能出現在行首 / 行尾的標點(PowerPoint 的中文避頭尾;不模擬會少算行數)
_NO_START = "」』)】〕》〉,。、;:!?%‰・…~～ー"
_NO_END = "「『(【〔《〈"
_GLUE = ".,:+-/'"          # 數字內部的連接符,不在這裡斷行


def _tokens(s):
    """切成不可再拆的最小單位:ASCII 數字/字母連寫算一塊,中日文逐字一塊。"""
    out, i, n = [], 0, len(s)
    while i < n:
        ch = s[i]
        if ch.isascii() and ch.isalnum():
            j = i
            while j < n and s[j].isascii() and (s[j].isalnum() or s[j] in _GLUE):
                j += 1
            while j > i + 1 and s[j - 1] in _GLUE:
                j -= 1
            out.append(s[i:j])
            i = j
        else:
            out.append(ch)
            i += 1
    merged = []
    for t in out:
        if merged and t[0] in _NO_START:
            merged[-1] += t
        elif merged and merged[-1][-1] in _NO_END:
            merged[-1] += t
        else:
            merged.append(t)
    return merged


def _wrap(text, w, size, bold=False):
    """回傳這段文字在寬 w 吋的框裡實際會排成的每一行(逐字模擬)。"""
    limit = max(0.1, w - 0.02)          # 0.02 吋量測餘裕
    lines, cur, cw = [], "", 0.0
    for t in _tokens(text):
        tw = _w(t, size, bold)
        if cur and cw + tw > limit:
            lines.append(cur)
            cur, cw = t, tw
        else:
            cur += t
            cw += tw
    lines.append(cur)
    return lines or [""]


def _nlines(paras, w, size, bold=False):
    return sum(len(_wrap(p, w, size, bold)) for p in paras)


def _blk(bag, bid, x, y, w, paras, size=12, ls=LS_DENSE, **kw):
    """把一塊文字排進 bag(高度照上面的算法算),回傳下一塊可用的 y(已含 GAP)。"""
    if isinstance(paras, str):
        paras = [paras]
    paras = list(paras)
    n = _nlines(paras, w, size, kw.get("bold", False))
    h = n * size * ls / 72.0 + 2 * PAD
    bag.append(dict(id=bid, x=x, y=y, w=w, h=h, text=paras,
                    size=size, spacing=ls / LINE_EM, _n=n, **kw))
    return y + h + GAP


def _pad_margins(boxes):
    """左右內距歸零(算寬度時就沒算它),上下各 0.03 吋 —— 與高度算法一致。"""
    for tb in boxes:
        tf = tb.text_frame
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = Inches(PAD)
    return boxes


def _audit(tag, bag, extra=(), y_limit=Y_BOTTOM):
    """🔴 程式 assert:所有框兩兩不重疊、不壓圖、底緣不出血。順便把 [y, y+h] 印出來。"""
    rects = [(b["id"], b["x"], b["y"], b["w"], b["h"], b["_n"]) for b in bag]
    rects += [(nm, x, y, w, h, -1) for nm, x, y, w, h in extra]
    print("[版面] %s" % tag)
    for bid, x, y, w, h, n in rects:
        print("       %-10s x %5.2f-%5.2f   y %5.3f-%5.3f   h %.3f   %s"
              % (bid, x, x + w, y, y + h, h,
                 ("%d 行" % n) if n >= 0 else "(圖)"))
    for bid, x, y, w, h, n in rects:
        if n >= 0 and y + h > y_limit + _EPS:
            raise AssertionError("%s / %s 底緣 %.3f 超過 %.2f 吋"
                                 % (tag, bid, y + h, y_limit))
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if a[5] < 0 and b[5] < 0:
                continue
            ox = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
            oy = min(a[2] + a[4], b[2] + b[4]) - max(a[2], b[2])
            if ox > _EPS and oy > _EPS:
                raise AssertionError(
                    "%s:%s 與 %s 重疊(x 交 %.3f 吋、y 交 %.3f 吋)"
                    % (tag, a[0], b[0], ox, oy))
    print("       -> %d 框兩兩不重疊,底緣 %.3f <= %.2f 吋"
          % (len(bag), max(b["y"] + b["h"] for b in bag), y_limit))
    return bag


# ==================================================================
# 封面
# ==================================================================
def _cover(prs, ctx):
    s = ctx["new_slide"](prs, 0, ctx=ctx)
    txt, NAVY, GREY, DARK = ctx["txt"], ctx["NAVY"], ctx["GREY"], ctx["DARK"]
    ORANGE = ctx["ORANGE"]

    txt(s, 1.00, 1.90, 10.25, 1.05,
        "讓機器讀懂一次事件的完整脈絡", size=40, color=NAVY, bold=True)
    txt(s, 1.00, 3.05, 10.25, 0.60,
        "地端 AI 事件判讀 —— 六個月、三道決策門的立案提案", size=20, color=GREY)

    # 開場那一句(錄影開場的主文),與它的尺度限定小字必須同框出現
    txt(s, 1.00, 4.05, 10.25, 0.55,
        "今天,五個人要看完三千支影片;而客戶要的答案,兩天內。",
        size=18, color=ORANGE, bold=True)
    txt(s, 1.00, 4.52, 10.25, 0.35,
        "單一大型車隊 · 約 3,000 筆/天 · 5 位專職分析人員",
        size=12, color=GREY)

    txt(s, 1.00, 5.30, 10.25, 1.20,
        "Po-Kai Huang(學號 26254793)\n"
        "421104 Artificial Intelligence for Enterprises · Assessment 3\n"
        "2026 年 8 月",
        size=15, color=DARK, spacing=1.45)

    ctx["speaker_notes"](s, "今天,五個人要看完三千支影片;而客戶要的答案,兩天內。")
    return s


# ==================================================================
# P1 · 用例:兩階段推論,與它下游那道人工防線
# ==================================================================
def _p1(prs, ctx):
    s = ctx["new_slide"](prs, 1, ctx=ctx)
    box = ctx["place_fig"](s, "fig_v4_01.png", top=ctx["TOP"])   # 12.20 x 5.70

    # fig_01 是滿版、四邊無白邊 → 唯一可用的留白是圖下緣 (6.75) 以下。
    y = box["bottom"] + 0.03
    bag = []
    _blk(bag, "P1-T01", X0, y, W_SAFE, [
        "提請核准:一個六個月、三道決策門的專案。"
        "架構邊界:本案不重新開啟架構選擇。",
        "前置是三件事:一組凍結的評估集、一份一致的標註、"
        "一層餵得進模型的脈絡 —— 那就是前三個工作包。",
    ], size=13, ls=LS_LOOSE, color=ctx["NAVY"], bold=True)
    _audit("P1", bag, extra=[("fig_01", box["left"], box["top"],
                              box["w"], box["h"])])
    _pad_margins(ctx["place_slide_text"](s, bag))

    ctx["speaker_notes"](s, _NOTES_P1)
    return s


# ==================================================================
# P2 · 為什麼是現在(移出圖的 14 塊全部由本頁的原生文字框承載)
# ==================================================================
def _rows(block, key="rows"):
    out = []
    for r in block.get(key, []):
        out.append(r["text"] if isinstance(r, dict) else r)
    return out


def _split_acct(s, marker="當責:"):
    """把「當責 / 期限 / 會改變的決策」那條尾巴切下來。回傳 (正文, 尾巴)。"""
    i = s.find(marker)
    if i < 0:
        return s, ""
    head = s[:i].rstrip().rstrip("——").rstrip()
    return head, s[i:]


def _p2(prs, ctx):
    """P2 是全份唯一的密排頁。可用高度只有這些,別再往裡塞:

        標題下緣 0.96 -> 上帶 1.86 吋(6 行) -> 圖 2.81 吋(不可縮放)
        -> 下帶 1.76 吋(7 行 / 4 個框) -> 底緣 7.43(上限 7.44)

    上帶把三格算式各自的「證據等級」收進該格自己的框(原本是一條 12.2 吋的
    大框硬吞三段,一格 2 行的字排成 3 行就會壓到下一框 —— 那正是這一輪的
    fatal)。下帶只放三塊:母體宣告、業務基準、四倍以上;放不下的整塊移進
    講者備註,清單見 _P2_MOVED。
    """
    s = ctx["new_slide"](prs, 2, ctx=ctx)
    NAVY, DARK, GREY = ctx["NAVY"], ctx["DARK"], ctx["GREY"]
    DEEP_ORANGE, ORANGE = ctx["DEEP_ORANGE"], ctx["ORANGE"]

    a1t = P2T["A1_TITLE"]["text"]
    c1 = _rows(P2T["A1_CELL1"])
    c2 = _rows(P2T["A1_CELL2"])
    c3 = _rows(P2T["A1_CELL3"])
    a2a = P2T["A2_PULLQUOTE"]["text"]
    a2b = P2T["A2_PULLQUOTE"]["second"]["text"]
    a3 = P2T["A3_DIVIDER"]["text"]
    b1 = P2T["B1_SCOPE"]["rows"]
    d_title = P2T["D_STRESS"]["title"]["text"]
    d_rows = _rows(P2T["D_STRESS"])
    d_cite = P2T["D_STRESS"]["intext"]["text"]
    b2l = _rows(P2T["B2_BASELINE"], "left")
    b2m = _rows(P2T["B2_BASELINE"], "mid")
    b2r = _rows(P2T["B2_BASELINE"], "right")
    b3 = P2T["B3_POPULATION"]["text"]
    f = _rows(P2T["F_THROUGHPUT"])
    g1 = _rows(P2T["C1_GROWTH"])
    g2 = _rows(P2T["C2_STEP"])
    e = P2T["E_FOOTER"]["text"]

    # ---- 12pt 下限 + 圖不可縮放 = 這一頁的容量硬是少於 14 塊的總字數。
    #      正面留下:三格算式(含各自的證據等級)、尖峰結論、口徑分隔句、
    #                母體宣告、業務基準與它的證據等級、階梯算式、四倍以上。
    #      移進講者備註的整塊列在 _P2_MOVED —— 那是這一輪付出的代價,不掩飾。
    c3_note = c3[3].split("下緣 74%")[0].rstrip()
    c3_tail = "下緣 74%" + c3[3].split("下緣 74%")[1]
    b2l2_head, b2l2_tail = _split_acct(b2l[2])
    moved = [
        c3_tail, b2l2_tail, b2r[0], b2r[1], b3,
        d_title, d_rows[0] + d_rows[1], d_rows[2], d_rows[3], d_rows[4] + d_cite,
        f[0] + f[1], f[2],
        g1[0] + g1[1], g1[2], g1[3],
        g2[1],
    ]

    bag = []
    # ============ 上帶(0.96 -> 2.72):平均編制口徑算式帶 ============
    y = 0.96
    y = _blk(bag, "P2-A1T", X0, y, W_FULL, [a1t], 12, color=DARK, bold=True)

    # 三格各自兩個框(算式框 + 該格自己的證據等級框),欄寬照實測字寬配。
    # 原本三格的註被併成一條 12.2 吋大框硬吞,那條框只給了 2 行的高度、實排 3 行,
    # 於是第 3 行壓到下一框 —— 這一輪的 fatal 就是這麼來的。現在一格排錯行只會撐高
    # 自己那一格,由 _audit() 直接擋下,壓不到別人。
    cols = [(0.55, 3.20, c1[0], c1[1], c1[2], NAVY, False),
            (3.87, 4.20, c2[0], c2[1], c2[2], NAVY, False),
            (8.19, 4.35, c3[0], c3[1] + "　" + c3[2], c3_note,
             DEEP_ORANGE, True)]
    ends = []
    for cx, cw, lab, val, note, col, bd in cols:
        yy = _blk(bag, "P2-A1@%.2f" % cx, cx, y, cw, [lab, val], 12,
                  color=col, bold=bd)
        ends.append(_blk(bag, "P2-A1n@%.2f" % cx, cx, yy, cw, [note], 12,
                         color=GREY))
    y = max(ends)

    # A2 引言 + 徵調研發那一句
    y = _blk(bag, "P2-A2", X0, y, W_FULL, [a2a + "　" + a2b], 12,
             color=NAVY, bold=True)
    # A3 口徑分隔句(算式帶與主圖的分界)
    y = _blk(bag, "P2-A3", X0, y, W_FULL, [a3], 12, color=GREY, align="center")

    # ============ 圖:11.95 x 2.81,100% 原尺寸置中 ============
    # 文字與圖之間留 0.02;框本身上下各有 0.03 內距,所以字與墨跡實距 0.05。
    box = ctx["place_fig"](s, "fig_v4_02.png", top=y - GAP + 0.02)

    # ============ 下帶(圖下緣 -> 7.44):只剩 7 行,四個框 ============
    y = box["bottom"] + 0.02
    y = _blk(bag, "P2-B1", X0, y, W_SAFE,
             [b1[0], b1[1] + "　" + b2l[0],
              b2m[0] + "(" + b2m[1] + ")"],
             12, color=DARK)
    y = _blk(bag, "P2-B2", X0, y, W_SAFE, [b2l[1]], 12, color=ORANGE, bold=True)
    y = _blk(bag, "P2-B2n", X0, y, W_SAFE, [b2l2_head], 12, color=GREY)
    y = _blk(bag, "P2-E", X0, y, W_SAFE, [g2[0], e], 12,
             color=DARK, bold=True, align="center")

    _audit("P2", bag, extra=[("fig_02", box["left"], box["top"],
                              box["w"], box["h"])])
    _pad_margins(ctx["place_slide_text"](s, bag))

    ctx["speaker_notes"](s, _NOTES_P2 + "\n\n補充說明(講述時帶到,正面沒有印):\n"
                         + "\n".join("· " + t for t in moved))
    _P2_MOVED[:] = moved
    return s


# 正面放不下、改由講者備註承載的整塊(交付時要據實回報,不是「已完成」)
_P2_MOVED = []


# ==================================================================
# P3 · 發現過程:兩種病,兩個缺口
# ==================================================================
def _p3(prs, ctx):
    s = ctx["new_slide"](prs, 3, ctx=ctx)
    box = ctx["place_fig"](s, "fig_v4_03.png", top=ctx["TOP"])   # 9.69 x 4.93

    # 圖裡已經有:樣本限定條、雙欄對照表、兩個缺口、103/124、速限資料、漏放預告。
    # 只補圖裡沒有的那一句(「同一把尺」的完整判準句)。
    bag = []
    _blk(bag, "P3-T01", X0, box["bottom"] + 0.22, W_SAFE, [
        "這兩個比例共用同一把尺,而那把尺的一致性我們從來沒量過"
        " —— 不比誰準,只指出錯的性質不同。",
    ], size=16, ls=LS_LOOSE, color=ctx["NAVY"], bold=True)
    _audit("P3", bag, extra=[("fig_03", box["left"], box["top"],
                              box["w"], box["h"])])
    _pad_margins(ctx["place_slide_text"](s, bag))

    ctx["speaker_notes"](s, _NOTES_P3)
    return s


# ==================================================================
# P4 · 我們看不見的那一半:有資料,沒有習慣
# ==================================================================
def _p4(prs, ctx):
    s = ctx["new_slide"](prs, 4, ctx=ctx)
    box = ctx["place_fig"](s, "fig_v4_04.png", top=ctx["TOP"])   # 10.07 x 5.62

    # 圖裡已經有:資料鏈路(做得到 / 沒有在做)、39 筆拆解、12 是下限、假說框、
    # 誤報與漏放的代價對比、資料難度三格。只補圖裡沒有的那一句結論(否決型護欄)。
    bag = []
    _blk(bag, "P4-T01", X0, box["bottom"] + 0.10, W_SAFE, [
        "成本不對稱:誤報只花人時;漏放是駕駛沒收到那次警示 → 漏放列為否決型護欄。",
    ], size=15, ls=LS_LOOSE, color=ctx["NAVY"], bold=True)
    _audit("P4", bag, extra=[("fig_04", box["left"], box["top"],
                              box["w"], box["h"])])
    _pad_margins(ctx["place_slide_text"](s, bag))

    ctx["speaker_notes"](s, _NOTES_P4)
    return s


# ==================================================================
# 講者備註 = notes/04 的「口白逐字」(投影片正面不印這些字)
# ==================================================================
_NOTES_P1 = (
    "地端 AI 的技術可行性,公司內部評估過,我是其中一員。今天我不是提一個新點子,"
    "是把它從技術研討,變成一個有業務數字、有驗證機制、有停止條件的正式立案。"
    "要建的能力:讓機器讀懂一次事件的完整脈絡——影片、客戶問題、規則——"
    "產出可交付的證據與描述。兩階段架構各位熟悉,自動化到第二階段就停了:"
    "剩下每一筆,都要由人看過。這道防線有兩種單價。看畫面就能判的,一筆二十秒。"
    "要離開畫面去找證據的——那面牌是什麼、速限多少——一筆五分多鐘。差約十六倍,"
    "差別不在人,在證據在不在畫面裡。我請委員會核准一個六個月、三道決策門的專案:"
    "在客戶要的兩天內交出分析,第一次量得到自己漏掉什麼。要建它,得先有凍結的評估集、"
    "一致的標註、餵進模型的脈絡,那是前三個工作包。本案不重新開啟架構選擇。"
)

_NOTES_P2 = (
    "利用率七成四到一百零七:平均還好,尖峰這五個人已經不夠——折算三點七到五點四人,"
    "我們只有五個。一件爭議目前要兩到五天,現況約一半超過兩天;客戶要兩天、單純案件當天,"
    "那是客戶期望,不是簽了的服務水準。這兩到五天花在哪裡,我拆開了:排隊零到一天、"
    "撈數據半天、判讀一到三天、內部覆核半天、回信半天。撈數據加判讀,就是模型幫得上的"
    "那兩段,佔六成到六成四。這兩段之所以慢,是同一個原因——模型看不到畫面外的東西。"
    "這是營運端估計,不是量測;前六週交出正式拆解,不成立就轉排班。二十秒是營運上的估計,"
    "還沒有正式量過——第六週交出正式基準,G1 驗收。上線約五萬台,售出更多;落差就是"
    "排不了程的工作量,開通權在客戶手上。我不預測撞牆的時點;第六週對齊三個分母,"
    "成長不納入回報估算。成長是階梯:一個大型車隊上線,事件量一次跳兩成三,手上正在談一個。"
)

_NOTES_P3 = (
    "那我們的時間到底花在哪裡?我把最近一份判讀拆開來看。四台車、二十三天、"
    "一千六百四十七筆,一個小型車隊一個月,比例僅在此樣本內成立。行車輔助錯的是模型,"
    "駕駛監控錯的是人。一邊缺脈絡,判定依據不在畫面裡;一邊缺判準,同一段影片兩人不同答案。"
    "這兩個比例共用同一把尺,而那把尺的一致性我們從來沒量過——標註品質那一包第十週建立基線,"
    "G2 訂目標值。這個樣本一百二十四筆誤報,一百零三筆同一個根因:交通標誌辨識,八成三。"
    "漏放那一側只有一份很薄的樣本,下一頁講。修好它,誤報跟漏放一起改善——而誤報,"
    "就是我們今天在人工端花掉的時間。"
)

_NOTES_P4 = (
    "這是我們看得見的一半。看不見的那一半更麻煩。被判否決的那一流,沒有人回看。"
    "我們有資料,沒有習慣。唯一的漏放量測,是一份三十九筆的人工觸發測試,獨立樣本:"
    "漏偵十二筆,另外十筆無法歸類,約四分之一;報告上我們自己註明,十二是下限。"
    "這是我目前手上最強的線索,不是結論;前六週由評估底座那一包做成帶信賴區間的估計,"
    "不成立就換靶心,G1 判。這兩種錯的代價不對稱:誤報只花我們的人時,"
    "漏放是駕駛沒收到那次警示。所以漏放這一側就算樣本再薄,也要先把它量出來。"
    "這批資料難在三件事:收得不完整、標註本身就會錯、內部對同一個標籤還沒有一致的理解。"
    "文獻上講的「沒有真實資料就只能靠代理指標」,就是這件事。"
)


def build(prs, ctx):
    """建立封面與 P1-P4。"""
    _cover(prs, ctx)
    _p1(prs, ctx)
    _p2(prs, ctx)
    _p3(prs, ctx)
    _p4(prs, ctx)
