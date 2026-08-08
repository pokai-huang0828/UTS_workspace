# -*- coding: utf-8 -*-
"""A3 v3 圖表(10 張)。v3 論證:先證明,再建置。
紅線:不得出現任何未經標示來源的數值;提案人設定值一律在圖上標明。
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
BLUE, PURPLE, ORANGE = "#2E75B6", "#7030A0", "#ED7D31"


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", name)


def newfig(w=12.5, h=6.4, title=None):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    if title:
        ax.text(.5, .985, title, ha="center", va="top", fontsize=15.5,
                color=NAVY, fontweight="bold")
    return fig, ax


def box(ax, x, y, w, h, text, fc, fs=10, tc="white", ec=None, lw=1.5, bold=True, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=.015",
                                fc=fc, ec=ec or fc, lw=lw, ls=ls, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal", zorder=4, linespacing=1.6)


def panel(ax, x, y, w, h, title, body, col, tfs=11, bfs=9, fc="#FAFAFA"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=.015",
                                fc=fc, ec=col, lw=1.6, zorder=3))
    ax.add_patch(FancyBboxPatch((x, y + h - .075), w, .075,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=col, ec=col, zorder=4))
    ax.text(x + w / 2, y + h - .0375, title, ha="center", va="center", fontsize=tfs,
            color="white", fontweight="bold", zorder=5)
    ax.text(x + w / 2, y + (h - .075) / 2, body, ha="center", va="center", fontsize=bfs,
            color="#333333", zorder=5, linespacing=1.85)


# ============================================================
# 01 · P2 CBA 既有能力(主動承認,不宣稱空白)
# ============================================================
def f01():
    fig, ax = newfig(12.5, 6.2)
    ROWS = [("Customer Engagement Engine", "跨通路次佳行動,每天約 3,500 萬項決策", "CBA (2022)"),
            ("已經做過「到期事件留存」", "對約 10 萬名定存到期客戶主動聯繫,續存率 85%", "CBA (2019)"),
            ("客服等待時間", "一財年內 -40%", "CBA (2024)"),
            ("業務信貸年審 / 房貸有條件核准", "14 小時 → 2 小時 / 少於 10 分鐘", "CBA (2024)"),
            ("客戶詐騙損失", "較 2022 年底高峰下降 76%;FY25 防詐投入約 A$9 億", "CBA (2025c)")]
    y = .77
    for i, (a, b, c) in enumerate(ROWS):
        hl = (i == 1)
        ax.add_patch(FancyBboxPatch((.03, y), .94, .105,
                                    boxstyle="round,pad=0,rounding_size=.012",
                                    fc="#FFF4F4" if hl else "#FAFAFA",
                                    ec=RED if hl else LIGHT, lw=2 if hl else 1.2, zorder=3))
        ax.text(.055, y + .0525, a, ha="left", va="center", fontsize=10.5,
                color=RED if hl else NAVY, fontweight="bold", zorder=4)
        ax.text(.42, y + .0525, b, ha="left", va="center", fontsize=9.5,
                color="#333333", zorder=4)
        ax.text(.955, y + .0525, c, ha="right", va="center", fontsize=8.5,
                color=GREY, zorder=4)
        y -= .125
    ax.text(.5, .175,
            "我不打算告訴各位 CBA 缺少 AI 能力 —— 那不是事實。",
            ha="center", fontsize=14, color=NAVY, fontweight="bold")
    ax.text(.5, .085,
            "所以今天要問的不是「我們有沒有能力」,\n"
            "而是「那套能力,能不能直接搬到房貸到期上」。",
            ha="center", va="center", fontsize=12.5, color=RED,
            fontweight="bold", linespacing=1.8)
    save(fig, "fig_v3_01_baseline")


# ============================================================
# 02 · P3 房貸到期 ≠ 定存到期
# ============================================================
def f02():
    fig, ax = newfig(12.5, 6.2)
    box(ax, .30, .845, .30, .075, "定存到期(CEE 已做)", BLUE, fs=11)
    box(ax, .645, .845, .30, .075, "房貸固定利率到期", RED, fs=11)
    ROWS = [("決策複雜度", "續存或不續存,\n單一決策",
             "涉及再融資成本、LMI、解約費、\ndischarge、抵押權登記 ——\n轉換摩擦高,但一旦啟動很難回頭"),
            ("競爭者主動性", "客戶多為自行決定",
             "broker 通路會主動接觸 ——\n競爭是被推動的,不是被動發生"),
            ("金額與期限量級", "單筆小、期限以月計",
             "單筆大、關係以年計 ——\n一次失誤的終身價值損失\n完全不同量級")]
    y = .60
    for a, b, c in ROWS:
        ax.text(.025, y + .105, a, ha="left", va="center", fontsize=11,
                color=NAVY, fontweight="bold")
        ax.add_patch(FancyBboxPatch((.30, y), .30, .21,
                                    boxstyle="round,pad=0,rounding_size=.012",
                                    fc="#F5F9FC", ec=BLUE, lw=1.3, zorder=3))
        ax.text(.45, y + .105, b, ha="center", va="center", fontsize=9,
                color="#333333", zorder=4, linespacing=1.8)
        ax.add_patch(FancyBboxPatch((.645, y), .30, .21,
                                    boxstyle="round,pad=0,rounding_size=.012",
                                    fc="#FFF7F7", ec=RED, lw=1.3, zorder=3))
        ax.text(.795, y + .105, c, ha="center", va="center", fontsize=9,
                color="#333333", zorder=4, linespacing=1.8)
        y -= .245
    ax.text(.5, .075,
            "定存到期的留存邏輯是「提醒你續約」。房貸到期,是要在客戶已經在跟別人談的時候,用對的價格留住他。\n"
            "這是不同的問題 —— 但沒有人量過現有做法在這個問題上能走多遠。",
            ha="center", va="center", fontsize=11, color=NAVY,
            fontweight="bold", linespacing=1.9)
    save(fig, "fig_v3_02_gap")


# ============================================================
# 03 · P4 六個未知
# ============================================================
def f03():
    fig, ax = newfig(12.5, 6.4)
    U = [("1", "CEE 目前是否已覆蓋房貸到期場景、覆蓋到什麼程度", "內部系統範圍不對外揭露", "訪談 + 系統盤點"),
         ("2", "每年落在固定利率到期窗口的房貸餘額與戶數", "內部到期分佈不對外揭露", "資料稽核"),
         ("3", "「流失」的操作型定義能否建立\n(外部再融資 / 售屋結清 / 內部再定價)", "需要內部事件紀錄", "業務與資料雙簽 + 人工複核"),
         ("4", "規則式主動介入到底有沒有增量效果", "從來沒有做過對照實驗", "★ 這就是本提案的核心"),
         ("5", "差別留存優惠在監管上的可行邊界", "需要合規正式意見", "合規諮詢"),
         ("6", "每戶年度淨貢獻與可讓利空間", "產品別 margin 為內部資料", "財務提供")]
    y = .795
    for n, q, why, how in U:
        hl = (n == "4")
        ax.add_patch(FancyBboxPatch((.03, y), .94, .108,
                                    boxstyle="round,pad=0,rounding_size=.012",
                                    fc="#FFF4F4" if hl else "#FAFAFA",
                                    ec=RED if hl else LIGHT, lw=2.2 if hl else 1.2, zorder=3))
        ax.add_patch(Circle((.062, y + .054), .019, fc=RED if hl else NAVY, zorder=4))
        ax.text(.062, y + .054, n, ha="center", va="center", fontsize=10,
                color="white", fontweight="bold", zorder=5)
        ax.text(.095, y + .054, q, ha="left", va="center", fontsize=9.5,
                color=RED if hl else "#222222", fontweight="bold" if hl else False,
                zorder=4, linespacing=1.5)
        ax.text(.60, y + .054, why, ha="left", va="center", fontsize=8.5,
                color=GREY, zorder=4)
        ax.text(.955, y + .054, how, ha="right", va="center", fontsize=8.5,
                color=RED if hl else GREEN, fontweight="bold" if hl else False, zorder=4)
        y -= .125
    ax.text(.60, .935, "為什麼公開資料答不了", ha="left", fontsize=9, color=GREY)
    ax.text(.955, .935, "8 週內能否解決", ha="right", fontsize=9, color=GREY)
    ax.text(.5, .055,
            "第四件 —— 主動介入到底有沒有用 —— 是整個投資案的地基。\n"
            "如果答案是沒有,後面所有的模型、平台、路線圖都不必談。",
            ha="center", va="center", fontsize=12, color=RED,
            fontweight="bold", linespacing=1.8)
    save(fig, "fig_v3_03_unknowns")


# ============================================================
# 04 · P5 三條路(含 no-AI baseline)
# ============================================================
def f04():
    fig, ax = newfig(12.5, 6.4)
    OPT = [(.03, "選項 0 · 不做", GREY,
            "維持現狀\n\n需要 AI:否\n成本:0\n\n前提:—"),
           (.355, "選項 1 · 規則式介入", BLUE,
            "用既有 CEE / 外撥流程,\n按到期日建立名單\n\n需要 AI:否\n到期日是確定事件,SQL 就能取\n\n成本:低(流程調整)\n\n前提:無"),
           (.68, "選項 2 · 房貸專用 uplift 模型", PURPLE,
            "只對「會被介入改變結果」\n的客群投放\n\n需要 AI:是\n\n成本:高(12 個月級)\n\n前提:必須先知道介入有效,\n且有 uplift 標籤")]
    for x, t, c, b in OPT:
        panel(ax, x, .30, .29, .58, t, b, c, tfs=11, bfs=9)
    ax.add_patch(FancyBboxPatch((.355, .195), .29, .075,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc="#FFF9E6", ec=AMBER, lw=1.6, zorder=3))
    ax.text(.50, .2325, "不知道有沒有用", ha="center", va="center",
            fontsize=10, color="#7F6000", fontweight="bold", zorder=4)
    ax.add_patch(FancyBboxPatch((.68, .195), .29, .075,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc="#FFF4F4", ec=RED, lw=1.6, zorder=3))
    ax.text(.825, .2325, "前提尚未成立", ha="center", va="center",
            fontsize=10, color=RED, fontweight="bold", zorder=4)
    ax.add_patch(FancyArrowPatch((.675, .49), (.65, .49), arrowstyle="-|>",
                                 mutation_scale=20, lw=2.2, color=RED, zorder=6))
    ax.text(.5, .105,
            "要訓練增量模型,得先有增量標籤;而增量標籤只能從對照實驗來。\n"
            "選項 2 在數學上必須以選項 1 的實驗為前提。",
            ha="center", va="center", fontsize=11.5, color=NAVY,
            fontweight="bold", linespacing=1.85)
    ax.text(.5, .028,
            "所以今天的問題不是「選 1 還是選 2」,是「我們有沒有資格現在就選」。",
            ha="center", fontsize=12, color=RED, fontweight="bold")
    save(fig, "fig_v3_04_options")


# ============================================================
# 05 · P6 八週工作包
# ============================================================
def f05():
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    WP = [("WP0-A", "系統與流程盤點", 0, 2, NAVY),
          ("WP0-B", "資料稽核", 0, 3, BLUE),
          ("WP0-C", "合規預審", 1, 3, RED),
          ("WP0-D", "規則式對照實驗", 2, 6, PURPLE),
          ("WP0-E", "決策文件", 7, 1, GREEN)]
    y = {}
    for i, (c, n, s, d, col) in enumerate(WP):
        yy = len(WP) - 1 - i
        y[c] = yy
        ax.barh(yy, d, left=s, height=.52, color=col, alpha=.92, zorder=3,
                edgecolor="white", lw=1.5)
        ax.text(s + d / 2, yy, f"{d} 週", ha="center", va="center", color="white",
                fontsize=9.5, fontweight="bold", zorder=4)
    # 關鍵路徑 C -> D
    ax.plot([1, 4, 4, 8], [y["WP0-C"] - .32, y["WP0-C"] - .32,
                           y["WP0-D"] - .32, y["WP0-D"] - .32],
            color=RED, lw=2.4, zorder=6, solid_capstyle="round")
    ax.text(4.05, y["WP0-D"] - .55, "關鍵路徑:合規意見書未出,實驗不能開始",
            fontsize=9, color=RED, fontweight="bold")
    ax.set_yticks(list(y.values()))
    ax.set_yticklabels([f"{c}  {n}" for c, n, *_ in WP], fontsize=10.5)
    ax.set_xticks(range(9))
    ax.set_xticklabels([f"W{i}" if i else "" for i in range(9)], fontsize=9.5)
    ax.set_xlim(0, 8.3); ax.set_ylim(-.60, len(WP) - .35)
    ax.grid(axis="x", ls=":", color=LIGHT, zorder=0); ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig_v3_05_plan")


# ============================================================
# 06 · P7 實驗設計
# ============================================================
def f06():
    fig, ax = newfig(12.5, 6.4)
    box(ax, .34, .80, .32, .095, "依到期日取出的客戶母體\n(SQL,不需要模型)", NAVY, fs=10)
    ax.add_patch(FancyArrowPatch((.50, .795), (.50, .735), arrowstyle="-|>",
                                 mutation_scale=18, lw=2, color=GREY, zorder=5))
    ax.text(.515, .765, "隨機分派", fontsize=9.5, color=RED, fontweight="bold")
    box(ax, .13, .60, .30, .115, "實驗組\n現有外撥流程主動介入", BLUE, fs=10.5)
    box(ax, .57, .60, .30, .115, "對照組\n維持現狀,不介入", GREY, fs=10.5)
    for x in (.28, .72):
        ax.add_patch(FancyArrowPatch((x, .595), (x, .525), arrowstyle="-|>",
                                     mutation_scale=16, lw=1.8, color=GREY, zorder=5))
    box(ax, .13, .415, .74, .105,
        "主要結果:到期後 90 日內仍為 CBA 房貸客戶的比例", NAVY, fs=11)
    SPEC = [("估計量", "兩組比例差(risk difference),獨立樣本"),
            ("區間", "獨立樣本比例差的 95% CI;叢集設計改用 cluster-robust 標準誤"),
            ("樣本量", "由最低商業可接受效果在 α=0.05、power=0.8 下反推"),
            ("判準", "95% CI 下界 > 0,且點估計不低於最低商業可接受效果")]
    y = .325
    for k, v in SPEC:
        ax.text(.135, y, k, ha="left", va="center", fontsize=9.5,
                color=NAVY, fontweight="bold")
        ax.text(.255, y, v, ha="left", va="center", fontsize=9.5, color="#333333")
        y -= .052
    ax.add_patch(FancyBboxPatch((.13, .015), .74, .095,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc="#FFF9E6", ec=AMBER, lw=1.6, zorder=3))
    ax.text(.50, .0625,
            "次要結果 · 異質性:哪些客群的增量效果最大 —— 模型的價值,恰恰等於效果的異質程度。\n"
            "若各客群效果都差不多,就不需要模型,規則式全打即可。",
            ha="center", va="center", fontsize=10, color="#7F6000",
            fontweight="bold", zorder=4, linespacing=1.8)
    ax.text(.955, .325, "MDE 是樣本量設計參數,\n不是成功門檻 ——\n兩者分別命名",
            ha="right", va="top", fontsize=8.5, color=RED, linespacing=1.7)
    save(fig, "fig_v3_06_experiment")


# ============================================================
# 07 · P8 風險矩陣(v3 清單)
# ============================================================
def f07():
    CAT = {"資料": BLUE, "實驗": PURPLE, "組織": ORANGE, "監管": RED, "經濟": GREEN}
    R = [("R1", "資料", "標籤定義歧義", (4, 5), (2, 2)),
         ("R2", "資料", "可尋址客群過小", (3, 4), (3, 2)),
         ("R3", "實驗", "溢出效應", (4, 4), (2, 3)),
         ("R4", "實驗", "介入的負向效果", (3, 4), (2, 3)),
         ("R5", "組織", "執行率不足污染實驗", (4, 3), (3, 2)),
         ("R6", "監管", "差別優惠合規邊界未定", (3, 5), (2, 4)),
         ("R7", "經濟", "結論是不值得做", (5, 2), (5, 2))]
    fig, ax = plt.subplots(figsize=(11.5, 6.6))
    for i in range(1, 6):
        for j in range(1, 6):
            sev = i * j
            c = "#F2F2F2" if sev <= 6 else ("#FFF2CC" if sev <= 12 else "#FBE5E5")
            ax.add_patch(Rectangle((i - .5, j - .5), 1, 1, facecolor=c,
                                   edgecolor="white", lw=1.5, zorder=0))
    ax.plot([.5, 5.5], [5.5, .5], ls="--", lw=2, color=RED, zorder=2)

    def spread(pts):
        from collections import defaultdict
        cnt, idx = defaultdict(int), defaultdict(int)
        for p in pts:
            cnt[p] += 1
        out = []
        for p in pts:
            n = cnt[p]
            if n == 1:
                out.append((float(p[0]), float(p[1])))
            else:
                k = idx[p]; a = 2 * np.pi * k / n + np.pi / 4
                out.append((p[0] + .16 * np.cos(a), p[1] + .16 * np.sin(a)))
                idx[p] += 1
        return out

    PRE, POST = spread([r[3] for r in R]), spread([r[4] for r in R])
    for (code, cat, lab, _, _), a, b in zip(R, PRE, POST):
        col = CAT[cat]
        if a != b:
            ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13,
                                         lw=1.3, color=col, alpha=.45,
                                         shrinkA=11, shrinkB=12, zorder=3,
                                         connectionstyle="arc3,rad=0.06"))
        ax.scatter(*a, s=250, facecolor="white", edgecolor=col, lw=1.6,
                   linestyle="--", zorder=4)
        ax.scatter(*b, s=290, facecolor=col, edgecolor="white", lw=1.8, zorder=5)
        ax.text(a[0], a[1], code, ha="center", va="center", fontsize=7.5,
                color=col, zorder=6)
        ax.text(b[0], b[1], code, ha="center", va="center", fontsize=8.5,
                color="white", fontweight="bold", zorder=6)
    ax.set_xlim(.5, 5.5); ax.set_ylim(.5, 5.5)
    ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
    ax.set_xlabel("可能性 →", fontsize=12, color=NAVY)
    ax.set_ylabel("影響 →", fontsize=12, color=NAVY)
    h = [plt.Line2D([], [], marker="o", ls="", ms=9, color=c, label=k) for k, c in CAT.items()]
    ax.legend(handles=h, loc="lower left", fontsize=9, ncol=2, framealpha=.95)
    ax.text(1.03, .98, "\n".join(f"{c}  {l}" for c, _, l, _, _ in R),
            transform=ax.transAxes, va="top", ha="left", fontsize=8.5, color="#404040",
            bbox=dict(boxstyle="round,pad=0.5", fc="#FAFAFA", ec=LIGHT))
    ax.text(1.03, .30, "R7 不做緩解:\n「結論是不值得做」\n本身就是有價值的交付 ——\n"
                       "用 3.5 人月避免\n27.5 人月的錯誤投資",
            transform=ax.transAxes, va="top", ha="left", fontsize=8.5,
            color=GREEN, fontweight="bold", linespacing=1.7,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F4F9F1", ec=GREEN))
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig_v3_07_risk")


# ============================================================
# 08 · P9 倫理(補上 LTV 加權的分配問題)
# ============================================================
def f08():
    fig, ax = newfig(13, 6.8)
    TALK = [(.545, "① 脆弱客戶:兩個方向的代價不對稱", RED,
             "還款行為異常同時是流失前兆與財務困難前兆,\n模型在數學上無法區分兩者。\n\n"
             "漏掉一個要走的客戶,只是損失利差;\n把財困客戶當商機,是監管事件。\n\n"
             "護欄:名單進入外撥前必須先過財務困難篩選,\n"
             "命中者強制轉入 hardship 並移出名單 ——\n此規則寫在系統層,不是人工判斷層。"),
            (.075, "② 分配原則:先照顧誰,不是技術決定", RED,
             "先前版本的排序是「流失傾向 × 終身價值」——\n"
             "等於高餘額客戶先得到人工關注與優惠,\n低 LTV 客戶即使同樣可能離開也被降級。\n\n"
             "地理與年齡的代理稽核,\n修不了目標函數本身的差別待遇。\n\n"
             "本案處理:實驗階段的名單排序只用流失傾向,\n不乘 LTV —— 把它變成需要委員會與合規\n明確決定的價值選擇。")]
    for y, t, c, b in TALK:
        ax.add_patch(FancyBboxPatch((.02, y), .50, .40,
                                    boxstyle="round,pad=0,rounding_size=.015",
                                    fc="#FFF7F7", ec=c, lw=1.8, zorder=3))
        ax.text(.27, y + .355, t, ha="center", va="center", fontsize=11.5,
                color=c, fontweight="bold", zorder=4)
        ax.text(.27, y + .15, b, ha="center", va="center", fontsize=8.6,
                color="#333333", zorder=4, linespacing=1.75)
    ROWS = [("可解釋性", "對客戶 / 客戶經理 / 監管\n三種粒度的說明", "合規"),
            ("禁用特徵清單", "CDR 資料分享請求紀錄 /\n贖回詢問紀錄 / 地理代理", "合規 + 資料"),
            ("代理歧視稽核", "地理區 / 貸款規模 / 年齡帶\n三切面量測優惠獲取率差異", "合規"),
            ("忠誠稅", "設前後簿利率差上限;\n對未被選中者定期主動檢視", "定價團隊")]
    x0, w = .545, .435
    ax.text(x0 + w / 2, .955, "其餘四項護欄與簽核責任", ha="center", va="top",
            fontsize=11.5, color=NAVY, fontweight="bold")
    hdr = [("議題", .115), ("護欄", .225), ("簽核", .095)]
    cx = x0
    for t, cw in hdr:
        ax.add_patch(FancyBboxPatch((cx, .865), cw, .045,
                                    boxstyle="round,pad=0,rounding_size=.008",
                                    fc=NAVY, ec=NAVY, zorder=3))
        ax.text(cx + cw / 2, .8875, t, ha="center", va="center", fontsize=9,
                color="white", fontweight="bold", zorder=4)
        cx += cw
    yy = .865
    for a, b, c in ROWS:
        yy -= .085
        cx = x0
        for txt_, cw in zip((a, b, c), [h[1] for h in hdr]):
            ax.add_patch(FancyBboxPatch((cx, yy), cw, .082,
                                        boxstyle="round,pad=0,rounding_size=.006",
                                        fc="#FAFAFA", ec=LIGHT, lw=1, zorder=3))
            ax.text(cx + cw / 2, yy + .041, txt_, ha="center", va="center",
                    fontsize=7.6, color="#333333", zorder=4, linespacing=1.5)
            cx += cw
    ax.add_patch(FancyBboxPatch((x0, .075), w, .40,
                                boxstyle="round,pad=0,rounding_size=.015",
                                fc="#F4F9F1", ec=GREEN, lw=1.8, zorder=3))
    ax.text(x0 + w / 2, .425, "為什麼這一頁放在實驗提案裡", ha="center", va="center",
            fontsize=11, color=GREEN, fontweight="bold", zorder=4)
    ax.text(x0 + w / 2, .245,
            "這個系統最根本的倫理問題,\n不在它用了什麼特徵,\n在它決定先照顧誰。\n\n"
            "那不是一個技術決定,\n所以我不打算在工程階段\n偷偷決定它。",
            ha="center", va="center", fontsize=10.5, color="#333333",
            zorder=4, linespacing=2.0)
    save(fig, "fig_v3_08_ethics")


# ============================================================
# 09 · P10 決策規則樹
# ============================================================
def f09():
    fig, ax = newfig(12.5, 6.4)
    box(ax, .34, .805, .32, .10, "W8 的實驗結果", NAVY, fs=13)
    OUT = [(.02, "增量效果顯著\n且異質性高", PURPLE, "→ 進選項 2\n建 uplift 模型\n\n屆時才提完整投資案\n與 KPI 樹",
            "模型的價值\n等於效果的異質程度"),
           (.265, "增量效果顯著\n但異質性低", BLUE, "→ 進選項 1\n規則式全打\n\n不建模型",
            "全打就有效,\n模型不會增加價值"),
           (.51, "增量效果\n不顯著", RED, "→ 停止\n\n實驗結果作為\n資產保留",
            "3.5 人月買到\n「不要投 27.5 人月」"),
           (.755, "可尋址客群\n過小", RED, "→ 停止", "同上")]
    for x, cond, col, act, why in OUT:
        ax.add_patch(FancyArrowPatch((.50, .80), (x + .1125, .715), arrowstyle="-|>",
                                     mutation_scale=14, lw=1.5, color=GREY, zorder=2,
                                     connectionstyle="arc3,rad=0.12"))
        box(ax, x, .60, .225, .105, cond, col, fs=9.5)
        ax.add_patch(FancyBboxPatch((x, .285), .225, .29,
                                    boxstyle="round,pad=0,rounding_size=.012",
                                    fc="#FAFAFA", ec=col, lw=1.5, zorder=3))
        ax.text(x + .1125, .43, act, ha="center", va="center", fontsize=9.5,
                color="#333333", zorder=4, linespacing=1.9)
        ax.text(x + .1125, .225, why, ha="center", va="center", fontsize=8.5,
                color=GREY, zorder=4, linespacing=1.7)
    ax.add_patch(FancyBboxPatch((.02, .035), .96, .125,
                                boxstyle="round,pad=0,rounding_size=.015",
                                fc="#FFF9E6", ec=AMBER, lw=1.8, zorder=3))
    ax.text(.50, .0975,
            "四種結果裡有兩種導向「停止」—— 而那不是失敗,是這個提案最重要的產出之一。\n"
            "Phase 1 的 KPI 樹要等 W8 帶著基準值回來才提;現在提,就是在沒有基準的情況下編目標。",
            ha="center", va="center", fontsize=10.5, color="#7F6000",
            fontweight="bold", zorder=4, linespacing=1.85)
    save(fig, "fig_v3_09_decision")


# ============================================================
# 10 · P11 資源
# ============================================================
def f10():
    ROLE = [("業務分析與流程", 1.0, NAVY), ("資料分析師", 1.0, BLUE),
            ("合規法務", 0.5, RED), ("統計 / 實驗設計", 0.5, PURPLE),
            ("專案經理(0.25×2 月)", 0.5, GREY)]
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    names = [r[0] for r in ROLE][::-1]
    vals = [r[1] for r in ROLE][::-1]
    cols = [r[2] for r in ROLE][::-1]
    ax.barh(range(len(names)), vals, color=cols, height=.55, zorder=3,
            edgecolor="white", lw=1.5)
    for i, v in enumerate(vals):
        ax.text(v + .03, i, f"{v:.1f} 人月", va="center", fontsize=10.5,
                color=NAVY, fontweight="bold")
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=11)
    ax.set_xlim(0, 1.42); ax.set_xlabel("人月(規劃值)", fontsize=11, color=NAVY)
    ax.grid(axis="x", ls=":", color=LIGHT, zorder=0); ax.set_axisbelow(True)
    ax.text(1.40, len(names) - .05, f"合計 {sum(v for _, v, _ in ROLE):.1f} 人月",
            ha="right", va="center", fontsize=22, color=NAVY, fontweight="bold")
    ax.text(0, -1.30,
            "Planning estimate — to be calibrated with CBA internal rates。\n"
            "成本 = 3.5 人月 × 澳洲 ICT 職類薪資中位數區間 × 1.3 間接費率(間接費率為提案人假設)。\n"
            "無新增系統採購、無平台授權、無外部顧問。",
            fontsize=9.5, color=GREY, linespacing=1.8)
    ax.text(1.40, len(names) - .55,
            "對比:先前版本請求 27.5 人月\n去建一個前提未驗證的系統。\n"
            "同一份標準下,\n先花 3.5 人月驗證那個前提,\n是更好的投資判斷。",
            ha="right", va="top", fontsize=9.5, color=GREEN, fontweight="bold",
            linespacing=1.8,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F4F9F1", ec=GREEN))
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig_v3_10_resource")


if __name__ == "__main__":
    print("產出 v3 圖表:")
    for f in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10):
        f()
    print("\n完成 10 張。")
