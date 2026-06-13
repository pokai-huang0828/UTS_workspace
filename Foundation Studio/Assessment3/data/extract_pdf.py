# -*- coding: utf-8 -*-
"""Extract text from nib FY21 annual report PDF; print lines with profit/revenue figures."""
import re, sys
PDF = r"C:\Users\User\.claude\projects\D--KennyWorkLife-UTS-workspace\e22d4337-2beb-417c-811d-f36d15c5a8b8\tool-results\webfetch-1781328881231-2nvs59.pdf"

text = None
for lib in ("pdfplumber", "fitz", "pypdf", "PyPDF2"):
    try:
        if lib == "pdfplumber":
            import pdfplumber
            with pdfplumber.open(PDF) as pdf:
                text = "\n".join((p.extract_text() or "") for p in pdf.pages[:15])
        elif lib == "fitz":
            import fitz
            d = fitz.open(PDF); text = "\n".join(d[i].get_text() for i in range(min(15, d.page_count)))
        else:
            mod = __import__(lib)
            R = getattr(mod, "PdfReader")
            text = "\n".join((pg.extract_text() or "") for pg in R(PDF).pages[:15])
        print("USED:", lib); break
    except Exception as e:
        print(f"  {lib} failed: {e}")

if not text:
    print("NO PDF LIBRARY AVAILABLE"); sys.exit()

# print lines mentioning key financial terms
keys = re.compile(r"(operating profit|net profit|NPAT|premium revenue|total revenue|underlying|earnings per share|statutory)", re.I)
for ln in text.splitlines():
    s = ln.strip()
    if s and keys.search(s) and re.search(r"\d", s):
        print("  >", s[:140])
