# -*- coding: utf-8 -*-
"""P6 用圖 —— 風險矩陣(緩解位移 + 殘餘風險)+ 右側四欄偵測訊號表。

規格來源:v4/notes/04_十頁內容_v2.md 的
「# P6 · 風險:七類八條,緩解位移與殘餘風險」一節之【視覺規格】區塊。

紅線:
- 只用 make_figs_v4 的色票常數(或由常數與黑/白調和出的階調),不出現新的品牌色值。
- 圖內最小字級 >= FS_MIN(9),存檔前由 save() 強制檢查。
- 不畫投影片標題、不畫頁面共通元素(右上角五格進度指示)—— 由組版程式負責。
- 負號一律 ASCII hyphen;不用 emoji / 全形減號 / U+2212。
- 文字寬度一律用 renderer 實測(不是估算),並以 bbox 斷言擋下重疊。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.colors as mcolors
from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle

from make_figs_v4 import (  # noqa: E402
    AMBER, GREEN, GREY, NAVY, ORANGE, RED,
    assert_min_fontsize, newfig, save,
)

# ------------------------------------------------------------------
# 版面常數
# ------------------------------------------------------------------
W_IN, H_IN = 14.0, 7.875          # 16:9

FS_BODY = 10.0                    # 表格內文 / 矩陣標籤(表格內文不得小於 10)
FS_SMALL = 9.0                    # in-text 引註與註腳(不得再小)
FS_TITLE = 12.0                   # 兩區的區塊小標
FS_AXIS = 11.0                    # 軸標題

MX0, MX1 = 0.055, 0.385           # 3x3 格線 x 範圍(左 58% 區內)
MY0, MY1 = 0.200, 0.850           # 3x3 格線 y 範圍
CW = (MX1 - MX0) / 3.0
CH = (MY1 - MY0) / 3.0
LABEL_BAND_X = 0.386              # 矩陣右側標籤帶(仍屬左區)
GUTTER_X = 0.594                  # 白槽(左右兩區之間,兩區不得互壓)
TX0, TX1 = 0.598, 0.988           # 右表 x 範圍(約佔全寬 42% 的內容區)
T_TOP, T_BOT = 0.912, 0.105       # 右表 y 範圍
RED_CORRIDOR_Y = 0.885            # R8 紅線的水平走廊(在矩陣上緣與標籤之上)


def mix(c1, c2, t):
    """兩色線性調和。只用來由機具色票常數 + 黑/白推階調,不引入新品牌色值。"""
    a, b = mcolors.to_rgb(c1), mcolors.to_rgb(c2)
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


C_RED = RED                                  # 行車安全 / 法律責任
C_DGREY = mix(GREY, "black", 0.55)           # 資料與模型品質
C_LGREY = mix(GREY, "white", 0.28)           # 組織 / 經濟 / 社會
C_TEXT = mix(GREY, "black", 0.72)
C_MUTED = mix(GREY, "black", 0.10)
C_RULE = mix(GREY, "white", 0.55)

BAND = [                                     # 左下淺綠 -> 對角淺黃 -> 右上淺紅
    mix(GREEN, "white", 0.88),
    mix(mix(GREEN, AMBER, 0.5), "white", 0.90),
    mix(AMBER, "white", 0.90),
    mix(mix(AMBER, RED, 0.5), "white", 0.91),
    mix(RED, "white", 0.91),
]

# ==================================================================
# 文字量測(renderer 實測)+ 可混排字級的斷行 / 繪製
# ==================================================================
_FIG = None
_WCACHE = {}


def wpt(s, fs, bold=False):
    """字串在該字級下的實際寬度(points)。"""
    key = (s, fs, bold)
    if key not in _WCACHE:
        t = _FIG.text(0, 0, s, fontsize=fs,
                      fontweight="bold" if bold else "normal")
        bb = t.get_window_extent(renderer=_FIG.canvas.get_renderer())
        t.remove()
        _WCACHE[key] = bb.width / _FIG.dpi * 72.0
    return _WCACHE[key]


def _tok(runs):
    """切 token:CJK 逐字可斷、拉丁整串不斷、nobreak 的 run 整塊不斷。"""
    out = []
    for r in runs:
        text, fs, color = r[0], r[1], r[2]
        bold = r[3] if len(r) > 3 else False
        nobreak = r[4] if len(r) > 4 else False
        if nobreak:
            out.append([text, fs, color, bold])
            continue
        buf = ""
        for ch in text:
            if ord(ch) > 127 or ch == " ":
                if buf:
                    out.append([buf, fs, color, bold])
                    buf = ""
                out.append([ch, fs, color, bold])
            else:
                buf += ch
        if buf:
            out.append([buf, fs, color, bold])
    return out


def _tw(t):
    return wpt(t[0], t[1], t[3])


def wrap_runs(runs, maxw_pt):
    lines, cur, curw = [], [], 0.0
    for tok in _tok(runs):
        w = _tw(tok)
        if cur and curw + w > maxw_pt:
            lines.append(cur)
            cur, curw = [], 0.0
            if tok[0] == " ":
                continue
        cur.append(tok)
        curw += w
    if cur:
        lines.append(cur)
    merged = []
    for ln in lines:
        m = []
        for t in ln:
            if m and m[-1][1:] == t[1:]:
                m[-1][0] += t[0]
            else:
                m.append(list(t))
        merged.append(m)
    return merged


def line_w_u(ln):
    return sum(_tw(t) for t in ln) / 72.0 / W_IN


def runs_w_u(runs):
    return sum(_tw(t) for t in _tok(runs)) / 72.0 / W_IN


def draw_lines(ax, lines, x0, y_top, line_h, ha="left"):
    for i, ln in enumerate(lines):
        y = y_top - i * line_h
        wu = line_w_u(ln)
        x = x0 if ha == "left" else (x0 - wu if ha == "right" else x0 - wu / 2)
        for t in ln:
            ax.text(x, y, t[0], ha="left", va="center", fontsize=t[1],
                    color=t[2], fontweight="bold" if t[3] else "normal",
                    zorder=6)
            x += _tw(t) / 72.0 / W_IN


# ---- 版面稽核:標籤 / 標記 bbox 不得互相重疊 ----
BOXES = []


def _reg(name, x0, x1, y0, y1):
    BOXES.append((name, x0, x1, y0, y1))


ALLOW = {("R8ring", "R8")}       # 紅虛線圈本來就套在 R8 實心圓外面


def audit_boxes():
    bad = []
    for i in range(len(BOXES)):
        for j in range(i + 1, len(BOXES)):
            a, b = BOXES[i], BOXES[j]
            if (a[0], b[0]) in ALLOW or (b[0], a[0]) in ALLOW:
                continue
            if a[1] < b[2] and b[1] < a[2] and a[3] < b[4] and b[3] < a[4]:
                bad.append((a[0], b[0]))
    assert not bad, "左圖元素重疊:%s" % bad
    over = [b[0] for b in BOXES if b[2] > GUTTER_X - 0.008]
    assert not over, "左區元素壓到白槽:%s" % over


# ==================================================================
# 資料
# ==================================================================
RISKS = {                       # st: thick=高 / thin=中 / dash=低 / none=尚無方案
    "R1": dict(pre=(0.255, 0.690), post=(0.238, 0.548), c=C_DGREY, st="thin"),
    "R2": dict(pre=(0.310, 0.672), post=(0.245, 0.500), c=C_DGREY, st="thin"),
    "R3": dict(pre=(0.352, 0.795), post=(0.255, 0.822), c=C_DGREY, st="thin"),
    "R4": dict(pre=(0.176, 0.822), post=(0.216, 0.806), c=C_RED, st="dash"),
    "R5": dict(pre=(0.196, 0.450), post=(0.120, 0.450), c=C_LGREY, st="thick"),
    "R6": dict(pre=(0.352, 0.470), post=(0.262, 0.450), c=C_LGREY, st="thin"),
    "R7": dict(pre=(0.185, 0.665), post=(0.118, 0.590), c=C_LGREY, st="thick"),
    "R8": dict(pre=(0.100, 0.775), post=None, c=C_RED, st="none"),
}

COL_RATIO = [18, 30, 24, 28]
HEADER = ["編號與類別", "緩解措施", "緩解自身的風險", "偵測訊號"]
G = FS_SMALL                    # in-text 引註(0.55 倍換算後不得低於 fs=9)

TABLE = [
    dict(no="R1", cat="技術局限",
         act=[("解釋:規則式脈絡層可逐條檢查;複核介面顯示外部證據"
               "(該路段速限來源)而非信心分數", FS_BODY, C_TEXT)],
         cost="規則層擋不住的情境仍回到黑箱",
         sig="複核者推翻模型判定的比例居高不下或不降"),
    dict(no="R2", cat="數據",
         act=[("審計:黃金題 + 抽樣雙人複核 + 脈絡資料來源版本快照", FS_BODY, C_TEXT)],
         cost="雙人複核使複核成本近倍增,需以抽樣比例控制",
         sig="交通標誌根因佔比偏離基準(基準見左下註)"),
    dict(no="R2 附", cat="數據",
         act=[("審計:脈絡資料進線前先做一致性檢查", FS_BODY, C_TEXT)],
         cost="地圖速限資料本身有誤時整批傳遞,且比模型錯更難察覺",
         sig="同一路段連續出現同向偏誤"),
    dict(no="R3", cat="數據",
         act=[("教育・介面", FS_BODY, C_TEXT),
              (" (Goddard et al., 2012)", G, C_MUTED, False, True),
              (":介面不顯示模型信心", FS_BODY, C_TEXT),
              (" (Guo et al., 2017)", G, C_MUTED, False, True),
              (",並在抽樣盲測組上做對照", FS_BODY, C_TEXT)],
         cost="不顯示信心使複核變慢,與時效缺口相衝",
         sig="盲測組與對照組的判定差異超過設計書所訂容忍值"),
    dict(no="R4", cat="倫理",
         act=[("問責:申訴機制到位前,本案產出不供個人考核使用", FS_BODY, C_TEXT)],
         cost="限制用途會降低客戶端採用意願",
         sig="駕駛端申訴請求無處可收,件數恆為零"),
    dict(no="R5", cat="社會性",
         act=[("教育:角色轉型說明 + 判準手冊共同編寫", FS_BODY, C_TEXT)],
         cost="參與式做法拉長判準定案時程",
         sig="複核團隊留任率或黃金題參與率下滑"),
    dict(no="R6", cat="經濟",
         act=[("審計:三道決策門逐段釋出額度", FS_BODY, C_TEXT)],
         cost="分段釋出使長週期工作包難以排人",
         sig="決策門審查時單位成本改善低於門檻"),
    dict(no="R7", cat="組織與管理",
         act=[("問責:贊助人指派 + 決策門出席為放行前提", FS_BODY, C_TEXT)],
         cost="決策門增加治理負擔與會議成本",
         sig="決策門會議連續兩次無高階出席"),
    dict(no="R8", cat="政治法律政策",
         act=[("問責:列為法務前置事項,本案不自行認定;", FS_BODY, C_TEXT),
              ("法務書面意見於 G1 前到位", FS_BODY, C_TEXT, True)],
         cost="無:目前沒有可執行的緩解措施",
         sig="客戶回頭標記的案件中出現援引我方誤報判定的事故爭議",
         focus=True),
]


# ==================================================================
# 左:2D 緩解位移矩陣
# ==================================================================
def _marker(ax, x, y, filled, color, label=None):
    if filled:
        ms = 17
        ax.plot([x], [y], marker="o", ms=ms, mfc=color, mec=color, mew=0,
                zorder=5, linestyle="none")
        ax.text(x, y, label, ha="center", va="center", fontsize=FS_SMALL,
                color="white", fontweight="bold", zorder=6)
    else:
        ms = 11
        ax.plot([x], [y], marker="o", ms=ms, mfc="white", mec=color, mew=1.8,
                zorder=5, linestyle="none")
    rx = ms / 2.0 / 72.0 / W_IN
    ry = ms / 2.0 / 72.0 / H_IN
    _reg((label or "o") + ("" if filled else "-post"),
         x - rx, x + rx, y - ry, y + ry)


def _arrow(ax, p, q, color, style):
    if style == "none":
        return
    kw = dict(color=color, zorder=4)
    if style == "thick":
        kw.update(lw=2.8)
    elif style == "thin":
        kw.update(lw=1.3)
    else:
        kw.update(lw=1.6, linestyle=(0, (2.4, 1.9)))
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13,
                                 shrinkA=10, shrinkB=7, **kw))


def draw_matrix(ax):
    # 區塊小標(不是投影片標題)+ 橘色母題點綴
    ax.add_patch(Rectangle((MX0, 0.938), 0.030, 0.007, fc=ORANGE, ec="none",
                           zorder=4))
    tx = MX0 + 0.040
    ttl = "緩解前 → 殘餘風險位移"
    ax.text(tx, 0.955, ttl, ha="left", va="center", fontsize=FS_TITLE,
            color=NAVY, fontweight="bold")
    ax.text(tx + wpt(ttl, FS_TITLE, True) / 72.0 / W_IN + 0.010, 0.953,
            "(NIST, 2023)", ha="left", va="center", fontsize=FS_SMALL,
            color=C_MUTED)

    for i in range(3):
        for j in range(3):
            ax.add_patch(Rectangle((MX0 + i * CW, MY0 + j * CH), CW, CH,
                                   fc=BAND[i + j], ec="white", lw=1.6, zorder=1))
    ax.add_patch(Rectangle((MX0, MY0), MX1 - MX0, MY1 - MY0, fc="none",
                           ec=C_RULE, lw=1.2, zorder=3))

    for i, s in enumerate(["低", "中", "高"]):
        ax.text(MX0 + (i + .5) * CW, 0.178, s, ha="center", va="top",
                fontsize=FS_BODY, color=C_TEXT)
        ax.text(0.046, MY0 + (i + .5) * CH, s, ha="right", va="center",
                fontsize=FS_BODY, color=C_TEXT)
    ax.text((MX0 + MX1) / 2, 0.140, "發生可能性", ha="center", va="top",
            fontsize=FS_AXIS, color=NAVY, fontweight="bold")
    ax.text(0.018, (MY0 + MY1) / 2, "對本案的衝擊", ha="center", va="center",
            rotation=90, fontsize=FS_AXIS, color=NAVY, fontweight="bold")

    # R8:紅色虛線圈(尚無可執行的緩解措施),周邊淨空
    r8 = RISKS["R8"]["pre"]
    rx = 0.026
    ry = rx * W_IN / H_IN
    ax.add_patch(Ellipse(r8, 2 * rx, 2 * ry, fc="none", ec=C_RED, lw=1.8,
                         linestyle=(0, (3.0, 2.2)), zorder=4))
    _reg("R8ring", r8[0] - rx, r8[0] + rx, r8[1] - ry, r8[1] + ry)

    for k in ["R5", "R6", "R7", "R1", "R2", "R3", "R4", "R8"]:
        d = RISKS[k]
        if d["post"] is not None:
            _arrow(ax, d["pre"], d["post"], d["c"], d["st"])
            _marker(ax, d["post"][0], d["post"][1], False, d["c"], label=k)
        _marker(ax, d["pre"][0], d["pre"][1], True, d["c"], label=k)

    # ---- 標籤:leader line 連回圓心;寧可拉長 leader,也不讓標籤重疊 ----
    def lab(name, anchor, runs, frm, ha="left"):
        w = runs_w_u(runs)
        x0 = anchor[0] if ha == "left" else (
            anchor[0] - w if ha == "right" else anchor[0] - w / 2)
        fs = max(r[1] for r in runs)
        hh = fs * 1.25 / 2 / 72.0 / H_IN
        draw_lines(ax, [_tok(runs)], x0, anchor[1], 0.0)
        _reg(name, x0 - 0.002, x0 + w + 0.002, anchor[1] - hh, anchor[1] + hh)
        tx0 = x0 if frm[0] < x0 else x0 + w
        ax.plot([tx0, frm[0]], [anchor[1], frm[1]], lw=0.8, color=C_RULE,
                zorder=2)

    lab("L8", (0.115, 0.868),
        [("R8 誤報紀錄舉證地位:尚無緩解方案", FS_BODY, C_RED, True)],
        (0.112, 0.822))
    lab("L4", (0.186, 0.775),
        [("R4 無申訴管道(幾乎沒動)", FS_BODY, C_RED, True)], (0.184, 0.810))
    lab("L7", (0.185, 0.708), [("R7 缺高層支持", FS_BODY, C_TEXT)],
        (0.185, 0.683), ha="center")
    lab("L5", (0.196, 0.400), [("R5 角色改變抵觸", FS_BODY, C_TEXT)],
        (0.199, 0.437))
    lab("L6", (0.290, 0.400), [("R6 回本難證與競合", FS_BODY, C_TEXT)],
        (0.350, 0.457))
    lab("L3", (LABEL_BAND_X, 0.812),
        [("R3 自動化偏差", FS_BODY, C_TEXT),
         (" (Parasuraman & Manzey, 2010)", G, C_MUTED, False, True)],
        (0.362, 0.798))
    lab("L1", (LABEL_BAND_X, 0.722),
        [("R1 不可解釋", FS_BODY, C_TEXT),
         (" (Rudin, 2019)", G, C_MUTED, False, True)], (0.265, 0.700))
    lab("L2", (LABEL_BAND_X, 0.640), [("R2 資料級聯", FS_BODY, C_TEXT)],
        (0.320, 0.672))

    # ---- 圖例:放左下角空白格內 ----
    lx, ly, dy = MX0 + 0.012, MY0 + CH - 0.028, 0.0255
    ax.plot([lx + 0.008], [ly], marker="o", ms=11, mfc=C_DGREY, mec=C_DGREY,
            linestyle="none", zorder=5)
    ax.text(lx + 0.024, ly, "緩解前", ha="left", va="center", fontsize=FS_SMALL,
            color=C_TEXT)
    ax.plot([lx + 0.008], [ly - dy], marker="o", ms=8, mfc="white", mec=C_DGREY,
            mew=1.6, linestyle="none", zorder=5)
    ax.text(lx + 0.024, ly - dy, "殘餘風險", ha="left", va="center",
            fontsize=FS_SMALL, color=C_TEXT)
    ax.text(lx, ly - 2 * dy, "箭頭樣式 = 成功可能性", ha="left", va="center",
            fontsize=FS_SMALL, color=C_TEXT, fontweight="bold")
    for i, (st, txt) in enumerate([("thick", "高"), ("thin", "中"),
                                   ("dash", "低")]):
        yy = ly - (3 + i) * dy
        kw = dict(color=C_TEXT)
        if st == "thick":
            kw["lw"] = 2.8
        elif st == "thin":
            kw["lw"] = 1.3
        else:
            kw.update(lw=1.6, linestyle=(0, (2.4, 1.9)))
        ax.plot([lx + 0.002, lx + 0.026], [yy, yy], zorder=5, **kw)
        ax.text(lx + 0.034, yy, txt, ha="left", va="center", fontsize=FS_SMALL,
                color=C_TEXT)
    yy = ly - 6 * dy
    ax.add_patch(Ellipse((lx + 0.014, yy), 0.021, 0.021 * W_IN / H_IN,
                         fc="none", ec=C_RED, lw=1.4, linestyle=(0, (2.4, 1.8)),
                         zorder=5))
    ax.text(lx + 0.034, yy, "尚無緩解方案", ha="left", va="center",
            fontsize=FS_SMALL, color=C_RED)

    # ---- 顏色語意帶:紅 + 兩級灰階(不引入第五個語意色)----
    x = MX0
    for col, txt in [(C_RED, "紅 = 行車安全或法律責任(R4、R8)"),
                     (C_DGREY, "深灰 = 資料與模型品質(R1-R3)"),
                     (C_LGREY, "淺灰 = 組織 / 經濟 / 社會(R5-R7)")]:
        ax.add_patch(Rectangle((x, 0.079), 0.011, 0.013, fc=col, ec="none",
                               zorder=4))
        ax.text(x + 0.016, 0.0855, txt, ha="left", va="center",
                fontsize=FS_SMALL, color=C_TEXT)
        x += 0.016 + wpt(txt, FS_SMALL) / 72.0 / W_IN + 0.018
    assert x < GUTTER_X, "顏色語意帶超出左區(x=%.3f)" % x


# ==================================================================
# 右:四欄偵測訊號表
# ==================================================================
def draw_table(ax):
    ax.add_patch(Rectangle((TX0, 0.938), 0.030, 0.007, fc=ORANGE, ec="none",
                           zorder=4))
    ax.text(TX0 + 0.040, 0.955, "緩解措施、緩解自身的風險與偵測訊號",
            ha="left", va="center", fontsize=FS_TITLE, color=NAVY,
            fontweight="bold")

    tw = TX1 - TX0
    tot = float(sum(COL_RATIO))
    xs, acc = [], TX0
    for r in COL_RATIO:
        xs.append(acc)
        acc += tw * r / tot
    xs.append(TX1)
    pad = 0.0042
    maxw = [(xs[i + 1] - xs[i] - 2 * pad) * W_IN * 72 for i in range(4)]
    line_h = 12.6 / 72.0 / H_IN

    rows = []
    for d in TABLE:
        c1 = (wrap_runs([(d["no"], FS_BODY, C_TEXT, True)], maxw[0])
              + wrap_runs([(d["cat"], FS_BODY, C_TEXT)], maxw[0]))
        c2 = wrap_runs(d["act"], maxw[1])
        c3 = wrap_runs([(d["cost"], FS_BODY, C_TEXT)], maxw[2])
        c4 = wrap_runs([(d["sig"], FS_BODY, C_TEXT)], maxw[3])
        rows.append(dict(cells=[c1, c2, c3, c4],
                         n=max(len(c1), len(c2), len(c3), len(c4)),
                         focus=d.get("focus", False)))
    print("   每列行數:", [r["n"] for r in rows], "合計", sum(r["n"] for r in rows))

    head_h = 0.040
    avail = (T_TOP - head_h) - T_BOT
    need = sum(r["n"] for r in rows) * line_h
    vpad = (avail - need) / len(rows)
    assert vpad > 0.006, "四欄表塞不下(列距 %.4f)" % vpad
    print("   列距 vpad = %.4f (%.3f 吋)" % (vpad, vpad * H_IN))

    ax.add_patch(Rectangle((TX0, T_TOP - head_h), tw, head_h, fc=NAVY, ec=NAVY,
                           zorder=3))
    for i, h in enumerate(HEADER):
        assert wpt(h, FS_BODY, True) <= maxw[i], "表頭欄 %d 過寬" % i
        ax.text(xs[i] + pad, T_TOP - head_h / 2, h, ha="left", va="center",
                fontsize=FS_BODY, color="white", fontweight="bold", zorder=5)

    y = T_TOP - head_h
    r8_center = None
    for k, r in enumerate(rows):
        rh = r["n"] * line_h + vpad
        if r["focus"]:
            fc = mix(NAVY, "white", 0.86)          # R8 底色深一階
        elif k % 2 == 0:
            fc = mix(NAVY, "white", 0.965)
        else:
            fc = "white"
        ax.add_patch(Rectangle((TX0, y - rh), tw, rh, fc=fc, ec="none", zorder=2))
        ax.plot([TX0, TX1], [y - rh, y - rh], lw=0.6, color=C_RULE, zorder=3)
        if r["focus"]:
            ax.add_patch(Rectangle((TX0, y - rh), 0.004, rh, fc=C_RED,
                                   ec="none", zorder=4))
            r8_center = y - rh / 2
        for i in range(4):
            lines = r["cells"][i]
            y_top = y - rh / 2 + (len(lines) - 1) * line_h / 2
            for ln in lines:
                assert line_w_u(ln) <= (xs[i + 1] - xs[i] - 2 * pad) + 1e-6, (
                    "欄 %d 有行超出欄寬" % i)
            draw_lines(ax, lines, xs[i] + pad, y_top, line_h)
        y -= rh

    for i in range(1, 4):
        ax.plot([xs[i], xs[i]], [T_TOP - head_h, y], lw=0.6, color=C_RULE,
                zorder=3)
    ax.add_patch(Rectangle((TX0, y), tw, T_TOP - y, fc="none", ec=C_RULE,
                           lw=1.0, zorder=4))

    note = ("R2 偵測訊號的基準 = 某小型車隊單月樣本的全部誤報中 103 / 124 = 83% "
            "屬交通標誌辨識根因;此為該樣本內的比例,不是全公司數字。")
    nl = wrap_runs([(note, FS_SMALL, C_MUTED)], tw * W_IN * 72)
    draw_lines(ax, nl, TX0, y - 0.030, 12.0 / 72.0 / H_IN)
    assert y - 0.030 - len(nl) * 12.0 / 72.0 / H_IN > 0.01, "表下註腳被裁切"
    return r8_center


def draw_r8_link(ax, r8_row_y):
    """R8 那一列拉一條紅色細線,連到左圖的紅色虛線圈(錄影停頓點)。"""
    if r8_row_y is None:
        return
    r8 = RISKS["R8"]["pre"]
    ax.plot([TX0, GUTTER_X, GUTTER_X, r8[0] - 0.022],
            [r8_row_y, r8_row_y, RED_CORRIDOR_Y, RED_CORRIDOR_Y],
            lw=0.85, color=C_RED, alpha=0.45, zorder=3,
            linestyle=(0, (3.6, 2.6)), solid_capstyle="round")
    ax.add_patch(FancyArrowPatch((r8[0] - 0.022, RED_CORRIDOR_Y),
                                 (r8[0] - 0.022, r8[1] + 0.040),
                                 arrowstyle="-|>", mutation_scale=11, lw=0.85,
                                 color=C_RED, alpha=0.45, zorder=3,
                                 linestyle=(0, (3.6, 2.6))))


def build():
    global _FIG
    BOXES.clear()
    _WCACHE.clear()
    fig, ax = newfig(W_IN, H_IN)                   # 不畫投影片標題
    # 讓 0-1 座標系正好等於整張畫布,量到的 point 寬度才能直接換算成座標
    ax.set_position([0, 0, 1, 1])
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="none", zorder=0))
    _FIG = fig
    fig.canvas.draw()
    draw_matrix(ax)
    r8_row_y = draw_table(ax)
    draw_r8_link(ax, r8_row_y)
    audit_boxes()
    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_06")
