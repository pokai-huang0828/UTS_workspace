# -*- coding: utf-8 -*-
"""P1 用圖:兩階段推論流程 + 單位成本帶。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P1 · 用例」→【視覺規格】。
圖只畫內容;頁首標題與右上角五格進度指示由組版程式負責,本圖不畫。
色值一律取自 make_figs_v4 的常數(NAVY #1F4E79 / ORANGE #E8833A ...),
不自行硬編色值(舊版橘/深藍已作廢)。圖內最小字級 9,存檔前由 save() 再驗一次。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    FancyArrowPatch, FancyBboxPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT, RED, GREY, LIGHT, GREEN,
    newfig, save, assert_min_fontsize, OUT,
)
from matplotlib.patches import Ellipse  # noqa: E402

FS_BIG = 30      # 成本帶大字
FS_MID = 26      # 「差約 13 倍」
FS_BLOCK = 15    # 流程方塊主字
FS_SUB = 13      # 流程方塊第二行(受方塊寬度所限,較主字小一級)
FS_ROW = 13      # 管理摘要行文 / 合計格
FS_T = 12
FS_S = 11
FS_N = 10        # 小字
FS_9 = 9         # 來源鏈 / 頁腳 / 序號(全圖下限,不得再低)

# 內文灰:沿用機具 panel() 的 body 色,不另立新色值
INK = "#333333"
INK2 = INK


# ------------------------------------------------------------------
# 量測輔助:精準排字,避免重疊
# ------------------------------------------------------------------
def _text_w(ax, s, fs, bold=False):
    """回傳字串在 0-1 座標下的寬度(x 方向)。"""
    r = ax.figure.canvas.get_renderer()
    t = ax.text(0, 0, s, fontsize=fs, fontweight="bold" if bold else "normal")
    bb = t.get_window_extent(renderer=r)
    t.remove()
    inv = ax.transData.inverted()
    return inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]


def _rich(ax, x, y, segs, fs, color):
    """由左而右接續排字,segs = [(文字, 是否粗體), ...]。"""
    cx = x
    for s, bold in segs:
        ax.text(cx, y, s, ha="left", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=6)
        cx += _text_w(ax, s, fs, bold)
    return cx


# ------------------------------------------------------------------
# 橘色視覺母題:人工防線方塊(P2 / P5 / P8 / P10 重用,
# 同一形狀同一色值,只換 scale:1.0 / 0.8 / 0.6 / 0.4 / 0.25)
# ------------------------------------------------------------------
def motif_block(ax, x, y, w, h, line1, line2, scale=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=ORANGE, ec=ORANGE_DARK, lw=3.0 * scale, zorder=4))
    ax.text(x + w / 2, y + h * .68, line1, ha="center", va="center",
            fontsize=FS_BLOCK * scale, color="white", fontweight="bold", zorder=5)
    ax.text(x + w / 2, y + h * .30, line2, ha="center", va="center",
            fontsize=FS_SUB * scale, color="white", fontweight="bold", zorder=5)


def stage_block(ax, x, y, w, h, line1, line2=""):
    """深藍的自動化階段方塊(方塊 A / B)。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=NAVY, ec=NAVY, lw=1.5, zorder=4))
    if line2:
        ax.text(x + w / 2, y + h * .68, line1, ha="center", va="center",
                fontsize=FS_BLOCK, color="white", fontweight="bold", zorder=5)
        ax.text(x + w / 2, y + h * .30, line2, ha="center", va="center",
                fontsize=FS_SUB, color="white", fontweight="bold", zorder=5)
    else:
        ax.text(x + w / 2, y + h / 2, line1, ha="center", va="center",
                fontsize=FS_BLOCK, color="white", fontweight="bold", zorder=5)


