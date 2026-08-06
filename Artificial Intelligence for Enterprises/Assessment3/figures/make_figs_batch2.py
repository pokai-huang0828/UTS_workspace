# -*- coding: utf-8 -*-
"""A3 投影片圖表 · 第二批(7 張)。承 batch1 的視覺規範。
紅線:不得出現任何未經標示來源的數值。凡提案人設定值一律在圖上標明。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY, RED, GREY = "#1F3864", "#C00000", "#808080"
LIGHT, AMBER, GREEN = "#D9D9D9", "#FFC000", "#548235"

def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", name)

def box(ax, x, y, w, h, text, fc, ec=None, fs=10, tc="white", bold=True, r=.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec or fc, lw=1.5, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal", zorder=4, linespacing=1.5)

# ============================================================
# 1. P2 市占對照(兩個並排數字,不畫趨勢 —— A1 無時間序列資料)
# ============================================================
def fig_market():
    fig, ax = plt.subplots(figsize=(11, 5.4))
    ax.axis("off")
    box(ax, .03, .40, .44, .46, "A$611.5bn", NAVY, fs=40)
    ax.text(.25, .34, "CBA 房貸帳(規模)", ha="center", fontsize=13, color=NAVY, fontweight="bold")
    ax.text(.25, .27, "房貸市占 25.4%(APRA 住房貸款口徑)\nCBA (2025b)",
            ha="center", fontsize=10, color=GREY, linespacing=1.6)
    box(ax, .53, .40, .44, .46, "其中僅  X%\n落在 12 個月內\n固定利率到期窗口", RED, fs=17)
    ax.text(.75, .34, "本案的可尋址曝險", ha="center", fontsize=13, color=RED, fontweight="bold")
    ax.text(.75, .27, "X 待 CBA 內部到期分佈校準", ha="center", fontsize=10, color=GREY)
    ax.add_patch(FancyArrowPatch((.475, .63), (.525, .63), arrowstyle="-|>",
                                 mutation_scale=22, lw=2.4, color=GREY, zorder=5))
    ax.text(.5, .93, "我要談的不是整本帳,是每年滾動到期的那一段",
            ha="center", fontsize=15, color=NAVY, fontweight="bold")
    ax.text(.5, .13,
            "交叉驗證:以 CBA A$611.5bn = 25.4% 反推市場規模約 A$2.41tn;\n"
            "Macquarie A$141.7bn ÷ A$2.41tn = 5.885% ≈ 5.9% —— 兩個市占數字內部一致。",
            ha="center", fontsize=9.5, color=GREY, linespacing=1.7,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F7F7F7", ec=LIGHT))
    ax.set_xlim(0, 1); ax.set_ylim(.05, 1)
    save(fig, "fig02_market")

# ============================================================
# 2. P3 選案加權矩陣熱圖
# ============================================================
def fig_matrix():
    DIM = ["戰略契合\n(25%)", "增量價值\n(20%)", "第一方資料\n完整度(15%)",
           "資料治理\n簡易度(10%)", "監管可行性\n(10%)", "用戶採用\n容易度(10%)",
           "6個月內\n可交付性(10%)"]
    W = np.array([.25, .20, .15, .10, .10, .10, .10])
    CASE = ["A  房貸流失預警與留存", "B  詐騙偵測強化", "C  信貸審批再加速"]
    M = np.array([[5, 5, 3, 2, 2, 2, 3],
                  [3, 2, 5, 4, 4, 4, 4],
                  [3, 2, 5, 4, 3, 4, 4]], dtype=float)
    tot = M @ W
    fig, ax = plt.subplots(figsize=(12.5, 4.6))
    im = ax.imshow(M, cmap="RdYlGn", vmin=1, vmax=5, aspect="auto", alpha=.85)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{int(M[i,j])}", ha="center", va="center",
                    fontsize=15, fontweight="bold", color="#222222")
    ax.set_xticks(range(len(DIM))); ax.set_xticklabels(DIM, fontsize=9.5)
    ax.set_yticks(range(3)); ax.set_yticklabels(CASE, fontsize=11)
    for i, t in enumerate(tot):
        ax.text(len(DIM) - .35, i, f"{t:.3f}", ha="left", va="center",
                fontsize=14, fontweight="bold", color=NAVY if i == 0 else GREY)
    ax.text(len(DIM) - .35, -.72, "加權總分", ha="left", fontsize=10.5,
            color=NAVY, fontweight="bold")
    ax.set_title("三案加權比較(1–5 分,分數越高越好)",
                 fontsize=15, color=NAVY, fontweight="bold", pad=16)
    ax.text(0, 2.95,
            "三案僅差 0.1 分。敏感度顯示七個維度中有六個可在權重 ±50% 內翻轉排序 —— "
            "矩陣本身不足以定案,\n真正的依據是:只有 A 案對應到一個尚無 AI 覆蓋的戰略缺口。"
            "所有權重與評分為提案人設定。",
            fontsize=9.5, color=GREY, va="top", linespacing=1.7)
    ax.set_xlim(-.5, len(DIM) + .45)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "fig03_matrix")

# ============================================================
# 3. P4 系統閉環 + 三條策略
# ============================================================
def fig_loop():
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # 閉環四節點
    nodes = [(.06, .70, .17, .13, "第一方資料\n還款 / 利率差 / 數位互動"),
             (.29, .70, .17, .13, "流失傾向評分\n+ 三個關聯特徵"),
             (.52, .70, .17, .13, "分層\n高 / 中 / 異常"),
             (.75, .70, .19, .13, "三條留存策略\n(見下)")]
    for x, y, w, h, t in nodes:
        box(ax, x, y, w, h, t, NAVY, fs=9.5)
    for i in range(3):
        x0 = nodes[i][0] + nodes[i][2]; x1 = nodes[i + 1][0]
        ax.add_patch(FancyArrowPatch((x0, .765), (x1, .765), arrowstyle="-|>",
                                     mutation_scale=16, lw=1.8, color=GREY, zorder=5))
    # 回饋線
    ax.add_patch(FancyArrowPatch((.845, .69), (.145, .69), arrowstyle="-|>",
                                 mutation_scale=16, lw=1.6, color=GREEN, zorder=5,
                                 connectionstyle="arc3,rad=0.28"))
    ax.text(.5, .565, "回饋:5% 隨機保留組取得無偏標籤;客戶經理推翻理由僅作模型審計,不直接當訓練標籤",
            ha="center", fontsize=9, color=GREEN)
    # 不可觀測盲區
    ax.add_patch(FancyBboxPatch((.29, .87), .17, .09,
                                boxstyle="round,pad=0,rounding_size=.02",
                                fc="#EFEFEF", ec=GREY, lw=1.5, ls="--", zorder=3))
    ax.text(.375, .915, "競品接觸訊號\n不可觀測(已知盲區)", ha="center", va="center",
            fontsize=8.5, color=GREY, zorder=4, linespacing=1.5)
    # 三策略卡
    S = [(.03, "策略一 · 到期前主動利率檢視", NAVY,
          "高分 × 高終身價值\n客戶經理外撥\n停止:增量留存率\n95% CI 下界 ≤ 0 則停"),
         (.355, "策略二 · 數位自助觸達", "#2E75B6",
          "中分群\n自動化利率檢視邀請\n近零邊際成本\n停止:轉換率低於自助基準"),
         (.68, "策略三 · 財務困難分流", GREEN,
          "還款異常但無再融資訊號\n強制轉入 hardship 流程\n不得計入留存業績\n(系統層規則,非人工判斷)")]
    for x, title, col, body in S:
        box(ax, x, .40, .29, .075, title, col, fs=10.5)
        ax.add_patch(FancyBboxPatch((x, .10), .29, .29,
                                    boxstyle="round,pad=0,rounding_size=.02",
                                    fc="#FAFAFA", ec=col, lw=1.5, zorder=3))
        ax.text(x + .145, .245, body, ha="center", va="center", fontsize=9,
                color="#333333", zorder=4, linespacing=1.9)
    ax.text(.5, .035,
            "模型只排順序。是否致電、是否給優惠由客戶經理與定價團隊決定 —— "
            "特徵貢獻反映的是對預測的貢獻,不是因果效果。",
            ha="center", fontsize=9.5, color=RED)
    ax.text(.5, .985, "系統閉環與三條留存策略", ha="center", va="top",
            fontsize=15, color=NAVY, fontweight="bold")
    save(fig, "fig04_loop")

# ============================================================
# 4. P5 可行性評估五維紅黃綠
# ============================================================
def fig_feasibility():
    D = [("資料", "amber", "交易 / 還款 / 數位互動\n皆為既有第一方資料",
          "固定利率到期樣本歷史\n是否 ≥ 24 個月"),
         ("技術", "green", "A2 已驗證方法;CBA 既有交付紀錄\n客服等待 -40%、年審 14h→2h",
          "與既有 CEE 的整合方式\n加模組 vs 另建平台"),
         ("組織", "amber", "既有客戶經理外撥流程可承接\n試點期並行舊制",
          "改動配額規則\n需哪一層簽字"),
         ("監管", "red", "—",
          "差別留存定價是否落入\n監管對自動化決策的期待"),
         ("經濟", "amber", "以損益兩平反解取代\n單點 ROI 宣稱",
          "房貸產品別淨利差\n(內部資料)")]
    COL = {"green": GREEN, "amber": AMBER, "red": RED}
    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    w = .186
    for i, (name, lv, ev, unk) in enumerate(D):
        x = .01 + i * (w + .012)
        ax.add_patch(Circle((x + w / 2, .80), .048, fc=COL[lv], ec="white",
                            lw=2.5, zorder=4, transform=ax.transData))
        ax.text(x + w / 2, .672, name, ha="center", fontsize=13,
                color=NAVY, fontweight="bold")
        ax.add_patch(FancyBboxPatch((x, .36), w, .27,
                                    boxstyle="round,pad=0,rounding_size=.02",
                                    fc="#FAFAFA", ec=LIGHT, lw=1.4, zorder=3))
        ax.text(x + w / 2, .495, ev, ha="center", va="center", fontsize=8.5,
                color="#333333", zorder=4, linespacing=1.8)
        ax.add_patch(FancyBboxPatch((x, .10), w, .22,
                                    boxstyle="round,pad=0,rounding_size=.02",
                                    fc="#FFF6F6" if lv == "red" else "#F7F7F7",
                                    ec=COL[lv] if lv == "red" else LIGHT, lw=1.4, zorder=3))
        ax.text(x + w / 2, .21, unk, ha="center", va="center", fontsize=8.5,
                color="#555555", zorder=4, linespacing=1.8)
    ax.text(.005, .50, "證據", fontsize=10, color=GREY, ha="right", va="center", rotation=90)
    ax.text(.005, .21, "最大未知", fontsize=10, color=GREY, ha="right", va="center", rotation=90)
    ax.text(.5, .965, "可行性評估:本案不需要新建 AI 能力,只需要把既有能力指向新的一軸",
            ha="center", va="top", fontsize=14.5, color=NAVY, fontweight="bold")
    ax.text(.5, .035,
            "go / no-go 門檻:若「資料」維為紅燈,本案順延,先做 6 週資料可行性研究再回委員會。",
            ha="center", fontsize=10, color=RED)
    save(fig, "fig06_feasibility")

# ============================================================
# 5. P8 價值方程式三段結構(不給絕對數值,只給結構與參數來源)
# ============================================================
def fig_value():
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    rows = [
        (.76, "① 年度可尋址曝險(上界)", NAVY,
         [("窗口內平均餘額", "待校準"), ("基準流失率", "待校準"),
          ("房貸產品別淨利差", "待校準"), ("曝險年數", "提案人設定")]),
        (.50, "② 可挽回上限", "#2E75B6",
         [("① 的結果", ""), ("模型 recall", "PoC 0.648"),
          ("增量留存率(實驗組減對照組)", "G5 實測")]),
        (.24, "③ 年度淨效益", GREEN,
         [("② 的結果", ""), ("扣:讓利成本(戶數×bps×餘額)", "待校準"),
          ("扣:外撥營運成本", "提案人設定"), ("扣:年度系統成本", "27.5 人月推估")]),
    ]
    for y, title, col, parts in rows:
        box(ax, .02, y, .235, .13, title, col, fs=11)
        ax.add_patch(FancyArrowPatch((.265, y + .065), (.30, y + .065),
                                     arrowstyle="-|>", mutation_scale=16, lw=1.8,
                                     color=GREY, zorder=5))
        n = len(parts)
        bw = (.66 - (n - 1) * .012) / n
        for k, (p, src) in enumerate(parts):
            x = .31 + k * (bw + .012)
            ax.add_patch(FancyBboxPatch((x, y), bw, .13,
                                        boxstyle="round,pad=0,rounding_size=.015",
                                        fc="#FAFAFA", ec=col, lw=1.3, zorder=3))
            ax.text(x + bw / 2, y + .082, p, ha="center", va="center", fontsize=8.6,
                    color="#333333", zorder=4)
            if src:
                ax.text(x + bw / 2, y + .034, f"[{src}]", ha="center", va="center",
                        fontsize=7.6, color=RED if "待校準" in src else GREY, zorder=4)
    for y in (.70, .44):
        ax.add_patch(FancyArrowPatch((.14, y), (.14, y - .07), arrowstyle="-|>",
                                     mutation_scale=16, lw=1.8, color=GREY, zorder=5))
    ax.add_patch(FancyBboxPatch((.02, .035), .95, .14,
                                boxstyle="round,pad=0,rounding_size=.02",
                                fc="#FFF9E6", ec=AMBER, lw=1.8, zorder=3))
    ax.text(.495, .105,
            "損益兩平反解:在讓利 X bps、系統成本 Y 的假設下,\n"
            "本案 12 個月回本所需的最小增量留存率是 Z pp。",
            ha="center", va="center", fontsize=12.5, color="#7F6000",
            fontweight="bold", zorder=4, linespacing=1.7)
    ax.text(.5, .985, "價值方程式:我不報一個假的 ROI,我報反解",
            ha="center", va="top", fontsize=15, color=NAVY, fontweight="bold")
    ax.text(.5, .205,
            "口徑:分母用平均餘額(與淨利差定義一致,非期末結餘)· "
            "以集團 NIM 代入時房貸為較低 margin 產品,故為上界 · 本數為淨利息收入,未扣信用減損與資本佔用",
            ha="center", fontsize=8.6, color=GREY)
    save(fig, "fig08_value")

# ============================================================
# 6. P9 KPI 樹
# ============================================================
def fig_kpi():
    LAYERS = [
        ("業務結果", NAVY, ["房貸留存率(增量)", "挽回的年化利息收入"]),
        ("成本", "#7030A0", ["cost per save", "讓利佔挽回收入比 < 1", "12 個月 TCO"]),
        ("作業效率 / 模型品質", "#2E75B6", ["外撥命中率(增量)", "Recall(FN 成本定閾值)",
                                            "漂移修復 MTTR ≤ 10 工作日"]),
        ("採用率", "#ED7D31", ["名單採納率(試點首月定基準)"]),
        ("倫理與客戶體驗護欄", GREEN, ["優惠涵蓋率下限", "財務困難誤判率(抽樣稽核)",
                                       "接觸後 30 日投訴率", "opt-out 率"]),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    box(ax, .35, .875, .30, .085, "本案是否成功?", NAVY, fs=13)
    y = .74
    for name, col, items in LAYERS:
        box(ax, .035, y, .245, .075, name, col, fs=10.5)
        ax.add_patch(FancyArrowPatch((.50, .875), (.285, y + .037), arrowstyle="-",
                                     lw=1.2, color=LIGHT, zorder=1,
                                     connectionstyle="angle,angleA=-90,angleB=0,rad=6"))
        n = len(items)
        bw = (.68 - (n - 1) * .012) / n
        for k, it in enumerate(items):
            x = .30 + k * (bw + .012)
            ax.add_patch(FancyBboxPatch((x, y), bw, .075,
                                        boxstyle="round,pad=0,rounding_size=.015",
                                        fc="#FAFAFA", ec=col, lw=1.3, zorder=3))
            ax.text(x + bw / 2, y + .037, it, ha="center", va="center", fontsize=8.6,
                    color="#333333", zorder=4)
        y -= .105
    ax.text(.5, .975, "KPI 樹:證明賺錢,也證明沒有傷到人",
            ha="center", va="top", fontsize=15, color=NAVY, fontweight="bold")
    ax.add_patch(FancyBboxPatch((.035, .075), .93, .075,
                                boxstyle="round,pad=0,rounding_size=.02",
                                fc="#FFF9E6", ec=AMBER, lw=1.6, zorder=3))
    ax.text(.5, .1125,
            "量測原則:所有業務層指標以「實驗組 減 對照組」的增量計;絕對值僅供監控,不作為成效證據。",
            ha="center", va="center", fontsize=11, color="#7F6000",
            fontweight="bold", zorder=4)
    ax.text(.5, .03, "每項指標另有基準 / 目標 / 達標期間 / 量測頻率 / 負責人 —— "
                     "空白處一律標示「待 CBA 內部基準校準」或「提案人設定,G4 校準」",
            ha="center", fontsize=9, color=GREY)
    save(fig, "fig09_kpi")

# ============================================================
# 7. P11 RACI 熱圖
# ============================================================
def fig_raci():
    ROLES = ["專案贊助人", "業務負責人", "資料負責人", "技術負責人", "合規法務", "客戶經理代表"]
    WPS = ["WP1\n資料整備", "WP2\n模型開發", "WP3\n合規審查",
           "WP4\n流程改造", "WP5\n對照試點", "WP6\n擴展監控"]
    R = [["I", "I", "I", "I", "I", "A"],
         ["I", "C", "I", "A", "A", "C"],
         ["A", "C", "C", "I", "C", "C"],
         ["C", "A", "C", "I", "C", "R"],
         ["C", "I", "A", "C", "C", "I"],
         ["I", "I", "I", "R", "R", "I"]]
    COL = {"A": NAVY, "R": "#2E75B6", "C": "#BDD7EE", "I": "#F2F2F2"}
    TXT = {"A": "white", "R": "white", "C": "#1F3864", "I": GREY}
    fig, ax = plt.subplots(figsize=(11, 5.6))
    for i in range(len(ROLES)):
        for j in range(len(WPS)):
            v = R[i][j]
            ax.add_patch(Rectangle((j, len(ROLES) - 1 - i), 1, 1, fc=COL[v],
                                   ec="white", lw=2.5, zorder=3))
            ax.text(j + .5, len(ROLES) - .5 - i, v, ha="center", va="center",
                    fontsize=13, fontweight="bold", color=TXT[v], zorder=4)
    ax.set_xlim(0, len(WPS)); ax.set_ylim(0, len(ROLES))
    ax.set_xticks([j + .5 for j in range(len(WPS))])
    ax.set_xticklabels(WPS, fontsize=9.5)
    ax.set_yticks([len(ROLES) - .5 - i for i in range(len(ROLES))])
    ax.set_yticklabels(ROLES, fontsize=10.5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("RACI:每個工作包恰有一個 A(當責)",
                 fontsize=15, color=NAVY, fontweight="bold", pad=14)
    handles = [Rectangle((0, 0), 1, 1, fc=COL[k],
                         label={"A": "A 當責", "R": "R 執行",
                                "C": "C 諮詢", "I": "I 告知"}[k]) for k in "ARCI"]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, -.10),
              ncol=4, fontsize=10, frameon=False)
    ax.text(0, -1.02, "技術角色:資料負責人(混合)、技術負責人 · "
                      "非技術角色:專案贊助人、業務負責人、合規法務、客戶經理代表",
            fontsize=9, color=GREY)
    # 驗算:每欄恰一個 A
    bad = [WPS[j].split("\n")[0] for j in range(len(WPS))
           if sum(1 for i in range(len(ROLES)) if R[i][j] == "A") != 1]
    save(fig, "fig11_raci")
    return bad

if __name__ == "__main__":
    print("產出第二批圖表:")
    fig_market()
    fig_matrix()
    fig_loop()
    fig_feasibility()
    fig_value()
    fig_kpi()
    bad = fig_raci()
    print("\nRACI 驗算:每個工作包恰有一個 A ->",
          "全部通過" if not bad else f"!! 不合格:{bad}")
