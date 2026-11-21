"""比對兩邊:A = Claude Sonnet、K = 關鍵字法。只輸出彙總數字(不含評論原文)。

2026-11-21 更正:第一版多了一個 B = GPT(Codex)。Kenny 的流程不用 ChatGPT,所以 B 已經整個拿掉,
這支程式也改成只比 A 和 K。
"""
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


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = None if p is None or r is None or p + r == 0 else 2 * p * r / (p + r)
    return {k: (None if v is None else round(v, 3)) for k, v in (("precision", p), ("recall", r), ("f1", f))}


A, K = load("labels_A_claude_sonnet.json"), load("labels_K_keyword.json")
rows = {r["rid"]: r for r in csv.DictReader(open(BASE / "data/sample_50.csv", encoding="utf-8"))}
out = {"n_reviews": 50, "n_cells": 350, "readers": {"A": "Claude Sonnet(Claude Code 分身)", "K": "關鍵字法"}}

# 1) K 對 A(把 A 當暫時的參考;A 不是人工答案)
kper = {}
TP = FP = FN = 0
pol_ok = pol_n = 0
same_cells = 0
for a in ASPECTS:
    tp = fp = fn = 0
    for r in RIDS:
        la, lk = A[r]["labels"][a], K[r]["labels"][a]
        same_cells += la == lk
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
out["K_vs_A"] = {"350 格標籤完全相同": same_cells, "per_aspect": kper, "tp": TP, "fp": FP, "fn": FN,
                 "micro": prf(TP, FP, FN), "macro_F1": round(sum(kf) / len(kf), 3),
                 "兩邊都提到的格數": pol_n, "其中好壞相同": pol_ok,
                 "好壞相同%": round(pol_ok / max(pol_n, 1) * 100, 1)}


# 2) A 引用的原文找不找得到
def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()


n = ok = longq = miss = 0
for r in RIDS:
    t = norm(rows[r]["text"])
    for a, lab in A[r]["labels"].items():
        if lab == "none":
            continue
        q = (A[r].get("evidence") or {}).get(a)
        if not q:
            miss += 1
            continue
        n += 1
        ok += norm(q) in t
        longq += len(q.split()) > 12
out["evidence_check_A"] = {"引用數": n, "原文裡找得到": ok, "找得到%": round(ok / max(n, 1) * 100, 1),
                           "超過 12 個字": longq, "該引用卻沒引用": miss}

# 3) 分布
cnt = []
for a in ASPECTS:
    for nm, L in (("A", A), ("K", K)):
        c = Counter(L[r]["labels"][a] for r in RIDS)
        cnt.append({"方面": ZH[a], "誰": nm, "pos": c["pos"], "neg": c["neg"], "mixed": c["mixed"], "none": c["none"]})
with open(RUN / "aspect_counts.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cnt[0]))
    w.writeheader()
    w.writerows(cnt)
out["A_overall"] = dict(Counter(A[r]["overall"] for r in RIDS))
out["by_stratum_A"] = {
    s: {"條數": sum(rows[r]["stratum"] == s for r in RIDS),
        "有負面或有好有壞": sum(any(v in ("neg", "mixed") for v in A[r]["labels"].values())
                                 for r in RIDS if rows[r]["stratum"] == s)}
    for s in ("random", "low_rated")}
out["每條平均提到幾個方面"] = {
    nm: round(sum(sum(v != "none" for v in L[r]["labels"].values()) for r in RIDS) / 50, 2)
    for nm, L in (("A", A), ("K", K))}

# 4) 成本粗估(字元 / 4 當 token;價目來自派工守則 0.1 節,2026-11-03 快取,今天沒重查)
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
    cost["美元"][m] = {k: {"一次50條": round(nn * (tin_batch * pi + tout * po) / 1e6),
                           "一次1條": round(nn * (tin_single * pi + tout * po) / 1e6)} for k, nn in N.items()}
(RUN / "cost_estimate.json").write_text(json.dumps(cost, ensure_ascii=False, indent=1), encoding="utf-8")
(RUN / "agreement.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "K_vs_A"}, ensure_ascii=False, indent=1))
kv = out["K_vs_A"]
print("K 對 A:", json.dumps({k: kv[k] for k in kv if k != "per_aspect"}, ensure_ascii=False))
for a, v in kv["per_aspect"].items():
    print("  ", v["中文"], "找對", v["tp"], "多找", v["fp"], "漏掉", v["fn"], "F1", v["f1"])
