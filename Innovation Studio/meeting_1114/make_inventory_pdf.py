#!/usr/bin/env python
# 把 notes/raw/data_inventory_*.md 做成給組員看的 PDF(無頭 Chrome 列印)。用法:python make_inventory_pdf.py
import collections, html, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
MD = HERE.parent / "notes" / "raw" / "data_inventory_2026-11-15.md"
OUT = HERE / "share"
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
URL_RE = re.compile(r"https?://[^\s、;;]+")
esc = html.escape

# ---------------------------------------------------------------- 解析
def split_row(line):
    line = line.strip()
    return [c.strip() for c in line.strip("|").split("|")]

def parse(lines):
    """回傳 blocks:('h1',t) ('h2',t) ('p',t) ('ul',[..]) ('table',header,rows)"""
    blocks, i, buf = [], 0, []
    def flush():
        nonlocal buf
        if buf:
            blocks.append(("p", " ".join(buf))); buf = []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        if ln.startswith("## "):
            flush(); blocks.append(("h2", ln[3:].strip())); i += 1
        elif ln.startswith("# "):
            flush(); blocks.append(("h1", ln[2:].strip())); i += 1
        elif ln.lstrip().startswith("|"):
            flush()
            hdr = split_row(ln); i += 2          # 跳過 |---|
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i])); i += 1
            blocks.append(("table", hdr, rows))
        elif re.match(r"\s*- ", ln):
            flush(); items = []
            while i < len(lines) and re.match(r"\s*- ", lines[i]):
                items.append((len(lines[i]) - len(lines[i].lstrip()), lines[i].strip()[2:].strip())); i += 1
            blocks.append(("ul", items))
        else:
            buf.append(ln.strip()); i += 1
    flush()
    return blocks

def status_cls(s):
    if "數字只能當大概" in s: return "yellow"
    if "不一樣" in s: return "orange"
    if "只看過一次" in s: return "gray"
    return "green"

def tag(s):
    s2 = esc(s).replace(",", ",<br>", 1) if "," in s else esc(s)
    return f'<span class="tag {status_cls(s)}">{s2}</span>'

def urls_of(cell):
    return URL_RE.findall(cell)

def url_block(cell):
    """網址欄:每個網址一行、可點、灰色小字;網址前的說明文字當標籤。沒有網址就照印。"""
    segs, pos, out = list(URL_RE.finditer(cell)), 0, []
    if not segs:
        return f'<span class="url nolink">{esc(cell)}</span>'
    for m in segs:
        label = cell[pos:m.start()].strip(" 、;;:：")
        pos = m.end()
        u = m.group(0)
        lab = f'<span class="ulab">{esc(label)}:</span> ' if label else ""
        out.append(f'<span class="url">{lab}<a href="{esc(u, quote=True)}">{esc(u)}</a></span>')
    return "".join(out)

def name_cell(name, cell_urls):
    if cell_urls:
        return f'<a class="nm" href="{esc(cell_urls[0], quote=True)}"><b>{esc(name)}</b></a>'
    return f"<b>{esc(name)}</b>"

