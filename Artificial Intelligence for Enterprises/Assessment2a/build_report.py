# -*- coding: utf-8 -*-
# A2a 報告產生器 v2(Codex round1 十八條缺陷全修)
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

EAST = '微軟正黑體'

def set_font(run, size=11, bold=False, italic=False):
    run.font.name = 'Calibri'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), EAST)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic

def para(doc, text, size=11, bold=False, align=None, space_after=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    set_font(r, size, bold)
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p

def heading(doc, text):
    h = doc.add_heading(level=1)
    r = h.add_run(text)
    set_font(r, 14, True)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_toc(doc):
    p = doc.add_paragraph()
    r = p.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin'); f1.set(qn('w:dirty'), 'true')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'TOC \\o "1-1" \\h \\z \\u'
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'separate')
    t = OxmlElement('w:t'); t.text = '(開啟文件後目錄將自動更新)'
    f3 = OxmlElement('w:fldChar'); f3.set(qn('w:fldCharType'), 'end')
    for el in (f1, it, f2, t, f3): r._r.append(el)

def add_page_footer(doc):
    sec = doc.sections[0]
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'PAGE'
    f3 = OxmlElement('w:fldChar'); f3.set(qn('w:fldCharType'), 'end')
    for el in (f1, it, f3): r._r.append(el)
    set_font(r, 9)

def table(doc, caption, headers, rows, source_note, font_size=9.5):
    cap = doc.add_paragraph(); rc = cap.add_run(caption); set_font(rc, 10, True)
    cap.paragraph_format.space_after = Pt(3)
    cap.paragraph_format.keep_with_next = True          # 標題不與表格分頁
    tb = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tb.style = 'Table Grid'
    # 表頭列跨頁重複
    trPr = tb.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    for row in tb.rows:                                  # 單列不跨頁分割
        rp = row._tr.get_or_add_trPr()
        cs = OxmlElement('w:cantSplit'); rp.append(cs)
    for j, h in enumerate(headers):
        r = tb.rows[0].cells[j].paragraphs[0].add_run(h); set_font(r, font_size, True)
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row):
            r = tb.rows[i].cells[j].paragraphs[0].add_run(str(v)); set_font(r, font_size)
    note = doc.add_paragraph(); r = note.add_run(source_note); set_font(r, 8.5, italic=True)
    note.paragraph_format.space_after = Pt(10)
    return tb

def fig(doc, caption, path, source_note):
    cap = doc.add_paragraph(); rc = cap.add_run(caption); set_font(rc, 10, True)
    cap.paragraph_format.space_after = Pt(3)
    cap.paragraph_format.keep_with_next = True          # 標題不與圖分頁
    doc.add_picture(path, width=Inches(5.9))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.keep_with_next = True
    note = doc.add_paragraph(); r = note.add_run(source_note); set_font(r, 8.5, italic=True)
    note.paragraph_format.space_after = Pt(10)

def count_units(texts):
    # Word 口徑近似:中日韓字元(含全形標點)逐字計 1,英文/數字連續串計 1
    n = 0
    for t in texts:
        n += len(re.findall('[一-鿿　-〿＀-￯]', t))
        n += len(re.findall('[A-Za-z0-9]+', t))
    return n

# ─────────────────────────── 內文 ───────────────────────────
BODY = {}

BODY['管理摘要'] = (
"本報告為電信公司建立客戶流失(Churn)預測的概念驗證。以 3,333 筆手機使用數據比較六種分類模型,"
"依事前訂定的規則推薦 XGBoost 為最終模型(測試集 accuracy 0.925、F1 0.715;RandomForest 表現相當,列為次選)。"
"最終模型於測試集漏判 51 名實際流失客戶(False Negative),十二個月收入暴露上限約 A$35,926;"
"以挽留成功率三成的情境估算,約 A$10,778 為可挽回價值。最重要變數為日間通話分鐘數;"
"月費與客服來電次數為同層級第二梯隊;合約續約次之。第四節據此提出三項行動與優先順序。")

