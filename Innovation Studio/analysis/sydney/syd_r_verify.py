import json, re, sys
import numpy as np
import pandas as pd
from scipy import stats

SRC = r"D:\KennyCode\UTS_workspace\scratchpad\insideairbnb_sydney\2026-09-16\data\listings.csv.gz"
OUT = r"D:\KennyCode\UTS_workspace\Innovation Studio\notes\raw\syd_r_verify_2026-11-21.json"

d = pd.read_csv(SRC, dtype=str, keep_default_na=False)
steps = [("all", len(d))]
isnum = lambda s: s.str.fullmatch(r"[0-9]+")
d = d[d["room_type"] == "Entire home/apt"]; steps.append(("room_type", len(d)))
d = d[d["bedrooms"].isin(["1", "2"])]; steps.append(("bedrooms", len(d)))
d = d[isnum(d["accommodates"])]
d = d[d["accommodates"].astype(int).between(2, 4)]; steps.append(("accommodates", len(d)))
d = d[isnum(d["minimum_nights"])]
d = d[d["minimum_nights"].astype(int).between(1, 7)]; steps.append(("minimum_nights", len(d)))
d = d[d["price"] != ""]; steps.append(("price", len(d)))
print(steps)
if len(d) != 6639:
    print("STOP: n != 6639"); sys.exit(1)


def amen_n(s):
    try:
        v = json.loads(s)
    except Exception:
        return 0
    if not isinstance(v, list):
        return 0
    return len({x.strip() for x in v if isinstance(x, str) and x.strip() != ""})


def num(s):
    return pd.to_numeric(s.replace("", np.nan))

VARS = ["price", "bedrooms", "accommodates", "amenities_n", "rating", "accuracy",
        "cleanliness", "checkin", "communication", "location", "value"]
df = pd.DataFrame({
    "price": d["price"].str.replace(r"[$,\s]", "", regex=True).astype(float),
    "bedrooms": d["bedrooms"].astype(int),
    "accommodates": d["accommodates"].astype(int),
    "amenities_n": d["amenities"].map(amen_n),
    "rating": num(d["review_scores_rating"]),
    "accuracy": num(d["review_scores_accuracy"]),
    "cleanliness": num(d["review_scores_cleanliness"]),
    "checkin": num(d["review_scores_checkin"]),
    "communication": num(d["review_scores_communication"]),
    "location": num(d["review_scores_location"]),
    "value": num(d["review_scores_value"]),
})[VARS].reset_index(drop=True)


def f(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else float(x)


desc = {}
for v in VARS:
    s = df[v].dropna()
    desc[v] = {"n": int(s.size), "missing": int(df[v].isna().sum()), "mean": f(s.mean()), "std": f(s.std(ddof=1)),
               "min": f(s.min()), "p25": f(s.quantile(.25)), "median": f(s.median()),
               "p75": f(s.quantile(.75)), "max": f(s.max()), "skew": f(s.skew())}


def mat(m):
    return {a: {b: f(m.loc[a, b]) for b in VARS} for a in VARS}

sp = df.corr(method="spearman")
dl = df.copy(); dl["price"] = np.log(dl["price"])
pe = dl.corr(method="pearson")
nn = df.notna().astype(int)
pn = nn.T.dot(nn)
pair_n = {a: {b: int(pn.loc[a, b]) for b in VARS} for a in VARS}

maxdiff = 0.0
for v in VARS[1:]:
    sub = df[["price", v]].dropna()
    r = stats.spearmanr(sub["price"], sub[v]).correlation
    diff = abs(r - sp.loc["price", v]); maxdiff = max(maxdiff, diff)
    print(f"price~{v}: scipy={r:.6f} pandas={sp.loc['price', v]:.6f} n={len(sub)}")
print("max |scipy - pandas| =", maxdiff)

pbb = {}
for b in ("1", "2"):
    s = df.loc[df["bedrooms"] == int(b), "price"]
    pbb[b] = {"n": int(s.size), "median": f(s.median()), "p25": f(s.quantile(.25)), "p75": f(s.quantile(.75))}

out = {"n": int(len(df)), "vars": VARS, "desc": desc, "spearman": mat(sp), "pearson_logprice": mat(pe),
       "pair_n": pair_n, "price_by_bedroom": pbb,
       "price_gt_1000": int((df["price"] > 1000).sum()), "price_gt_2000": int((df["price"] > 2000).sum())}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("amenities_n median", desc["amenities_n"]["median"], "rating missing", desc["rating"]["missing"])
print("bedroom", pbb, "gt2000", out["price_gt_2000"])
print("spearman price:", {v: round(sp.loc["price", v], 4) for v in VARS[1:]})
