"""墨爾本 2024-01 到 2026-09:用手上 Inside Airbnb 2026-09-16 這一批(listings + 評論摘要檔)能看到什麼。
只讀本機快取,不上網。輸出:彙總 JSON、三張圖、短報告 md。可重跑。
篩選定義、price 解析直接 import 自 airbnb_ab_field_inventory.py(同一份定義)。
"""
import collections
import csv
import gzip
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from airbnb_ab_field_inventory import is_scope, num  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = HERE.parents[1]
CACHE = ROOT / "scratchpad/airbnb_2024_two_cities"
PROFILE = ROOT / "Innovation Studio/notes/raw/airbnb_two_city_profile_2026-11-07.json"
LINKS = CACHE / "official_links.json"
DATE = "2026-11-11"
OUT_JSON = ROOT / f"Innovation Studio/notes/raw/airbnb_melbourne_2024_2026_{DATE}.json"
OUT_MD = ROOT / f"Innovation Studio/notes/raw/airbnb_melbourne_2024_2026_{DATE}.md"
FIG = ROOT / "Innovation Studio/notes/figures"
BLUE, ORANGE, GRAY, DARK = "#1f5fa8", "#e07b1a", "#9aa0a6", "#222222"
SUB = "只含 2026-09 還在架上的房源;評論數不是訂單數"
CUTOFF_12M = "2025-09-18"  # 與 airbnb_new_listing_definition_2026-11-11.json windows.12m.cutoff_inclusive 相同
EXPECT = dict(rows=25715, scope=10940, scope_price=8223)


def ym_range(start, end):
    y, m = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    out = []
    while (y, m) <= (ey, em):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def pct(a, b):
    return round(100 * (a / b - 1), 1)


