# -*- coding: utf-8 -*-
"""P4 用圖:我們看不見的那一半。資料鏈路(做得到 / 沒有在做)+ 39 筆拆解 + 資料難度三格帶。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P4」節 → ## 視覺規格。
標題由組版程式放,本圖不畫;頁首進度指示同樣不畫。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    plt, np, FancyArrowPatch, FancyBboxPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT, RED, GREY, LIGHT, GREEN,
    newfig, box, save, assert_min_fontsize,
)
from matplotlib.path import Path  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402

DARK = "#333333"
BAND_BG = "#F2F2F2"      # 資料難度帶底色(規格指定的中性底)
HYP_BG = "#FFF7E0"       # 假說框底色(規格指定)
HYP_EC = "#E0C271"       # 假說框框線(規格指定)


def _rrect(ax, x, y, w, h, fc, ec, lw=1.2, ls="-", z=3, r=.014, hatch=None):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0,rounding_size=%s" % r,
                       fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
    if hatch:
        p.set_hatch(hatch)
    ax.add_patch(p)
    return p


def build():
    fig, ax = newfig(13.0, 7.3)

    # ==============================================================
    # 左上:資料鏈路圖(上層做得到 / 下層沒有在做)
    # ==============================================================
    ax.add_patch(Rectangle((.020, .968), .022, .016, fc=NAVY, ec=NAVY, zorder=4))
    ax.text(.050, .976, "做得到", ha="left", va="center", fontsize=11,
            color=NAVY, fontweight="bold")

    box(ax, .020, .818, .210, .140, "裝置記憶卡:\n整天分段影片", NAVY, fs=12)
    box(ax, .275, .818, .195, .140,
        "遠端調閱\n(約 10-15 分鐘/天,\n有流量成本)", NAVY, fs=12)
    ax.add_patch(FancyArrowPatch((.232, .888), (.272, .888),
                                 arrowstyle="-|>", mutation_scale=15,
                                 color=NAVY, lw=1.8, zorder=5))

    box(ax, .020, .706, .300, .075, "當月事件匯出檔 → 客戶自助下載", NAVY, fs=12)
    ax.plot([.125, .125], [.818, .783], color=NAVY, lw=1.8, zorder=2)

    ax.add_patch(Rectangle((.020, .672), .022, .016, fc=GREY, ec=GREY, zorder=4))
    ax.text(.050, .680, "沒有在做", ha="left", va="center", fontsize=11,
            color=GREY, fontweight="bold")

    _rrect(ax, .015, .482, .485, .173, "white", GREY, lw=1.4,
           ls=(0, (6, 3)), z=2)

    box(ax, .030, .537, .165, .085, "伺服器判為否決的\n事件流", GREY, fs=12)
    ax.add_patch(FancyArrowPatch((.197, .5795), (.313, .5795),
                                 arrowstyle="-|>", mutation_scale=15,
                                 color=GREY, lw=1.6,
                                 linestyle=(0, (6, 3)), zorder=4))
    _rrect(ax, .211, .5585, .090, .042, ORANGE, ORANGE, lw=1.0, z=6, r=.010)
    ax.text(.256, .5795, "無常設流程", ha="center", va="center", fontsize=11,
            color="white", fontweight="bold", zorder=7)

    _rrect(ax, .315, .537, .095, .085, "none", GREY, lw=1.4, z=4)
    ax.plot([.322, .403], [.544, .615], color=LIGHT, lw=1.4, zorder=5)
    ax.text(.3625, .524, "(無人回看)", ha="center", va="top", fontsize=11,
            color=GREY, fontweight="bold", zorder=5)

    ax.text(.422, .5795, "(Ensign\net al.,\n2018)", ha="left", va="center",
            fontsize=10, color=GREY, linespacing=1.5, zorder=5)

    ax.text(.232, .446, "有資料,沒有習慣", ha="center", va="center",
            fontsize=22, color=ORANGE, fontweight="bold")

    # ==============================================================
    # 成本不對稱小框(左右兩區之間、上區下端)
    # ==============================================================
    _rrect(ax, .372, .325, .215, .145, "white", "#595959", lw=1.0, z=3)
    ax.add_patch(Rectangle((.382, .336), .006, .062, fc=RED, ec=RED, zorder=5))
    ax.text(.390, .450, "誤報 = 花我們的人時", ha="left", va="center",
            fontsize=11, color=DARK, zorder=5)
    ax.text(.390, .420, "(可換算成錢)", ha="left", va="center",
            fontsize=11, color=DARK, zorder=5)
    ax.text(.394, .382, "漏放 = 駕駛沒收到那次警示", ha="left", va="center",
            fontsize=11, color=RED, fontweight="bold", zorder=5)
    ax.text(.394, .352, "(安全)", ha="left", va="center",
            fontsize=11, color=RED, fontweight="bold", zorder=5)

    # ==============================================================
    # 右上:39 筆測試拆解
    # ==============================================================
    ax.text(.555, .992, "唯一的漏放量測 · 39 筆人工觸發測試",
            ha="left", va="top", fontsize=11, color=NAVY, fontweight="bold")
    ax.text(.555, .958, "(獨立樣本,非 1,647 筆母體)",
            ha="left", va="top", fontsize=11, color=GREY)

    bx, bw, by, bh = .555, .430, .825, .080
    w17 = bw * 17 / 39.0
    w12 = bw * 12 / 39.0
    w10 = bw - w17 - w12
    ax.add_patch(Rectangle((bx, by), w17, bh, fc=GREEN, ec=GREEN, zorder=3))
    ax.add_patch(Rectangle((bx + w17, by), w12, bh, fc=RED, ec=RED, zorder=3))
    ax.add_patch(Rectangle((bx + w17 + w12, by), w10, bh, fc=LIGHT,
                           ec=GREY, lw=1.0, hatch="///", zorder=3))
    ax.text(bx + w17 / 2, by + bh / 2, "正確 17", ha="center", va="center",
            fontsize=12, color="white", fontweight="bold", zorder=5)
    ax.text(bx + w17 + w12 / 2, by + bh / 2, "漏偵 12", ha="center",
            va="center", fontsize=12, color="white", fontweight="bold", zorder=5)

    cx10 = bx + w17 + w12 + w10 / 2
    ax.plot([cx10, cx10], [.822, .806], color=GREY, lw=1.0, zorder=4)
    ax.text(.925, .798, "待客戶說明用途 10", ha="center", va="top",
            fontsize=12, color=DARK, fontweight="bold")
    ax.text(.925, .760, "約占四分之一,無法歸類", ha="center", va="top",
            fontsize=10, color=GREY)

    cx12 = bx + w17 + w12 / 2
    ax.plot([cx12, cx12], [.821, .750], color=RED, lw=1.3,
            linestyle=(0, (5, 3)), zorder=4)
    _rrect(ax, .555, .668, .290, .078, "white", RED, lw=1.2, z=3)
    ax.text(.700, .707, "報告上我們自己註明:12 是下限", ha="center",
            va="center", fontsize=12, color=RED, fontweight="bold", zorder=5)

    ax.text(.555, .652, "12 筆漏偵的組成", ha="left", va="center",
            fontsize=10, color=GREY)
    ax.add_patch(Rectangle((.555, .548), .145, .085, fc=ORANGE, ec=ORANGE,
                           zorder=3))
    ax.add_patch(Rectangle((.700, .548), .145, .085, fc=GREY, ec=GREY,
                           zorder=3))
    ax.text(.6275, .5905, "超速標誌\n低光/雨天 6", ha="center", va="center",
            fontsize=11, color="white", fontweight="bold", zorder=5,
            linespacing=1.4)
    ax.text(.7725, .5905, "其他 6", ha="center", va="center", fontsize=11,
            color="white", fontweight="bold", zorder=5)

    _rrect(ax, .636, .395, .359, .137, HYP_BG, HYP_EC, lw=1.2, z=3)
    ax.text(.8155, .501, "這是我目前手上最強的線索,不是結論。",
            ha="center", va="center", fontsize=11, color=ORANGE_DARK,
            fontweight="bold", zorder=5)
    ax.text(.8155, .462, "母體只有 12 筆 · 自註為下限 · 另有 10 筆無法歸類",
            ha="center", va="center", fontsize=11, color=DARK, zorder=5)
    ax.text(.8155, .425, "→ W1-6 做成帶信賴區間的估計,G1 判是否換靶心。",
            ha="center", va="center", fontsize=11, color=DARK, zorder=5)

    # ==============================================================
    # 跨側橘色曲線:低光/雨天 6 → 與誤報同源
    # ==============================================================
    verts = [(.630, .545),
             (.617, .455), (.614, .360), (.590, .300),
             (.540, .276), (.430, .272), (.318, .302)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.CURVE4]
    ax.add_patch(PathPatch(Path(verts, codes), fc="none", ec=ORANGE, lw=2.0,
                           zorder=6, capstyle="round"))
    ax.add_patch(FancyArrowPatch((.330, .3005), (.306, .3035),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color=ORANGE, lw=2.0, zorder=6))

    _rrect(ax, .040, .282, .262, .090, ORANGE, ORANGE, lw=1.2, z=4)
    ax.text(.171, .327, "與誤報第一大根因同源:\n交通標誌辨識", ha="center",
            va="center", fontsize=12, color="white", fontweight="bold",
            zorder=5, linespacing=1.5)

    # ==============================================================
    # 下區:資料難度三格帶
    # ==============================================================
    _rrect(ax, .010, .003, .985, .263, BAND_BG, BAND_BG, lw=0, z=1, r=.012)
    ax.text(.978, .020, "五項資料品質屬性:準確 · 完整 · 一致 · 及時 · 可解釋",
            ha="right", va="center", fontsize=9, color=GREY, zorder=5)

    cells = [
        (.020, .262, NAVY, 1.2,
         "收集難度 → 完整性 / 及時性",
         "裝置離線與鏡頭遮蔽時段無資料;\n事件分批上傳、頻率不一"),
        (.292, .262, NAVY, 1.2,
         "處理難度 → 準確性 / 一致性",
         "感測器故障;\n人工標註的無意與有意錯誤;\n跨系統重複記錄"),
        (.564, .420, ORANGE_DARK, 1.5,
         "處理後的理解程度 → 可解釋性",
         "目前不一致。同一段影片,不同複核者會給不同標籤(低頭 vs 閉眼、\n"
         "香腸 vs 香菸、保溫瓶 vs 手機),而這個不一致從來沒有被量測過。\n"
         "也就是說,我們處理完的資料,連內部都還沒有一致的理解。\n"
         "這正是標註品質那一包要交的東西。"),
    ]
    for cx, cw, col, clw, ctitle, cbody in cells:
        _rrect(ax, cx, .038, cw, .218, "white", col, lw=clw, z=2)
        ax.add_patch(Rectangle((cx + .013, .227), .014, .014, fc=col, ec=col,
                               zorder=4))
        ax.text(cx + .034, .234, ctitle, ha="left", va="center", fontsize=12,
                color=col, fontweight="bold", zorder=4)
        ax.text(cx + .013, .199, cbody, ha="left", va="top", fontsize=10,
                color=DARK, linespacing=1.62, zorder=4)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_04")
