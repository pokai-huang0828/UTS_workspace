# -*- coding: utf-8 -*-
"""P7 用圖 —— 澳洲 AI 倫理八原則逐條對照 + 四張張力卡片(含連接線)。

規格來源:v4/notes/04_十頁內容_v2.md 的 `# P7 ...` 節「## 視覺規格」。
共用機具:scripts/make_figs_v4.py(字型 / 色票 / save / newfig / assert_min_fontsize)。

紅線:
- 色值只用機具常數(ORANGE #E8833A / NAVY #1F4E79);v3 的舊橘 / 舊深藍已作廢,不得出現。
- 圖內最小字級 fs=9。
- 圖不畫投影片標題、不畫右上角五格進度指示(由組版程式負責)。
- 不用 emoji、不用 U+2212 / 全形減號 / 破折號;負號一律 ASCII hyphen。
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
from matplotlib.patches import PathPatch, Ellipse, Rectangle  # noqa: E402

# ------------------------------------------------------------------
# 畫布(16:9)。座標一律 0-1,且 axes 撐滿整張圖(見 build() 的 subplots_adjust),
# 所以 x 的 1.0 = FIGW 英吋、y 的 1.0 = FIGH 英吋。
# ------------------------------------------------------------------
FIGW, FIGH = 13.6, 7.65

LX0, LX1 = 0.006, 0.376          # 左 38%:八原則
RX0, RX1 = 0.436, 0.996          # 右 56%:張力卡片(中間 6% 為連接線走道)

BODY = "#333333"

FS_TITLE = 13.0
FS_NAME = 11.5
FS_CARD = 12.0
FS_BODY = 9.5
FS_QUOTE = 10.0
FS_BAND = 11.0

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
    """貪婪換行,maxw 為 x 軸 0-1 單位。收尾標點不落行首。

    字串裡的 \\n 為人工指定的斷句點(避免詞被硬拆),各段各自再自動換行。
    """
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
# ------------------------------------------------------------------
PRINCIPLES = [
    (1, "人類、社會與環境福祉", "amber",
     "同樣人力承接更高複核量,工作性質改變而非人力削減;\n轉任規劃列為移交前置條件"),
    (2, "以人為本的價值觀", "amber",
     "判定的最終使用者是駕駛與車隊安全主管,\n本案先處理判準一致性,使用政策仍在客戶端"),
    (3, "公平性", "red",
     "品質防線目前是配給制,依客戶購買量與問題嚴重性排序;\n分配依據是客戶大小,不是風險大小"),
    (4, "隱私保護與安全", "amber",
     "本案會擴大影像調閱範圍與判定紀錄的保存,\n存取控制、保存期限與最小化原則列為移交前置條件"),
    (5, "可靠性與安全性", "amber",
     "漏放率目前不存在,只有一份 39 筆的人工觸發測試\n"
     "(獨立樣本,不屬於誤報側的複核母體),且我們自註為下限;\n"
     "要等含信賴區間的估計建立後才談得上可靠"),
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

CARDS = [
    dict(
        tag="張力零", name="品質防線目前是配給制",
        cite="(Australian Human Rights Commission, 2020)",
        strong=True,
        rows=[
            ("張力", "人工驗證的量能有限,依客戶購買量與問題嚴重性排序,\n"
                     "結果是大客戶拿到人工驗證過的判定,小客戶拿到的判定沒有人看過", RED),
            ("我決定的", "錯誤率量測一旦建立,複核優先序改以風險排序而非客戶大小,"
                        "新的排序規則提交委員會核定", NAVY),
            ("我不能決定的", "商業上的客戶分級本身", GREY),
            ("當責 · 時點 · 會改變哪個決策",
             "複核營運主管於 W6 交出「這道防線目前覆蓋了誰」的第一份紀錄;\n"
             "新的風險排序規則於 G1 提交委員會;委員會核定與否,"
             "決定這一條在移交時是紅燈還是琥珀。", ORANGE_DARK),
        ],
        quote="被產能擋住的不是簽約,是我們能對多少客戶維持同一個品質水準。",
    ),
    dict(
        # 橘 = 人力成本(全片色語意),故此卡以橘色母題描邊
        tag="張力一", name="工作性質改變", cite=None, strong=False, accent=ORANGE,
        rows=[
            ("張力", "5 位專職分析人員的工作從逐筆看片變成處理難題與治理", ORANGE_DARK),
            ("我決定的", "轉任與再訓練規劃列為移交前置條件", NAVY),
            ("我不能決定的", "人事承諾本身,需贊助人於 G1(第 6 週)核定;\n"
                            "在核定之前,本案不對任何人的職位或編制做出承諾。", GREY),
            ("當責 · 時點 · 會改變哪個決策",
             "項目贊助人 · G1(第 6 週) · 核定與否決定移交條件能不能簽", ORANGE_DARK),
        ],
        quote=None,
    ),
    dict(
        tag="張力二", name="判定會影響駕駛", cite=None, strong=False,
        rows=[
            ("張力", "語意模糊題(香菸 vs 香腸、手機 vs 保溫瓶)判錯,可能進入駕駛考核", RED),
            ("處置", "判準手冊明文化 + 抽樣雙人複核 + 判定可回溯", GREEN),
            ("我決定的", "申訴機制到位前不供個人考核使用", NAVY),
            ("我決定的", "回抽採最小必要抽樣,以事件片段入庫而非整日影片,樣本用畢即銷毀;\n"
                        "資料授權範圍的確認列為 G1 前置事項", NAVY),
            ("我不能決定的", "客戶端的申訴流程本身", GREY),
        ],
        quote=None,
    ),
    dict(
        tag="張力三", name="透明度的界線", cite=None, strong=False,
        rows=[
            ("張力", "量測底座讓「我們知道自己錯多少」變成可證明", ORANGE_DARK),
            ("我決定的", "內部稽核報表常態化", NAVY),
            ("我不能決定的", "要不要對客戶揭露、揭露到哪", GREY),
            ("當責 · 時點 · 會改變哪個決策",
             "提案人於 G1 把揭露層級的選項與各自後果整理成一頁提交;\n"
             "委員會在 G1 選一個層級,這個選擇決定 WP-F 移交文件裡對外報表的欄位。",
             ORANGE_DARK),
        ],
        quote=None,
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
    c0 = (p0[0] - 0.030, p0[1])
    c1 = (p1[0] + 0.030, p1[1])
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

    BAND_H = 0.048
    TOPY, BOTY = 0.908, BAND_H + 0.016

    # ============ 底部窄帶(通欄,深底白字)============
    ax.add_patch(Rectangle((0.0, 0.0), 1.0, BAND_H, fc=NAVY, ec=NAVY, zorder=3))
    ax.text(0.5, BAND_H / 2, "表上的狀態不是自我打分,是移交前的待辦清單。",
            ha="center", va="center", fontsize=FS_BAND, color="white",
            fontweight="bold", zorder=4)

    # ================================================================
    # 左欄:八原則逐條對照
    # ================================================================
    ax.text(LX0 + 0.008, 0.993, "澳洲 AI 倫理八原則 · 逐條對照", ha="left", va="top",
            fontsize=FS_TITLE, color=NAVY, fontweight="bold")
    ax.text(LX0 + 0.008, 0.961,
            "(Department of Industry, Science and Resources, 2019)",
            ha="left", va="top", fontsize=FS_BODY, color=GREY)

    lx, ly = LX0 + 0.008, 0.932
    for key, note in (("green", "已處理"), ("amber", "本案提出處置但未完成"),
                      ("red", "目前未達成")):
        col = BADGE[key][1]
        ax.add_patch(Rectangle((lx, ly - 0.0075), 0.010, 0.015, fc=col, ec=col,
                               zorder=4))
        ax.text(lx + 0.014, ly, note, ha="left", va="center", fontsize=FS_BODY,
                color=BODY, zorder=4)
        lx += 0.014 + W(note) + 0.016

    tx = LX0 + 0.038                       # 原則名 / 理由行的左緣
    reason_w = LX1 - 0.008 - tx
    wrapped = [wrap(p[3], FS_BODY, reason_w) for p in PRINCIPLES]
    need = [0.012 + LH_NAME + len(w) * LH + 0.010 for w in wrapped]
    assert sum(need) + 7 * 0.006 <= TOPY - BOTY, "八原則清單總高超出版面"
    gap = max((TOPY - BOTY - sum(need)) / (len(need) - 1), 0.004)

    row_y = {}
    y = TOPY
    for i, (num, name, st, _) in enumerate(PRINCIPLES):
        h = need[i]
        is_red = (st == "red")
        if is_red:
            ax.add_patch(Rectangle((LX0, y - h), LX1 - LX0, h, fc=RED, ec="none",
                                   alpha=0.10, zorder=2))
            ax.add_patch(Rectangle((LX0, y - h), 0.005, h, fc=RED, ec=RED, zorder=3))

        cx = LX0 + 0.021
        cy = y - 0.012 - LH_NAME / 2
        col = RED if is_red else NAVY
        ax.add_patch(Ellipse((cx, cy), 0.0155, 0.0155 * FIGW / FIGH, fc=col, ec=col,
                             zorder=4))
        ax.text(cx, cy, str(num), ha="center", va="center", fontsize=FS_BODY,
                color="white", fontweight="bold", zorder=5)
        ax.text(tx, cy, name, ha="left", va="center", fontsize=FS_NAME,
                color=col, fontweight="bold", zorder=5)

        lab, bfc, btc = BADGE[st]
        bw = W(lab, FS_BODY, bold=True) + 0.012
        pill(ax, LX1 - 0.008 - bw, cy, lab, bfc, btc, padx=0.006, z=5)

        ax.text(tx, y - 0.012 - LH_NAME - 0.002, "\n".join(wrapped[i]),
                ha="left", va="top", fontsize=FS_BODY, color=BODY,
                linespacing=LSP, zorder=5)
        row_y[num] = cy
        y -= h + gap

    # ================================================================
    # 右欄:四張張力卡片(等寬堆疊,順序固定 零 -> 一 -> 二 -> 三)
    # ================================================================
    CPAD = 0.008
    hx = RX0 + CPAD
    inner = (RX1 - CPAD) - hx

    # 標籤內縮 <= FLUSH 時用懸掛縮排;標籤過長時續行齊左,免得可用寬度被吃掉
    FLUSH = 0.085
    wc = []
    for c in CARDS:
        rows = []
        for lab, body, col in c["rows"]:
            lw = W(lab + ":", FS_BODY, bold=True) + 0.004
            hang = lw <= FLUSH
            lines = wrap2(body, FS_BODY, inner - lw, inner - (lw if hang else 0.0))
            rows.append((lab, body, col, lw, hang, lines))
        wc.append(rows)

    QH = 0.036
    RPAD = 0.004
    need_c = []
    for c, rows in zip(CARDS, wc):
        h = 0.012 + LH_CARD + 0.005 \
            + sum(len(r[5]) * LH + RPAD for r in rows) + 0.008
        if c["quote"]:
            h += QH + 0.004
        need_c.append(h)

    CTOP, CBOT = 0.990, BOTY
    cgap = max((CTOP - CBOT - sum(need_c)) / (len(need_c) - 1), 0.008)
    assert sum(need_c) + 3 * 0.008 <= CTOP - CBOT, "卡片總高超出版面,需縮字或改寫"

    card_box = []
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

        hy = top - 0.012 - LH_CARD / 2
        head = RED if strong else (ORANGE_DARK if c.get("accent") else NAVY)
        pw = pill(ax, hx, hy, c["tag"], head, "white", z=6)
        nx = hx + pw + 0.007
        ax.text(nx, hy, c["name"], ha="left", va="center", fontsize=FS_CARD,
                color=head, fontweight="bold", zorder=6)
        if c["cite"]:
            ax.text(nx + W(c["name"], FS_CARD, bold=True) + 0.010, hy, c["cite"],
                    ha="left", va="center", fontsize=FS_BODY, color=GREY, zorder=6)

        ty = top - 0.012 - LH_CARD - 0.005
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

        if c["quote"]:
            qy = top - h + 0.008
            ax.add_patch(FancyBboxPatch((RX0 + 0.006, qy), (RX1 - RX0) - 0.012, QH,
                                        boxstyle="round,pad=0,rounding_size=.007",
                                        fc=NAVY, ec=NAVY, zorder=6))
            ax.text((RX0 + RX1) / 2, qy + QH / 2, "「" + c["quote"] + "」",
                    ha="center", va="center", fontsize=FS_QUOTE, color="white",
                    fontweight="bold", zorder=7)

        card_box.append((top, top - h))
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
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_07")