# ---------------- 讀資料與對帳 ----------------
def load():
    with gzip.open(CACHE / "melbourne_listings.csv.gz", "rt", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == EXPECT["rows"], ("listings 列數", len(rows))
    scope = [r for r in rows if is_scope(r)]
    scope_price = [r for r in scope if r["price"]]
    assert len(scope) == EXPECT["scope"], ("篩選樣本", len(scope))
    assert len(scope_price) == EXPECT["scope_price"], ("篩選且有價", len(scope_price))
    return rows, scope, scope_price


def scan_reviews(all_ids, scope_ids):
    """逐月/逐年計數;不保留評論文字(評論摘要檔本來就只有 listing_id 與 date)。"""
    path = CACHE / "melbourne_reviews_summary.csv"
    assert path.exists(), f"找不到墨爾本評論檔: {path}"
    month_all, month_scope = collections.Counter(), collections.Counter()
    year_all, year_scope = collections.Counter(), collections.Counter()
    first = {}
    active = collections.defaultdict(lambda: collections.defaultdict(set))  # year -> 'all'/'scope' -> ids
    n_rows = n_dated = orphan = 0
    with path.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            n_rows += 1
            d, lid = r["date"], r["listing_id"]
            if not d:
                continue
            n_dated += 1
            m, y = d[:7], d[:4]
            in_scope = lid in scope_ids
            month_all[m] += 1
            year_all[y] += 1
            if in_scope:
                month_scope[m] += 1
                year_scope[y] += 1
            if lid not in all_ids:
                orphan += 1
                continue
            active[y]["all"].add(lid)
            if in_scope:
                active[y]["scope"].add(lid)
            if lid not in first or d < first[lid]:
                first[lid] = d
    return dict(month_all=month_all, month_scope=month_scope, year_all=year_all, year_scope=year_scope,
                first=first, active=active, n_rows=n_rows, n_dated=n_dated, orphan=orphan)


# ---------------- 計算 ----------------
def compute():
    rows, scope, scope_price = load()
    all_ids = {r["id"] for r in rows}
    scope_ids = {r["id"] for r in scope}
    sp_ids = {r["id"] for r in scope_price}
    rv = scan_reviews(all_ids, scope_ids)
    prof = json.loads(PROFILE.read_text(encoding="utf-8"))["cities"]["melbourne"]
    first = rv["first"]

    months = ym_range("2024-01", "2026-09")
    complete = months[:-1]  # 2026-09 只到抓取日 09-18
    fm_all, fm_scope = collections.Counter(), collections.Counter()
    fy_all, fy_scope = collections.Counter(), collections.Counter()
    for lid, d in first.items():
        fm_all[d[:7]] += 1
        fy_all[d[:4]] += 1
        if lid in scope_ids:
            fm_scope[d[:7]] += 1
            fy_scope[d[:4]] += 1

    monthly = {m: dict(reviews_all=rv["month_all"][m], reviews_scope=rv["month_scope"][m],
                       new_listings_all=fm_all[m], new_listings_scope=fm_scope[m],
                       complete=(m != months[-1])) for m in months}
    yearly = {}
    for y in ("2024", "2025", "2026"):
        yearly[y] = dict(reviews_all=rv["year_all"][y], reviews_scope=rv["year_scope"][y],
                         active_listings_all=len(rv["active"][y]["all"]),
                         active_listings_scope=len(rv["active"][y]["scope"]),
                         first_review_listings_all=fy_all[y], first_review_listings_scope=fy_scope[y])
    since = dict(reviews_all=sum(rv["year_all"][y] for y in ("2024", "2025", "2026")),
                 reviews_scope=sum(rv["year_scope"][y] for y in ("2024", "2025", "2026")))
    recon = dict(
        profile_reviews_2024=prof["reviews_by_year"]["2024"], mine_reviews_2024=yearly["2024"]["reviews_all"],
        diff_2024=yearly["2024"]["reviews_all"] - prof["reviews_by_year"]["2024"],
        profile_since_2024=prof["reviews_since_2024"], mine_since_2024=since["reviews_all"],
        diff_since_2024=since["reviews_all"] - prof["reviews_since_2024"],
        profile_review_rows_with_date=prof["review_rows_with_date"], mine_review_rows_with_date=rv["n_dated"],
        profile_review_date_max=prof["review_date_max"], review_file_rows=rv["n_rows"],
        reviews_of_listings_not_in_listings_file=rv["orphan"])

    # 月走勢:完整月份 top/bottom 3
    ranked = sorted(complete, key=lambda m: monthly[m]["reviews_all"])
    bottom3 = [dict(month=m, reviews_all=monthly[m]["reviews_all"]) for m in ranked[:3]]
    top3 = [dict(month=m, reviews_all=monthly[m]["reviews_all"]) for m in ranked[::-1][:3]]
    jan_aug = lambda y: sum(monthly[f"{y}-{k:02d}"]["reviews_all"] for k in range(1, 9))
    growth = dict(y2025_vs_y2024_pct=pct(yearly["2025"]["reviews_all"], yearly["2024"]["reviews_all"]),
                  jan_aug_2026_vs_2025_pct=pct(jan_aug(2026), jan_aug(2025)),
                  jan_aug_2025=jan_aug(2025), jan_aug_2026=jan_aug(2026))

    # 淡旺季:2024、2025 兩個完整年度,指數 = 當月 / 該年月平均 * 100
    idx = {}
    for y in (2024, 2025):
        v = [monthly[f"{y}-{k:02d}"]["reviews_all"] for k in range(1, 13)]
        mean = sum(v) / 12
        idx[y] = [round(100 * x / mean, 1) for x in v]
    corr = float(np.corrcoef(idx[2024], idx[2025])[0, 1])
    avg_idx = [round((a + b) / 2, 1) for a, b in zip(idx[2024], idx[2025])]
    order = sorted(range(12), key=lambda i: avg_idx[i])
    season = dict(index_2024={str(i + 1): idx[2024][i] for i in range(12)},
                  index_2025={str(i + 1): idx[2025][i] for i in range(12)},
                  avg_index={str(i + 1): avg_idx[i] for i in range(12)},
                  corr_2024_2025=round(corr, 3),
                  high3_months=[order[-1 - j] + 1 for j in range(3)], low3_months=[order[j] + 1 for j in range(3)])

    # 新上架 12 個月口徑對照(截止 2025-09-18 含)
    fr_field = {r["id"]: r["first_review"] for r in scope_price}
    new12 = dict(
        cutoff_inclusive=CUTOFF_12M,
        all_listings_summary_first=sum(1 for d in first.values() if d >= CUTOFF_12M),
        scope_summary_first=sum(1 for lid, d in first.items() if lid in scope_ids and d >= CUTOFF_12M),
        scope_price_summary_first=sum(1 for lid, d in first.items() if lid in sp_ids and d >= CUTOFF_12M),
        scope_price_listings_field=sum(1 for v in fr_field.values() if v and v >= CUTOFF_12M),
        expected_known=2056,
        scope_price_no_review_in_summary=sum(1 for lid in sp_ids if lid not in first),
        scope_price_no_first_review_field=sum(1 for v in fr_field.values() if not v),
        scope_price_field_vs_summary_mismatch=sum(1 for lid, v in fr_field.items()
                                                  if v and lid in first and v != first[lid]))

    # 價格:只有 2026-09 一期,篩選且有價
    prices, by_nb, unparsed = [], collections.defaultdict(list), 0
    for r in scope_price:
        p = num(r["price"])
        if p is None:
            unparsed += 1
            continue
        prices.append(p)
        by_nb[r["neighbourhood_cleansed"]].append(p)
    p25, p50, p75 = (float(x) for x in np.percentile(prices, [25, 50, 75]))
    top10 = sorted(by_nb.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
    price = dict(sample="篩選且有價", n=len(prices), n_unparsed=unparsed, p25=round(p25, 1), median=statistics.median(prices),
                 p75=round(p75, 1), percentile_method="numpy linear", unit="掛牌價/晚,當地幣別,2026-09 一期",
                 n_neighbourhoods=len(by_nb),
                 top10_neighbourhoods=[dict(neighbourhood=k, n=len(v), median=statistics.median(v)) for k, v in top10])

    return dict(
        batch="2026-09-16", scope_id="IS-1111-BR-MEL", city="melbourne",
        definitions=dict(
            sample_filter="整套(Entire home/apt)/1-2 房/可住 2-4 人/最低 1-7 晚;定義見 airbnb_ab_field_inventory.is_scope",
            n_listings=len(rows), n_scope=len(scope), n_scope_price=len(scope_price),
            reviews_file="visualisations/reviews.csv(評論摘要:listing_id + date)",
            review_date_max=prof["review_date_max"], last_month_complete=False,
            first_review_def="該房源在評論摘要檔裡最早的一則評論日期(只算 2026-09 還在架上的房源)"),
        recon=recon, yearly=yearly, since_2024=since, growth=growth, monthly=monthly,
        top3_months=top3, bottom3_months=bottom3, seasonality=season, new_12m=new12, price=price)


# ---------------- 圖 ----------------
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


def new_fig(main, sub):
    fig = plt.figure(figsize=(14, 6.8), dpi=100, facecolor="white")
    fig.text(0.02, 0.97, main, fontsize=17, fontweight="bold", color=DARK, va="top")
    fig.text(0.02, 0.905, sub, fontsize=12, color="#555555", va="top")
    ax = fig.add_axes([0.075, 0.12, 0.905, 0.68])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRAY)
    ax.spines["bottom"].set_color(GRAY)
    ax.tick_params(colors=DARK, labelsize=12)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    return fig, ax


def fig_monthly(D):
    months = list(D["monthly"])
    ya = [D["monthly"][m]["reviews_all"] for m in months]
    ys = [D["monthly"][m]["reviews_scope"] for m in months]
    x = list(range(len(months)))
    fig, ax = new_fig("墨爾本每月評論數(2024-01 到 2026-09)", SUB)
    for y, c, lab in ((ya, BLUE, f"全體 {D['definitions']['n_listings']:,} 間"),
                      (ys, ORANGE, f"篩選樣本 {D['definitions']['n_scope']:,} 間")):
        ax.plot(x[:-1], y[:-1], color=c, lw=2.2, marker="o", ms=4, label=lab)
        ax.plot(x[-2:], y[-2:], color=c, lw=2.2, ls="--")
        ax.plot(x[-1], y[-1], marker="o", ms=9, mfc="white", mec=c, mew=2)
    ax.annotate("2026-09 只到 09-18\n(不完整,不能跟別月比)", xy=(x[-1], ya[-1]), xytext=(x[-1] - 7.5, ya[-1] - 4200),
                fontsize=12, color=DARK, arrowprops=dict(arrowstyle="->", color=GRAY))
    top, bot = D["top3_months"][0], D["bottom3_months"][0]
    for d, dy in ((top, 700), (bot, -3000)):
        i = months.index(d["month"])
        ax.annotate(f"{d['month']}\n{d['reviews_all']:,}", xy=(i, d["reviews_all"]), xytext=(i, d["reviews_all"] + dy),
                    ha="center", fontsize=12, color=DARK)
    ax.set_xticks(x[::3])
    ax.set_xticklabels(months[::3])
    ax.set_ylim(0, max(ya) * 1.18)
    ax.set_ylabel("評論數(則/月)", fontsize=12)
    ax.grid(axis="y", color="#e5e5e5")
    ax.legend(loc="upper left", frameon=False, fontsize=12)
    fig.savefig(FIG / f"melbourne_reviews_monthly_{DATE}.png", facecolor="white")
    plt.close(fig)


def fig_season(D):
    s = D["seasonality"]
    a, b = [s["index_2024"][str(i)] for i in range(1, 13)], [s["index_2025"][str(i)] for i in range(1, 13)]
    fig, ax = new_fig("墨爾本評論的淡旺季:各月相對全年月平均的指數(100 = 平均)", SUB)
    x = np.arange(12)
    w = 0.38
    b1 = ax.bar(x - w / 2, a, w, color=BLUE, label="2024 年")
    b2 = ax.bar(x + w / 2, b, w, color=ORANGE, label="2025 年")
    for bars in (b1, b2):
        for r in bars:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 1.5, f"{r.get_height():.0f}", ha="center", fontsize=12, color=DARK)
    ax.axhline(100, color=GRAY, ls="--", lw=1.2, label="100 = 平均")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{i}月" for i in range(1, 13)])
    ax.set_ylim(0, max(a + b) * 1.15)
    ax.set_ylabel("指數", fontsize=12)
    ax.legend(loc="upper left", frameon=False, fontsize=12, ncol=3)
    fig.savefig(FIG / f"melbourne_seasonality_{DATE}.png", facecolor="white")
    plt.close(fig)


