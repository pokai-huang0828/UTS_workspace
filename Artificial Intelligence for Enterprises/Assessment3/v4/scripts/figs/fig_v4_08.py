# -*- coding: utf-8 -*-
"""P8 用圖:三層 KPI 帶(指標卡三欄制 + 否決閘 + 底部閉環)。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P8 · 怎麼算成功:三層 KPI,一條回圈」→ ## 視覺規格
機具:scripts/make_figs_v4.py(直接 import,不修改)

不畫:頁首標題、右上角五格進度指示(頁面共通元素,由組版程式負責)。
不用:U+2212 負號、U+2248、U+27F2、U+2014、emoji(字型缺字或已列為禁用)。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # .../v4/scripts

from make_figs_v4 import (                          # noqa: E402
    plt, FancyBboxPatch, FancyArrowPatch,
    NAVY, ORANGE, ORANGE_DARK, RED, GREY, LIGHT, BLUE,
    newfig, save, assert_min_fontsize,
)

# ------------------------------------------------------------------ 度量
FW, FH = 16.0, 9.0                 # 16:9
UX, UY = FW * 72.0, FH * 72.0      # 每 1 個 axes 單位 = 多少 pt
LS = 1.24                          # 行距係數
CLOSERS = "」』)〕】,、。;:!?%〉》｝/"
OPENERS = "((「『【〔《〈"


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
                if len(tk) == 1 and tk in CLOSERS and len(cur.rstrip()) > 1:
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


def draw_badge(ax, x, y_top, text, fs=9, fc=ORANGE):
    """橘底白字小徽章(只用在欄 2)。"""
    w = tw(text, fs) + 9.0
    h = fs * 1.50
    ax.add_patch(FancyBboxPatch((x, y_top - py(h)), px(w), py(h),
                                boxstyle="round,pad=0,rounding_size=.004",
                                fc=fc, ec=fc, zorder=6))
    ax.text(x + px(w) / 2, y_top - py(h) / 2, text, ha="center", va="center",
            fontsize=fs, color="white", fontweight="bold", zorder=7)
    return y_top - py(h) - py(2.5)


# ------------------------------------------------------------------ 指標卡
SLACK = []


def draw_card(ax, x, y, w, h, name, cols, foot=None, foot_fs=9,
              ec=NAVY, lw=1.2, name_fs=13, name_color=NAVY,
              name_tag=None, tag_fs=10, tag_color=GREY, tag_boxed=False,
              col1_color=GREY, col2_header=None, tag_ibm=None):
    """三欄制指標卡。cols = [欄1, 欄2, 欄3],每欄是 [(文字, fs, 色), ...] 或 ('badge', 文字)。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc="white", ec=ec, lw=lw, zorder=3))
    padx, pady = 7.0, 5.0
    inner_x = x + px(padx)
    inner_w = w - 2 * px(padx)

    # ---- 卡名列(右上角可掛標籤)
    tag_w = 0.0
    if name_tag is not None:
        tag_w = tw(name_tag, tag_fs) + (10.0 if tag_boxed else 4.0)
    if tag_ibm is not None:
        tag_w = tw(tag_ibm, 9) + 4.0
    n_lines = wrap(name, inner_w * UX - tag_w - 4, name_fs)
    y_name_top = y + h - py(pady)
    draw_lines(ax, inner_x, y_name_top, n_lines, name_fs, name_color, bold=True)
    name_bot = y_name_top - lines_h(len(n_lines), name_fs)

    if name_tag is not None:
        ty = y_name_top - py(tag_fs * LS) * 0.5
        if tag_boxed:
            bw, bh = tw(name_tag, tag_fs) + 9.0, tag_fs * 1.55
            ax.add_patch(FancyBboxPatch((x + w - px(padx + bw), ty - py(bh) / 2),
                                        px(bw), py(bh),
                                        boxstyle="round,pad=0,rounding_size=.004",
                                        fc=NAVY, ec=NAVY, zorder=6))
            ax.text(x + w - px(padx + bw / 2), ty, name_tag, ha="center",
                    va="center", fontsize=tag_fs, color="white",
                    fontweight="bold", zorder=7)
        else:
            ax.text(x + w - px(padx), ty, name_tag, ha="right", va="center",
                    fontsize=tag_fs, color=tag_color, zorder=6)
    if tag_ibm is not None:
        ax.text(x + w - px(padx), y_name_top - py(9 * LS) * 0.5, tag_ibm,
                ha="right", va="center", fontsize=9, color=GREY, zorder=6)

    # ---- 三欄
    fracs = (0.34, 0.33, 0.33)
    cw = [inner_w * f for f in fracs]
    cx = [inner_x, inner_x + cw[0], inner_x + cw[0] + cw[1]]
    col_top = name_bot - py(4)
    bottoms = []
    for i, items in enumerate(cols):
        text_w = cw[i] * UX - 6.0
        xx = cx[i] + px(3)
        yy = col_top
        if i == 1 and col2_header:
            hl = wrap(col2_header, text_w, 10)
            draw_lines(ax, xx, yy, hl, 10, GREY)
            yy -= lines_h(len(hl), 10)
            yy -= py(1.5)
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

    # ---- 底緣註記(靠卡底,與欄位之間留白)
    foot_top = y
    if foot:
        fl = wrap(foot, inner_w * UX, foot_fs)
        foot_h = lines_h(len(fl), foot_fs)
        foot_top = y + py(pady * 0.6) + foot_h
        draw_lines(ax, inner_x, foot_top, fl, foot_fs, GREY)
        ax.plot([inner_x, inner_x + inner_w], [foot_top + py(3)] * 2,
                color=LIGHT, lw=0.8, zorder=4)

    # ---- 欄間 1px 淺灰分隔線(只跨欄位區,不穿過任何文字)
    sep_bot = max(col_bot, foot_top + py(4))
    for i in (1, 2):
        ax.plot([cx[i], cx[i]], [col_top, sep_bot], color=LIGHT, lw=0.8, zorder=4)

    slack = (col_bot - (foot_top + py(4))) * UY
    SLACK.append((name[:12], round(slack, 1)))
    assert slack > -0.5, "卡片內容溢出:%s(不足 %.1f pt)" % (name, -slack)


