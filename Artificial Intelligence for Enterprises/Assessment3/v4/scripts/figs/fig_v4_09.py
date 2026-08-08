# -*- coding: utf-8 -*-
"""P9 用圖:六個月 · 六個工作包 · 三道決策門(甘特主視覺)。

規格來源:v4/notes/04_十頁內容_v2.md 的「# P9 · 六個月 · 六個工作包 · 三道決策門」→ ## 視覺規格。
共用機具:scripts/make_figs_v4.py(字型 / 色票 / save / newfig / assert_min_fontsize),只 import 不修改。

🔴 裁決 O(v4/notes/12_出圖稽核與畫布裁決.md §二):
- 畫布**鎖死** 12.2 x 5.7 吋 = 組版時內容區的實際形狀,置入縮放比 = 1.0,所以 fs=9 就是真的 9pt。
  不得為了塞下內容而放大畫布。
- 內容塞不下時**砍內容**:本頁依規格「寧可縮短副標也不縮字級」的原則,
  處置順序 = ①帶狀純文字移出圖(由組版程式以投影片文字框放)②縮短圖內標籤 ③才動主視覺。
- 本輪移出圖的元素見檔尾 MOVED_TO_SLIDE(組版程式照該清單放,一個字都不能少)。

圖裡只留「需要圖形關係才講得清楚」的主視覺:
  時間軸 + 六條甘特條 + 三道門的位置 + 六個里程碑的位置 + 顏色三帶 + 左側順序箭頭 + 第一段括弧。

紅線:
- 色值只用 make_figs_v4 的常數(ORANGE / NAVY / BLUE / RED / GREY / LIGHT),本檔不寫死任何色碼。
- 圖內最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形破折號 / U+2212 / U+00D7。
- 圖不畫投影片標題、不畫右上角五格進度指示(兩者由組版程式負責)。
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
# 畫布 —— 裁決 O 鎖死值,不得更動
# ------------------------------------------------------------------
FIG_W, FIG_H = 12.2, 5.7
H_PT = FIG_H * 72.0

# 兩欄:左欄工作包標籤 / 右側時間軸(原「今天 → 第 26 週」對照欄整組移出圖)
ARROW_X, WORD_X = 0.008, 0.034    # 左側順序箭頭與四個詞
LX0, LX1 = 0.062, 0.245           # 左欄文字
MX0, MX1 = 0.258, 0.982           # 時間軸(W0 ~ W26);右緣留給 W26 刻度字不出血

WK = (MX1 - MX0) / 26.0

BAND_TOP, BAND_BOT = 0.840, 0.250
ROW_H = (BAND_TOP - BAND_BOT) / 6.0
BAR_H = ROW_H * 0.55
RC = [BAND_TOP - ROW_H * (i + 0.5) for i in range(6)]   # A..F 列心

GATE_Y = 0.878                    # 決策門菱形所在列
BK_Y, BK_DROP = 0.938, 0.018      # 第一段括弧


def xw(week):
    return MX0 + week * WK


# ------------------------------------------------------------------
# 文字量測與換行(以 renderer 實測,單位一律「圖寬比例」)
# ------------------------------------------------------------------
_TOK = re.compile(r"\([A-Za-z][^)]*\)|[A-Za-z0-9][A-Za-z0-9\.\-_/%]*|.", re.S)
_NOBREAK = "、。,;:)」』】,.;:)!?%"
_REND = [None]
_AX = [None]


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
    """把字串折成每行寬度不超過 max_w 的多行 list。"""
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
# 圖內內容(全部取自 P9 視覺規格,未新增任何數值)
# 工作包副標、交付物長句、決策門說明卡內文、右欄對照表、底部註記 -> 移出圖(見 MOVED_TO_SLIDE)
# ------------------------------------------------------------------
WPS = [
    ("WP-A 評估底座", 1, 6, NAVY),
    ("WP-B 標註品質", 3, 10, NAVY),
    ("WP-C 脈絡特徵工程", 5, 12, NAVY),
    ("WP-D 爭議回覆自動化", 8, 16, BLUE),
    ("WP-E 對照重訓", 8, 24, ORANGE),
    ("WP-F 治理與移交", 20, 26, ORANGE),
]

# 決策門:圖上只留位置 + 代號 + 門的性質(說明卡內文移出圖)
GATES = [("G1", 6, "因果判定門"),
         ("G2", 12, "三方比較門"),
         ("G3", 24, "部署決定門")]

# 里程碑:(列索引, 週次, 短交付名, in-text 引用標記)
MILESTONES = [
    (0, 6, "M1 W6 · 首份含漏放的錯誤率", ""),
    (1, 10, "M2 W10 · 判準手冊 + 一致性儀表板", "(Northcutt et al., 2021)"),
    (2, 12, "M3 W12 · 規則式脈絡層 + 誤報下降量測", "(Rudin, 2019)"),
    (3, 16, "M4 W16 · 自動證據包 + 回覆時效改善", ""),
    (4, 24, "M5 W24 · 對照重訓結果", ""),
    (5, 26, "M6 W26 · 移交文件 + 常態儀表板", ""),
]

SHAPE_LEGEND = [("gate", "決策門 = 可喊停"),
                ("mile", "里程碑 = 交付時點"),
                ("bar", "條形 = 工作包期間")]

COLOR_LEGEND = [(NAVY, None, "深藍 = ML 資料工程"),
                (BLUE, None, "中藍 = 營運自動化"),
                (ORANGE, None, "橘 = 模型訓練與評估"),
                (NAVY, "////", "斜線紋 = 限額探索")]


# ==================================================================
def build():
    fig, ax = newfig(FIG_W, FIG_H)          # 不下標題:標題由組版程式放
    _bind(fig, ax)

    # ---------------- 時間軸:格線 / 軸線 / 週刻度 ----------------
    for w in range(2, 27, 2):
        ax.plot([xw(w)] * 2, [BAND_BOT, BAND_TOP], color=LIGHT, lw=0.7,
                alpha=0.9, zorder=0.5)
    ax.plot([xw(0), xw(26)], [BAND_BOT] * 2, color=GREY, lw=0.9, zorder=1)
    for w in range(2, 27, 2):
        if w in (6, 12, 24):                # 這三週改由決策門標示,避免疊字
            continue
        ax.text(xw(w), BAND_BOT - 0.030, "W%d" % w, ha="center", va="center",
                fontsize=9, color=GREY, zorder=2)

    # ---------------- 左欄:順序箭頭(順序不可換) ----------------
    ax.add_patch(FancyArrowPatch((ARROW_X, RC[0] + 0.030), (ARROW_X, RC[4] - 0.032),
                                 arrowstyle="-|>", mutation_scale=13, color=GREY,
                                 lw=1.3, zorder=3))
    for idx, word in ((0, "評估集"), (1, "標註"), (2, "特徵"), (4, "模型")):
        ax.text(WORD_X, RC[idx], word, ha="center", va="center", fontsize=11,
                color=NAVY, fontweight="bold", zorder=4)

    # ---------------- 左欄:工作包名 + 起訖週 ----------------
    for i, (name, s, e, col) in enumerate(WPS):
        nl = wrap(fig, name, LX1 - LX0, 12, "bold")
        assert len(nl) == 1, "工作包名折行了,請縮短:%s" % name
        top = RC[i] + (ph(12) + ph(9)) / 2.0
        y = put(ax, LX0, top, nl, 12, col, weight="bold")
        put(ax, LX0, y - 0.001, ["W%d-%d" % (s, e)], 9, GREY)

    # ---------------- 決策門:貫穿虛線 + 實心菱形 + 代號 ----------------
    for code, wk, kind in GATES:
        gx = xw(wk)
        ax.plot([gx] * 2, [BAND_BOT - 0.014, GATE_Y - 0.022], color=GREY, lw=1.5,
                ls=(0, (4, 3)), zorder=1.5)
        diamond(ax, gx, GATE_Y, 0.019, RED, RED, lw=1.2)
        ax.text(gx - 0.014, GATE_Y, "%s · W%d %s" % (code, wk, kind), ha="right",
                va="center", fontsize=11, color=RED, fontweight="bold", zorder=7)

    # ---------------- 六列條形 ----------------
    for i, (_n, s, e, col) in enumerate(WPS):
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
    ax.text((xw(7) + xw(12)) / 2.0, RC[4], "最小離線模型試驗", ha="center",
            va="center", fontsize=10, color="white", fontweight="bold", zorder=5)
    ax.text((xw(12) + xw(24)) / 2.0, RC[4], "2x2 對照 · 同一冷凍 hold-out",
            ha="center", va="center", fontsize=10, color="white",
            fontweight="bold", zorder=5)

    # ---------------- 里程碑(空心菱形)+ 短交付名 ----------------
    for i, wk, label, cite in MILESTONES:
        mx = xw(wk)
        diamond(ax, mx, RC[i], 0.0133, "white", NAVY, lw=1.5)
        if i <= 3:                          # 右側有空間 -> 標在條形右端外側
            tx = mx + 0.012
            ax.text(tx, RC[i], label, ha="left", va="center", fontsize=10,
                    color=NAVY, fontweight="bold", zorder=7, bbox=dict(BG))
            if cite:
                cx = tx + tw(fig, label, 10, "bold") + 0.010
                ax.text(cx, RC[i], cite, ha="left", va="center", fontsize=9,
                        color=GREY, zorder=7, bbox=dict(BG))
        else:                               # 右側無空間 -> 移到條形上緣(壓在列界上)
            ax.text(mx - 0.009, RC[i] + ROW_H / 2.0, label, ha="right",
                    va="center", fontsize=10, color=NAVY, fontweight="bold",
                    zorder=7, bbox=dict(BG))

    # ---------------- 第一段(W1-6)範圍括弧 ----------------
    cx = (xw(0) + xw(6)) / 2.0
    ax.plot([xw(0), xw(6)], [BK_Y] * 2, color=GREY, lw=1.5, zorder=4)
    for bx in (xw(0), xw(6)):
        ax.plot([bx] * 2, [BK_Y, BK_Y - BK_DROP], color=GREY, lw=1.5, zorder=4)
    ax.text(cx, BK_Y + 0.030, "第一段(W1-6):WP-A 全部 + WP-B / WP-C 限額探索",
            ha="center", va="center", fontsize=11, color=NAVY,
            fontweight="bold", zorder=4)

    # ---------------- 圖例:形狀(置中一列) ----------------
    gap, pad = 0.030, 0.009
    sw = 0.021
    total = sum(sw + pad + tw(fig, t, 10) for _k, t in SHAPE_LEGEND) \
        + gap * (len(SHAPE_LEGEND) - 1)
    sx, sy = (1.0 - total) / 2.0, 0.148
    for kind, txt in SHAPE_LEGEND:
        if kind == "gate":
            diamond(ax, sx + sw / 2.0, sy, 0.014, RED, RED, lw=1.0)
        elif kind == "mile":
            diamond(ax, sx + sw / 2.0, sy, 0.0098, "white", NAVY, lw=1.4)
        else:
            ax.add_patch(FancyBboxPatch((sx, sy - 0.010), sw, 0.020,
                                        boxstyle="round,pad=0,rounding_size=0.004",
                                        fc=NAVY, ec=NAVY, zorder=6))
        ax.text(sx + sw + pad, sy, txt, ha="left", va="center", fontsize=10,
                color=NAVY, zorder=7)
        sx += sw + pad + tw(fig, txt, 10) + gap

    # ---------------- 圖例:顏色三帶 + 斜線紋(置中一列) ----------------
    total = sum(sw + pad + tw(fig, t, 10) for _c, _h, t in COLOR_LEGEND) \
        + gap * (len(COLOR_LEGEND) - 1)
    lx, ly = (1.0 - total) / 2.0, 0.058
    for col, hat, txt in COLOR_LEGEND:
        ax.add_patch(Rectangle((lx, ly - 0.010), sw, 0.020, fc=col,
                               ec="white" if hat else col, lw=0.0, hatch=hat,
                               zorder=6))
        ax.text(lx + sw + pad, ly, txt, ha="left", va="center", fontsize=10,
                color=NAVY, zorder=7)
        lx += sw + pad + tw(fig, txt, 10) + gap

    assert_min_fontsize(fig)
    return fig


# ==================================================================
# 🔑 移出圖、改由 build_deck_v4.py 以投影片文字框放置的元素(一個字都不能少)
#    格式:(區塊代號, 版面位置, 內容行 list)
# ==================================================================
MOVED_TO_SLIDE = [
    ("P9-T1", "圖上方 · 第一段括弧下方的說明行(靠左,對齊圖左緣)", [
        "G1 決定的是要不要續行剩下的工作,不是要不要開始",
    ]),
    ("P9-T2", "圖下方左欄 · 決策門說明卡(三段並排或三段條列)", [
        "G1 · W6 因果判定門:交出爭議處理的時間拆解(等待 / 找證據 / 判讀 / 內部覆核 / 回信)、"
        "兩天逾時率與尖峰到件分布。只有當「證據搜尋、誤報量與證據包製作」佔主要延遲,才續行後段;"
        "否則本案轉為排班與尖峰人力池方案。評估底座未產出,剩餘工作全數不續行。"
        "待確認:時間拆解與兩天逾時率目前無現成數字,這正是 W1-6 要交的東西。",
        "G2 · W12 三方比較門:在同一凍結評估集上同時比三組:①現行影像模型 ②規則式脈絡基線 "
        "③脈絡增強的學習模型。成功條件:誤報改善達預註冊門檻,且漏放率信賴區間不惡化。"
        "本門只能調整模型的假設與規模,不能取消實驗。"
        "規則式若已解掉大部分誤報,靶心改為殘餘(情境模糊與判準爭議);"
        "若無效,先查脈絡資料本身的品質,再決定模型端的規模。",
        "G3 · W24 部署決定門:對照重訓證不出增量,模型端不部署,只留前四包的成果。",
    ]),
    ("P9-T3", "圖左欄延伸 · 六個工作包的副標與交付(緊貼圖左側或置於圖下方,順序同圖)", [
        "WP-A 評估底座:分層抽樣 + 冷凍 hold-out + 首份含漏放的錯誤率 (Press, 2016)"
        "｜交付:可稽核的錯誤率(含信賴區間)+ 冷凍評估集 + 兩條工作流的單位工時正式基準 "
        "+ 時間拆解(等待 / 找證據 / 判讀 / 內部覆核 / 回信)+ 兩天逾時率 + 尖峰到件分布",
        "WP-B 標註品質:誤報的操作型定義 + 判準明文化 + 黃金題 + 複核者一致性係數 (Press, 2016)"
        "｜交付:判準手冊 + 一致性儀表板 (Northcutt et al., 2021)",
        "WP-C 脈絡特徵工程:定位與地圖速限特徵化,規則式為基線"
        "｜交付:規則式脈絡層 + 誤報下降量測 (Rudin, 2019)",
        "WP-D 爭議回覆自動化｜交付:自動證據包 + 回覆時效改善",
        "WP-E 對照重訓:W8-12 最小離線模型試驗 -> W12-24 2x2(有無脈絡特徵 x 乾淨/現況標註),"
        "同一冷凍 hold-out｜交付:三方對照結果(現行影像模型 / 規則式脈絡基線 / 脈絡增強的學習模型)"
        "+ 有脈絡 vs 無脈絡的對照結果",
        "總投入 4.50 人月不變,係 WP-E 內部人力前移,不增加總人月",
        "WP-F 治理與移交｜交付:移交文件 + 常態儀表板",
    ]),
    ("P9-T4", "圖右側或圖下方右欄 · 「今天 -> 第 26 週」對照四列(欄首標題 + 四列)", [
        "今天 -> 第 26 週",
        "① 判讀依據:人去外面找 -> 事件送到人手上時已附證據",
        "② 複核判準:口耳相傳 -> 明文手冊 + 一致性儀表板",
        "③ 漏放:沒有數字 -> 有數字、有信賴區間、每月更新",
        "④ 交付時效:現況單件爭議 2-5 天 -> 提案目標 2 天內;單純案件當天",
    ]),
    ("P9-T5", "投影片頁腳 · 當責註記兩行(第一行深藍,第二行灰)", [
        "對照實驗的設計(hold-out 怎麼凍、因子怎麼拆、預註冊門檻訂在哪)"
        "由技術負責人在 W8 前提出、G2 核可;判準必須寫在跑實驗之前。",
        "公開數據:資料工作佔掉分析人員約八成時間;前兩包份量偏重是常態,"
        "不是計畫灌水 (Press, 2016)。",
    ]),
]


if __name__ == "__main__":
    save(build(), "fig_v4_09")
