"""算 A3 報告正文字數（沿用 A2 口徑）：漢字 1 字 = 1；英文／數字每個詞 = 1；標題計入。

範圍：「0 摘要與決策」標題起，到「參考文獻」標題前。
不計：封面、目錄、所有表格（含「框」與表內文字）、表標題（表 N｜）、表註（註：）、
      圖與圖說（圖 N｜）、參考文獻、附錄。
用法：python count_chars.py [docx 路徑]（預設 Huang_26254793_321513_A3.docx）
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
DOCX = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "Huang_26254793_321513_A3.docx"

CJK = re.compile(r"[一-鿿]")
# 英數詞：連續英數片段，含 $ % . , : / - + 等連接符（A$62,905、2:1、-0.21 各算 1）；圓圈數字 ①② 各算 1
WORD = re.compile(r"[A-Za-z0-9$%][A-Za-z0-9$%.,:/+\-]*|[①-⑳]")
EXCLUDE_PARA = re.compile(r"^(表 [0-9A-Z]+｜|圖 [0-9A-Z]+｜|註：)")


def iter_body(doc):
    """依文件順序產生 ('p', paragraph) 或 ('t', None)。"""
    from docx.text.paragraph import Paragraph
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            yield "p", Paragraph(el, doc)
        elif el.tag == qn("w:tbl"):
            yield "t", None


def count(text):
    cjk = len(CJK.findall(text))
    words = len(WORD.findall(CJK.sub(" ", text)))
    return cjk, words


def main():
    doc = Document(str(DOCX))
    started = False
    rows = []  # (h1, h2, kind, cjk, words, text)
    h1 = h2 = ""
    for kind, p in iter_body(doc):
        if kind == "t":
            continue
        style = p.style.name if p.style is not None else ""
        text = p.text.strip()
        if style == "Heading 1":
            if text.startswith("0 摘要"):
                started = True
            if text.startswith("參考文獻"):
                break
            h1, h2 = text, ""
        elif style == "Heading 2":
            h2 = text
        if not started or not text:
            continue
        if style not in ("Heading 1", "Heading 2") and EXCLUDE_PARA.match(text):
            continue
        c, w = count(text)
        rows.append((h1, h2, "標題" if style.startswith("Heading") else "正文", c, w, text))

    tot_c = sum(r[3] for r in rows)
    tot_w = sum(r[4] for r in rows)
    print(f"檔案：{DOCX.name}")
    print(f"{'節':<34}{'漢字':>6}{'英數':>6}{'合計':>7}")
    sections = {}
    for h1_, h2_, _, c, w, _ in rows:
        key = h1_
        s = sections.setdefault(key, {"c": 0, "w": 0, "sub": {}})
        s["c"] += c
        s["w"] += w
        sub = s["sub"].setdefault(h2_ or "（節首）", [0, 0])
        sub[0] += c
        sub[1] += w
    for key, s in sections.items():
        print(f"{key:<34}{s['c']:>6}{s['w']:>6}{s['c'] + s['w']:>7}")
        if len(s["sub"]) > 1:
            for sk, (c, w) in s["sub"].items():
                print(f"    {sk:<30}{c:>6}{w:>6}{c + w:>7}")
    head_c = sum(r[3] for r in rows if r[2] == "標題")
    head_w = sum(r[4] for r in rows if r[2] == "標題")
    print("-" * 53)
    print(f"{'正文合計（含標題）':<30}{tot_c:>6}{tot_w:>6}{tot_c + tot_w:>7}")
    print(f"{'  其中標題':<32}{head_c:>6}{head_w:>6}{head_c + head_w:>7}")
    print(f"TOTAL={tot_c + tot_w} CJK={tot_c} WORDS={tot_w}")


if __name__ == "__main__":
    main()
