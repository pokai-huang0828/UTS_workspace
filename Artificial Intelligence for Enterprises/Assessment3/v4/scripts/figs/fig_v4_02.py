# -*- coding: utf-8 -*-
"""P2 用圖 —— 為什麼是現在:工作量沒變多,客戶要的時效變了。

🔴 裁決 O 改版(畫布鎖死 12.2 x 5.7 吋,置入縮放比 = 1.0,fs=9 就是真的 9pt)。

本圖只保留「需要圖形關係才講得清楚」的主視覺:
  · 左:那一件判讀的 latency waterfall(X 軸 = 工作日;帶 1 已知粗結構 /
        帶 2 未知細結構五等欄 / 帶 3 判定句深藍塊)。
  · 右:人力堆疊(高度按人數比例)+ 紅色引線 + 成長方向斜線 + 三階台階圖示。

以下帶狀純文字元素**已移出本圖**,改由 build_deck_v4.py 以投影片文字框放置
(完整文字與擺放位置見本次交付的 moved_to_slide 清單):
  平均編制口徑算式帶(含三格與證據等級行)· 算式帶下的引言 · 口徑分隔句 ·
  界定小字(兩個母體警語之一)· 業務基準帶三格 + 帶底母體警語 ·
  壓力測試框(含 Hopp & Spearman, 2011 in-text 標記)· 成長段三行文字 + 階梯佐證兩句 ·
  頁腳「四倍以上」單行。

紅線:
- 畫布固定 newfig(12.2, 5.7);🚫 不得為了塞內容放大畫布。
- 圖不畫投影片標題、不畫頁首進度指示(那兩樣由組版程式負責)。
- 色值只取自 make_figs_v4 的色票常數(ORANGE #E8833A / NAVY #1F4E79 ...)。
- 全圖最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形減號 / 破折號。
- 主圖不得出現任何「Y 軸 = 人力」的柱狀圖,不得出現 3.5-4.8 / 5.5-9.0 / 9.0-15.8。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    plt, FancyArrowPatch, FancyBboxPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, RED,
    newfig, save, assert_min_fontsize,
)

# ---- 本圖用到的中性灰階(非色相,不屬色票語意色) -------------------
INK = "#333333"          # 內文深灰
INK2 = "#5A5A5A"         # 次級灰
FLAG = "#8C8C8C"         # 旗標灰(規格指定)
STACK_MID = "#E0B84C"    # 人力堆疊中層黃(規格指定)

# ---- 版面常數(0-1 座標 = 12.2 x 5.7 吋畫布)-----------------------
# 只使用畫布的上半段;save() 的 bbox_inches="tight" 會裁掉下方空白,
# 裁切後實體寬 <= 12.2 吋 → 置入投影片內容區縮放比 = 1.0。
L0, L1 = 0.010, 0.688          # 左主圖欄
S0, S1 = 0.706, 0.990          # 右側欄
PX0, PX5 = 0.030, 0.560        # waterfall X 軸 0 天 / 5 天
DAY = (PX5 - PX0) / 5.0


def _line(ax, x0, x1, y0, y1, color, lw=1.0, ls="-", z=5, alpha=1.0):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls,
            zorder=z, alpha=alpha, solid_capstyle="butt")


def _rect(ax, x, y, w, h, fc, ec="none", lw=1.0, ls="-", z=3):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def _round(ax, x, y, w, h, fc, ec, lw=1.2, z=3, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


# ==================================================================
# 一、主圖:那一件判讀的 latency waterfall
# ==================================================================
def _waterfall(ax):
    # 圖內小標 + 母體標籤(規格「不可省」;是這張圖自己的標題,非投影片標題)
    ax.text(L0 + .004, 0.990,
            "那一件判讀,時間是這樣被用掉的;而其中大部分,我們還沒有拆開",
            ha="left", va="top", fontsize=13, color=INK, fontweight="bold", zorder=6)
    ax.text(L0 + .004, 0.951,
            "這一件 = 1,647 筆事件的批次判讀(某小型車隊 · 單月 · 4 台車 · 23 天)",
            ha="left", va="top", fontsize=10, color=INK2, zorder=6)

    # --- X 軸:時間(工作日),刻度每 1 個工作日一格 ----------------
    ay = 0.884
    _line(ax, PX0, PX5 + .010, ay, ay, "#8A8A8A", lw=1.2, z=5)
    for d in range(6):
        x = PX0 + d * DAY
        _line(ax, x, x, ay, ay - .010, "#8A8A8A", lw=1.2, z=5)
        ax.text(x, ay + .004, str(d), ha="center", va="bottom",
                fontsize=10, color=INK2, zorder=6)
    ax.text(PX5 + .018, ay + .004, "工作日", ha="left", va="bottom",
            fontsize=10, color=INK2, fontweight="bold", zorder=6)

    # --- 帶 1:已知的粗結構 ----------------------------------------
    b1b, b1t = 0.756, 0.868
    xa0, xa1 = PX0, PX0 + 3 * DAY
    xb0, xb1 = xa1, PX5
    _rect(ax, xa0, b1b, xa1 - xa0, b1t - b1b, ORANGE, z=3)
    _rect(ax, xb0, b1b, xb1 - xb0, b1t - b1b, ORANGE_DARK, z=3)
    _line(ax, xa1, xa1, b1b, b1t, "white", lw=1.6, z=5)

    ax.text((xa0 + xa1) / 2, 0.848, "分析:約 3 個工作日", ha="center", va="center",
            fontsize=13, color="white", fontweight="bold", zorder=6)
    ax.text((xa0 + xa1) / 2, 0.826, "5 位專職分析人員並行 · 合計 120 人時",
            ha="center", va="top", fontsize=10, color="white", zorder=6)

    ax.text((xb0 + xb1) / 2, 0.848, "整理與回信:約 2 個工作日", ha="center", va="center",
            fontsize=13, color="white", fontweight="bold", zorder=6)
    ax.text((xb0 + xb1) / 2, 0.826, "不含在那 120 人時裡;\n這一段的工時從未量測",
            ha="center", va="top", fontsize=10, color="white",
            linespacing=1.25, zorder=6)

    # 段 B 右端小旗標(貼在段 B 右緣,不與 X 軸線端點混淆)
    my = (b1b + b1t) / 2
    ax.add_patch(plt.Polygon([[xb1, my + .015], [xb1 + .013, my],
                              [xb1, my - .015]], closed=True, fc=FLAG,
                             ec=FLAG, zorder=5))
    ax.text(PX5 + .019, my, "客戶收到答覆", ha="left", va="center",
            fontsize=11, color=FLAG, fontweight="bold", zorder=6)

    # --- 帶 2:未知的細結構(五欄等寬、不填色)---------------------
    b2b, b2t = 0.596, 0.721
    _round(ax, PX0, b2b, PX5 - PX0, b2t - b2b, "white", "#5A5A5A", lw=1.1, z=3)
    ax.add_patch(FancyBboxPatch((PX0, b2b), PX5 - PX0, b2t - b2b,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc="none", ec="#5A5A5A", lw=1.1, ls=(0, (4, 3)),
                                zorder=4))
    labels = ["等待 / 排隊", "找證據", "判讀", "內部覆核", "寫報告回信"]
    colw = (PX5 - PX0) / 5.0
    for i, lb in enumerate(labels):
        cx0 = PX0 + i * colw
        if i:
            _line(ax, cx0, cx0, b2b + .006, b2t - .006, "#8A8A8A",
                  lw=1.0, ls=(0, (3, 3)), z=5)
        ax.text(cx0 + colw / 2, 0.693, "?", ha="center", va="center",
                fontsize=12, color="#5A5A5A", fontweight="bold", zorder=6)
        ax.text(cx0 + colw / 2, 0.609, lb, ha="center", va="bottom",
                fontsize=10, color=INK, zorder=6)
    ax.text(PX5 + .008, 0.6585, "W1-6 交出\n這張拆解圖", ha="left", va="center",
            fontsize=11, color=NAVY, fontweight="bold", linespacing=1.3, zorder=6)

    # --- 帶 3:判定句(本圖唯一的深藍色塊)-------------------------
    b3b, b3t = 0.499, 0.556
    _rect(ax, L0 + .004, b3b, L1 - L0 - .004, b3t - b3b, NAVY, z=3)
    ax.text((L0 + L1) / 2, (b3b + b3t) / 2,
            "若主要延遲落在證據搜尋、誤報量與證據包製作 -> 續行後段;"
            "否則本案轉排班方案。G1 判。",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", zorder=6)


# ==================================================================
# 二、右側側欄:人力堆疊 + 成長方向
# ==================================================================
def _sidebar(ax):
    sx0, sx1 = S0, 0.945

    # --- 人力堆疊(高度按人數比例:5 : (未宣稱) : 7)---------------
    unit = 0.0127
    bot_b, bot_t = 0.795, 0.795 + 5 * unit          # 5 位
    mid_b, mid_t = bot_t, bot_t + 0.036             # 產品經理與主管(未宣稱人數)
    top_b, top_t = mid_t, mid_t + 7 * unit          # 7 位

    _rect(ax, sx0, bot_b, sx1 - sx0, bot_t - bot_b, NAVY, z=3)
    # 橘色母題:底層方塊的橘色識別條(沿用 P1 方塊 C 的色值)
    _rect(ax, sx0, bot_b, 0.0045, bot_t - bot_b, ORANGE, z=4)
    ax.text((sx0 + sx1) / 2, (bot_b + bot_t) / 2, "5 位專職分析人員 · 常態編制",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", zorder=6)

    _rect(ax, sx0, mid_b + .0015, sx1 - sx0, mid_t - mid_b - .003, STACK_MID, z=3)
    ax.text((sx0 + sx1) / 2, (mid_b + mid_t) / 2, "+ 產品經理與主管 · 處理客訴",
            ha="center", va="center", fontsize=12, color=INK,
            fontweight="bold", zorder=6)

    # 頂層:2px 外框 + 陰影(讓紅塊在版面上「明顯不該在那裡」)
    _rect(ax, sx0 + .003, top_b - .0015, sx1 - sx0, top_t - top_b, "#9A9A9A", z=2)
    _rect(ax, sx0, top_b + .0015, sx1 - sx0, top_t - top_b, RED,
          ec=RED, lw=2.0, z=3)
    ax.text((sx0 + sx1) / 2, (top_b + top_t) / 2 + .0015,
            "+ 7 位研發工程師\n尖峰時離開本職",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", linespacing=1.3, zorder=6)

    # 頂層右側紅色引線 -> 機會成本(本頁字級第二大的文字)
    ly = (top_b + top_t) / 2
    oy = 0.742
    _line(ax, sx1, 0.960, ly, ly, RED, lw=1.6, z=5)
    _line(ax, 0.960, 0.960, ly, oy, RED, lw=1.6, z=5)
    ax.add_patch(FancyArrowPatch((0.960, oy), (0.892, oy),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=RED, lw=1.6, zorder=5))
    ax.text(S0, oy, "機會成本:\n開發產能被拿去補分析產能",
            ha="left", va="center", fontsize=13, color=RED,
            fontweight="bold", linespacing=1.25, zorder=6)

    # --- 成長方向:方向性斜線(不承載任何數值)---------------------
    ax_y = 0.560
    _line(ax, 0.716, 0.716, ax_y, 0.675, "#A6A6A6", lw=1.0, z=4)
    _line(ax, 0.716, 0.985, ax_y, ax_y, "#A6A6A6", lw=1.0, z=4)
    ax.add_patch(FancyArrowPatch((0.726, 0.568), (0.965, 0.658),
                                 arrowstyle="-|>", mutation_scale=15,
                                 color=ORANGE, lw=2.0, zorder=5))
    ax.text(0.716, 0.688, "事件量", ha="left", va="top", fontsize=10,
            color=INK2, zorder=6)
    ax.text(0.985, 0.556, "時間", ha="right", va="top", fontsize=10,
            color=INK2, zorder=6)

    # --- 三階小台階圖示(第三階虛線 = 尚未發生)+ 圖示標題 ----------
    st_x, st_w, st_b, st_u = 0.706, 0.020, 0.492, 0.013
    for i in range(3):
        x = st_x + i * st_w
        h = (i + 1) * st_u
        if i < 2:
            _rect(ax, x, st_b, st_w, h, ORANGE, ec=ORANGE_DARK, lw=0.8, z=5)
        else:
            _rect(ax, x, st_b, st_w, h, "none", ec=ORANGE_DARK, lw=1.1,
                  ls=(0, (3, 2)), z=5)
    ax.text(0.775, 0.512, "階梯,不是斜坡", ha="left", va="center",
            fontsize=11, color=ORANGE_DARK, fontweight="bold", zorder=6)


# ==================================================================
def build():
    # 🔴 裁決 O:畫布固定 12.2 x 5.7 吋,不得放大。
    fig, ax = newfig(12.2, 5.7)

    # 座標尺度鎖死為「1.0 x 單位 = 12.2 吋 / 1.0 y 單位 = 5.7 吋」,
    # 再把 axes 收到實際用到的那塊(X0..X1, Y0..Y1)。
    # save() 用 bbox_inches="tight"(pad 0.1 吋/邊),裁切後:
    #   寬 = 0.980 x 12.2 + 0.2 = 12.16 吋 <= 12.2 吋 → 置入縮放比 1.0,fs 值即真實 pt。
    X0, X1 = 0.010, 0.990
    Y0, Y1 = 0.488, 0.996
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    ax.set_position([0.010, 0.300, (X1 - X0), (Y1 - Y0)])

    _waterfall(ax)
    _sidebar(ax)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_02")
