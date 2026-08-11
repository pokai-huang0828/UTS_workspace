# -*- coding: utf-8 -*-
"""P8 用圖:三層 KPI 帶(指標卡三欄制 + 否決閘 + 底部閉環)。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P8 · 怎麼算成功:三層 KPI,一條回圈」→ ## 視覺規格
畫布裁決:v4/notes/12_出圖稽核與畫布裁決.md 裁決 O —— 畫布鎖死 12.2 x 5.7 吋,
          置入投影片內容區的縮放比 = 1.0,所以圖內 fs=9 就是真的 9pt。
機具:scripts/make_figs_v4.py(直接 import,不修改)

不畫:頁首標題、右上角五格進度指示(頁面共通元素,由組版程式負責)。
不用:U+2212 負號、U+2248、U+27F2、U+2014、emoji(字型缺字或已列為禁用)。

【本頁自訂的處置順序】(規格未寫,依裁決 O 第 3 條自訂並回報)
  ① 帶狀純文字先移出圖 → 由 build_deck_v4.py 以投影片文字框放置
     (貫穿說明句、四條當責三件套、錯誤攔截比例註記、各卡限定語、閉環註記)
  ② 卡內欄位保留「數值 + 最短可辨識限定語」,完整限定語落在投影片頁腳
  ③ 仍不足時才縮短卡名 —— 本輪未動用
  🔒 全程不縮字(最小 fs=9)、不放大畫布。
"""
import logging
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # .../v4/scripts

from make_figs_v4 import (                          # noqa: E402
    plt, FancyBboxPatch, FancyArrowPatch,
    NAVY, ORANGE, ORANGE_DARK, RED, GREY, LIGHT, BLUE,
    newfig, save, assert_min_fontsize,
)

# ------------------------------------------------------------------ 度量
FW, FH = 12.2, 5.7                 # 🔒 裁決 O:畫布鎖死,不得放大
UX, UY = FW * 72.0, FH * 72.0      # 每 1 個 axes 單位 = 多少 pt
LS = 1.24                          # 行距係數
CLOSERS = "」』)〕】,、。;:!?%〉》｝/"
OPENERS = "((「『【〔《〈"

FS_BODY = 9                        # 欄位正文(= 全圖最小字級)
FS_NAME = 11                       # 卡名
FS_LAYER = 11                      # 左側層名直立色塊
FS_SIDE = 9                        # 右側成效面向直欄
FS_GATE = 11                       # 否決閘
FS_NODE = 10                       # 閉環節點


def px(pt):
    return pt / UX


def py(pt):
    return pt / UY


def _cw(ch, fs):
    """單字寬(pt)的保守估計:ASCII 半形、箭號/圓點全形、CJK 全形。"""
    o = ord(ch)
    if o < 0x2000:
        return 0.58 * fs
    if o < 0x2E80:
        return 1.00 * fs
    return 1.02 * fs


def tw(s, fs):
    return sum(_cw(c, fs) for c in s)


def tokenize(para):
    """CJK 一字一單位;連續的半形字(數字、單位、代號)綁成一個不可拆單位。

    這條是為了不讓「3,000」被折成「3,」/「000」、
    「NT$1,040-1,870」被折成「1,040-1,87」/「0」;數字被折斷會讀成別的數字。
    """
    toks, i, n = [], 0, len(para)
    while i < n:
        ch = para[i]
        if ch == " ":
            toks.append(" ")
            i += 1
        elif ord(ch) < 0x2000:
            # 半形串前導的收尾標點(如 ",W16" 的逗號)要單獨成 token,
            # 否則它會被綁進數字串、被推到行首。
            if ch in CLOSERS:
                toks.append(ch)
                i += 1
                continue
            j = i
            while j < n and ord(para[j]) < 0x2000 and para[j] != " ":
                j += 1
            toks.append(para[i:j])
            i = j
        else:
            toks.append(ch)
            i += 1
    return toks


def chunk(tk):
    """半形長串真的塞不下時的次要斷點:只在 - 或 / 之後斷,連字號留在行尾。"""
    out, cur = [], ""
    for ch in tk:
        cur += ch
        if ch in "-/":
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out or [tk]


