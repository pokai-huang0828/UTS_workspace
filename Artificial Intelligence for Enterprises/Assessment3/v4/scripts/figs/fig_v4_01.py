# -*- coding: utf-8 -*-
"""P1 用圖:立案定位 + 兩階段推論流程 + 單位成本帶(含 AI 能力定義)。

規格來源:v4/notes/_v2_parts/P01-04.md 的「# P1 · 用例」→【視覺規格】(v2.2,方案升級後)。
圖只畫內容;頁首標題與右上角五格進度指示由組版程式負責,本圖不畫。
色值一律取自 make_figs_v4 的常數(NAVY #1F4E79 / ORANGE #E8833A ...),不自行硬編色值。

🔴 裁決 O:畫布鎖 newfig(12.2, 5.7);圖內最小字級 9;塞不下砍內容,不放大畫布。
   save() 已設 pad_inches=0 —— 本檔不做任何尺寸補償。
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
from matplotlib.text import Text  # noqa: E402

FIG_W, FIG_H = 12.2, 5.7          # 🔴 裁決 O:鎖死,不得放大

FS_BIG = 30      # 成本帶大字
FS_MID = 26      # 「差約 16 倍」
FS_BLOCK = 15    # 流程方塊主字
FS_SUB = 12      # 流程方塊第二行(受方塊高度所限,較主字小)
FS_ROW = 13      # 管理摘要行文 / 合計格
FS_T = 12
FS_S = 11
FS_N = 10        # 小字
FS_9 = 9         # 來源鏈 / 頁腳 / 序號(全圖下限,不得再低)

# 內文灰:沿用機具 panel() 的 body 色,不另立新色值
INK = "#333333"
INK2 = INK

# 圓的長寬比補償(0-1 座標下,w/h = H_inch / W_inch 才是正圓)
ASPECT = FIG_H / FIG_W


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


def _rich(ax, x, y, segs, fs, color, bold_color=None):
    """由左而右接續排字,segs = [(文字, 是否粗體), ...]。"""
    cx = x
    for s, bold in segs:
        ax.text(cx, y, s, ha="left", va="center", fontsize=fs,
                color=(bold_color or color) if bold else color,
                fontweight="bold" if bold else "normal", zorder=6)
        cx += _text_w(ax, s, fs, bold)
    return cx


# ------------------------------------------------------------------
# 重疊稽核:把全圖文字的 display bbox 兩兩相交檢查一次
# ------------------------------------------------------------------
def check_overlap(fig, tol=1.0, whitelist=()):
    """回傳重疊清單 [(文字A, 文字B, 交集寬, 交集高)]。tol = 容許的像素交疊。"""
    r = fig.canvas.get_renderer()
    items = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        bb = t.get_window_extent(renderer=r)
        items.append((s.replace("\n", " / "), bb))
    bad = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            (sa, ba), (sb, bbx) = items[i], items[j]
            ow = min(ba.x1, bbx.x1) - max(ba.x0, bbx.x0)
            oh = min(ba.y1, bbx.y1) - max(ba.y0, bbx.y0)
            if ow > tol and oh > tol:
                if (sa[:12], sb[:12]) in whitelist or (sb[:12], sa[:12]) in whitelist:
                    continue
                bad.append((sa[:34], sb[:34], round(ow, 1), round(oh, 1)))
    return bad


def check_inside(fig, margin=0.0):
    """檢查是否有文字超出畫布(裁切)。"""
    r = fig.canvas.get_renderer()
    W, H = fig.get_size_inches() * fig.dpi
    out = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        bb = t.get_window_extent(renderer=r)
        if bb.x0 < -margin or bb.y0 < -margin or bb.x1 > W + margin or bb.y1 > H + margin:
            out.append((s.replace("\n", " / ")[:34],
                        round(bb.x0, 1), round(bb.y0, 1),
                        round(bb.x1, 1), round(bb.y1, 1)))
    return out


# ------------------------------------------------------------------
# 橘色視覺母題:人工防線方塊(P2 / P5 / P8 / P10 重用,
# 同一形狀同一色值,只換 scale:1.0 / 0.8 / 0.6 / 0.4 / 0.25)
# ------------------------------------------------------------------
def motif_block(ax, x, y, w, h, line1, line2, scale=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=ORANGE, ec=ORANGE_DARK, lw=3.0 * scale, zorder=4))
    ax.text(x + w / 2, y + h * .70, line1, ha="center", va="center",
            fontsize=FS_BLOCK * scale, color="white", fontweight="bold", zorder=5)
    ax.text(x + w / 2, y + h * .28, line2, ha="center", va="center",
            fontsize=FS_SUB * scale, color="white", fontweight="bold", zorder=5)


def stage_block(ax, x, y, w, h, line1, line2=""):
    """深藍的自動化階段方塊(方塊 A / B)。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=NAVY, ec=NAVY, lw=1.5, zorder=4))
    if line2:
        ax.text(x + w / 2, y + h * .70, line1, ha="center", va="center",
                fontsize=FS_BLOCK, color="white", fontweight="bold", zorder=5)
        ax.text(x + w / 2, y + h * .28, line2, ha="center", va="center",
                fontsize=FS_SUB, color="white", fontweight="bold", zorder=5)
    else:
        ax.text(x + w / 2, y + h / 2, line1, ha="center", va="center",
                fontsize=FS_BLOCK, color="white", fontweight="bold", zorder=5)