BODY['一、分類模型的評估與推薦'] = [
("沿用課程範本流程並加入方法改進:分層抽樣切分(70/30,random_state=42,兩集流失比例約 14.5%)、"
"以 Pipeline 封裝使縮放只在訓練折內擬合、模型選擇僅使用訓練集的 5×5 重複分層交叉驗證(共 25 個折次);"
"測試集不參與任何模型與配置選擇,僅於選模完成後用於最終評估與解釋。"
"資料高度不平衡:把全部客戶預測為「不流失」也有 85.5% 的 accuracy,"
"因此評估以 churn 類的 F 值、召回率(recall)與精確率(precision)為主,accuracy 為輔。"),
("結果如表一與圖一:XGBoost 與 RandomForest 明顯領先其餘四模型,交叉驗證 F1 幾乎相同(0.732 對 0.732),"
"經重複交叉驗證的校正檢定(Nadeau & Bengio, 2003),F1、recall、precision 皆無統計顯著差異。"
"兩模型性能相當,故依事前訂定的業務平手規則裁決:流失情境下 recall 直接對應漏抓的流失客戶,"
"取 recall 均值較高的 XGBoost(0.656 對 0.639)為最終模型——此為規則選定,而非性能勝出。"
"單次測試集上 RandomForest 的 F1(0.745)較高,惟成對 bootstrap 95% 信賴區間 [−0.001, +0.064] 與零相容;"
"依協議不以測試集回選,RandomForest 列為次選。")]

BODY['二、最佳模型誤判造成的收入損失'] = [
("混淆矩陣(圖二)中的 False Negative(FN)是實際流失卻被預測為留存的客戶:公司不會對其啟動挽留,收入默默流失。"
"XGBoost 於測試集(1,000 筆,含 145 名流失者)產生 51 名 FN,其實際月費合計 A$2,993.8(平均每人每月 A$58.7)。"),
("損失以三層呈現(表二):以留存十二個月為基準情境,毛收入暴露上限約 A$35,926;"
"獲取新客成本為留客的五至二十五倍(Gallo, 2014),故設挽留成功率 30% 的管理情境,預期可挽回價值約 A$10,778。"
"將測試集 FN 率外推至全體 483 名流失者,預估漏抓約 170 人、年暴露約 A$119,669,屬量級參考而非預測。"
"本估算為毛收入口徑的範圍界定:未扣除毛利率、挽留方案成本與自然回流,實際淨損失視此三者而定(表二附 6/24 個月敏感度)。")]

BODY['三、最重要屬性的識別與領域解釋'] = [
("各模型原生重要度排序並不一致,單看任一模型不足以下結論,"
"故以最終模型在測試集上的 permutation importance 裁決(重複 30 次、以 F1 評分):"
"日間通話分鐘數(DayMins)在 30 次重複中全數排名第一;月費(MonthlyCharge)與客服來電次數(CustServCalls)"
"互有領先(23/30),屬同層級第二梯隊;合約續約(ContractRenewal)多數位居第四(圖三)。"
"此一致性屬同一已擬合模型與同一測試集內的結果,而非跨樣本重訓的穩健性宣稱。"),
("原始資料的群組差異支持此結果(表三):流失者的日間通話、月費與客服來電均較高,續約率明顯較低。"),
("領域解釋(與資料一致的假說,非因果結論):高用量客戶帳單高,可能對資費與體驗較敏感——"
"與電信文獻「重度使用為流失關鍵預測因子」一致(Ahmad et al., 2019);頻繁致電客服是可觀察的不滿信號;"
"未續約客戶轉換成本低。另 DayMins 與 MonthlyCharge 中度相關(r = 0.57),重要度可能互相分攤,"
"宜視為同一「高用量-高帳單」信號;流失模型的價值正在於及早識別此類高風險組合(Neslin et al., 2006)。")]

BODY['四、降低客戶流失率的策略'] = [
("挽留策略完全建立於第三節識別的變數,由模型評分驅動:每月以 XGBoost 對全體客戶評分,高風險名單交由挽留團隊執行三項行動。"
"試點門檻、覆蓋與該群實際流失率見表四:三個門檻群流失率為全體的 1.8 至 2.9 倍,確實鎖定高風險客群;門檻於正式上線前依模型分數細調。"),
("行動一(對應 CustServCalls)服務恢復:來電達門檻即觸發專員回訪與問題升級,直接處理不滿來源。"
"行動二(對應 ContractRenewal)續約轉化:向未續約的高風險客戶提供限時續約優惠,鎖定流失最集中的客群。"
"行動三(對應 DayMins 與 MonthlyCharge)高用量資費重組:主動推薦封頂或客製方案,預防帳單震撼。"),
("優先順序為一、二、三(表四)。各行動以試點先行、隨機保留對照組,三個月檢視 KPI,該群流失率未優於對照組即停止並檢討。"
"以 30% 挽留情境計,年可挽回毛收入 A$10,778 可作為行動一、二試點成本的粗略上限參考(未調整毛利率)。")]

