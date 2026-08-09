# -*- coding: utf-8 -*-
"""P2 用圖 —— 為什麼是現在:工作量沒變多,客戶要的時效變了。

🔴 裁決 O 改版(畫布鎖死 12.2 x 5.7 吋,置入縮放比 = 1.0,fs=9 就是真的 9pt)。
🔴 2026-08-09 依 `notes/15_Kenny第二批答覆_全案重算.md`(位階最高)全面重畫:
   · 節奏改 3.6 個分析日 + 0.5 天整理回信(全程 4.1 天,不是 5 天)
   · 144 人時(不是 120);每筆深入判讀 5.25 分(不是 4.4 分)
   · 帶 2 五個問號**全部填上 Q45 的時間拆解**,並標出 AI 可處理段佔全程 60%-64%
   · 人力堆疊補上「折算 3.7-5.4 人 · 尖峰已不夠」(舊敘事「剛剛好」已作廢)

本圖只保留「需要圖形關係才講得清楚」的主視覺:
  · 左:那一件判讀的 latency waterfall(X 軸 = 工作日;帶 1 = 1,647 筆批次的實際節奏 /
        帶 2 = 單件客戶爭議的時間拆解五欄 + AI 可處理段括弧 / 帶 3 判定句深藍塊)。
  · 右:人力堆疊(高度按人數比例)+ 紅色引線 + 成長方向斜線 + 三階台階圖示。

以下帶狀純文字元素**已移出本圖**,改由 build_deck_v4.py 以投影片文字框放置
(完整文字與擺放位置見 module-level 的 SLIDE_TEXT 與 notes/14 區塊 1):
  平均編制口徑算式帶(含三格與證據等級行)· 算式帶下的引言 · 口徑分隔句 ·
  界定小字(兩個母體警語之一)· 業務基準帶三格 + 帶底母體警語 ·
  壓力測試框(含 Hopp & Spearman, 2011 in-text 標記)· 成長段三行文字 + 階梯佐證兩句 ·
  頁腳「四倍以上」單行。

紅線:
- 畫布固定 newfig(12.2, 5.7);🚫 不得為了塞內容放大畫布。
- 圖不畫投影片標題、不畫頁首進度指示(那兩樣由組版程式負責)。
- 色值只取自 make_figs_v4 的色票常數(ORANGE #E8833A / NAVY #1F4E79 ...)。
- 全圖最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形減號 / 破折號。
- 主圖不得出現任何「Y 軸 = 人力」的柱狀圖。
- 🚫 作廢數字一個都不得出現:4.4 分 · 120 人時 · 27.7-38.7 · 69%-97% · 3.5-4.8 人 ·
  119.9-167.5 · 15-21 人 · 10-16 人 · 3.0/7.5/15.0 人 · 13 倍 · 全程 5 天。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    plt, FancyArrowPatch, FancyBboxPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT, RED,
    newfig, save, assert_min_fontsize,
)

# ---- 本圖用到的中性灰階(非色相,不屬色票語意色) -------------------
INK = "#333333"          # 內文深灰
INK2 = "#5A5A5A"         # 次級灰
FLAG = "#8C8C8C"         # 旗標灰(規格指定)
STACK_MID = "#E0B84C"    # 人力堆疊中層黃(規格指定)

# ---- 版面常數(0-1 座標 = 12.2 x 5.7 吋畫布)-----------------------
L0, L1 = 0.010, 0.688          # 左主圖欄
S0, S1 = 0.706, 0.945          # 右側欄

# 帶 1 waterfall 的 X 軸:0 - 4.5 個工作日(實際用掉 4.1 天)
PX0 = 0.030
PX_AXIS_END = 0.513
DAY = (PX_AXIS_END - PX0) / 4.5
X_ANALYSIS_END = PX0 + 3.6 * DAY      # 分析段結束(第 3.6 天)
X_DONE = PX0 + 4.1 * DAY              # 客戶收到答覆(第 4.1 天)

# 帶 2 單件爭議拆解:五等欄
BX0, BX1 = 0.030, 0.556
COLW = (BX1 - BX0) / 5.0


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
# 一、主圖:那一件判讀的 latency waterfall(帶 1)
# ==================================================================
def _waterfall(ax):
    # 圖內小標 + 母體標籤(規格「不可省」;是這張圖自己的標題,非投影片標題)
    ax.text(L0 + .004, 0.9945,
            "那一件判讀,時間是這樣被用掉的;而爭議案件的時間,現在也拆開了",
            ha="left", va="top", fontsize=13, color=INK, fontweight="bold", zorder=6)
    ax.text(L0 + .004, 0.9585,
            "這一件 = 1,647 筆事件的批次判讀(某小型車隊 · 單月 · 4 台車 · 23 天)",
            ha="left", va="top", fontsize=10, color=INK2, zorder=6)

    # --- X 軸:時間(工作日),刻度每 1 個工作日一格 ----------------
    ay = 0.8955
    _line(ax, PX0, PX_AXIS_END, ay, ay, "#8A8A8A", lw=1.2, z=5)
    for d in range(5):
        x = PX0 + d * DAY
        _line(ax, x, x, ay, ay - .010, "#8A8A8A", lw=1.2, z=5)
        ax.text(x, ay + .003, str(d), ha="center", va="bottom",
                fontsize=10, color=INK2, zorder=6)
    ax.text(PX_AXIS_END + .012, ay + .003, "工作日", ha="left", va="bottom",
            fontsize=10, color=INK2, fontweight="bold", zorder=6)

    # --- 帶 1:1,647 筆批次的實際節奏(3.6 天分析 + 0.5 天整理回信)---
    b1b, b1t = 0.766, 0.884
    _rect(ax, PX0, b1b, X_ANALYSIS_END - PX0, b1t - b1b, ORANGE, z=3)
    _rect(ax, X_ANALYSIS_END, b1b, X_DONE - X_ANALYSIS_END, b1t - b1b,
          ORANGE_DARK, z=3)
    _line(ax, X_ANALYSIS_END, X_ANALYSIS_END, b1b, b1t, "white", lw=1.6, z=5)

    cxa = (PX0 + X_ANALYSIS_END) / 2
    ax.text(cxa, 0.868, "分析:3.6 個工作日", ha="center", va="top",
            fontsize=13, color="white", fontweight="bold", zorder=6)
    ax.text(cxa, 0.830, "5 位專職分析人員並行 · 合計 144 人時",
            ha="center", va="top", fontsize=10, color="white", zorder=6)
    ax.text(cxa, 0.800, "-> 每筆深入判讀 5.25 分(144 人時 ÷ 1,647 筆)",
            ha="center", va="top", fontsize=10, color="white", zorder=6)

    # 段末小旗標(貼在 4.1 天處)+ 右側三行說明
    my = (b1b + b1t) / 2
    ax.add_patch(plt.Polygon([[X_DONE, my + .015], [X_DONE + .013, my],
                              [X_DONE, my - .015]], closed=True, fc=FLAG,
                             ec=FLAG, zorder=5))
    cox = X_DONE + .022
    ax.text(cox, 0.876, "客戶收到答覆 · 第 4.1 天", ha="left", va="top",
            fontsize=11, color=FLAG, fontweight="bold", zorder=6)
    ax.text(cox, 0.840, "末段 0.5 天 = 整理與回信", ha="left", va="top",
            fontsize=11, color=ORANGE_DARK, fontweight="bold", zorder=6)
    ax.text(cox, 0.806, "(不含在 144 人時內,未量測)", ha="left", va="top",
            fontsize=10, color=INK2, zorder=6)


# ==================================================================
# 二、帶 2:單件客戶爭議的時間拆解(Q45;五格問號已填實)
# ==================================================================
def _breakdown(ax):
    # 帶頭:母體宣告 + 合計。右側掛逾時率與基準線互證。
    ax.text(L0 + .004, 0.752,
            "另一個母體(非上方那件批次):單件客戶爭議的時間拆解,合計 2.5-5.5 天",
            ha="left", va="top", fontsize=10, color=NAVY,
            fontweight="bold", zorder=6)
    ax.text(L1, 0.752, "約半數爭議超過兩天;與登記在案的 2-5 天吻合",
            ha="right", va="top", fontsize=10, color=ORANGE_DARK,
            fontweight="bold", zorder=6)

    b2b, b2t = 0.638, 0.720
    # (段名, 天數, 是否 AI 可處理)
    cells = [
        ("等待 / 排隊", "0-1 天", False),
        ("撈數據 · 找證據", "0.5 天", True),
        ("判讀", "1-3 天", True),
        ("內部覆核", "0.5 天", False),
        ("寫報告回信", "0.5 天", False),
    ]
    _round(ax, BX0, b2b, BX1 - BX0, b2t - b2b, "white", "#5A5A5A", lw=1.1, z=3)
    for i, (lb, days, is_ai) in enumerate(cells):
        cx0 = BX0 + i * COLW
        if is_ai:
            _rect(ax, cx0 + (.0015 if i else 0), b2b + .0015,
                  COLW - .003, (b2t - b2b) - .003, ORANGE_LIGHT, z=4)
        if i:
            _line(ax, cx0, cx0, b2b + .006, b2t - .006, "#8A8A8A",
                  lw=1.0, ls=(0, (3, 3)), z=5)
        ax.text(cx0 + COLW / 2, 0.714, lb, ha="center", va="top",
                fontsize=11, color=INK if is_ai else INK2, zorder=6)
        ax.text(cx0 + COLW / 2, 0.680, days, ha="center", va="top",
                fontsize=13, color=ORANGE_DARK if is_ai else INK,
                fontweight="bold", zorder=6)

    # 右側:拆解已到手,量測版仍待交
    ax.text((BX1 + L1) / 2 + .004, 0.679,
            "初步拆解已到手;\nW1-6 交出量測版",
            ha="center", va="center", fontsize=11, color=NAVY,
            fontweight="bold", linespacing=1.3, zorder=6)

    # --- AI 可處理段括弧(撈數據 + 判讀 兩欄相鄰)------------------
    ax0 = BX0 + 1 * COLW
    ax1 = BX0 + 3 * COLW
    _line(ax, ax0, ax1, 0.630, 0.630, ORANGE_DARK, lw=1.8, z=5)
    _line(ax, ax0, ax0, 0.630, 0.636, ORANGE_DARK, lw=1.8, z=5)
    _line(ax, ax1, ax1, 0.630, 0.636, ORANGE_DARK, lw=1.8, z=5)
    ax.text((ax0 + ax1) / 2, 0.624,
            "AI 可處理段:1.5-3.5 天 = 全程的 60%-64%",
            ha="center", va="top", fontsize=12, color=ORANGE_DARK,
            fontweight="bold", zorder=6)

    ax.text(L1, 0.624, "非 AI 段(排隊 + 覆核 + 回信)只佔 36%-40%,",
            ha="right", va="top", fontsize=10, color=INK2, zorder=6)
    ax.text(L1, 0.596, "而排隊本身只有 0-1 天。", ha="right", va="top",
            fontsize=10, color=INK2, zorder=6)

    # --- 帶 3:判定句(本圖唯一的深藍色塊)-------------------------
    b3b, b3t = 0.507, 0.564
    _rect(ax, L0 + .004, b3b, L1 - L0 - .004, b3t - b3b, NAVY, z=3)
    ax.text((L0 + L1) / 2, (b3b + b3t) / 2,
            "規則不變:主要延遲落在 AI 可處理段 -> 續行後段,否則轉排班。"
            "拆解已指向續行,待量測確認。G1 判。",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", zorder=6)


# ==================================================================
# 三、右側側欄:人力堆疊 + 成長方向
# ==================================================================
def _sidebar(ax):
    sx0, sx1 = S0, S1

    # --- 人力堆疊(高度按人數比例:5 : (未宣稱) : 7)---------------
    unit = 0.0135
    top_t = 0.992
    top_b = top_t - 7 * unit
    mid_t = top_b
    mid_b = mid_t - 0.036
    bot_t = mid_b
    bot_b = bot_t - 5 * unit

    # 頂層:2px 外框 + 陰影(讓紅塊在版面上「明顯不該在那裡」)
    _rect(ax, sx0 + .003, top_b - .0015, sx1 - sx0, top_t - top_b, "#9A9A9A", z=2)
    _rect(ax, sx0, top_b, sx1 - sx0, top_t - top_b, RED, ec=RED, lw=2.0, z=3)
    ax.text((sx0 + sx1) / 2, (top_b + top_t) / 2,
            "+ 7 位研發工程師\n尖峰時離開本職",
            ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", linespacing=1.3, zorder=6)

    _rect(ax, sx0, mid_b + .0015, sx1 - sx0, mid_t - mid_b - .003, STACK_MID, z=3)
    ax.text((sx0 + sx1) / 2, (mid_b + mid_t) / 2, "+ 產品經理與主管 · 處理客訴",
            ha="center", va="center", fontsize=11, color=INK,
            fontweight="bold", zorder=6)

    _rect(ax, sx0, bot_b, sx1 - sx0, bot_t - bot_b, NAVY, z=3)
    # 橘色母題:底層方塊的橘色識別條(沿用 P1 方塊 C 的色值)
    _rect(ax, sx0, bot_b, 0.0045, bot_t - bot_b, ORANGE, z=4)
    ax.text((sx0 + sx1) / 2, 0.8435, "5 位專職分析人員 · 常態編制",
            ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", zorder=6)
    ax.text((sx0 + sx1) / 2, 0.8125, "折算 3.7-5.4 人 · 尖峰已不夠",
            ha="center", va="center", fontsize=10, color=ORANGE_LIGHT, zorder=6)

    # 頂層右側紅色引線 -> 機會成本(本頁字級第二大的文字)
    ly = (top_b + top_t) / 2
    oy = 0.752
    _line(ax, sx1, 0.968, ly, ly, RED, lw=1.6, z=5)
    _line(ax, 0.968, 0.968, ly, oy, RED, lw=1.6, z=5)
    ax.add_patch(FancyArrowPatch((0.968, oy), (0.898, oy),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=RED, lw=1.6, zorder=5))
    ax.text(S0, oy, "機會成本:\n開發產能被拿去補分析產能",
            ha="left", va="center", fontsize=12, color=RED,
            fontweight="bold", linespacing=1.25, zorder=6)

    # --- 成長方向:方向性斜線(不承載任何數值)---------------------
    gy = 0.560
    _line(ax, 0.716, 0.716, gy, 0.666, "#A6A6A6", lw=1.0, z=4)
    _line(ax, 0.716, 0.985, gy, gy, "#A6A6A6", lw=1.0, z=4)
    ax.add_patch(FancyArrowPatch((0.726, 0.568), (0.965, 0.654),
                                 arrowstyle="-|>", mutation_scale=15,
                                 color=ORANGE, lw=2.0, zorder=5))
    ax.text(0.716, 0.678, "事件量", ha="left", va="top", fontsize=10,
            color=INK2, zorder=6)
    ax.text(0.985, 0.556, "時間", ha="right", va="top", fontsize=10,
            color=INK2, zorder=6)

    # --- 三階小台階圖示(第三階虛線 = 尚未發生)+ 圖示標題 ----------
    st_x, st_w, st_b, st_u = 0.706, 0.019, 0.5125, 0.0095
    for i in range(3):
        x = st_x + i * st_w
        h = (i + 1) * st_u
        if i < 2:
            _rect(ax, x, st_b, st_w, h, ORANGE, ec=ORANGE_DARK, lw=0.8, z=5)
        else:
            _rect(ax, x, st_b, st_w, h, "none", ec=ORANGE_DARK, lw=1.1,
                  ls=(0, (3, 2)), z=5)
    ax.text(0.775, 0.523, "階梯,不是斜坡", ha="left", va="center",
            fontsize=11, color=ORANGE_DARK, fontweight="bold", zorder=6)


# ==================================================================
def build():
    # 🔴 裁決 O:畫布固定 12.2 x 5.7 吋,不得放大。
    fig, ax = newfig(12.2, 5.7)

    # 座標尺度鎖死為「1.0 x 單位 = 12.2 吋 / 1.0 y 單位 = 5.7 吋」,
    # 再把 axes 收到實際用到的那塊(X0..X1, Y0..Y1)。
    # save() 用 bbox_inches="tight" + pad_inches=0 → 輸出寬 <= 0.980 x 12.2 吋,
    # 置入 12.2 吋內容區縮放比 = 1.0,fs 值即真實 pt。
    X0, X1 = 0.010, 0.990
    Y0, Y1 = 0.503, 0.996
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    ax.set_position([0.010, 0.300, (X1 - X0), (Y1 - Y0)])

    _waterfall(ax)
    _breakdown(ax)
    _sidebar(ax)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_02")
