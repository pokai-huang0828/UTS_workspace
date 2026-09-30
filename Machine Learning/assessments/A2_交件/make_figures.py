"""產生 A2 報告的圖 1、圖 2（PNG, 300 dpi）。數字全部由 TeleMarketing.csv 重算。"""
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

matplotlib.rcParams["font.family"] = ["Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).resolve().parent
CSV = HERE.parent.parent / "data" / "bank_x" / "TeleMarketing.csv"

INK = "#0b0b0b"
INK2 = "#52514e"
SURFACE = "#ffffff"
ACCENT = "#eb6834"
GRAY_DARK = "#5f5e5a"
GRAY_LIGHT = "#b9b7b0"
GRAY_MID = "#8d8b85"
HOURLY = 50  # 示意假設：時薪 A$50


def numbers():
    d = pd.read_csv(CSV)
    d["yy"] = (d["y"] == "yes").astype(int)
    t, c = d[d.campaign == 1], d[d.campaign == 0]
    fail_cost = round(t.loc[t.yy == 0, "duration"].sum() / 3600 * HOURLY)
    total = round(t["duration"].sum() / 3600 * HOURLY)
    succ_cost = total - fail_cost  # 取整後讓兩段加總等於合計
    buyers = int(t.yy.sum())
    inc = len(t) * (t.yy.mean() - c.yy.mean())
    return dict(fail_cost=fail_cost, succ_cost=succ_cost, total=fail_cost + succ_cost,
                buyers=buyers, inc=round(inc), natural=buyers - round(inc), n=len(t))


def fig1(v):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.8), dpi=300)
    fig.patch.set_facecolor(SURFACE)
    width = 0.5

    def stack(ax, segs, title, total_label):
        bottom = 0.0
        tot = sum(s[1] for s in segs)
        for label, val, color, hatch, txt in segs:
            h = val / tot * 100
            ax.bar(0, h, width, bottom=bottom, color=color, edgecolor=SURFACE, linewidth=2,
                   hatch=hatch, zorder=2)
            ax.text(0, bottom + h / 2, label, ha="center", va="center", fontsize=9.5,
                    color=txt, zorder=3, linespacing=1.4,
                    bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none") if hatch else None)
            bottom += h
        ax.text(0, 103, total_label, ha="center", va="bottom", fontsize=10, color=INK, fontweight="bold")
        ax.set_title(title, fontsize=11, color=INK, pad=4, loc="center")
        ax.set_xlim(-0.45, 0.45)
        ax.set_ylim(0, 112)
        ax.axis("off")

    stack(axes[0], [
        (f"未成交通話\nA${v['fail_cost']:,.0f}（{v['fail_cost']/v['total']:.1%}）", v["fail_cost"], GRAY_DARK, None, "#ffffff"),
        (f"成交通話\nA${v['succ_cost']:,.0f}（{v['succ_cost']/v['total']:.1%}）", v["succ_cost"], GRAY_LIGHT, None, INK),
    ], "看得見：目標組一輪通話成本", f"合計 A${v['total']:,.0f}")

    plt.rcParams["hatch.color"] = "#ffffff"
    plt.rcParams["hatch.linewidth"] = 0.6
    stack(axes[1], [
        (f"本來就會買的人\n{v['natural']:,} 人（{v['natural']/v['buyers']:.1%}）", v["natural"], ACCENT, "//", INK),
        (f"打了才會買的人\n{v['inc']:,} 人（{v['inc']/v['buyers']:.1%}）", v["inc"], GRAY_MID, None, "#ffffff"),
    ], f"看不見：{v['buyers']:,} 位成交者", "全部拿到折扣")

    breakeven = v["total"] / v["natural"]
    fig.text(0.5, 0.075,
             f"每張卡折扣若超過約 A${breakeven:.0f}，右側白給的折扣總額（{v['natural']:,} × 折扣）就超過左側整輪通話成本",
             ha="center", va="center", fontsize=9, color=INK2)
    arrow = FancyArrowPatch((0.66, 0.12), (0.34, 0.12), transform=fig.transFigure,
                            arrowstyle="-|>", mutation_scale=10, color=INK2, linewidth=0.8)
    fig.add_artist(arrow)
    fig.text(0.5, 0.025, f"依試點原始資料（目標組 {v['n']:,} 人）；通話成本依示意時薪 A$50、只計通話時間",
             ha="center", va="center", fontsize=7.5, color=INK2)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.17, wspace=0.12)
    out = HERE / "fig1_cost_vs_leakage.png"
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    return out


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, fs=7.2, lw=0.9, ls="-", bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.012",
                                fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK,
            zorder=3, linespacing=1.35, fontweight="bold" if bold else "normal")


