"""第二次試跑的樣本:挑 10 間房,每間取最近的 30 條評論(共 300 條)。
目的:讓「讀評論」的結果可以按房源加總,示範「這間房先改什麼」。
規則寫死、種子固定,可重跑。和第一次(50 條)不同的地方:這次連短評論也收(40 字元以上)。
"""
import csv
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parents[1]
REV = ROOT / "scratchpad/insideairbnb_sydney/2026-09-16/data/reviews.csv.gz"
MT = ROOT / "Innovation Studio/model_training/data"
SEED, N_LOW, N_OTHER, PER_LISTING = 42, 5, 5, 30
DATE_FROM, LEN_MIN, LEN_MAX = "2024-01-01", 40, 1200

tt = pd.read_csv(MT / "processed/train_table_2026-09.csv", dtype=str, keep_default_na=False)
ex = pd.read_csv(MT / "processed/extremes_dropped_24.csv", dtype=str, keep_default_na=False)
idcol = "id" if "id" in tt.columns else tt.columns[0]
scope_ids = set(tt[idcol]) | set(ex[idcol])
assert len(scope_ids) == 6639, len(scope_ids)

ls = pd.read_csv(MT / "raw/listings_2026-09-16.csv.gz", dtype=str, keep_default_na=False,
                 usecols=["id", "neighbourhood_cleansed", "bedrooms", "accommodates", "review_scores_rating"])
ls = ls[ls.id.isin(scope_ids)].copy()
ls["rating"] = pd.to_numeric(ls.review_scores_rating, errors="coerce")
p10 = ls.rating.quantile(0.10)
low_ids = set(ls[ls.rating <= p10].id)

rv = pd.read_csv(REV, dtype=str, keep_default_na=False, usecols=["listing_id", "id", "date", "comments"])  # 不讀評論者欄位
rv = rv[rv.listing_id.isin(scope_ids) & (rv.date >= DATE_FROM)].copy()
stats = {"可比房源、%s 以後的評論" % DATE_FROM: len(rv)}
rv["text"] = rv.comments.str.replace(r"<br\s*/?>", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
rv["n_char"] = rv.text.str.len()
letters = rv.text.str.count(r"[^\W\d_]")
ascii_letters = rv.text.str.count(r"[A-Za-z]")
rv["is_en"] = (letters > 0) & (ascii_letters / letters.clip(lower=1) >= 0.9) & (rv.text.str.split().str.len() >= 5)
el = rv[rv.is_en & rv.n_char.between(LEN_MIN, LEN_MAX)].copy()
stats["其中英文、%d–%d 字元" % (LEN_MIN, LEN_MAX)] = len(el)
stats["符合條件的比例%"] = round(len(el) / max(len(rv), 1) * 100, 1)
cnt = el.groupby("listing_id").size()
ok = sorted(cnt[cnt >= PER_LISTING].index)          # 排序後再抽,結果才固定
stats["有 %d 條以上符合條件評論的房源數" % PER_LISTING] = len(ok)
pool = pd.Series(ok)
low_pool = pool[pool.isin(low_ids)]
oth_pool = pool[~pool.isin(low_ids)]
stats["其中評分最低一成的房源數"] = len(low_pool)
pick_low = list(low_pool.sample(n=N_LOW, random_state=SEED))
pick_oth = list(oth_pool.sample(n=N_OTHER, random_state=SEED))
picked = [(x, "low_rated") for x in pick_low] + [(x, "other") for x in pick_oth]

rows, listings = [], []
k = 0
for j, (lid, stratum) in enumerate(picked):
    code = "房源" + "ABCDEFGHIJ"[j]
    sub = el[el.listing_id == lid].sort_values(["date", "id"], ascending=[False, False]).head(PER_LISTING)
    info = ls[ls.id == lid].iloc[0]
    listings.append({"code": code, "listing_id": lid, "stratum": stratum, "區": info.neighbourhood_cleansed,
                     "臥室": info.bedrooms, "可住人數": info.accommodates, "總評分": info.review_scores_rating,
                     "符合條件的評論數": int(cnt[lid]), "取樣最早日期": sub.date.min(), "取樣最晚日期": sub.date.max()})
    for _, r in sub.iterrows():
        k += 1
        rows.append({"rid": "R%03d" % k, "code": code, "listing_id": lid, "review_id": r["id"], "date": r["date"],
                     "n_char": int(r["n_char"]), "text": r["text"]})
df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)      # 打亂順序,讀的人看不出哪幾條是同一間
df["rid"] = ["R%03d" % (i + 1) for i in range(len(df))]
df.to_csv(BASE / "data/sample_listing10.csv", index=False, encoding="utf-8")
pd.DataFrame(listings).to_csv(BASE / "data/sample_listing10_listings.csv", index=False, encoding="utf-8")
for b in range(6):                                                    # 6 批,每批 50 條;只有編號和原文
    part = df.iloc[b * 50:(b + 1) * 50][["rid", "text"]]
    part.to_csv(BASE / ("data/sample_listing10_input_batch%d.csv" % (b + 1)), index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
stats["抽出"] = {"房源": len(listings), "評論": len(df), "評分最低一成的房源": N_LOW, "其他房源": N_OTHER}
stats["樣本長度(字元)"] = {"最短": int(df.n_char.min()), "中位數": int(df.n_char.median()), "最長": int(df.n_char.max()),
                         "短於 150 的條數": int((df.n_char < 150).sum())}
stats["評分最低一成的門檻"] = float(p10)
stats["sample_listing10.csv sha256"] = hashlib.sha256((BASE / "data/sample_listing10.csv").read_bytes()).hexdigest()
(BASE / "data/sample_listing10_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(stats, ensure_ascii=False, indent=1))
print(pd.DataFrame(listings).drop(columns=["listing_id"]).to_string(index=False))