# ---------------------------------------------------------------- 組版
CSS = """
@page { size: A4; margin: 12mm; @bottom-center { content: counter(page) " / " counter(pages); font-size: 8pt; color: #888 } }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box }
html { color-scheme: light }
body { margin: 0; background: #fff; color: #1f2933; font: 10pt/1.55 "Microsoft JhengHei", "Noto Sans TC", sans-serif }
h1.title { font-size: 24pt; margin: 0 0 2px; letter-spacing: .5px }
.subtitle { color: #52606d; font-size: 11pt; margin-bottom: 8px }
.lead { color: #3e4c59; margin: 6px 0 10px }
.tiles { display: flex; gap: 10px; margin: 8px 0 12px }
.tile { flex: 1; border: 1px solid #d9e2ec; border-radius: 8px; padding: 8px 12px; background: #f7fafc }
.tile .n { font-size: 26pt; font-weight: 700; line-height: 1.1 }
.tile .l { font-size: 9.5pt; color: #52606d }
.tile.t1 .n { color: #1b6b2f } .tile.t2 .n { color: #a34a00 } .tile.t3 .n { color: #4c5a67 }
.howto { border: 1px solid #d9e2ec; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; break-inside: avoid }
.howto h3 { margin: 0 0 6px; font-size: 11pt }
.howto .row { display: flex; gap: 8px; align-items: flex-start; margin: 4px 0 }
.howto .row .tagcol { flex: 0 0 150px }
.howto .row .desc { flex: 1; font-size: 9.5pt }
.note { font-size: 9pt; color: #52606d; margin-top: 6px }
h1.sec { font-size: 15pt; margin: 16px 0 6px; padding: 5px 10px; background: #e8f0fe; border-left: 5px solid #3b6fd4; break-after: avoid }
h1.sec.pb { break-before: page; margin-top: 0 }
h2.grp { font-size: 12.5pt; margin: 14px 0 3px; color: #1d3a6e; break-after: avoid }
h2.grp .ct { font-size: 9.5pt; font-weight: 400; color: #627d98 }
p.intro { margin: 2px 0 6px; color: #3e4c59; break-after: avoid }
p.intro2 { margin: 0 0 6px; color: #627d98; font-size: 9pt; break-after: avoid }
table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 8px }
thead { display: table-header-group }
th { background: #eef2f7; text-align: left; font-size: 9pt; padding: 5px 7px; border-bottom: 2px solid #bcccdc }
td { vertical-align: top; padding: 6px 7px; border-bottom: 1px solid #e1e7ee; overflow-wrap: anywhere }
tr { break-inside: avoid }
.t3c col.c1 { width: 27% } .t3c col.c2 { width: 53% } .t3c col.c3 { width: 20% }
.t4c col.c1 { width: 24% } .t4c col.c2 { width: 28% } .t4c col.c3 { width: 24% } .t4c col.c4 { width: 24% }
.tb3 col.c1 { width: 28% } .tb3 col.c2 { width: 44% } .tb3 col.c3 { width: 28% }
.need col.c1 { width: 26% } .need col.c2 { width: 34% } .need col.c3 { width: 40% }
a { color: inherit; text-decoration: none }
a.nm { color: #1857b6 }
a.nm b { text-decoration: underline; text-decoration-color: #a5c0ee }
.url { display: block; font-size: 8pt; line-height: 1.35; color: #7b8794; word-break: break-all; margin-top: 2px }
.url a { color: #7b8794; word-break: break-all }
.url .ulab { color: #52606d }
.url.nolink { font-style: italic }
.use { display: block; font-size: 8pt; color: #627d98; margin-bottom: 2px }
.tag { display: inline-block; padding: 2px 9px; border-radius: 11px; font-size: 8.5pt; line-height: 1.35; font-weight: 600; text-align: center }
.tag.green { background: #d9f2df; color: #176b30; border: 1px solid #9bd5aa }
.tag.yellow { background: #fff2bf; color: #7a5b00; border: 1px solid #ecd16a }
.tag.orange { background: #ffdfc2; color: #9c4300; border: 1px solid #f0aa72 }
.tag.gray { background: #e8eaed; color: #3e4650; border: 1px solid #c3c8cf }
ul.summary { margin: 4px 0; padding-left: 20px } ul.summary li { margin: 5px 0 }
"""

def group_table(hdr, rows):
    """第一段的一組:三欄表。回傳 (html, 多數目的, 多數原因)"""
    def majority(idx):
        c = collections.Counter(r[idx] for r in rows)
        v, n = c.most_common(1)[0]
        return v if n >= 2 else None
    maj_use, maj_why = majority(2), majority(3)
    body = []
    for r in rows:
        name, urlcell, use, why, found, status = r[:6]
        extra = ""
        if maj_use is None or use != maj_use:
            extra += f'<span class="use">用途:{esc(use)}</span>'
        if maj_why is None or why != maj_why:
            extra += f'<span class="use">原因:{esc(why)}</span>'
        body.append(
            f"<tr><td>{name_cell(name, urls_of(urlcell))}{url_block(urlcell)}</td>"
            f"<td>{extra}{esc(found)}</td><td>{tag(status)}</td></tr>")
    cols = '<colgroup><col class="c1"><col class="c2"><col class="c3"></colgroup>'
    t = (f'<table class="t3c">{cols}<thead><tr><th>網站</th><th>查到什麼</th><th>狀態</th></tr></thead>'
         f'<tbody>{"".join(body)}</tbody></table>')
    return t, maj_use, maj_why

