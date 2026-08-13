# -*- coding: utf-8 -*-
"""P6 用圖 —— 風險矩陣(緩解位移 + 殘餘風險)+ 右側三欄偵測訊號表。

規格來源:v4/notes/04_十頁內容_v2.md 的
「# P6 · 風險:七類八條,緩解位移與殘餘風險」一節之【視覺規格】區塊。

裁決 O(v4/notes/12_出圖稽核與畫布裁決.md §二)後的重畫版:
- 畫布**鎖死 12.2 x 5.7 吋** = 組版時內容區的實際形狀,置入縮放比 = 1.0,
  所以圖內 fs=9 在投影片上就是真的 9pt。**不得為了塞內容而放大畫布。**
- 塞不下時砍內容 / 把純文字移出圖,由組版程式以 PowerPoint 原生字型放置
  (向量、可縮放、永遠清晰;烘進 PNG 只會跟著被縮小)。
  本頁移出圖的三項見檔尾「移出圖、改由組版程式放的元素」清單。

紅線:
- 只用 make_figs_v4 的色票常數(或由常數與黑/白調和出的階調),不出現新的品牌色值。
- 圖內最小字級 >= FS_MIN(9),表格內文 >= 10;存檔前由 save() 強制檢查。
- 不畫投影片標題、不畫頁面共通元素(右上角五格進度指示)—— 由組版程式負責。
- 負號一律 ASCII hyphen;不用 emoji / 全形減號 / U+2212。
- 文字寬度一律用 renderer 實測(不是估算),並以 bbox 斷言擋下重疊。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
import matplotlib.colors as mcolors
from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle

# 共用機具的 save() 用 bbox_inches="tight",預設會在四周補 0.1 吋留白 ——
# 那會讓交件 PNG 變成 12.4 x 5.9 吋,置入 12.23 x 5.75 的內容區時縮放比掉到
# 0.975,fs=9 又變成 8.8pt。把 pad 歸零,PNG 才會等於畫布、縮放比才是 1.0。
# 只改本行程的 rcParam,不動 make_figs_v4.py(其他六支同時在跑)。
matplotlib.rcParams["savefig.pad_inches"] = 0.0

from make_figs_v4 import (  # noqa: E402
    AMBER, GREEN, GREY, NAVY, ORANGE, RED,
    assert_min_fontsize, newfig, save,
)

# ------------------------------------------------------------------
# 版面常數 —— 畫布尺寸是硬約束,不得放大(裁決 O)
# ------------------------------------------------------------------
W_IN, H_IN = 12.2, 5.7            # = build_deck 內容區 (W-1.1) x (H-TOP-BOT)

FS_BODY = 10.0                    # 表格內文 / 矩陣刻度 / 右側風險索引
FS_SMALL = 9.0                    # in-text 引註與圖例(不得再小)
FS_TITLE = 12.0                   # 兩區的區塊小標
FS_AXIS = 11.0                    # 軸標題

# ---- 左區:矩陣 ----
MX0, MX1 = 0.058, 0.298           # 3x3 格線 x 範圍
MY0, MY1 = 0.360, 0.880           # 3x3 格線 y 範圍
CW = (MX1 - MX0) / 3.0
CH = (MY1 - MY0) / 3.0

IDX_X = 0.308                     # 右側風險索引帶(仍屬左區)
IDX_R = 0.482                     # 索引帶右界
LEFT_R = 0.482                    # 左區右界

GUTTER_X = 0.490                  # 白槽中線(左右兩區之間,兩區不得互壓)

# ---- 右區:三欄表 ----
TX0, TX1 = 0.500, 0.997
T_TOP, T_BOT = 0.905, 0.045
HEAD_H = 0.046

RED_CORRIDOR_Y = 0.930            # R8 紅線的水平走廊(矩陣上緣與索引帶之上)

MS_PRE = 16.0                     # 實心圓(緩解前)直徑,points
MS_POST = 10.0                    # 空心圓(殘餘風險)直徑,points


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


def wu(s, fs, bold=False):
    """字串寬度換算成 0-1 座標。"""
    return wpt(s, fs, bold) / 72.0 / W_IN


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
        w = line_w_u(ln)
        x = x0 if ha == "left" else (x0 - w if ha == "right" else x0 - w / 2)
        for t in ln:
            ax.text(x, y, t[0], ha="left", va="center", fontsize=t[1],
                    color=t[2], fontweight="bold" if t[3] else "normal",
                    zorder=6)
            x += _tw(t) / 72.0 / W_IN


# ---- 版面稽核:標籤 / 標記 bbox 不得互相重疊,且都在容器框內 ----
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
    over = [b[0] for b in BOXES if b[2] > LEFT_R + 0.002]
    assert not over, "左區元素壓到白槽:%s" % over
    out = [b[0] for b in BOXES if b[1] < 0.004 or b[3] < 0.010 or b[4] > 0.990]
    assert not out, "左區元素超出畫布:%s" % out


# ==================================================================
# 資料
# ==================================================================
# 座標依 3x3 格位手排,同格內以 12px 為單位錯開;st: thick=高 / thin=中 /
# dash=低 / none=尚無方案。rad = 箭頭弧度,用來讓箭身避開其他圓。
RISKS = {
    "R1": dict(pre=(0.176, 0.855), post=(0.196, 0.665),
               c=C_DGREY, st="thin", rad=0.16),
    "R2": dict(pre=(0.238, 0.848), post=(0.144, 0.585),
               c=C_DGREY, st="thin", rad=-0.10),
    "R3": dict(pre=(0.272, 0.752), post=(0.176, 0.730),
               c=C_DGREY, st="thin", rad=-0.16),
    "R4": dict(pre=(0.206, 0.855), post=(0.206, 0.796),
               c=C_RED, st="dash", rad=0.0),
    "R5": dict(pre=(0.202, 0.608), post=(0.112, 0.612),
               c=C_LGREY, st="thick", rad=0.16),
    "R6": dict(pre=(0.256, 0.600), post=(0.172, 0.552),
               c=C_LGREY, st="thin", rad=0.16),
    "R7": dict(pre=(0.144, 0.760), post=(0.086, 0.560),
               c=C_LGREY, st="thick", rad=-0.14),
    "R8": dict(pre=(0.092, 0.790), post=None,
               c=C_RED, st="none", rad=0.0),
    # 🔴 讀法(i)造成的兩條新風險(裁決 21_ X-a)。兩條的錯誤後果不同量級 ——
    #    R9 落在安全(漏放真實危險事件)、R10 落在個人權益(駕駛被機器單方面駁回),
    #    刻意分開兩個位移,不得合併成一條。緩解主要靠「本案六個月不對外生效」,
    #    所以位移大但殘餘仍高 —— 它們掛在移交後那道獨立的門上。
    "R9": dict(pre=(0.286, 0.812), post=(0.228, 0.702),
               c=C_RED, st="dash", rad=0.12),
    "R10": dict(pre=(0.300, 0.688), post=(0.244, 0.620),
                c=C_RED, st="dash", rad=-0.12),
}

# 右側風險索引帶:編號 -> 短名(+ in-text 引註)。色塊 = 類別色。
INDEX = [
    ("R1", C_DGREY, "模型不可解釋", "(Rudin, 2019)", False),
    ("R2", C_DGREY, "資料級聯", None, False),
    ("R3", C_DGREY, "自動化偏差", "(Parasuraman & Manzey, 2010)", False),
    ("R4", C_RED, "無申訴管道 (幾乎沒動)", None, True),
    ("R5", C_LGREY, "角色改變抵觸", None, False),
    ("R6", C_LGREY, "回本難證與競合", None, False),
    ("R7", C_LGREY, "缺高層支持", None, False),
    # 「尚無緩解方案」由紅虛線圈 + 圖例 A 行負責,索引帶不再重複、避免壞斷行
    ("R8", C_RED, "誤報紀錄舉證地位", None, True),
    ("R9", C_RED, "自動結案的漏放", None, True),
    ("R10", C_RED, "自動結案的冤枉", None, True),
]

COL_RATIO = [17, 43, 40]
HEADER = ["編號與類別", "緩解措施", "偵測訊號"]
G = FS_SMALL                    # in-text 引註(不得低於 fs=9)

TABLE = [
    dict(no="R1", cat="技術局限",
         act=[("解釋:規則式脈絡層可逐條檢查;複核介面顯示外部證據"
               "(該路段速限來源)而非信心分數", FS_BODY, C_TEXT)],
         sig="複核者推翻模型判定的比例居高不下或不降"),
    dict(no="R2", cat="數據",
         act=[("審計:黃金題 + 抽樣雙人複核 + 脈絡資料來源版本快照",
               FS_BODY, C_TEXT)],
         sig="交通標誌根因佔比偏離基準(基準見頁腳)"),
    dict(no="R2 附", cat="數據",
         act=[("審計:脈絡資料進線前先做一致性檢查", FS_BODY, C_TEXT)],
         sig="同一路段連續出現同向偏誤"),
    dict(no="R3", cat="數據",
         act=[("教育・介面", FS_BODY, C_TEXT),
              (" (Goddard et al., 2012)", G, C_MUTED, False, True),
              (":介面不顯示模型信心", FS_BODY, C_TEXT),
              (" (Guo et al., 2017)", G, C_MUTED, False, True),
              (",並在抽樣盲測組上做對照", FS_BODY, C_TEXT)],
         sig="盲測組與對照組的判定差異超過設計書所訂容忍值"),
    dict(no="R4", cat="倫理",
         act=[("問責:申訴機制到位前,本案產出不供個人考核使用",
               FS_BODY, C_TEXT)],
         sig="駕駛端申訴請求無處可收,件數恆為零"),
    dict(no="R5", cat="社會性",
         act=[("教育:角色轉型說明 + 判準手冊共同編寫", FS_BODY, C_TEXT)],
         sig="複核團隊留任率或黃金題參與率下滑"),
    dict(no="R6", cat="經濟",
         act=[("審計:三道決策門逐段釋出額度", FS_BODY, C_TEXT)],
         sig="決策門審查時單位成本改善低於門檻"),
    dict(no="R7", cat="組織與管理",
         act=[("問責:贊助人指派 + 決策門出席為放行前提", FS_BODY, C_TEXT)],
         sig="決策門會議連續兩次無高階出席"),
    dict(no="R8", cat="政治法律政策",
         act=[("問責:列為法務前置事項,本案不自行認定;", FS_BODY, C_TEXT),
              ("法務書面意見於 G1 前到位", FS_BODY, C_TEXT, True)],
         sig="客戶回頭標記的案件中出現援引我方誤報判定的事故爭議",
         focus=True),
]


# ==================================================================
# 左:2D 緩解位移矩陣
# ==================================================================
def _marker(ax, key, x, y, filled, color, label=None):
    ms = MS_PRE if filled else MS_POST
    if filled:
        ax.plot([x], [y], marker="o", ms=ms, mfc=color, mec=color, mew=0,
                zorder=5, linestyle="none")
        ax.text(x, y, label, ha="center", va="center", fontsize=FS_SMALL,
                color="white", fontweight="bold", zorder=6)
    else:
        ax.plot([x], [y], marker="o", ms=ms, mfc="white", mec=color, mew=1.7,
                zorder=5, linestyle="none")
    rx = ms / 2.0 / 72.0 / W_IN
    ry = ms / 2.0 / 72.0 / H_IN
    _reg(key, x - rx, x + rx, y - ry, y + ry)


def _arrow(ax, p, q, color, style, rad):
    if style == "none":
        return
    kw = dict(color=color, zorder=4)
    if style == "thick":
        kw.update(lw=2.6)
    elif style == "thin":
        kw.update(lw=1.3)
    else:
        kw.update(lw=1.6, linestyle=(0, (2.2, 1.7)))
    ax.add_patch(FancyArrowPatch(
        p, q, arrowstyle="-|>", mutation_scale=12,
        connectionstyle="arc3,rad=%.3f" % rad,
        shrinkA=9, shrinkB=6.5, **kw))


def draw_matrix(ax):
    # 區塊小標(不是投影片標題)+ 橘色母題點綴
    ax.add_patch(Rectangle((MX0, 0.940), 0.026, 0.009, fc=ORANGE, ec="none",
                           zorder=4))
    tx = MX0 + 0.036
    ttl = "緩解前 -> 殘餘風險位移"
    ax.text(tx, 0.957, ttl, ha="left", va="center", fontsize=FS_TITLE,
            color=NAVY, fontweight="bold")
    ax.text(tx + wu(ttl, FS_TITLE, True) + 0.009, 0.955, "(NIST, 2023)",
            ha="left", va="center", fontsize=FS_SMALL, color=C_MUTED)

    for i in range(3):
        for j in range(3):
            ax.add_patch(Rectangle((MX0 + i * CW, MY0 + j * CH), CW, CH,
                                   fc=BAND[i + j], ec="white", lw=1.5,
                                   zorder=1))
    ax.add_patch(Rectangle((MX0, MY0), MX1 - MX0, MY1 - MY0, fc="none",
                           ec=C_RULE, lw=1.2, zorder=3))

    for i, s in enumerate(["低", "中", "高"]):
        ax.text(MX0 + (i + .5) * CW, 0.345, s, ha="center", va="top",
                fontsize=FS_BODY, color=C_TEXT)
        ax.text(MX0 - 0.010, MY0 + (i + .5) * CH, s, ha="right", va="center",
                fontsize=FS_BODY, color=C_TEXT)
    ax.text((MX0 + MX1) / 2, 0.300, "發生可能性", ha="center", va="top",
            fontsize=FS_AXIS, color=NAVY, fontweight="bold")
    ax.text(0.018, (MY0 + MY1) / 2, "對本案的衝擊", ha="center", va="center",
            rotation=90, fontsize=FS_AXIS, color=NAVY, fontweight="bold")

    # R8:紅色虛線圈(尚無可執行的緩解措施),周邊淨空 >= 24px
    r8 = RISKS["R8"]["pre"]
    rx = 0.018
    ry = rx * W_IN / H_IN
    ax.add_patch(Ellipse(r8, 2 * rx, 2 * ry, fc="none", ec=C_RED, lw=1.8,
                         linestyle=(0, (3.0, 2.2)), zorder=4))
    _reg("R8ring", r8[0] - rx, r8[0] + rx, r8[1] - ry, r8[1] + ry)

    for k in ["R5", "R6", "R7", "R1", "R2", "R3", "R4", "R8"]:
        d = RISKS[k]
        if d["post"] is not None:
            _arrow(ax, d["pre"], d["post"], d["c"], d["st"], d["rad"])
            _marker(ax, k + "-post", d["post"][0], d["post"][1], False, d["c"])
        _marker(ax, k, d["pre"][0], d["pre"][1], True, d["c"], label=k)


def draw_index(ax):
    """右側風險索引帶:色塊 + 編號 + 短名(+ in-text 引註)。

    編號寫在圓內,索引帶用同一組編號當鍵,不需 leader line,
    也就不會出現 leader 與箭頭互相穿越的雜訊。
    """
    sw = 0.009                                   # 色塊寬
    gap = 0.007
    x_txt = IDX_X + sw + gap
    maxw = (IDX_R - x_txt) * W_IN * 72
    line_h = 12.8 / 72.0 / H_IN

    blocks = []
    for no, col, name, cite, red in INDEX:
        runs = [(no + "  ", FS_BODY, C_RED if red else C_TEXT, True),
                (name, FS_BODY, C_RED if red else C_TEXT, red)]
        lines = wrap_runs(runs, maxw)
        if cite:
            lines += wrap_runs([(cite, FS_SMALL, C_MUTED, False, True)], maxw)
        blocks.append((col, lines))

    n_lines = sum(len(b[1]) for b in blocks)
    y_hi, y_lo = 0.872, 0.372
    gap_v = ((y_hi - y_lo) - n_lines * line_h) / (len(blocks) - 1)
    assert gap_v > 0.004, "風險索引帶塞不下(entry gap %.4f)" % gap_v

    y = y_hi
    for col, lines in blocks:
        h = len(lines) * line_h
        ax.add_patch(Rectangle((IDX_X, y - h + line_h * 0.30), sw,
                               line_h * 0.62, fc=col, ec="none", zorder=5))
        draw_lines(ax, lines, x_txt, y - line_h / 2, line_h)
        for i, ln in enumerate(lines):
            w = line_w_u(ln)
            assert x_txt + w <= IDX_R + 1e-6, "索引帶超寬:%s" % ln[0][0]
            yy = y - line_h / 2 - i * line_h
            _reg("idx-%s-%d" % (lines[0][0][0][:2], i), IDX_X, x_txt + w,
                 yy - line_h * 0.45, yy + line_h * 0.45)
        y -= h + gap_v


def draw_legend(ax):
    """矩陣下方三條橫向圖例:標記語意 / 箭頭樣式 / 顏色語意。"""
    fs = FS_SMALL
    lh = 12.4 / 72.0 / H_IN

    # --- A 行:實心 / 空心 / 紅虛線圈 ---
    y = 0.222
    x = MX0
    for kind, txt in [("pre", "緩解前"), ("post", "殘餘風險"),
                      ("ring", "尚無緩解方案 (R8)")]:
        if kind == "pre":
            ax.plot([x + 0.006], [y], marker="o", ms=11, mfc=C_DGREY,
                    mec=C_DGREY, linestyle="none", zorder=5)
            adv = 0.017
        elif kind == "post":
            ax.plot([x + 0.006], [y], marker="o", ms=8, mfc="white",
                    mec=C_DGREY, mew=1.6, linestyle="none", zorder=5)
            adv = 0.017
        else:
            ax.add_patch(Ellipse((x + 0.008, y), 0.017, 0.017 * W_IN / H_IN,
                                 fc="none", ec=C_RED, lw=1.4,
                                 linestyle=(0, (2.4, 1.8)), zorder=5))
            adv = 0.022
        c = C_RED if kind == "ring" else C_TEXT
        ax.text(x + adv, y, txt, ha="left", va="center", fontsize=fs, color=c)
        x += adv + wu(txt, fs) + 0.024
    assert x < LEFT_R, "圖例 A 行超出左區(x=%.3f)" % x
    _reg("legA", MX0, x, y - lh / 2, y + lh / 2)

    # --- B 行:箭頭樣式 = 緩解成功可能性 ---
    y = 0.150
    x = MX0
    head = "箭頭樣式 = 緩解成功可能性"
    ax.text(x, y, head, ha="left", va="center", fontsize=fs, color=C_TEXT,
            fontweight="bold")
    x += wu(head, fs, True) + 0.018
    for st, txt in [("thick", "高"), ("thin", "中"), ("dash", "低")]:
        kw = dict(color=C_TEXT)
        if st == "thick":
            kw["lw"] = 2.6
        elif st == "thin":
            kw["lw"] = 1.3
        else:
            kw.update(lw=1.6, linestyle=(0, (2.2, 1.7)))
        ax.plot([x, x + 0.022], [y, y], zorder=5, **kw)
        ax.text(x + 0.028, y, txt, ha="left", va="center", fontsize=fs,
                color=C_TEXT)
        x += 0.028 + wu(txt, fs) + 0.022
    assert x < LEFT_R, "圖例 B 行超出左區(x=%.3f)" % x
    _reg("legB", MX0, x, y - lh / 2, y + lh / 2)

    # --- C 行:顏色語意(紅 + 兩級灰階,不引入第五個語意色)---
    y = 0.072
    x = MX0
    for col, txt in [(C_RED, "紅 = 安全或法律責任"),
                     (C_DGREY, "深灰 = 資料與模型品質"),
                     (C_LGREY, "淺灰 = 組織 / 經濟 / 社會")]:
        ax.add_patch(Rectangle((x, y - 0.011), 0.010, 0.022, fc=col,
                               ec="none", zorder=4))
        ax.text(x + 0.015, y, txt, ha="left", va="center", fontsize=fs,
                color=C_TEXT)
        x += 0.015 + wu(txt, fs) + 0.020
    assert x < LEFT_R, "顏色語意帶超出左區(x=%.3f)" % x
    _reg("legC", MX0, x, y - lh / 2, y + lh / 2)


# ==================================================================
# 右:三欄偵測訊號表(「緩解自身的風險」欄已移出圖,改由組版程式放)
# ==================================================================
def draw_table(ax):
    ax.add_patch(Rectangle((TX0, 0.940), 0.026, 0.009, fc=ORANGE, ec="none",
                           zorder=4))
    ax.text(TX0 + 0.036, 0.957, "緩解措施與偵測訊號", ha="left", va="center",
            fontsize=FS_TITLE, color=NAVY, fontweight="bold")

    tw = TX1 - TX0
    tot = float(sum(COL_RATIO))
    xs, acc = [], TX0
    for r in COL_RATIO:
        xs.append(acc)
        acc += tw * r / tot
    xs.append(TX1)
    pad = 0.0042
    maxw = [(xs[i + 1] - xs[i] - 2 * pad) * W_IN * 72 for i in range(3)]
    line_h = 12.8 / 72.0 / H_IN

    rows = []
    for d in TABLE:
        c1 = (wrap_runs([(d["no"], FS_BODY, C_TEXT, True)], maxw[0])
              + wrap_runs([(d["cat"], FS_BODY, C_TEXT)], maxw[0]))
        c2 = wrap_runs(d["act"], maxw[1])
        c3 = wrap_runs([(d["sig"], FS_BODY, C_TEXT)], maxw[2])
        rows.append(dict(cells=[c1, c2, c3],
                         n=max(len(c1), len(c2), len(c3)),
                         focus=d.get("focus", False)))
    print("   每列行數:", [r["n"] for r in rows],
          "合計", sum(r["n"] for r in rows))

    avail = (T_TOP - HEAD_H) - T_BOT
    need = sum(r["n"] for r in rows) * line_h
    vpad = (avail - need) / len(rows)
    assert vpad > 0.006, "三欄表塞不下(列距 %.4f)" % vpad
    print("   列距 vpad = %.4f (%.3f 吋)" % (vpad, vpad * H_IN))

    ax.add_patch(Rectangle((TX0, T_TOP - HEAD_H), tw, HEAD_H, fc=NAVY, ec=NAVY,
                           zorder=3))
    for i, h in enumerate(HEADER):
        assert wpt(h, FS_BODY, True) <= maxw[i], "表頭欄 %d 過寬" % i
        ax.text(xs[i] + pad, T_TOP - HEAD_H / 2, h, ha="left", va="center",
                fontsize=FS_BODY, color="white", fontweight="bold", zorder=5)

    y = T_TOP - HEAD_H
    r8_center = None
    for k, r in enumerate(rows):
        rh = r["n"] * line_h + vpad
        if r["focus"]:
            fc = mix(NAVY, "white", 0.86)          # R8 底色深一階
        elif k % 2 == 0:
            fc = mix(NAVY, "white", 0.965)
        else:
            fc = "white"
        ax.add_patch(Rectangle((TX0, y - rh), tw, rh, fc=fc, ec="none",
                               zorder=2))
        ax.plot([TX0, TX1], [y - rh, y - rh], lw=0.6, color=C_RULE, zorder=3)
        if r["focus"]:
            ax.add_patch(Rectangle((TX0, y - rh), 0.0035, rh, fc=C_RED,
                                   ec="none", zorder=4))
            r8_center = y - rh / 2
        for i in range(3):
            lines = r["cells"][i]
            y_top = y - rh / 2 + (len(lines) - 1) * line_h / 2
            for ln in lines:
                assert line_w_u(ln) <= (xs[i + 1] - xs[i] - 2 * pad) + 1e-6, (
                    "欄 %d 有行超出欄寬" % i)
            draw_lines(ax, lines, xs[i] + pad, y_top, line_h)
        y -= rh

    for i in range(1, 3):
        ax.plot([xs[i], xs[i]], [T_TOP - HEAD_H, y], lw=0.6, color=C_RULE,
                zorder=3)
    ax.add_patch(Rectangle((TX0, y), tw, T_TOP - y, fc="none", ec=C_RULE,
                           lw=1.0, zorder=4))
    assert y > 0.012, "表格下緣被裁切(y=%.4f)" % y
    return r8_center


def draw_r8_link(ax, r8_row_y):
    """R8 那一列拉一條紅色細線,連到左圖的紅色虛線圈(錄影停頓點)。"""
    if r8_row_y is None:
        return
    r8 = RISKS["R8"]["pre"]
    ry = 0.018 * W_IN / H_IN
    ax.plot([TX0, GUTTER_X, GUTTER_X, r8[0]],
            [r8_row_y, r8_row_y, RED_CORRIDOR_Y, RED_CORRIDOR_Y],
            lw=0.85, color=C_RED, alpha=0.45, zorder=3,
            linestyle=(0, (3.6, 2.6)), solid_capstyle="round")
    ax.add_patch(FancyArrowPatch((r8[0], RED_CORRIDOR_Y),
                                 (r8[0], r8[1] + ry + 0.012),
                                 arrowstyle="-|>", mutation_scale=11, lw=0.85,
                                 color=C_RED, alpha=0.45, zorder=3,
                                 linestyle=(0, (3.6, 2.6))))


def build():
    global _FIG
    BOXES.clear()
    _WCACHE.clear()
    fig, ax = newfig(W_IN, H_IN)                   # 畫布鎖死,不畫投影片標題
    # 讓 0-1 座標系正好等於整張畫布,量到的 point 寬度才能直接換算成座標
    ax.set_position([0, 0, 1, 1])
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="none", zorder=0))
    _FIG = fig
    fig.canvas.draw()
    draw_matrix(ax)
    draw_index(ax)
    draw_legend(ax)
    r8_row_y = draw_table(ax)
    draw_r8_link(ax, r8_row_y)
    audit_boxes()
    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_06")

# ==================================================================
# 移出圖、改由組版程式(build_deck_v4.slide_06)以投影片文字框放置的元素:
#   1. 「緩解自身的風險」欄(九條,對應 R1 / R2 / R2 附 / R3 / R4 / R5 /
#      R6 / R7 / R8)—— 純文字、不靠位置或顏色傳意,烘進 PNG 只會被縮小。
#   2. 表格左下角的 R2 基準註腳 —— 放投影片頁腳 note()。
#   3. 七類八條的分類列 —— 放 header 的 sub 行。
#   完整文字與建議落點見交件回報的 moved_to_slide 欄位。
# ==================================================================