def wrap(text, width_pt, fs):
    """依實際估寬折行:數字/代號不拆;行首不出現收尾標點。"""
    out = []
    for para in text.split("\n"):
        cur, curw = "", 0.0
        for tk in tokenize(para):
            if tk == " ":
                if cur:
                    cur += " "
                    curw += _cw(" ", fs)
                continue
            w = tw(tk, fs)
            if cur and curw + w > width_pt:
                # 收尾標點(含 ");" 這種被 tokenize 綁在一起的半形串)不得起行
                if all(c in CLOSERS for c in tk) and len(cur.rstrip()) > 1:
                    c = cur.rstrip()
                    out.append(c[:-1])
                    cur = c[-1] + tk
                    curw = tw(cur, fs)
                elif w > width_pt:
                    for ck in chunk(tk):
                        cw2 = tw(ck, fs)
                        if cur and curw + cw2 > width_pt:
                            out.append(cur.rstrip())
                            cur, curw = "", 0.0
                        cur += ck
                        curw += cw2
                else:
                    c = cur.rstrip()
                    if len(c) > 1 and c[-1] in OPENERS:
                        out.append(c[:-1])          # 行尾不留孤零零的開括號
                        cur = c[-1] + tk
                        curw = tw(cur, fs)
                    else:
                        out.append(c)
                        cur, curw = tk, w
            else:
                cur += tk
                curw += w
        out.append(cur.rstrip())
    return out


def lines_h(n, fs):
    return py(n * fs * LS)


def draw_lines(ax, x, y_top, lines, fs, color, bold=False, z=6):
    lh = py(fs * LS)
    y = y_top
    for ln in lines:
        ax.text(x, y - lh * 0.5, ln, ha="left", va="center", fontsize=fs,
                color=color, fontweight="bold" if bold else "normal", zorder=z)
        y -= lh
    return y


def draw_badge(ax, x, y_top, text, fs=FS_BODY, fc=ORANGE):
    """橘底白字小徽章(只用在欄 2)。"""
    w = tw(text, fs) + 8.0
    h = fs * 1.45
    ax.add_patch(FancyBboxPatch((x, y_top - py(h)), px(w), py(h),
                                boxstyle="round,pad=0,rounding_size=.004",
                                fc=fc, ec=fc, zorder=6))
    ax.text(x + px(w) / 2, y_top - py(h) / 2, text, ha="center", va="center",
            fontsize=fs, color="white", fontweight="bold", zorder=7)
    return y_top - py(h) - py(2.0)


# ------------------------------------------------------------------ 指標卡
SLACK = []
CARDS = []          # (x, y, w, h) —— 供 audit() 檢查文字是否都在容器框內


