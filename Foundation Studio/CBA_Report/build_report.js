// CBA Report Generator — 231708 Foundation Studio Assessment Task 1 (v2 with IBISWorld PDF additions)
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  ExternalHyperlink, TabStopType, TabStopPosition,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak,
} = require('docx');

const FIG_DIR = '/sessions/brave-vigilant-gauss/mnt/Foundation Studio/CBA_Report/figures';

const FONT = 'DengXian';
const FONT_ENG = 'Arial';
const SIZE_BODY = 24;
const SIZE_H1 = 32;
const SIZE_H2 = 28;
const SIZE_H3 = 26;
const LINE_SPACING = 360;
const PARA_SPACING = 120;

const PAGE_WIDTH = 11906;
const PAGE_HEIGHT = 16838;
const MARGIN = 1417;

function bodyPara(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_BODY })],
    alignment: opts.alignment || AlignmentType.JUSTIFIED,
    spacing: { line: LINE_SPACING, after: PARA_SPACING, ...opts.spacing },
    indent: opts.indent,
  });
}

function inlineRuns(parts) {
  return parts.map(p => new TextRun({
    text: p.text,
    font: FONT,
    size: SIZE_BODY,
    bold: p.bold || false,
    italics: p.italic || false,
  }));
}

function richPara(parts, opts = {}) {
  return new Paragraph({
    children: inlineRuns(parts),
    alignment: opts.alignment || AlignmentType.JUSTIFIED,
    spacing: { line: LINE_SPACING, after: PARA_SPACING, ...opts.spacing },
  });
}

function h1(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_H1, bold: true })],
    spacing: { before: 360, after: 180, line: LINE_SPACING },
    heading: HeadingLevel.HEADING_1,
  });
}

function h2(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_H2, bold: true })],
    spacing: { before: 240, after: 120, line: LINE_SPACING },
    heading: HeadingLevel.HEADING_2,
  });
}

function caption(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: 20, italics: true })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 100, after: 200, line: LINE_SPACING },
  });
}

function image(filename, widthCm = 14, heightCm = 8) {
  const filePath = path.join(FIG_DIR, filename);
  return new Paragraph({
    children: [new ImageRun({
      type: 'png',
      data: fs.readFileSync(filePath),
      transformation: { width: Math.round(widthCm * 28.35), height: Math.round(heightCm * 28.35) },
      altText: { title: filename, description: filename, name: filename },
    })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 100 },
  });
}

const border = { style: BorderStyle.SINGLE, size: 4, color: '666666' };
const borders = { top: border, bottom: border, left: border, right: border };

function tableCell(text, width, opts = {}) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.header ? { fill: '04254A', type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      children: [new TextRun({
        text,
        font: FONT,
        size: 22,
        bold: opts.bold || opts.header || false,
        color: opts.header ? 'FFFFFF' : (opts.color || '000000'),
      })],
      alignment: opts.alignment || AlignmentType.CENTER,
      spacing: { line: 280 },
    })],
  });
}

function makeTable(headers, rows, columnWidths) {
  const headerRow = new TableRow({
    children: headers.map((h, i) => tableCell(h, columnWidths[i], { header: true })),
    tableHeader: true,
  });
  const dataRows = rows.map(row => new TableRow({
    children: row.map((cell, i) => {
      const isFirst = i === 0;
      const isBold = typeof cell === 'object' && cell.bold;
      const text = typeof cell === 'object' ? cell.text : cell;
      return tableCell(text, columnWidths[i], {
        bold: isBold,
        alignment: isFirst ? AlignmentType.LEFT : AlignmentType.CENTER,
      });
    }),
  }));
  return new Table({
    width: { size: columnWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths,
    rows: [headerRow, ...dataRows],
  });
}

// ============== BUILD CONTENT ==============
const children = [];

// Title page
children.push(new Paragraph({
  children: [new TextRun({ text: '澳洲聯邦銀行(CBA)房貸業務行業分析', font: FONT, size: 40, bold: true })],
  alignment: AlignmentType.CENTER,
  spacing: { before: 2000, after: 240, line: 480 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: 'Industry Analysis of Commonwealth Bank of Australia (CBA) Home Loan Business', font: FONT_ENG, size: 28, italics: true })],
  alignment: AlignmentType.CENTER,
  spacing: { after: 400, line: 360 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: '231708 Foundation Studio — 評估任務一:案例分析', font: FONT, size: 24 })],
  alignment: AlignmentType.CENTER,
  spacing: { after: 120 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: 'ANZSIC 2006 Division K | Class 6221 Banks (IBISWorld K6221A)', font: FONT_ENG, size: 22 })],
  alignment: AlignmentType.CENTER,
  spacing: { after: 600 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: '學生:PoKai Huang', font: FONT, size: 22 })],
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: '日期:2026 年 5 月', font: FONT, size: 22 })],
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: '字數:約 2,400 字(不含參考文獻)', font: FONT, size: 22 })],
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
}));
children.push(new Paragraph({ children: [new PageBreak()] }));