def vband(ax, x, y, w, h, label, color, fs=14):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=color, ec=color, zorder=4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
            color="white", fontweight="bold", rotation=90, zorder=5)


# ================================================================== 建圖
def build():
    fig, ax = newfig(FW, FH)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    LX, LW = 0.004, 0.040          # 左側直立層名色塊
    RX, RW = 0.958, 0.038          # 右側成效面向窄欄
    CX0, CX1 = 0.052, 0.950        # 卡片區左右界

    # -------------------------------------------------- 帶 1|業務層
    b1y, b1h = 0.712, 0.286
    ax.add_patch(FancyBboxPatch((LX, b1y), RX + RW - LX, b1h,
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=NAVY, ec="none", alpha=0.07, zorder=1))
    vband(ax, LX, b1y, LW, b1h, "業務層", NAVY)
    ax.text(RX + RW / 2, b1y + b1h / 2, "利潤(成本降低)· 客戶滿意度",
            ha="center", va="center", fontsize=10, color=GREY, rotation=90, zorder=5)

    cy, ch = 0.7425, 0.2475
    gw, gap = 0.048, 0.0085        # gw = 橘色母題方塊寬
    w1 = (CX1 - CX0 - gw - 5 * gap) / 4
    x1 = [CX0,
          CX0 + w1 + gap,
          CX0 + 2 * (w1 + gap),
          CX0 + 3 * (w1 + gap) + gw + gap]
    x_motif = CX0 + 3 * (w1 + gap)

    draw_card(
        ax, x1[0], cy, w1, ch, "客戶爭議回覆時效",
        [[("現況單件平均 2-5 天(從分析到回信的完整鏈路)", 11, GREY)],
         [("2 天內;單純案件當天回覆", 11, "black"), ("badge", "提案目標")],
         [("●期內建立基準,G2 給第一個趨勢,W16 後量測改善", 10, "black")]],
        foot="時效改善的一半來自證據包自動化,另一半來自誤報量下降(脈絡特徵 → 對照重訓)",
        foot_fs=10, ec=NAVY, lw=2.0,
        name_tag="主要業務價值指標", tag_fs=10, tag_boxed=True)

    draw_card(
        ax, x1[1], cy, w1, ch, "獲得人工驗證判定的客戶涵蓋率",
        [[("現況為配給制,依購買量與問題嚴重性排序;涵蓋率無紀錄,W6 建立", 11, GREY)],
         [("以 W6 建立的基線為準,目標值於 G1 訂定", 11, "black"), ("badge", "提案規劃")],
         [("○移交後", 10, "black")]],
        foot="當責:業務負責人 · W6 交出基線 · 它決定 G1 要不要把複核優先序從客戶大小改成風險大小")

    draw_card(
        ax, x1[2], cy, w1, ch, "可服務的每日事件量上限",
        [[("現況撐一個大型車隊約 3,000 筆/天", 11, GREY)],
         [("支撐全客戶 13,000+ 筆/天", 11, "black"), ("badge", "提案目標"),
          ("所需人力由 G2 後依實測單位工時重估", 9, GREY)],
         [("○移交後", 10, "black")]],
        foot="此項的驅動因子不在我方控制內 - 由客戶的開通時點決定",
        tag_ibm="(IBM, n.d.)")

    draw_card(
        ax, x1[3], cy, w1, ch, "可避免的年度增聘成本",
        [[("以現行做法覆蓋全部既有客戶需 15-21 人(現有 5 人)", 11, GREY)],
         [("每年約 NT$1,040-1,870 萬(以公開薪資量級推算,非核定預算)", 11, "black")],
         [("○移交後", 10, "black")]],
        col2_header="不做本案時的年度增聘成本")

    # 橘色母題:人工複核防線(全片同形同色,本頁只出現一次)
    mh = 0.100
    my = cy + (ch - mh) / 2
    ax.add_patch(FancyBboxPatch((x_motif, my), gw, mh,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=ORANGE, ec=ORANGE_DARK, lw=1.4, zorder=5))
    ax.text(x_motif + gw / 2, my + mh / 2, "人工\n複核\n防線", ha="center",
            va="center", fontsize=10, color="white", fontweight="bold",
            linespacing=1.5, zorder=6)

    # 貫穿說明句(置於業務層帶內底緣,讓帶間空隙留給細連線)
    ax.text(CX0, b1y + py(11.5),
            "最上層第一個指標,是客戶等多久拿到分析。下面兩層的指標,都是它的支撐。",
            ha="left", va="center", fontsize=12, color=NAVY,
            fontweight="bold", zorder=6)

    # -------------------------------------------------- 帶 2|營運層
    b2y, b2h = 0.368, 0.314
    ax.add_patch(FancyBboxPatch((LX, b2y), RX + RW - LX, b2h,
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=BLUE, ec="none", alpha=0.06, zorder=1))
    vband(ax, LX, b2y, LW, b2h, "營運層", BLUE)
    ax.text(RX + RW / 2, b2y + b2h / 2, "節省的工時", ha="center", va="center",
            fontsize=10, color=GREY, rotation=90, zorder=5)

    cy2, ch2 = 0.402, 0.272
    gap2 = 0.009
    w2 = (CX1 - CX0 - 4 * gap2) / 5
    x2 = [CX0 + i * (w2 + gap2) for i in range(5)]

    draw_card(
        ax, x2[0], cy2, w2, ch2, "每筆批次複核的人工工時",
        [[("約 20 秒/筆(例行批次複核 · 全量;營運端的實務估計,尚未以計時量測驗證)", 11, GREY)],
         [("W6 建立正式基準,目標值於 G1 訂定", 11, "black")],
         [("●期內", 10, "black")]],
        foot="當責:複核營運主管 · W6 交出計時量測 · 它決定全客戶人力推算要不要在 G2 整組重算",
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[1], cy2, w2, ch2, "每筆深入判讀的人工工時",
        [[("約 4.4 分鐘/筆(由一次實際判讀反推,不含報告與回信)", 11, GREY)],
         [("目標值於 W16 爭議回覆自動化交付後量測", 11, "black")],
         [("●期內", 10, "black")]],
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[2], cy2, w2, ch2, "ADAS · 行車輔助誤報率",
        [[("某小型車隊單月樣本 104 / 1,029,約 10.1%", 11, GREY)],
         [("降至 7% 以下", 11, "black"), ("badge", "提案目標"),
          ("G2 第 12 週判", 11, "black"),
          ("以該樣本為基準,G1 後依重新校準的量測重訂", 9, GREY)],
         [("●期內", 10, "black")]],
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[3], cy2, w2, ch2, "客戶回頭標記率(越低越好)",
        [[("現況 5-10%", 11, GREY)],
         [("降至 5% 以下", 11, "black"), ("badge", "提案目標")],
         [("●期內", 10, "black")]],
        foot="同時是「駕駛端無效警示率」的可觀測代理", foot_fs=10,
        ec=BLUE, name_color=BLUE)

    draw_card(
        ax, x2[4], cy2, w2, ch2, "尖峰徵調研發人時",
        [[("尖峰徵調 7 位研發工程師(離開本職、非常態編制、非專職)", 11, ORANGE_DARK)],
         [("期內建立峰值徵調人時的量測基準,目標值於 G2 訂定;歸零列為移交後目標", 11, "black")],
         [("●期內建立基準,G2 後兩個月量測(相依:脈絡特徵那一包 W5-12)", 10, "black")]],
        ec=BLUE, name_color=ORANGE_DARK)

    # 營運層帶內:卡 7 → 卡 5 的因果細箭頭
    ay = cy2 - py(11.0)
    ax.add_patch(FancyArrowPatch((x2[2] + w2 * 0.35, ay),
                                 (x2[0] + w2 * 0.45, ay),
                                 arrowstyle="-|>", mutation_scale=10,
                                 color=GREY, lw=1.0, zorder=5))
    ax.text((x2[0] + x2[2] + w2 * 0.8) / 2, ay, "誤報率 ↓ → 批次量 ↓",
            ha="center", va="center", fontsize=9, color=GREY, zorder=6,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="none"))

    # -------------------------------------------------- 細連線(四條,不織網)
    ytop, ybot = b1y, cy2 + ch2 + py(4)
    for xa, xb in ((x1[0] + w1 * 0.42, x2[1] + w2 * 0.5),
                   (x1[0] + w1 * 0.58, x2[2] + w2 * 0.5),
                   (x1[2] + w1 * 0.5, x2[0] + w2 * 0.62),
                   (x1[3] + w1 * 0.5, x2[0] + w2 * 0.38)):
        ax.add_patch(FancyArrowPatch((xa, ytop), (xb, ybot),
                                     arrowstyle="-", color=LIGHT, lw=1.0,
                                     connectionstyle="arc3,rad=0.06", zorder=2))

    # -------------------------------------------------- 否決閘
    gy = 0.358
    ax.plot([LX, RX + RW], [gy, gy], color=RED, lw=2.0, ls=(0, (5, 3)), zorder=5)
    ax.text(0.5, gy, "否決閘:任一護欄未達標,上面兩層的成績不採計",
            ha="center", va="center", fontsize=11, color=RED, fontweight="bold",
            zorder=6, bbox=dict(boxstyle="round,pad=0.35", fc="white",
                                ec="none"))

    # -------------------------------------------------- 帶 3|護欄層
    b3y, b3h = 0.134, 0.218
    ax.add_patch(FancyBboxPatch((LX, b3y), RX + RW - LX, b3h,
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=LIGHT, ec=RED, lw=2.0, alpha=0.55, zorder=1))
    vband(ax, LX, b3y, LW, b3h, "護欄層｜否決型", RED, fs=12)
    ax.text(RX + RW / 2, b3y + b3h / 2, "風險管理", ha="center", va="center",
            fontsize=10, color=GREY, rotation=90, zorder=5)

    cy3, ch3 = 0.148, 0.198
    CX3 = 0.700
    gap3 = 0.012
    w3 = (CX3 - CX0 - 2 * gap3) / 3
    x3 = [CX0 + i * (w3 + gap3) for i in range(3)]

    draw_card(
        ax, x3[0], cy3, w3, ch3, "漏放率",
        [[("目前不存在;唯一量測是一份 39 筆人工觸發測試,且自註為下限", 11, GREY)],
         [("W6 交出帶 95% 信賴區間的點估計,上限值於 G1 由委員會核定", 11, "black")],
         [("●期內", 10, "black")]],
        foot="當責:技術負責人 · W6 交出點估計與信賴區間 · 它決定 G1 放不放行後段工作",
        ec=RED, name_color=RED)

    draw_card(
        ax, x3[1], cy3, w3, ch3, "複核者一致性",
        [[("現況未量測", 11, GREY)],
         [("W10 前建立基線,目標值於 G2 訂定", 11, "black")],
         [("●期內", 10, "black")]],
        foot="當責:複核營運主管 · W10 交出基線 · 它決定 G2 准不准開放對照重訓",
        ec=RED, name_color=RED)

    draw_card(
        ax, x3[2], cy3, w3, ch3, "訓練資料可追溯率",
        [[("0%", 11, GREY)],
         [("100%(否決型,無中間值)", 11, "black")],
         [("●期內", 10, "black")]],
        ec=RED, name_color=RED)

    # 護欄層右端外側:期內不可得的那一項
    nx, nw = 0.712, 0.238
    nl = wrap("錯誤攔截比例:需漏放率先建立才算得出來,期內不可得。"
              "當責:技術負責人;待漏放率基線建立後進入移交後的常態儀表板",
              nw * UX - 18, 10)
    nh = py(12) + lines_h(len(nl) + 1, 10) + py(9)
    ny = cy3 + ch3 - nh
    ax.add_patch(FancyBboxPatch((nx, ny), nw, nh,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc="white", ec=GREY, lw=1.0, ls=(0, (4, 3)),
                                zorder=3))
    ax.text(nx + px(9), cy3 + ch3 - py(6) - py(10 * LS) * 0.5,
            "期內不可得(仍須當責與交期)", ha="left", va="center",
            fontsize=10, color=RED, fontweight="bold", zorder=6)
    draw_lines(ax, nx + px(9), cy3 + ch3 - py(6) - lines_h(1, 10) - py(3),
               nl, 10, GREY)

    # -------------------------------------------------- 帶 4|底部閉環
    by, bh = 0.024, 0.100
    ax.add_patch(FancyBboxPatch((LX, by), RX + RW - LX, bh,
                                boxstyle="round,pad=0,rounding_size=.010",
                                fc=ORANGE, ec=ORANGE, zorder=3))
    nodes = ["脈絡特徵讓誤報下降", "每日批次複核量下降", "釋放人力",
             "人力投入事件訓練照片生成", "訓練資料品質提升"]
    n_y, n_h = 0.084, 0.030
    n_x0, n_x1 = 0.030, 0.970
    n_w = 0.140
    step = (n_x1 - n_x0 - n_w) / 4
    for i, t in enumerate(nodes):
        xx = n_x0 + i * step
        ax.add_patch(FancyBboxPatch((xx, n_y), n_w, n_h,
                                    boxstyle="round,pad=0,rounding_size=.006",
                                    fc=ORANGE_DARK, ec="white", lw=1.0, zorder=5))
        ax.text(xx + n_w / 2, n_y + n_h / 2, t, ha="center", va="center",
                fontsize=11, color="white", fontweight="bold", zorder=6)
        if i < 4:
            ax.add_patch(FancyArrowPatch((xx + n_w + px(2), n_y + n_h / 2),
                                         (xx + step - px(2), n_y + n_h / 2),
                                         arrowstyle="-|>", mutation_scale=11,
                                         color="white", lw=1.6, zorder=5))
    # 回捲弧線:訓練資料品質提升 → 模型誤報下降 → 回到第一節點
    rx0, rx1, ry = n_x1, n_x0, 0.050
    dx = 0.016
    ax.plot([rx0, rx0 + dx, rx0 + dx], [n_y + n_h / 2, n_y + n_h / 2, ry],
            color="white", lw=1.6, zorder=5)
    ax.plot([rx0 + dx, rx1 - dx], [ry, ry], color="white", lw=1.6, zorder=5)
    ax.add_patch(FancyArrowPatch((rx1 - dx, ry),
                                 (rx1 - dx, n_y + n_h / 2 - py(1)),
                                 arrowstyle="-|>", mutation_scale=11,
                                 color="white", lw=1.6, zorder=5))
    ax.plot([rx1 - dx, rx1], [n_y + n_h / 2, n_y + n_h / 2],
            color="white", lw=1.6, zorder=5)
    ax.text(0.44, ry, "模型誤報下降", ha="center", va="center", fontsize=10,
            color="white", fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.30", fc=ORANGE, ec="none"))
    ax.text(RX + RW - px(10), by + py(7.5), "這條同時回答:省下的人去哪了 / 訓練資料哪裡來",
            ha="right", va="center", fontsize=9, color="white", zorder=6)

    # -------------------------------------------------- 頁腳
    ax.text(LX, 0.0075,
            "欄位:左 = 基準與來源｜中 = 目標,或目標值由哪一道門、第幾週訂出"
            "｜右 = 量測期間(● 期內可得 ○ 移交後可得)",
            ha="left", va="center", fontsize=9, color=GREY, zorder=6)
    ax.text(RX + RW, 0.0075, "移交後的成熟度階段語彙參照 (IBM, 2020)",
            ha="right", va="center", fontsize=9, color=GREY, zorder=6)

    assert_min_fontsize(fig)
    print("  卡片餘裕(pt):", SLACK)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_08")
