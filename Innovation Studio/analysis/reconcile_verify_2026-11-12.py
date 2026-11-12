# -*- coding: utf-8 -*-
"""獨立驗算 15 條數字(IS-1112-RECON-VERIFY-NUM)。
只從原始 csv.gz 重算;只印彙總數字,不印姓名/房源名稱/評論文字/個別 id。
執行:python -I "Innovation Studio/analysis/reconcile_verify_2026-11-12.py" [scratchpad 路徑]
備註:-I 會排除使用者 site-packages(dateutil、six 裝在那裡),
      所以腳本開頭把「使用者自己的」site-packages 明確加進 sys.path(不含 cwd 與腳本目錄)。
"""
import sys, os, json, site
for _p in (site.getusersitepackages(),):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.append(_p)
import numpy as np
import pandas as pd

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"D:\KennyCode\UTS_workspace\scratchpad"
NOTES_RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notes", "raw")
PER = ["2025-12-12", "2026-03-21", "2026-06-16", "2026-09-16"]
P12, P03, P06, P09 = PER
CITY = {"mel": "insideairbnb_melbourne", "syd": "insideairbnb_sydney"}
WANT = ["id", "host_id", "room_type", "bedrooms", "accommodates", "minimum_nights", "price",
        "review_scores_rating", "estimated_occupancy_l365d", "first_review",
        "hosts_time_as_host_years", "hosts_time_as_host_months",
        "hosts_time_as_user_years", "hosts_time_as_user_months",
        "host_since", "last_scraped"]


def path(city, per, f):
    return os.path.join(ROOT, CITY[city], per, "data", f)


_missing = set()