// Executive Summary
children.push(h1('摘要(Executive Summary)'));
children.push(bodyPara('本報告以澳洲聯邦銀行(Commonwealth Bank of Australia, CBA;ASX: CBA)之住宅房貸業務為案例,分析其所處的全國與區域商業銀行業(ANZSIC 2006 Class 6221)。研究運用 Porter 五力模型與 SWOT 框架,結合 IBISWorld、APRA、RBA 與 CoreLogic 之最新數據,評估 CBA 房貸組合在行業循環中的相對地位。報告顯示,CBA 雖在 2024–2025 年面臨利差壓縮與同業競爭加劇,仍以 25.4% 的房貸市占穩居行業領導者,其營收成長(+4.2%)亦顯著跑贏行業整體(−8.3%)。展望 2026 年,RBA 重啟升息、移民放緩、首購政策刺激三股力量並行,CBA 房貸業務面臨量價拉鋸的關鍵轉折,管理層宜以「規模優勢 + 自有通路 + 數位轉型」三軸防禦並深化高品質客群滲透。'));

// Section 1
children.push(h1('1. 公司背景(Company Overview)'));
children.push(h2('1.1 公司簡介'));
children.push(richPara([
  { text: '澳洲聯邦銀行(CBA)', bold: true },
  { text: ' 為澳洲市值最大的金融機構,1911 年成立,1991 年完成民營化並於澳交所(ASX)掛牌。截至 2025 年 6 月 30 日(FY25 財政年度),CBA 擁有約 1,700 萬名客戶與 51,346 名員工,服務人口涵蓋全澳三分之二(IBISWorld, 2025)。其旗下品牌包含 Aussie、Aussie Home Loans 與 Bankwest,核心業務分為:零售銀行服務(Retail Banking Services)、企業及機構銀行、紐西蘭子公司 ASB 與財富管理。' },
  { text: '本報告聚焦其最大且最具策略性的單一業務 — 住宅房貸', bold: true },
  { text: ',該業務貢獻 CBA 利息收入近六成,亦為澳洲整體銀行業最大產品線(2025 年規模 A$161.5 bn,占行業營收 62.3%)(IBISWorld, 2025)。' }
]));

children.push(h2('1.2 ANZSIC 行業分類'));
children.push(bodyPara('依澳大利亞和新西蘭標準產業分類(ANZSIC 2006)系統,CBA 歸入:'));
children.push(bodyPara('• Division K — 金融與保險業(Finance and Insurance Services)', { indent: { left: 720 } }));
children.push(bodyPara('• Subdivision 62 — 金融(Finance)', { indent: { left: 720 } }));
children.push(bodyPara('• Group 622 — 存款型金融中介(Depository Financial Intermediation)', { indent: { left: 720 } }));
children.push(bodyPara('• Class 6221 — 銀行業(Banks)', { indent: { left: 720 } }));
children.push(bodyPara('IBISWorld 將此 Class 進一步區分為 K6221A — National and Regional Commercial Banks in Australia(本國/區域商業銀行)與 K6221B(外資銀行),CBA 屬於 K6221A(IBISWorld, 2025)。'));