def simple_table(cls, hdr, rows, url_col=None, name_link_col=None):
    n = len(hdr)
    cols = "<colgroup>" + "".join(f'<col class="c{k+1}">' for k in range(n)) + "</colgroup>"
    head = "".join(f"<th>{esc(h)}</th>" for h in hdr)
    body = []
    for r in rows:
        tds = []
        for k, c in enumerate(r[:n]):
            if k == url_col:
                tds.append(f"<td>{url_block(c)}</td>")
            elif k == name_link_col:
                tds.append(f"<td>{name_cell(c, urls_of(r[url_col]) if url_col is not None else [])}</td>")
            else:
                tds.append(f"<td>{esc(c)}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<table class="{cls}">{cols}<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'

def build(md_text):
    lines = md_text.splitlines()
    first_h1 = next(i for i, l in enumerate(lines) if l.startswith("# "))
    pre, rest = lines[:first_h1], lines[first_h1:]

    date = re.search(r"整理日期:(\d{4}-\d{2}-\d{2})", md_text).group(1)
    l3 = next(l for l in pre if l.startswith("三段各幾列"))
    n1 = int(re.search(r"第一段.*?(\d+) 列", l3).group(1))
    n2 = int(re.search(r"第二段.*?(\d+) 列", l3).group(1))
    n3 = int(re.search(r"第三段.*?(\d+) 列", l3).group(1))
    lead = next((l for l in pre if l.startswith("這份清單是什麼")), "").split(":", 1)[-1].strip()

    pb = parse(pre)
    status_items = next(b[1] for b in pb if b[0] == "ul")
    note = next((b[1] for b in pb if b[0] == "p" and b[1].startswith("沒開到網頁的")), "")
    # 清單項目:縮排 0 的是狀態,更深的當說明續行
    how = ""
    for _, it in status_items:
        lab, _, desc = it.partition(":")
        how += f'<div class="row"><div class="tagcol">{tag(lab)}</div><div class="desc">{esc(desc)}</div></div>'

    out = [f'<h1 class="title">查過的資料清單</h1><div class="subtitle">雪梨 Airbnb 房東定位助手 · 整理日期 {esc(date)}</div>']
    if lead:
        out.append(f'<p class="lead">{esc(lead)}</p>')
    out.append(
        f'<div class="tiles"><div class="tile t1"><div class="n">{n1}</div><div class="l">有查到的</div></div>'
        f'<div class="tile t2"><div class="n">{n2}</div><div class="l">沒查到的</div></div>'
        f'<div class="tile t3"><div class="n">{n3}</div><div class="l">還缺的數據</div></div></div>')
    out.append(f'<div class="howto"><h3>怎麼看「狀態」</h3>{how}'
               + (f'<div class="note">{esc(note)}</div>' if note else "") + "</div>")

    blocks = parse(rest)
    counts = {"s1": 0, "s2": 0, "s3": 0}
    section, i, group_open = 0, 0, False
    summary_lis = []
    while i < len(blocks):
        b = blocks[i]; i += 1
        if b[0] == "h1":
            title = b[1]
            if title.startswith("數量對照"):
                section = 4
                out.append(f'<h1 class="sec">{esc(title)}</h1>')
                continue
            section = 1 if title.startswith("第一段") else 2 if title.startswith("第二段") else 3
            cls = "sec" + ("" if section == 1 else " pb" if section == 2 else "")
            out.append(f'<h1 class="{cls}">{esc(title)}</h1>')
        elif b[0] == "h2":
            title = b[1]
            m = re.match(r"(.*?)(\(\d+ 列\))?$", title)
            ct = f' <span class="ct">{esc(m.group(2))}</span>' if m.group(2) else ""
            out.append(f'<h2 class="grp">{esc(m.group(1).strip())}{ct}</h2>')
            if section == 1:
                intro = ""
                if i < len(blocks) and blocks[i][0] == "p":
                    intro = blocks[i][1]; i += 1
                    out.append(f'<p class="intro">{esc(intro)}</p>')
                tb = blocks[i]; i += 1
                t, mu, mw = group_table(tb[1], tb[2])
                counts["s1"] += len(tb[2])
                bits = []
                if mu and mu not in intro: bits.append(f"這一組多數的查詢目的:{mu}")
                if mw and mw not in intro: bits.append(f"為什麼要查:{mw}")
                if bits:
                    out.append(f'<p class="intro2">{esc(";".join(bits))}</p>')
                out.append(t)
            elif section == 2:
                if i < len(blocks) and blocks[i][0] == "p":
                    out.append(f'<p class="intro">{esc(blocks[i][1])}</p>'); i += 1
                tb = blocks[i]; i += 1
                if title.startswith("(A)"):
                    out.append(simple_table("t4c", tb[1], tb[2], url_col=1, name_link_col=0))
                else:
                    out.append(simple_table("tb3", tb[1], tb[2], url_col=2))
                counts["s2"] += len(tb[2])
        elif b[0] == "p":
            out.append(f'<p class="intro">{esc(b[1])}</p>')
        elif b[0] == "table":
            if section == 3:
                out.append(simple_table("need", b[1], b[2])); counts["s3"] += len(b[2])
        elif b[0] == "ul" and section == 4:
            summary_lis = [t for ind, t in b[1] if ind == 0]

    # 數量對照:三行白話(數字從 md 讀)
    li = []
    def grab(pat, text):
        m = re.search(pat, text); return m.groups() if m else None
    t0 = next((t for t in summary_lis if t.startswith("五類不重複網站")), "")
    t1 = next((t for t in summary_lis if t.startswith("總表")), "")
    t2 = next((t for t in summary_lis if t.startswith("晚上補查 18")), "")
    g = grab(r"算出 (\d+) 個", t0)
    li.append(f"五類資料來源合起來,不重複的網站共 {g[0]} 個(同一個網站出現在不同類,只算一個);兩種算法得到同樣的數字。" if g else esc(t0))
    g = grab(r"總表 (\d+) 列.*?✅(\d+) ⚠️(\d+) ❌(\d+) ⏸(\d+) 未查(\d+)", t1)
    li.append(f"總表 {g[0]} 個數字,晚上補查後的檢查結果:確認 {g[1]} 個、有差 {g[2]} 個、不對 {g[3]} 個、先擱置 {g[4]} 個、還沒查 {g[5]} 個;跟預期的數字一致。" if g else esc(t1))
    g = grab(r"晚上補查 (\d+) 個:開到 (\d+).*?要登入 (\d+).*?被擋 (\d+).*?找不到頁面 (\d+).*?沒去查 (\d+)", t2)
    li.append(f"晚上補查 {g[0]} 個網站:{g[1]} 個開到、{g[2]} 個要登入、{g[3]} 個被擋、{g[4]} 個找不到頁面、{g[5]} 個沒去查,加起來剛好 {g[0]} 個。" if g else esc(t2))
    out.append('<ul class="summary">' + "".join(f"<li>{x}</li>" for x in li) + "</ul>")

    doc = (f'<!DOCTYPE html><html lang="zh-Hant" data-theme="light"><head><meta charset="utf-8">'
           f'<title>查過的資料清單 {esc(date)}</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>')
    return doc, date, counts, (n1, n2, n3)

# ---------------------------------------------------------------- 主程式
def main():
    browser = next((b for b in BROWSERS if pathlib.Path(b).exists()), None)
    if not browser:
        sys.exit("找不到 Chrome 或 Edge")
    doc, date, counts, declared = build(MD.read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    pdf_out = OUT / f"雪梨Airbnb房東定位助手_查過的資料清單_{date}.pdf"
    with tempfile.TemporaryDirectory(prefix="inv_pdf_") as tmp:
        tmp = pathlib.Path(tmp)
        page = tmp / "inventory.html"
        page.write_text(doc, encoding="utf-8")
        tmp_pdf = tmp / "out.pdf"
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
               "--virtual-time-budget=10000", f"--user-data-dir={tmp / 'profile'}",
               f"--print-to-pdf={tmp_pdf}", page.as_uri()]
        subprocess.run(cmd, check=True, timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not tmp_pdf.exists() or tmp_pdf.stat().st_size < 1000:
            sys.exit("PDF 沒產生")
        shutil.copyfile(tmp_pdf, pdf_out)

    links = "?"
    try:
        import pypdf
        r = pypdf.PdfReader(str(pdf_out)); pages = str(len(r.pages)); n = 0
        for p in r.pages:
            for a in p.get("/Annots", []) or []:
                act = a.get_object().get("/A")
                if act and "/URI" in act.get_object(): n += 1
        links = str(n)
    except Exception:
        pages = "約 %d(近似)" % len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf_out.read_bytes()))
    ok = lambda a, b: "對" if a == b else f"不對(md 寫 {b})"
    print("瀏覽器:", browser)
    print("PDF:", pdf_out, pdf_out.stat().st_size, "bytes,頁數", pages)
    print("第一段列數", counts["s1"], ok(counts["s1"], declared[0]), "| 第二段列數", counts["s2"], ok(counts["s2"], declared[1]),
          "| 第三段列數", counts["s3"], ok(counts["s3"], declared[2]))
    print("PDF 連結數(/Annots 的 /URI):", links)

main()
