# -*- coding: utf-8 -*-
"""P3 用圖 —— 雙欄對照 + 根因匯流。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P3 · 發現過程:兩種病,兩個缺口」→ ## 視覺規格

上半 = 分岔(一套複核流程被拆成兩種病),下半 = 匯流(所有誤報回到同一根因)。
頁首進度指示與投影片標題由組版程式負責,本圖不畫。
負號一律 ASCII hyphen;不使用 U+2212 / 全形減號 / em dash / emoji。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matplotlib.colors import to_rgb
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from make_figs_v4 import (  # noqa: F401
    AMBER, BLUE, GREEN, GREY, LIGHT, NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT,
    RED, assert_min_fontsize, newfig, save,
)


# ------------------------------------------------------------------
# 只用機具色票常數;需要的深/淺階一律由常數混黑 / 混白推導,不另外硬寫色碼。
# ------------------------------------------------------------------
def shade(color, f):
    """f<0 混黑(變深),f>0 混白(變淺)。f 為 0~1 的混合比例。"""
    r, g, b = to_rgb(color)
    if f < 0:
        k = 1.0 + f
        return (r * k, g * k, b * k)
    return (r + (1 - r) * f, g + (1 - g) * f, b + (1 - b) * f)


DARKGREY = shade(GREY, -0.5)      # 由 GREY(#808080)混黑 50% 推得 #404040
ROWLINE = shade(GREY, 0.72)       # 列分隔線
LABELBG = shade(GREY, 0.86)       # 列標籤欄底
AMBER_PALE = shade(AMBER, 0.92)   # 根因方塊淺黃底
BANDBG = shade(GREY, 0.94)        # 下層匯流區襯底

TXT = shade(GREY, -0.75)          # 內文深灰

# ---- 版面常數(0-1 座標;圖寬 12.5in / 高 6.4in)-------------------
XL, XR = 0.020, 0.980             # 左右邊界
XLAB = 0.155                      # 列標籤欄右界
XAXIS = 0.5655                    # 中央分隔軸
GAP = 0.009                       # 軸兩側淨距
CL = (XLAB + (XAXIS - GAP)) / 2   # 左欄中心
CR = ((XAXIS + GAP) + XR) / 2     # 右欄中心

TOP_BAR_Y, TOP_BAR_H = 0.925, 0.070
T_TOP, T_BOT = 0.902, 0.500       # 對照表上下界


def build():
    fig, ax = newfig(12.5, 6.4)

    # ==============================================================
    # 一、樣本限定條(不可省、不可縮成腳註;fs=13)
    # ==============================================================
    ax.add_patch(FancyBboxPatch(
        (XL, TOP_BAR_Y), XR - XL, TOP_BAR_H,
        boxstyle="round,pad=0,rounding_size=.012",
        fc=DARKGREY, ec=DARKGREY, zorder=3))
    ax.text((XL + XR) / 2, TOP_BAR_Y + TOP_BAR_H / 2,
            "樣本:4 台車 · 23 天 · 1,647 筆 · 一個小型車隊、一個月,"
            "以下所有比例僅在此樣本內成立",
            ha="center", va="center", fontsize=13, color="white",
            fontweight="bold", zorder=4)

    # ==============================================================
    # 二、雙欄對照表(分岔)
    # ==============================================================
    # 列標籤欄底
    ax.add_patch(Rectangle((XL, T_BOT), XLAB - XL, T_TOP - T_BOT,
                           fc=LABELBG, ec="none", zorder=2))

    # ---- 表頭 ----
    h_hd = 0.058
    y_hd = T_TOP - h_hd
    ax.add_patch(FancyBboxPatch(
        (XLAB, y_hd), (XAXIS - GAP) - XLAB, h_hd,
        boxstyle="round,pad=0,rounding_size=.010", fc=NAVY, ec=NAVY, zorder=3))
    ax.text(CL, y_hd + h_hd / 2, "ADAS · 行車輔助", ha="center", va="center",
            fontsize=14, color="white", fontweight="bold", zorder=4)
    ax.add_patch(FancyBboxPatch(
        (XAXIS + GAP, y_hd), XR - (XAXIS + GAP), h_hd,
        boxstyle="round,pad=0,rounding_size=.010", fc=GREEN, ec=GREEN, zorder=3))
    ax.text(CR, y_hd + h_hd / 2, "DMS · 駕駛監控", ha="center", va="center",
            fontsize=14, color="white", fontweight="bold", zorder=4)

    # ---- 三列資料列 ----
    rows = [
        ("量體", "1,029 筆", "618 筆", 0.062),
        ("誤報", "104 筆", "20 筆", 0.062),          # 不得加任何倍數比較標籤
        ("該樣本人工\n判定為正確", "89.9%", "96.8%", 0.090),
    ]
    y = y_hd
    for label, lv, rv, h in rows:
        y -= h
        ax.plot([XL, XR], [y, y], color=ROWLINE, lw=1.0, zorder=2)
        ax.text((XL + XLAB) / 2, y + h / 2, label, ha="center", va="center",
                fontsize=11, color=TXT, linespacing=1.5, zorder=4)
        vy = y + h / 2 if label != "該樣本人工\n判定為正確" else y + h * 0.70
        ax.text(CL, vy, lv, ha="center", va="center", fontsize=16,
                color=TXT, fontweight="bold", zorder=4)
        ax.text(CR, vy, rv, ha="center", va="center", fontsize=16,
                color=TXT, fontweight="bold", zorder=4)
        if label == "該樣本人工\n判定為正確":
            # 同一把尺的附註標籤:把兩個比例降級成「只能指出性質差異的觀察」
            ax.text(XR - 0.006, y + h * 0.24, "同一把尺 · 一致性未量測",
                    ha="right", va="center", fontsize=10, color=shade(GREY, -0.2),
                    bbox=dict(boxstyle="round,pad=0.30", fc=shade(GREY, 0.80),
                              ec=shade(GREY, 0.55), lw=0.8), zorder=5)

    # ---- 第 4 列:錯的是誰(列高加倍、加底色,表格的視覺高潮)----
    h4 = y - T_BOT
    ax.plot([XL, XR], [T_BOT, T_BOT], color=ROWLINE, lw=1.0, zorder=2)
    ax.add_patch(Rectangle((XLAB, T_BOT), XR - XLAB, h4,
                           fc=shade(GREY, 0.90), ec="none", zorder=2))
    ax.text((XL + XLAB) / 2, T_BOT + h4 / 2, "錯的是誰", ha="center", va="center",
            fontsize=11, color=TXT, fontweight="bold", zorder=4)

    bw, bh = 0.150, h4 - 0.038          # 上下各留內距,大字不壓列分隔線
    for cx, word, col in ((CL, "模型", NAVY), (CR, "人", GREEN)):
        ax.add_patch(FancyBboxPatch(
            (cx - bw / 2, T_BOT + 0.019), bw, bh,
            boxstyle="round,pad=0,rounding_size=.014", fc=col, ec=col, zorder=3))
        ax.text(cx, T_BOT + 0.019 + bh / 2, word, ha="center", va="center",
                fontsize=22, color="white", fontweight="bold", zorder=4)

    # ---- 中央分隔軸(不是格線:讓觀眾看到「兩件不同的事」)----
    ax.plot([XAXIS, XAXIS], [T_BOT - 0.004, T_TOP + 0.004],
            color=DARKGREY, lw=4.5, solid_capstyle="butt", zorder=5)

    # ---- in-text 引用標記(第 4 列右下角外側)----
    ax.text(XR, T_BOT - 0.014, "(Sambasivan et al., 2021)", ha="right", va="top",
            fontsize=10, color=shade(GREY, -0.1), zorder=4)

    # ---- 表格正下方引言(左側 4px 深灰色條)----
    yq = 0.443
    ax.add_patch(Rectangle((XL + 0.010, yq - 0.024), 0.0035, 0.048,
                           fc=DARKGREY, ec="none", zorder=4))
    ax.text(XL + 0.022, yq,
            "同一套複核流程在處理兩個本質不同的問題,所以兩邊都沒被解決。",
            ha="left", va="center", fontsize=13, color=TXT, style="italic", zorder=4)

    # ---- 引言下方兩個缺口小標籤,各自對齊欄位 ----
    yg = 0.400
    ax.text(CL, yg, "缺口 = 脈絡(判定依據不在畫面裡)", ha="center", va="center",
            fontsize=11, color=NAVY, fontweight="bold", zorder=4)
    ax.text(CR, yg, "缺口 = 判準(同一段影片,不同複核者給不同標籤)",
            ha="center", va="center", fontsize=11, color=shade(GREEN, -0.15),
            fontweight="bold", zorder=4)

    # ==============================================================
    # 三、根因匯流圖(匯流)—— 本頁最醒目的圖形
    # ==============================================================
    ax.add_patch(FancyBboxPatch(
        (XL, 0.008), XR - XL, 0.366,
        boxstyle="round,pad=0,rounding_size=.014",
        fc=BANDBG, ec=shade(GREY, 0.70), lw=1.0, zorder=1))

    ymid = 0.270

    # ---- 誤報 FP 方塊 ----
    fx, fw, fh = 0.035, 0.190, 0.098
    ax.add_patch(FancyBboxPatch(
        (fx, ymid - fh / 2), fw, fh,
        boxstyle="round,pad=0,rounding_size=.014", fc=ORANGE, ec=ORANGE, zorder=3))
    ax.text(fx + fw / 2, ymid, "誤報 FP ｜ 124 筆", ha="center", va="center",
            fontsize=15, color="white", fontweight="bold", zorder=4)
    ax.text(fx + fw / 2, ymid - fh / 2 - 0.016,
            "該樣本全部誤報\n(行車輔助 104 + 駕駛監控 20)",
            ha="center", va="top", fontsize=10, color=TXT, linespacing=1.5, zorder=4)

    # ---- 粗橘箭頭 + 根因比例標籤(分子分母必須同時顯示)----
    ax0, ax1 = fx + fw + 0.012, 0.428
    ax.add_patch(FancyArrowPatch(
        (ax0, ymid), (ax1, ymid), arrowstyle="-|>", mutation_scale=26,
        lw=5.0, color=ORANGE, shrinkA=0, shrinkB=0, zorder=4))
    ax.text((ax0 + ax1) / 2, ymid + 0.028, "103 / 124 = 83%", ha="center",
            va="bottom", fontsize=14, color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text((ax0 + ax1) / 2, ymid - 0.028, "公司自己的口徑", ha="center",
            va="top", fontsize=9, color=TXT, zorder=5)

    # ---- 匯流終點:根因方塊(全頁最大字級)----
    rx, rw, rh = 0.440, 0.258, 0.140
    ax.add_patch(FancyBboxPatch(
        (rx, ymid - rh / 2), rw, rh,
        boxstyle="round,pad=0,rounding_size=.014",
        fc=AMBER_PALE, ec="black", lw=2.5, zorder=3))
    ax.text(rx + rw / 2, ymid, "交通標誌辨識", ha="center", va="center",
            fontsize=24, color="black", fontweight="bold", zorder=4)

    # ---- 根因 → 既有資產 ----
    ax.add_patch(FancyArrowPatch(
        (rx + rw + 0.010, ymid), (0.762, ymid), arrowstyle="-|>",
        mutation_scale=22, lw=3.2, color=shade(GREEN, -0.1),
        shrinkA=0, shrinkB=0, zorder=4))
    gx, gw, gh = 0.772, 0.196, 0.108
    ax.add_patch(FancyBboxPatch(
        (gx, ymid - gh / 2), gw, gh,
        boxstyle="round,pad=0,rounding_size=.014", fc=GREEN, ec=GREEN, zorder=3))
    ax.text(gx + gw / 2, ymid, "速限資料:\n公司既有資產", ha="center", va="center",
            fontsize=14, color="white", fontweight="bold", linespacing=1.5, zorder=4)
    ax.text(gx + gw / 2, ymid - gh / 2 - 0.016,
            "不必外購、不必等新模型,\n這條今天就能動",
            ha="center", va="top", fontsize=10, color=TXT, linespacing=1.5, zorder=4)

    # ---- 匯流方塊正下方的結論 ----
    ax.text(0.492, 0.128,
            "誤報的第一大來源只有一個 → 成本論證有一個可工程化的靶心。",
            ha="center", va="center", fontsize=13, color=ORANGE_DARK,
            fontweight="bold", zorder=5)

    # ---- 左下角:漏放那一側 ----
    ax.text(XL + 0.016, 0.043,
            "漏放那一側只有一份很薄的獨立樣本,下一頁講。",
            ha="left", va="center", fontsize=11, color=shade(GREY, -0.4), zorder=5)

    # ---- 右下角:誤報率離散度的解讀限制 ----
    ax.text(XR - 0.012, 0.052,
            "該樣本四台車誤報率 2.5%-16.5%,差異主要反映各路線的路標環境,\n"
            "不應解讀為駕駛行為差異。",
            ha="right", va="center", fontsize=10, color=TXT, linespacing=1.6,
            bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=shade(GREY, 0.55),
                      lw=0.9), zorder=5)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_03")
