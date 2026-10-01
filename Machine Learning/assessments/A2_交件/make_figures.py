"""產生 A2 報告的圖 1、圖 2（PNG, 300 dpi）。數字全部由 TeleMarketing.csv 重算。

兩張圖都以實際列印寬度（15.8 cm ≈ 6.2 in）設計，印出後文字 ≥ 8 pt。
"""
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

matplotlib.rcParams["font.family"] = ["Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).resolve().parent
CSV = HERE.parent.parent / "data" / "bank_x" / "TeleMarketing.csv"

INK = "#0b0b0b"
INK2 = "#52514e"
SURFACE = "#ffffff"
ACCENT = "#eb6834"
ORANGE_FILL = "#fff4ee"
RED = "#c0392b"
BLUE = "#2a78d6"
GRAY_DARK = "#5f5e5a"
GRAY_LIGHT = "#b9b7b0"
GRAY_MID = "#8d8b85"
HOURLY = 50  # 假設時薪 A$50


def numbers():
    d = pd.read_csv(CSV)
    d["yy"] = (d["y"] == "yes").astype(int)
    t, c = d[d.campaign == 1], d[d.campaign == 0]
    fail_h = t.loc[t.yy == 0, "duration"].sum() / 3600
    succ_h = t.loc[t.yy == 1, "duration"].sum() / 3600
    fail_cost = round(fail_h * HOURLY)
    total = round(t["duration"].sum() / 3600 * HOURLY)
    succ_cost = total - fail_cost  # 取整後讓兩段加總等於合計
    buyers = int(t.yy.sum())
    inc = round(len(t) * (t.yy.mean() - c.yy.mean()))
    return dict(fail_cost=fail_cost, succ_cost=succ_cost, total=total, fail_h=fail_h, succ_h=succ_h,
                buyers=buyers, inc=inc, natural=buyers - inc, n=len(t))


# ---------------------------------------------------------------- 圖 1
def fig1(v):
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 4.4), dpi=300)
    fig.patch.set_facecolor(SURFACE)
    plt.rcParams["hatch.color"] = "#ffffff"
    plt.rcParams["hatch.linewidth"] = 0.6

    def stack(ax, segs, title, total_label):
        bottom = 0.0
        tot = sum(s[1] for s in segs)
        for label, val, color, hatch, txt in segs:
            h = val / tot * 100
            ax.bar(0, h, 0.55, bottom=bottom, color=color, edgecolor=SURFACE, linewidth=2,
                   hatch=hatch, zorder=2)
            ax.text(0, bottom + h / 2, label, ha="center", va="center", fontsize=9,
                    color=txt, zorder=3, linespacing=1.35,
                    bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none") if hatch else None)
            bottom += h
        ax.text(0, 103, total_label, ha="center", va="bottom", fontsize=9.5, color=INK, fontweight="bold")
        ax.set_title(title, fontsize=10, color=INK, pad=4)
        ax.set_xlim(-0.45, 0.45)
        ax.set_ylim(0, 112)
        ax.axis("off")

    stack(axes[0], [
        (f"未成交通話\nA${v['fail_cost']:,}\n（{v['fail_cost']/v['total']:.1%}，{v['fail_h']:.1f} 小時）",
         v["fail_cost"], GRAY_DARK, None, "#ffffff"),
        (f"成交通話\nA${v['succ_cost']:,}\n（{v['succ_cost']/v['total']:.1%}，{v['succ_h']:.1f} 小時）",
         v["succ_cost"], GRAY_LIGHT, None, INK),
    ], "看得見：目標組一輪通話成本", f"合計 A${v['total']:,}")
    stack(axes[1], [
        (f"本來就會買的人\n{v['natural']:,} 人（{v['natural']/v['buyers']:.1%}）", v["natural"], ACCENT, "//", INK),
        (f"打了才會買的人\n{v['inc']:,} 人（{v['inc']/v['buyers']:.1%}）", v["inc"], GRAY_MID, None, INK),
    ], f"看不見：{v['buyers']:,} 位成交者", "全部拿到折扣")

    breakeven = v["total"] / v["natural"]
    fig.add_artist(FancyArrowPatch((0.68, 0.10), (0.32, 0.10), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=10, color=INK2, linewidth=0.9))
    fig.text(0.5, 0.045,
             f"每張卡折扣若超過約 A${breakeven:.0f}，右側白給的折扣總額（{v['natural']:,} × 折扣）\n就超過左側整輪通話成本",
             ha="center", va="center", fontsize=8.5, color=INK2, linespacing=1.3)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.14, wspace=0.10)
    out = HERE / "fig1_cost_vs_leakage.png"
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- 圖 2
def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, fs=8.2, lw=0.9, ls="-", color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            zorder=3, linespacing=1.3)