def draw_card(ax, x, y, w, h, name, cols, ec=NAVY, lw=1.1,
              name_color=NAVY, name_tag=None, tag_boxed=False,
              col2_header=None, tag_ibm=None):
    """三欄制指標卡。cols = [欄1, 欄2, 欄3],每欄是 [(文字, fs, 色), ...] 或 ('badge', 文字)。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc="white", ec=ec, lw=lw, zorder=3))
    CARDS.append((x, y, w, h))
    padx, pady = 5.0, 4.0
    inner_x = x + px(padx)
    inner_w = w - 2 * px(padx)

    # ---- 卡名列(右上角可掛標籤)
    tag_w = 0.0
    if name_tag is not None:
        tag_w = tw(name_tag, FS_BODY) + (6.0 if tag_boxed else 4.0)
    if tag_ibm is not None:
        tag_w = tw(tag_ibm, FS_BODY) + 4.0
    n_lines = wrap(name, inner_w * UX - tag_w - 3, FS_NAME)
    y_name_top = y + h - py(pady)
    draw_lines(ax, inner_x, y_name_top, n_lines, FS_NAME, name_color, bold=True)
    name_bot = y_name_top - lines_h(len(n_lines), FS_NAME)

    if name_tag is not None:
        ty = y_name_top - py(FS_BODY * LS) * 0.5
        if tag_boxed:
            bw, bh = tw(name_tag, FS_BODY) + 5.0, FS_BODY * 1.45
            ax.add_patch(FancyBboxPatch((x + w - px(padx + bw), ty - py(bh) / 2),
                                        px(bw), py(bh),
                                        boxstyle="round,pad=0,rounding_size=.004",
                                        fc=NAVY, ec=NAVY, zorder=6))
            ax.text(x + w - px(padx + bw / 2), ty, name_tag, ha="center",
                    va="center", fontsize=FS_BODY, color="white",
                    fontweight="bold", zorder=7)
        else:
            ax.text(x + w - px(padx), ty, name_tag, ha="right", va="center",
                    fontsize=FS_BODY, color=GREY, zorder=6)
    if tag_ibm is not None:
        ax.text(x + w - px(padx), y_name_top - py(FS_BODY * LS) * 0.5, tag_ibm,
                ha="right", va="center", fontsize=FS_BODY, color=GREY, zorder=6)

    # ---- 三欄
    fracs = (0.34, 0.33, 0.33)
    cw = [inner_w * f for f in fracs]
    cx = [inner_x, inner_x + cw[0], inner_x + cw[0] + cw[1]]
    col_top = name_bot - py(3)
    bottoms = []
    for i, items in enumerate(cols):
        text_w = cw[i] * UX - 5.0
        xx = cx[i] + px(2.5)
        yy = col_top
        if i == 1 and col2_header:
            hl = wrap(col2_header, text_w, FS_BODY)
            draw_lines(ax, xx, yy, hl, FS_BODY, GREY)
            yy -= lines_h(len(hl), FS_BODY)
            yy -= py(1.0)
        for it in items:
            if it[0] == "badge":
                yy = draw_badge(ax, xx, yy, it[1])
            else:
                txt, fs, col = it
                ln = wrap(txt, text_w, fs)
                draw_lines(ax, xx, yy, ln, fs, col)
                yy -= lines_h(len(ln), fs)
                yy -= py(1.0)
        bottoms.append(yy)
    col_bot = min(bottoms)

    # ---- 欄間 1px 淺灰分隔線(只跨欄位區,不穿過任何文字)
    for i in (1, 2):
        ax.plot([cx[i], cx[i]], [col_top, max(col_bot, y + py(3))],
                color=LIGHT, lw=0.8, zorder=4)

    slack = (col_bot - (y + py(pady))) * UY
    SLACK.append((name[:10], round(slack, 1)))
    assert slack > -0.5, "卡片內容溢出:%s(不足 %.1f pt)" % (name, -slack)


def vband(ax, x, y, w, h, label, color, fs=FS_LAYER):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=color, ec=color, zorder=4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
            color="white", fontweight="bold", rotation=90, zorder=5)


# ================================================================== 建圖
def build():
    fig, ax = newfig(FW, FH)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    LX, LW = 0.004, 0.028          # 左側直立層名色塊
    RW = 0.030                     # 右側成效面向窄欄
    RX = 0.996 - RW
    CX0, CX1 = LX + LW + 0.007, RX - 0.007
    SPAN = CX1 - CX0               # = 0.920

    TOPY = 1 - py(11)                                   # 內容頂
    b1y = TOPY - py(104)                                # 業務層帶
    b2top = b1y - py(22)                                # 22pt 細連線走廊
    b2y = b2top - py(104)                               # 營運層帶
    gate_y = b2y - py(10)
    b3top = b2y - py(20)
    b3y = b3top - py(78)                                # 護欄層帶
    loop_top = b3y - py(6)
    loop_y = loop_top - py(42)                          # 底部閉環
    legend_y = loop_y - py(10)

    # -------------------------------------------------- 帶 1|業務層
    ax.add_patch(FancyBboxPatch((LX, b1y), 0.996 - LX, py(104),
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=NAVY, ec="none", alpha=0.07, zorder=1))
    vband(ax, LX, b1y, LW, py(104), "業務層", NAVY)
    ax.text(RX + RW / 2, b1y + py(52), "利潤(成本降低)\n客戶滿意度",
            ha="center", va="center", fontsize=FS_SIDE, color=GREY,
            rotation=90, linespacing=1.35, zorder=5)

    cy1, ch1 = b1y + py(4), py(96)
    gw, g1 = 0.038, 0.0088         # gw = 橘色母題方塊寬
    w1 = (SPAN - gw - 4 * g1) / 4
    x1 = [CX0,
          CX0 + w1 + g1,
          CX0 + 2 * (w1 + g1),
          CX0 + 3 * (w1 + g1) + gw + g1]
    x_motif = CX0 + 3 * (w1 + g1)

    draw_card(
        ax, x1[0], cy1, w1, ch1, "客戶爭議回覆時效",
        [[("現況單件平均 2-5 天(從分析到回信的完整鏈路)", FS_BODY, GREY)],
         [("2 天內;單純案件當天回覆", FS_BODY, "black"), ("badge", "提案目標")],
         [("●期內建立基準;G2 給第一個趨勢,W16 後量測改善", FS_BODY, "black")]],
        ec=NAVY, lw=2.0, name_tag="主要業務價值指標", tag_boxed=True)

    draw_card(
        ax, x1[1], cy1, w1, ch1, "獲得人工驗證判定的客戶涵蓋率",
        [[("現況配給制(依購買量與問題嚴重性);涵蓋率無紀錄,W6 建立",
           FS_BODY, GREY)],
         [("以 W6 基線為準,目標值於 G1 訂定", FS_BODY, "black"),
          ("badge", "提案規劃")],
         [("○移交後", FS_BODY, "black")]])

    draw_card(
        ax, x1[2], cy1, w1, ch1, "可服務的每日事件量上限",
        [[("現況撐一個大型車隊約 3,000 筆/天", FS_BODY, GREY)],
         [("支撐全客戶 13,000+ 筆/天", FS_BODY, "black"), ("badge", "提案目標")],
         [("○移交後", FS_BODY, "black")]],
        tag_ibm="(IBM, n.d.)")

    draw_card(
        ax, x1[3], cy1, w1, ch1, "可避免的年度增聘成本",
        [[("以現行做法覆蓋全部既有客戶需 15-21 人(現有 5 人)", FS_BODY, GREY)],
         [("每年約 NT$1,040-1,870 萬", FS_BODY, "black")],
         [("○移交後", FS_BODY, "black")]],
        col2_header="不做本案時的年度增聘成本")

    # 橘色母題:人工複核防線(全片同形同色,本頁只出現一次)
    mh = py(46)
    my = cy1 + (ch1 - mh) / 2
    ax.add_patch(FancyBboxPatch((x_motif, my), gw, mh,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=ORANGE, ec=ORANGE_DARK, lw=1.2, zorder=5))
    ax.text(x_motif + gw / 2, my + mh / 2, "人工\n複核\n防線", ha="center",
            va="center", fontsize=FS_BODY, color="white", fontweight="bold",
            linespacing=1.45, zorder=6)

    # -------------------------------------------------- 帶 2|營運層
    ax.add_patch(FancyBboxPatch((LX, b2y), 0.996 - LX, py(104),
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=BLUE, ec="none", alpha=0.06, zorder=1))
    vband(ax, LX, b2y, LW, py(104), "營運層", BLUE)
    ax.text(RX + RW / 2, b2y + py(52), "節省的工時", ha="center", va="center",
            fontsize=FS_SIDE, color=GREY, rotation=90, zorder=5)

    cy2, ch2 = b2y + py(16), py(88)
    g2 = 0.0088
    w2 = (SPAN - 4 * g2) / 5
    x2 = [CX0 + i * (w2 + g2) for i in range(5)]

    draw_card(
        ax, x2[0], cy2, w2, ch2, "每筆批次複核的人工工時",
        [[("約 20 秒/筆(全量;營運端估計,未計時驗證)", FS_BODY, GREY)],
         [("W6 建立正式基準,目標值於 G1 訂定", FS_BODY, "black")],
         [("●期內", FS_BODY, "black")]],
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[1], cy2, w2, ch2, "每筆深入判讀的人工工時",
        [[("約 4.4 分鐘/筆(由一次實際判讀反推)", FS_BODY, GREY)],
         [("目標值於 W16 爭議回覆自動化交付後量測", FS_BODY, "black")],
         [("●期內", FS_BODY, "black")]],
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[2], cy2, w2, ch2, "ADAS · 行車輔助誤報率",
        [[("某小型車隊單月樣本 104 / 1,029,約 10.1%", FS_BODY, GREY)],
         [("降至 7% 以下(G2 第 12 週判)", FS_BODY, "black"),
          ("badge", "提案目標")],
         [("●期內", FS_BODY, "black")]],
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[3], cy2, w2, ch2, "客戶回頭標記率(越低越好)",
        [[("現況 5-10%", FS_BODY, GREY)],
         [("降至 5% 以下", FS_BODY, "black"), ("badge", "提案目標")],
         [("●期內", FS_BODY, "black")]],
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[4], cy2, w2, ch2, "尖峰徵調研發人時",
        [[("尖峰徵調 7 位研發工程師(非常態編制)", FS_BODY, ORANGE_DARK)],
         [("期內建立量測基準,目標值於 G2 訂定", FS_BODY, "black")],
         [("●期內建立基準,G2 後兩個月量測", FS_BODY, "black")]],
        ec=BLUE, name_color=ORANGE_DARK)

    # 營運層帶內:卡 7 → 卡 5 的因果細箭頭
    ay = b2y + py(8)
    ax.add_patch(FancyArrowPatch((x2[2] + w2 * 0.30, ay),
                                 (x2[0] + w2 * 0.50, ay),
                                 arrowstyle="-|>", mutation_scale=9,
                                 color=GREY, lw=0.9, zorder=5))
    ax.text((x2[0] + x2[2] + w2 * 0.8) / 2, ay, "誤報率 ↓ → 批次量 ↓",
            ha="center", va="center", fontsize=FS_BODY, color=GREY, zorder=6,
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none"))

    # -------------------------------------------------- 細連線(四條,不織網)
    ytop, ybot = cy1, cy2 + ch2
    for xa, xb in ((x1[0] + w1 * 0.40, x2[1] + w2 * 0.50),
                   (x1[0] + w1 * 0.60, x2[2] + w2 * 0.50),
                   (x1[2] + w1 * 0.50, x2[0] + w2 * 0.62),
                   (x1[3] + w1 * 0.50, x2[0] + w2 * 0.38)):
        ax.add_patch(FancyArrowPatch((xa, ytop), (xb, ybot),
                                     arrowstyle="-", color=LIGHT, lw=0.9,
                                     connectionstyle="arc3,rad=0.05", zorder=2))

    # -------------------------------------------------- 否決閘
    ax.plot([LX, 0.996], [gate_y, gate_y], color=RED, lw=1.8,
            ls=(0, (5, 3)), zorder=5)
    ax.text(0.5, gate_y, "否決閘:任一護欄未達標,上面兩層的成績不採計",
            ha="center", va="center", fontsize=FS_GATE, color=RED,
            fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.30", fc="white", ec="none"))

    # -------------------------------------------------- 帶 3|護欄層
    ax.add_patch(FancyBboxPatch((LX, b3y), 0.996 - LX, py(78),
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=LIGHT, ec=RED, lw=1.8, alpha=0.55, zorder=1))
    vband(ax, LX, b3y, LW, py(78), "護欄層｜否決型", RED, fs=10)
    ax.text(RX + RW / 2, b3y + py(39), "風險管理", ha="center", va="center",
            fontsize=FS_SIDE, color=GREY, rotation=90, zorder=5)

    cy3, ch3 = b3y + py(3), py(72)
    g3 = 0.012
    w3 = (SPAN - 2 * g3) / 3
    x3 = [CX0 + i * (w3 + g3) for i in range(3)]

    draw_card(
        ax, x3[0], cy3, w3, ch3, "漏放率",
        [[("目前不存在;唯一量測是一份 39 筆人工觸發測試,自註為下限",
           FS_BODY, GREY)],
         [("W6 交出帶 95% 信賴區間的點估計,上限值於 G1 由委員會核定",
           FS_BODY, "black")],
         [("●期內", FS_BODY, "black")]],
        ec=RED, name_color=RED)

    draw_card(
        ax, x3[1], cy3, w3, ch3, "複核者一致性",
        [[("現況未量測", FS_BODY, GREY)],
         [("W10 前建立基線,目標值於 G2 訂定", FS_BODY, "black")],
         [("●期內", FS_BODY, "black")]],
        ec=RED, name_color=RED)

    draw_card(
        ax, x3[2], cy3, w3, ch3, "訓練資料可追溯率",
        [[("0%", FS_BODY, GREY)],
         [("100%(否決型,無中間值)", FS_BODY, "black")],
         [("●期內", FS_BODY, "black")]],
        ec=RED, name_color=RED)

    # -------------------------------------------------- 帶 4|底部閉環
    ax.add_patch(FancyBboxPatch((LX, loop_y), 0.996 - LX, py(42),
                                boxstyle="round,pad=0,rounding_size=.010",
                                fc=ORANGE, ec=ORANGE, zorder=3))
    nodes = ["脈絡特徵讓誤報下降", "每日批次複核量下降", "釋放人力",
             "人力投入事件訓練照片生成", "訓練資料品質提升"]
    n_w, n_h = 0.160, py(24)
    n_y = loop_y + py(14)
    n_x0, n_x1 = 0.020, 0.980
    step = (n_x1 - n_x0 - n_w) / 4
    for i, t in enumerate(nodes):
        xx = n_x0 + i * step
        ax.add_patch(FancyBboxPatch((xx, n_y), n_w, n_h,
                                    boxstyle="round,pad=0,rounding_size=.006",
                                    fc=ORANGE_DARK, ec="white", lw=0.9, zorder=5))
        ax.text(xx + n_w / 2, n_y + n_h / 2, t, ha="center", va="center",
                fontsize=FS_NODE, color="white", fontweight="bold", zorder=6)
        if i < 4:
            ax.add_patch(FancyArrowPatch((xx + n_w + px(2), n_y + n_h / 2),
                                         (xx + step - px(2), n_y + n_h / 2),
                                         arrowstyle="-|>", mutation_scale=10,
                                         color="white", lw=1.4, zorder=5))
    # 回捲弧線:訓練資料品質提升 → 模型誤報下降 → 回到第一節點
    ry = loop_y + py(7)
    dx = 0.012
    ax.plot([n_x1, n_x1 + dx, n_x1 + dx], [n_y + n_h / 2, n_y + n_h / 2, ry],
            color="white", lw=1.4, zorder=5)
    ax.plot([n_x1 + dx, n_x0 - dx], [ry, ry], color="white", lw=1.4, zorder=5)
    ax.add_patch(FancyArrowPatch((n_x0 - dx, ry),
                                 (n_x0 - dx, n_y + n_h / 2 - py(1)),
                                 arrowstyle="-|>", mutation_scale=10,
                                 color="white", lw=1.4, zorder=5))
    ax.plot([n_x0 - dx, n_x0], [n_y + n_h / 2, n_y + n_h / 2],
            color="white", lw=1.4, zorder=5)
    ax.text(0.46, ry, "模型誤報下降", ha="center", va="center",
            fontsize=FS_BODY, color="white", fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.26", fc=ORANGE, ec="none"))

    # -------------------------------------------------- 欄位圖例(解碼三欄制用)
    ax.text(LX, legend_y,
            "欄位:左 = 基準與來源｜中 = 目標,或目標值由哪一道門、第幾週訂出"
            "｜右 = 量測期間(● 期內可得 ○ 移交後可得);"
            "〔提案目標〕〔提案規劃〕= 提案人設定值",
            ha="left", va="center", fontsize=FS_BODY, color=GREY, zorder=6)

    assert_min_fontsize(fig)
    return fig


# ================================================================== 自我稽核
def audit(fig):
    """1) 所有 Text 兩兩 bbox 無重疊 2) 所有 Text 都在容器框內。"""
    from matplotlib.text import Text

    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    ax = fig.axes[0]
    inv = ax.transData.inverted()

    items = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        bb = t.get_window_extent(renderer=rend)
        items.append((s.replace("\n", "/")[:24], bb,
                      bb.transformed(inv)))

    # ---- 兩兩重疊
    over = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            ix = min(a.x1, b.x1) - max(a.x0, b.x0)
            iy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ix > 0 and iy > 0:
                area = ix * iy
                small = min(a.width * a.height, b.width * b.height)
                if area > 0.02 * small:
                    over.append((items[i][0], items[j][0], round(area, 1)))
    assert not over, "文字重疊 %d 處:%s" % (len(over), over[:6])

    # ---- 在畫布內
    outside = [n for n, _, d in items
               if d.x0 < -0.001 or d.x1 > 1.001 or d.y0 < -0.001 or d.y1 > 1.001]
    assert not outside, "文字超出畫布:%s" % outside[:6]

    # ---- 在所屬卡片框內(以文字中心點歸屬)
    bad = []
    for n, _, d in items:
        cxm, cym = (d.x0 + d.x1) / 2, (d.y0 + d.y1) / 2
        for (x, y, w, h) in CARDS:
            if x <= cxm <= x + w and y <= cym <= y + h:
                if (d.x0 < x - 0.0015 or d.x1 > x + w + 0.0015
                        or d.y0 < y - 0.0015 or d.y1 > y + h + 0.0015):
                    bad.append(n)
                break
    assert not bad, "文字溢出卡片框:%s" % bad[:6]

    print("  稽核:%d 個文字物件,零重疊、零越界、%d 張卡片框內。"
          % (len(items), len(CARDS)))
    print("  卡片餘裕(pt):", SLACK)


if __name__ == "__main__":
    log = []

    class _H(logging.Handler):
        def emit(self, record):
            log.append(record.getMessage())

    h = _H(level=logging.WARNING)
    logging.getLogger("matplotlib").addHandler(h)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        f = build()
        audit(f)
        save(f, "fig_v4_08")
        msgs = [str(x.message) for x in w]
    logging.getLogger("matplotlib").removeHandler(h)
    glyph = [m for m in msgs + log
             if "findfont" in m or "missing from font" in m or "Glyph" in m]
    print("  字型警告:", glyph if glyph else "無")
    assert not glyph, "有缺字警告:%s" % glyph[:4]
