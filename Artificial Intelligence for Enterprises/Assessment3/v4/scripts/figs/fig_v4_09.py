# -*- coding: utf-8 -*-
"""P9 用圖:六個月 · 六個工作包 · 三道決策門(甘特圖 + 三道決策門)。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P9 · 六個月 · 六個工作包 · 三道決策門」→ ## 視覺規格。
共用機具:scripts/make_figs_v4.py(字型 / 色票 / save / newfig / assert_min_fontsize),只 import 不修改。

紅線:
- 色值只用 make_figs_v4 的常數(ORANGE / NAVY / BLUE / RED / GREY / LIGHT),本檔不寫死任何色碼,
  因此不可能混入 v3 已作廢的舊橘、舊深藍。
- 圖內最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形破折號 / U+2212。
- 圖不畫投影片標題、不畫右上角五格進度指示(兩者由組版程式負責)。
- 所有換行都用 renderer 實測字串寬度,避免文字溢出框外或互相重疊。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    NAVY, BLUE, ORANGE, GREY, LIGHT, RED,
    assert_min_fontsize, save, newfig,
)
from matplotlib.patches import (  # noqa: E402
    FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle,
)

# ------------------------------------------------------------------
# 畫布(16:9 取向)
# ------------------------------------------------------------------
FIG_W, FIG_H = 15.0, 8.4
H_PT = FIG_H * 72.0

# 三欄:左欄工作包標籤 / 中欄時間軸 / 右欄「今天 → 第 26 週」對照
ARROW_X, WORD_X = 0.006, 0.028   # 左側順序箭頭
LX0, LX1 = 0.050, 0.250          # 左欄文字
MX0, MX1 = 0.262, 0.772          # 中欄(W0 ~ W26)
DIVX = 0.780                     # 中/右欄分隔線
RX0, RX1 = 0.788, 0.999          # 右欄

WK = (MX1 - MX0) / 26.0

BAND_TOP, BAND_BOT = 0.840, 0.335
ROW_H = (BAND_TOP - BAND_BOT) / 6.0
BAR_H = ROW_H * 0.55
RC = [BAND_TOP - ROW_H * (i + 0.5) for i in range(6)]   # A..F 列心

GATE_Y = 0.862                   # 決策門菱形所在列
CARD_TOP = 0.292                 # 決策門說明卡上緣


def xw(week):
    return MX0 + week * WK


# ------------------------------------------------------------------
# 文字量測與換行(以 renderer 實測,單位一律「圖寬比例」)
# ------------------------------------------------------------------
# 引用標記整組不折行,避免出現「(Press,」/「2016)」這種斷法
_TOK = re.compile(r"\([A-Za-z][^)]*\)|[A-Za-z0-9][A-Za-z0-9\.\-_/%]*|.", re.S)
_NOBREAK = "、。,;:)」』】,.;:)!?%"
_REND = [None]
_AX = [None]                      # 量測基準:座標軸(= 版面 0-1 座標)


def _bind(fig, ax):
    """把畫布攤滿整張圖,讓 0-1 座標 = 圖面比例;並備妥 renderer。"""
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.canvas.draw()
    _REND[0] = fig.canvas.get_renderer()
    _AX[0] = ax


def tw(fig, s, fs, weight="normal"):
    """字串寬度,單位 = 版面 0-1 座標的 x 比例。"""
    if not s:
        return 0.0
    t = fig.text(0, 0, s, fontsize=fs, fontweight=weight)
    w = t.get_window_extent(renderer=_REND[0]).width / _AX[0].bbox.width
    t.remove()
    return w


def wrap(fig, s, max_w, fs, weight="normal"):
    """把字串折成每行寬度不超過 max_w 的多行 list;字串內的 \\n 為強制斷行。"""
    if "\n" in s:
        out = []
        for part in s.split("\n"):
            out += wrap(fig, part, max_w, fs, weight)
        return out
    lines, cur = [], ""
    for tok in _TOK.findall(s):
        if not cur and tok == " ":
            continue
        if cur and tok != " " and tok[0] not in _NOBREAK and \
                tw(fig, cur + tok, fs, weight) > max_w:
            lines.append(cur.rstrip())
            cur = tok
        else:
            cur += tok
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def ph(fs, lp=1.38):
    """單行行高,單位 = 版面 0-1 座標的 y 比例。"""
    return fs / H_PT * lp


BG = dict(boxstyle="square,pad=0.10", fc="white", ec="none")   # 讓格線/虛線不穿字


def put(ax, x, y_top, lines, fs, color, ha="left", lp=1.38, weight="normal",
        zorder=6, bg=False):
    """自 y_top 往下逐行寫字,回傳寫完後的 y。"""
    p = ph(fs, lp)
    y = y_top - p / 2.0
    for ln in lines:
        ax.text(x, y, ln, ha=ha, va="center", fontsize=fs, color=color,
                fontweight=weight, zorder=zorder,
                bbox=dict(BG) if bg else None)
        y -= p
    return y + p / 2.0


def diamond(ax, x, y, half_h, fc, ec, lw=1.5, zorder=7):
    hw = half_h * (FIG_H / FIG_W)
    ax.add_patch(Polygon([(x, y + half_h), (x + hw, y), (x, y - half_h),
                          (x - hw, y)], closed=True, fc=fc, ec=ec, lw=lw,
                         zorder=zorder))


# ------------------------------------------------------------------
# 內容(全部取自 P9 視覺規格,未新增任何數值)
# ------------------------------------------------------------------
WPS = [
    ("WP-A 評估底座", "分層抽樣 + 冷凍 hold-out + 首份含漏放的錯誤率 (Press, 2016)", 1, 6, NAVY),
    ("WP-B 標註品質", "誤報的操作型定義 + 判準明文化\n黃金題 + 複核者一致性係數 (Press, 2016)", 3, 10, NAVY),
    ("WP-C 脈絡特徵工程", "定位與地圖速限特徵化,規則式為基線", 5, 12, NAVY),
    ("WP-D 爭議回覆自動化", "", 8, 16, BLUE),
    ("WP-E 對照重訓", "", 8, 24, ORANGE),
    ("WP-F 治理與移交", "", 20, 26, ORANGE),
]

GATES = [
    ("G1", 6, "G1 · W6 因果判定門",
     "交出爭議處理的時間拆解(等待 / 找證據 / 判讀 / 內部覆核 / 回信)、兩天逾時率與尖峰到件分布。"
     "只有當「證據搜尋、誤報量與證據包製作」佔主要延遲,才續行後段;"
     "否則本案轉為排班與尖峰人力池方案。評估底座未產出,剩餘工作全數不續行。",
     "待確認:時間拆解與兩天逾時率目前無現成數字,這正是 W1-6 要交的東西。"),
    ("G2", 12, "G2 · W12 三方比較門",
     "在同一凍結評估集上同時比三組:①現行影像模型 ②規則式脈絡基線 ③脈絡增強的學習模型。"
     "成功條件:誤報改善達預註冊門檻,且漏放率信賴區間不惡化。"
     "本門只能調整模型的假設與規模,不能取消實驗。"
     "規則式若已解掉大部分誤報,靶心改為殘餘(情境模糊與判準爭議);"
     "若無效,先查脈絡資料本身的品質,再決定模型端的規模。", ""),
    ("G3", 24, "G3 · W24 部署決定門",
     "對照重訓證不出增量,模型端不部署,只留前四包的成果。", ""),
]

# 里程碑 =(列索引, 週次, 交付名);引用標記接在字串右端
MILESTONES = [
    (0, 6, "M1 W6 · 首份含漏放的錯誤率 + 時間拆解", ""),
    (1, 10, "M2 W10 · 判準手冊 + 一致性儀表板", "(Northcutt et al., 2021)"),
    (2, 12, "M3 W12 · 規則式脈絡層 + 誤報下降量測", "(Rudin, 2019)"),
    (3, 16, "M4 W16 · 自動證據包 + 回覆時效改善", ""),
    (4, 24, "M5 W24 · 對照重訓結果", ""),
    (5, 26, "M6 W26 · 移交文件 + 常態儀表板", ""),
]

DELIV_A = ("交付:可稽核的錯誤率(含信賴區間)+ 冷凍評估集 + 兩條工作流的單位工時正式基準 "
           "+ 時間拆解(等待 / 找證據 / 判讀 / 內部覆核 / 回信)+ 兩天逾時率 + 尖峰到件分布")

DELIV_E = ["WP-E 交付:三方對照結果(現行影像模型 / 規則式脈絡基線 / 脈絡增強的學習模型)"
           "+ 有脈絡 vs 無脈絡的對照結果",
           "總投入 4.50 人月不變,係 WP-E 內部人力前移,不增加總人月"]

RIGHT_CELLS = [
    ("① 判讀依據", "人去外面找", "事件送到人手上時已附證據"),
    ("② 複核判準", "口耳相傳", "明文手冊 + 一致性儀表板"),
    ("③ 漏放", "沒有數字", "有數字、有信賴區間、每月更新"),
    ("④ 交付時效", "現況單件爭議 2-5 天", "提案目標 2 天內;單純案件當天"),
]


# ==================================================================
def build():
    fig, ax = newfig(FIG_W, FIG_H)          # 不下標題:標題由組版程式放
    _bind(fig, ax)

    # ---------------- 中欄:格線 / 軸線 / 週刻度 ----------------
    for w in range(2, 27, 2):
        ax.plot([xw(w)] * 2, [BAND_BOT, BAND_TOP], color=LIGHT, lw=0.7,
                alpha=0.9, zorder=0.5)
    ax.plot([xw(0), xw(26)], [BAND_BOT] * 2, color=GREY, lw=0.9, zorder=1)
    for w in range(2, 27, 2):
        if w in (6, 12, 24):                # 這三週改由決策門標示,避免與虛線疊字
            continue
        ax.text(xw(w), BAND_BOT - 0.021, "W%d" % w, ha="center", va="center",
                fontsize=9, color=GREY, zorder=2)

    # ---------------- 左欄:順序箭頭 ----------------
    ax.add_patch(FancyArrowPatch((ARROW_X, RC[0] + 0.026), (ARROW_X, RC[4] - 0.028),
                                 arrowstyle="-|>", mutation_scale=13, color=GREY,
                                 lw=1.3, zorder=3))
    for idx, word in ((0, "評估集"), (1, "標註"), (2, "特徵"), (4, "模型")):
        ax.text(WORD_X, RC[idx], word, ha="center", va="center", fontsize=11,
                color=NAVY, fontweight="bold", zorder=4)

    # ---------------- 左欄:工作包標籤 ----------------
    for i, (name, sub, s, e, col) in enumerate(WPS):
        sub_lines = wrap(fig, sub, LX1 - LX0, 9) if sub else []
        top = RC[i] + (ph(12) + ph(9) * len(sub_lines)) / 2.0
        y = put(ax, LX0, top, [name], 12, col, weight="bold")
        ax.text(LX1, top - ph(12) / 2.0, "W%d-%d" % (s, e), ha="right",
                va="center", fontsize=9, color=col, fontweight="bold", zorder=4)
        put(ax, LX0, y - 0.001, sub_lines, 9, GREY)

    # ---------------- 決策門:貫穿虛線 + 實心菱形 ----------------
    for code, wk, _t, _b, _n in GATES:
        gx = xw(wk)
        ax.plot([gx] * 2, [BAND_BOT - 0.012, GATE_Y - 0.020], color=GREY, lw=1.5,
                ls=(0, (4, 3)), zorder=1.5)
        diamond(ax, gx, GATE_Y, 0.016, RED, RED, lw=1.2)
        ax.text(gx - 0.014, GATE_Y, "%s · W%d" % (code, wk), ha="right",
                va="center", fontsize=11, color=RED, fontweight="bold", zorder=7)

    # ---------------- 六列條形 ----------------
    for i, (_n, _s, s, e, col) in enumerate(WPS):
        x0, x1 = xw(s - 1), xw(e)
        y0 = RC[i] - BAR_H / 2.0
        ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, BAR_H,
                                    boxstyle="round,pad=0,rounding_size=0.004",
                                    fc=col, ec=col, lw=1.0, zorder=3))
        if i in (1, 2):                     # WP-B / WP-C 在 W1-6 內的限額探索
            ax.add_patch(Rectangle((x0, y0), xw(6) - x0, BAR_H, fc=col,
                                   ec="white", lw=0.0, hatch="////", zorder=4))

    # WP-E:W12 處切成前後兩段,段內白字
    ye0 = RC[4] - BAR_H / 2.0
    ax.plot([xw(12)] * 2, [ye0, ye0 + BAR_H], color="white", lw=1.4, zorder=5)
    ax.text((xw(7) + xw(12)) / 2.0, RC[4], "最小離線\n模型試驗", ha="center",
            va="center", fontsize=10, color="white", fontweight="bold",
            linespacing=1.25, zorder=5)
    ax.text((xw(12) + xw(24)) / 2.0, RC[4],
            "2×2(有無脈絡特徵 × 乾淨/現況標註)\n同一冷凍 hold-out", ha="center",
            va="center", fontsize=10, color="white", fontweight="bold",
            linespacing=1.25, zorder=5)

    # ---------------- 里程碑(空心菱形)+ 交付物 ----------------
    for i, wk, label, cite in MILESTONES:
        mx = xw(wk)
        diamond(ax, mx, RC[i], 0.0112, "white", NAVY, lw=1.5)
        if i <= 3:                          # 右側有空間 → 標在條形右端外側
            tx = mx + 0.010
            ml = wrap(fig, label, MX1 - tx, 10, "bold")
            dl = wrap(fig, DELIV_A, MX1 - tx, 9) if i == 0 else []
            top = RC[i] + (ph(10) * len(ml) + ph(9) * len(dl)) / 2.0
            y = put(ax, tx, top, ml, 10, NAVY, weight="bold", zorder=7, bg=True)
            if dl:
                put(ax, tx, y - 0.001, dl, 9, GREY, zorder=7, bg=True)
            if cite:                        # 引用標記印在交付物字串右端
                cx = tx + tw(fig, ml[-1], 10, "bold") + 0.008
                cy = y + ph(10) / 2.0
                if cx + tw(fig, cite, 9) > MX1:
                    cx, cy = tx, y - ph(9) / 2.0
                ax.text(cx, cy, cite, ha="left", va="center", fontsize=9,
                        color=GREY, zorder=7, bbox=dict(BG))
        else:                               # 右側空間不足 → 移到條形上緣
            ax.text(mx - 0.007, RC[i] + BAR_H / 2.0 + 0.015, label, ha="right",
                    va="center", fontsize=10, color=NAVY, fontweight="bold",
                    zorder=7, bbox=dict(BG))

    # WP-E 交付物與人月說明:右端無空間 → 置於條形帶左下留白區的白底卡
    bx0 = 0.270
    bx1 = xw(26) - tw(fig, MILESTONES[5][2], 10, "bold") - 0.016   # 讓開 M6 標籤
    el = []
    for s in DELIV_E:
        el += wrap(fig, s, bx1 - bx0 - 0.020, 9)
    bh = ph(9) * len(el) + 0.017
    by1 = RC[5] + ROW_H / 2.0 - 0.004
    ax.add_patch(FancyBboxPatch((bx0, by1 - bh), bx1 - bx0, bh,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                fc="white", ec=LIGHT, lw=1.0, zorder=6))
    ax.add_patch(Rectangle((bx0, by1 - bh), 0.0035, bh, fc=ORANGE, ec=ORANGE,
                           lw=0, zorder=6.5))
    put(ax, bx0 + 0.012, by1 - 0.0085, el, 9, GREY, zorder=7)

    # ---------------- 第一段(W1-6)範圍括弧 ----------------
    bk_y, drop = 0.940, 0.013
    cx = (xw(0) + xw(6)) / 2.0
    ax.plot([xw(0), xw(6)], [bk_y] * 2, color=GREY, lw=1.5, zorder=4)
    for bx in (xw(0), xw(6)):
        ax.plot([bx] * 2, [bk_y, bk_y - drop], color=GREY, lw=1.5, zorder=4)
    ax.text(cx, bk_y + 0.021, "第一段(W1-6):WP-A 全部 + WP-B / WP-C 限額探索",
            ha="center", va="center", fontsize=11, color=NAVY,
            fontweight="bold", zorder=4)
    ax.text(cx, bk_y - drop - 0.018,
            "G1 決定的是要不要續行剩下的工作,不是要不要開始",
            ha="center", va="center", fontsize=9, color=GREY, zorder=4)

    # ---------------- 決策門說明卡 ----------------
    for (cx0, cx1), (_code, wk, title, body, note) in zip(
            [(0.140, 0.442), (0.452, 0.722), (0.732, 0.966)], GATES):
        inner = cx1 - cx0 - 0.022
        bl = wrap(fig, body, inner, 9)
        nl = wrap(fig, note, inner, 9) if note else []
        h = 0.011 + ph(10) + 0.003 + ph(9) * len(bl) + \
            ((0.006 + ph(9) * len(nl)) if nl else 0.0) + 0.011
        ax.add_patch(FancyBboxPatch((cx0, CARD_TOP - h), cx1 - cx0, h,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    fc="white", ec=GREY, lw=1.1, zorder=6))
        ax.plot([xw(wk)] * 2, [BAND_BOT - 0.012, CARD_TOP], color=GREY, lw=1.0,
                ls=(0, (4, 3)), zorder=1.5)
        y = put(ax, cx0 + 0.011, CARD_TOP - 0.011, [title], 10, RED,
                weight="bold", zorder=7)
        y = put(ax, cx0 + 0.011, y - 0.003, bl, 9, NAVY, zorder=7)
        if nl:
            put(ax, cx0 + 0.011, y - 0.006, nl, 9, GREY, zorder=7)

    # ---------------- 圖例:形狀(說明卡左側留白) ----------------
    sx, sy = 0.018, 0.268
    for kind, txt in (("gate", "決策門 = 可喊停"),
                      ("mile", "里程碑 = 交付時點"),
                      ("bar", "條形 = 工作包期間")):
        if kind == "gate":
            diamond(ax, sx, sy, 0.011, RED, RED, lw=1.0)
        elif kind == "mile":
            diamond(ax, sx, sy, 0.0077, "white", NAVY, lw=1.4)
        else:
            ax.add_patch(FancyBboxPatch((sx - 0.010, sy - 0.008), 0.021, 0.016,
                                        boxstyle="round,pad=0,rounding_size=0.004",
                                        fc=NAVY, ec=NAVY, zorder=6))
        ax.text(sx + 0.017, sy, txt, ha="left", va="center", fontsize=10,
                color=NAVY, zorder=7)
        sy -= 0.037

    # ---------------- 圖例:顏色三帶 + 斜線紋 ----------------
    lx, ly = 0.018, 0.086
    for col, hat, txt in ((NAVY, None, "深藍 = ML 資料工程(WP-A / B / C)"),
                          (BLUE, None, "中藍 = 營運自動化(WP-D)"),
                          (ORANGE, None, "橘 = 模型訓練與評估(WP-E / F)"),
                          (NAVY, "////", "斜線紋 = 限額探索(已含在第一段額度內)")):
        ax.add_patch(Rectangle((lx, ly - 0.009), 0.022, 0.018, fc=col,
                               ec="white" if hat else col, lw=0.0, hatch=hat,
                               zorder=6))
        ax.text(lx + 0.029, ly, txt, ha="left", va="center", fontsize=10,
                color=NAVY, zorder=7)
        lx += 0.029 + tw(fig, txt, 10) + 0.030

    # ---------------- 右欄:今天 → 第 26 週 ----------------
    ax.plot([DIVX] * 2, [BAND_BOT, 0.884], color=LIGHT, lw=1.2, zorder=2)
    ax.text(RX0, 0.900, "今天 → 第 26 週", ha="left", va="center", fontsize=12,
            color=NAVY, fontweight="bold", zorder=7)
    cell_h = (BAND_TOP - BAND_BOT) / 4.0
    for j, (head, now, later) in enumerate(RIGHT_CELLS):
        cy = BAND_TOP - cell_h * (j + 0.5)
        if j:
            ax.plot([RX0, RX1], [BAND_TOP - cell_h * j] * 2, color=LIGHT, lw=0.8,
                    zorder=2)
        nl = wrap(fig, "今天:" + now, RX1 - RX0, 9)
        ll = wrap(fig, "第 26 週:" + later, RX1 - RX0 - 0.020, 9)
        total = ph(10) + ph(9) * (len(nl) + len(ll)) + 0.010
        y = put(ax, RX0, cy + total / 2.0, [head], 10, NAVY, weight="bold")
        y = put(ax, RX0, y - 0.003, nl, 9, GREY)
        ax.add_patch(FancyArrowPatch((RX0 + 0.001, y - 0.0135),
                                     (RX0 + 0.014, y - 0.0135),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color=ORANGE, lw=1.2, zorder=7))
        put(ax, RX0 + 0.020, y - 0.004, ll, 9, NAVY)

    # ---------------- 底部當責註記 ----------------
    ax.text(0.5, 0.044,
            "對照實驗的設計(hold-out 怎麼凍、因子怎麼拆、預註冊門檻訂在哪)"
            "由技術負責人在 W8 前提出、G2 核可;判準必須寫在跑實驗之前。",
            ha="center", va="center", fontsize=10, color=NAVY, zorder=7)
    ax.text(0.5, 0.012,
            "公開數據:資料工作佔掉分析人員約八成時間;前兩包份量偏重是常態,"
            "不是計畫灌水 (Press, 2016)。",
            ha="center", va="center", fontsize=9, color=GREY, zorder=7)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_09")