BODY['結論'] = (
"本概念驗證確認:現有數據即可建立可用的流失預測模型;XGBoost 為依事前規則選定的推薦模型;"
"誤判成本可量化為挽留投資的依據;重要變數排序於重複檢驗中一致且具清楚業務意涵。"
"建議先將行動一試點上線,三個月後以 KPI 檢視並逐步擴大。")

# ─────────────────────────── 組裝 ───────────────────────────
doc = Document()
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'), EAST)
add_page_footer(doc)

# 封面
for _ in range(5): doc.add_paragraph()
para(doc, '電信客戶流失預測概念驗證報告', 20, True, WD_ALIGN_PARAGRAPH.CENTER)
para(doc, '評估任務二a:使用監督學習技術分析數據', 14, False, WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
for line in ('課程:421104 Artificial Intelligence for Enterprises(企業人工智能)',
             '姓名:黃柏凱(PoKai Huang)', '學號:26254793',
             '參考格式:APA 第 7 版', '日期:2026 年 7 月',
             '附件:Huang_26254793_421104_Assessment 2a.ipynb(完整程式與輸出)'):
    para(doc, line, 12, False, WD_ALIGN_PARAGRAPH.CENTER, 4)
doc.add_page_break()

# 目錄
para(doc, '目錄', 14, True)
add_toc(doc)
doc.add_page_break()

# 管理摘要
heading(doc, '管理摘要')
para(doc, BODY['管理摘要'])

# 一、
heading(doc, '一、分類模型的評估與推薦')
para(doc, BODY['一、分類模型的評估與推薦'][0])
table(doc, '表一、六模型於 5×5 重複分層交叉驗證與保留測試集之表現(churn 類指標)',
    ['模型', 'CV F1(mean±std)', '測試 Accuracy', '測試 Precision', '測試 Recall', '測試 F1'],
    [['XGBoost(推薦)', '0.732 ± 0.053', '0.925', '0.797', '0.648', '0.715'],
     ['RandomForest(次選)', '0.732 ± 0.053', '0.935', '0.864', '0.655', '0.745'],
     ['SVC(balanced)', '0.652 ± 0.034', '0.854', '0.498', '0.807', '0.616'],
     ['DecisionTree', '0.625 ± 0.047', '0.878', '0.578', '0.586', '0.582'],
     ['KNN', '0.555 ± 0.042', '0.892', '0.713', '0.428', '0.535'],
     ['LogisticRegression(balanced)', '0.483 ± 0.028', '0.765', '0.356', '0.766', '0.486']],
    '註:資料來源為附件 notebook 第八、九節輸出;CV 僅用訓練集,測試集不參與模型與配置選擇。')
para(doc, BODY['一、分類模型的評估與推薦'][1])
fig(doc, '圖一、六分類器於保留測試集之表現', 'figures/fig1_model_comparison.png',
    '註:虛線為「全猜不流失」的 accuracy 基準(85.5%)。資料來源:附件 notebook 第九節。')

# 二、
heading(doc, '二、最佳模型誤判造成的收入損失')
para(doc, BODY['二、最佳模型誤判造成的收入損失'][0])
fig(doc, '圖二、XGBoost 測試集混淆矩陣(FN = 51)', 'figures/fig2_confusion_winner.png',
    '註:FN = 實際流失(1)而被預測為留存(0)。資料來源:附件 notebook 第十節。')
para(doc, BODY['二、最佳模型誤判造成的收入損失'][1])
table(doc, '表二、FN 收入損失三層估算(依 FN 個體實際月費)',
    ['留存假設', '測試集 FN 毛暴露上限', '預期可挽回(@30%)', '全資料集預估 FN 暴露(推估)'],
    [['6 個月', 'A$17,963', 'A$5,389', 'A$59,835'],
     ['12 個月(基準)', 'A$35,926', 'A$10,778', 'A$119,669'],
     ['24 個月', 'A$71,851', 'A$21,555', 'A$239,339']],
    '註:挽留成功率 30% 為管理情境假設;挽留之高報酬依據為獲客成本高於留客五至二十五倍(Gallo, 2014)。'
    '全資料集欄以測試集 FN 率外推(約 170 人),屬量級推估。資料來源:附件 notebook 第十一節。')

# 三、
heading(doc, '三、最重要屬性的識別與領域解釋')
para(doc, BODY['三、最重要屬性的識別與領域解釋'][0])
fig(doc, '圖三、Permutation importance(測試集,重複 30 次,scoring=F1)', 'figures/fig3_perm_importance.png',
    '註:橫軸為打亂該欄後 F1 的平均降幅(±標準差)。資料來源:附件 notebook 第十三節。')
para(doc, BODY['三、最重要屬性的識別與領域解釋'][1])
table(doc, '表三、重要變數於流失/未流失群組的平均值差異',
    ['變數', '未流失(Churn=0)', '流失(Churn=1)', '差異方向'],
    [['DayMins(日間通話分鐘)', '175.2', '206.9', '流失者較高'],
     ['MonthlyCharge(月費, A$)', '55.8', '59.2', '流失者較高'],
     ['CustServCalls(客服來電次數)', '1.45', '2.23', '流失者較高'],
     ['ContractRenewal(續約率)', '93.5%', '71.6%', '流失者較低']],
    '註:全體 3,333 筆之群組平均。資料來源:附件 notebook 第十四節。')
para(doc, BODY['三、最重要屬性的識別與領域解釋'][2])

# 四、
heading(doc, '四、降低客戶流失率的策略')
para(doc, BODY['四、降低客戶流失率的策略'][0])
table(doc, '表四、三項行動之試點設計與決策矩陣',
    ['行動(對應變數)', '試點門檻', '覆蓋客群', '該群流失率(倍數)', '成本/時程', '負責單位', '優先'],
    [['一、服務恢復\n(CustServCalls)', '來電 ≥3 次', '696 人(21%)', '26.1%(1.8×)', '低/即刻', '客服部', '1'],
     ['二、續約轉化\n(ContractRenewal)', '未續約', '323 人(10%)', '42.4%(2.9×)', '中/1–2 月', '行銷部', '2'],
     ['三、資費重組\n(DayMins/MonthlyCharge)', '日通話 ≥216 分且月費 ≥ 中位(A$53.5)', '767 人(23%)', '31.3%(2.2×)', '中高/3–6 月', '資費部', '3']],
    '註:覆蓋與流失率為全資料集實算(附件 notebook);倍數 = 該群流失率 ÷ 全體 14.5%。'
    '各行動共同停止條件:試點三個月後該群流失率未優於隨機對照組即停止。', font_size=9)
para(doc, BODY['四、降低客戶流失率的策略'][1])
para(doc, BODY['四、降低客戶流失率的策略'][2])

# 結論
heading(doc, '結論')
para(doc, BODY['結論'])

# 參考文獻(期刊名+卷斜體)
heading(doc, '參考文獻')
REFS = [
 [('Ahmad, A. K., Jafar, A., & Aljoumaa, K. (2019). Customer churn prediction in telecom using machine learning in big data platform. ', False),
  ('Journal of Big Data, 6', True), (', Article 28. https://doi.org/10.1186/s40537-019-0191-6', False)],
 [('Gallo, A. (2014, October 29). The value of keeping the right customers. ', False),
  ('Harvard Business Review', True), ('. https://hbr.org/2014/10/the-value-of-keeping-the-right-customers', False)],
 [('Nadeau, C., & Bengio, Y. (2003). Inference for the generalization error. ', False),
  ('Machine Learning, 52', True), ('(3), 239–281. https://doi.org/10.1023/A:1024068626366', False)],
 [('Neslin, S. A., Gupta, S., Kamakura, W., Lu, J., & Mason, C. H. (2006). Defection detection: Measuring and understanding the predictive accuracy of customer churn models. ', False),
  ('Journal of Marketing Research, 43', True), ('(2), 204–211. https://doi.org/10.1509/jmkr.43.2.204', False)],
]
for segs in REFS:
    p = doc.add_paragraph()
    for text, ital in segs:
        r = p.add_run(text); set_font(r, 10.5, italic=ital)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.space_after = Pt(6)

OUT = 'Huang_26254793_421104_Assessment 2a.docx'
doc.save(OUT)

# 字數
units = count_units(['管理摘要', '一、分類模型的評估與推薦', '二、最佳模型誤判造成的收入損失',
                     '三、最重要屬性的識別與領域解釋', '四、降低客戶流失率的策略', '結論'])
for k in ('管理摘要', '結論'):
    units += count_units([BODY[k]])
for k in ('一、分類模型的評估與推薦', '二、最佳模型誤判造成的收入損失',
          '三、最重要屬性的識別與領域解釋', '四、降低客戶流失率的策略'):
    units += count_units(BODY[k])
print(f'SAVED: {OUT}')
print(f'字數(近似 Word 口徑,含標題,不含表格/圖說/文獻):{units}(規定 1350–1650,安全目標 ≤1600)')
