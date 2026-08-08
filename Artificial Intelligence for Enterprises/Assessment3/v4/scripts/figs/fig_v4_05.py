# -*- coding: utf-8 -*-
"""P5 用圖:五欄選項卡 + 成本形狀縮圖 + G1 因果判定門帶 + 三條策略窄帶 + 競爭地位帶。

規格來源:v4/notes/04_十頁內容_v2.md  # P5 · 五條路,含三條不用 AI  →  ## 視覺規格
共用機具:v4/scripts/make_figs_v4.py(直接 import,不修改)

紅線:
- 色值只用 make_figs_v4 的常數(橘 #E8833A / 深藍 #1F4E79),不得出現舊值。
- 圖內最小字級 fs=9。
- 圖不畫投影片標題、不畫右上角五格進度指示(由組版程式負責)。
- 負號一律 ASCII hyphen;不用 emoji / 全形減號 / em dash。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from make_figs_v4 import (  # noqa: E402
    NAVY, ORANGE, ORANGE_DARK, RED, GREY, LIGHT, AMBER, GREEN, BLUE,
    save, newfig, assert_min_fontsize,
)
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch  # noqa: E402
from matplotlib.text import Text  # noqa: E402

# ------------------------------------------------------------------ 版面常數
W, H = 20.0, 11.25          # 16:9
FS_S = 9                    # 小字(說明 / 註記)
FS_B = 9                    # 卡片正文
FS_M = 10                   # 徽章 / 算式框 / 競爭地位帶
FS_T = 11                   # 卡片標題 / 帶內小標
FS_H = 12                   # G1 帶標題

BODY = "#333333"
PAPER = "#FAFAFA"

# 五欄:選項 0 佔 24%,其餘四欄各 19%(欄間留白)
X_L, X_R = 0.020, 0.980
GAP = 0.008
_usable = (X_R - X_L) - 4 * GAP
COL_W = [0.24 * _usable, 0.19 * _usable, 0.19 * _usable, 0.19 * _usable, 0.19 * _usable]
COL_X = []
_x = X_L
for _w in COL_W:
    COL_X.append(_x)
    _x += _w + GAP
COL_C = [COL_X[i] + COL_W[i] / 2 for i in range(5)]

CARD_TOP, CARD_BOT = 0.988, 0.452
HDR_H = 0.034
BADGE_Y, BADGE_H = 0.906, 0.026
PLOT_TOP, PLOT_H = 0.896, 0.070
PLOT_W, YLAB_W = 0.093, 0.019
TICK_Y = 0.8165
CAP_Y = 0.7985
TEXT_TOP = 0.7875
KF_Y, KF_H = 0.458, 0.030
TEXT_FLOOR = KF_Y + KF_H + 0.006

BAND_TOP = 0.374          # G1 帶上緣
BAND_BOT = 0.268
STRAT_TOP, STRAT_BOT = 0.262, 0.090
COMP_TOP, COMP_BOT = 0.084, 0.034
FOOT_TOP, FOOT_BOT = 0.029, 0.002

WIDE = "→←↑↓※"


# ------------------------------------------------------------------ 文字工具
def tw(s, fs):
    """回傳字串寬度(英吋)。CJK = 1 em,ASCII 約 0.55 em。"""
    u = 0.0
    for ch in s:
        if ch in WIDE or ord(ch) >= 0x2E80:
            u += 1.0
        else:
            u += 0.55
    return u * fs / 72.0


def _tokens(s):
    """英數字連寫成一個不可拆的 token;CJK、空白、半形括號各自成 token。

    半形括號要獨立出來,行首行尾的括號規則才管得到它;
    但半形逗號不獨立(否則 13,000 會被拆行)。
    """
    out, buf = [], ""
    for ch in s:
        if ch != " " and ch not in WIDE and ch not in "()" and ord(ch) < 0x2E80:
            buf += ch
        else:
            if buf:
                out.append(buf)
                buf = ""
            out.append(ch)
    if buf:
        out.append(buf)
    return out


# 用碼位寫死,避免全形 / 半形括號在編輯過程被換掉而讓規則失效
HANG = "，。；：、）」』〕％,.;:)%"
OPEN = "（「『〔【("


def wrap(s, fs, max1, maxr=None):
    """貪婪換行。max1 = 第一行可用寬度(英吋),maxr = 其餘行(預設同 max1)。

    兩條中文排版規則:①行首不落標點(懸掛);②行尾不落開括號。
    """
    if maxr is None:
        maxr = max1
    lines = []
    for para in s.split("\n"):
        toks = _tokens(para)
        cur, lim, i = "", max1, 0
        while i < len(toks):
            tok = toks[i]
            if tok == " " and cur == "":
                i += 1
                continue
            # 行尾不落開括號:括號與其後一字綁在一起判斷
            if cur and tok in OPEN and i + 1 < len(toks):
                if tw(cur + tok + toks[i + 1], fs) > lim:
                    lines.append(cur)
                    cur, lim = "", maxr
                    continue
            cand = cur + tok
            if cur and tw(cand, fs) > lim:
                if tok in HANG:                   # 標點懸掛,不另起一行
                    cur = cand
                    i += 1
                    continue
                lines.append(cur)
                cur, lim = ("" if tok == " " else tok), maxr
            else:
                cur = cand
            i += 1
        lines.append(cur)
    return lines


def lh(fs, mul=1.36):
    """行高(y 單位)。"""
    return fs * mul / 72.0 / H


def draw_lines(ax, x, y_top, lines, fs, color, ha="left", weight="normal",
               first_dx=0.0, mul=1.36, z=7):
    """由 y_top 往下逐行畫,回傳畫完後的 y。first_dx 只位移第一行(給標籤留位)。"""
    step = lh(fs, mul)
    y = y_top
    for i, ln in enumerate(lines):
        ax.text(x + (first_dx if i == 0 else 0.0), y - step / 2, ln,
                ha=ha, va="center", fontsize=fs, color=color, fontweight=weight,
                zorder=z)
        y -= step
    return y


def labeled(ax, x, y_top, label, body, fs, max_in, lcolor=NAVY, bcolor=BODY):
    """「標籤:內文」— 標籤深藍粗體,內文接在同一行後面續排。"""
    lw = tw(label, fs) / W
    lines = wrap(body, fs, max_in - tw(label, fs), max_in)
    ax.text(x, y_top - lh(fs) / 2, label, ha="left", va="center",
            fontsize=fs, color=lcolor, fontweight="bold", zorder=7)
    return draw_lines(ax, x, y_top, lines, fs, bcolor, first_dx=lw)


def rbox(ax, x, y, w, h, fc, ec, lw=1.4, ls="solid", alpha=1.0, z=2, r=0.006):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%.4f" % r,
                                fc=fc, ec=ec, lw=lw, ls=ls, alpha=alpha, zorder=z))


# ------------------------------------------------------------------ 成本形狀縮圖
def _lin(x, x0, y0, x1, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def mini_plot(ax, cx, kind):
    """五欄共用同一組軸的小折線圖(同尺寸、同軸、同線寬)。"""
    x0 = cx - (YLAB_W + PLOT_W) / 2 + YLAB_W
    yb = PLOT_TOP - PLOT_H

    def PX(u):
        return x0 + u * PLOT_W

    def PY(v):
        return yb + v * PLOT_H

    # 軸
    ax.plot([PX(0), PX(1)], [PY(0), PY(0)], color=GREY, lw=1.0, zorder=4)
    ax.plot([PX(0), PX(0)], [PY(0), PY(1)], color=GREY, lw=1.0, zorder=4)
    for u in (0.0, 1.0):
        ax.plot([PX(u), PX(u)], [PY(0), PY(0) - 0.004], color=GREY, lw=1.0, zorder=4)
    ax.text(PX(0.02), TICK_Y, "3K", ha="left", va="center", fontsize=FS_S, color=GREY, zorder=7)
    ax.text(PX(0.98), TICK_Y, "13K+", ha="right", va="center", fontsize=FS_S, color=GREY, zorder=7)
    ax.text(PX(0.5), TICK_Y, "每日事件量", ha="center", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(PX(0) - 0.0025, PY(0.94), "高", ha="right", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(PX(0) - 0.0025, PY(0.06), "低", ha="right", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(x0 - 0.0132, PY(0.5), "人工複核工時", ha="center", va="center",
            fontsize=FS_S, color=GREY, rotation=90, zorder=7)

    LW = 1.9
    if kind == 0:                                   # 直線線性上升(紅)
        ax.plot([PX(.03), PX(1)], [PY(.12), PY(.93)], color=RED, lw=LW, zorder=5)

    elif kind == "0b":                              # 線性、斜率略低、中段尖峰被削平
        def base(u):
            return _lin(u, .03, .10, 1.0, .80)
        us = np.linspace(.03, .50, 60)
        vs = np.array([base(u) for u in us])
        vs[(us >= .34) & (us <= .48)] = base(.41)   # 削平的尖峰
        ax.plot([PX(u) for u in us], [PY(v) for v in vs], color=ORANGE, lw=LW, zorder=5)
        pk = [(.34, base(.34)), (.41, base(.41) + .30), (.48, base(.48))]
        ax.plot([PX(p[0]) for p in pk], [PY(p[1]) for p in pk],
                color=GREY, lw=1.0, ls=(0, (2, 2)), zorder=4)
        us2 = np.linspace(.50, 1.0, 30)
        ax.plot([PX(u) for u in us2], [PY(base(u)) for u in us2],
                color=GREY, lw=LW, ls=(0, (3, 2)), zorder=5)
        ax.add_patch(FancyArrowPatch((PX(.41), PY(base(.41)) - .022),
                                     (PX(.41), PY(base(.41)) - .004),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color=ORANGE_DARK, lw=1.2, zorder=6))

    elif kind == 1:                                 # 整段向下平移一階、之後仍線性
        ax.plot([PX(.03), PX(.32)], [PY(.12), PY(.36)], color=GREEN, lw=LW, zorder=5)
        ax.plot([PX(.32), PX(.32)], [PY(.36), PY(.13)], color=GREEN, lw=LW, zorder=5)
        ax.plot([PX(.32), PX(1)], [PY(.13), PY(.70)], color=GREEN, lw=LW, zorder=5)
        ax.add_patch(FancyArrowPatch((PX(.50), PY(.30)), (PX(.35), PY(.245)),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color=GREEN, lw=1.2, zorder=6))

    elif kind == 2:                                 # 前期投入區 + 之後次線性平緩
        ax.add_patch(Rectangle((PX(.03), PY(0)), PX(.33) - PX(.03), PY(1) - PY(0),
                               fc=LIGHT, ec="none", alpha=.55, zorder=3))
        ax.plot([PX(.03), PX(.33)], [PY(.12), PY(.42)], color=NAVY, lw=LW, zorder=5)
        us = np.linspace(.33, 1.0, 60)
        vs = .42 + .18 * ((us - .33) / .67) ** .45
        ax.plot([PX(u) for u in us], [PY(v) for v in vs], color=NAVY, lw=LW, zorder=5)

    elif kind == 3:                                 # 前段空白,中後段灰虛線才開始
        ax.plot([PX(.55), PX(1)], [PY(.28), PY(.52)], color=GREY, lw=LW,
                ls=(0, (3, 2)), zorder=5)


# ------------------------------------------------------------------ 卡片內容
CARDS = [
    dict(
        title="選項 0 · 加人", kind=0, motif=True,
        badge=("拒絕", RED, "white", RED, "solid", 1.2),
        cap="線性:量成長,人力等比成長", cap_c=RED,
        bullets=[
            ("做什麼:", "增聘複核人力,以現行做法覆蓋全部既有客戶。"),
            ("成本形狀:", "線性上升,事件量成長多少,人力就成長多少。"),
            ("為什麼:", "加人會讓迴路轉得更久,不會讓它停:裝機量成長 → 複核量成長 → "
                      "人力吃緊 → 標註品質不穩 → 回流訓練資料不穩 → 誤報降不下來 → 複核量繼續成長。"),
        ],
        cite="(Sambasivan et al., 2021)",
        kf=("以現行做法覆蓋全部既有客戶:15-21 人(現有 5 人)", LIGHT, BODY),
    ),
    dict(
        title="選項 0b · 調班 + 尖峰人力池", kind="0b", motif=False,
        badge=("待 G1 判定", AMBER, "white", ORANGE_DARK, (0, (3, 2)), 1.6),
        cap="削峰:尖峰徵調的正規化;斜率待 W1-6 量測", cap_c=ORANGE_DARK,
        bullets=[
            ("做什麼:", "重排班表把人力挪到尖峰時段 + 建一個可調用的尖峰人力池"
                      "(含目前尖峰徵調的 7 位研發工程師,使其從臨時徵調變成有編組、有訓練的正式安排)"),
            ("成本形狀:", "線性,但斜率低於選項 0;可削掉尖峰,削不掉每日底量。"
                       "〔注意〕斜率與削峰幅度目前沒有量測。"),
            ("為什麼:", "〔待確認〕本案目前沒有實證理由否決這條路。它夠不夠,取決於兩天逾時的時間"
                      "究竟落在排隊與排班,還是落在找證據、誤報量與證據包製作。"
                      "這正是 G1 要判的事,所以這裡不寫結論,寫的是判它的方法。"),
        ],
        cite=None,
        kf=("最便宜的一條;本案不預先否決它", AMBER, "white"),
    ),
    dict(
        title="選項 1 · 規則式脈絡融合", kind=1, motif=False,
        badge=("先做", GREEN, "white", GREEN, "solid", 1.2),
        cap="83% 同一根因:整段下移一階", cap_c=GREEN,
        bullets=[
            ("做什麼:", "定位 + 地圖速限硬規則比對,不用機器學習。"),
            ("成本形狀:", "整段向下平移一階後仍線性;基準線一次降下來。"),
            ("為什麼:", "某小型車隊單月樣本的誤報 103 / 124 = 83% 同一根因,而速限資料自有。"),
        ],
        cite=None,
        kf=("速限資料:自有", GREEN, "white"),
    ),
    dict(
        title="選項 2 · 脈絡 + 判準 + 對照重訓", kind=2, motif=False,
        badge=("採用", NAVY, "white", NAVY, "solid", 2.4),
        cap="前期專案投入後轉為次線性", cap_c=NAVY,
        bullets=[
            ("做什麼:", "規則式脈絡 + 判準一致性 + 以乾淨標註做對照重訓。"),
            ("成本形狀:", "前段一塊前期專案投入,之後轉為次線性平緩。"),
            ("為什麼:", "三者共用同一份凍結評估集,誤報改善與漏放率才能被同一把尺量。"),
            ("價值傳導鏈:", "誤報下降 → 每日批次複核量下降 → 單筆判讀變快 → 交付時效縮短。"),
        ],
        cite=None,
        kf=("三件事共用同一凍結評估集", NAVY, "white"),
    ),
    dict(
        title="選項 3 · 雲端判讀規劃", kind=3, motif=False,
        badge=("前置條件", "white", GREY, GREY, (0, (3, 2)), 1.4),
        cap="仍在研擬:中後段才起步", cap_c=GREY,
        bullets=[
            ("做什麼:", "公司既有的雲端判讀規劃,目前仍在研擬。"),
            ("成本形狀:", "前段完全空白,中後段才以灰虛線起步。"),
            ("為什麼:", "雲端判定真假,誰判定雲端?本案是它的前置條件,不是競爭關係。"),
        ],
        cite=None,
        kf=("本案是它的前置條件", LIGHT, BODY),
    ),
]

FORMULA = [
    ("批次", "13,000 x 20 秒 = 72.2 人時"),
    ("爭議", "13,000 x 5-10% x 4.4 分 = 47.7-95.3 人時"),
    ("合計", "119.9-167.5 人時 / 8 小時 = 15-21 人(現有 5 人)"),
    ("工作量比", "119.9 / 27.7 = 4.33 倍,這就是「四倍以上」的算術依據"),
]
FORMULA_NOTES = [
    "全客戶每日平均總事件量 13,000+ 筆為雲端伺服器實測統計;人力數為提案推算,非核定編制。",
    "本推算沿用兩個尚未驗證的假設:(1) 約 20 秒/筆為營運端的實務估計,尚未以計時量測驗證;"
    "(2) 所有客戶有相同的案件組合與 5-10% 的爭議比例。兩項都由 W1-6 檢驗,結果在 G1 上桌;"
    "若任一項被推翻,15-21 人這個數字要重算。",
]

OPT2_G2 = ("離線模型試驗(對照重訓那一包,WP-E)提前到 W8-12;G2(第 12 週)以同一份凍結評估集"
           "同時比三組:(1) 現行影像模型 (2) 規則式脈絡基線 (3) 脈絡增強的學習模型。"
           "通過條件:誤報改善達預先註冊的門檻,且漏放率的信賴區間不惡化。"
           "G2 只能調整模型假設與規模,不能取消這個實驗;要不要部署由 G3 決定。")
OPT2_BLUE = ("這一軌買的不是那二十筆誤報。它買兩件事:第一,判準不一致會直接變成訓練標籤,"
             "污染的是整個模型;第二,這一類判定會進到駕駛考核,判錯的成本落在人身上,不落在報表上。")

G1_CELLS = [
    ("W1-6 要交出什麼",
     "一件客戶爭議的時間拆解:等待 → 找證據 → 判讀 → 內部覆核 → 回信,五段各佔多少;"
     "兩天逾時率;尖峰到件分布。"),
    ("怎麼判",
     "把五段分成兩堆:「AI 可處理」(找證據、誤報量、證據包製作)與"
     "「AI 不可處理」(排隊、排班、人力調度)。"),
    ("判定規則",
     "AI 可處理的那一堆佔主要延遲 → 放行選項 1 / 2 的後段;否則 → 轉選項 0b"
     "(調班 + 尖峰人力池),本案的後五個工作包不執行。"),
]
G1_NOTE = ("〔注意〕這五段時間目前沒有拆解過,兩天逾時率目前沒有數字。"
           "這正是第一段預算要買的東西:六週買一個答案,答案不對就不做後面。")

STRAT = [
    ("(1) 脈絡特徵工程",
     "靶心是某小型車隊單月樣本中 103 / 124 = 83% 的同一根因;對應以現行做法覆蓋全部既有客戶時,"
     "每年可避免的增聘成本 NT$1,040-1,870 萬〔提案推算〕。"
     "此為不做本案時的年度增聘成本暴露,非本案承諾的節省額。",
     ["以公開薪資量級推算,非核定預算。",
      "〔待確認〕此金額採用的是「一般工程師」的公開薪資量級,而實際要增聘的是「複核分析人員」;"
      "兩者的薪資水準可能有落差,職類確認前這個金額只能當量級看,不得視為定案。"
      "由業務負責人於 G1 前確認職類與薪資尺;確認結果會改變這一格的數字,不改變選項的排序。",
      "〔提案推算〕"]),
    ("(2) 標註品質",
     "現況複核者一致性未量測,本案從零建立;量化目標為一致性達到設定門檻。"
     "這是對照重訓的結果能不能進入部署的前提,不是能不能做這個實驗的前提:"
     "實驗自 W8 起跑,G2 只調整假設與規模、不得取消,G3 才決定是否部署(G3 放行條件)。",
     ["〔提案目標〕"]),
    ("(3) 爭議回覆自動化",
     "單件客戶爭議回覆時效基準 2-5 天 → 目標 2 天內、單純案件當天。",
     ["〔提案目標〕"]),
]

COMPETE = ("競爭者用更貴的車上算力換更準的初判。他們買得到算力,買不到我們每天上萬筆"
           "已經被人判過的判定回饋,那是我們這個架構的副產品。"
           "本案要做的,是把這批回饋從一次性專案變成常設、可稽核的量測資產。硬體買得到,這個買不到。")

FOOT_L = "設計指引:利害關係人需要完全透明時,規則式可能更優 · 不要為了可以用 AI 而用 AI"
FOOT_R = "(Rudin, 2019)"


# ------------------------------------------------------------------ 主建圖
def build():
    fig, ax = newfig(W, H)
    # 讓座標軸鋪滿整張圖:1 個 x 單位 = W 英吋、1 個 y 單位 = H 英吋,
    # 排版全部用英吋算,才不會被 subplot 預設邊界打亂。
    ax.set_position([0, 0, 1, 1])
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="none", zorder=0))
    used = []

    # ============ 五欄卡片 ============
    for i, c in enumerate(CARDS):
        x, w = COL_X[i], COL_W[i]
        cx = COL_C[i]
        hot = (i == 3)
        rbox(ax, x, CARD_BOT, w, CARD_TOP - CARD_BOT,
             fc=(BLUE if hot else PAPER), ec=(NAVY if hot else LIGHT),
             lw=(2.6 if hot else 1.4), alpha=(0.09 if hot else 1.0), z=2)
        if hot:   # 淡藍底是 alpha 疊出來的,外框要再描一次才不會被沖淡
            rbox(ax, x, CARD_BOT, w, CARD_TOP - CARD_BOT, fc="none", ec=NAVY, lw=2.6, z=6)

        # (1) 頂條
        rbox(ax, x, CARD_TOP - HDR_H, w, HDR_H, fc=NAVY, ec=NAVY, lw=1.0, z=3)
        if c["motif"]:
            # 橘色母題:與 P1 同形狀、同色的人工防線方塊(本頁只出現這一次)
            ms = 0.0118
            ax.add_patch(Rectangle((x + 0.006, CARD_TOP - HDR_H / 2 - ms * W / H / 2),
                                   ms, ms * W / H, fc=ORANGE, ec="white", lw=1.0, zorder=5))
            ax.text(x + 0.006 + ms + 0.005, CARD_TOP - HDR_H / 2, c["title"],
                    ha="left", va="center", fontsize=FS_T, color="white", fontweight="bold",
                    zorder=5)
            ax.text(x + 0.006, CARD_TOP - HDR_H - 0.008, "這條路是把它放大",
                    ha="left", va="top", fontsize=FS_S, color=ORANGE_DARK, zorder=5)
        else:
            ax.text(cx, CARD_TOP - HDR_H / 2, c["title"], ha="center", va="center",
                    fontsize=FS_T, color="white", fontweight="bold", zorder=5)

        # 判決徽章
        btxt, bfc, btc, bec, bls, blw = c["badge"]
        bw = tw(btxt, FS_M) / W + 0.014
        rbox(ax, cx - bw / 2, BADGE_Y, bw, BADGE_H, fc=bfc, ec=bec, lw=blw, ls=bls, z=5,
             r=0.005)
        ax.text(cx, BADGE_Y + BADGE_H / 2, btxt, ha="center", va="center",
                fontsize=FS_M, color=btc, fontweight="bold", zorder=6)

        # (2) 成本形狀縮圖(五欄同尺寸、同軸、同線寬)
        mini_plot(ax, cx, c["kind"])
        ax.text(cx, CAP_Y, c["cap"], ha="center", va="center", fontsize=FS_S,
                color=c["cap_c"], zorder=5)

        # (3) 三行要點
        pad = 0.007
        tx = x + pad
        maxin = (w - 2 * pad) * W
        y = TEXT_TOP
        for lab, bod in c["bullets"]:
            y = labeled(ax, tx, y, lab, bod, FS_B, maxin)
            y -= 0.0025
        if c["cite"]:
            ax.text(x + w - pad, y - lh(FS_S) / 2, c["cite"], ha="right", va="center",
                    fontsize=FS_S, color=GREY)
            y -= lh(FS_S)

        # (4) 選項 0 專屬算式框 —— 本頁最重要的一格,完整印出,不縮字
        if i == 0:
            y -= 0.004
            fx, fw = x + 0.002, w - 0.004
            fpad = 0.005
            lab_w = max(tw(l, FS_M) for l, _ in FORMULA) / W + 0.005
            rows = []
            for lab, expr in FORMULA:
                rows.append((lab, wrap(expr, FS_M, (fw - 2 * fpad) * W - lab_w * W)))
            nrow = sum(len(r[1]) for r in rows)
            fh = nrow * lh(FS_M, 1.40) + 2 * fpad
            ax.add_patch(Rectangle((fx, y - fh), fw, fh, fc="white", ec=GREY, lw=1.0,
                                   zorder=5))
            ry = y - fpad
            for lab, ls_ in rows:
                ax.text(fx + fpad, ry - lh(FS_M, 1.40) / 2, lab, ha="left", va="center",
                        fontsize=FS_M, color=NAVY, fontweight="bold", zorder=7)
                for k, ln in enumerate(ls_):
                    ax.text(fx + fpad + lab_w, ry - lh(FS_M, 1.40) / 2, ln, ha="left",
                            va="center", fontsize=FS_M, color=BODY, zorder=7)
                    ry -= lh(FS_M, 1.40)
            y = y - fh - 0.005
            for nt in FORMULA_NOTES:
                y = draw_lines(ax, tx, y, wrap(nt, FS_S, maxin), FS_S, GREY, mul=1.3)
                y -= 0.001

        # 選項 2:價值傳導鏈之後的 G2 段 + 卡片下緣淺藍小框
        if i == 3:
            y = draw_lines(ax, tx, y, wrap(OPT2_G2, FS_B, maxin), FS_B, BODY)
            y -= 0.005
            bpad = 0.005
            bl = wrap(OPT2_BLUE, FS_S, (w - 2 * pad - 2 * bpad) * W)
            bh = len(bl) * lh(FS_S, 1.32) + 2 * bpad
            rbox(ax, x + pad, y - bh, w - 2 * pad, bh, fc=BLUE, ec=BLUE, lw=1.0,
                 alpha=0.16, z=5, r=0.004)
            draw_lines(ax, x + pad + bpad, y - bpad, bl, FS_S, NAVY, mul=1.32)
            y = y - bh

        used.append((c["title"], round((TEXT_FLOOR - y) * H, 3)))

        # (5) 底部關鍵事實
        kft, kfc, kftc = c["kf"]
        rbox(ax, x + 0.004, KF_Y, w - 0.008, KF_H, fc=kfc, ec=kfc, lw=1.0, z=5, r=0.005)
        kl = wrap(kft, FS_B, (w - 0.016) * W)
        ax.text(x + w / 2, KF_Y + KF_H / 2, "\n".join(kl), ha="center", va="center",
                fontsize=FS_B, color=kftc, fontweight="bold", zorder=6, linespacing=1.3)

    # ============ 選項 2 → 選項 3 關係線 ============
    rl_y = 0.390
    ax.plot([0.755, 0.755], [CARD_BOT, rl_y], color=NAVY, lw=1.6, zorder=3)
    ax.plot([0.755, COL_C[4]], [rl_y, rl_y], color=NAVY, lw=1.6, zorder=3)
    ax.add_patch(FancyArrowPatch((COL_C[4], rl_y), (COL_C[4], CARD_BOT - 0.002),
                                 arrowstyle="-|>", mutation_scale=13, color=NAVY,
                                 lw=1.6, zorder=3))
    ax.text((0.755 + COL_C[4]) / 2, rl_y + 0.004, "提供可稽核的量測與乾淨標註",
            ha="center", va="bottom", fontsize=FS_S, color=NAVY, zorder=7)

    # ============ G1 因果判定門帶 ============
    rbox(ax, X_L, BAND_BOT, X_R - X_L, BAND_TOP - BAND_BOT, fc="white", ec=NAVY,
         lw=2.0, z=3, r=0.005)
    ax.text(0.030, BAND_TOP - 0.026, "G1(第 6 週)", ha="left", va="center",
            fontsize=FS_H, color=NAVY, fontweight="bold", zorder=7)
    ax.text(0.030, BAND_TOP - 0.026 - lh(FS_H, 1.45), "= 因果判定門", ha="left",
            va="center", fontsize=FS_H, color=NAVY, fontweight="bold", zorder=7)

    cx0, cx1 = 0.158, 0.780
    cw = (cx1 - cx0 - 2 * GAP) / 3
    for j, (t, b) in enumerate(G1_CELLS):
        gx = cx0 + j * (cw + GAP)
        rbox(ax, gx, BAND_BOT + 0.010, cw, BAND_TOP - BAND_BOT - 0.020, fc=PAPER,
             ec=LIGHT, lw=1.0, z=4, r=0.004)
        ax.text(gx + 0.006, BAND_TOP - 0.028, "格 %d  %s" % (j + 1, t), ha="left",
                va="center", fontsize=FS_T, color=NAVY, fontweight="bold", zorder=5)
        draw_lines(ax, gx + 0.006, BAND_TOP - 0.040,
                   wrap(b, FS_B, (cw - 0.012) * W), FS_B, BODY)

    ax.text(0.790, BAND_TOP - 0.028, "為什麼要買這六週", ha="left", va="center",
            fontsize=FS_T, color=NAVY, fontweight="bold", zorder=7)
    draw_lines(ax, 0.790, BAND_TOP - 0.040, wrap(G1_NOTE, FS_S, (0.972 - 0.790) * W),
               FS_S, GREY)

    # 判定分岔:菱形 + 兩條同粗同樣清楚的箭頭
    dcx, dcy, dhw, dhh = 0.600, 0.412, 0.050, 0.024
    ax.plot([dcx, dcx], [BAND_TOP, dcy - dhh], color=NAVY, lw=1.6, zorder=3)
    ax.add_patch(Polygon([[dcx, dcy + dhh], [dcx + dhw, dcy], [dcx, dcy - dhh],
                          [dcx - dhw, dcy]], closed=True, fc="white", ec=NAVY, lw=1.8,
                         zorder=5))
    ax.text(dcx, dcy, "主要延遲在哪一堆?", ha="center", va="center", fontsize=FS_S,
            color=NAVY, fontweight="bold", zorder=6)

    ax.plot([dcx - dhw, COL_C[1]], [dcy, dcy], color=ORANGE, lw=2.0, zorder=4)
    ax.add_patch(FancyArrowPatch((COL_C[1], dcy), (COL_C[1], CARD_BOT - 0.002),
                                 arrowstyle="-|>", mutation_scale=14, color=ORANGE,
                                 lw=2.0, zorder=4))
    ax.text((dcx - dhw + COL_C[1]) / 2, dcy + 0.009, "轉向:選項 0b", ha="center",
            va="bottom", fontsize=FS_S, color=ORANGE_DARK, fontweight="bold", zorder=7)

    ax.plot([dcx + dhw, COL_C[3]], [dcy, dcy], color=NAVY, lw=2.0, zorder=4)
    ax.add_patch(FancyArrowPatch((COL_C[3], dcy), (COL_C[3], CARD_BOT - 0.002),
                                 arrowstyle="-|>", mutation_scale=14, color=NAVY,
                                 lw=2.0, zorder=4))
    ax.text((dcx + dhw + COL_C[3]) / 2, dcy + 0.009, "放行:選項 1 / 2", ha="center",
            va="bottom", fontsize=FS_S, color=NAVY, fontweight="bold", zorder=7)

    # ============ 三條策略窄帶 ============
    rbox(ax, X_L, STRAT_BOT, X_R - X_L, STRAT_TOP - STRAT_BOT, fc=LIGHT, ec=LIGHT,
         lw=1.0, alpha=0.42, z=2, r=0.005)
    ax.text(0.028, STRAT_TOP - 0.011, "三條策略,各自的量化落點", ha="left", va="center",
            fontsize=FS_T, color=NAVY, fontweight="bold")
    sx0, sx1 = 0.025, 0.975
    sw = (sx1 - sx0 - 2 * GAP) / 3
    for j, (t, b, notes) in enumerate(STRAT):
        gx = sx0 + j * (sw + GAP)
        top = STRAT_TOP - 0.024
        rbox(ax, gx, STRAT_BOT + 0.006, sw, top - STRAT_BOT - 0.004, fc="white",
             ec=LIGHT, lw=1.0, z=3, r=0.004)
        yy = top - 0.008
        ax.text(gx + 0.006, yy - lh(FS_T) / 2, t, ha="left", va="center",
                fontsize=FS_T, color=NAVY, fontweight="bold", zorder=4)
        yy -= lh(FS_T, 1.45)
        yy = draw_lines(ax, gx + 0.006, yy, wrap(b, FS_B, (sw - 0.012) * W), FS_B, BODY)
        yy -= 0.002
        for nt in notes:
            yy = draw_lines(ax, gx + 0.006, yy, wrap(nt, FS_S, (sw - 0.012) * W),
                            FS_S, GREY, mul=1.3)

    # ============ 競爭地位帶 ============
    rbox(ax, X_L, COMP_BOT, X_R - X_L, COMP_TOP - COMP_BOT, fc=NAVY, ec=NAVY, lw=1.0,
         z=3, r=0.005)
    cl = wrap(COMPETE, FS_B, tw(COMPETE, FS_B) / 2 + 0.35)
    ax.text((X_L + X_R) / 2, (COMP_TOP + COMP_BOT) / 2, "\n".join(cl), ha="center",
            va="center", fontsize=FS_B, color="white", zorder=7, linespacing=1.6)

    # ============ 頁腳引文條 ============
    rbox(ax, X_L, FOOT_BOT, X_R - X_L, FOOT_TOP - FOOT_BOT, fc=LIGHT, ec=LIGHT, lw=1.0,
         alpha=0.55, z=2, r=0.004)
    ax.text(0.030, (FOOT_TOP + FOOT_BOT) / 2, FOOT_L, ha="left", va="center",
            fontsize=FS_S, color=BODY, zorder=4)
    ax.text(0.970, (FOOT_TOP + FOOT_BOT) / 2, FOOT_R, ha="right", va="center",
            fontsize=FS_S, color=GREY, zorder=4)

    # ------------- 自我稽核 -------------
    print("  欄位文字用高(英吋,>0 表示超出可用區,需縮排):")
    for t, u in used:
        print("    %-22s 溢出 %+.3f in" % (t, u))
    assert_min_fontsize(fig)
    return fig


def audit(fig):
    """出圖前檢查:所有文字是否落在畫布內。"""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fb = fig.bbox
    bad = []
    for t in fig.findobj(Text):
        if not t.get_text().strip():
            continue
        bb = t.get_window_extent(r)
        if bb.x0 < fb.x0 - 1 or bb.x1 > fb.x1 + 1 or bb.y0 < fb.y0 - 1 or bb.y1 > fb.y1 + 1:
            bad.append(t.get_text()[:28])
    print("  超出畫布的文字:", bad if bad else "無")


if __name__ == "__main__":
    f = build()
    audit(f)
    save(f, "fig_v4_05")