children.push(h2('1.3 三年財務概況'));
children.push(makeTable(
  ['指標', 'FY23', 'FY24', 'FY25'],
  [
    ['Cash NPAT(現金淨利)', 'A$10,164 m', 'A$9,836 m', { text: 'A$10,252 m', bold: true }],
    ['Cash NPAT 年增率', '+6.0%', '−3.2%', '+4.2%'],
    ['淨利息差(NIM)', '2.07%', '1.99%(↓8 bp)', '2.08%(+9 bp)'],
    ['股東權益報酬率(ROE)', '14.0%', '13.6%', '13.5%'],
    ['每股盈餘(EPS)', 'A$5.97', 'A$5.83', 'A$6.12'],
    ['全年股利(每股)', 'A$4.50', 'A$4.65', 'A$4.85'],
    ['房貸組合(年底)', '~A$558 bn', 'A$586 bn', 'A$611 bn (Nov-25)'],
  ],
  [3200, 1957, 1957, 1958]
));
children.push(caption('表 1:CBA 三年關鍵財務指標(資料來源:CBA Annual Reports 2023–2025;APRA, 2025)'));
children.push(bodyPara('CBA 房貸組合在 FY25 達 A$611 bn,年增 +6.5%,顯著高於行業整體成長率約 +4.5%(APRA, 2025)。'));

children.push(image('fig2_cba_npat.png', 13, 7));
children.push(caption('圖 2:CBA Cash NPAT(FY23–FY25)— 資料來源:CBA Annual Reports'));

// Section 2
children.push(h1('2. 行業整體表現(Industry Performance)'));

children.push(h2('2.1 行業規模與成長'));
children.push(richPara([
  { text: 'IBISWorld(2025)顯示,澳洲本國 / 區域商業銀行業(K6221A)2025 年營收達 ' },
  { text: 'A$259.2 bn', bold: true },
  { text: ',過去五年複合年增率(CAGR)+9.3%,顯著高於同期 GDP 平均 CAGR(約 +2.8%),反映行業在 RBA 升息週期中享受利息收入結構性擴張之紅利。然而,2025 年單年營收下滑 −8.3%,且未來五年預測 CAGR 僅 +0.3%,顯示行業已步入成熟期(Mature Life Cycle)。利潤率自 2020 年高峰 23.4% 下滑至 2025 年 22.3%(降幅 1.1 pp),反映存款定價戰侵蝕淨利差。受 2022–23 升息衝擊,該年度房屋過戶數驟降 18.7%,造成銀行新貸款業務量收縮(IBISWorld, 2025)。' }
]));

children.push(h2('2.2 全體 ADI 表現'));
children.push(richPara([
  { text: 'APRA 季度 ADI Performance Statistics(2024)指出,全體授權存款機構(ADI)2024 年累計淨利為 A$39.0 bn。資產規模方面,2025 年 3 月底全行業總資產達 A$9.8 兆,住宅房貸總餘額達 ' },
  { text: 'A$2.29 兆', bold: true },
  { text: '(其中自住房貸 1.56 兆、投資房貸 0.73 兆),為行業最大資產類別(APRA, 2025)。' }
]));

children.push(h2('2.3 行業集中度'));
children.push(richPara([
  { text: '四大行(CBA、Westpac、NAB、ANZ)合計房貸市占於 2025 年 3 月達 ' },
  { text: '74.6%', bold: true },
  { text: '(APRA),屬高度集中之寡占市場(Oligopoly)。其中 CBA 以 25.4% 居首,領先第二名 Westpac 約 7.2 個百分點。IBISWorld(2025)以行業總營收計,四大行合計亦達 75.6%,赫芬達指數(HHI)估算約 1,800,屬中度走向高度集中。' }
]));

children.push(image('fig1_market_share_pie.png', 12, 9));
children.push(caption('圖 1:澳洲銀行業 K6221A 市占率(2025)— 資料來源:IBISWorld(2025)'));

// Section 3
children.push(h1('3. CBA 相對於行業表現(Company vs Industry)'));
children.push(bodyPara('對比 IBISWorld 行業基準與 CBA 自身數據,可見 CBA 在多項關鍵指標上跑贏行業:'));

children.push(makeTable(
  ['指標', 'CBA(FY25)', '行業基準', '差距'],
  [
    ['營收 / Cash NPAT 年增率', '+4.2%', '−8.3%', { text: '+12.5 pp', bold: true }],
    ['房貸組合年成長', '+6.5%', '~+4.5%', '+2.0 pp'],
    ['NIM(淨利息差)', '2.08%', '~1.85%', '+23 bp'],
    ['ROE', '13.5%', 'n/a', '高於四大行均值 ~12%'],
    ['自有通路新貸款占比', '66%', '~50%', '+16 pp'],
  ],
  [3600, 1824, 1824, 1824]
));
children.push(caption('表 2:CBA 對行業基準指標對比(資料來源:CBA 2025 Full Year Results;IBISWorld, 2025;APRA, 2025)'));

