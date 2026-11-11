"""獨立驗算 IS-1111-SYD-Y(驗收者自寫,不 import 產出者腳本)。只讀 reviews 的 listing_id、date 兩欄;
不輸出任何評論文字 / 評論者 / 個別 id,只印彙總數字。用法: python -I syd_y_verify.py"""
import site, sys; sys.path.append(site.getusersitepackages())
import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(r"D:/KennyCode/UTS_workspace/scratchpad/insideairbnb_sydney")
NEW = BASE / "2026-09-16/data"
CUT = "2025-09-17"
out = {}


def read_rev(p):
    return pd.read_csv(p, usecols=["listing_id", "date"], dtype={"listing_id": "int64", "date": "string"})


def read_lst(p, cols):
    return pd.read_csv(p, usecols=cols, dtype=str, keep_default_na=False)


rv = read_rev(NEW / "reviews.csv.gz")
ls = read_lst(NEW / "listings.csv.gz", ["id", "room_type", "bedrooms", "accommodates", "minimum_nights", "price", "first_review", "number_of_reviews_ltm"])
ls["idn"] = ls["id"].astype("int64")

# Y1
out["Y1_rows"] = len(rv)
out["Y1_undated"] = int(rv["date"].isna().sum())
rv = rv.dropna(subset=["date"])
out["date_min"], out["date_max"] = rv["date"].min(), rv["date"].max()
rv["y"] = rv["date"].str[:4]
rv["m"] = rv["date"].str[:7]

# Y2
yc = rv["y"].value_counts().sort_index()
out["Y2_year_counts"] = {k: int(v) for k, v in yc.items() if k >= "2023"}

# Y3
mc = rv["m"].value_counts().sort_index()
y24, y25 = int(yc["2024"]), int(yc["2025"])
out["Y3_2025_vs_2024_pct"] = round(100 * (y25 / y24 - 1), 2)
ja = lambda y: sum(int(mc[f"{y}-{k:02d}"]) for k in range(1, 9))
out["Y3_janaug_2025"], out["Y3_janaug_2026"] = ja(2025), ja(2026)
out["Y3_janaug_pct"] = round(100 * (ja(2026) / ja(2025) - 1), 2)

# Y4 (2024-01 起、完整月份到 2026-08)
mm = mc[(mc.index >= "2024-01") & (mc.index <= "2026-08")]
out["Y4_max"] = (mm.idxmax(), int(mm.max()))
out["Y4_min"] = (mm.idxmin(), int(mm.min()))
out["Y4_ratio"] = round(mm.max() / mm.min(), 3)
out["Y4_2026_09_partial"] = int(mc.get("2026-09", 0))
# 若把範圍改成 2023-01 起 / 2024-01 起各算一次,看最少月是否變
mm2 = mc[(mc.index >= "2023-01") & (mc.index <= "2026-08")]
out["Y4_alt_from_2023_min"] = (mm2.idxmin(), int(mm2.min()))

# Y5 指數 = 月數 / 該年 12 月平均 *100;2024、2025 各一;取平均
idx = {}
for y in (2024, 2025):
    v = np.array([mc[f"{y}-{k:02d}"] for k in range(1, 13)], dtype=float)
    idx[y] = 100 * v / v.mean()
avg = (idx[2024] + idx[2025]) / 2
out["Y5_avg_idx"] = [round(float(x), 1) for x in avg]
out["Y5_max"] = (int(avg.argmax()) + 1, round(float(avg.max()), 1))
out["Y5_min"] = (int(avg.argmin()) + 1, round(float(avg.min()), 1))
out["Y5_ratio"] = round(float(avg.max() / avg.min()), 3)
out["Y5_corr"] = round(float(np.corrcoef(idx[2024], idx[2025])[0, 1]), 4)

# Y6 / Y7
def is_scope(r):
    return (r.room_type == "Entire home/apt" and r.bedrooms in ("1", "2") and r.accommodates.isdigit()
            and 2 <= int(r.accommodates) <= 4 and r.minimum_nights.isdigit() and 1 <= int(r.minimum_nights) <= 7)