def build():
    fig, ax = newfig(12.5, 7.3)      # 橫幅;頁首標題與進度指示由組版程式放,圖不畫
    fig.canvas.draw()                 # 先備妥 renderer 供量測

    # ==============================================================
    # 上層:管理摘要框(細灰框 + 左側深藍色條)
    # ==============================================================
    sx, sy, sw, sh = .02, .826, .96, .169
    ax.add_patch(Rectangle((sx, sy), sw, sh, fc="white", ec=GREY, lw=1.0, zorder=2))
    ax.add_patch(Rectangle((sx, sy), .006, sh, fc=NAVY, ec=NAVY, lw=0, zorder=3))
    ax.text(sx + .016, .968, "管理摘要 / Executive Summary", ha="left", va="center",
            fontsize=FS_T, color=NAVY, fontweight="bold", zorder=5)

    rows = [
        (.926, [("要解什麼:人工複核在客戶要求的時效內做不完", False)]),
        (.890, [("期望收益:在複核量達現況四倍以上時,"
                 "仍維持同一個品質水準與客戶要的交付時效", False)]),
        (.854, [("如何衡量成功:", False), ("第 6 週", True),
                ("交出公司第一份含漏放的錯誤率;", False), ("第 24 週", True),
                ("交出對照重訓結果", False)]),
    ]
    for i, (ry, segs) in enumerate(rows):
        ax.add_patch(Ellipse((sx + .026, ry), .0136, .0233, fc=NAVY, ec=NAVY,
                             lw=0, zorder=4))
        ax.text(sx + .026, ry, "%d" % (i + 1), ha="center", va="center",
                fontsize=FS_9, color="white", fontweight="bold", zorder=5)
        _rich(ax, sx + .040, ry, segs, FS_ROW, INK)

    # ==============================================================
    # 左上角對比註記(流程主軸左上)
    #   —— 與管理摘要框之間留 3% 高度空白帶(.796 對 .826)
    # ==============================================================
    ax.add_patch(FancyBboxPatch((.02, .706), .370, .090,
                                boxstyle="round,pad=0,rounding_size=.010",
                                fc=LIGHT, ec=LIGHT, lw=1.0, alpha=.45, zorder=2))
    ax.text(.038, .774, "競爭者路線:把更強算力堆進車上", ha="left", va="center",
            fontsize=FS_N, color=INK2, zorder=5)
    ax.add_patch(Rectangle((.028, .717), .005, .026, fc=NAVY, ec=NAVY,
                           lw=0, zorder=5))
    ax.text(.038, .729, "我們的架構:輕量初判 + 雲端複判,成本移到下游",
            ha="left", va="center", fontsize=FS_N, color=NAVY,
            fontweight="bold", zorder=5)

    # ==============================================================
    # 中層:流程主軸(三個等寬圓角方塊 + 兩支箭頭)
    # ==============================================================
    by, bh, bw = .555, .135, .225
    xa, xb, xc = .025, .350, .750
    mid_y = by + bh / 2

    stage_block(ax, xa, by, bw, bh, "① 車上裝置", "即時初判")
    stage_block(ax, xb, by, bw, bh, "② 雲端 · 複判")
    motif_block(ax, xc, by, bw, bh, "③ 人工防線", "5 位專職分析人員 · 逐筆")

    # 箭頭 1:實心深藍 —— 自動化仍在線上
    ax.add_patch(FancyArrowPatch((xa + bw + .005, mid_y), (xb - .005, mid_y),
                                 arrowstyle="-|>", mutation_scale=22,
                                 lw=4, color=NAVY, zorder=3))
    ax.text((xa + bw + xb) / 2, .657, "初判結果上傳", ha="center", va="center",
            fontsize=FS_N, color=INK2, zorder=5)

    # 箭頭 2:橘色虛線 —— 自動化到此為止,剩下的全落在方塊 C
    ax.add_patch(FancyArrowPatch((xb + bw + .005, mid_y), (xc - .005, mid_y),
                                 arrowstyle="-|>", mutation_scale=20,
                                 lw=2.6, color=ORANGE, ls=(0, (6, 3)), zorder=3))
    ax.text((xb + bw + xc) / 2, .672, "複判後仍有誤報 /\n客戶回頭標記 5-10%",
            ha="center", va="center", fontsize=FS_N, color=ORANGE_DARK,
            fontweight="bold", linespacing=1.5, zorder=5)

    # 方塊下方小字
    ax.text(xa + bw / 2, .527, "輕量模型,即時初判", ha="center", va="center",
            fontsize=FS_N, color=INK2, zorder=5)
    ax.text(xb + bw / 2, .527, "判定屬實 → 回傳裝置向駕駛警示", ha="center",
            va="center", fontsize=FS_N, color=INK2, zorder=5)

    # 方塊 C 引線 + 小字框(尖峰徵調)
    ax.plot([xc + bw / 2, xc + bw / 2], [by, .543], color=GREY, lw=1.0, zorder=3)
    ax.add_patch(FancyBboxPatch((xc, .461), bw, .082,
                                boxstyle="round,pad=0,rounding_size=.010",
                                fc="white", ec=GREY, lw=1.0, zorder=4))
    ax.text(xc + bw / 2, .520, "尖峰時另徵調 7 位", ha="center", va="center",
            fontsize=FS_N, color=INK2, zorder=5)
    ax.text(xc + bw / 2, .488, "研發工程師離開本職", ha="center", va="center",
            fontsize=FS_N, color=INK2, zorder=5)

    # ==============================================================
    # 下層:成本帶(淺橘底,左 34% / 中 32% / 右 34%)
    # ==============================================================
    bx, byy, bwid, bhh = .02, .227, .96, .222
    ax.add_patch(Rectangle((bx, byy), bwid, bhh, fc=ORANGE_LIGHT, ec="none",
                           alpha=.38, zorder=1))
    d1 = bx + bwid * .34
    d2 = bx + bwid * .66
    for d in (d1, d2):
        ax.plot([d, d], [byy + .014, byy + bhh - .014], color="white", lw=1.6,
                zorder=2)

    lc = (bx + d1) / 2
    mc = (d1 + d2) / 2
    rc = (d2 + bx + bwid) / 2

    # 左格:例行批次複核 —— 全量
    ax.text(lc, .425, "例行批次複核", ha="center", va="center", fontsize=FS_T,
            color=NAVY, fontweight="bold", zorder=5)
    ax.text(lc, .391, "全量 · 每一筆都看", ha="center", va="center", fontsize=FS_S,
            color=INK, zorder=5)
    ax.text(lc, .333, "約 20 秒 / 筆", ha="center", va="center", fontsize=FS_BIG,
            color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text(lc, .277, "營運端的實務估計,尚未以計時量測驗證", ha="center", va="center",
            fontsize=FS_9, color=GREY, zorder=5)

    # 中格:兩條工作流的單價差
    ax.text(mc, .351, "差約 13 倍", ha="center", va="center", fontsize=FS_MID,
            color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text(mc, .293, "差在要不要離開畫面去找證據", ha="center", va="center",
            fontsize=FS_T, color=INK, zorder=5)

    # 右格:客戶爭議深入判讀
    ax.text(rc, .425, "客戶爭議深入判讀", ha="center", va="center", fontsize=FS_T,
            color=NAVY, fontweight="bold", zorder=5)
    ax.text(rc, .391, "客戶回頭標記的 5-10%", ha="center", va="center", fontsize=FS_S,
            color=INK, zorder=5)
    ax.text(rc, .333, "約 4.4 分鐘 / 筆", ha="center", va="center", fontsize=FS_BIG,
            color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text(rc, .289, "由一次實際判讀反推:5 人 × 3 天 × 8 小時 ÷ 1,647 筆\n"
                      "不含報告與回信",
            ha="center", va="top", fontsize=FS_9, color=GREY,
            linespacing=1.35, zorder=5)

    # 成本帶正下方的合計格
    ax.add_patch(Rectangle((bx, .159), bwid, .058, fc=ORANGE_DARK, ec=ORANGE_DARK,
                           lw=0, zorder=3))
    ax.text(bx + bwid / 2, .188,
            "合計 27.7-38.7 人時/天(單一大型車隊約 3,000 筆/天;"
            "現有產能 40 人時/天 = 5 人 × 8 小時)",
            ha="center", va="center", fontsize=FS_ROW, color="white",
            fontweight="bold", zorder=5)

    # ==============================================================
    # 來源鏈小字(成本帶右下角,四行,誠實揭露:誰負責 / 什麼時候 / 改變哪個決策)
    # ==============================================================
    src = [
        "4.4 分鐘的來源樣本:某小型車隊 · 單月 · 4 台車 · 23 天 · 1,647 筆",
        "20 秒為營運端估計值,尚未以計時量測驗證",
        "當責:複核營運主管 · 期限:第 6 週交出正式基準 · 決策:G1 驗收後才據以重估人力與時效目標",
        "(Sculley et al., 2015)",
    ]
    for i, s in enumerate(src):
        ax.text(.98, .135 - i * .026, s, ha="right", va="center",
                fontsize=FS_9, color=GREY, zorder=5)

    # ==============================================================
    # 顏色圖例小字(頁腳正上方單行)+ 頁腳
    # ==============================================================
    ly, lx = .030, .02
    ax.text(lx, ly, "本片顏色語意:", ha="left", va="center", fontsize=FS_N,
            color=INK2, zorder=5)
    lx += _text_w(ax, "本片顏色語意:", FS_N)
    for col, lab in ((ORANGE, "橘 = 人力成本"), (NAVY, "藍 = 已自動化"),
                     (RED, "紅 = 安全與否決"), (GREEN, "綠 = 已具備的資產")):
        ax.add_patch(Rectangle((lx, ly - .008), .009, .016, fc=col, ec=col,
                               lw=0, zorder=5))
        lx += .013
        ax.text(lx, ly, lab, ha="left", va="center", fontsize=FS_N,
                color=INK2, zorder=5)
        lx += _text_w(ax, lab, FS_N) + .014

    ax.text(.02, .002, "事件量與工時為單一車隊樣本,已抽象化處理;架構僅描述至概念層次。",
            ha="left", va="center", fontsize=FS_9, color=GREY, zorder=5)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_01")
    for ext in ("png", "svg"):
        p = os.path.join(OUT, "fig_v4_01.%s" % ext)
        print("%s  %d bytes" % (p, os.path.getsize(p)))
