"""11/11 組會簡報用的 3 張圖(可重跑):python build_ab_meeting_figures.py
輸出到 Innovation Studio/notes/figures/。所有數字都在下面的常數區,圖只是把常數畫出來。
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

# ---------------- 常數區(每個常數後面註解來源) ----------------
# 三面向分數(1-5,5 最好;我們的判斷,不是老師給的)順序:A、B①、B②
SCORES = {
    "可執行性": (4, 3, 2),  # notes/16_方案AB_深度分析.md L15
    "難度(越高越好做)": (4, 3, 2),  # 同檔 L16
    "資料完整度": (3, 2, 2),  # 同檔 L17
}
OPTIONS = ("A", "B①", "B②")  # 同檔 L13 表頭

# 四個候選的預估總分區間(滿分 80;照評分表推的估計,不是老師給的分數)
RANGES = [  # (名稱, 下限, 上限)  來源:notes/16 L33-L36
    ("A+B①", 63, 74),  # L33
    ("只做 A", 62, 74),  # L34
    ("只做 B①", 57, 69),  # L35
    ("只做 B②", 51, 65),  # L36
]

# 新上架房源逐層篩出(雪梨, 墨爾本)
FUNNEL = [  # 來源:notes/17_定題與三層目標_v1.md §3;鍵名在 notes/raw/airbnb_new_listing_definition_2026-11-11.json cities.<城>.*
    ("同類且有價樣本", 6639, 8223),  # n_scope_price
    ("新上架(首評 12 個月內)", 2028, 2056),  # windows.12m.n_new
    ("且房東在本城只有這一間", 688, 713),  # windows.12m.n_new_single_host
    ("且當房東 12 個月以內", 444, 514),  # windows.12m.n_new_single_and_tenure_le_window
]
FUNNEL_NOTE = "年資欄官方說明還沒查,加註使用"  # 17 §3 ⚠️;notes/raw/aim_review_2026-11-11.md L30

# ---------------- 樣式 ----------------
BLUE, ORANGE, GRAY = "#1f5fa8", "#e07b1a", "#9aa0a6"
DARK = "#222222"
OUT = Path(__file__).resolve().parent.parent / "notes" / "figures"
DATE = "2026-11-11"

def setup_font():
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Microsoft JhengHei", "Microsoft YaHei", "SimHei"):
        if name in have:
            plt.rcParams["font.sans-serif"] = [name]
            break
    else:
        raise SystemExit("找不到中文字型(Microsoft JhengHei / Microsoft YaHei / SimHei)")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.size"] = 12

def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRAY); ax.spines["bottom"].set_color(GRAY)
    ax.tick_params(colors=DARK, labelsize=12)

def title(fig, main, sub):
    fig.text(0.02, 0.96, main, fontsize=17, fontweight="bold", color=DARK, va="top")
    fig.text(0.02, 0.885, sub, fontsize=12, color="#555555", va="top")

def fig_scores():
    fig, ax = plt.subplots(figsize=(8.75, 5.0), dpi=160)
    cols = (BLUE, ORANGE, GRAY)
    h = 0.24
    cats = list(SCORES)
    for gi, cat in enumerate(cats):
        for oi, v in enumerate(SCORES[cat]):
            y = gi + (oi - 1) * h
            ax.barh(y, v, height=h * 0.9, color=cols[oi], label=OPTIONS[oi] if gi == 0 else None)
            ax.text(v + 0.06, y, str(v), va="center", fontsize=12, color=DARK)
    ax.set_yticks(range(len(cats))); ax.set_yticklabels(cats)
    ax.invert_yaxis(); ax.set_xlim(0, 5); ax.set_xticks(range(0, 6))
    ax.legend(loc="lower right", frameon=False, fontsize=12, ncol=3)
    style(ax)
    fig.subplots_adjust(left=0.22, right=0.96, top=0.78, bottom=0.1)
    title(fig, "A、B①、B② 三個面向的分數", "我們的判斷(5 最好),不是課程給的分數;B① 是整合時推的")
    fig.savefig(OUT / f"ab_scores_{DATE}.png", facecolor="white")

def fig_ranges():
    fig, ax = plt.subplots(figsize=(8.75, 4.6), dpi=160)
    for i, (name, lo, hi) in enumerate(RANGES):
        c = BLUE if i == 0 else GRAY
        ax.barh(i, hi - lo, left=lo, height=0.5, color=c)
        ax.text(hi + 0.4, i, f"{lo}–{hi}", va="center", fontsize=13, color=DARK)
    ax.set_yticks(range(len(RANGES))); ax.set_yticklabels([r[0] for r in RANGES])
    ax.invert_yaxis(); ax.set_xlim(45, 80); ax.set_xlabel("預估總分(滿分 80;橫軸從 45 分起)", fontsize=12)
    style(ax)
    fig.subplots_adjust(left=0.16, right=0.96, top=0.78, bottom=0.16)
    title(fig, "四個候選的預估總分區間", "照評分表推的估計,不是老師給的分數;滿分 80")
    fig.savefig(OUT / f"ab_expected_range_{DATE}.png", facecolor="white")

def fig_funnel():
    fig, ax = plt.subplots(figsize=(8.75, 5.2), dpi=160)
    h = 0.34
    for i, (name, syd, mel) in enumerate(FUNNEL):
        for v, dy, c, lab in ((syd, -h / 2, BLUE, "雪梨"), (mel, h / 2, ORANGE, "墨爾本")):
            y = i + dy
            ax.barh(y, v, height=h * 0.92, color=c, label=lab if i == 0 else None)
            ax.text(v + 120, y, f"{v:,}", va="center", fontsize=12, color=DARK)
    ax.text(FUNNEL[-1][2] + 900, len(FUNNEL) - 1 + 0.0, FUNNEL_NOTE, va="center", fontsize=13, color="#555555")
    ax.set_yticks(range(len(FUNNEL))); ax.set_yticklabels([f[0] for f in FUNNEL])
    ax.invert_yaxis(); ax.set_xlim(0, 11500); ax.set_xlabel("房源筆數", fontsize=12)
    ax.legend(loc="lower right", frameon=False, fontsize=12)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
    style(ax)
    fig.subplots_adjust(left=0.27, right=0.97, top=0.8, bottom=0.13)
    title(fig, "「新上架房源」從有價樣本逐層篩出", "雪梨、墨爾本;每一層都是上一層的子集")
    fig.savefig(OUT / f"new_listing_funnel_{DATE}.png", facecolor="white")

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    setup_font()
    fig_scores(); fig_ranges(); fig_funnel()
    print("ok ->", OUT)
