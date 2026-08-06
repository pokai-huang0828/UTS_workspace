# -*- coding: utf-8 -*-
"""A3 投影片圖表 · 第一批(5 張)
依 notes/A3_提案內容_v2.md 的規格產出。300dpi PNG + SVG(貼進 PowerPoint 可縮放不糊)。
配色三色制:主色深藍 / 強調紅(只用於風險與缺口)/ 中性灰。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, RegularPolygon
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY, RED, GREY = "#1F3864", "#C00000", "#808080"
LIGHT = "#D9D9D9"

def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", name)

# ============================================================
# 1. 影響 × 可能性矩陣(含緩解位移)—— Reflection 30 分項關鍵圖
# ============================================================
def fig_risk_matrix():
    CAT = {"資料": "#2E75B6", "模型": "#7030A0", "組織": "#ED7D31",
           "監管": RED, "經濟": "#548235"}
    # (代號, 類別, 短標, 緩解前(可能性,影響), 緩解後)
    R = [
        ("R1", "資料", "標籤定義歧義",     (4, 5), (2, 2)),
        ("R2", "資料", "時點對齊",         (4, 4), (2, 3)),
        ("R3", "模型", "流失≠可挽回",      (5, 5), (3, 3)),
        ("R4", "模型", "回饋迴路偏誤",     (5, 4), (2, 2)),
        ("R5", "模型", "概念漂移",         (4, 5), (3, 3)),
        ("R6", "組織", "客戶經理不採用",   (4, 4), (3, 3)),
        ("R7", "監管", "差別定價合規",     (3, 5), (2, 4)),
        ("R8", "經濟", "讓利侵蝕利差",     (3, 5), (2, 3)),
        ("R9", "經濟", "初期ROI難證",      (4, 4), (3, 2)),
    ]
    fig, ax = plt.subplots(figsize=(11, 7.5))
    # 背景熱區
    for i in range(1, 6):
        for j in range(1, 6):
            sev = i * j
            c = "#F2F2F2" if sev <= 6 else ("#FFF2CC" if sev <= 12 else "#FBE5E5")
            ax.add_patch(Rectangle((i - .5, j - .5), 1, 1, facecolor=c,
                                   edgecolor="white", lw=1.5, zorder=0))
    # 風險胃納線
    ax.plot([0.5, 5.5], [5.5, 0.5], ls="--", lw=2, color=RED, zorder=2)
    ax.text(5.35, 4.9, "風險胃納線\n線上方的殘餘風險\n須由專案贊助人簽字接受",
            fontsize=9, color=RED, ha="right", va="top", zorder=6,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=RED, alpha=.92))
    # 同格點做環狀偏移,避免標籤重疊
    def spread(points):
        from collections import defaultdict
        idx, cnt = defaultdict(int), defaultdict(int)
        for p in points:
            cnt[p] += 1
        out = []
        for p in points:
            n = cnt[p]
            if n == 1:
                out.append((float(p[0]), float(p[1])))
            else:
                k = idx[p]
                ang = 2 * np.pi * k / n + np.pi / 4
                r = .17
                out.append((p[0] + r * np.cos(ang), p[1] + r * np.sin(ang)))
                idx[p] += 1
        return out

    PRE = spread([r[3] for r in R])
    POST = spread([r[4] for r in R])
    for (code, cat, label, _, _), pre, post in zip(R, PRE, POST):
        col = CAT[cat]
        ax.add_patch(FancyArrowPatch(pre, post, arrowstyle="-|>", mutation_scale=13,
                                     lw=1.3, color=col, alpha=.40,
                                     shrinkA=11, shrinkB=12, zorder=3,
                                     connectionstyle="arc3,rad=0.06"))
        # 緩解前 = 空心虛線圈;緩解後 = 實心
        ax.scatter(*pre, s=250, facecolor="white", edgecolor=col, lw=1.6,
                   alpha=.85, linestyle="--", zorder=4)
        ax.scatter(*post, s=290, facecolor=col, edgecolor="white", lw=1.8, zorder=5)
        ax.text(pre[0], pre[1], code, ha="center", va="center", fontsize=7.5,
                color=col, alpha=.9, zorder=6)
        ax.text(post[0], post[1], code, ha="center", va="center", fontsize=8.5,
                color="white", fontweight="bold", zorder=6)
    ax.set_xlim(.5, 5.5); ax.set_ylim(.5, 5.5)
    ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
    ax.set_xlabel("可能性 →", fontsize=12, color=NAVY)
    ax.set_ylabel("影響 →", fontsize=12, color=NAVY)
    ax.set_title("限制與挑戰:緩解前 → 緩解後的風險位移",
                 fontsize=15, color=NAVY, fontweight="bold", pad=14)
    handles = [plt.Line2D([], [], marker="o", ls="", ms=9, color=c, label=k)
               for k, c in CAT.items()]
    handles += [plt.Line2D([], [], marker="o", ls="", ms=9, mfc="white", mec=GREY,
                           mew=1.6, color="none", label="空心 = 緩解前"),
                plt.Line2D([], [], marker="o", ls="", ms=9, color=GREY,
                           label="實心 = 緩解後")]
    ax.legend(handles=handles, loc="lower left", fontsize=8.5, framealpha=.95, ncol=2,
              handletextpad=.5, columnspacing=1.2)
    # 風險代號對照(圖內,免去另開一頁)
    ax.text(1.06, .98, "\n".join(f"{c}  {l}" for c, _, l, _, _ in R),
            transform=ax.transAxes, va="top", ha="left", fontsize=8.5, color="#404040",
            bbox=dict(boxstyle="round,pad=0.5", fc="#FAFAFA", ec=LIGHT))
    ax.text(.5, -.115, "每一條殘餘風險,在專案計畫裡都有一個對應的停止或回退關卡",
            transform=ax.transAxes, ha="center", fontsize=10, color=GREY)
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig05_risk_matrix")

# ============================================================
# 2. 甘特圖(依賴 + 關鍵路徑 + 緩衝)—— Project plan 30 分項關鍵圖
# ============================================================
def fig_gantt():
    # (WP, 名稱, 起月(0-based), 工期(月), 是否關鍵路徑)
    WP = [
        ("WP1", "資料整備與同意治理", 0, 2.0, True),
        ("WP2", "模型開發與驗證",     2, 2.0, True),
        ("WP3", "可解釋性與合規審查", 4, 1.0, True),
        ("WP4", "流程改造與訓練",     5, 1.0, True),
        ("WP5", "隨機對照試點",       6.5, 2.5, True),
        ("WP6", "擴展與監控",         9, 3.0, True),
    ]
    fig, ax = plt.subplots(figsize=(12, 6))
    y = {}
    for i, (code, name, s, d, crit) in enumerate(WP):
        yy = len(WP) - 1 - i
        y[code] = yy
        ax.barh(yy, d, left=s, height=.5, color=NAVY,
                alpha=.92, zorder=3, edgecolor="white", lw=1.5)
        lbl = f"{d:g} 個月" if d != int(d) else f"{int(d)} 個月"
        ax.text(s + d / 2, yy, lbl, ha="center", va="center",
                color="white", fontsize=9, fontweight="bold", zorder=4)
    # 關鍵路徑:用一條紅線串起所有工作包(全鏈串行,故不用整條染紅)
    xs, ys = [], []
    for code, name, s, d, crit in WP:
        xs += [s, s + d]; ys += [y[code] - .30, y[code] - .30]   # 貼條下緣,不遮文字
    ax.plot(xs, ys, color=RED, lw=2.2, alpha=.9, zorder=6,
            solid_capstyle="round", label="關鍵路徑")
    ax.scatter(xs, ys, s=22, color=RED, zorder=7)
    # 合規預審併行條(風險緩解手段,畫成淺色)
    ax.barh(y["WP3"], 1, left=3, height=.24, color="#9DC3E6", zorder=3,
            edgecolor="white", lw=1)
    ax.text(3.5, y["WP3"] + .32, "合規預審提早併行", ha="center", fontsize=8, color="#2E75B6")
    # 緩衝條(WP4 結束 → WP5 開始之間的空檔)
    ax.barh(y["WP5"], .5, left=6.0, height=.5, color="#FFD966", zorder=3,
            edgecolor="#BF9000", lw=1.2, hatch="///")
    ax.text(6.25, y["WP5"] - .48, "2 週緩衝\n(吸收合規簽核不確定性)",
            ha="center", fontsize=8, color="#7F6000")
    # 依賴箭頭
    for a, b in [("WP1", "WP2"), ("WP2", "WP3"), ("WP3", "WP4"), ("WP4", "WP5"), ("WP5", "WP6")]:
        ai = [w for w in WP if w[0] == a][0]
        bi = [w for w in WP if w[0] == b][0]
        ax.add_patch(FancyArrowPatch((ai[2] + ai[3], y[a]), (bi[2] + .04, y[b]),
                                     arrowstyle="-|>", mutation_scale=11, lw=1.2,
                                     color=GREY, zorder=5,
                                     connectionstyle="angle,angleA=0,angleB=90,rad=4"))
    ax.set_yticks(list(y.values()))
    ax.set_yticklabels([f"{c}  {n}" for c, n, *_ in WP], fontsize=10.5)
    ax.set_xticks(range(13))
    ax.set_xticklabels([f"M{i}" if i else "" for i in range(13)], fontsize=9)
    ax.set_xlim(0, 12.4); ax.set_ylim(-.7, len(WP) - .3)
    ax.grid(axis="x", ls=":", color=LIGHT, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title("實施時程:12 個月、六個工作包", fontsize=15, color=NAVY,
                 fontweight="bold", pad=14)
    ax.legend(loc="upper left", fontsize=9, framealpha=.95)
    ax.text(0, -.62, "六個工作包完全串行,全鏈即關鍵路徑(紅線)—— 任一包延誤都直接推遲交付,"
                     "這正是在試點前置入緩衝的理由。",
            fontsize=9.5, color=GREY)
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig09_gantt")

# ============================================================
# 3. Stage-gate 里程碑軸
# ============================================================
def fig_stagegate():
    G = [
        ("G1", "資料就緒", 2, "特徵完整度達門檻\n流失事件定義已簽署", "資料負責人", False),
        ("G2", "模型",     4, "Recall 達 FN 成本\n反推之閾值", "技術負責人", True),
        ("G3", "合規放行", 5, "模型風險評估\n簽核完成", "合規主管", True),
        ("G4", "流程就緒", 6, "訓練完成且採納率\n達試點首月基準", "業務負責人", True),
        ("G5", "試點裁決", 9, "增量留存率 95% CI\n下界 > 0 且達 δ", "指導委員會", True),
        ("G6", "全面上線", 12, "漂移監控與季度\n重訓機制上線", "專案贊助人", True),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    ax.plot([0, 13], [0, 0], color=NAVY, lw=2.5, zorder=1)
    for code, name, m, crit, owner, kill in G:
        ax.add_patch(RegularPolygon((m, 0), 4, radius=.42, orientation=np.pi / 4,
                                    facecolor=RED if kill else NAVY,
                                    edgecolor="white", lw=2, zorder=3))
        ax.text(m, 0, code, ha="center", va="center", color="white",
                fontsize=9, fontweight="bold", zorder=4)
        ax.text(m, .62, f"{name}\nM{m}", ha="center", va="bottom",
                fontsize=10, color=NAVY, fontweight="bold")
        ax.text(m, -.62, crit, ha="center", va="top", fontsize=8, color="#404040")
        ax.text(m, -1.42, owner, ha="center", va="top", fontsize=8, color=GREY, style="italic")
    ax.set_xlim(0.6, 13.2); ax.set_ylim(-2.1, 1.9)
    ax.axis("off")
    ax.set_title("六道關卡:每一道都有通過判準與決策者",
                 fontsize=15, color=NAVY, fontweight="bold", pad=4)
    ax.text(0.8, 1.55, "◆ 紅色 = 含 Kill 判準的關卡(未達則停止或回退,不續投)",
            fontsize=9.5, color=RED)
    ax.text(0.8, -1.95, "每道關卡四態:Go / Conditional-Go / Hold / Kill", fontsize=9, color=GREY)
    save(fig, "fig10_stagegate")

# ============================================================
# 4. 資源直方圖(rubric 明文要件「資源」)
# ============================================================
def fig_resource():
    # 角色 -> {WP: 人月};WP 起訖(0-based 月)
    SPAN = {"WP1": (0, 2), "WP2": (2, 2), "WP3": (4, 1),
            "WP4": (5, 1), "WP5": (6, 3), "WP6": (9, 3)}
    ROLE = {
        "資料工程師":     {"WP1": 3.0, "WP2": 0.5, "WP5": 0.5, "WP6": 1.0},
        "資料科學家":     {"WP1": 0.5, "WP2": 3.0, "WP3": 1.0, "WP5": 1.0, "WP6": 1.5},
        "MLOps":          {"WP2": 1.0, "WP3": 0.5, "WP5": 0.5, "WP6": 3.0},
        "合規法務":       {"WP1": 0.5, "WP3": 1.5, "WP4": 0.5, "WP5": 0.5, "WP6": 0.5},
        "業務分析與流程": {"WP1": 0.5, "WP4": 2.0, "WP5": 1.0, "WP6": 0.5},
    }
    COL = {"資料工程師": "#2E75B6", "資料科學家": "#7030A0", "MLOps": "#ED7D31",
           "合規法務": RED, "業務分析與流程": "#548235", "專案經理": GREY}
    months = np.arange(12)
    stacks = {}
    for r, wps in ROLE.items():
        arr = np.zeros(12)
        for wp, pm in wps.items():
            s, d = SPAN[wp]
            arr[s:s + d] += pm / d
        stacks[r] = arr
    stacks["專案經理"] = np.full(12, 0.25)

    fig, ax = plt.subplots(figsize=(11.5, 6))
    bottom = np.zeros(12)
    for r, arr in stacks.items():
        ax.bar(months, arr, bottom=bottom, width=.72, label=f"{r}({arr.sum():.1f})",
               color=COL[r], edgecolor="white", lw=1, zorder=3)
        bottom += arr
    total = bottom.sum()
    for m in months:
        ax.text(m, bottom[m] + .06, f"{bottom[m]:.2f}", ha="center",
                fontsize=8, color=GREY)
    ax.set_xticks(months); ax.set_xticklabels([f"M{i+1}" for i in months], fontsize=9)
    ax.set_ylabel("FTE(人月 / 月)", fontsize=11, color=NAVY)
    ax.set_title(f"資源配置:總計 {total:.1f} 人月(規劃值)",
                 fontsize=15, color=NAVY, fontweight="bold", pad=14)
    ax.legend(fontsize=9, ncol=3, loc="upper center", framealpha=.95)
    ax.grid(axis="y", ls=":", color=LIGHT, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylim(0, bottom.max() * 1.42)
    ax.text(0, -bottom.max() * .19,
            "Planning estimate — to be calibrated with CBA internal rates。"
            "成本 = 總人月 × 澳洲 ICT 職類薪資中位數區間 × 1.3 間接費率(間接費率為提案人假設)。",
            fontsize=9, color=GREY)
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig11_resource")
    return total

# ============================================================
# 5. 敏感度龍捲風圖(選案矩陣)
# ============================================================
def fig_tornado():
    W = {"戰略契合": .25, "增量價值": .20, "第一方資料完整度": .15,
         "資料治理簡易度": .10, "監管可行性": .10, "用戶採用容易度": .10,
         "6個月可交付性": .10}
    S = {"A": {"戰略契合": 5, "增量價值": 5, "第一方資料完整度": 3, "資料治理簡易度": 2,
               "監管可行性": 2, "用戶採用容易度": 2, "6個月可交付性": 3},
         "B": {"戰略契合": 3, "增量價值": 2, "第一方資料完整度": 5, "資料治理簡易度": 4,
               "監管可行性": 4, "用戶採用容易度": 4, "6個月可交付性": 4}}

    def score(k, w):
        return sum(w[d] * S[k][d] for d in w)

    base = score("A", W) - score("B", W)
    rows = []
    for d in W:
        lo, hi = [], []
        for mult in (0.5, 1.5):                     # 該維權重 ±50%
            w = dict(W); w[d] = W[d] * mult
            rest = (1 - w[d]) / (1 - W[d])
            for k in w:
                if k != d:
                    w[k] = W[k] * rest
            v = score("A", w) - score("B", w)
            (lo if mult < 1 else hi).append(v)
        rows.append((d, lo[0], hi[0]))
    rows.sort(key=lambda r: abs(r[2] - r[1]))

    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    for i, (d, lo, hi) in enumerate(rows):
        ax.barh(i, hi - base, left=base, height=.6,
                color=NAVY, alpha=.85, zorder=3)
        ax.barh(i, lo - base, left=base, height=.6,
                color=RED, alpha=.85, zorder=3)
        ax.text(max(hi, lo) + .004, i, f"{min(lo,hi):+.3f} ~ {max(lo,hi):+.3f}",
                va="center", fontsize=8.5, color=GREY)
    ax.axvline(0, color=RED, ls="--", lw=1.8, zorder=4)
    ax.axvline(base, color=GREY, ls=":", lw=1.5, zorder=4)
    ax.text(0, len(rows) - .35, "  排序翻轉線(A 與 B 同分)", color=RED, fontsize=9.5, va="bottom")
    ax.text(base, -.85, f"基準 {base:+.3f}", color=GREY, fontsize=9, ha="center")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=10.5)
    ax.set_xlabel("A 案與 B 案的加權總分差", fontsize=11, color=NAVY)
    ax.set_title("敏感度:加權矩陣不足以定案",
                 fontsize=15, color=NAVY, fontweight="bold", pad=14)
    flippable = sum(1 for _, lo, hi in rows if (lo < 0 <= hi) or (hi < 0 <= lo))
    ax.text(0, -1.62,
            f"深藍 = 該權重提高 50%;紅 = 降低 50%。越過虛線即推薦翻轉為 B 案。\n"
            f"基準差僅 {base:+.2f} —— 七個維度中有 {flippable} 個可在 ±50% 權重內翻轉結論。\n"
            f"因此本案的選擇依據不是矩陣分數,而是一個質性判斷:"
            f"只有 A 案對應到一個尚無 AI 覆蓋的戰略缺口。",
            fontsize=9.5, color=GREY)
    ax.grid(axis="x", ls=":", color=LIGHT, zorder=0)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(LIGHT)
    save(fig, "fig03_tornado")
    return base, rows

if __name__ == "__main__":
    print("產出第一批圖表:")
    fig_risk_matrix()
    fig_gantt()
    fig_stagegate()
    total = fig_resource()
    base, rows = fig_tornado()
    print(f"\n人月合計驗算 = {total:.1f}")
    print(f"A−B 基準差 = {base:+.4f}")
    print("敏感度(依影響幅度排序,最後一列最敏感):")
    for d, lo, hi in rows:
        flip = "  <-- 可翻轉" if (lo < 0 <= hi) or (hi < 0 <= lo) else ""
        print(f"  {d:<18} {lo:+.4f} ~ {hi:+.4f}{flip}")
