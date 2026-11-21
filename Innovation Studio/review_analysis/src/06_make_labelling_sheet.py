"""做一份給人標的表(Excel):60 條評論,每條 7 個方面 + 整體感受,用下拉選單填。
用途:請兩位隊友各自標一次,當「人工答案」,才能算 AI 讀得準不準。
輸出只留本機(含評論原文):data/labelling_sheet_60_local.xlsx
"""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

BASE = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(BASE / "data/sample_listing10_input_second60.csv", encoding="utf-8")))
assert len(rows) == 60

ASPECTS = ["清潔", "噪音", "位置與交通", "入住", "房東溝通", "性價比", "設施與舒適"]
wb = Workbook()

# ---------- 說明 ----------
ws = wb.active
ws.title = "說明"
lines = [
    ("怎麼標(請先看完這一頁,大約 5 分鐘)", True),
    ("", False),
    ("要做什麼:第二個分頁有 60 條英文評論。每一條請判斷它有沒有講到下面 7 件事,是好評還是抱怨。用下拉選單選。", False),
    ("為什麼:我們讓 AI 讀了這些評論。要知道 AI 讀得準不準,需要人自己標一次當答案。請不要互相討論,各標各的。", False),
    ("大約要多久:30 到 40 分鐘。", False),
    ("", False),
    ("7 件事", True),
    ("清潔:乾不乾淨(乾淨、髒、灰塵、發霉、有味道、有蟲)。打掃人員做得好不好也算這一項。", False),
    ("噪音:吵不吵(街上的聲音、鄰居、施工、隔音差;或是「很安靜」)。", False),
    ("位置與交通:地點好不好、離海邊/商店/市中心近不近、大眾交通方不方便。", False),
    ("入住:拿鑰匙、密碼、進門、退房、入住說明清不清楚、能不能提早或延後。", False),
    ("房東溝通:房東這個人或他的回覆(回得快、熱心、友善;或不回、態度差)。", False),
    ("性價比:值不值這個價錢(划算、太貴、費用)。", False),
    ("設施與舒適:屋裡的東西和住起來舒不舒服(床、廚房、網路、冷氣、熱水、空間、家具、停車、泳池、景觀)。東西壞了、維護得好不好也算這一項。", False),
    ("", False),
    ("每一格的 4 個選項", True),
    ("沒提到:這條評論沒有講到這件事。(留空白也算沒提到)", False),
    ("好評:有講到,只有稱讚。", False),
    ("負評:有講到,只有抱怨。客人說「如果有電風扇就好了」這種建議,也算負評。", False),
    ("有好有壞:同一件事既有稱讚也有抱怨。", False),
    ("", False),
    ("最後一欄「整體感受」", True),
    ("好:整條都是滿意的。", False),
    ("有好有壞:至少有一個明確的抱怨,也至少有一個明確的稱讚。(開心的評論裡夾一個小建議,也選這個)", False),
    ("壞:客人整體很不滿意。", False),
    ("", False),
    ("要注意", True),
    ("1. 只標評論明確寫出來的,不要猜。", False),
    ("2. 沒有主題的稱讚(「很棒的地方」「會再來」「推薦」)不算任何一件事,7 格都是沒提到。", False),
    ("3. 入住說明寫得清不清楚 → 入住。房東回得快不快、人好不好 → 房東溝通。一句話兩件事都有講,就兩格都填。", False),
    ("4. 拿不定主意的,在最後一欄「備註」寫一句為什麼。這些地方之後要拿來改規則。", False),
    ("5. 標完請把檔名加上自己的名字,私下傳回來。這個檔有評論原文,請不要放到公開的地方。", False),
]
for i, (t, bold) in enumerate(lines, start=1):
    c = ws.cell(row=i, column=1, value=t)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if bold:
        c.font = Font(bold=True, size=12)
ws.column_dimensions["A"].width = 120

# ---------- 標註 ----------
ws2 = wb.create_sheet("標註")
head = ["編號", "評論原文"] + ASPECTS + ["整體感受", "備註(拿不定主意時寫)"]
ws2.append(head)
for c in ws2[1]:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="DDEBF7")
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
for r in rows:
    ws2.append([r["rid"], r["text"]] + [""] * (len(ASPECTS) + 2))
n = len(rows) + 1
dv = DataValidation(type="list", formula1='"沒提到,好評,負評,有好有壞"', allow_blank=True)
dv2 = DataValidation(type="list", formula1='"好,有好有壞,壞"', allow_blank=True)
ws2.add_data_validation(dv)
ws2.add_data_validation(dv2)
dv.add("C2:I%d" % n)
dv2.add("J2:J%d" % n)
ws2.column_dimensions["A"].width = 8
ws2.column_dimensions["B"].width = 90
for col in "CDEFGHI":
    ws2.column_dimensions[col].width = 12
ws2.column_dimensions["J"].width = 12
ws2.column_dimensions["K"].width = 36
for row in ws2.iter_rows(min_row=2, max_row=n):
    row[1].alignment = Alignment(wrap_text=True, vertical="top")
    row[0].alignment = Alignment(vertical="top")
ws2.freeze_panes = "C2"
out = BASE / "data/labelling_sheet_60_local.xlsx"
wb.save(out)
print("寫好了:", out, "| 評論", len(rows), "條 | 總字元", sum(len(r["text"]) for r in rows))