def fig_new(D):
    months = list(D["monthly"])
    v = [D["monthly"][m]["new_listings_all"] for m in months]
    x = np.arange(len(months))
    fig, ax = new_fig("墨爾本每月「首評落在該月」的房源數(新上架的代理)", "用第一則評論的月份代理上架時間;全體 2026-09 還在架上的房源")
    ax.bar(x[:-1], v[:-1], 0.72, color=BLUE)
    ax.bar(x[-1], v[-1], 0.72, facecolor="white", edgecolor=BLUE, hatch="//", lw=1.6)
    for i, n in enumerate(v):
        ax.text(i, n + max(v) * 0.012, f"{n}", ha="center", fontsize=12, color=DARK)
    ax.annotate("2026-09 只到 09-18\n(不完整)", xy=(x[-1], v[-1]), xytext=(x[-1] - 0.8, max(v) * 0.86), ha="center",
                fontsize=12, color=DARK, arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.set_xticks(x[::3])
    ax.set_xticklabels(months[::3])
    ax.set_ylim(0, max(v) * 1.12)
    ax.set_ylabel("首評落在該月的房源數", fontsize=12)
    ax.grid(axis="y", color="#e5e5e5")
    ax.set_axisbelow(True)
    fig.savefig(FIG / f"melbourne_new_listings_{DATE}.png", facecolor="white")
    plt.close(fig)


# ---------------- 報告 ----------------
def n(v):
    return f"{v:,}"


def build_md(D):
    Y, rc, S, N, P = D["yearly"], D["recon"], D["seasonality"], D["new_12m"], D["price"]
    g, sin = D["growth"], D["since_2024"]
    df = D["definitions"]
    links = json.loads(LINKS.read_text(encoding="utf-8")) if LINKS.exists() else None
    corr = S["corr_2024_2025"]
    corr_word = "很像" if corr >= 0.8 else ("有點像" if corr >= 0.5 else "不太像")
    mon = lambda lst: "、".join(f"{k}月" for k in lst)
    top = "、".join(f"{d['month']}({n(d['reviews_all'])})" for d in D["top3_months"])
    bot = "、".join(f"{d['month']}({n(d['reviews_all'])})" for d in D["bottom3_months"])
    sg = lambda v: f"+{v}%" if v >= 0 else f"{v}%"
    L = []
    A = L.append
    A("# 墨爾本 2024–2026:手上這批看得到什麼(2026-11-11)")
    A("")
    A("**結論:這批看得到「現在還在架上的房源」在 2024-01 到 2026-09 留下的評論量、淡旺季、新上架代理;看不到當時的價格、已下架的房源、真實訂單與入住率。**")
    A("")
    A(f"資料:Inside Airbnb 墨爾本 2026-09-16 批。listings {n(df['n_listings'])} 列;篩選樣本 {n(df['n_scope'])}(整套 / 1–2 房 / 2–4 人 / 最低 1–7 晚);其中有價 {n(df['n_scope_price'])}。評論檔最後一則是 {df['review_date_max']},所以 2026 年只到 9 月 18 日。")
    A("")
    A("## 1. 每年總覽")
    A(f"結論:評論量 2025 年比 2024 年 {sg(g['y2025_vs_y2024_pct'])};2026 年 1–8 月比 2025 年 1–8 月 {sg(g['jan_aug_2026_vs_2025_pct'])}(只含還在架上的房源,早年被低估,成長率會偏高)。")
    A("")
    A("| 年 | 評論數 全體 | 評論數 篩選樣本 | 有評論的房源 全體 | 有評論的房源 篩選 | 首評落在當年 全體 | 首評落在當年 篩選 |")
    A("|---|---|---|---|---|---|---|")
    for y, lab in (("2024", "2024"), ("2025", "2025"), ("2026", "2026(到 09-18)")):
        r = Y[y]
        A(f"| {lab} | {n(r['reviews_all'])} | {n(r['reviews_scope'])} | {n(r['active_listings_all'])} | {n(r['active_listings_scope'])} | {n(r['first_review_listings_all'])} | {n(r['first_review_listings_scope'])} |")
    A(f"| 2024 起累計 | {n(sin['reviews_all'])} | {n(sin['reviews_scope'])} | | | | |")
    A("")
    ok = rc["diff_2024"] == 0 and rc["diff_since_2024"] == 0
    if ok:
        A(f"**對賬:過。** 2024 年評論數 {n(rc['mine_reviews_2024'])} = 11/07 記錄 {n(rc['profile_reviews_2024'])};2024 起累計 {n(rc['mine_since_2024'])} = {n(rc['profile_since_2024'])}(差 0)。")
    else:
        A(f"**對賬:沒對上。** 2024 年 {n(rc['mine_reviews_2024'])} vs 11/07 記錄 {n(rc['profile_reviews_2024'])}(差 {rc['diff_2024']:+,});累計 {n(rc['mine_since_2024'])} vs {n(rc['profile_since_2024'])}(差 {rc['diff_since_2024']:+,})。可能原因:評論檔版本不同、空日期列。")
    A(f"評論檔 {n(rc['review_file_rows'])} 列,有日期 {n(rc['mine_review_rows_with_date'])} 列(11/07 記錄 {n(rc['profile_review_rows_with_date'])});評論對不到 listings 的有 {n(rc['reviews_of_listings_not_in_listings_file'])} 則。「全體」= 評論檔全部;「篩選」= 房源在篩選樣本 10,940 間內。「有評論的房源」只算 listings 檔裡有的房源。")
    A("")
    A("## 2. 每月走勢")
    A(f"結論:評論逐年墊高;最多的月份都在近年,最少的月份是 {D['bottom3_months'][0]['month']} 前後(只看 2024-01 到 2026-08 完整月份)。")
    A("")
    A(f"![每月評論數](../figures/melbourne_reviews_monthly_{DATE}.png)")
    A("")
    A("| 排名 | 評論最多的 3 個月(全體) | 評論最少的 3 個月(全體) |")
    A("|---|---|---|")
    for i in range(3):
        t, b = D["top3_months"][i], D["bottom3_months"][i]
        A(f"| {i + 1} | {t['month']}:{n(t['reviews_all'])} | {b['month']}:{n(b['reviews_all'])} |")
    A("2026-09 只到 09-18,不參與排名。")
    A("")
    A("## 3. 淡旺季")
    A(f"結論:兩年平均來看,偏高的是 {mon(S['high3_months'])};偏低的是 {mon(S['low3_months'])};2024 和 2025 的各月指數相關係數 {corr:.2f},形狀{corr_word}。")
    A("")
    A(f"![淡旺季指數](../figures/melbourne_seasonality_{DATE}.png)")
    A("")
    A("注意:每年評論量本來就在長,後半年的指數會被墊高一點;評論是住完才寫,評論的高峰會比入住晚一些。所以這是「評論的淡旺季」,不等於「入住的淡旺季」。")
    A("")
    A("## 4. 新上架(首評月份代理)")
    A(f"結論:首評落在當年的房源,2024 年 {n(Y['2024']['first_review_listings_all'])} 間、2025 年 {n(Y['2025']['first_review_listings_all'])} 間、2026 年到 09-18 {n(Y['2026']['first_review_listings_all'])} 間(全體;早年已下架的房源不在內,數字偏低)。")
    A("")
    A(f"![每月新上架](../figures/melbourne_new_listings_{DATE}.png)")
    A("")
    A(f"對照已知的「首評在最近 12 個月內 = {n(N['expected_known'])}」:那是「篩選且有價 {n(df['n_scope_price'])}」的子集。我這裡的年度表是「全體」與「篩選(不限有價)」,分母不同,數字不能直接比。用同一截止日 {N['cutoff_inclusive']}(含)重算:")
    A("")
    A("| 口徑 | 首評在近 12 個月內的房源數 |")
    A("|---|---|")
    A(f"| 全體 {n(df['n_listings'])}(評論檔最早日期) | {n(N['all_listings_summary_first'])} |")
    A(f"| 篩選 {n(df['n_scope'])}(評論檔最早日期) | {n(N['scope_summary_first'])} |")
    A(f"| 篩選且有價 {n(df['n_scope_price'])}(評論檔最早日期) | {n(N['scope_price_summary_first'])} |")
    A(f"| 篩選且有價 {n(df['n_scope_price'])}(listings 的 first_review 欄) | {n(N['scope_price_listings_field'])} |")
    A("")
    eq = N["scope_price_listings_field"] == N["expected_known"]
    A(("最後一列對上 2,056" if eq else "最後一列(沒對上 2,056,差 " + f"{N['scope_price_listings_field'] - N['expected_known']:+,})") + f"。評論檔與 listings 欄的首評日不同的有 {n(N['scope_price_field_vs_summary_mismatch'])} 間;篩選且有價裡一則評論都沒有的有 {n(N['scope_price_no_first_review_field'])} 間(不算新上架)。")
    A("")
    A("## 5. 現在這一期的價格(只有 2026-09,不是歷史)")
    A(f"結論:篩選且有價 {n(P['n'])} 間,掛牌價 p25 / 中位 / p75 = {P['p25']:g} / {P['median']:g} / {P['p75']:g}(當地幣別,每晚,掛牌價不是成交價)。")
    A("")
    A("| 區(neighbourhood_cleansed) | 房源數 | 掛牌價中位數 |")
    A("|---|---|---|")
    for d in P["top10_neighbourhoods"]:
        A(f"| {d['neighbourhood']} | {n(d['n'])} | {d['median']:g} |")
    A("")
    A("## 6. 看不到的事")
    A("| 看不到什麼 | 不要這樣說 | 改這樣說 |")
    A("|---|---|---|")
    A("| 2024、2025 當時的價格 | 「2024 年墨爾本均價是 X」 | 「2026-09 這一期的掛牌價中位數是 X;2024、2025 的價格這批沒有」 |")
    A("| 已經下架的房源(存活者偏誤) | 「2024 年墨爾本一共有 X 則評論」 | 「2024 年仍在架上的房源留下 X 則評論;下架房源不在內,實際較多」 |")
    A("| 真實訂單量與入住率 | 「評論數 = 訂單數」「入住率 X%」 | 「評論數是訂單的下限代理;不是每位房客都留評論」 |")
    A("| 評論有延遲(住完才寫) | 「9 月評論多 = 9 月旺季」 | 「評論集中在 9 月;入住可能在 8–9 月」 |")
    A("| 上架日期 | 「這間 2025-03 上架」 | 「這間第一則評論在 2025-03;上架可能更早」 |")
    A("| 篩選條件是 2026-09 的狀態 | 「這些房源 2024 年就是整套 1–2 房」 | 「以 2026-09 的房型 / 房數篩出的樣本」 |")
    A("")
    A("## 7. 資料出處連結(11/07 紀錄,今天未重開)")
    if links is None:
        A("repo 沒有紀錄網址。")
    else:
        pick = lambda tail: next((u for u in links if "/melbourne/" in u and u.endswith(tail)), None)
        lst, rev = pick("/data/listings.csv.gz"), pick("/visualisations/reviews.csv")
        A(f"- listings:[{lst}]({lst})" if lst else "- listings:repo 沒有紀錄網址")
        A(f"- 評論摘要檔:[{rev}]({rev})" if rev else "- 評論摘要檔:repo 沒有紀錄網址")
    A("")
    A("## 8. 數字來源對照(JSON:`airbnb_melbourne_2024_2026_2026-11-11.json`)")
    A("| 數字 | JSON 鍵名 |")
    A("|---|---|")
    for a, b in (("每年評論數 全體 / 篩選", "yearly.<年>.reviews_all / reviews_scope"),
                 ("有評論的房源 全體 / 篩選", "yearly.<年>.active_listings_all / active_listings_scope"),
                 ("首評落在當年 全體 / 篩選", "yearly.<年>.first_review_listings_all / first_review_listings_scope"),
                 ("2024 起累計", "since_2024.reviews_all / reviews_scope"),
                 ("對賬(11/07 記錄 vs 本次)", "recon.*"),
                 ("成長率", "growth.*"),
                 ("每月評論 / 新上架", "monthly.<YYYY-MM>.reviews_all / new_listings_all"),
                 ("最多 / 最少 3 個月", "top3_months / bottom3_months"),
                 ("淡旺季指數、相關係數", "seasonality.index_2024 / index_2025 / avg_index / corr_2024_2025"),
                 ("12 個月口徑對照", "new_12m.*"),
                 ("價格 p25 / 中位 / p75、前 10 區", "price.p25 / median / p75 / top10_neighbourhoods"),
                 ("樣本與抓取日", "definitions.*")):
        A(f"| {a} | `{b}` |")
    assert len(L) <= 100, f"報告 {len(L)} 行,超過 100"
    return "\n".join(L) + "\n"


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    D = compute()
    OUT_JSON.write_text(json.dumps(D, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    setup_font()
    fig_monthly(D)
    fig_season(D)
    fig_new(D)
    md = build_md(D)
    OUT_MD.write_text(md, encoding="utf-8")
    print("recon", D["recon"])
    print("yearly", json.dumps(D["yearly"], ensure_ascii=False))
    print("top3", D["top3_months"], "bottom3", D["bottom3_months"])
    print("season", D["seasonality"]["avg_index"], D["seasonality"]["corr_2024_2025"], D["seasonality"]["high3_months"], D["seasonality"]["low3_months"])
    print("new12", D["new_12m"])
    print("price", {k: v for k, v in D["price"].items() if k != "top10_neighbourhoods"}, D["price"]["top10_neighbourhoods"][:3])
    print("md lines", len(md.splitlines()))


if __name__ == "__main__":
    main()