children.push(richPara([
  { text: 'CBA 表現優於行業的關鍵原因有三:' },
  { text: '第一,規模優勢攤平固定成本', bold: true },
  { text: ',在 NIM 收窄期間仍能維持較高邊際利潤;' },
  { text: '第二,自有通路占比 66%', bold: true },
  { text: ',降低對房貸經紀商(Mortgage Brokers)之佣金支出,行業內競爭者多達 40–50% 透過 broker 取得新貸款;' },
  { text: '第三,客戶基礎廣', bold: true },
  { text: ',1,700 萬客戶提供強大交叉銷售與資料優勢,降低獲客成本。' }
]));
children.push(bodyPara('四大行內部對比中,CBA 房貸組合(A$611.5 bn,Nov 2025)為 Westpac(A$498.5 bn)的 1.23 倍、NAB 的 1.79 倍、ANZ 的 1.90 倍。年增率亦居四大行之首(+6.5% vs WBC +3.9%、NAB +5.5%、ANZ +4.7%)(APRA, 2025)。然而,Macquarie Bank 之房貸組合於同期達 A$160.8 bn 並以年增率近 +20% 快速逼近 ANZ,顯示非傳統四大行勢力崛起。'));

children.push(image('fig4_big4_mortgage_books.png', 14, 8));
children.push(caption('圖 4:四大行 + Macquarie 房貸組合餘額對比(Nov 2025)— 資料來源:APRA Monthly ADI Statistics'));

children.push(bodyPara('CBA 在 K6221A 行業之長期市占走勢(2013–2025)如圖 6 所示,呈現「疫情期高峰、升息期回落、復甦中」三段循環。市占於 2022 年高點 24.8% 後因利率快速上升,2024 年降至 20.0%,2025 年回升至 21.7%,顯示其在新一輪利率循環中重新搶回市場領導地位(IBISWorld, 2025)。'));

children.push(image('fig6_cba_history.png', 15, 7.5));
children.push(caption('圖 6:CBA 在 K6221A 行業之營收與市占率(2013–2025)— 資料來源:IBISWorld(2025)'));

// Section 4 (CORE)
children.push(h1('4. 需求與供給因素討論(Demand and Supply Factors)'));
children.push(bodyPara('本節為報告核心,以 Porter 五力模型系統性檢視 CBA 房貸業務之競爭環境,並結合 SWOT 框架延伸至需求 / 供給雙面影響因子。'));

children.push(h2('4.1 五力競爭結構'));
children.push(bodyPara('IBISWorld(2025)對 K6221A 之五力評估如下:'));

children.push(makeTable(
  ['競爭力量', '強度', '趨勢'],
  [
    ['行業集中度', 'High', 'Stable'],
    ['現有業者競爭', 'High', '↑ Increasing'],
    ['新進入者威脅', 'Low(進入障礙 High,下降中)', '↓ Decreasing'],
    ['替代品威脅', 'Low', 'Steady'],
    ['買方議價力', 'Low', '↑ Increasing'],
    ['供應商議價力', 'High', 'Steady'],
  ],
  [3024, 3024, 3024]
));
children.push(caption('表 3:K6221A 五力強度與趨勢(資料來源:IBISWorld, 2025)'));

children.push(image('fig5_porter_radar.png', 12, 12));
children.push(caption('圖 5:Porter 五力強度雷達圖 — 資料來源:IBISWorld(2025),作者整理'));

