# -*- coding: utf-8 -*-
"""P9 用圖:六個月 · 六個工作包 · 三道決策門(甘特主視覺)。

規格來源:v4/notes/_v2_parts/P08-11.md 的「# P9 · 六個月 · 六個工作包 · 三道決策門」→ ## 視覺規格
(2026-08-09 地端 VLM 升級版:含【🔴 AI 主包視覺加重】整段)。
共用機具:scripts/make_figs_v4.py(字型 / 色票 / save / newfig / assert_min_fontsize),只 import 不修改。

🔴 本輪主改(視覺規格【AI 主包視覺加重】①~⑦):
  這張圖的讀者要在三秒內看出**哪一包是 AI**。原本六條外觀相同 = 沒說。
  ① WP-E 條高 = 該列列高 80%(其餘五條 55%),且該列列高本身放大為其他列的 1.45 倍
     —— 這是為了容納「徽章 + 名稱 + 起訖週」三行左欄標籤與條內兩行白字,不動任何週次。
  ② WP-E 填 ORANGE 實心(全圖唯一的橘塊);WP-A/B/C 深藍降為 72% 不透明、WP-D 中藍降為 72%、
     WP-F 改為 NAVY 30% 不透明(= 淺灰藍,收尾不與主角爭視線)。
  ③ WP-E 加 2.5pt ORANGE_DARK 外框,其餘五條無外框。
  ④ 左欄:WP-E 名稱 fs=13 粗體 + 橘底白字徽章「AI 主體」,該列底色刷 8% 橘。
  ⑤ 加註兩段(AI 主體宣告 + 主線模型 + 「AI 不做判定」)—— 見下方 ⚠️ 位置說明。
  ⑥ 左緣 3pt 直立引導條分三段:AI 的前置 / 併行的營運自動化 / AI 之後的治理移交。
  ⑦ 圖例色塊列第一格 = 「橘色實心加粗 = 本案的 AI 主體(只有一包)」,fs=11 粗體。
  🚫 加重只走外觀:WP-E 仍是 W8-24、切點仍是 W12、G1/G2/G3 仍在 W6/W12/W24、總投入仍是 4.50 人月。

⚠️ 與視覺規格的一處位置偏離(裁決 O 逼出來的,已如實記錄):
  規格⑤要求加註放「條形上緣外側」。實測 WP-D 條底與 WP-E 條頂之間只有約 13.8pt 淨空,
  放不下 fs=11 + fs=11 + fs=9 三行(約 54pt),放大畫布為裁決 O 明文禁止。
  → 改置於 **WP-E 條形正下方**(WP-F 列 W1-19 的整片空白區,左對齊時間軸左緣),
    仍緊貼 WP-E 條形、仍在條形外側、不壓任何條形或刻度。文字一字未刪。

🔴 裁決 O(v4/notes/12_出圖稽核與畫布裁決.md §二):
- 畫布**鎖死** 12.2 x 5.7 吋 = 組版時內容區的實際形狀,置入縮放比 = 1.0,所以 fs=9 就是真的 9pt。
  不得為了塞下內容而放大畫布。save() 已設 pad_inches=0,本檔不做任何尺寸補償。
- 內容塞不下時**砍內容**:處置順序 = ①帶狀純文字移出圖 ②縮短圖內標籤 ③才動主視覺。
- 本輪移出圖的元素見檔尾 MOVED_TO_SLIDE(組版程式照該清單放,一個字都不能少)。

圖裡只留「需要圖形關係才講得清楚」的主視覺:
  時間軸 + 六條甘特條(AI 那條加重)+ 三道門的位置 + 六個里程碑的位置 + 顏色四階
  + 左側順序箭頭 + 左緣前置/併行/後續引導條 + 第一段括弧 + AI 主體加註。

紅線:
- 色值只用 make_figs_v4 的常數(ORANGE / ORANGE_DARK / NAVY / BLUE / RED / GREY / LIGHT),
  本檔不寫死任何色碼;規格裡的 #7F3F0F 以機具常數 ORANGE_DARK 代之,
  「淺灰藍 #B4C6DC」以 NAVY @ 30% 不透明代之(白底上等效)。
- 圖內最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形破折號 / U+2212 / U+00D7
  (規格的「2×2」在圖上一律寫成 2x2)。
- 圖不畫投影片標題、不畫右上角五格進度指示(兩者由組版程式負責)。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    NAVY, BLUE, ORANGE, ORANGE_DARK, GREY, LIGHT, RED,
    assert_min_fontsize, save, newfig,
)
from matplotlib.text import Text  # noqa: E402
from matplotlib.patches import (  # noqa: E402
    FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle,
)

# ------------------------------------------------------------------
# 畫布 —— 裁決 O 鎖死值,不得更動
# ------------------------------------------------------------------
FIG_W, FIG_H = 12.2, 5.7
H_PT = FIG_H * 72.0

# 左緣四道:引導條 / 引導條分段標字 / 順序箭頭 / 順序四詞
GBAR_X, GTXT_X = 0.005, 0.019
ARROW_X, WORD_X = 0.030, 0.064
LX0, LX1 = 0.098, 0.246           # 左欄工作包名
MX0, MX1 = 0.262, 0.982           # 時間軸(W0 ~ W26);右緣留給 W26 刻度字不出血

WK = (MX1 - MX0) / 26.0

BAND_TOP, BAND_BOT = 0.840, 0.250

# 🔴 列高非等分:WP-E(索引 4)那一列 1.45 倍,其餘五列等高。
#    放大的是「列」不是「畫布」—— 總帶高仍是 BAND_TOP-BAND_BOT,裁決 O 不受影響。
E_IDX = 4
ROW_W = [1.0, 1.0, 1.0, 1.0, 1.45, 1.0]
U = (BAND_TOP - BAND_BOT) / sum(ROW_W)
RH = [w * U for w in ROW_W]
RTOP, _y = [], BAND_TOP
for _h in RH:
    RTOP.append(_y)
    _y -= _h
RC = [RTOP[i] - RH[i] / 2.0 for i in range(6)]          # A..F 列心
BARH = [RH[i] * (0.80 if i == E_IDX else 0.55) for i in range(6)]

GATE_Y = 0.878                    # 決策門菱形所在列
BK_Y, BK_DROP = 0.938, 0.018      # 第一段括弧


def xw(week):
    return MX0 + week * WK


def top_of(i):
    """第 i 條的條頂 y。"""
    return RC[i] + BARH[i] / 2.0


def bot_of(i):
    """第 i 條的條底 y。"""
    return RC[i] - BARH[i] / 2.0


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


def th(fig, s, fs, weight="normal"):
    """字串高度(直排引導條標字用),單位 = 版面 0-1 座標的 y 比例。"""
    if not s:
        return 0.0
    t = fig.text(0, 0, s, fontsize=fs, fontweight=weight)
    h = t.get_window_extent(renderer=_REND[0]).width / _AX[0].bbox.height
    t.remove()
    return h


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
        zorder=6, bg=False, alpha=None):
    """自 y_top 往下逐行寫字,回傳寫完後的 y。"""
    p = ph(fs, lp)
    y = y_top - p / 2.0
    for ln in lines:
        ax.text(x, y, ln, ha=ha, va="center", fontsize=fs, color=color,
                fontweight=weight, zorder=zorder, alpha=alpha,
                bbox=dict(BG) if bg else None)
        y -= p
    return y + p / 2.0


def diamond(ax, x, y, half_h, fc, ec, lw=1.5, zorder=7):
    hw = half_h * (FIG_H / FIG_W)
    ax.add_patch(Polygon([(x, y + half_h), (x + hw, y), (x, y - half_h),
                          (x - hw, y)], closed=True, fc=fc, ec=ec, lw=lw,
                         zorder=zorder))


def assert_no_text_overlap(fig, slack_pt=0.6):
    """程式驗:圖內任兩個文字物件的實體外框不得相交(留 slack_pt 容差)。"""
    rend = _REND[0]
    items = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        bb = t.get_window_extent(renderer=rend)
        items.append((s.replace("\n", " / ")[:26], bb))
    bad = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > slack_pt and oy > slack_pt:
                bad.append((items[i][0], items[j][0],
                            round(ox, 1), round(oy, 1)))
    assert not bad, "圖內文字重疊 %d 處:%s" % (len(bad), bad[:6])
    return len(items)


# ------------------------------------------------------------------
# 圖內內容(全部取自 P9 視覺規格,未新增任何數值)
# 工作包副標、交付物長句、決策門說明卡內文、右欄對照表、底部註記 -> 移出圖(見 MOVED_TO_SLIDE)
# ------------------------------------------------------------------
# (工作包名, 起週, 迄週, 條色, 條的不透明度, 左欄名色, 左欄名的不透明度)
WPS = [
    ("WP-A 評估底座",      1,  6, NAVY,   0.72, NAVY,        1.0),
    ("WP-B 標註品質",      3, 10, NAVY,   0.72, NAVY,        1.0),
    ("WP-C 脈絡特徵工程",  5, 12, NAVY,   0.72, NAVY,        1.0),
    ("WP-D 爭議回覆自動化", 8, 16, BLUE,   0.72, BLUE,        1.0),
    ("WP-E 地端 VLM 事件判讀", 8, 24, ORANGE, 1.00, ORANGE_DARK, 1.0),
    ("WP-F 治理與移交",   20, 26, NAVY,   0.30, GREY,        1.0),
]

# ⑥ 左緣引導條三段:(起列, 迄列, 標字, 色, 不透明度)
GUIDE = [
    (0, 2, "AI 的前置",        NAVY, 0.85),
    (3, 3, "併行的營運自動化",  BLUE, 0.85),
    (5, 5, "AI 之後的治理移交", NAVY, 0.45),
]

# 決策門:圖上只留位置 + 代號 + 門的性質(說明卡內文移出圖)
GATES = [("G1", 6, "因果判定門"),
         ("G2", 12, "三方比較門"),
         ("G3", 24, "部署決定門")]

# 里程碑:(列索引, 週次, 短交付名, in-text 引用標記)
MILESTONES = [
    (0, 6, "M1 W6 · 首份含漏放的錯誤率 + 時間拆解", ""),
    (1, 10, "M2 W10 · 判準手冊 + 一致性儀表板", "(Northcutt et al., 2021)"),
    (2, 12, "M3 W12 · 規則式脈絡層 + 誤報下降量測", "(Rudin, 2019)"),
    (3, 16, "M4 W16 · 自動證據包 + 回覆時效改善", ""),
    (4, 24, "M5 W24 · 三方對照結果(含地端 VLM)", ""),
    (5, 26, "M6 W26 · 移交文件 + 常態儀表板", ""),
]

# ⑤ AI 主體加註(置於 WP-E 條形正下方,見檔頭偏離說明)
AI_NOTE = [
    ("本案的 AI 主體:地端 VLM 事件判讀", 11, ORANGE_DARK, "bold"),
    ("主線模型 Qwen3.5 122B-A10B(4-bit),跑在地端 128G 設備上", 11, NAVY, "normal"),
    ("AI 不做判定,AI 做的是把證據整理好;判定仍由人做。", 9, GREY, "normal"),
]

SHAPE_LEGEND = [("gate", "決策門 = 可喊停"),
                ("mile", "里程碑 = 交付時點"),
                ("bar", "條形 = 工作包期間")]

# ⑦ 色塊圖例五格,AI 主體那一格排第一且加粗放大
COLOR_LEGEND = [
    (ORANGE, 1.00, None, "橘色實心加粗 = 本案的 AI 主體(只有一包)", 11, "bold"),
    (NAVY,   0.72, None, "深藍 = AI 的前置", 10, "normal"),
    (BLUE,   0.72, None, "中藍 = 併行的營運自動化", 10, "normal"),
    (NAVY,   0.30, None, "淺灰藍 = AI 之後的治理移交", 10, "normal"),
    (NAVY,   0.72, "////", "斜線紋 = 限額探索", 10, "normal"),
]


# ==================================================================
def build():
    fig, ax = newfig(FIG_W, FIG_H)          # 不下標題:標題由組版程式放
    _bind(fig, ax)

    # ---------------- ④ WP-E 那一列的左欄底色(8% 橘) ----------------
    ax.add_patch(Rectangle((ARROW_X - 0.004, RTOP[E_IDX] - RH[E_IDX]),
                           LX1 + 0.008 - (ARROW_X - 0.004), RH[E_IDX],
                           fc=ORANGE, ec="none", alpha=0.08, zorder=0.2))

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

    # ---------------- ⑥ 左緣引導條:前置 / 併行 / 後續 ----------------
    for i0, i1, word, col, al in GUIDE:
        y_hi = RTOP[i0] - RH[i0] * 0.08
        y_lo = RTOP[i1] - RH[i1] * 0.92
        ax.plot([GBAR_X] * 2, [y_lo, y_hi], color=col, lw=3.0, alpha=al,
                solid_capstyle="butt", zorder=3)
        ax.text(GTXT_X, (y_hi + y_lo) / 2.0, word, ha="center", va="center",
                rotation=270, rotation_mode="anchor", fontsize=9, color=col,
                alpha=max(al, 0.8), zorder=4)

    # ---------------- 左欄:工作包名 + 起訖週 ----------------
    for i, (name, s, e, _c, _a, tcol, tal) in enumerate(WPS):
        if i == E_IDX:
            continue
        nl = wrap(fig, name, LX1 - LX0, 12, "bold")
        assert len(nl) == 1, "工作包名折行了,請縮短:%s" % name
        top = RC[i] + (ph(12) + ph(9)) / 2.0
        y = put(ax, LX0, top, nl, 12, tcol, weight="bold", alpha=tal)
        put(ax, LX0, y - 0.001, ["W%d-%d" % (s, e)], 9, GREY)

    # ④ WP-E 左欄:徽章「AI 主體」+ WP-E + 名稱 fs=13 粗體 + 起訖週
    name, s, e = WPS[E_IDX][0], WPS[E_IDX][1], WPS[E_IDX][2]
    head, tail = name.split(" ", 1)                     # "WP-E" / "地端 VLM 事件判讀"
    tot = ph(10) + ph(13) + ph(9)
    ytop = RC[E_IDX] + tot / 2.0
    bh = ph(10) * 0.84
    bw = tw(fig, "AI 主體", 10, "bold") + 0.014
    by = ytop - ph(10) / 2.0 - bh / 2.0
    ax.add_patch(FancyBboxPatch((LX0, by), bw, bh,
                                boxstyle="round,pad=0,rounding_size=0.004",
                                fc=ORANGE, ec=ORANGE_DARK, lw=1.0, zorder=6))
    ax.text(LX0 + bw / 2.0, by + bh / 2.0, "AI 主體", ha="center", va="center",
            fontsize=10, color="white", fontweight="bold", zorder=7)
    ax.text(LX0 + bw + 0.009, ytop - ph(10) / 2.0, head, ha="left", va="center",
            fontsize=13, color=ORANGE_DARK, fontweight="bold", zorder=6)
    assert tw(fig, tail, 13, "bold") <= LX1 - LX0, "WP-E 名稱過寬:%s" % tail
    ax.text(LX0, ytop - ph(10) - ph(13) / 2.0, tail, ha="left", va="center",
            fontsize=13, color=ORANGE_DARK, fontweight="bold", zorder=6)
    ax.text(LX0, ytop - ph(10) - ph(13) - ph(9) / 2.0, "W%d-%d" % (s, e),
            ha="left", va="center", fontsize=9, color=GREY, zorder=6)

    # ---------------- 左欄:順序箭頭(順序不可換) ----------------
    # 末詞「地端 VLM」對齊 WP-E 那一列的**徽章行**(不對列心)——
    # 對列心會與名稱第二行「地端 VLM 事件判讀」並排,讀起來像重複印了一次。
    e_word_y = ytop - ph(10) / 2.0
    ax.add_patch(FancyArrowPatch((ARROW_X, RC[0] + 0.030),
                                 (ARROW_X, e_word_y - 0.026),
                                 arrowstyle="-|>", mutation_scale=13, color=GREY,
                                 lw=1.3, zorder=3))
    for idx, word in ((0, "評估集"), (1, "標註"), (2, "特徵")):
        ax.text(WORD_X, RC[idx], word, ha="center", va="center", fontsize=11,
                color=NAVY, fontweight="bold", zorder=4)
    ax.text(WORD_X, e_word_y, "地端 VLM", ha="center", va="center", fontsize=11,
            color=ORANGE_DARK, fontweight="bold", zorder=4)

    # ---------------- 決策門:貫穿虛線 + 實心菱形 + 代號 ----------------
    for code, wk, kind in GATES:
        gx = xw(wk)
        ax.plot([gx] * 2, [BAND_BOT - 0.014, GATE_Y - 0.022], color=GREY, lw=1.5,
                ls=(0, (4, 3)), zorder=1.5)
        diamond(ax, gx, GATE_Y, 0.019, RED, RED, lw=1.2)
        ax.text(gx - 0.014, GATE_Y, "%s · W%d %s" % (code, wk, kind), ha="right",
                va="center", fontsize=11, color=RED, fontweight="bold", zorder=7)

    # ---------------- 六列條形(①②③ AI 主包加重) ----------------
    for i, (_n, s, e, col, al, _tc, _ta) in enumerate(WPS):
        x0, x1 = xw(s - 1), xw(e)
        y0 = RC[i] - BARH[i] / 2.0
        is_ai = (i == E_IDX)
        ax.add_patch(FancyBboxPatch(
            (x0, y0), x1 - x0, BARH[i],
            boxstyle="round,pad=0,rounding_size=0.004",
            fc=col, ec=ORANGE_DARK if is_ai else col,
            lw=2.5 if is_ai else 1.0, alpha=al, zorder=4 if is_ai else 3))
        if i in (1, 2):                     # WP-B / WP-C 在 W1-6 內的限額探索
            ax.add_patch(Rectangle((x0, y0), xw(6) - x0, BARH[i], fc=col,
                                   ec="white", lw=0.0, hatch="////", alpha=al,
                                   zorder=3.5))

    # WP-E:W12 處切成前後兩段,段內白字(後段兩行)
    ye0, ye1 = bot_of(E_IDX), top_of(E_IDX)
    ax.plot([xw(12)] * 2, [ye0, ye1], color="white", lw=1.6, zorder=5)
    ax.text((xw(7) + xw(12)) / 2.0, RC[E_IDX], "最小離線試驗", ha="center",
            va="center", fontsize=10, color="white", fontweight="bold", zorder=5)
    put(ax, (xw(12) + xw(24)) / 2.0,
        RC[E_IDX] + ph(10, 1.30),
        ["2x2 對照:有無脈絡特徵 x 乾淨/現況標註", "同一冷凍 hold-out"],
        10, "white", ha="center", lp=1.30, weight="bold", zorder=5)

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
        else:                               # 右側無空間 -> 移到上一條與本條之間的淨空
            ax.text(mx - 0.009, (bot_of(i - 1) + top_of(i)) / 2.0, label,
                    ha="right", va="center", fontsize=10, color=NAVY,
                    fontweight="bold", zorder=7, bbox=dict(BG))

    # ---------------- ⑤ AI 主體加註(WP-E 條形正下方的空白區) ----------------
    # 起點盡量貼齊 WP-E 條形左端(xw(7)),塞不下才往左退,但不得越過時間軸左緣,
    # 也不得撞上 WP-F 條形左端(xw(19))。
    nw = max(tw(fig, t, f, w) for t, f, _c, w in AI_NOTE)
    nx = max(MX0, min(xw(7), xw(19) - 0.014 - nw))
    # 與橘條相連的細引線(L 形:自條底左端橫過來,再往下沿著加註)
    ax.plot([nx - 0.008, xw(7) + 0.010], [bot_of(E_IDX) - 0.004] * 2,
            color=ORANGE, lw=2.0, zorder=3, solid_capstyle="butt")
    ax.plot([nx - 0.008] * 2, [bot_of(E_IDX) - 0.004, BAND_BOT + 0.010],
            color=ORANGE, lw=2.0, zorder=3)
    y = bot_of(E_IDX) - 0.007
    for txt, fs, col, wt in AI_NOTE:
        y -= ph(fs, 1.18) / 2.0
        assert nx + tw(fig, txt, fs, wt) < xw(19) - 0.010, "AI 加註過寬:%s" % txt
        ax.text(nx, y, txt, ha="left", va="center", fontsize=fs, color=col,
                fontweight=wt, zorder=7, bbox=dict(BG))
        y -= ph(fs, 1.18) / 2.0 + 0.001
    assert y > BAND_BOT - 0.004, "AI 加註掉出條形帶"

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
                                        fc=NAVY, ec=NAVY, alpha=0.72, zorder=6))
        ax.text(sx + sw + pad, sy, txt, ha="left", va="center", fontsize=10,
                color=NAVY, zorder=7)
        sx += sw + pad + tw(fig, txt, 10) + gap
    assert sx - gap <= 1.0, "形狀圖例超出畫布"

    # ---------------- 圖例:顏色四階 + 斜線紋(置中一列,AI 主體排第一) ----------------
    total = sum(sw + pad + tw(fig, t, f, w) for _c, _a, _h, t, f, w in COLOR_LEGEND) \
        + gap * (len(COLOR_LEGEND) - 1)
    lx, ly = (1.0 - total) / 2.0, 0.058
    assert lx > 0.0, "顏色圖例超出畫布"
    for col, al, hat, txt, fs, wt in COLOR_LEGEND:
        is_ai = (fs == 11)
        hh = 0.013 if is_ai else 0.010
        ax.add_patch(Rectangle((lx, ly - hh), sw, hh * 2.0, fc=col,
                               ec=ORANGE_DARK if is_ai else ("white" if hat else col),
                               lw=1.6 if is_ai else 0.0, hatch=hat, alpha=al,
                               zorder=6))
        ax.text(lx + sw + pad, ly, txt, ha="left", va="center", fontsize=fs,
                color=ORANGE_DARK if is_ai else NAVY, fontweight=wt, zorder=7)
        lx += sw + pad + tw(fig, txt, fs, wt) + gap

    assert_min_fontsize(fig)
    n = assert_no_text_overlap(fig)
    print("  文字物件 %d 個,兩兩無重疊" % n)
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
        "初步拆解顯示 AI 可處理段(找證據 + 判讀)佔全程約六成;"
        "該拆解為營運端的初步估計,W1-6 要交的是可稽核的版本。",
        "G2 · W12 三方比較門:在同一凍結評估集上同時比三組:①現行影像模型 ②規則式脈絡基線 "
        "③地端 VLM 事件判讀。成功條件:誤報改善達預註冊門檻,且漏放率信賴區間不惡化。"
        "本門只能調整模型的假設與規模,不能取消實驗。"
        "三方結構、凍結評估集、預註冊門檻與不可取消實驗四項一字不動(裁決 K);"
        "本輪只升級第三組的技術主體,規則式脈絡基線正式成為地端 VLM 的對照基線。"
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
        # 🔴 這一條在投影片上要用深色粗體印(視覺規格【交付物】E:與 AI 主包的加重一致)
        "WP-E 地端 VLM 事件判讀(對照重訓)—— 本案的 AI 主體:讓機器讀懂一次事件的完整脈絡"
        "(影片 + 客戶問題 + 規則),產出可交付的證據與描述;"
        "W8-12 最小離線試驗 -> W12-24 2x2(有無脈絡特徵 x 乾淨/現況標註),同一冷凍 hold-out"
        "｜交付:三方對照結果(現行影像模型 / 規則式脈絡基線 / 地端 VLM 事件判讀)"
        "+ 有脈絡 vs 無脈絡的對照結果",
        "總投入 4.50 人月不變,係 WP-E 內部人力前移,不增加總人月",
        "WP-F 治理與移交｜交付:移交文件 + 常態儀表板",
    ]),
    ("P9-T4", "圖右側或圖下方右欄 · 「今天 -> 第 26 週」對照四列(欄首標題 + 四列)", [
        "今天 -> 第 26 週",
        "① 判讀依據:人去外面找 -> 地端 VLM 先看片、先把證據與描述整理好,"
        "事件送到人手上時已附證據",
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
