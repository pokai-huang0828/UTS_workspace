# -*- coding: utf-8 -*-
"""P5 用圖:五欄選項卡(成本形狀縮圖)+ G1 因果判定門帶與判定分岔。

規格來源:v4/notes/_v2_parts/P05-07.md **v2.3**  # P5  →  ## 視覺規格
方案升級:v4/notes/16_地端VLM方案升級_裁決與待辦.md(位階最高)
  · 選項 2 由「脈絡+判準+對照重訓」升級為**地端 VLM 事件判讀**,圖上寫成兩模型分工
  · 選項 1 的規則式脈絡層改標成選項 2 的**對照基線**(先後關係,不是二選一)
  · G1 帶右端註記改口徑:2-5 天與 2.5-5.5 天同一營運來源,**不算交叉驗證**(與 P2 同口徑)
畫布裁決:v4/notes/12_出圖稽核與畫布裁決.md  §二 裁決 O
共用機具:v4/scripts/make_figs_v4.py(直接 import,不修改)

紅線:
- 畫布固定 12.2 x 5.7 吋(= 組版內容區的實際形狀,置入縮放比 = 1.0),
  不得為了塞下內容而放大畫布。
- 色值只用 make_figs_v4 的常數(橘 #E8833A / 深藍 #1F4E79),不得出現舊值。
- 圖內最小字級 fs=9,不得下修。
- 圖不畫投影片標題、不畫右上角五格進度指示(由組版程式負責)。
- 負號一律 ASCII hyphen;不用 emoji / 全形減號 / em dash。

🔑 帶狀純文字一律移出圖,由 build_deck_v4.py 以投影片文字框放置(向量、可縮放)。
   本檔把移出的內容完整保留在 SLIDE_TEXT 裡,供組版程式直接 import 使用,
   一個字都沒有刪。圖裡只留「需要圖形關係才講得清楚」的主視覺:
   五條成本曲線(同一組軸才可比)、判決徽章色碼、G1 判定分岔的兩個出口、
   選項 2 -> 選項 3 的關係線、選項 2 的兩模型分工(快 / 準各對一條工作流)。

⚠️ 85% 的三個要件(推估非實測 / 第 12 週凍結測試集驗 / 人現在判得多準沒量過)
   與第四段「這 85% 是分流率」整段移出圖(SLIDE_TEXT 的 P5-T15,fs>=10)。
   **圖內刻意不出現 85% 這個數字** —— 只印數字而不印三個要件正是規格禁止的寫法,
   且圖上也不得與 10.1% 並排。

🔴 2026-08-12 v2.5(依 `notes/21_第五輪裁決_影子模式_v25.md`,位階最高)四處改動:
   1. 裁決 Y-a:選項 0 由 16-23 人改 **17-24 人**;算式框改雙層(先 FTE 容量再無條件進位取員額)
   2. 裁決 Y-c:窄帶(1)由 NT$1,144-2,106 萬改 **NT$1,248-2,223 萬**,增聘 11-18 改 **12-19 人**;
      口徑同步由「可避免的增聘成本」更正為「**增聘成本暴露**」(可避免額是 NT$520-1,521 萬,另一格)
   3. 裁決 AA:圖上兩個具體型號拿掉,改「**一套地端視覺語言模型;篩檢與深挖同一台設備分時處理**」
      —— 順帶消掉 61+72=133GB > 128GB 的硬矛盾(舊寫法隱含兩模型同時常駐)
   4. 裁決 W/X:關鍵事實格由「三組共用凍結評估集 / AI 整理證據,判定仍由人做」
      (**Codex 判 REFUTED 的紅線**)改為「**四臂共用同一份凍結評估集;第四臂為影子模式**」
   🚫 作廢、一個都不得再出現:16-23 人 · 11-18 人 · NT$1,144-2,106 萬 · 60%-64%(含「六成」寫法)·
      Qwen3.5 122B-A10B / Qwen2.5-VL 72B(主片層級)· 「AI 不做判定」「判定仍由人做」· G2「三組」。
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

# ------------------------------------------------------------------ 畫布(鎖死)
W, H = 12.2, 5.7            # 裁決 O:組版內容區的實際形狀,縮放比 = 1.0

# save() 已改成 bbox_inches="tight" + pad_inches=0(裁決 O),tight 的下界是 axes 自己的框。
# 所以 axes 要撐滿整張畫布、不再內縮,輸出才是 12.2 x 5.7(縮放比 1.0)。
# 舊版留 0.1 吋內縮是為了補償 matplotlib 預設的 pad 0.1,那個補償現在會反過來吃掉 0.2 吋
# (實測舊輸出是 12.0 x 5.5),故歸零。座標本來就是「整張畫布的絕對英吋」,元素位置不受影響。
PAD = 0.0
DX0, DX1 = PAD, W - PAD     # 可畫區(英吋)
DY0, DY1 = PAD, H - PAD
XS, YS = DX1 - DX0, DY1 - DY0

FS_S = 9                    # 小字(軸標籤 / 註記 / 帶內正文)
FS_B = 9                    # 卡片正文(關鍵事實)
FS_M = 10                   # 徽章 / 帶內小標
FS_T = 10                   # 卡片標題
FS_H = 12                   # G1 帶標題

BODY = "#333333"
PAPER = "#FAFAFA"


def X(inch):
    """絕對橫座標(英吋)-> axes 分數。"""
    return (inch - DX0) / XS


def Y(inch):
    """絕對縱座標(英吋)-> axes 分數。"""
    return (inch - DY0) / YS


def XW(d):
    """橫向長度(英吋)-> axes 分數。"""
    return d / XS


def YH(d):
    """縱向長度(英吋)-> axes 分數。"""
    return d / YS


# ------------------------------------------------------------------ 版面(英吋)
# 五欄等寬:算式框移出圖之後,選項 0 就沒有加寬的理由;
# 規格說加寬「不是強調」,所以框一走、寬度就該回到齊平,否則反而變成強調。
COL_L, COL_R = 0.24, 11.96
GAP_IN = 0.10
COL_W_IN = (COL_R - COL_L - 4 * GAP_IN) / 5
COL_X_IN = [COL_L + i * (COL_W_IN + GAP_IN) for i in range(5)]
COL_C_IN = [x + COL_W_IN / 2 for x in COL_X_IN]

CARD_TOP_IN = 5.56
HDR_H_IN = 0.24
MOTIF_Y_IN = 5.23                      # 選項 0 頂條下那行極小字的中心
BADGE_TOP_IN, BADGE_H_IN = 5.09, 0.21
# 縮圖由 1.78 x 2.18 改為 1.78 x 1.78:規格寫的是「約 130x90」的橫向縮圖,舊值反而比規格更瘦高。
# 壓回接近規格的比例後,每張卡片下半多出 0.40 吋 —— 選項 2 的兩模型分工就放在這裡,
# 不必為了塞它去動畫布(裁決 O)。曲線可讀性不受影響:五張仍同尺寸、同軸、同線寬。
PLOT_TOP_IN, PLOT_H_IN = 4.80, 1.78
PLOT_W_IN, YLAB_W_IN = 1.78, 0.34
TICK_Y_IN = 2.91
CAP_TOP_IN = 2.78
KF_TOP_IN, KF_H_IN = 2.16, 0.56
CARD_BOT_IN = 1.56

BAND_TOP_IN, BAND_BOT_IN = 1.04, 0.12
DCX_IN, DCY_IN = COL_C_IN[2], 1.30     # 判定菱形中心
DHW_IN, DHH_IN = 1.15, 0.19            # 菱形半寬 / 半高
REL_X_IN, REL_Y_IN = 8.90, 1.36        # 選項 2 -> 選項 3 關係線

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
    """英數字連寫成一個不可拆的 token;CJK、空白、半形括號各自成 token。"""
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


HANG = "，。；：、）」』〕％,.;:)%"
OPEN = "（「『〔【("


def wrap(s, fs, max1, maxr=None):
    """貪婪換行。max1 / maxr 為英吋。行首不落標點、行尾不落開括號。"""
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
            if cur and tok in OPEN and i + 1 < len(toks):
                if tw(cur + tok + toks[i + 1], fs) > lim:
                    lines.append(cur)
                    cur, lim = "", maxr
                    continue
            cand = cur + tok
            if cur and tw(cand, fs) > lim:
                if tok in HANG:
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


def lh_in(fs, mul=1.36):
    """行高(英吋)。"""
    return fs * mul / 72.0


def draw_lines(ax, x_in, y_top_in, lines, fs, color, ha="left", weight="normal",
               mul=1.36, z=7):
    """由 y_top(英吋)往下逐行畫,回傳畫完後的 y(英吋)。"""
    step = lh_in(fs, mul)
    y = y_top_in
    for ln in lines:
        ax.text(X(x_in), Y(y - step / 2), ln, ha=ha, va="center", fontsize=fs,
                color=color, fontweight=weight, zorder=z)
        y -= step
    return y


def rbox(ax, x_in, y_in, w_in, h_in, fc, ec, lw=1.4, ls="solid", alpha=1.0, z=2,
         r=0.006):
    ax.add_patch(FancyBboxPatch((X(x_in), Y(y_in)), XW(w_in), YH(h_in),
                                boxstyle="round,pad=0,rounding_size=%.4f" % r,
                                fc=fc, ec=ec, lw=lw, ls=ls, alpha=alpha, zorder=z))


# ------------------------------------------------------------------ 成本形狀縮圖
def mini_plot(ax, cx_in, kind):
    """五欄共用同一組軸的小折線圖(同尺寸、同軸範圍、同線寬)。"""
    x0 = cx_in - (YLAB_W_IN + PLOT_W_IN) / 2 + YLAB_W_IN
    yb = PLOT_TOP_IN - PLOT_H_IN

    def PX(u):
        return X(x0 + u * PLOT_W_IN)

    def PY(v):
        return Y(yb + v * PLOT_H_IN)

    # 軸
    ax.plot([PX(0), PX(1)], [PY(0), PY(0)], color=GREY, lw=1.0, zorder=4)
    ax.plot([PX(0), PX(0)], [PY(0), PY(1)], color=GREY, lw=1.0, zorder=4)
    for u in (0.0, 1.0):
        ax.plot([PX(u), PX(u)], [PY(0), PY(0) - YH(0.05)], color=GREY, lw=1.0, zorder=4)

    ax.text(PX(0.015), Y(TICK_Y_IN), "3K", ha="left", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(PX(0.985), Y(TICK_Y_IN), "13K+", ha="right", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(PX(0.5), Y(TICK_Y_IN), "每日事件量", ha="center", va="center",
            fontsize=FS_S, color=GREY, zorder=7)
    ax.text(X(x0 - 0.04), PY(0.95), "高", ha="right", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(X(x0 - 0.04), PY(0.05), "低", ha="right", va="center", fontsize=FS_S,
            color=GREY, zorder=7)
    ax.text(X(x0 - 0.24), PY(0.5), "人工複核工時", ha="center", va="center",
            fontsize=FS_S, color=GREY, rotation=90, zorder=7)

    LW = 2.0
    if kind == 0:                                   # 直線線性上升(紅)
        ax.plot([PX(.03), PX(1)], [PY(.12), PY(.93)], color=RED, lw=LW, zorder=5)

    elif kind == "0b":                              # 線性、斜率略低、中段尖峰被削平
        def base(u):
            return _lin(u, .03, .10, 1.0, .80)
        us = np.linspace(.03, .50, 60)
        vs = np.array([base(u) for u in us])
        vs[(us >= .34) & (us <= .48)] = base(.41)
        ax.plot([PX(u) for u in us], [PY(v) for v in vs], color=ORANGE, lw=LW, zorder=5)
        pk = [(.34, base(.34)), (.41, base(.41) + .30), (.48, base(.48))]
        ax.plot([PX(p[0]) for p in pk], [PY(p[1]) for p in pk],
                color=GREY, lw=1.0, ls=(0, (2, 2)), zorder=4)
        us2 = np.linspace(.50, 1.0, 30)
        ax.plot([PX(u) for u in us2], [PY(base(u)) for u in us2],
                color=GREY, lw=LW, ls=(0, (3, 2)), zorder=5)
        ax.add_patch(FancyArrowPatch((PX(.41), PY(base(.41) + .22)),
                                     (PX(.41), PY(base(.41) + .04)),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=ORANGE_DARK, lw=1.3, zorder=6))

    elif kind == 1:                                 # 整段向下平移一階、之後仍線性
        # 平移點放在前段,後面留一整條長直線 —— 否則會被讀成尖峰而不是「下移一階」
        ax.plot([PX(.03), PX(.20)], [PY(.14), PY(.30)], color=GREEN, lw=LW, zorder=5)
        ax.plot([PX(.20), PX(.20)], [PY(.30), PY(.06)], color=GREEN, lw=LW, zorder=5)
        ax.plot([PX(.20), PX(1)], [PY(.06), PY(.74)], color=GREEN, lw=LW, zorder=5)
        ax.add_patch(FancyArrowPatch((PX(.40), PY(.30)), (PX(.24), PY(.19)),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=GREEN, lw=1.3, zorder=6))

    elif kind == 2:                                 # 前期投入區 + 之後次線性平緩
        ax.add_patch(Rectangle((PX(.03), PY(0)), PX(.33) - PX(.03), PY(1) - PY(0),
                               fc=LIGHT, ec="none", alpha=.55, zorder=3))
        ax.plot([PX(.03), PX(.33)], [PY(.12), PY(.42)], color=NAVY, lw=LW, zorder=5)
        us = np.linspace(.33, 1.0, 60)
        vs = .42 + .18 * ((us - .33) / .67) ** .45
        ax.plot([PX(u) for u in us], [PY(v) for v in vs], color=NAVY, lw=LW, zorder=5)
        ax.text(PX(.18), PY(.68), "前期專案投入", ha="center", va="center",
                fontsize=FS_S, color=GREY, rotation=90, zorder=7)

    elif kind == 3:                                 # 前段空白,中後段灰虛線才開始
        ax.plot([PX(.55), PX(1)], [PY(.28), PY(.52)], color=GREY, lw=LW,
                ls=(0, (3, 2)), zorder=5)
        ax.text(PX(.26), PY(.72), "仍在研擬", ha="center", va="center",
                fontsize=FS_S, color=GREY, zorder=7)


def _lin(x, x0, y0, x1, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


# ------------------------------------------------------------------ 圖內卡片資料
CARDS = [
    dict(title="選項 0 · 加人", kind=0, motif=True,
         badge=("拒絕", RED, "white", RED, "solid", 1.2),
         cap="線性:量成長,人力等比成長", cap_c=RED,
         # 明寫斷行點,免得「17-24 人」被拆到兩行
         kf=("以現行做法覆蓋全部既有客戶:\n17-24 人(現有 5 人)", LIGHT, BODY)),
    dict(title="選項 0b · 調班+尖峰人力池", kind="0b", motif=False,
         badge=("待 G1 判定", AMBER, "white", ORANGE_DARK, (0, (3, 2)), 1.6),
         cap="削峰:尖峰徵調的正規化;斜率待 W1-6 量測", cap_c=ORANGE_DARK,
         kf=("最便宜的一條;本案不預先否決它", AMBER, "white")),
    dict(title="選項 1 · 規則式脈絡融合", kind=1, motif=False,
         badge=("先做", GREEN, "white", GREEN, "solid", 1.2),
         cap="83% 同一根因:整段下移一階", cap_c=GREEN,
         # 升級後這一欄多了一個身分:它是選項 2 的對照基線,兩欄是先後關係不是二選一
         kf=("速限資料:自有\n同時是選項 2 的對照基線", GREEN, "white")),
    dict(title="選項 2 · 地端 VLM 事件判讀", kind=2, motif=False,
         badge=("採用", NAVY, "white", NAVY, "solid", 2.4),
         cap="前期專案投入後轉為次線性", cap_c=NAVY,
         # 🔴 2026-08-12 裁決 AA(技術規格降概念層次):圖上不再出現具體型號與量化級別。
         #    舊版寫兩個模型並列,同時隱含「兩模型同時常駐」→ 61+72=133GB > 128GB 的硬矛盾;
         #    改成「一套模型、兩種負載分時處理」後矛盾自然消失,答辯攻擊面也縮小。
         #    具體選型降到附錄層級(SLIDE_TEXT P5-T06 標明「公開技術選型,非公司資訊」)。
         extra=[("一套地端視覺語言模型", NAVY),
                ("篩檢與深挖:同一台設備分時處理", NAVY)],
         # 🔴 2026-08-12 裁決 W/X:舊句「三組共用…AI 整理證據,判定仍由人做」是 Codex 判
         #    REFUTED 的紅線(讀法(i) 下那句話是假的),全片撤除;G2 同步由三組改四臂。
         kf=("四臂共用同一份凍結評估集\n第四臂為影子模式", NAVY, "white")),
    dict(title="選項 3 · 雲端判讀規劃", kind=3, motif=False,
         badge=("前置條件", "white", GREY, GREY, (0, (3, 2)), 1.4),
         cap="仍在研擬:中後段才起步", cap_c=GREY,
         kf=("本案是它的前置條件", LIGHT, BODY)),
]

G1_CELLS = [
    ("格 1  W1-6 要交出什麼",
     "五段時間的量測值:等待 → 找證據 → 判讀 → 內部覆核 → 回信;"
     "兩天逾時率;尖峰到件分布。"),
    ("格 2  怎麼判",
     "把五段分成兩堆:「AI 可處理」(找證據、誤報量、證據包製作)與"
     "「AI 不可處理」(排隊、排班、人力調度)。"),
    ("格 3  判定規則",
     "AI 可處理的那一堆佔主要延遲 → 放行選項 1 / 2 的後段;否則 → 轉選項 0b,"
     "本案的後五個工作包不執行。"),
]
# 🔴 口徑更正(16 號檔 §五 + §六-6):現況 2-5 天與五段拆解合計 2.5-5.5 天出自同一個營運來源,
#    量級相符只說明同一位受訪者前後口述一致,**不算交叉驗證**。舊版本頁寫成「可作為交叉驗證」,
#    與 P2 打架,本輪改成與 P2 同口徑。
#    「合計的 2.5-5.5 天」那個「的」是排版用的:少了它,換行會把「2.5-5.5」和「天」拆到兩行。
G1_NOTE = ("〔注意〕現況 2-5 天與五段拆解合計的 2.5-5.5 天同一營運來源,不算交叉驗證;"
           "AI 可處理段佔 43%-78%、逾時率約半數也都是回憶式估計。"
           "六週買一個答案,不對就不做後面。")


# ==================================================================
# 移出圖、改由 build_deck_v4.py 以投影片文字框放置的內容(逐字保留)
# 位置代號:
#   COL0..COL4 = 五欄卡片正下方對齊該欄的文字欄(圖下方文字區)
#   BAND       = 通欄
# ==================================================================
SLIDE_TEXT = [
    dict(id="P5-T01", slot="COL0", label="選項 0 · 算式框(fs>=10,四列標籤靠左對齊、算式靠左對齊)",
         rows=[("批次", "13,000 x 20 秒 = 72.2 人時"),
               ("爭議", "13,000 x 5-10% x 5.25 分 = 56.8-113.7 人時"),
               # 🔴 2026-08-12:算式框改雙層。舊版單層寫「/ 8 小時 = 16-23 人」,
               #    但 129.1/8 = 16.14,對不上卡片上的 17 —— 少了「無條件進位」那一步。
               ("合計", "129.1-185.9 人時 / 8 小時 = 16.14-23.24 FTE 容量"),
               ("", "→ 取整員額 17-24 人(保產能只能無條件進位;現有 5 人)"),
               ("工作量比", "129.1 / 29.8 = 4.33 倍,這就是「四倍以上」的算術依據")]),
    dict(id="P5-T02", slot="COL0", label="選項 0 · 算式框框底兩行灰字(fs>=9)",
         text=["全客戶每日平均總事件量 13,000+ 筆為雲端伺服器實測統計;人力數為提案推算,非核定編制。",
               "每筆爭議 5.25 分來自那份 1,647 筆判讀的實際節奏(5 人 x 3.6 個分析日 x 8 小時 = 144 人時),"
               "是回推值,不是計時量測值。",
               "本推算沿用兩個尚未驗證的假設:(1) 約 20 秒/筆為營運端的實務估計,尚未以計時量測驗證;"
               "(2) 所有客戶有相同的案件組合與 5-10% 的爭議比例。兩項都由 W1-6 檢驗,結果在 G1 上桌;"
               "若任一項被推翻,17-24 人這個數字要重算。"]),
    dict(id="P5-T03", slot="COL0", label="選項 0 · 三行要點",
         text=["做什麼:增聘複核人力,以現行做法覆蓋全部既有客戶。",
               "成本形狀:線性上升,事件量成長多少,人力就成長多少。",
               "為什麼:加人會讓迴路轉得更久,不會讓它停:裝機量成長 → 複核量成長 → 人力吃緊 → "
               "標註品質不穩 → 回流訓練資料不穩 → 誤報降不下來 → 複核量繼續成長。",
               "(Sambasivan et al., 2021)"]),
    dict(id="P5-T04", slot="COL1", label="選項 0b · 三行要點(規格明訂:任何情況下不得縮字或省略)",
         text=["做什麼:重排班表把人力挪到尖峰時段 + 建一個可調用的尖峰人力池"
               "(含目前尖峰徵調的 7 位研發工程師,使其從臨時徵調變成有編組、有訓練的正式安排)",
               "成本形狀:線性,但斜率低於選項 0;可削掉尖峰,削不掉每日底量。"
               "〔注意〕斜率與削峰幅度目前沒有量測。",
               "為什麼不夠(三個實務理由,均為營運端自陳,尚未量化):"
               "(1) 新進複核人員約需三個月才判得準,尖峰人力池無法臨時擴張,調得到人不等於調得到判準;"
               "(2) 行車影像有隱私限制,判讀工作不能外包給外部人力,人力池只能在內部湊;"
               "(3) 過去試過臨時增援,判準反而更不一致,等於把選項 1 / 2 要解的標註品質問題放大。",
               "另有一條時間上的理由:一件爭議的初步時間拆解顯示,"
               "AI 可處理的兩段(找證據 0.5 天 + 判讀 1-3 天)佔全程 2.5-5.5 天的 43%-78%,"
               "而排隊本身只有 0-1 天。排班動得到的是排隊那一段,動不到那兩段。"
               "〔注意〕這份拆解是回憶式估計,不是計時量測;確認它正是 G1 要做的事,"
               "所以本案仍把 0b 列為正式選項,不預先否決。"]),
    dict(id="P5-T05", slot="COL2", label="選項 1 · 三行要點 + 對照基線那一句",
         text=["做什麼:定位 + 地圖速限硬規則比對,不用機器學習。",
               "成本形狀:整段向下平移一階後仍線性;基準線一次降下來。",
               "為什麼:某小型車隊單月樣本的誤報 103 / 124 = 83% 同一根因,而速限資料自有。",
               "它同時是選項 2 的對照基線:要證明地端模型有增量,得先有一個不用它的基準。"
               "所以選項 1 與選項 2 是先後關係,不是二選一。"]),
    dict(id="P5-T06", slot="COL3",
         label="選項 2 · 三行要點 + 前置關係 + 價值傳導鏈 + 技術選型分工 + G2 段",
         text=["做什麼:地端視覺語言模型(VLM)事件判讀:讓機器讀懂一次事件的完整脈絡"
               "(影片 + 客戶問題 + 規則),產出可交付的描述與證據包。",
               "成本形狀:前段一塊前期專案投入,之後轉為次線性平緩。",
               "前置關係(這一行不得省,它是本頁最重要的邏輯):量測底座 = 評估基準,"
               "沒有它不知道模型判得對不對;判準統一 = 驗證資料,判準不一致的標註餵給模型"
               "就是垃圾進垃圾出;規則式脈絡層 = 對照基線,要證明模型有增量得先有一個不用它的基準。"
               "所以前六週不是流程改善,是評估地端 AI 的必要前置。",
               "價值傳導鏈:誤報下降 → 每日批次複核量下降 → 單筆判讀變快 → 交付時效縮短。",
               # 🔴 2026-08-12 裁決 AA:技術規格降到概念層次(兌現對 Jiwei Guan 的說法)。
               #    具體型號與量化級別降為附錄層級的一句,並標明「公開技術選型,非公司資訊」。
               "技術架構寫到概念層次:一套地端視覺語言模型;篩檢(每日全量初篩)與"
               "深挖(客戶爭議判讀)兩種負載由同一台設備分時處理 —— "
               "兩者正好對應現有兩條工作流(20 秒批次 / 5.25 分深挖);地端設備一台起步。"
               "實際選型與量化規格於 G1 依 W1-6 的量測定案。",
               "吞吐量落點:1,000 支 15 秒 720P 約 10-16 分〔估算,非實測;"
               "同一批影片人以 1.0 倍速看完約 250 分〕。"
               "依一組公開可得模型的公開吞吐特性推估,實際數值於 G1 定案。"
               "(附錄層級的公開技術選型、非公司資訊:試算所依據的是 Qwen3.5 122B-A10B 級"
               "與 Qwen2.5-VL 72B 級的公開吞吐數據。)",
               # 🔴 2026-08-12 裁決 W:G2 由三組改四臂,第四臂 = 影子模式。
               #    舊版三組全部含人,而要部署的是無人系統 —— 一臂都沒在測它。
               "離線模型試驗(WP-E)提前到 W8-12;G2(第 12 週)以同一份凍結評估集"
               "同時比四臂:(1) 現行影像模型 (2) 規則式脈絡基線 (3) 人機協作(機器輔助、人判定)"
               "(4) 影子模式 —— 機器自己結案但不對外送,人照常逐筆判,兩邊比對。"
               "第四臂是唯一算得出「自動結案漏放率」的設計。"
               "通過條件:人機判定品質不劣於現況(自動結案桶與人工桶的漏放率差值,其 95% 信賴區間"
               "上界不得超過 G1 事前預註冊的非劣性邊際 δ),且人工觸碰時間與 P90 回覆時間"
               "達預註冊門檻。G2 只能調整模型假設與規模,不能取消這個實驗;要不要部署由 G3 決定 —— "
               "而「自動結案要不要對外開啟」不由 G2、也不由 G3 決定,它需要移交後一道獨立的門,"
               "不在本次請求範圍。"]),
    dict(id="P5-T15", slot="COL3",
         label="🔴 選項 2 · 卡片下緣【第一個】框 = 準確率口徑框(白底、深灰 1px 外框,"
               "字級不得低於 fs=10;四段整段照印,不得縮寫、不得只留其中兩段;"
               "第五行為紅字警語,字級與③④同級,不得縮成灰色小字)",
         # 🔴 2026-08-12 全面改寫(裁決 W / X / 讀法(i)):
         #    ① 85% 由「描述準確率」改為「機器有把握、可直接結案的爭議件比例」,
         #       並當場加上本案六個月的對外自動結案覆蓋率 = 0%(影子模式)。
         #    ④ 舊句「AI 不做判定 / 判定還是人做的」是 Codex 判 REFUTED 的紅線,全片撤除。
         text=["① 以現行小模型的表現外推,預期約 85% 的爭議件,機器有把握、可直接結案 —— "
               "1,000 筆進來約 850 筆,剩約 150 筆送人細看〔提案推估,非實測〕。"
               "🔴 本案六個月內的對外自動結案覆蓋率目標 = 0%。",
               "② 這個數字要不要成立,由第十二週用同一份凍結測試集驗。",
               "③ 而人現在判得多準,我們沒有量過;所以我也不知道 85% 是進步還是退步,"
               "那正是第一個工作包要建的東西。",
               "④ 這 85% 是分流率:它決定「這筆要不要人細看」,不是「這筆是不是誤報」。"
               "機器對那 850 筆做出的是結案判定 —— 但這六個月它不對外生效。"
               "影子期機器照出結論、不對外送,人照常逐筆判 —— 只是他不用再花半天"
               "去把證據找出來。15% 會描述錯,所以設計上人仍須覆核:五位分析人員不是被裁掉,"
               "是從逐筆看片變成處理難題與治理(這一條在倫理頁是同一句話)。",
               "〔紅字警語〕85% 是可自動結案的比例(移交後上限目標),現有 10.1% 是偵測誤報率,"
               "兩者量的不是同一件事,"
               "不可比、不可並排、不可相減。本頁不得把這兩個數字放在同一張圖或同一行上。"]),
    dict(id="P5-T07", slot="COL3", label="選項 2 · 卡片下緣【第二個】框,淺藍小框"
                                        "(底色 #2E75B6 16% 透明,字色 #1F4E79)",
         text=["這一軌買的不是那二十筆誤報。它買兩件事:第一,判準不一致會直接變成訓練標籤,"
               "污染的是整個模型;第二,這一類判定會進到駕駛考核,判錯的成本落在人身上,不落在報表上。"]),
    dict(id="P5-T08", slot="COL4", label="選項 3 · 三行要點",
         text=["做什麼:公司既有的雲端判讀規劃,目前仍在研擬。",
               "成本形狀:前段完全空白,中後段才以灰虛線起步。",
               "為什麼:雲端判定真假,誰判定雲端?本案是它的前置條件,不是競爭關係。"]),
    dict(id="P5-T09", slot="BAND", label="三條策略窄帶 · 標題(淺灰底通欄,三等分)",
         text=["三條策略,各自的量化落點"]),
    dict(id="P5-T10", slot="BAND", label="三條策略窄帶 · 第 1 格「(1) 脈絡特徵工程」",
         text=["靶心是某小型車隊單月樣本中 103 / 124 = 83% 的同一根因;對應以現行做法覆蓋全部既有客戶時,"
               "每年的增聘成本暴露 NT$1,248-2,223 萬〔提案推算〕。"
               "此為不做本案時的年度增聘成本暴露,非本案承諾的節省額。",
               "算式:增聘 12-19 人 x 年薪量級 x 間接費率。以公開薪資量級推算,非核定預算。",
               "職類已確認:要增聘的複核人員本身就是初階工程師,薪資水準與所採用的公開量級相當,"
               "原先「職類可能有落差」的保留可以撤銷。但這仍是公開薪資量級、不是核定編制與預算,"
               "只能當量級看;實際薪資結構由業務負責人於 G1 前確認。"
               "確認結果會改變這一格的數字,不改變選項的排序。",
               "〔提案推算〕"]),
    dict(id="P5-T11", slot="BAND", label="三條策略窄帶 · 第 2 格「(2) 標註品質」",
         text=["現況複核者一致性未量測,本案從零建立;量化目標為一致性達到設定門檻。",
               "它同時是地端 VLM 的驗證資料:判準不一致的標註拿去驗模型,"
               "量出來的準確率本身就不可信。",
               "這是 VLM 判讀結果能不能進入部署的前提,不是能不能做這個實驗的前提:"
               "實驗自 W8 起跑,G2 只調整假設與規模、不得取消,G3 才決定是否部署(G3 放行條件)。",
               "〔提案目標〕"]),
    dict(id="P5-T12", slot="BAND", label="三條策略窄帶 · 第 3 格「(3) 爭議回覆自動化」",
         text=["單件客戶爭議回覆時效基準 2-5 天 → 目標 2 天內、單純案件當天。",
               "〔提案目標〕"]),
    dict(id="P5-T13", slot="BAND", label="競爭地位帶(深藍 #1F4E79 底、白字,單段落通欄)",
         text=["競爭者用更貴的車上算力換更準的初判。他們買得到算力,買不到我們每天上萬筆"
               "已經被人判過的判定回饋,那是我們這個架構的副產品。"
               "本案要做的,是把這批回饋從一次性專案變成常設、可稽核的量測資產。硬體買得到,這個買不到。"]),
    dict(id="P5-T14", slot="BAND", label="頁腳引文條(淺灰底通欄,左句右引文)",
         text=["設計指引:利害關係人需要完全透明時,規則式可能更優 · 不要為了可以用 AI 而用 AI",
               "(Rudin, 2019)"]),
]


# ------------------------------------------------------------------ 主建圖
def build():
    fig, ax = newfig(W, H)
    # axes 撐滿整張畫布;白底 Rectangle 把 tight 裁切框釘死,輸出即 12.2 x 5.7
    ax.set_position([DX0 / W, DY0 / H, XS / W, YS / H])
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec="none", zorder=0))

    # ============ 五欄卡片 ============
    for i, c in enumerate(CARDS):
        x, w = COL_X_IN[i], COL_W_IN
        cx = COL_C_IN[i]
        hot = (i == 3)
        rbox(ax, x, CARD_BOT_IN, w, CARD_TOP_IN - CARD_BOT_IN,
             fc=(BLUE if hot else PAPER), ec=(NAVY if hot else LIGHT),
             lw=(2.6 if hot else 1.4), alpha=(0.09 if hot else 1.0), z=2)
        if hot:
            rbox(ax, x, CARD_BOT_IN, w, CARD_TOP_IN - CARD_BOT_IN, fc="none",
                 ec=NAVY, lw=2.6, z=6)

        # (1) 頂條
        rbox(ax, x, CARD_TOP_IN - HDR_H_IN, w, HDR_H_IN, fc=NAVY, ec=NAVY, lw=1.0, z=3)
        if c["motif"]:
            # 橘色母題:與 P1 同形狀、同色的人工防線方塊(本頁只出現這一次)
            ms = 0.19
            ax.add_patch(Rectangle((X(x + 0.10), Y(CARD_TOP_IN - HDR_H_IN / 2 - ms / 2)),
                                   XW(ms), YH(ms), fc=ORANGE, ec="white", lw=1.0,
                                   zorder=5))
            ax.text(X(x + 0.10 + ms + 0.07), Y(CARD_TOP_IN - HDR_H_IN / 2), c["title"],
                    ha="left", va="center", fontsize=FS_T, color="white",
                    fontweight="bold", zorder=5)
            ax.text(X(x + 0.10), Y(MOTIF_Y_IN), "這條路是把它放大", ha="left",
                    va="center", fontsize=FS_S, color=ORANGE_DARK, zorder=5)
        else:
            ax.text(X(cx), Y(CARD_TOP_IN - HDR_H_IN / 2), c["title"], ha="center",
                    va="center", fontsize=FS_T, color="white", fontweight="bold",
                    zorder=5)

        # 判決徽章
        btxt, bfc, btc, bec, bls, blw = c["badge"]
        bw = tw(btxt, FS_M) + 0.20
        rbox(ax, cx - bw / 2, BADGE_TOP_IN - BADGE_H_IN, bw, BADGE_H_IN, fc=bfc,
             ec=bec, lw=blw, ls=bls, z=5, r=0.005)
        ax.text(X(cx), Y(BADGE_TOP_IN - BADGE_H_IN / 2), btxt, ha="center",
                va="center", fontsize=FS_M, color=btc, fontweight="bold", zorder=6)

        # (2) 成本形狀縮圖(五欄同尺寸、同軸、同線寬)
        mini_plot(ax, cx, c["kind"])

        # (3) 形狀說明(緊貼縮圖,是曲線的圖說,不是帶狀文字)
        y_cur = draw_lines(ax, cx, CAP_TOP_IN, wrap(c["cap"], FS_S, w - 0.16),
                           FS_S, c["cap_c"], ha="center", z=5)

        # (3b) 選項 2 專屬:兩模型分工。這是「哪個模型接哪條工作流」的對應關係,
        #      不是帶狀敘述文字,所以留在圖裡;完整的量化級別與吞吐量估算在 SLIDE_TEXT。
        for txt, col in c.get("extra", []):
            y_cur = draw_lines(ax, cx, y_cur - 0.04, wrap(txt, FS_S, w - 0.16),
                               FS_S, col, ha="center", weight="bold", z=5)

        # (4) 底部關鍵事實(色碼與徽章同一套語意,靠位置與底色說話)
        kft, kfc, kftc = c["kf"]
        rbox(ax, x + 0.05, KF_TOP_IN - KF_H_IN, w - 0.10, KF_H_IN, fc=kfc, ec=kfc,
             lw=1.0, z=5, r=0.005)
        kl = wrap(kft, FS_B, w - 0.20)
        ax.text(X(cx), Y(KF_TOP_IN - KF_H_IN / 2), "\n".join(kl), ha="center",
                va="center", fontsize=FS_B, color=kftc, fontweight="bold",
                zorder=6, linespacing=1.3)

    # ============ 選項 2 -> 選項 3 關係線 ============
    ax.plot([X(REL_X_IN), X(REL_X_IN)], [Y(CARD_BOT_IN), Y(REL_Y_IN)],
            color=NAVY, lw=1.6, zorder=3)
    ax.plot([X(REL_X_IN), X(COL_C_IN[4])], [Y(REL_Y_IN), Y(REL_Y_IN)],
            color=NAVY, lw=1.6, zorder=3)
    ax.add_patch(FancyArrowPatch((X(COL_C_IN[4]), Y(REL_Y_IN)),
                                 (X(COL_C_IN[4]), Y(CARD_BOT_IN - 0.02)),
                                 arrowstyle="-|>", mutation_scale=13, color=NAVY,
                                 lw=1.6, zorder=3))
    ax.text(X((REL_X_IN + COL_C_IN[4]) / 2), Y(REL_Y_IN + 0.05),
            "提供可稽核的量測與乾淨標註", ha="center", va="bottom", fontsize=FS_S,
            color=NAVY, zorder=7)

    # ============ G1 因果判定門帶 ============
    rbox(ax, COL_L, BAND_BOT_IN, COL_R - COL_L, BAND_TOP_IN - BAND_BOT_IN,
         fc="white", ec=NAVY, lw=2.0, z=3, r=0.005)
    ax.text(X(0.42), Y(BAND_TOP_IN - 0.17), "G1(第 6 週)", ha="left", va="center",
            fontsize=FS_H, color=NAVY, fontweight="bold", zorder=7)
    ax.text(X(0.42), Y(BAND_TOP_IN - 0.17 - lh_in(FS_H, 1.45)), "= 因果判定門",
            ha="left", va="center", fontsize=FS_H, color=NAVY, fontweight="bold",
            zorder=7)

    # 右端註記加了「不算交叉驗證」那一句,字數變長 -> 三格右界左收 0.35 吋讓出寬度。
    cx0, cx1 = 1.72, 9.05
    cw = (cx1 - cx0 - 2 * GAP_IN) / 3
    for j, (t, b) in enumerate(G1_CELLS):
        gx = cx0 + j * (cw + GAP_IN)
        rbox(ax, gx, BAND_BOT_IN + 0.04, cw, BAND_TOP_IN - BAND_BOT_IN - 0.08,
             fc=PAPER, ec=LIGHT, lw=1.0, z=4, r=0.004)
        ax.text(X(gx + 0.07), Y(BAND_TOP_IN - 0.17), t, ha="left", va="center",
                fontsize=FS_M, color=NAVY, fontweight="bold", zorder=5)
        draw_lines(ax, gx + 0.07, BAND_TOP_IN - 0.30,
                   wrap(b, FS_S, cw - 0.14), FS_S, BODY, z=5)

    ax.text(X(9.15), Y(BAND_TOP_IN - 0.17), "為什麼要買這六週", ha="left",
            va="center", fontsize=FS_M, color=NAVY, fontweight="bold", zorder=7)
    draw_lines(ax, 9.15, BAND_TOP_IN - 0.30, wrap(G1_NOTE, FS_S, 11.90 - 9.15),
               FS_S, GREY, mul=1.22)

    # ============ 判定分岔:菱形 + 兩條同粗同樣清楚的箭頭 ============
    ax.plot([X(DCX_IN), X(DCX_IN)], [Y(BAND_TOP_IN), Y(DCY_IN - DHH_IN)],
            color=NAVY, lw=1.6, zorder=3)
    ax.add_patch(Polygon([[X(DCX_IN), Y(DCY_IN + DHH_IN)],
                          [X(DCX_IN + DHW_IN), Y(DCY_IN)],
                          [X(DCX_IN), Y(DCY_IN - DHH_IN)],
                          [X(DCX_IN - DHW_IN), Y(DCY_IN)]],
                         closed=True, fc="white", ec=NAVY, lw=1.8, zorder=5))
    ax.text(X(DCX_IN), Y(DCY_IN), "主要延遲在哪一堆?", ha="center", va="center",
            fontsize=FS_S, color=NAVY, fontweight="bold", zorder=6)

    # 左:轉向選項 0b(橘,人力成本語意)
    ax.plot([X(DCX_IN - DHW_IN), X(COL_C_IN[1])], [Y(DCY_IN), Y(DCY_IN)],
            color=ORANGE, lw=2.0, zorder=4)
    ax.add_patch(FancyArrowPatch((X(COL_C_IN[1]), Y(DCY_IN)),
                                 (X(COL_C_IN[1]), Y(CARD_BOT_IN - 0.02)),
                                 arrowstyle="-|>", mutation_scale=14, color=ORANGE,
                                 lw=2.0, zorder=4))
    ax.text(X((DCX_IN - DHW_IN + COL_C_IN[1]) / 2), Y(DCY_IN + 0.04),
            "轉向:選項 0b", ha="center", va="bottom", fontsize=FS_S,
            color=ORANGE_DARK, fontweight="bold", zorder=7)

    # 右:放行選項 1 / 2(深藍)
    ax.plot([X(DCX_IN + DHW_IN), X(COL_C_IN[3])], [Y(DCY_IN), Y(DCY_IN)],
            color=NAVY, lw=2.0, zorder=4)
    ax.add_patch(FancyArrowPatch((X(COL_C_IN[3]), Y(DCY_IN)),
                                 (X(COL_C_IN[3]), Y(CARD_BOT_IN - 0.02)),
                                 arrowstyle="-|>", mutation_scale=14, color=NAVY,
                                 lw=2.0, zorder=4))
    ax.text(X((DCX_IN + DHW_IN + COL_C_IN[3]) / 2), Y(DCY_IN + 0.04),
            "放行:選項 1 / 2", ha="center", va="bottom", fontsize=FS_S,
            color=NAVY, fontweight="bold", zorder=7)

    assert_min_fontsize(fig)
    return fig


# ------------------------------------------------------------------ 出圖前稽核
def audit(fig):
    """① 所有 Text 落在可畫區內 ② 所有 Text 兩兩 bbox 不重疊。"""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    dpi = fig.dpi

    items = []
    for t in fig.findobj(Text):
        s = t.get_text()
        if not s or not s.strip():
            continue
        bb = t.get_window_extent(r)
        items.append((s.replace("\n", " / ")[:30],
                      bb.x0 / dpi, bb.x1 / dpi, bb.y0 / dpi, bb.y1 / dpi))

    TOL = 0.01                     # 英吋:字型 bbox 含上下伸部,留一點容差
    out = [it[0] for it in items
           if it[1] < DX0 - TOL or it[2] > DX1 + TOL
           or it[3] < DY0 - TOL or it[4] > DY1 + TOL]
    print("  超出可畫區的文字:", out if out else "無")

    # 容器框:五張卡片 + G1 判定門帶 + 兩者之間的分岔區。每個文字必須整個落在其中一個裡面。
    boxes = [(COL_X_IN[i], COL_X_IN[i] + COL_W_IN, CARD_BOT_IN, CARD_TOP_IN)
             for i in range(5)]
    boxes.append((COL_L, COL_R, BAND_BOT_IN, BAND_TOP_IN))          # G1 帶
    boxes.append((COL_L, COL_R, BAND_TOP_IN, CARD_BOT_IN))          # 分岔區
    esc = [it[0] for it in items
           if not any(it[1] >= bx0 - TOL and it[2] <= bx1 + TOL
                      and it[3] >= by0 - TOL and it[4] <= by1 + TOL
                      for bx0, bx1, by0, by1 in boxes)]
    print("  跑出容器框的文字:", esc if esc else "無")
    assert not esc, "有文字跑出容器框:%s" % esc

    bad = []
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            A, B = items[a], items[b]
            ox = min(A[2], B[2]) - max(A[1], B[1])
            oy = min(A[4], B[4]) - max(A[3], B[3])
            if ox > TOL and oy > TOL:
                bad.append((A[0], B[0], round(ox, 3), round(oy, 3)))
    print("  文字兩兩重疊:", "無" if not bad else bad[:10])
    print("  文字物件數:", len(items))
    assert not out, "有文字超出可畫區:%s" % out
    assert not bad, "有文字互相重疊:%s" % bad[:10]


def dump_slide_text():
    print("\n  === 移出圖、交給 build_deck_v4.py 放的文字(逐字保留)===")
    n = 0
    for b in SLIDE_TEXT:
        print("  [%s] %s / %s" % (b["id"], b["slot"], b["label"]))
        for ln in b.get("text", []):
            n += len(ln)
        for lab, expr in b.get("rows", []):
            n += len(lab) + len(expr)
    print("  共 %d 塊,合計 %d 字。" % (len(SLIDE_TEXT), n))


if __name__ == "__main__":
    f = build()
    audit(f)
    save(f, "fig_v4_05")
    dump_slide_text()