ls["scope"] = [is_scope(r) for r in ls.itertuples()]
ls["haspx"] = ls["price"] != ""
ls["sp"] = ls["scope"] & ls["haspx"]
out["listings_rows"], out["scope"], out["scope_price"] = len(ls), int(ls.scope.sum()), int(ls.sp.sum())
first = rv.groupby("listing_id")["date"].min().rename("first_rev")
ls = ls.merge(first, left_on="idn", right_index=True, how="left")
out["orphan_review_rows_not_in_listings"] = int((~rv["listing_id"].isin(set(ls.idn))).sum())
out["listings_without_any_review"] = int(ls.first_rev.isna().sum())
for tag, mask in (("all", ls.index == ls.index), ("scope", ls.scope), ("scope_price", ls.sp)):
    d = ls[mask]
    r = {}
    for y in ("2024", "2025", "2026"):
        r[y] = dict(field=int(d.first_review.str[:4].eq(y).sum()), reviewfile=int(d.first_rev.str[:4].eq(y).fillna(False).sum()))
    out[f"Y6_{tag}"] = r
d = ls[ls.sp]
a = int((d.first_rev >= CUT).fillna(False).sum())
b = int((d.first_review >= CUT).sum())          # 空字串 '' < 日期,自然排除
both_diff = int(((d.first_review != "") & d.first_rev.notna() & (d.first_review != d.first_rev)).sum())
out["Y7"] = dict(reviewfile=a, field=b, diff=a - b, mismatched_rows=both_diff,
                 sp_no_field=int((d.first_review == "").sum()), sp_no_review=int(d.first_rev.isna().sum()))
# 備註:bedrooms 欄是否有 '1.0' 之類格式(會被字串比對漏掉)
out["bedrooms_values_top"] = ls["bedrooms"].value_counts().head(8).to_dict()

# 存活者偏差:舊期(2025-12-12 / 2026-03-21 / 2026-06-16)評論檔含當時在架、後來下架的房源
surv = {}
for snap in ("2025-12-12", "2026-03-21", "2026-06-16", "2026-09-16"):
    r0 = read_rev(BASE / snap / "data/reviews.csv.gz").dropna(subset=["date"])
    s = {}
    s["rows"] = len(r0)
    s["reviews_2024"] = int(r0.date.str[:4].eq("2024").sum())
    s["reviews_2025_01_11"] = int(((r0.date >= "2025-01-01") & (r0.date <= "2025-11-30")).sum())
    s["reviews_2025_full"] = int(r0.date.str[:4].eq("2025").sum())
    rng = lambda a, b: int(((r0.date >= a) & (r0.date <= b)).sum())
    s["r2024_01_11"], s["r2025_01_11"] = rng("2024-01-01", "2024-11-30"), rng("2025-01-01", "2025-11-30")
    s["growth_01_11_pct"] = round(100 * (s["r2025_01_11"] / s["r2024_01_11"] - 1), 1)
    s["r2024_01_08"], s["r2025_01_08"] = rng("2024-01-01", "2024-08-31"), rng("2025-01-01", "2025-08-31")
    s["growth_01_08_pct"] = round(100 * (s["r2025_01_08"] / s["r2024_01_08"] - 1), 1)
    surv[snap] = s
out["survivor_snapshots"] = surv
old_ids = set(read_lst(BASE / "2025-12-12/data/listings.csv.gz", ["id"])["id"].astype("int64"))
new_ids = set(ls.idn)
out["churn_2025-12_to_2026-09"] = dict(old=len(old_ids), gone=len(old_ids - new_ids), new=len(new_ids - old_ids),
                                       gone_pct=round(100 * len(old_ids - new_ids) / len(old_ids), 1))
# 這些下架房源在舊期評論檔裡貢獻的 2024 評論數(=新檔缺的下限)
r_old = read_rev(BASE / "2025-12-12/data/reviews.csv.gz").dropna(subset=["date"])
gone = r_old[~r_old.listing_id.isin(new_ids)]
out["gone_listings_reviews_in_old_snapshot"] = dict(y2024=int(gone.date.str[:4].eq("2024").sum()),
                                                    y2025_01_11=int(((gone.date >= "2025-01-01") & (gone.date <= "2025-11-30")).sum()),
                                                    total=len(gone))
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
