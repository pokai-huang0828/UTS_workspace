# -*- coding: utf-8 -*-
"""P7 用圖 —— 澳洲 AI 倫理八原則逐條對照 + 四張張力卡片(含連接線)。

規格來源:v4/notes/04_十頁內容_v2.md 的 `# P7 ...` 節「## 視覺規格」。
共用機具:scripts/make_figs_v4.py(字型 / 色票 / save / newfig / assert_min_fontsize)。

紅線:
- 🔴 裁決 O:畫布固定 12.2 x 5.7 吋(= 組版內容區實形),置入縮放比 = 1.0。
  內容塞不下時砍內容,**不得放大畫布**、不得縮字。
- 圖內最小字級 fs=9。
- 色值只用機具常數(ORANGE #E8833A / NAVY #1F4E79);v3 的舊橘 / 舊深藍已作廢。
- 圖不畫投影片標題、不畫右上角五格進度指示(由組版程式負責)。
- 不用 emoji、不用 U+2212 / 全形減號 / 破折號;負號一律 ASCII hyphen。

本頁「內容塞不下」的處置順序(本檔自訂,依裁決 O 第 4 條「帶狀純文字移出圖」):
  ① 底部通欄窄帶、卡片零底部引句                    -> 移出圖,改投影片文字框
  ② 四張卡片的「當責 · 時點 · 會改變哪個決策」行     -> 移出圖
  ③ 四張卡片的「我不能決定的」行                     -> 移出圖
  ④ 卡片二的「處置」行與第二條「我決定的」行         -> 移出圖
  ⑤ (本輪未用到)左欄理由行改寫為單行摘要
留在圖裡的是「需要圖形關係才講得清楚」的部分:八原則的狀態色形狀(全頁綠燈只有一條)、
兩條紅燈的底色與色條、四張卡片與原則之間的連線(含兩條紅色加粗線與跨線避讓),
以及左欄標題與出處(出處若離開表格就失去指涉對象,故不視為可搬離的純文字)。
移出圖的文字一字不刪,逐項交給 build_deck_v4.py 以投影片文字框放置。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    np, FancyBboxPatch,
    NAVY, ORANGE, ORANGE_DARK, RED, GREY, AMBER, GREEN,
    newfig, save, assert_min_fontsize,
)
from matplotlib.path import Path  # noqa: E402
from matplotlib.text import Text  # noqa: E402
from matplotlib.patches import PathPatch, Ellipse, Rectangle  # noqa: E402

# ------------------------------------------------------------------
# 畫布。座標一律 0-1,且 axes 撐滿整張圖(見 build() 的 subplots_adjust),
# 所以 x 的 1.0 = FIGW 英吋、y 的 1.0 = FIGH 英吋。
# 🔴 12.2 x 5.7 是裁決 O 鎖死的值,不得為了塞內容改大。
# ------------------------------------------------------------------
OUT_W, OUT_H = 12.2, 5.7         # 🔴 裁決 O 鎖死的成品實體吋數(= 組版內容區實形)

# 共用機具 save() 用 bbox_inches='tight',而 tight 框恆等於整張 figure,
# 再各邊加 pad_inches=0.1 => 成品 = figsize + 0.2 吋。
# 所以 figsize 取 12.0 x 5.5,出檔後恰為 12.2 x 5.7(__main__ 有實測 assert)。
# 這是把畫布**縮小**去對齊鎖死值,不是放大畫布規避字級規則。
FIGW, FIGH = OUT_W - 0.2, OUT_H - 0.2

LX0, LX1 = 0.005, 0.556          # 左 55%:八原則
RX0, RX1 = 0.596, 0.995          # 右 40%:張力卡片(中間 4% 為連接線走道)

BODY = "#333333"

FS_NAME = 11.5
FS_CARD = 11.5
FS_BODY = 9.5                    # >= FS_MIN(9),且置入縮放比 1.0 => 真的 9.5pt

LSP = 1.45                                   # 內文行距
LH = FS_BODY * LSP / 72.0 / FIGH             # 一行內文的 y 高
LH_NAME = FS_NAME * 1.50 / 72.0 / FIGH
LH_CARD = FS_CARD * 1.55 / 72.0 / FIGH

CLOSERS = set("，,。;;::)）」』】、!!??")

_CACHE = {}
_AX = None
_FIG = None


def W(s, fs=FS_BODY, bold=False):
    """字串寬度(x 軸 0-1 單位)。逐字實測 + 快取,不用估算。"""
    tot = 0.0
    key_ax = _AX
    for ch in s:
        k = (ch, fs, bold)
        if k not in _CACHE:
            t = key_ax.text(0.0, -0.5, ch, fontsize=fs,
                            fontweight="bold" if bold else "normal")
            bb = t.get_window_extent(renderer=_FIG.canvas.get_renderer())
            t.remove()
            _CACHE[k] = bb.width / _FIG.bbox.width
        tot += _CACHE[k]
    return tot


def _tok(s):
    toks, buf = [], ""
    for ch in s:
        if ord(ch) < 0x2E80 and ch != " ":
            buf += ch
        else:
            if buf:
                toks.append(buf)
                buf = ""
            toks.append(ch)
    if buf:
        toks.append(buf)
    return toks


def wrap(s, fs, maxw):
    """貪婪換行,maxw 為 x 軸 0-1 單位。收尾標點不落行首。"""
    return wrap2(s, fs, maxw, maxw)


def wrap2(s, fs, w_first, w_rest):
    """同 wrap(),但第一行與後續行可用不同寬度(標籤內縮 / 續行齊左)。"""
    w_first, w_rest = max(w_first, 0.05), max(w_rest, 0.05)
    lines = []
    for seg in s.split("\n"):
        cur = ""
        for t in _tok(seg):
            cand = cur + t
            lim = w_first if not lines else w_rest
            if cur.strip() and W(cand, fs) > lim:
                if t in CLOSERS:
                    cur = cand
                    continue
                lines.append(cur.rstrip())
                cur = "" if t == " " else t
            else:
                cur = cand
        if cur.strip():
            lines.append(cur.rstrip())
    return lines


# ------------------------------------------------------------------
# 內容(全部取自視覺規格;內部作業註記不入圖)
# 理由行不再人工斷行 —— 12.2 吋畫布下左欄可用 6.2 吋,交給 wrap() 自動排。
# ------------------------------------------------------------------
PRINCIPLES = [
    (1, "人類、社會與環境福祉", "amber",
     "同樣人力承接更高複核量,工作性質改變而非人力削減;轉任規劃列為移交前置條件"),
    (2, "以人為本的價值觀", "amber",
     "判定的最終使用者是駕駛與車隊安全主管,本案先處理判準一致性,使用政策仍在客戶端"),
    (3, "公平性", "red",
     "品質防線目前是配給制,依客戶購買量與問題嚴重性排序;分配依據是客戶大小,不是風險大小"),
    (4, "隱私保護與安全", "amber",
     "本案會擴大影像調閱範圍與判定紀錄的保存,存取控制、保存期限與最小化原則列為移交前置條件"),
    (5, "可靠性與安全性", "amber",
     "漏放率目前不存在,只有一份 39 筆的人工觸發測試(獨立樣本,不屬於誤報側的複核母體),"
     "且我們自註為下限;要等含信賴區間的估計建立後才談得上可靠"),
    (6, "透明性與解釋性", "amber",
     "規則式脈絡層可逐條檢查,但對客戶揭露到哪一層尚未決定"),
    (7, "可申訴性", "red",
     "只有車隊安全主管能標記,駕駛本人不能提出質疑"),
    (8, "問責性", "green",
     "以 RACI + 三道決策門 + 資料版本快照處理"),
]

BADGE = {
    "green": ("已處理", GREEN, "white"),
    "amber": ("部分", AMBER, NAVY),
    "red": ("未達成", RED, "white"),
}

# 卡片:只留「張力」一行(處置順序 ②③④ 全部套用)。
# 「張力」不移出的理由:卡名(如「工作性質改變」)單獨存在無法指涉任何東西,
# 張力行是連線另一端的語意,拿掉連線就失去意義 —— 屬於靠位置與連線傳達的內容。
# 其餘每一行都移出圖、由 build_deck_v4.py 放在該卡下方的預留白帶,一字不刪。
CARDS = [
    dict(
        tag="張力零", name="品質防線目前是配給制",
        cite="(Australian Human Rights Commission, 2020)",
        strong=True,
        rows=[
            ("張力", "人工驗證的量能有限,依客戶購買量與問題嚴重性排序,"
                     "結果是大客戶拿到人工驗證過的判定,小客戶拿到的判定沒有人看過", RED),
        ],
    ),
    dict(
        # 橘 = 人力成本(全片色語意),故此卡以橘色母題描邊
        tag="張力一", name="工作性質改變", cite=None, strong=False, accent=ORANGE,
        rows=[
            ("張力", "5 位專職分析人員的工作從逐筆看片變成處理難題與治理", ORANGE_DARK),
        ],
    ),
    dict(
        tag="張力二", name="判定會影響駕駛", cite=None, strong=False,
        rows=[
            ("張力", "語意模糊題(香菸 vs 香腸、手機 vs 保溫瓶)判錯,可能進入駕駛考核", RED),
        ],
    ),
    dict(
        tag="張力三", name="透明度的界線", cite=None, strong=False,
        rows=[
            ("張力", "量測底座讓「我們知道自己錯多少」變成可證明", ORANGE_DARK),
        ],
    ),
]

# (卡片索引, 原則編號, 是否紅色加粗)。第 5 條刻意不連線。
LINKS = [
    (0, 3, True),
    (1, 1, False),
    (1, 2, False),
    (2, 7, True),
    (2, 4, False),
    (3, 6, False),
    (3, 8, False),
]


# ------------------------------------------------------------------
# 小元件
# ------------------------------------------------------------------
def pill(ax, x, y_mid, text, fc, tc, fs=FS_BODY, padx=0.006, z=6):
    w = W(text, fs, bold=True) + 2 * padx
    h = fs * 1.95 / 72.0 / FIGH
    ax.add_patch(FancyBboxPatch((x, y_mid - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=.007",
                                fc=fc, ec=fc, lw=0, zorder=z))
    ax.text(x + w / 2, y_mid, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold", zorder=z + 1)
    return w


def bezier(ax, p0, p1, color, lw, z):
    c0 = (p0[0] - 0.026, p0[1])
    c1 = (p1[0] + 0.026, p1[1])
    verts = [p0, c0, c1, p1]
    ax.add_patch(PathPatch(Path(verts, [Path.MOVETO, Path.CURVE4, Path.CURVE4,
                                        Path.CURVE4]),
                           fc="none", ec=color, lw=lw, zorder=z, capstyle="round"))
    t = np.linspace(0, 1, 120)[:, None]
    p = np.array([p0, c0, c1, p1])
    return ((1 - t) ** 3) * p[0] + (3 * (1 - t) ** 2 * t) * p[1] \
        + (3 * (1 - t) * t ** 2) * p[2] + (t ** 3) * p[3]


def _cross(a1, a2, b1, b2):
    d = (a2[0] - a1[0]) * (b2[1] - b1[1]) - (a2[1] - a1[1]) * (b2[0] - b1[0])
    if abs(d) < 1e-12:
        return None
    t = ((b1[0] - a1[0]) * (b2[1] - b1[1]) - (b1[1] - a1[1]) * (b2[0] - b1[0])) / d
    u = ((b1[0] - a1[0]) * (a2[1] - a1[1]) - (b1[1] - a1[1]) * (a2[0] - a1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (a1[0] + t * (a2[0] - a1[0]), a1[1] + t * (a2[1] - a1[1]))
    return None


def crossings(pa, pb):
    out = []
    for i in range(len(pa) - 1):
        for j in range(len(pb) - 1):
            c = _cross(pa[i], pa[i + 1], pb[j], pb[j + 1])
            if c is not None:
                out.append(c)
    return out


# ------------------------------------------------------------------
def build():
    global _AX, _FIG
    fig, ax = newfig(FIGW, FIGH)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)   # axes 撐滿,座標=版面
    fig.canvas.draw()
    _AX, _FIG = ax, fig

    # 把 savefig(bbox_inches='tight') 的裁切框釘死在整張畫布上,
    # 否則輸出的實體吋數會被內容輪廓改掉,置入縮放比就不再是 1.0。
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="none", zorder=0))

    # BOTY 抬高到 0.0255:圖的最下緣讓出一條 0.24 吋通欄白帶(1 行 @9pt 綽綽有餘),
    # 給 build_deck_v4.py 放移出的底部窄帶(那是純文字,烘進 PNG 只會跟著縮小)。
    TOPY, BOTY = 0.908, 0.0255

    # ================================================================
    # 左欄:八原則逐條對照
    # 標題與出處留在圖裡:出處是「這張表對照的是哪一份公開框架」的錨點,
    # 一旦離開表格就失去指涉對象;色票圖例則是解讀顏色的鑰匙,兩者都不是純文字。
    # ================================================================
    ax.text(LX0 + 0.008, 0.975, "澳洲 AI 倫理八原則 · 逐條對照", ha="left",
            va="center", fontsize=FS_NAME, color=NAVY, fontweight="bold")
    ax.text(LX0 + 0.008 + W("澳洲 AI 倫理八原則 · 逐條對照", FS_NAME, bold=True)
            + 0.012, 0.975,
            "(Department of Industry, Science and Resources, 2019)",
            ha="left", va="center", fontsize=FS_BODY, color=GREY)

    lx, ly = LX0 + 0.008, 0.932
    for key, note in (("green", "已處理"), ("amber", "本案提出處置但未完成"),
                      ("red", "目前未達成")):
        col = BADGE[key][1]
        ax.add_patch(Rectangle((lx, ly - 0.0090), 0.010, 0.018, fc=col, ec=col,
                               zorder=4))
        ax.text(lx + 0.014, ly, note, ha="left", va="center", fontsize=FS_BODY,
                color=BODY, zorder=4)
        lx += 0.014 + W(note) + 0.018

    tx = LX0 + 0.033                       # 原則名 / 理由行的左緣
    reason_w = LX1 - 0.008 - tx
    wrapped = [wrap(p[3], FS_BODY, reason_w) for p in PRINCIPLES]
    need = [0.010 + LH_NAME + len(w) * LH + 0.009 for w in wrapped]
    assert sum(need) + 7 * 0.006 <= TOPY - BOTY, (
        "八原則清單總高超出版面 —— 依處置順序 ⑤ 砍內容,不得放大畫布")
    gap = max((TOPY - BOTY - sum(need)) / (len(need) - 1), 0.004)

    row_y, left_boxes = {}, []
    y = TOPY
    for i, (num, name, st, _) in enumerate(PRINCIPLES):
        h = need[i]
        is_red = (st == "red")
        if is_red:
            ax.add_patch(Rectangle((LX0, y - h), LX1 - LX0, h, fc=RED, ec="none",
                                   alpha=0.10, zorder=2))
            ax.add_patch(Rectangle((LX0, y - h), 0.005, h, fc=RED, ec=RED, zorder=3))

        cx = LX0 + 0.019
        cy = y - 0.010 - LH_NAME / 2
        col = RED if is_red else NAVY
        ax.add_patch(Ellipse((cx, cy), 0.0150, 0.0150 * FIGW / FIGH, fc=col, ec=col,
                             zorder=4))
        ax.text(cx, cy, str(num), ha="center", va="center", fontsize=FS_BODY,
                color="white", fontweight="bold", zorder=5)
        ax.text(tx, cy, name, ha="left", va="center", fontsize=FS_NAME,
                color=col, fontweight="bold", zorder=5)

        lab, bfc, btc = BADGE[st]
        bw = W(lab, FS_BODY, bold=True) + 0.012
        pill(ax, LX1 - 0.008 - bw, cy, lab, bfc, btc, padx=0.006, z=5)

        ax.text(tx, y - 0.010 - LH_NAME - 0.002, "\n".join(wrapped[i]),
                ha="left", va="top", fontsize=FS_BODY, color=BODY,
                linespacing=LSP, zorder=5)
        row_y[num] = cy
        left_boxes.append((LX0, y - h, LX1, y))
        y -= h + gap

    # ================================================================
    # 右欄:四張張力卡片(等寬堆疊,順序固定 零 -> 一 -> 二 -> 三)
    # ================================================================
    CPAD = 0.010
    hx = RX0 + CPAD
    inner = (RX1 - CPAD) - hx

    # 標籤內縮 <= FLUSH 時用懸掛縮排;標籤過長時續行齊左,免得可用寬度被吃掉
    FLUSH = 0.090
    wc = []
    for c in CARDS:
        rows = []
        for lab, body, col in c["rows"]:
            lw = W(lab + ":", FS_BODY, bold=True) + 0.004
            hang = lw <= FLUSH
            lines = wrap2(body, FS_BODY, inner - lw, inner - (lw if hang else 0.0))
            rows.append((lab, body, col, lw, hang, lines))
        wc.append(rows)

    RPAD = 0.004
    CITE_H = FS_BODY * 1.45 / 72.0 / FIGH
    need_c = []
    for c, rows in zip(CARDS, wc):
        h = 0.010 + LH_CARD + 0.005 \
            + sum(len(r[5]) * LH + RPAD for r in rows) + 0.008
        if c["cite"]:
            h += CITE_H + 0.004
        need_c.append(h)

    # 每張卡片下方留一條白帶(共 4 條,含 card3 下方)給移出的卡片內文。
    # 所以除數是 len(need_c) 而不是 len(need_c)-1。
    CTOP, CBOT = 0.988, BOTY
    assert sum(need_c) + 4 * 0.060 <= CTOP - CBOT, (
        "卡片 + 預留白帶超出版面 —— 依處置順序再砍一行,不得縮字或放大畫布")
    cgap = (CTOP - CBOT - sum(need_c)) / len(need_c)

    card_box, card_rect = [], []
    top = CTOP
    for c, rows, h in zip(CARDS, wc, need_c):
        strong = c["strong"]
        ec = RED if strong else c.get("accent", NAVY)
        ax.add_patch(FancyBboxPatch((RX0, top - h), RX1 - RX0, h,
                                    boxstyle="round,pad=0,rounding_size=.009",
                                    fc="#FAFAFA", ec=ec, lw=2.8 if strong else 1.6,
                                    zorder=3))
        if strong:
            ax.add_patch(FancyBboxPatch((RX0, top - h), RX1 - RX0, h,
                                        boxstyle="round,pad=0,rounding_size=.009",
                                        fc=RED, ec="none", alpha=0.07, zorder=3))

        hy = top - 0.010 - LH_CARD / 2
        head = RED if strong else (ORANGE_DARK if c.get("accent") else NAVY)
        pw = pill(ax, hx, hy, c["tag"], head, "white", z=6)
        nx = hx + pw + 0.007
        ax.text(nx, hy, c["name"], ha="left", va="center", fontsize=FS_CARD,
                color=head, fontweight="bold", zorder=6)

        ty = top - 0.010 - LH_CARD - 0.005
        if c["cite"]:
            # 出處另起一行:12.2 吋畫布上「卡名 + 出處」同列會超出卡片內寬
            ax.text(hx, ty, c["cite"], ha="left", va="top", fontsize=FS_BODY,
                    color=GREY, zorder=6)
            ty -= CITE_H + 0.004

        for lab, body, col, lw, hang, lines in rows:
            ax.text(hx, ty, lab + ":", ha="left", va="top", fontsize=FS_BODY,
                    color=col, fontweight="bold", zorder=6)
            ax.text(hx + lw, ty, lines[0], ha="left", va="top",
                    fontsize=FS_BODY, color=BODY, zorder=6)
            if len(lines) > 1:
                ax.text(hx + (lw if hang else 0.0), ty - LH, "\n".join(lines[1:]),
                        ha="left", va="top", fontsize=FS_BODY, color=BODY,
                        linespacing=LSP, zorder=6)
            ty -= len(lines) * LH + RPAD

        card_box.append((top, top - h))
        card_rect.append((RX0, top - h, RX1, top))
        top -= h + cgap

    # ================================================================
    # 連接線:全部走中央 6% 走道,不穿越任何文字
    # ================================================================
    cnt = {}
    for ci, _, _ in LINKS:
        cnt[ci] = cnt.get(ci, 0) + 1

    used, reds, greys = {}, [], []
    for ci, pnum, is_red in LINKS:
        y_hi, y_lo = card_box[ci]
        n = cnt[ci]
        k = used.get(ci, 0)
        used[ci] = k + 1
        mid = (y_hi + y_lo) / 2
        span = (y_hi - y_lo) * 0.42
        ay = mid + span * ((n - 1) / 2.0 - k) if n > 1 else mid
        (reds if is_red else greys).append(((RX0, ay), (LX1 + 0.002, row_y[pnum])))

    gp = [bezier(ax, a, b, GREY, 1.0, 6) for a, b in greys]
    rp = [bezier(ax, a, b, RED, 3.0, 8) for a, b in reds]

    # 交叉避讓:灰線讓開(白色小缺口),紅線連續通過
    for r in rp:
        for g in gp:
            for cxx, cyy in crossings(r, g):
                ax.add_patch(Ellipse((cxx, cyy), 0.0085, 0.0085 * FIGW / FIGH,
                                     fc="white", ec="white", zorder=7))
    # 兩條紅線若相交,以跨線小弧避讓,不得看成同一條線
    for i in range(len(rp)):
        for j in range(i + 1, len(rp)):
            for cxx, cyy in crossings(rp[i], rp[j]):
                ax.add_patch(Ellipse((cxx, cyy), 0.012, 0.012 * FIGW / FIGH,
                                     fc="white", ec="white", zorder=8.5))
                ax.add_patch(Ellipse((cxx, cyy), 0.012, 0.012 * FIGW / FIGH,
                                     fc="none", ec=RED, lw=2.0, zorder=8.6))

    assert_min_fontsize(fig)

    # 預留白帶(輸出 png 左上角起算的英吋座標),交給 build_deck_v4.py 放移出的文字。
    def _in(x, y):
        return (0.1 + x * FIGW, 0.1 + (1 - y) * FIGH)

    bands = []
    for i, (_, ry0, _, _) in enumerate(card_rect):
        by1 = ry0                                   # 卡片下緣
        by0 = by1 - cgap                            # 下一張卡片上緣 / CBOT
        l, t = _in(RX0, by1)
        r, b = _in(RX1, by0)
        bands.append(("卡片%d 下方" % i, round(l, 2), round(t, 2),
                      round(r, 2), round(b, 2), round(b - t, 2)))
    l, t = _in(LX0, BOTY)
    r, b = _in(LX1 if False else 0.995, 0.0)
    bands.append(("底部通欄", round(0.1 + LX0 * FIGW, 2), round(t, 2),
                  round(0.1 + 0.995 * FIGW, 2), 5.70, round(5.70 - t, 2)))
    return fig, dict(left_boxes=left_boxes, card_rect=card_rect, bands=bands)


# ------------------------------------------------------------------
# 出圖前自檢:文字兩兩不重疊、全部落在容器框內
# ------------------------------------------------------------------
def audit(fig, meta):
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    W_, H_ = fig.bbox.width, fig.bbox.height

    items = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        bb = t.get_window_extent(renderer=rend)
        if bb.width <= 0 or bb.height <= 0:
            continue
        items.append((s.replace("\n", " / ")[:26],
                      bb.x0 / W_, bb.y0 / H_, bb.x1 / W_, bb.y1 / H_))

    bad = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            ox = min(a[3], b[3]) - max(a[1], b[1])
            oy = min(a[4], b[4]) - max(a[2], b[2])
            if ox > 1e-9 and oy > 1e-9:
                bad.append((a[0], b[0], round(ox * FIGW, 3), round(oy * FIGH, 3)))
    assert not bad, "文字重疊 %d 處:%s" % (len(bad), bad[:6])

    out = [it for it in items
           if it[1] < -1e-6 or it[2] < -1e-6 or it[3] > 1 + 1e-6 or it[4] > 1 + 1e-6]
    assert not out, "文字超出畫布 %d 處:%s" % (len(out), out[:6])

    # 卡片內文字必須落在自己那張卡片的框內
    esc = []
    for s, x0, y0, x1, y1 in items:
        if x0 < RX0 - 1e-6:
            continue
        if not any(rx0 - 1e-6 <= x0 and x1 <= rx1 + 1e-6
                   and ry0 - 1e-6 <= y0 and y1 <= ry1 + 1e-6
                   for rx0, ry0, rx1, ry1 in meta["card_rect"]):
            esc.append(s)
    assert not esc, "卡片文字溢出卡框:%s" % esc[:6]

    # 左欄文字必須落在左欄框內
    lesc = [s for s, x0, y0, x1, y1 in items
            if x1 <= LX1 + 1e-6 and (x0 < LX0 - 1e-6 or x1 > LX1 + 1e-6)]
    assert not lesc, "左欄文字溢出:%s" % lesc[:6]

    print("  audit OK:%d 個 Text,零重疊、零溢出" % len(items))
    print("  預留白帶(png 左上角起算,英吋)—— build_deck_v4.py 照此放移出文字:")
    for nm, l, t, r, b, h in meta["bands"]:
        cap = int((r - l) / (9.0 / 72.0)) * max(int(h / 0.16), 0)
        print("    %-12s x %5.2f-%5.2f  y %5.2f-%5.2f  h=%.2f  約可容 %d 字 @9pt"
              % (nm, l, r, t, b, h, cap))


class _FontGuard(__import__("logging").Handler):
    """matplotlib 的 findfont / 缺字是走 logging 不是 warnings,兩邊都要攔。"""
    hits = []

    def emit(self, record):
        msg = record.getMessage()
        if "findfont" in msg or "Glyph" in msg or "missing from" in msg:
            _FontGuard.hits.append(msg[:160])


if __name__ == "__main__":
    import logging
    import warnings
    _g = _FontGuard(level=logging.WARNING)
    logging.getLogger("matplotlib").addHandler(_g)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)   # findfont / missing glyph 直接炸
        f, m = build()
        audit(f, m)
        save(f, "fig_v4_07")

    # 出檔後驗實體尺寸 —— 裁決 O 的可量測判準:置入 12.2 吋內容區時縮放比 = 1.0
    from PIL import Image
    import make_figs_v4 as MK
    px = Image.open(os.path.join(MK.OUT, "fig_v4_07.png")).size
    got = (round(px[0] / 300.0, 3), round(px[1] / 300.0, 3))
    assert abs(got[0] - OUT_W) <= 0.02 and abs(got[1] - OUT_H) <= 0.02, \
        "輸出實體尺寸 %s 吋 != 鎖死的 %s x %s" % (got, OUT_W, OUT_H)
    assert not _FontGuard.hits, "matplotlib 字型警告:%s" % _FontGuard.hits[:5]
    print("  png %s px = %s 吋,縮放比 1.0,fs=%.1f 即真實 %.1fpt;字型警告 0 則"
          % (px, got, FS_BODY, FS_BODY))