def arrow(ax, p, q, ls="-", color=INK2, lw=1.1):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, color=color, lw=lw,
                                 linestyle=ls, zorder=4, shrinkA=0, shrinkB=0))


def fig2():
    """座標：寬 100 × 高 130；圖寬 6.2 in＝列印寬度。"""
    fig = plt.figure(figsize=(6.2, 8.1), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    fig.patch.set_facecolor(SURFACE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 130)
    ax.axis("off")

    # 圖例
    ax.plot([2, 6], [127, 127], color=INK2, lw=1.1)
    ax.text(7, 127, "一定執行", fontsize=8, va="center", color=INK2)
    ax.plot([19, 23], [127, 127], color=INK2, lw=1.1, linestyle="--")
    ax.text(24, 127, "條件成立才執行", fontsize=8, va="center", color=INK2)
    ax.add_patch(FancyBboxPatch((44, 125.8), 3.2, 2.4, boxstyle="round,pad=0,rounding_size=0.4",
                                fc=ORANGE_FILL, ec=ACCENT, lw=1))
    ax.text(48, 127, "驗證關卡", fontsize=8, va="center", color=INK2)
    ax.add_patch(FancyBboxPatch((61, 125.8), 3.2, 2.4, boxstyle="round,pad=0,rounding_size=0.4",
                                fc="none", ec=INK2, lw=1, linestyle=(0, (1, 1.5))))
    ax.text(65, 127, "Level 1 自動化範圍", fontsize=8, va="center", color=INK2)

    # 開發端泳道
    ax.add_patch(FancyBboxPatch((0.5, 104), 99, 19, boxstyle="round,pad=0,rounding_size=1.2",
                                fc="#eef3fb", ec="none", zorder=0))
    ax.text(2, 120.5, "開發端", fontsize=9.5, color=BLUE, fontweight="bold", va="center")
    box(ax, 2, 106, 28, 11, "客戶資料倉儲\n（假名化）")
    box(ax, 36, 106, 28, 11, "開發環境\n探索分析、模組化組件")
    box(ax, 70, 106, 28, 11, "原始碼版本庫＋註冊文件\n（欄位同表 7 註 1）")
    arrow(ax, (30, 111.5), (36, 111.5))
    arrow(ax, (64, 111.5), (70, 111.5))

    # 運營端泳道
    ax.add_patch(FancyBboxPatch((0.5, 1), 99, 101, boxstyle="round,pad=0,rounding_size=1.2",
                                fc="#f6f5f2", ec="none", zorder=0))
    ax.text(2, 99.5, "運營端", fontsize=9.5, color=GRAY_DARK, fontweight="bold", va="center")
    arrow(ax, (84, 106), (84, 96.5), color=BLUE, lw=1.8)
    ax.text(82.5, 101, "部署整條\n訓練流程", fontsize=8, color=BLUE, ha="right", va="center", fontweight="bold")
    arrow(ax, (10, 106), (10, 88))
    ax.text(11.5, 97.5, "撥號前欄位", fontsize=8, color=INK2, va="center")

    # Level 1 自動化範圍（點線框）
    ax.add_patch(FancyBboxPatch((2.2, 50), 96.3, 46.5, boxstyle="round,pad=0,rounding_size=1.0",
                                fc="none", ec=INK2, lw=1.1, linestyle=(0, (1, 1.5)), zorder=1))
    # 第一列：擷取 → 資料驗證 → 前處理＋訓練
    box(ax, 3, 77, 26, 11, "擷取撥號前欄位\n（依表 5 欄位合約）")
    box(ax, 36, 77, 26, 11, "資料驗證\n（訓練前）", fc=ORANGE_FILL, ec=ACCENT, lw=1.2)
    box(ax, 70, 77, 26, 11, "前處理＋訓練\n（只在訓練資料擬合）")
    arrow(ax, (29, 82.5), (36, 82.5))
    arrow(ax, (62, 82.5), (70, 82.5))
    ax.text(49, 91, "分布偏移 → 照常重訓", fontsize=8, color=INK2, ha="center", va="center")
    arrow(ax, (49, 77), (49, 73.5), color=RED, ls="--")
    ax.text(49, 71.6, "欄位不符 → 停止並通知", fontsize=8, color=RED, ha="center", va="center")
    # 第二列（右 → 左）：模型驗證 → 註冊文件；批次評分
    ax.add_patch(FancyBboxPatch((66, 51), 30, 24, boxstyle="round,pad=0,rounding_size=0.8",
                                fc=ORANGE_FILL, ec=ACCENT, lw=1.2, zorder=2))
    ax.text(81, 65, "模型驗證（晉升前）\n撥號前 AUC ≥ 0.75\n訓練與測試差 ≤ 0.05\n各群 AUC 差 ≤ 0.05\n勝過同期手機規則組\n勝過現行模型",
            ha="center", va="center", fontsize=8, color=INK, zorder=3, linespacing=1.3)
    ax.text(81, 53.3, "未過 → 不晉升、保留現行版", ha="center", va="center", fontsize=7.8, color=RED, zorder=3)
    arrow(ax, (83, 77), (83, 75))
    box(ax, 36, 58, 24, 10, "註冊文件\n（候選）")
    arrow(ax, (66, 63), (60, 63), ls="--")
    box(ax, 3, 55, 26, 15, "批次評分\n（每個外撥日前）\n欄位異常 → 改用\n手機規則名單", fs=8)

    # 人工 go/no-go（點線框外）
    box(ax, 30, 38, 34, 8, "人工 go/no-go：市場總監＋法遵", fs=8)
    arrow(ax, (48, 58), (48, 46))
    arrow(ax, (30, 42), (20, 55), ls="--")
    ax.text(66, 42, "第 12 週決定是否擴大（表 9）；\n之後每次新版晉升；\n核准後狀態改為「生產」",
            fontsize=7.8, color=INK2, va="center", linespacing=1.25)

    # 交付與回饋
    box(ax, 2, 18, 40, 15, "名單：依當日產能截斷\n分數＋入選原因＋對照組／隨機外撥組標記\n已排除拒接行銷名單", fs=8)
    arrow(ax, (10, 55), (10, 33))
    box(ax, 56, 18, 42, 15, "呼叫中心撥號系統\n（對照組只評分、不外撥）", fs=8)
    arrow(ax, (42, 25.5), (56, 25.5))
    box(ax, 56, 3, 42, 12, "外撥結果＋對照組申辦結果\n→ 回寫資料倉儲成為新標籤", fs=8)
    arrow(ax, (77, 18), (77, 15))
    box(ax, 3.5, 2, 47.5, 14,
        "監控（表 10）：輸入分布、名單轉換率、增量、分群差距\n觸發重訓：① 排程（每輪結束）② 輸入分布漂移\n"
        "③ 效能低於表 4 門檻（先改手機規則，重訓後回影子模式）\n④ 資格標準變更（先影子評分）", fs=7.4)
    arrow(ax, (56, 9), (51, 9))
    # 觸發 → 擷取（沿左緣）
    ax.plot([0.9, 0.9], [9, 82.5], color=INK2, lw=1.1, zorder=4, linestyle="--")
    ax.plot([0.9, 3.5], [9, 9], color=INK2, lw=1.1, zorder=4, linestyle="--")
    arrow(ax, (0.9, 82.5), (3, 82.5), ls="--")

    out = HERE / "fig2_mlops_level1.png"
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    return out


if __name__ == "__main__":
    v = numbers()
    print(v)
    print(fig1(v))
    print(fig2())
