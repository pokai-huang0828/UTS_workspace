"""最簡單的對照組:關鍵字法。不是報告寫的 VADER(電腦沒裝、不能安裝),是自己列的字表。
做法:把評論切成句子;句子裡出現某方面的關鍵字 -> 算提到;同一句有負面字 -> neg,否則 pos;同一方面正負都有 -> mixed。
"""
import csv
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUN = BASE / "runs/run_2026-11-21_pilot50"
ASPECTS = ["cleanliness", "noise", "location_transport", "checkin", "communication", "value", "amenities_comfort"]
KW = {
    "cleanliness": r"\b(clean|cleanliness|spotless|tidy|dirty|dust|dusty|mould|mold|mouldy|smell|smelly|stain|stains|stained|filthy|hygiene|cockroach|cockroaches|bugs?)\b",
    "noise": r"\b(nois[ey]|noises|quiet|peaceful|loud|traffic noise|construction|thin walls|soundproof|earplugs)\b",
    "location_transport": r"\b(location|located|neighbou?rhood|area|close to|near|walk|walking|walkable|beach|station|train|bus|ferry|transport|cbd|city|shops?|restaurants?|cafes?|central|convenient)\b",
    "checkin": r"\b(check[- ]?in|check[- ]?out|checked in|checking in|key|keys|lockbox|lock box|access code|self check|instructions|luggage)\b",
    "communication": r"\b(host|hosts|communicat\w+|responsive|respond\w*|reply|replied|helpful|friendly|accommodating|message[sd]?|quick to)\b",
    "value": r"\b(value|price|priced|pricey|expensive|overpriced|cheap|worth|affordable|money|fee|fees)\b",
    "amenities_comfort": r"\b(bed|beds|kitchen|wifi|wi-fi|internet|air ?con\w*|aircon|heating|heater|shower|hot water|bathroom|spacious|space|furniture|appliances?|parking|pool|view|views|balcony|equipped|comfortable|comfy|cosy|cozy|washing machine|dryer|tv|fan)\b",
}
NEG = (
    r"\b(not|no|never|dirty|dusty|mould\w*|mold\w*|smell\w*|stain\w*|filthy|nois[ey]|loud|broken|issue|issues|problem|problems|"
    r"disappoint\w*|unfortunately|however|but|although|though|lack\w*|missing|poor|bad|worst|terrible|awful|uncomfortable|tiny|"
    r"cramped|slow|difficult|hard to|expensive|overpriced|pricey|could be|would be nice|needs?|downside|complain\w*|rude)\b"
    r"|n[’']t\b"
)


def label(text):
    out = {a: set() for a in ASPECTS}
    for sent in re.split(r"(?<=[.!?])\s+", text):
        s = sent.lower()
        neg = bool(re.search(NEG, s))
        for a in ASPECTS:
            if re.search(KW[a], s):
                out[a].add("neg" if neg else "pos")
    lab = {a: ("none" if not v else "mixed" if len(v) == 2 else next(iter(v))) for a, v in out.items()}
    vals = [v for v in lab.values() if v != "none"]
    if vals and all(v == "neg" for v in vals):
        overall = "neg"
    elif all(v == "pos" for v in vals):
        overall = "pos"
    else:
        overall = "mixed"
    return lab, overall


rows = list(csv.DictReader(open(BASE / "data/sample_50_input.csv", encoding="utf-8")))
res = []
for r in rows:
    lab, ov = label(r["text"])
    res.append({"rid": r["rid"], "labels": lab, "evidence": {}, "overall": ov})
RUN.mkdir(parents=True, exist_ok=True)
(RUN / "labels_K_keyword.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("keyword 標了", len(res), "條;各方面提到的條數:", {a: sum(1 for x in res if x["labels"][a] != "none") for a in ASPECTS})