children.push(richPara([
  { text: '現有業者競爭(High, Increasing↑)', bold: true },
  { text: ' 為 CBA 最大威脅。四大行內部競爭白熱化,Macquarie 與中型銀行(Bendigo, Suncorp)以較低利率切入;非銀行 fintech 放款方(Athena、Pepper Money、Tic:Toc)透過數位通路與低於 SVR 60–80 bp 的利率搶客。' },
  { text: '新進入者威脅', bold: true },
  { text: ' 雖因 APRA 銀行牌照仍構成顯著資本與合規門檻而保持 Low,但 Consumer Data Right(CDR,開放銀行)讓 fintech 取得客戶資料,降低部分壁壘(Australian Government, 2024)。' },
  { text: '替代品威脅 Low', bold: true },
  { text: ' — 房貸的最根本替代品為租屋與自有資金,但住房需求結構性穩固。' },
  { text: '買方議價力', bold: true },
  { text: ' 雖在個體層面偏低,但澳洲約 70% 新貸款透過房貸經紀商,broker 通路聚合需求進而提升整體買方議價力,迫使銀行讓利(MFAA, 2024)。' },
  { text: '供應商議價力(High)', bold: true },
  { text: ' — 銀行的「供應商」即存款戶與監管機構,升息期間存款戶積極比較利率推升銀行資金成本,直接擠壓 NIM。' }
]));

children.push(h2('4.2 需求面驅動因子'));
children.push(bodyPara('CBA 房貸需求受四項宏觀因子主導:'));

children.push(richPara([
  { text: '(1)RBA 利率政策', bold: true },
  { text: '為最關鍵變數。RBA 自 2022 年 5 月起連續升息 13 次至 4.35%(2023 年 11 月),為澳洲史上最快升息週期;2025 年 2–8 月短暫降息至 3.60%,然 2026 年 2–5 月通膨二度反撲,RBA 重啟升息回到 ' },
  { text: '4.35%', bold: true },
  { text: '(2026 年 5 月)(RBA, 2026)。每升息 25 bp,A$700,000 房貸戶月供約增 A$215,直接抑制新貸款申請。CBA FY24 NIM 下滑 8 bp 即反映此影響;FY25 NIM 回升至 2.08% 則受惠存款成本逐步穩定。' }
]));

children.push(image('fig3_rba_cashrate.png', 14, 6.5));
children.push(caption('圖 3:RBA Cash Rate 走勢(2022年4月–2026年5月)— 資料來源:Reserve Bank of Australia'));

children.push(richPara([
  { text: '(2)淨海外移民(NOM)', bold: true },
  { text: '為結構性需求支柱。ABS(2025)數據顯示,FY22–23 NOM 達歷史高點 53.8 萬,FY24–25 雖降至 30.6 萬,但 2022–2025 三年累計移民達 130 萬人,而住房新建供給僅約 65 萬戶,' },
  { text: '累積過剩需求', bold: true },
  { text: '支撐房貸結構性增長。即使 FY25–26 預測 NOM 將進一步降至 23.4 萬,既有缺口仍將推動租金與房價。' }
]));

children.push(richPara([
  { text: '(3)房價預期', bold: true },
  { text: '直接影響購屋意願與借款規模。CoreLogic(2025)指出 2025 年全國房價上漲 +8.6%,中位數增加約 A$71,400;然 2026 年 4 月房價成長放緩至 +0.3%,且 Sydney 與 Melbourne(CBA 兩大主力市場)月跌 −0.6%。此「冷熱不均」格局意味 CBA 房貸組合面臨重估壓力,但其平均貸款價值比(LVR)約 47% 提供緩衝。' }
]));

children.push(richPara([
  { text: '(4)首購政策', bold: true },
  { text: '為政府主動拉抬之需求面槓桿。2024 年起取消 First Home Guarantee 收入上限、2024 年 12 月推出 Help to Buy(年 10,000 名額,政府最多承擔 40% 股權),擴大可申貸群體(Housing Australia, 2024)。作為市占第一的房貸放款方,CBA 直接受惠。' }
]));

children.push(h2('4.3 供給面驅動因子'));
children.push(bodyPara('供給面則由三股力量主導:'));

children.push(richPara([
  { text: '(1)銀行資金成本', bold: true },
  { text: ' 直接決定 CBA 房貸定價底線。CBA 約 75% 資金來自零售存款,升息期存款戶要求更高存款利率,2024 年起存款定價戰白熱化,擠壓 NIM。批發融資(Wholesale Funding)約占 25%,受國際信用利差影響。' }
]));

children.push(richPara([
  { text: '(2)APRA 監管框架', bold: true },
  { text: '約束供給。' },
  { text: '服務能力緩衝(Serviceability Buffer)', bold: true },
  { text: ' 自 2021 年 11 月起維持 3%,要求借款人證明在利率再加 3% 情境下仍能還款;APRA ' },
  { text: 'Revised Capital Framework', bold: true },
  { text: ' 於 2023 年 1 月對齊全球 Basel III 生效,大行需維持 CET1 最低 10.5%(CBA 目前約 12.0%);APRA 並於 2024 年宣布 2032 年前完全淘汰 AT1 資本工具,進一步強化銀行體質(IBISWorld, 2025)。' }
]));

