# -*- coding: utf-8 -*-
"""把外部行情總表(meeting_1114_external_facts.md)第 1-5 段的表格列、第 8-A 段,
解析成 JSON,嵌進同資料夾 index.html 的 <script id="ext-data" type="application/json">。

- index.html 本身就是模板:腳本只替換 ext-data 那一段,其他內容不動。
- web_verify_blocked8_2026-11-14.md 的 Chrome 補查判定,用下面的 OVERRIDES 覆蓋總表裡對應列的 ⏸。
- 另外依「網站(網址的網域)」統計每個網站貢獻幾列、查核結果各幾列,給頁面「我怎麼做的」那一節用。
用法:python "Innovation Studio/meeting_1114/build_page.py"
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "notes" / "raw"
SRC = RAW / "meeting_1114_external_facts.md"
HTML = HERE / "index.html"

COLS = ["item", "low", "mid", "high", "unit", "period", "geo", "source", "url",
        "stype", "verdict", "note", "origin"]
SECTION_NAMES = {1: "短租市場", 2: "法規與平台費", 3: "裝修與佈置", 4: "營運成本", 5: "房市"}

# web_verify_blocked8_2026-11-14.md 的逐列判定(第 11-19 行)→ 總表列編號
OVERRIDES = {
    "3.09": ("✅", "Domain 頁在 Chrome 打開,The Makeover Group 負責人原句「a full budget renovation will set you back between $20,000 and $27,000」,頁面年份 2025;頁面小標整段預算級是 $5,000 – $27,000,20,000–27,000 只是「整間預算翻新」那一句;未標幣別字樣,推定 AUD。"),
    "3.32": ("❌", "價格要登入才看得到;頁面結構化資料為 price 550.00 AUD、compare_at_price 787.07(折扣 30%),與 520/660 對不上,不能再引用。"),
    "3.33": ("❌", "頁面上沒有 145:比價範圍 $157.21–$315.17(最近一次見價 2026-11-03),當日價 $199.99,歷史最低 $115.40(2025-02-04);低情境要改用頁面有的數。"),
    "5.04": ("✅", "Domain 2025 年 9 月季報告頁:雪梨 Units「record of $750 per week」,季增 1.4%,年增 4.9%($35)。"),
    "5.05": ("✅", "同一頁:雪梨 Houses「record high of $780 per week」,季增 0%,年增 1.3%。"),
    "5.11": ("✅", "同一頁:「Vacancy rates fell to 0.9% in September」(雪梨段落)。"),
    "2.17": ("⏸", "工具呼叫上限用完,這次沒開,維持 ⏸。"),
    "4.07": ("⏸", "工具呼叫上限用完,這次沒開,維持 ⏸;E2/E4/E6 仍只有 Canstar 轉述。"),
}
# 加查但沒改判定的列(只加註)
EXTRA_NOTES = {
    "5.02": "加查 Domain 2026 年 9 月季原頁沒開到(⏸);旁證(不算驗證):2025 年 9 月季雪梨 780 是獨棟、公寓是 750,要確認 L2「公寓 780」沒有把獨棟與公寓混了。",
}

ROW_ID = re.compile(r"^(\d\.\d\d)")
GAP_ID = re.compile(r"^(8\.\d\d)")
URL_RE = re.compile(r"https?://[^\s;]+")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tcat(t):
    if "換算" in t:
        return "換算"
    if t.startswith("官方"):
        return "官方"
    if "產業報告" in t:
        return "產業報告"
    if "部落格" in t:
        return "部落格"
    if "商業網站" in t:
        return "商業網站"
    return "不明"


def vnorm(v):
    for k in ("✅", "⚠️", "❌", "⏸"):
        if k in v:
            return k
    return "未查"


def parse(text):
    rows, gaps, bad = [], [], []
    sec, sub = None, None
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^## (\d)\. ", line)
        if m:
            sec = int(m.group(1))
            sub = None
            continue
        if line.startswith("### "):
            sub = line[4:].strip()
            continue
        if not line.startswith("| "):
            continue
        cells = split_row(line)
        if sec in SECTION_NAMES and ROW_ID.match(cells[0]):
            if len(cells) != len(COLS):
                bad.append((n, len(cells)))
                continue
            r = dict(zip(COLS, cells))
            r["id"] = ROW_ID.match(cells[0]).group(1)
            r["section"] = sec
            r["verdict"] = vnorm(r["verdict"])
            r["orig_verdict"] = r["verdict"]
            r["override"] = False
            r["override_note"] = ""
            r["line"] = n
            rows.append(r)
        elif sec == 8 and sub and sub.startswith("8-A") and GAP_ID.match(cells[0]):
            gaps.append({"id": GAP_ID.match(cells[0]).group(1),
                         "item": cells[0][len(GAP_ID.match(cells[0]).group(1)):].strip(),
                         "status": cells[1], "origin": cells[2] if len(cells) > 2 else ""})
    return rows, gaps, bad


def site_stats(rows):
    """依主題(段)× 網站(網域)統計。一列列了多個網址時,每個網域各算一次。"""
    agg = OrderedDict()
    for r in rows:
        hosts = []
        for u in URL_RE.findall(r["url"]):
            h = urlparse(u).netloc.lower()
            h = h[4:] if h.startswith("www.") else h
            if h not in hosts:
                hosts.append(h)
        if not hosts:
            hosts = ["(沒有網址)" + r["source"]]
        for h in hosts:
            key = (r["section"], h)
            a = agg.setdefault(key, {"section": r["section"], "site": h, "names": [], "types": [],
                                     "n": 0, "snippet": 0,
                                     "v": {"✅": 0, "⚠️": 0, "❌": 0, "⏸": 0, "未查": 0},
                                     "url": URL_RE.findall(r["url"])[0] if URL_RE.findall(r["url"]) else ""})
            if r["source"] not in a["names"]:
                a["names"].append(r["source"])
            c = tcat(r["stype"])
            if c not in a["types"]:
                a["types"].append(c)
            a["n"] += 1
            if "搜尋摘要" in r["stype"]:
                a["snippet"] += 1
            a["v"][r["verdict"]] += 1
    return list(agg.values())


def main():
    text = SRC.read_text(encoding="utf-8")
    rows, gaps, bad = parse(text)
    by = {r["id"]: r for r in rows}

    before = {k: 0 for k in ("✅", "⚠️", "❌", "⏸", "未查")}
    for r in rows:
        before[r["verdict"]] += 1

    for rid, (v, note) in OVERRIDES.items():
        r = by.get(rid)
        if not r:
            print(f"[警告] 覆蓋表的 {rid} 在總表找不到")
            continue
        if r["verdict"] != "⏸":
            print(f"[警告] {rid} 原判定是 {r['verdict']},不是 ⏸")
        r["override"] = True
        if v != r["verdict"]:
            # 判定已改:舊加註(例如「補查前不要用」)標成補查前,避免與新判定並列時被誤讀
            r["note"] = "補查前:" + r["note"]
        r["verdict"] = v
        r["override_note"] = note
    for rid, note in EXTRA_NOTES.items():
        if rid in by:
            by[rid]["override_note"] = note

    after = {k: 0 for k in before}
    for r in rows:
        after[r["verdict"]] += 1

    per = OrderedDict()
    for s in SECTION_NAMES:
        per[str(s)] = sum(1 for r in rows if r["section"] == s)
    m = re.search(r"總表共 (\d+) 列", text)
    expected = int(m.group(1)) if m else None
    m2 = re.search(r"✅ (\d+)、⚠️ (\d+)、⏸/未查/沒涵蓋 \d+[((]⏸ (\d+)、未查 (\d+)", text)

    sites = site_stats(rows)
    distinct = sorted({s["site"] for s in sites})

    for s, name in SECTION_NAMES.items():
        print(f"第 {s} 段 {name}:{per[str(s)]} 列")
    total = len(rows)
    print(f"合計 {total} 列;總表檔尾寫 {expected} 列 → {'一致' if total == expected else '不一致,差 ' + str((expected or 0) - total) + ' 列'}")
    print("覆蓋前判定:", before)
    if m2:
        exp_v = {"✅": int(m2.group(1)), "⚠️": int(m2.group(2)), "⏸": int(m2.group(3)), "未查": int(m2.group(4))}
        diff = {k: (before[k], exp_v[k]) for k in exp_v if before[k] != exp_v[k]}
        print("覆蓋前判定與檔尾比對:", "一致" if not diff else f"不一致 {diff}")
    print("覆蓋後判定(Chrome 補查):", after)
    print(f"第 8-A 段「仍然沒有」:{len(gaps)} 列")
    print(f"網站統計:{len(sites)} 個(主題 × 網站)組合;不重複網站 {len(distinct)} 個")
    if bad:
        print("[警告] 欄數不是 13 的列(行號, 欄數):", bad)

    payload = {
        "rows": rows,
        "gaps": gaps,
        "sites": sites,
        "stats": {"per_section": per, "total": total, "expected_total": expected,
                  "verdict_before": before, "verdict_after": after,
                  "sites_distinct": len(distinct), "site_groups": len(sites)},
    }
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = HTML.read_text(encoding="utf-8")
    start_tag = '<script id="ext-data" type="application/json">'
    i = html.find(start_tag)
    j = html.find("</script>", i)
    if i < 0 or j < 0:
        sys.exit("index.html 找不到 ext-data 區塊")
    html = html[: i + len(start_tag)] + blob + html[j:]
    HTML.write_text(html, encoding="utf-8", newline="\n")
    print(f"已寫入 {HTML}({HTML.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
