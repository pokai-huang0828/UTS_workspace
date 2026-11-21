"""比對三邊:A = Claude Sonnet、B = GPT(Codex)、K = 關鍵字法。只輸出彙總數字(不含評論原文)。"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUN = BASE / "runs/run_2026-11-21_pilot50"
ASPECTS = ["cleanliness", "noise", "location_transport", "checkin", "communication", "value", "amenities_comfort"]
ZH = {"cleanliness": "清潔", "noise": "噪音", "location_transport": "位置與交通", "checkin": "入住",
      "communication": "房東溝通", "value": "性價比", "amenities_comfort": "設施與舒適"}
VALS = ["pos", "neg", "mixed", "none"]
RIDS = [f"R{i:02d}" for i in range(1, 51)]


def load(name):
    d = json.loads((RUN / name).read_text(encoding="utf-8"))
    assert len(d) == 50 and [x["rid"] for x in d] == RIDS, name
    for x in d:
        assert set(x["labels"]) == set(ASPECTS), (name, x["rid"])
        assert all(v in VALS for v in x["labels"].values()), (name, x["rid"])
    return {x["rid"]: x for x in d}


def kappa(x, y, cats):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    pe = sum((x.count(c) / n) * (y.count(c) / n) for c in cats)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = None if p is None or r is None or p + r == 0 else 2 * p * r / (p + r)
    return {k: (None if v is None else round(v, 3)) for k, v in (("precision", p), ("recall", r), ("f1", f))}


A, B, K = load("labels_A_claude_sonnet.json"), load("labels_B_gpt.json"), load("labels_K_keyword.json")
rows = {r["rid"]: r for r in csv.DictReader(open(BASE / "data/sample_50.csv", encoding="utf-8"))}
out = {"n_reviews": 50, "n_cells": 350}

# 1) A vs B
per = {}
cellA, cellB = [], []
TP = FP = FN = 0
for a in ASPECTS:
    xa = [A[r]["labels"][a] for r in RIDS]
    xb = [B[r]["labels"][a] for r in RIDS]
    cellA += xa
    cellB += xb
    ma = [v != "none" for v in xa]
    mb = [v != "none" for v in xb]
    tp = sum(p and q for p, q in zip(ma, mb))
    fp = sum(p and not q for p, q in zip(ma, mb))
    fn = sum(q and not p for p, q in zip(ma, mb))
    TP += tp
    FP += fp
    FN += fn
    both = [(p, q) for p, q in zip(xa, xb) if p != "none" and q != "none"]
    per[a] = {"中文": ZH[a], "A提到": sum(ma), "B提到": sum(mb), "兩邊都提到": tp, "只有A": fp, "只有B": fn,
              "有沒有提到_一致率%": round(sum(p == q for p, q in zip(ma, mb)) / 50 * 100, 1),
              "有沒有提到_kappa": kappa(ma, mb, [True, False]),
              "有沒有提到_F1": prf(tp, fp, fn)["f1"],
              "都提到時好壞一致": sum(p == q for p, q in both), "都提到的條數": len(both)}
out["A_vs_B_per_aspect"] = per
f1s = [v["有沒有提到_F1"] for v in per.values() if v["有沒有提到_F1"] is not None]
bothcells = [(p, q) for p, q in zip(cellA, cellB) if p != "none" and q != "none"]
out["A_vs_B_overall"] = {
    "350 格完全相同的比例%": round(sum(p == q for p, q in zip(cellA, cellB)) / 350 * 100, 1),
    "四類 kappa": kappa(cellA, cellB, VALS),
    "有沒有提到_micro": prf(TP, FP, FN),
    "有沒有提到_macro_F1": round(sum(f1s) / len(f1s), 3),
    "都提到的格數": len(bothcells),
    "都提到時好壞一致%": round(sum(p == q for p, q in bothcells) / max(len(bothcells), 1) * 100, 1),
    "好壞不一致的組合": dict(Counter(f"{p}/{q}" for p, q in bothcells if p != q)),
    "整體感受一致%": round(sum(A[r]["overall"] == B[r]["overall"] for r in RIDS) / 50 * 100, 1),
    "整體感受分布_A": dict(Counter(A[r]["overall"] for r in RIDS)),
    "整體感受分布_B": dict(Counter(B[r]["overall"] for r in RIDS)),
}

# 2) K vs 兩個 AI 的共識(兩邊標一樣的格才算有答案)
kper = {}
TP = FP = FN = 0
pol_ok = pol_n = 0
n_cons = 0
for a in ASPECTS:
    tp = fp = fn = 0
    for r in RIDS:
        la, lb, lk = A[r]["labels"][a], B[r]["labels"][a], K[r]["labels"][a]
        if la != lb:
            continue
        n_cons += 1
        ref, got = la != "none", lk != "none"
        tp += ref and got
        fp += (not ref) and got
        fn += ref and not got
        if ref and got:
            pol_n += 1
            pol_ok += lk == la
    kper[a] = {"中文": ZH[a], **prf(tp, fp, fn), "tp": tp, "fp": fp, "fn": fn}
    TP += tp
    FP += fp
    FN += fn
kf = [v["f1"] for v in kper.values() if v["f1"] is not None]
out["K_vs_consensus"] = {"有共識的格數": n_cons, "per_aspect": kper, "micro": prf(TP, FP, FN),
                         "macro_F1": round(sum(kf) / len(kf), 3),
                         "提到且好壞也對%": round(pol_ok / max(pol_n, 1) * 100, 1), "提到且有共識的格數": pol_n}


# 3) 引用的原文找不找得到
def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()


def ev(L):
    n = ok = longq = miss = 0
    for r in RIDS:
        t = norm(rows[r]["text"])
        for a, lab in L[r]["labels"].items():
            if lab == "none":
                continue
            q = (L[r].get("evidence") or {}).get(a)
            if not q:
                miss += 1
                continue
            n += 1
            ok += norm(q) in t
            longq += len(q.split()) > 12
    return {"引用數": n, "原文裡找得到": ok, "找得到%": round(ok / max(n, 1) * 100, 1), "超過 12 個字": longq, "該引用卻沒引用": miss}


out["evidence_check"] = {"A": ev(A), "B": ev(B)}

# 4) 分布
cnt = []
for a in ASPECTS:
    for nm, L in (("A", A), ("B", B), ("K", K)):
        c = Counter(L[r]["labels"][a] for r in RIDS)
        cnt.append({"方面": ZH[a], "誰": nm, "pos": c["pos"], "neg": c["neg"], "mixed": c["mixed"], "none": c["none"]})
with open(RUN / "aspect_counts.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cnt[0]))
    w.writeheader()
    w.writerows(cnt)


def anyneg(L, r):
    return any(v in ("neg", "mixed") for v in L[r]["labels"].values())


out["by_stratum"] = {
    s: {"條數": sum(rows[r]["stratum"] == s for r in RIDS),
        "A_有負面或有好有壞": sum(anyneg(A, r) for r in RIDS if rows[r]["stratum"] == s),
        "B_有負面或有好有壞": sum(anyneg(B, r) for r in RIDS if rows[r]["stratum"] == s)}
    for s in ("random", "low_rated")}
out["每條平均提到幾個方面"] = {
    nm: round(sum(sum(v != "none" for v in L[r]["labels"].values()) for r in RIDS) / 50, 2)
    for nm, L in (("A", A), ("B", B), ("K", K))}

# 5) 成本粗估(字元 / 4 當 token;價目來自派工守則 0.1 節,2026-11-03 快取,今天沒重查)
prompt_chars = len((BASE / "src/prompt_aspect_v1.md").read_text(encoding="utf-8"))
rev_chars = sum(len(rows[r]["text"]) for r in RIDS) / 50
out_chars = len(json.dumps([A[r] for r in RIDS], ensure_ascii=False)) / 50
tin_batch = (prompt_chars / 50 + rev_chars) / 4
tin_single = (prompt_chars + rev_chars) / 4
tout = out_chars / 4
PRICE = {"Sonnet 5.5": (2, 10), "Haiku 5.5": (0.10, 0.50), "Opus 5.5": (4, 20)}
stats = json.loads((BASE / "data/sample_stats.json").read_text(encoding="utf-8"))
N = {"2025 年以後、可比房源的評論": stats["2025-01-01 以後"], "全部評論": stats["全部評論"]}
cost = {"假設": {"每條評論平均字元": round(rev_chars), "規則字元": prompt_chars, "每條輸出字元": round(out_chars),
                 "1 token 約 4 字元": True, "每條輸入token_一次50條": round(tin_batch),
                 "每條輸入token_一次1條": round(tin_single), "每條輸出token": round(tout)},
        "美元": {}}
for m, (pi, po) in PRICE.items():
    cost["美元"][m] = {k: {"一次50條": round(n * (tin_batch * pi + tout * po) / 1e6),
                           "一次1條": round(n * (tin_single * pi + tout * po) / 1e6)} for k, n in N.items()}
(RUN / "cost_estimate.json").write_text(json.dumps(cost, ensure_ascii=False, indent=1), encoding="utf-8")
(RUN / "agreement.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
dis = [{"rid": r, "aspect": a, "A": A[r]["labels"][a], "B": B[r]["labels"][a]}
       for r in RIDS for a in ASPECTS if A[r]["labels"][a] != B[r]["labels"][a]]
(RUN / "disagreements_local.json").write_text(json.dumps(dis, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("A_vs_B_overall", "evidence_check", "by_stratum", "每條平均提到幾個方面")}, ensure_ascii=False, indent=1))
print("K:", json.dumps({k: out["K_vs_consensus"][k] for k in ("micro", "macro_F1", "提到且好壞也對%", "有共識的格數")}, ensure_ascii=False))
print("不一致格數", len(dis))
print(json.dumps(cost, ensure_ascii=False))