children.push(richPara([
  { text: '(3)行業技術與商業模式變革', bold: true },
  { text: ' 改變供給結構。Open Banking(CDR)讓 fintech 取得客戶資料降低轉換成本;Macquarie 與非銀行放款方靠數位流程將房貸申辦時間從 30 天壓縮至 1–2 天,直接搶奪 CBA 之傳統客戶。CBA 應對策略為加碼數位投資,自有通路占新貸款 66%(行業均值約 50%)為其護城河。' }
]));

children.push(h2('4.4 行業成本結構與 CBA 規模優勢'));
children.push(richPara([
  { text: '銀行業利潤率 22.3% 雖看似亮眼,卻顯著低於金融保險業整體 43.36%(IBISWorld, 2025)。如圖 7 所示,主因在於銀行業薪資成本占營收 14.1%(整體金融業僅 7.10%,等於 2 倍),反映其勞動密集本質;此外 ' },
  { text: '「Other Costs」高達 59.6%', bold: true },
  { text: ',主要為利息支出與合規成本。對 CBA 而言,21.7% 行業市占帶來的規模經濟可顯著攤平固定 IT 與合規成本,構成中型銀行難以模仿的護城河。' }
]));
children.push(image('fig7_cost_structure.png', 14, 7));
children.push(caption('圖 7:銀行業 K6221A vs. 金融保險業整體成本結構對比 — 資料來源:IBISWorld(2025)'));

children.push(h2('4.5 SWOT 綜合評估'));
children.push(makeTable(
  ['維度', 'CBA 房貸業務'],
  [
    ['Strengths(優勢)', '市占第一(25.4%)、自有通路 66%、NIM 領先、客戶數最大、資本充足'],
    ['Weaknesses(劣勢)', 'ROE 仍低於全球同業(13.5% vs 15–18%)、本土集中、房貸風險集中'],
    ['Opportunities(機會)', '首購政策紅利、再融資需求、綠色金融(CBA 2030 永續貸款目標 A$70 bn、化石燃料貸款僅占 0.2%)、AI 自動化降本'],
    ['Threats(威脅)', 'Macquarie 與 fintech 競爭、RBA 升息壓抑需求、Sydney/Melbourne 房價回落、Open Banking 增加流失率'],
  ],
  [2200, 6872]
));
children.push(caption('表 4:CBA 房貸業務 SWOT 分析(作者整理)'));

// Section 5
children.push(h1('5. 結論與展望(Conclusion and Outlook)'));
children.push(richPara([
  { text: '對 CBA 管理層而言,' },
  { text: '短期(2026)', bold: true },
  { text: ' 面臨「量價拉鋸」:RBA 重啟升息將短期擴大既有房貸利息收入(浮動利率重訂價紅利),但同時壓抑新貸款需求並提升違約風險;Sydney 與 Melbourne 房價回落需密切監控組合 LVR 結構。' },
  { text: '中期(2027–2030)', bold: true },
  { text: ' 行業已進入成熟期(IBISWorld 預測 CAGR +0.3%),爭奪存量市占將取代市場擴張,CBA 須以三軸策略防禦:(一)維持規模優勢與自有通路 66% 比例;(二)加大 AI 與數位投資以壓縮房貸申辦時間,迎戰 Macquarie 與 fintech;(三)深化高品質客群滲透並擴展綠色金融以分散風險。整體而言,CBA 在五力結構中享有領導者護城河,但需在「成長極大化」與「風險紀律」之間維持平衡,以延續其房貸帝國的長期競爭優勢。' }
]));

// References
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1('參考文獻(References)'));

