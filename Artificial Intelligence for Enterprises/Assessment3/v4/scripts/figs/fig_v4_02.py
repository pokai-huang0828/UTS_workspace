# -*- coding: utf-8 -*-
"""P2 用圖 —— 為什麼是現在:工作量沒變多,客戶要的時效變了。

主視覺 = 那一件判讀的 latency waterfall(帶 1 已知粗結構 / 帶 2 未知細結構 /
帶 3 判定句)+ 右下角壓力測試框 + 頂部平均編制口徑算式帶 + 下方業務基準帶
+ 右側人力堆疊與成長方向(含階梯佐證框)。

紅線:
- 圖不畫投影片標題、不畫頁首進度指示(那兩樣由組版程式負責)。
- 色值只取自 make_figs_v4 的色票常數(ORANGE #E8833A / NAVY #1F4E79 ...)。
- 全圖最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形減號 / 破折號。
- 主圖不得出現任何「Y 軸 = 人力」的柱狀圖,不得出現 3.5-4.8 / 5.5-9.0 / 9.0-15.8。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    plt, np, FancyArrowPatch, FancyBboxPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, RED,
    newfig, save, assert_min_fontsize,
)

# ---- 本圖用到的中性灰階(非色相,不屬色票語意色) -------------------
BAND_BG = "#F7F7F7"      # 算式帶 / 業務基準帶底
DARKCELL = "#3F3F3F"     # 算式帶格 3 深灰底
INK = "#333333"          # 內文深灰
INK2 = "#5A5A5A"         # 次級灰
RULE = "#BFBFBF"         # 分隔線
BOX_BG = "#FFF7E0"       # 壓力測試框 / 階梯佐證框 底(規格指定)
BOX_EC = "#E0C271"       # 上述框線(規格指定)
FLAG = "#8C8C8C"         # 旗標灰(規格指定)
STACK_MID = "#E0B84C"    # 人力堆疊中層黃(規格指定)

# ---- 版面常數 ------------------------------------------------------
L0, L1 = 0.006, 0.640          # 左主圖欄
S0, S1 = 0.658, 0.996          # 右側欄
PX0, PX5 = 0.040, 0.545        # waterfall X 軸 0 天 / 5 天
DAY = (PX5 - PX0) / 5.0


def _line(ax, x0, x1, y0, y1, color, lw=1.0, ls="-", z=5, alpha=1.0):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls,
            zorder=z, alpha=alpha, solid_capstyle="butt")


def _rect(ax, x, y, w, h, fc, ec="none", lw=1.0, ls="-", z=3):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def _round(ax, x, y, w, h, fc, ec, lw=1.2, z=3, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


# ==================================================================
# 一、頂部:平均編制口徑算式帶
# ==================================================================
def _formula_band(ax):
    top, bot = 0.995, 0.825
    _rect(ax, L0, bot, S1 - L0, top - bot, BAND_BG, ec=RULE, lw=0.8, z=2)

    # 口徑宣告標題(不可省)
    ax.text(0.014, 0.990, "平均編制口徑:每日工作量 ÷ 每日產能",
            ha="left", va="top", fontsize=12, color=INK, fontweight="bold", zorder=6)

    cy_t, cy_b = 0.958, 0.828
    c1, c2, c3 = L0, 0.362, 0.758

    # 格 3 深灰底
    _rect(ax, c3, cy_b, S1 - c3, cy_t - cy_b, DARKCELL, z=3)
    # 格間 1pt 白線
    for x in (c2, c3):
        _line(ax, x, x, cy_b, cy_t, "white", lw=1.6, z=6)

    # --- 格 1 -------------------------------------------------------
    ax.text(c1 + .010, 0.952, "例行批次複核 · 全量",
            ha="left", va="top", fontsize=11, color=NAVY, fontweight="bold", zorder=6)
    ax.text(c1 + .010, 0.905, "3,000 筆 × 20 秒 ÷ 3,600 = 16.7 人時/天",
            ha="left", va="center", fontsize=13, color=INK, zorder=6)
    ax.text(c1 + .010, 0.836, "證據等級:營運端的實務估計,尚未以計時量測驗證",
            ha="left", va="bottom", fontsize=9, color=INK2, zorder=6)

    # --- 格 2 -------------------------------------------------------
    ax.text(c2 + .012, 0.952, "客戶爭議深入判讀 · 客戶回頭標記的 5-10%",
            ha="left", va="top", fontsize=11, color=NAVY, fontweight="bold", zorder=6)
    ax.text(c2 + .012, 0.905, "3,000 筆 × 5-10% × 4.4 分 ÷ 60 = 11.0-22.0 人時/天",
            ha="left", va="center", fontsize=13, color=INK, zorder=6)
    ax.text(c2 + .012, 0.836, "證據等級:由一次實際判讀反推(5 人 × 3 天 × 8 小時 ÷ 1,647 筆)",
            ha="left", va="bottom", fontsize=9, color=INK2, zorder=6)

    # --- 格 3(深灰底白字)-----------------------------------------
    ax.text((c3 + S1) / 2, 0.952,
            "合計 27.7-38.7 人時/天 ÷ 40 人時/天\n= 利用率 69%-97%,折算 3.5-4.8 人",
            ha="center", va="top", fontsize=14, color="white",
            fontweight="bold", linespacing=1.3, zorder=6)
    ax.text(c3 + .008, 0.833,
            "本格為提案人依現有單價所做的推算;此處的『折算人數』\n"
            "是平均編制,不是任何一天的同時在線人力。",
            ha="left", va="bottom", fontsize=9, color="#CFCFCF",
            linespacing=1.3, zorder=6)

    # --- 算式帶正下方的引言(左側 4px 深藍色條)---------------------
    _rect(ax, L0, 0.780, 0.0035, 0.036, NAVY, z=4)
    ax.text(0.016, 0.798, "在平均意義上,今天這五個人是剛剛好,不是有餘裕。",
            ha="left", va="center", fontsize=13, color=NAVY, fontweight="bold", zorder=6)


# ==================================================================
# 二、口徑分隔帶(算式帶與主圖之間,不得相鄰)
# ==================================================================
def _divider(ax):
    _line(ax, L0, S1, 0.756, 0.756, RULE, lw=1.0, z=4)
    ax.text(0.501, 0.756,
            "以下換一個口徑:不是每天要幾個人,是那一件的時間怎麼被用掉",
            ha="center", va="center", fontsize=10, color=INK2, zorder=6,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="none"))


# ==================================================================
# 三、主圖:那一件判讀的 latency waterfall
# ==================================================================
def _waterfall(ax):
    # 主圖標題 + 母體標籤(此為圖內小標,非投影片標題)
    ax.text(L0 + .004, 0.732,
            "那一件判讀,時間是這樣被用掉的;而其中大部分,我們還沒有拆開",
            ha="left", va="top", fontsize=13, color=INK, fontweight="bold", zorder=6)
    ax.text(L0 + .004, 0.704,
            "這一件 = 1,647 筆事件的批次判讀(某小型車隊 · 單月 · 4 台車 · 23 天)",
            ha="left", va="top", fontsize=10, color=INK2, zorder=6)

    # --- X 軸:時間(工作日),刻度每 1 個工作日一格 ----------------
    ay = 0.652
    _line(ax, PX0, PX5 + .010, ay, ay, "#8A8A8A", lw=1.2, z=5)
    for d in range(6):
        x = PX0 + d * DAY
        _line(ax, x, x, ay, ay - .007, "#8A8A8A", lw=1.2, z=5)
        ax.text(x, ay + .004, str(d), ha="center", va="bottom",
                fontsize=11, color=INK2, zorder=6)
    ax.text(PX5 + .016, ay + .004, "工作日", ha="left", va="bottom",
            fontsize=11, color=INK2, fontweight="bold", zorder=6)

    # --- 帶 1:已知的粗結構 ----------------------------------------
    b1b, b1t = 0.563, 0.643
    xa0, xa1 = PX0, PX0 + 3 * DAY
    xb0, xb1 = xa1, PX5
    _rect(ax, xa0, b1b, xa1 - xa0, b1t - b1b, ORANGE, z=3)
    _rect(ax, xb0, b1b, xb1 - xb0, b1t - b1b, ORANGE_DARK, z=3)
    _line(ax, xa1, xa1, b1b, b1t, "white", lw=1.6, z=5)

    ax.text((xa0 + xa1) / 2, 0.626, "分析:約 3 個工作日", ha="center", va="center",
            fontsize=13, color="white", fontweight="bold", zorder=6)
    ax.text((xa0 + xa1) / 2, 0.607, "5 位專職分析人員並行 · 合計 120 人時",
            ha="center", va="top", fontsize=10, color="white", zorder=6)

    ax.text((xb0 + xb1) / 2, 0.626, "整理與回信:約 2 個工作日", ha="center", va="center",
            fontsize=13, color="white", fontweight="bold", zorder=6)
    ax.text((xb0 + xb1) / 2, 0.607, "不含在那 120 人時裡;\n這一段的工時從未量測",
            ha="center", va="top", fontsize=10, color="white",
            linespacing=1.25, zorder=6)

    # 段 B 右端小旗標(貼在段 B 右緣,不與 X 軸線端點混淆)
    my = (b1b + b1t) / 2
    ax.add_patch(plt.Polygon([[xb1, my + .013], [xb1 + .013, my],
                              [xb1, my - .013]], closed=True, fc=FLAG,
                             ec=FLAG, zorder=5))
    ax.text(PX5 + .019, my, "客戶收到答覆", ha="left", va="center",
            fontsize=11, color=FLAG, fontweight="bold", zorder=6)

    # --- 帶 2:未知的細結構(五欄等寬、不填色)---------------------
    b2b, b2t = 0.490, 0.552
    _round(ax, PX0, b2b, PX5 - PX0, b2t - b2b, "white", "#5A5A5A", lw=1.1, z=3)
    ax.add_patch(FancyBboxPatch((PX0, b2b), PX5 - PX0, b2t - b2b,
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc="none", ec="#5A5A5A", lw=1.1, ls=(0, (4, 3)),
                                zorder=4))
    labels = ["等待 / 排隊", "找證據", "判讀", "內部覆核", "寫報告回信"]
    colw = (PX5 - PX0) / 5.0
    for i, lb in enumerate(labels):
        cx0 = PX0 + i * colw
        if i:
            _line(ax, cx0, cx0, b2b + .004, b2t - .004, "#8A8A8A",
                  lw=1.0, ls=(0, (3, 3)), z=5)
        ax.text(cx0 + colw / 2, 0.535, "?", ha="center", va="center",
                fontsize=12, color="#5A5A5A", fontweight="bold", zorder=6)
        ax.text(cx0 + colw / 2, 0.505, lb, ha="center", va="bottom",
                fontsize=10, color=INK, zorder=6)
    ax.text(PX5 + .008, (b2b + b2t) / 2, "W1-6 交出\n這張拆解圖", ha="left", va="center",
            fontsize=11, color=NAVY, fontweight="bold", linespacing=1.3, zorder=6)

    # --- 帶 3:判定句(本圖唯一的深藍色塊)-------------------------
    b3b, b3t = 0.440, 0.478
    _rect(ax, L0 + .004, b3b, L1 - L0 - .004, b3t - b3b, NAVY, z=3)
    ax.text((L0 + L1) / 2, (b3b + b3t) / 2,
            "若主要延遲落在證據搜尋、誤報量與證據包製作 → 續行後段;"
            "否則本案轉排班方案。G1 判。",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", zorder=6)

    # --- 壓力測試框(主圖右下角)-----------------------------------
    bx0, bx1 = L1 - 0.340, L1
    by0, by1 = 0.265, 0.426
    _round(ax, bx0, by0, bx1 - bx0, by1 - by0, BOX_BG, BOX_EC, lw=1.2, z=3)
    ax.text(bx0 + .010, by1 - .007,
            "壓力測試:完美平行化下的理論下限(非人力需求實證)",
            ha="left", va="top", fontsize=11, color=ORANGE_DARK,
            fontweight="bold", zorder=6)
    ax.text(bx0 + .010, 0.394,
            "同一份 120 人時的分析,若能完美平行化:壓進 2 個工作日 → 7.5 人;\n"
            "壓進 1 個工作日 → 15.0 人。算式:120 人時 ÷(工作日數 × 8 小時)\n"
            "批次複核每天必須做完,無壓縮空間;可被時效壓縮的是爭議判讀那一條。",
            ha="left", va="top", fontsize=10, color=INK, linespacing=1.3, zorder=6)
    ax.text(bx0 + .010, 0.329,
            "四項未驗證假設:工作已全部到齊 · 任務可任意切分 ·\n"
            "無協調與 QA 成本 · 加人仍線性加速。\n"
            "因此這是下限,不是人力需求;實際節奏見左方 waterfall。",
            ha="left", va="top", fontsize=9, color=INK2, linespacing=1.3, zorder=6)
    # 框右下角外側 in-text 標記
    ax.text(bx1, 0.254, "(Hopp & Spearman, 2011)", ha="right", va="top",
            fontsize=9, color=INK2, zorder=6)

    # --- 界定小字(主圖正下方,加 1pt 上框線,不可省)---------------
    _line(ax, L0, L1, 0.234, 0.234, "#8A8A8A", lw=1.0, z=5)
    ax.text(L0 + .004, 0.230,
            "本圖的天數是這一件批次判讀的時間結構,與單件客戶爭議 2-5 天不是同一個母體;\n"
            "單件爭議的時效基準與量測落在下方業務基準帶與『效益與衡量』那一頁。",
            ha="left", va="top", fontsize=10, color=INK, linespacing=1.35, zorder=6)


# ==================================================================
# 四、業務基準帶(與主圖之間留空白帶,兩個母體)
# ==================================================================
def _baseline_band(ax):
    bb, bt = 0.028, 0.148
    _rect(ax, L0, bb, S1 - L0, bt - bb, BAND_BG, z=2)
    _line(ax, L0, S1, bt, bt, "#8A8A8A", lw=1.0, z=5)

    g1, g2 = 0.340, 0.660
    for x in (g1, g2):
        _line(ax, x, x, bb + .010, bt - .010, RULE, lw=1.0, z=5)

    ax.text(L0 + .010, 0.140,
            "基準:現況單件爭議 2-5 天\n(從分析到回信的完整鏈路)",
            ha="left", va="top", fontsize=13, color=INK,
            fontweight="bold", linespacing=1.35, zorder=6)

    ax.text(g1 + .012, 0.140, "客戶期望:2 天內;單純案件當天",
            ha="left", va="top", fontsize=13, color=INK, zorder=6)
    ax.text(g1 + .012, 0.107, "客戶期望,非已簽訂之服務水準協議",
            ha="left", va="top", fontsize=10, color=INK2,
            fontweight="bold", zorder=6)

    ax.text(g2 + .012, 0.140,
            "兩天逾時率目前沒有數字;與時間拆解同批,W1-6 交出。\n"
            "當責:複核營運主管 · 期限:第 6 週 ·\n"
            "會改變的決策:G1 是否續行後段。",
            ha="left", va="top", fontsize=10, color=INK, linespacing=1.35, zorder=6)

    ax.text(0.501, 0.034,
            "本帶與上方 waterfall 是兩個母體:上方是一件 1,647 筆的批次判讀,"
            "本帶是單件客戶爭議。兩者不得互相換算。",
            ha="center", va="bottom", fontsize=9, color=INK2, zorder=6)


# ==================================================================
# 五、右側側欄:人力堆疊 + 成長方向
# ==================================================================
def _sidebar(ax):
    sx0, sx1 = S0, 0.900

    # --- 人力堆疊(高度按人數比例)---------------------------------
    bot_b, bot_t = 0.564, 0.618      # 5 位
    mid_b, mid_t = 0.618, 0.645      # 產品經理與主管(未宣稱人數)
    top_b, top_t = 0.645, 0.720      # 7 位

    _rect(ax, sx0, bot_b, sx1 - sx0, bot_t - bot_b, NAVY, z=3)
    # 橘色母題:底層方塊的橘色識別條
    _rect(ax, sx0, bot_b, 0.0045, bot_t - bot_b, ORANGE, z=4)
    ax.text((sx0 + sx1) / 2, (bot_b + bot_t) / 2, "5 位專職分析人員 · 常態編制",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", zorder=6)

    _rect(ax, sx0, mid_b + .002, sx1 - sx0, mid_t - mid_b - .002, STACK_MID, z=3)
    ax.text((sx0 + sx1) / 2, (mid_b + mid_t) / 2 + .001, "+ 產品經理與主管 · 處理客訴",
            ha="center", va="center", fontsize=12, color=INK,
            fontweight="bold", zorder=6)

    # 頂層:2px 外框 + 陰影(規格指定,讓紅塊在版面上「明顯不該在那裡」)
    _rect(ax, sx0 + .003, top_b - .001, sx1 - sx0, top_t - top_b - .002,
          "#9A9A9A", z=2)
    _rect(ax, sx0, top_b + .002, sx1 - sx0, top_t - top_b - .002, RED,
          ec=RED, lw=2.0, z=3)
    ax.text((sx0 + sx1) / 2, (top_b + top_t) / 2 + .001,
            "+ 7 位研發工程師\n尖峰時離開本職",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", linespacing=1.3, zorder=6)

    # 頂層右側紅色引線 -> 機會成本(本頁字級第二大的文字)
    ly = (top_b + top_t) / 2
    _line(ax, sx1, 0.950, ly, ly, RED, lw=1.6, z=5)
    _line(ax, 0.950, 0.950, ly, 0.552, RED, lw=1.6, z=5)
    ax.add_patch(FancyArrowPatch((0.950, 0.552), (0.876, 0.546),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=RED, lw=1.6, zorder=5))
    ax.text(S0 + .002, 0.545, "機會成本:開發產能被拿去補分析產能",
            ha="left", va="center", fontsize=13, color=RED,
            fontweight="bold", zorder=6)

    # --- 成長方向:方向性斜線(不承載任何數值)---------------------
    ax_y = 0.486
    _line(ax, 0.674, 0.674, ax_y, 0.522, "#A6A6A6", lw=1.0, z=4)
    _line(ax, 0.674, 0.985, ax_y, ax_y, "#A6A6A6", lw=1.0, z=4)
    ax.add_patch(FancyArrowPatch((0.684, 0.490), (0.962, 0.518),
                                 arrowstyle="-|>", mutation_scale=15,
                                 color=ORANGE, lw=2.0, zorder=5))
    ax.text(0.679, 0.521, "事件量", ha="left", va="top", fontsize=9,
            color=INK2, zorder=6)
    ax.text(0.985, 0.484, "時間", ha="right", va="top", fontsize=9,
            color=INK2, zorder=6)

    ax.text(S0 + .002, 0.460, "售出台數是上限,上線台數是已實現的量。",
            ha="left", va="top", fontsize=11, color=ORANGE_DARK,
            fontweight="bold", zorder=6)
    ax.text(S0 + .002, 0.433,
            "兩者的落差,就是我們接下來要承接、但排不了程的工作量;\n"
            "開通的時點由客戶決定。",
            ha="left", va="top", fontsize=10, color=INK, linespacing=1.3, zorder=6)
    ax.text(S0 + .002, 0.389,
            "第 6 週對齊售出、開通與在線三個分母;成長不納入目前的回報估算。\n"
            "當責:複核營運主管(交付物列入評估底座那一包)· 期限:第 6 週 ·\n"
            "會改變的決策:分母對齊之後才決定成長要不要進入任何回報估算。",
            ha="left", va="top", fontsize=10, color=INK2, linespacing=1.3, zorder=6)

    # --- 階梯佐證框 -------------------------------------------------
    fb0, fb1 = 0.250, 0.324
    _round(ax, S0, fb0, S1 - S0, fb1 - fb0, BOX_BG, BOX_EC, lw=1.2, z=3)
    ax.text(S0 + .008, 0.316,
            "階梯不是斜坡:一個大型車隊約占全客戶每日\n"
            "事件量的 23.1%(3,000 ÷ 13,000 筆/天)。\n"
            "目前正在洽談中的案子裡,就有一個同級規模的車隊。",
            ha="left", va="top", fontsize=10, color=INK, linespacing=1.3, zorder=6)
    # 三階小台階圖示(第三階虛線 = 尚未發生),寬度 < 框的 40%
    st_x, st_w, st_b, st_u = 0.930, 0.020, 0.258, 0.012
    for i in range(3):
        x = st_x + i * st_w
        h = (i + 1) * st_u
        if i < 2:
            _rect(ax, x, st_b, st_w, h, ORANGE, ec=ORANGE_DARK, lw=0.8, z=5)
        else:
            _rect(ax, x, st_b, st_w, h, "none", ec=ORANGE_DARK, lw=1.1,
                  ls=(0, (3, 2)), z=5)


# ==================================================================
def build():
    fig, ax = newfig(16.0, 9.0)          # 16:9;不畫投影片標題(組版程式負責)
    ax.set_position([0, 0, 1, 1])        # 讓 0-1 座標 = 整張 16x9 畫布(排版算式的前提)
    _formula_band(ax)
    _divider(ax)
    _waterfall(ax)
    _baseline_band(ax)
    _sidebar(ax)

    # 頁腳(全寬單行,只講量不出現人數)
    ax.text(0.501, 0.024, "若涵蓋全部既有客戶,複核量將達現況四倍以上。",
            ha="center", va="top", fontsize=10, color=INK,
            fontweight="bold", zorder=6)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_02")
