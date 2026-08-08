# -*- coding: utf-8 -*-
"""A3 v4 圖表產生器 —— **骨架**。

helper 段(save / newfig / box / panel + 色票 + 字型設定)照抄 v3 的
`Assessment3/figures/make_figs_v3.py`,已實證可用,不要重寫。

v4 = 10 頁內容,每頁一張圖 → fig_v4_01 ~ fig_v4_10,共 10 個佔位函式。
**每個佔位函式的內容都待 v2.1 定稿後才填,現在不得自行編造。**

紅線(沿用 v3):
- 不得出現任何未經標示來源的數值;提案人設定值一律在圖上標明。
- 圖內最小字級不得低於 FS_MIN(= 9),一般筆電要看得清楚 → 由 save() 強制檢查。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle
from matplotlib.text import Text
import numpy as np

# ------------------------------------------------------------------
# 字型:Microsoft JhengHei
# axes.unicode_minus = False 是 U+2212(負號)缺字的解方 —— 不要刪這行
# ------------------------------------------------------------------
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

# ------------------------------------------------------------------
# 輸出目錄:v4/figures(與 scripts/ 同層的姊妹目錄)
# ------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.dirname(HERE)
OUT = os.path.join(V4, "figures")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------
# 色票 —— 主迴圈裁決過的唯一色值。
# 不要沿用 v3 的 NAVY #1F3864 / ORANGE #E36C0A。
# ------------------------------------------------------------------
NAVY = "#1F4E79"
ORANGE = "#E8833A"
ORANGE_DARK = "#B45F1F"
ORANGE_LIGHT = "#F6C9A0"
RED = "#C00000"
GREY = "#808080"
LIGHT = "#D9D9D9"
AMBER = "#FFC000"
GREEN = "#548235"
BLUE = "#2E75B6"
PURPLE = "#7030A0"

PALETTE = {
    "NAVY": NAVY, "ORANGE": ORANGE, "ORANGE_DARK": ORANGE_DARK,
    "ORANGE_LIGHT": ORANGE_LIGHT, "RED": RED, "GREY": GREY, "LIGHT": LIGHT,
    "AMBER": AMBER, "GREEN": GREEN, "BLUE": BLUE, "PURPLE": PURPLE,
}

# 圖內最小字級。低於此值一般筆電看不清楚 → save() 直接 assert 擋下。
FS_MIN = 9.0


# ==================================================================
# helper 段(照抄 v3,已實證可用)
# ==================================================================
def assert_min_fontsize(fig, fs_min=FS_MIN):
    """掃描整張圖的所有文字物件,任何一個字級低於 fs_min 就 assert 失敗。

    涵蓋 ax.text / 軸標籤 / 刻度標籤 / 圖例,不必在每個 call site 自己檢查。
    """
    bad = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        size = t.get_fontsize()
        if size < fs_min:
            bad.append((round(size, 2), s.replace("\n", " / ")[:40]))
    assert not bad, (
        f"圖內字級低於 fs={fs_min} 共 {len(bad)} 處(一般筆電看不清楚):{bad[:8]}"
    )


def save(fig, name):
    """同時輸出 png + svg,300 dpi,bbox_inches='tight',白底。存檔前先驗字級。"""
    assert_min_fontsize(fig)
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", name)


def newfig(w=12.5, h=6.4, title=None):
    """開一張 0–1 座標的空白畫布,可帶標題。"""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    if title:
        ax.text(.5, .985, title, ha="center", va="top", fontsize=15.5,
                color=NAVY, fontweight="bold")
    return fig, ax


def box(ax, x, y, w, h, text, fc, fs=10, tc="white", ec=None, lw=1.5, bold=True, ls="-"):
    """圓角方塊 + 置中文字。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=.015",
                                fc=fc, ec=ec or fc, lw=lw, ls=ls, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal", zorder=4, linespacing=1.6)


def panel(ax, x, y, w, h, title, body, col, tfs=11, bfs=9, fc="#FAFAFA"):
    """有色標題列的面板(最常用)。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=.015",
                                fc=fc, ec=col, lw=1.6, zorder=3))
    ax.add_patch(FancyBboxPatch((x, y + h - .075), w, .075,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=col, ec=col, zorder=4))
    ax.text(x + w / 2, y + h - .0375, title, ha="center", va="center", fontsize=tfs,
            color="white", fontweight="bold", zorder=5)
    ax.text(x + w / 2, y + (h - .075) / 2, body, ha="center", va="center", fontsize=bfs,
            color="#333333", zorder=5, linespacing=1.85)


# ==================================================================
# 10 張圖的佔位函式(對應十頁內容)
# 命名最終為 fig_v4_XX_<slug>,slug 待 v2.1 定稿後補。
# 每個函式的圖形內容一律待 v2.1 定稿後填,現在不得自行編造。
# ==================================================================
def fig_v4_01():
    """P1 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_02():
    """P2 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_03():
    """P3 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_04():
    """P4 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_05():
    """P5 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_06():
    """P6 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_07():
    """P7 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_08():
    """P8 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_09():
    """P9 用圖。內容待 v2.1 定稿後填。"""
    return None


def fig_v4_10():
    """P10 用圖。內容待 v2.1 定稿後填。"""
    return None


FIGS = [fig_v4_01, fig_v4_02, fig_v4_03, fig_v4_04, fig_v4_05,
        fig_v4_06, fig_v4_07, fig_v4_08, fig_v4_09, fig_v4_10]


if __name__ == "__main__":
    print("產出 v4 圖表(輸出目錄:%s):" % OUT)
    made = 0
    for f in FIGS:
        if f() is not None:
            made += 1
    print("\n完成 %d / %d 張。" % (made, len(FIGS)))
    if made < len(FIGS):
        print("尚未填內容的圖不會輸出檔案。")

# ==================================================================
# ⚠️ 本檔目前只有 helper 段可用,10 個 fig_v4_* 皆為空殼。
#    圖形內容待 v2.1 定稿後填,填完再逐張出圖並目視稽核。
#
# v3 踩過、v4 出圖後必須逐項複查的坑(見 v4/notes/03_出圖與組版機具.md §三):
#   1. 文字重疊 / 被裁切 —— 出圖後必須匯出逐頁圖目視稽核,不能只看原始檔。
#   2. 圖內文字與軸重疊、對比框壓住資料標籤。
#   3. 配時表加總錯(犯過兩次)—— 逐列相加一律程式驗算,不得手算。
#   4. 主檔與講稿漂成兩份事實來源 —— 任何數字改動三邊對賬。
#   5. 圖內最小字級 >= FS_MIN(本檔已由 save() 強制)。
# ==================================================================