const refs = [
  'Australian Bureau of Statistics. (2025). Overseas migration, 2024-25 financial year. https://www.abs.gov.au/statistics/people/population/overseas-migration/latest-release',
  'Australian Government. (2024). Consumer Data Right (CDR). Treasury. https://treasury.gov.au/consumer-data-right',
  'Australian Prudential Regulation Authority. (2024). Quarterly authorised deposit-taking institution performance statistics — June 2024. https://www.apra.gov.au/quarterly-authorised-deposit-taking-institution-statistics',
  'Australian Prudential Regulation Authority. (2025). Monthly authorised deposit-taking institution statistics — November 2025. https://www.apra.gov.au/monthly-authorised-deposit-taking-institution-statistics',
  'Commonwealth Bank of Australia. (2023). Full year profit announcement: For the full year ended 30 June 2023. https://www.commbank.com.au/content/dam/commbank-assets/investors/docs/results/fy23/CBA-FY23-Profit-Announcement.pdf',
  'Commonwealth Bank of Australia. (2024). Full year profit announcement: For the full year ended 30 June 2024. https://www.commbank.com.au/content/dam/commbank-assets/investors/docs/results/fy24/CBA-FY24-Profit-Announcement.pdf',
  'Commonwealth Bank of Australia. (2025). 2025 annual report. https://www.commbank.com.au/content/dam/commbank-assets/investors/docs/results/fy25/2025-annual-report.pdf',
  'Commonwealth Bank of Australia. (2025). Full year 2025 results profit announcement. https://www.commbank.com.au/content/dam/commbank-assets/investors/docs/results/fy25/full-year-profit-announcement.pdf',
  'Cotality (formerly CoreLogic). (2025). Home Value Index — 2025 annual review. https://www.cotality.com/au/insights',
  'Housing Australia. (2024). First Home Guarantee. https://www.housingaustralia.gov.au/first-home-guarantee',
  'Housing Australia. (2024). Help to Buy scheme. https://www.housingaustralia.gov.au/help-to-buy',
  'IBISWorld. (2025). K6221A — National and regional commercial banks in Australia [Industry report, M. Reilly]. IBISWorld. Retrieved via UTS Library.',
  'McGahan, A. M., & Porter, M. E. (1997). How much does industry matter, really? Strategic Management Journal, 18(S1), 15–30. https://doi.org/10.1002/(SICI)1097-0266(199707)18:1+<15::AID-SMJ916>3.0.CO;2-1',
  'Mortgage & Finance Association of Australia. (2024). MFAA industry intelligence service report. https://www.mfaa.com.au',
  'Porter, M. E. (1980). Competitive strategy: Techniques for analyzing industries and competitors. Free Press.',
  'Reserve Bank of Australia. (2026). Cash rate target — historical data. https://www.rba.gov.au/statistics/cash-rate/',
];

for (const ref of refs) {
  children.push(new Paragraph({
    children: [new TextRun({ text: ref, font: FONT_ENG, size: 22 })],
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: LINE_SPACING, after: 100 },
    indent: { left: 567, hanging: 567 },
  }));
}

// Build document
const doc = new Document({
  creator: 'PoKai Huang',
  title: 'CBA Home Loan Industry Analysis',
  description: '231708 Foundation Studio Assessment Task 1',
  styles: {
    default: { document: { run: { font: FONT, size: SIZE_BODY } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: SIZE_H1, bold: true, font: FONT, color: '04254A' },
        paragraph: { spacing: { before: 360, after: 180, line: LINE_SPACING }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: SIZE_H2, bold: true, font: FONT, color: 'E91E2C' },
        paragraph: { spacing: { before: 240, after: 120, line: LINE_SPACING }, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN, header: 720, footer: 720 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: '231708 Foundation Studio | Assessment Task 1 | CBA Home Loan Industry Analysis',
                                                   font: FONT_ENG, size: 18, color: '888888' })],
          alignment: AlignmentType.RIGHT,
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          children: [
            new TextRun({ text: 'PoKai Huang | ', font: FONT_ENG, size: 18, color: '888888' }),
            new TextRun({ children: [PageNumber.CURRENT], font: FONT_ENG, size: 18, color: '888888' }),
            new TextRun({ text: ' / ', font: FONT_ENG, size: 18, color: '888888' }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT_ENG, size: 18, color: '888888' }),
          ],
          alignment: AlignmentType.CENTER,
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  const outPath = '/sessions/brave-vigilant-gauss/mnt/Foundation Studio/CBA_Report/CBA_Home_Loan_Industry_Analysis.docx';
  fs.writeFileSync(outPath, buffer);
  console.log('Report saved:', outPath);
  console.log('Size:', (buffer.length / 1024).toFixed(1), 'KB');
});