def build():
    fig, ax = newfig(FIG_W, FIG_H)   # 🔴 裁決 O 鎖死;標題與進度指示由組版程式放
    # axes 撐滿整張畫布 + 白底 Rectangle 把 tight 裁切框釘死 → 輸出即 12.2 x 5.7。
    # 🚫 不做任何 0.1 吋內縮補償(save() 已 pad_inches=0,補償會反過來吃掉 0.2 吋)。
    ax.set_position([0, 0, 1, 1])
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="none", zorder=0))
    fig.canvas.draw()                # 先備妥 renderer 供量測

    # ==============================================================
    # 上層:管理摘要框(細灰框 + 左側深藍色條)
    #   本輪新增第一列【立案定位條】—— 三秒內看出「這是送審,不是發想」
    # ==============================================================
    sx, sy, sw, sh = .02, .778, .96, .222
    ax.add_patch(Rectangle((sx, sy), sw, sh, fc="white", ec=GREY, lw=1.0, zorder=2))
    ax.add_patch(Rectangle((sx, sy), .005, sh, fc=NAVY, ec=NAVY, lw=0, zorder=3))
    ax.text(sx + .016, .972, "管理摘要 / Executive Summary", ha="left", va="center",
            fontsize=FS_T, color=NAVY, fontweight="bold", zorder=5)

    # 【立案定位條】(16 號檔 §三③;不可省,不得寫成仍在提議階段的措辭)
    _rich(ax, sx + .016, .930, [
        ("地端 AI 的技術可行性已由內部研討評估過(提案人為成員之一) —— 本簡報是把它變成", False),
        ("有業務數字、有驗證機制、有停止條件的正式立案。", True),
    ], FS_S, INK, bold_color=NAVY)

    rows = [
        (.884, [("要解什麼:人工複核在客戶要求的時效內做不完", False)]),
        (.840, [("期望收益:在複核量達現況四倍以上時,"
                 "仍維持同一個品質水準與客戶要的交付時效", False)]),
        (.798, [("如何衡量成功:", False), ("第 6 週", True),
                ("交出公司第一份含漏放的錯誤率;", False), ("第 24 週", True),
                ("交出對照重訓結果", False)]),
    ]
    for i, (ry, segs) in enumerate(rows):
        ax.add_patch(Ellipse((sx + .026, ry), .030 * ASPECT, .030, fc=NAVY, ec=NAVY,
                             lw=0, zorder=4))
        ax.text(sx + .026, ry, "%d" % (i + 1), ha="center", va="center",
                fontsize=FS_9, color="white", fontweight="bold", zorder=5)
        _rich(ax, sx + .040, ry, segs, FS_ROW, INK)

    # ==============================================================
    # 左上角對比註記(流程主軸左上)
    #   —— 與管理摘要框之間留 3% 高度空白帶(.748 對 .778)
    # ==============================================================
    cmp1 = "競爭者路線:把更強算力堆進車上"
    cmp2 = "我們的架構:輕量初判 + 雲端複判,成本移到下游"
    cmp_w = max(_text_w(ax, cmp1, FS_N), _text_w(ax, cmp2, FS_N, bold=True)) + .036
    ax.add_patch(FancyBboxPatch((.02, .658), cmp_w, .090,
                                boxstyle="round,pad=0,rounding_size=.010",
                                fc=LIGHT, ec=LIGHT, lw=1.0, alpha=.45, zorder=2))
    ax.text(.038, .726, cmp1, ha="left", va="center",
            fontsize=FS_N, color=INK2, zorder=5)
    ax.add_patch(Rectangle((.028, .672), .004, .026, fc=NAVY, ec=NAVY,
                           lw=0, zorder=5))
    ax.text(.038, .684, cmp2,
            ha="left", va="center", fontsize=FS_N, color=NAVY,
            fontweight="bold", zorder=5)

    # ==============================================================
    # 中層:流程主軸(三個等寬圓角方塊 + 兩支箭頭)
    # ==============================================================
    by, bh, bw = .495, .115, .225
    xa, xb, xc = .025, .350, .750
    mid_y = by + bh / 2

    stage_block(ax, xa, by, bw, bh, "① 車上裝置", "即時初判")
    stage_block(ax, xb, by, bw, bh, "② 雲端 · 複判")
    motif_block(ax, xc, by, bw, bh, "③ 人工防線", "5 位專職分析人員 · 逐筆")

    # 箭頭 1:實心深藍 —— 自動化仍在線上
    ax.add_patch(FancyArrowPatch((xa + bw + .005, mid_y), (xb - .005, mid_y),
                                 arrowstyle="-|>", mutation_scale=20,
                                 lw=3.6, color=NAVY, zorder=3))
    ax.text((xa + bw + xb) / 2, .590, "初判結果上傳", ha="center", va="center",
            fontsize=FS_N, color=INK2, zorder=5)

    # 箭頭 2:橘色虛線 —— 自動化到此為止,剩下的全落在方塊 C
    ax.add_patch(FancyArrowPatch((xb + bw + .005, mid_y), (xc - .005, mid_y),
                                 arrowstyle="-|>", mutation_scale=18,
                                 lw=2.4, color=ORANGE, ls=(0, (6, 3)), zorder=3))
    ax.text((xb + bw + xc) / 2, .606, "複判後仍有誤報 /\n客戶回頭標記 5-10%",
            ha="center", va="center", fontsize=FS_N, color=ORANGE_DARK,
            fontweight="bold", linespacing=1.45, zorder=5)

    # 方塊下方小字(三格同一水平線)
    ax.text(xa + bw / 2, .462, "輕量模型,即時初判", ha="center", va="center",
            fontsize=FS_N, color=INK2, zorder=5)
    ax.text(xb + bw / 2, .462, "判定屬實 → 回傳裝置向駕駛警示", ha="center",
            va="center", fontsize=FS_N, color=INK2, zorder=5)
    ax.text(xc + bw / 2, .462, "尖峰時另徵調 7 位研發工程師離開本職", ha="center",
            va="center", fontsize=FS_N, color=INK2, zorder=5)

    # ==============================================================
    # 下層:成本帶(淺橘底,左 30% / 中 40% / 右 30%)
    #   中格加寬,是為了容納本輪新增的【AI 能力定義】—— 成因與解法印在同一格
    # ==============================================================
    bx, byy, bwid, bhh = .02, .175, .96, .255
    ax.add_patch(Rectangle((bx, byy), bwid, bhh, fc=ORANGE_LIGHT, ec="none",
                           alpha=.38, zorder=1))
    d1 = bx + bwid * .30
    d2 = bx + bwid * .70
    for d in (d1, d2):
        ax.plot([d, d], [byy + .012, byy + bhh - .012], color="white", lw=1.6,
                zorder=2)

    lc = (bx + d1) / 2
    mc = (d1 + d2) / 2
    rc = (d2 + bx + bwid) / 2

    # 左格:例行批次複核 —— 全量
    ax.text(lc, .408, "例行批次複核", ha="center", va="center", fontsize=FS_T,
            color=NAVY, fontweight="bold", zorder=5)
    ax.text(lc, .370, "全量 —— 每一筆都看", ha="center", va="center", fontsize=FS_S,
            color=INK, zorder=5)
    ax.text(lc, .300, "約 20 秒 / 筆", ha="center", va="center", fontsize=FS_BIG,
            color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text(lc, .222, "營運端的實務估計,尚未以計時量測驗證", ha="center", va="center",
            fontsize=FS_9, color=GREY, zorder=5)

    # 中格:兩條工作流的單價差 + 🔴 本案要建的 AI 能力(全片唯一視覺落點)
    ax.text(mc, .386, "差約 16 倍", ha="center", va="center", fontsize=FS_MID,
            color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text(mc, .322, "差在要不要離開畫面去找證據", ha="center", va="center",
            fontsize=FS_S, color=INK, zorder=5)
    ax.text(mc, .272, "本案要建的 AI 能力:讓機器讀懂一次事件的完整脈絡",
            ha="center", va="center", fontsize=FS_S, color=NAVY,
            fontweight="bold", zorder=5)
    ax.text(mc, .234, "(影片 + 客戶問題 + 規則),並產出可交付的證據與描述",
            ha="center", va="center", fontsize=FS_S, color=NAVY,
            fontweight="bold", zorder=5)

    # 右格:客戶爭議深入判讀
    ax.text(rc, .408, "客戶爭議深入判讀", ha="center", va="center", fontsize=FS_T,
            color=NAVY, fontweight="bold", zorder=5)
    ax.text(rc, .370, "客戶回頭標記的 5-10%", ha="center", va="center", fontsize=FS_S,
            color=INK, zorder=5)
    ax.text(rc, .300, "約 5.25 分鐘 / 筆", ha="center", va="center", fontsize=FS_BIG,
            color=ORANGE_DARK, fontweight="bold", zorder=5)
    ax.text(rc, .230, "由一次實際判讀反推:5 人 × 3.6 天 × 8 小時 ÷ 1,647 筆",
            ha="center", va="center", fontsize=FS_9, color=GREY, zorder=5)
    ax.text(rc, .203, "不含整理與回信", ha="center", va="center",
            fontsize=FS_9, color=GREY, zorder=5)

    # ==============================================================
    # 成本帶正下方的合計格 + 右端「上緣已超過現有產能」橘色徽章
    # ==============================================================
    gy, gh = .118, .058
    ax.add_patch(Rectangle((bx, gy), bwid, gh, fc=ORANGE_DARK, ec=ORANGE_DARK,
                           lw=0, zorder=3))

    badge = "上緣已超過現有產能"
    bw_txt = _text_w(ax, badge, FS_S, bold=True)
    bpad = .010
    b_x1 = bx + bwid - .012
    b_x0 = b_x1 - bw_txt - bpad * 2
    ax.add_patch(FancyBboxPatch((b_x0, gy + .009), b_x1 - b_x0, gh - .018,
                                boxstyle="round,pad=0,rounding_size=.008",
                                fc=ORANGE, ec="white", lw=1.2, zorder=4))
    ax.text((b_x0 + b_x1) / 2, gy + gh / 2, badge, ha="center", va="center",
            fontsize=FS_S, color="white", fontweight="bold", zorder=5)

    ax.text((bx + b_x0) / 2, gy + gh / 2,
            "合計 29.8-42.9 人時/天(單一大型車隊約 3,000 筆/天;"
            "現有產能 40 人時/天 = 5 人 × 8 小時)",
            ha="center", va="center", fontsize=FS_ROW, color="white",
            fontweight="bold", zorder=5)

    # ==============================================================
    # 來源鏈小字(合計格下方,兩行;裁決 N 的載體:
    #   誠實揭露必須同時帶「誰負責 / 什麼時候 / 會改變哪個決策」,缺一不可)
    # ==============================================================
    ax.text(.98, .096,
            "5.25 分鐘的來源樣本:某小型車隊 · 單月 · 4 台車 · 23 天 · 1,647 筆"
            "(5 人 × 3.6 個工作日) · 20 秒為營運端估計值,尚未以計時量測驗證",
            ha="right", va="center", fontsize=FS_9, color=GREY, zorder=5)
    ax.text(.98, .066,
            "當責:複核營運主管 · 期限:第 6 週交出正式基準 · "
            "決策:G1 驗收後才據以重估人力與時效目標 · (Sculley et al., 2015)",
            ha="right", va="center", fontsize=FS_9, color=GREY, zorder=5)

    # ==============================================================
    # 顏色圖例小字(左)+ 頁腳(右),同一行
    # ==============================================================
    ly, lx = .026, .02
    ax.text(lx, ly, "本片顏色語意:", ha="left", va="center", fontsize=FS_N,
            color=INK2, zorder=5)
    lx += _text_w(ax, "本片顏色語意:", FS_N)
    for col, lab in ((ORANGE, "橘 = 人力成本"), (NAVY, "藍 = 已自動化"),
                     (RED, "紅 = 安全與否決"), (GREEN, "綠 = 已具備的資產")):
        ax.add_patch(Rectangle((lx, ly - .011), .0085, .022, fc=col, ec=col,
                               lw=0, zorder=5))
        lx += .013
        ax.text(lx, ly, lab, ha="left", va="center", fontsize=FS_N,
                color=INK2, zorder=5)
        lx += _text_w(ax, lab, FS_N) + .014

    ax.text(.98, ly, "事件量與工時為單一車隊樣本,已抽象化處理;架構僅描述至概念層次。",
            ha="right", va="center", fontsize=FS_9, color=GREY, zorder=5)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    f = build()
    f.canvas.draw()
    ov = check_overlap(f)
    oob = check_inside(f)
    print("重疊檢查:%s" % ("PASS(0 處)" if not ov else "FAIL %d 處" % len(ov)))
    for a, b, w, h in ov:
        print("   x  [%s] <-> [%s]  交疊 %.1f x %.1f px" % (a, b, w, h))
    print("越界檢查:%s" % ("PASS(0 處)" if not oob else "FAIL %d 處 %s" % (len(oob), oob)))
    print("最小字級:%.1f pt" % min(
        t.get_fontsize() for t in f.findobj(Text) if t.get_text().strip()))
    print("畫布:%.2f x %.2f in" % tuple(f.get_size_inches()))
    save(f, "fig_v4_01")
    for ext in ("png", "svg"):
        p = os.path.join(OUT, "fig_v4_01.%s" % ext)
        print("%s  %d bytes" % (p, os.path.getsize(p)))