def load(city, per):
    p = path(city, per, "listings.csv.gz")
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    use = [c for c in WANT if c in hdr]
    for c in WANT:
        if c not in hdr:
            _missing.add(f"{city}/{per}:{c}")
    d = pd.read_csv(p, usecols=use, low_memory=False)
    if "price" in d:
        d["p"] = pd.to_numeric(d["price"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce")
    for c in ("first_review", "host_since", "last_scraped"):
        if c in d:
            d[c] = pd.to_datetime(d[c], errors="coerce")
    if "hosts_time_as_host_years" in d and "hosts_time_as_host_months" in d:
        d["hm"] = d["hosts_time_as_host_years"] * 12 + d["hosts_time_as_host_months"]
    return d


def filt(d):
    return d[(d.room_type == "Entire home/apt") & d.bedrooms.isin([1, 2]) &
             d.accommodates.between(2, 4) & d.minimum_nights.between(1, 7)]


def pct(a, b, nd=1):
    return f"{100*a/b:.{nd}f}%"


def hr(t):
    print(f"\n===== {t} =====")


L = {(c, p): load(c, p) for c in CITY for p in PER}
print("欄位缺漏:", sorted(_missing) or "無")
print("列數:", {f"{c}/{p}": len(v) for (c, p), v in L.items()})
m9, m12, m3, m6 = L["mel", P09], L["mel", P12], L["mel", P03], L["mel", P06]

# ---------- 1
hr("1 評分(墨 09)")
n = len(m9); r = m9.review_scores_rating.dropna()
print("全體", n, "有評分", len(r), pct(len(r), n), "中位數", r.median(),
      "5.0占", pct((r == 5).sum(), len(r)), "<4占", pct((r < 4).sum(), len(r)))

# ---------- 2
hr("2 occupancy(墨 09,篩選且有價)")
f9 = filt(m9); f9p = f9[f9.p.notna()]
o = f9p.estimated_occupancy_l365d
print("n", len(f9p), "篩選(不論價)", len(f9), "occ非空", o.notna().sum(), "中位數", o.median(), "平均", round(o.mean(), 2),
      "==0占(分母全部)", pct((o == 0).sum(), len(f9p)), "==0占(分母非空)", pct((o == 0).sum(), o.notna().sum()),
      "==255占(分母全部)", pct((o == 255).sum(), len(f9p)), "==255占(分母非空)", pct((o == 255).sum(), o.notna().sum()),
      "max", o.max())

# ---------- 3
hr("3 reviews(墨 09)")
rv = pd.read_csv(path("mel", P09, "reviews.csv.gz"), usecols=["listing_id", "date"])
rv["date"] = pd.to_datetime(rv["date"], errors="coerce")
rv["y"] = rv.date.dt.year
for y in (2024, 2025):
    s = rv[rv.y == y]
    print(y, "有評論房源", s.listing_id.nunique(), "評論數", len(s), "每間", round(len(s) / s.listing_id.nunique(), 2))
a, b = rv[rv.y == 2024].listing_id.nunique(), rv[rv.y == 2025].listing_id.nunique()
print("房源數變化", f"{100*(b-a)/a:+.1f}%", "評論數最大日期", rv.date.max().date())
mo = rv[(rv.date >= "2024-01-01") & (rv.date < "2026-09-01")].groupby(rv.date.dt.to_period("M")).size()
print("月數", len(mo), "最多", mo.max(), str(mo.idxmax()), "最少", mo.min(), str(mo.idxmin()), "倍數", round(mo.max() / mo.min(), 2))

# ---------- 4
hr("4 有價比例(墨,全部列)")
for p in PER:
    d = L["mel", p]
    print(p, len(d), d.p.notna().sum(), pct(d.p.notna().sum(), len(d)))

# ---------- 5 / 6
hr("5 三期皆有價(以 id,不限房型)")
pr = {k: L["mel", p].dropna(subset=["p"]).drop_duplicates("id").set_index("id").p for k, p in (("3", P03), ("6", P06), ("9", P09))}
ids = pr["3"].index.intersection(pr["6"].index).intersection(pr["9"].index)
print("id 重複(各期):", {c: int(L["mel", p].id.duplicated().sum()) for c, p in (("03", P03), ("06", P06), ("09", P09))})
c36 = (pr["6"][ids] / pr["3"][ids] - 1) * 100
c69 = (pr["9"][ids] / pr["6"][ids] - 1) * 100
c39 = (pr["9"][ids] / pr["3"][ids] - 1) * 100
print("n", len(ids), "中位數 3→6", round(c36.median(), 2), "6→9", round(c69.median(), 2), "3→9", round(c39.median(), 2),
      "3→9 漲", pct((c39 > 0).sum(), len(ids)), "跌", pct((c39 < 0).sum(), len(ids)), "不變", pct((c39 == 0).sum(), len(ids)))
hr("6 與 2025-12 期的交集與新手")
d12 = m12.drop_duplicates("id").set_index("id")
both = ids.intersection(d12.index)
hm = d12.loc[both, "hm"]
new = hm <= 12
print("交集", len(both), "新手(≤12)", int(new.sum()), "缺值", int(hm.isna().sum()),
      "其餘(缺值算老手)", int((~new).sum()), "其餘(排除缺值)", int(((hm > 12)).sum()))
print("3→9 中位數 新手", round(c39[both][new.values].median(), 2),
      "老手(缺值算老手)", round(c39[both][~new.values].median(), 2),
      "老手(排除缺值)", round(c39[both][(hm > 12).values].median(), 2))

# ---------- 7 / 13
def host_months(city):
    a, b = L[city, P09], L[city, P12]
    ga = a.dropna(subset=["host_id"]).groupby("host_id")["hm"]
    gb = b.dropna(subset=["host_id"]).groupby("host_id")["hm"]
    ha, hb = ga.max(), gb.max()
    common = ha.index.intersection(hb.index)
    incons_a = int((ga.nunique() > 1).sum()); incons_b = int((gb.nunique() > 1).sum())
    out = {}
    for name, fa, fb in (("取max", ga.max(), gb.max()), ("取min", ga.min(), gb.min()),
                         ("取眾數", ga.agg(lambda s: s.mode().iloc[0] if s.notna().any() else np.nan),
                          gb.agg(lambda s: s.mode().iloc[0] if s.notna().any() else np.nan))):
        diff = (fa[common] - fb[common])
        out[name] = {k: int((diff == k).sum()) for k in (8, 9, 10, 11)} | {"缺值": int(diff.isna().sum())}
    print(city, "09 host_id 去重", ha.index.size, "12 期", hb.index.size, "交集", len(common),
          "同房東多值(09/12)", incons_a, incons_b)
    for k, v in out.items():
        print("  ", k, v)


hr("7 墨 房東年資變化"); host_months("mel")
hr("13 雪 房東年資變化"); host_months("syd")

# ---------- 8
hr("8 MAE 算術與 json 鍵")
for nm, num, den in (("mel B?→M2 a", 78.4 - 75.1, 78.4), ("mel b", 87.4 - 75.1, 87.4), ("syd", 101.7 - 93.4, 101.7)):
    print(nm, f"{100*num/den:.2f}%")
for city in ("mel", "syd"):
    j = json.load(open(os.path.join(NOTES_RAW, f"{city}_b_positioning_2026-11-11.json"), encoding="utf-8"))
    r = j["d_experiment"]["results_group_cv"]
    print(city, {k: r[k]["all"]["MAE_aud"] for k in ("B0", "B1", "M2") if k in r})

# ---------- 9 / 10
hr("9 新手 × 首評代理(墨 09,新手用 09 期年資欄)")
nw = f9p[f9p.hm <= 12]
cut = pd.Timestamp("2025-09-18"); end = pd.Timestamp("2026-09-16")
inwin = nw.first_review.between(cut, end)
print("篩選且有價新手", len(nw), "首評代理也新", int(inwin.sum()), "沒抓到", int((~inwin).sum()),
      "其中無首評", int(nw.first_review.isna().sum()), "首評早於截止", int((nw.first_review < cut).sum()),
      "首評晚於基準日", int((nw.first_review > end).sum()))
fr = lambda d: int(d.first_review.between(cut, end).sum())
print("首評代理總數: 全體", fr(m9), "篩選", fr(f9), "篩選且有價", fr(f9p), "全體整套房", fr(m9[m9.room_type == "Entire home/apt"]))
hr("10"); print("1122/8223 =", pct(1122, 8223))

# ---------- 11
hr("11 掛牌價中位數(墨 09)")
e = m9[(m9.room_type == "Entire home/apt") & m9.p.notna()]
for b in (1, 2, 3):
    s = e[e.bedrooms == b].p
    print("全體整套房", b, "房 n", len(s), "中位數", s.median())
for b in (1, 2):
    s = f9p[f9p.bedrooms == b].p
    print("篩選且有價", b, "房 n", len(s), "中位數", s.median())

# ---------- 12
hr("12 3 月期缺席(墨,id 存在即算)")
s12, s3, s6 = set(m12.id), set(m3.id), set(m6.id)
print("06∩12 且不在03:", len(s6 & s12 - s3), "06∩12∩03:", len(s6 & s12 & s3), "06∩12:", len(s6 & s12))

# ---------- 14
hr("14 雪梨 09 篩選且有價新手")
sy9 = L["syd", P09]; sf = filt(sy9); sfp = sf[sf.p.notna()]
print("n", len(sfp), "≤12", int((sfp.hm <= 12).sum()), "<12", int((sfp.hm < 12).sum()), "(篩選不論價", len(sf), ")")

# ---------- 15
hr("15 雪梨 2025-12 host_since 對照")
s = L["syd", P12]; s = s[s.host_since.notna()]
ls = s.last_scraped
dm = (ls.dt.year - s.host_since.dt.year) * 12 + (ls.dt.month - s.host_since.dt.month)
variants = {
    "A 整月(日不足扣1)": dm - (ls.dt.day < s.host_since.dt.day).astype(int),
    "B 只算年月差(不看日)": dm,
    "C floor(天數/30.4375)": ((ls - s.host_since).dt.days / 30.4375).apply(np.floor),
}
usr = s.hosts_time_as_user_years * 12 + s.hosts_time_as_user_months
hst = s.hosts_time_as_host_years * 12 + s.hosts_time_as_host_months
print("host_since 非空列", len(s), "last_scraped 唯一值數", ls.nunique())
for k, v in variants.items():
    print(k, "user 相同", pct((usr == v).sum(), len(s), 2), " host 相同", pct((hst == v).sum(), len(s), 2),
          "(user 欄缺值", int(usr.isna().sum()), " host 欄缺值", int(hst.isna().sum()), ")")