def diamond(ax, cx, cy, w, h, text, fs=7.0):
    ax.add_patch(Polygon([(cx - w / 2, cy), (cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2)],
                         closed=True, fc="#fff4ee", ec=ACCENT, lw=1.0, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK, zorder=3, linespacing=1.3)


def arrow(ax, p, q, ls="-", color=INK2, rad=0.0, lw=0.9):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=8, color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=1))


def fig2():
    fig, ax = plt.subplots(figsize=(10.5, 6.6), dpi=300)
    fig.patch.set_facecolor(SURFACE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # 泳道
    ax.add_patch(FancyBboxPatch((0.005, 0.74), 0.99, 0.23, boxstyle="round,pad=0,rounding_size=0.01",
                                fc="#eef3fb", ec="none", zorder=0))
    ax.add_patch(FancyBboxPatch((0.005, 0.02), 0.99, 0.70, boxstyle="round,pad=0,rounding_size=0.01",
                                fc="#f6f5f2", ec="none", zorder=0))
    ax.text(0.015, 0.945, "開發端", fontsize=9, color="#2a78d6", fontweight="bold", va="center")
    ax.text(0.015, 0.695, "運營端", fontsize=9, color=GRAY_DARK, fontweight="bold", va="center")

    # 開發端
    box(ax, 0.03, 0.775, 0.12, 0.11, "客戶資料倉儲\n（假名化）", fc="#ffffff")
    box(ax, 0.22, 0.775, 0.20, 0.11, "開發環境\n探索分析、模組化組件")
    box(ax, 0.49, 0.775, 0.22, 0.11, "原始碼版本庫＋註冊文件\n（欄位同表 7 註 1）")
    arrow(ax, (0.15, 0.83), (0.22, 0.83))
    arrow(ax, (0.42, 0.83), (0.49, 0.83))
    ax.text(0.61, 0.715, "部署整條訓練流程", fontsize=7, color="#2a78d6", va="center", fontweight="bold")
    arrow(ax, (0.60, 0.775), (0.60, 0.665), color="#2a78d6", lw=1.6)

    # Level 1 自動化範圍
    ax.add_patch(FancyBboxPatch((0.03, 0.30), 0.94, 0.36, boxstyle="round,pad=0,rounding_size=0.01",
                                fc="none", ec=INK2, lw=1.0, linestyle=(0, (4, 3)), zorder=1))
    ax.text(0.045, 0.64, "Level 1 自動化範圍", fontsize=7.5, color=INK2, va="center")

    y = 0.49
    box(ax, 0.045, y - 0.06, 0.12, 0.12, "擷取撥號前欄位\n（依表 5「預測\n當下可得？」欄）")
    box(ax, 0.19, y - 0.06, 0.11, 0.12, "資料驗證\n（訓練前）", fc="#fff4ee", ec=ACCENT, lw=1.1)
    box(ax, 0.325, y - 0.05, 0.10, 0.10, "前處理＋訓練")
    box(ax, 0.445, y - 0.12, 0.165, 0.24,
        "模型驗證（晉升前）\n撥號前 AUC ≥ 0.75\n訓練與測試差 ≤ 0.05\n各群 AUC 差 ≤ 0.05\n勝過同期手機規則組\n勝過現行模型",
        fc="#fff4ee", ec=ACCENT, fs=6.4, lw=1.1)
    box(ax, 0.625, y - 0.05, 0.11, 0.10, "註冊文件\n（候選）")
    box(ax, 0.83, y - 0.06, 0.12, 0.12, "批次評分\n（每個外撥日前）")
    arrow(ax, (0.165, y), (0.19, y))
    arrow(ax, (0.30, y), (0.325, y))
    arrow(ax, (0.425, y), (0.445, y))
    arrow(ax, (0.61, y), (0.625, y))
    # 資料驗證 → 停止
    ax.text(0.245, 0.345, "欄位不符 → 停止並通知", fontsize=6.5, color="#c0392b", ha="center")
    arrow(ax, (0.245, y - 0.06), (0.245, 0.365), color="#c0392b")
    ax.text(0.245, y + 0.075, "分布偏移 → 照常重訓", fontsize=6.3, color=INK2, ha="center")

    # 人工 go/no-go（虛線框外）
    box(ax, 0.72, 0.68, 0.19, 0.05, "人工 go/no-go：市場總監＋法遵", fc="#ffffff", ec=INK2, fs=6.8, ls="--")
    arrow(ax, (0.70, y + 0.05), (0.76, 0.68), ls="--")
    arrow(ax, (0.87, 0.68), (0.89, y + 0.06), ls="--")
    ax.text(0.815, 0.745, "首次上線＝第 12 週（表 9）；之後每次晉升", fontsize=6.0, color=INK2, ha="center")

    # 交付與回饋
    box(ax, 0.62, 0.075, 0.33, 0.14,
        "名單：依當日產能截斷；分數＋入選原因\n＋對照組／隨機外撥組標記；已排除拒接行銷名單\n→ 呼叫中心撥號系統（對照組只評分、不外撥）", fs=6.8)
    arrow(ax, (0.89, y - 0.06), (0.89, 0.215))
    box(ax, 0.33, 0.075, 0.24, 0.14, "外撥結果＋對照組申辦結果\n→ 回寫資料倉儲成為新標籤", fs=6.8)
    arrow(ax, (0.62, 0.145), (0.57, 0.145))
    box(ax, 0.03, 0.075, 0.25, 0.14,
        "監控（表 10）：輸入分布、名單轉換率、\n相對對照組的增量、分群差距\n觸發：① 排程 ② 效能低於表 4 門檻\n③ 資格標準變更", fs=6.6)
    arrow(ax, (0.33, 0.145), (0.28, 0.145))
    arrow(ax, (0.105, 0.215), (0.105, y - 0.06), color=ACCENT, lw=1.3)
    ax.text(0.115, 0.265, "觸發重訓", fontsize=6.5, color=ACCENT)

    # 圖例
    ax.plot([0.04, 0.075], [0.985, 0.985], color=INK2, lw=0.9)
    ax.text(0.08, 0.985, "自動", fontsize=6.5, va="center", color=INK2)
    ax.plot([0.12, 0.155], [0.985, 0.985], color=INK2, lw=0.9, linestyle="--")
    ax.text(0.16, 0.985, "人工", fontsize=6.5, va="center", color=INK2)
    ax.add_patch(FancyBboxPatch((0.20, 0.977), 0.014, 0.016, boxstyle="round,pad=0,rounding_size=0.003",
                                fc="#fff4ee", ec=ACCENT, lw=0.8))
    ax.text(0.22, 0.985, "驗證關卡", fontsize=6.5, va="center", color=INK2)

    out = HERE / "fig2_mlops_level1.png"
    fig.savefig(out, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return out


if __name__ == "__main__":
    v = numbers()
    print(v)
    print(fig1(v))
    print(fig2())
