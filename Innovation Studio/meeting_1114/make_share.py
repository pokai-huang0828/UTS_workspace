#!/usr/bin/env python
# 產生分享用的 HTML 複本 + PDF(無頭瀏覽器列印)。用法:python make_share.py
import hashlib, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "index.html"
OUT = HERE / "share"
NAME = "雪梨Airbnb房東定位助手_1114組會"
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

PRINT_STYLE = """<style>
@page { size: A4; margin: 10mm }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact }
nav { display: none !important }
figure, .card, .mock, tr, .stack-row, .rng-row { break-inside: avoid }
.tbl-wrap { overflow: visible !important }
.grid { display: block !important }
.grid > * { break-inside: auto !important; margin-bottom: 10px }
table.mid, table.mtab, table.wide, #map-top10 table { min-width: 0 !important; width: 100% !important }
</style>
"""
PRINT_SCRIPT = """<script>
window.addEventListener('load', function () {
  var main = ['pitch','meeting','ab','approach','data','methods','where','roadmap','websites'];
  main.forEach(function (id) {
    var s = document.getElementById(id);
    if (s) s.querySelectorAll('details').forEach(function (d) { d.open = true; });
  });
  var by = document.getElementById('bysection');
  if (by) {
    var outer = by.closest('details.dsec');
    if (outer) outer.open = true;
    (outer || by).querySelectorAll('details').forEach(function (d) { d.open = true; });
  }
  var h1 = document.querySelector('h1');
  if (h1) {
    var p = document.createElement('p');
    p.style.cssText = 'font-size:12px;color:#555;margin:4px 0 10px';
    p.textContent = '這是 PDF 版:地圖不能點、附錄的來源表和算式沒有展開。要看完整版請打開 HTML 檔。';
    h1.insertAdjacentElement('afterend', p);
  }
});
</script>
"""

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def main():
    browser = next((b for b in BROWSERS if pathlib.Path(b).exists()), None)
    if not browser:
        sys.exit("找不到 Chrome 或 Edge")
    OUT.mkdir(exist_ok=True)
    html_out = OUT / f"{NAME}.html"
    pdf_out = OUT / f"{NAME}.pdf"
    shutil.copyfile(SRC, html_out)

    text = SRC.read_text(encoding="utf-8")
    assert "</head>" in text and "</body>" in text
    text = re.sub(r"<html", '<html data-theme="light"', text, count=1)  # 強制淺色(跳過 prefers-color-scheme 深色)
    text = text.replace("</head>", PRINT_STYLE + "</head>", 1)
    i = text.rfind("</body>")
    text = text[:i] + PRINT_SCRIPT + text[i:]

    with tempfile.TemporaryDirectory(prefix="share_pdf_") as tmp:
        tmp = pathlib.Path(tmp)
        page = tmp / "print.html"
        page.write_text(text, encoding="utf-8")
        tmp_pdf = tmp / "out.pdf"
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
               "--virtual-time-budget=20000", "--window-size=760,1000",
               f"--user-data-dir={tmp / 'profile'}", f"--print-to-pdf={tmp_pdf}",
               page.as_uri()]
        subprocess.run(cmd, check=True, timeout=180, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not tmp_pdf.exists() or tmp_pdf.stat().st_size < 1000:
            sys.exit("PDF 沒產生")
        shutil.copyfile(tmp_pdf, pdf_out)

    try:
        import pypdf
        pages = str(len(pypdf.PdfReader(str(pdf_out)).pages))
    except Exception:
        pages = "約 %d(近似,正則數 /Type /Page)" % len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf_out.read_bytes()))
    print("瀏覽器:", browser)
    print("HTML:", html_out, html_out.stat().st_size, "bytes")
    print("PDF :", pdf_out, pdf_out.stat().st_size, "bytes,頁數", pages)
    print("sha256 原檔:", sha(SRC))
    print("sha256 複本:", sha(html_out), "相同" if sha(SRC) == sha(html_out) else "不同!")

main()
