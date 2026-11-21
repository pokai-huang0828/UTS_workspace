"""把 300 條評論的標籤按房源加總,並用一條暫定規則排出「這間房先改什麼」。
輸入:runs/run_2026-11-21_listing10/labels_A_batch1..6.json、data/sample_listing10*.csv
輸出(同一個 run 資料夾):
  labels_A_all.json            300 條合併(只留本機)
  listing_summary_local.csv    每間房 x 每個方面的統計,含房源 id、區、評分(只留本機)
  listing_summary_public.csv   同上但只有代號,不含 id、區、評分(可進版控)
  summary.json                 彙總數字(可進版控)
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUN = BASE / "runs/run_2026-11-21_listing10"
ROOT = Path(__file__).resolve().parents[3]
ASPECTS = ["cleanliness", "noise", "location_transport", "checkin", "communication", "value", "amenities_comfort"]
ZH = {"cleanliness": "清潔", "noise": "噪音", "location_transport": "位置與交通", "checkin": "入住",
      "communication": "房東溝通", "value": "性價比", "amenities_comfort": "設施與舒適"}
SUBSCORE = {"cleanliness": "review_scores_cleanliness", "checkin": "review_scores_checkin",
            "communication": "review_scores_communication", "location_transport": "review_scores_location",
            "value": "review_scores_value"}
VALS = ["pos", "neg", "mixed", "none"]
MIN_MENTIONS, NEG_SHARE_MIN, TOP_N = 3, 0.20, 3      # T5 暫定規則的三個門檻

rows = list(csv.DictReader(open(BASE / "data/sample_listing10.csv", encoding="utf-8")))
by_rid = {r["rid"]: r for r in rows}
listings = list(csv.DictReader(open(BASE / "data/sample_listing10_listings.csv", encoding="utf-8")))
labels = []
for b in range(1, 7):
    d = json.loads((RUN / ("labels_A_batch%d.json" % b)).read_text(encoding="utf-8"))
    assert len(d) == 50, (b, len(d))
    labels += d
L = {x["rid"]: x for x in labels}
assert len(L) == 300 and set(L) == set(by_rid), (len(L), len(set(L) ^ set(by_rid)))
for x in labels:
    assert set(x["labels"]) == set(ASPECTS) and all(v in VALS for v in x["labels"].values()), x["rid"]
(RUN / "labels_A_all.json").write_text(json.dumps(labels, ensure_ascii=False, indent=1), encoding="utf-8")


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()


# 引用檢查
n_q = ok_q = long_q = miss_q = 0
for rid, x in L.items():
    t = norm(by_rid[rid]["text"])
    for a, lab in x["labels"].items():
        if lab == "none":
            continue
        q = (x.get("evidence") or {}).get(a)
        if not q:
            miss_q += 1
            continue
        n_q += 1
        ok_q += norm(q) in t
        long_q += len(q.split()) > 12

# 分項評分(只留本機用)
import pandas as pd  # noqa: E402

ids = [l["listing_id"] for l in listings]
ls = pd.read_csv(ROOT / "Innovation Studio/model_training/data/raw/listings_2026-09-16.csv.gz", dtype=str,
                 keep_default_na=False, usecols=["id"] + sorted(set(SUBSCORE.values())))
ls = ls[ls.id.isin(ids)].set_index("id")

per = defaultdict(lambda: {a: Counter() for a in ASPECTS})
n_rev = Counter()
for rid, x in L.items():
    code = by_rid[rid]["code"]
    n_rev[code] += 1
    for a in ASPECTS:
        per[code][a][x["labels"][a]] += 1

local_rows, public_rows, priorities = [], [], {}
for l in listings:
    code = l["code"]
    cand = []
    for a in ASPECTS:
        c = per[code][a]
        m = c["pos"] + c["neg"] + c["mixed"]
        share = (c["neg"] + c["mixed"]) / m if m else None
        sub = ls.loc[l["listing_id"], SUBSCORE[a]] if a in SUBSCORE else ""
        base = {"房源": code, "方面": ZH[a], "評論數": n_rev[code], "有提到": m, "好評": c["pos"], "負評": c["neg"],
                "有好有壞": c["mixed"], "有抱怨的比例%": "" if share is None else round(share * 100, 1)}
        public_rows.append({**base, "分組": "評分最低一成" if l["stratum"] == "low_rated" else "其他"})
        local_rows.append({**base, "listing_id": l["listing_id"], "區": l["區"], "臥室": l["臥室"], "總評分": l["總評分"],
                           "Airbnb 分項評分": sub})
        if m >= MIN_MENTIONS and share is not None and share >= NEG_SHARE_MIN:
            cand.append((share, m, ZH[a]))
    cand.sort(key=lambda t: (-t[0], -t[1]))
    priorities[code] = [{"方面": z, "有抱怨的比例%": round(s * 100, 1), "有提到": m} for s, m, z in cand[:TOP_N]]

for name, data in (("listing_summary_local.csv", local_rows), ("listing_summary_public.csv", public_rows)):
    with open(RUN / name, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)

# 彙總
tot = {a: Counter(L[r]["labels"][a] for r in L) for a in ASPECTS}
short = [r for r in L if int(by_rid[r]["n_char"]) < 150]
long_ = [r for r in L if int(by_rid[r]["n_char"]) >= 150]


def avg_aspects(rids):
    return round(sum(sum(v != "none" for v in L[r]["labels"].values()) for r in rids) / max(len(rids), 1), 2)


def all_none(rids):
    return sum(all(v == "none" for v in L[r]["labels"].values()) for r in rids)


def stratum_of(code):
    return next(l["stratum"] for l in listings if l["code"] == code)


def neg_any(rids):
    return sum(any(v in ("neg", "mixed") for v in L[r]["labels"].values()) for r in rids)


low_r = [r for r in L if stratum_of(by_rid[r]["code"]) == "low_rated"]
oth_r = [r for r in L if stratum_of(by_rid[r]["code"]) == "other"]
out = {
    "n_listings": len(listings), "n_reviews": len(L), "規則版本": "prompt_aspect_v2.md", "讀的模型": "Claude Sonnet(Claude Code 分身,6 批各 50 條)",
    "引用檢查": {"引用數": n_q, "原文裡找得到": ok_q, "找得到%": round(ok_q / max(n_q, 1) * 100, 1), "超過 12 個字": long_q, "該引用卻沒引用": miss_q},
    "整體感受": dict(Counter(x["overall"] for x in labels)),
    "各方面合計": {ZH[a]: {"有提到": tot[a]["pos"] + tot[a]["neg"] + tot[a]["mixed"], "好評": tot[a]["pos"], "負評": tot[a]["neg"], "有好有壞": tot[a]["mixed"]} for a in ASPECTS},
    "短評論(<150 字元)": {"條數": len(short), "平均提到幾個方面": avg_aspects(short), "完全沒提到任何方面的條數": all_none(short)},
    "長評論(>=150 字元)": {"條數": len(long_), "平均提到幾個方面": avg_aspects(long_), "完全沒提到任何方面的條數": all_none(long_)},
    "有抱怨的評論": {"評分最低一成的 5 間(150 條)": neg_any(low_r), "其他 5 間(150 條)": neg_any(oth_r)},
    "T5 暫定規則": {"說明": "某方面至少被提到 %d 次,且「有抱怨的比例」(負評+有好有壞)/有提到 >= %d%%,才列入;依比例由高到低取前 %d 項" % (MIN_MENTIONS, int(NEG_SHARE_MIN * 100), TOP_N),
                 "每間房的優先改進項": priorities},
}
(RUN / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
# 本機用:AI 讀出的抱怨比例 vs Airbnb 分項評分(只印,不存到公開檔)
print("--- 本機對照:房源 | 分組 | 清潔抱怨% / 清潔分 | 入住 | 溝通 | 位置 | 性價比")
for l in listings:
    code = l["code"]
    cells = []
    for a in ("cleanliness", "checkin", "communication", "location_transport", "value"):
        c = per[code][a]
        m = c["pos"] + c["neg"] + c["mixed"]
        cells.append("%s/%s" % ("-" if not m else round((c["neg"] + c["mixed"]) / m * 100), ls.loc[l["listing_id"], SUBSCORE[a]]))
    print(code, l["stratum"], l["總評分"], " | ".join(cells))
