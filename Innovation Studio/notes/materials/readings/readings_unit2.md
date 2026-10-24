# 單元二 外部連結閱讀筆記(readings_unit2)

> **範圍**:Canvas 單元二(模組 352284)頁面裡所有 `link` 類型的外部連結,共 45 列(第 156 列含 5 個框架首頁,合計 49 個網址)。來源清單 = `notes/raw/inventory_2026-10-24.tsv` 第 134–178 列。
> **章節順序**:照課程頁面順序(#7 → #21)排。inventory 原檔是按字串排序(#10 會排在 #7 前面),所以這裡改用項目序號由小到大,方便對照 `notes/02_單元二_數據分析與機器學習技術概述.md` 的「## N.」。
> **抓取日期**:2026-10-24。方法:WebFetch;被擋的(help.openai.com、Medium、百度百科、Tableau 回 403)改用內建瀏覽器唯讀開頁;nbviewer 回 429 的兩本 Gemini notebook 改抓 GitHub 官方原檔(jsDelivr 鏡像)閱讀。
> **不在本筆記範圍**:inventory 第 53 列「VIDEO: Bagging and random forests - Bloomberg」(類型 `link-video`,屬影片組)。
> **著作權**:第三方文章一律用自己的話摘要,不轉貼原文。

---

## 先看這裡:AT2 / AT3 怎麼用這些連結(1 分鐘版)

| 你要做的事 | 直接去看 | 為什麼 |
|---|---|---|
| AT2「數據」章節找公開資料集 | #7 NYC 車禍資料集 | 227 萬筆、29 欄、有時間＋經緯度＋傷亡數,探索性分析好做;⚠️ 2026/6 起自動更新暫停 |
| AT2/AT3 選圖表類型 | #8 from Data to Viz | 依資料型態(數值/類別/時間/地圖/網路)查該用哪種圖,每種圖附「常見錯誤」 |
| AT2「分析系統架構」畫圖 | #10 sequencediagram.org、DFD 兩篇、ER 圖 | 架構圖、資料流程圖、資料表關聯圖的畫法與規則 |
| AT3 做互動式介面/圖表 | #11 Plotly、Tableau(Desktop 已免費) | AT3 50 分那項 HD 要「互動式使用者介面」 |
| AT2「分析方法」寫前沿 AI | #21 提示工程、微調(LoRA)、RAG | HD 要談 LLM/深度學習＋選擇標準 |
| AT3 把 LLM 做成「可行動的功能」 | #21 cookbook:**File Search RAG**、**資料萃取 ELT**、**Embedding 分類**、**結構化 JSON 輸出(行銷案)** | 這 4 個最適合當 AT3 系統裡的一個功能模組(見 #21 末尾對照表) |
| AT2「實驗與評估」要有基準方法 | #21 File Search RAG 的檢索評估(Recall@5、MRR、MAP)、#20 TF 時間序列(用 baseline 對照) | 示範「先定 baseline 再比較模型」 |
| 計程車案例(單元一/二同一案例) | #11 NYC Taxi 一天、#12 shapefile | 同一套紐約計程車資料的視覺化範例、區域資料的檔案格式限制 |

⚠️ **課程頁本身的問題(建議 Zoom 時順口確認)**:
1. #21「檢索增強生成 RAG」段落說「請參閱相關教程」,但連結指向的是**提示工程最佳實踐**那篇(跟上一段同一個網址),那篇完全沒講 RAG。真正的 RAG 範例請看 #21 cookbook 的 File Search 與 Parse PDF 兩本。
2. #20「深度學習庫」的 TensorFlow 連到 `tensorflowcn.cn`,頁面沒寫是不是官方站,版本停在 v2.16.1;同頁時間序列教程用的是 Google 官方的 `tensorflow.google.cn`。要查 TensorFlow 文件建議用官方網域。
3. #20 列的 MXNet **已退役**(Apache 官網明寫 retired,移入 Attic),AT3 不要選它。
4. #21「Generation for Story Writing」連到的是 SourceForge 的**非官方鏡像首頁**,不是那本 notebook 本身;本筆記另外讀了 GitHub 官方 notebook 補上內容。

---

## #7 2.5 數據可視化(5 個連結)

### 30% 的大腦皮層 — Discover Magazine
- 網址:https://www.discovermagazine.com/mind/the-vision-thing-mainly-in-the-brain ｜狀態:已讀
- 作者 Denise Grady,**1993 年 6 月**《Discover》雜誌科普文章。
- 重點:
  - 負責視覺處理的神經元約佔大腦皮質 30%;相比之下觸覺約 8%、聽覺約 3%。
  - 心理學家 Stuart Anstis 戴了 3 天會把明暗與顏色反轉的護目鏡,認臉、看食物、判斷深度都變困難,而且幾乎適應不了。
  - 「看見」不是被動接收,而是大腦根據內建假設(例如光從上方來、陰影比較暗)主動建構;假設被打破就產生錯覺。
  - 動作、顏色、形狀走不同的平行處理路徑(學界對到底有幾條路徑沒有共識)。
  - 大腦會自動「補洞」(例如盲點);有些皮質受損的病人能對視覺刺激做出反應,自己卻不覺得有看到(盲視)。
- 課程為什麼放:佐證「人是視覺動物,所以要做視覺化」。
- 對作業:報告若要引用「30%」這個數字,這是 1993 年的科普文章,建議另找神經科學原始文獻再引,不然評分者可能覺得來源弱。

### Driven by Data(作品集網站)
- 網址:https://driven-by-data.net/ ｜狀態:已讀
- Gregor Aisch 的資料新聞作品集(現任 DIE ZEIT,曾任《紐約時報》圖表編輯,Datawrapper 共同創辦人)。收錄 2009–2026 年作品,依年份與主題(選舉、經濟、科學、運動…)分類,2026 年仍持續更新。
- 課程為什麼放:當作「說明性視覺化(explanatory visualisation)」的優秀範例庫。
- 對作業:AT2 簡報/AT3 展示要對非技術聽眾講故事,可以來這裡找「一張圖講一件事」的版面靈感。

### 運動員出生國家的堆疊面積圖
- 網址:https://driven-by-data.net/2017/12/29/sports-i18n ｜狀態:部分(作品集頁只有作品簡介)
- 這頁只是作品集條目:2017-12-29 刊在《紐約時報》,Gregor Aisch 與 Kevin Quealy、Rory Smith 合作,標題大意是「英超、NBA 等聯賽球員來自哪裡,15 張圖」;資料是爬各運動資料庫網站的球員名單與出生地,圖型標籤為堆疊面積圖(area chart)。
- 課程頁描述的「葡萄牙超級聯賽 1960 年多數本國球員 → 2015 年超過一半來自歐洲其他國家、南美、非洲」這些細節**不在這頁**,在《紐約時報》原文(付費牆,本次未抓)。
- 課程為什麼放:示範用堆疊面積圖呈現「組成比例隨時間變化」。

### NYC Open Data 視覺化工具
- 網址:https://data.cityofnewyork.us/d/h9gi-nx95/visualization ｜狀態:已讀(看得到的部分)
- 打開是 Socrata 平台的「Configure Visualization」視窗:左邊 Data Selection 有「Dimension(維度)」「Measure(度量)」兩個欄位,上方一排圖表類型圖示。一進去會跳「要不要登入以儲存視覺化」的提示,**不登入也能繼續用**,只是不能存。
- 課程練習:Dimension 填 `CRASH DATE`、Measure 填 `NUMBER OF PERSONS INJURED`,系統應推薦時間線圖(Timeline Chart),看受傷人數隨時間的變化。
- 課程為什麼放:讓學生不寫程式就體驗「探索性視覺化(exploratory visualisation)」。

### 紐約市機動車碰撞資料集(Motor Vehicle Collisions – Crashes)
- 網址:https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95 ｜狀態:已讀(頁面＋公開 metadata API)
- **規模**:約 **227 萬列(2,269,187)、29 欄**;每一列 = 一起警方登錄的車禍,唯一鍵 `COLLISION_ID`。
- **提供者**:紐約市警察局(NYPD);分類 Public Safety;2014-04-29 建立。
- **更新**:標示每日更新,但頁面公告自動更新流程**暫停中**(資料最後更新 2026-06-16,說預計 8 月修好,截至 2026-10-24 頁面仍掛著這則公告)。
- **欄位(29)**:CRASH DATE、CRASH TIME、BOROUGH、ZIP CODE、LATITUDE、LONGITUDE、LOCATION、ON / CROSS / OFF STREET NAME、受傷/死亡人數(總人數、行人、自行車、機車騎士各一組,共 8 欄)、CONTRIBUTING FACTOR VEHICLE 1–5(肇事因素)、VEHICLE TYPE CODE 1–5(車種)、COLLISION_ID。另附資料字典 Excel。
- **資料限制**:只收警方 MV-104AN 表單有登錄的車禍(有人受傷/死亡或損失 ≥ 1,000 美元);資料屬初步、表單修改後會變動;官方建議要最準確的死亡統計看 NYPD 或 Vision Zero View。
- **授權**:頁面與 metadata **沒有列出授權條款**;NYC Open Data 網站另有使用條款(Terms of Use),本次未逐條核對。
- 對作業:是 AT2 很順手的候選公開資料(時間序列＋地理＋類別欄位都有,可做趨勢、熱點、肇因分析);缺點是更新暫停,報告「數據與資源」要寫明資料截止日。

---

## #8 2.6 圖形與圖表(1 個連結)

### from Data to Viz
- 網址:https://www.data-to-viz.com/ ｜狀態:已讀
- 重點:
  - 用**決策樹**幫你選圖:先選資料型態 —— 數值(1 個/2 個/3 個/多個變數)、類別、數值＋類別、地圖、網路(節點與連線)、時間序列 —— 再一路點到建議的圖型。
  - 每種圖的頁面有:用途說明、「常見錯誤(Common Mistakes)」、R / Python / D3.js(部分還有 React)範例程式碼連結。
  - 另有「Caveats(陷阱)」專區:Y 軸截斷、義大利麵圖(線太多)、圓餅圖、直方圖組距、箱型圖藏資訊、重疊過度(overplotting)、彩虹配色等。
  - 「Data Story」區有約 20 種資料集的完整分析示範(用 R)。
  - 作者 Yan Holtz(資料分析師)與 Conor Healy(設計師);網站免費瀏覽,實體海報要付費。
- 課程為什麼放:配合「選擇合適的可視化方式」——圖型取決於問題、變數型態與變數數量。
- 對作業:AT3 評分有「視覺化」項目;每張圖放進報告前,可以用它的 Caveats 清單自我檢查一次。

---

## #10 2.8 圖示(8 個連結)

### sequencediagram.org(工具)
- 網址:http://sequencediagram.org/ ｜狀態:已讀
- 一行:用**文字語法**畫 UML 時序圖(sequence diagram)的線上工具;解析與繪圖都在瀏覽器端完成、可離線用;可匯出 SVG(內嵌原始文字)/PNG,可存到本機、Google Drive、OneDrive 或產生分享網址。網頁版沒標價(有 Patreon 贊助、企業內部部署版另有授權),程式碼非開源。**適合 AT2「分析系統架構」畫「使用者 → 前端 → API → 模型 → 資料庫」的互動順序。**

### 在流程圖內使用一致設計元素的重要性 — Yonyx
- 網址:https://corp.yonyx.com/customer-service/importance-using-consistent-design-elements-within-flowchart/ ｜狀態:已讀
- 重點:
  - 同一種意義用同一種形狀,同類形狀(例如決策菱形)大小一致。
  - 先定一套配色並貫徹全圖;起點與終點用相同顏色(作者不建議起點綠、終點紅);人工輸入步驟統一一種顏色。
  - 版面由左到右、子流程連續、步驟對齊水平線,減少眼睛來回跳。
  - 連接線:一般步驟用直線箭頭;決策後的路徑可用不同顏色;虛線表示備援或平行流程;折線箭頭省版面。
  - 一致性的好處:使用者讀得順、日後改版能延續舊設計、給審閱者好印象。
  - 出版者 Yonyx 是做客服「互動式決策樹」的公司,文末有試用廣告。
- 課程為什麼放:呼應頁面「優秀圖示的提示 → 一致性」。

### 流程圖的定義 — TechTerms(簡中)
- 網址:https://techterms.com/zh/definition/flowchart ｜狀態:已讀
- 很短的名詞解釋:流程圖把一個程序拆成步驟、依序由頭走到尾;長方形 = 步驟、菱形 = 決策、箭頭 = 方向;可用於營運規劃、故障排除步驟、演算法設計;手畫或用 SmartDraw、Visio、OmniGraffle 都行。
- 課程為什麼放:給完全沒畫過流程圖的同學一個最基本定義。

### 流程圖(Flowchart)— 百度百科
- 網址:https://baike.baidu.com/item/%E6%B5%81%E7%A8%8B%E5%9B%BE/206961 ｜狀態:已讀(WebFetch 403,改用瀏覽器開啟成功)
- 重點:
  - 定義:用特定圖形符號加說明來表示演算法/流程的圖,又叫「框圖」;中國國家標準 GB/T 1526—1989 規定了常用符號。
  - 五種類型:數據流程圖、程序流程圖(程式的操作順序)、系統流程圖(控制＋資料流)、程序網絡圖(程式啟動路徑與資料互動)、系統資源圖。
  - 基本結構:順序、條件(選擇)、循環、分支。
  - 企業用途:說明生產工序或管理流程,用「是/否」分支表示決策;也是品質管理(例如 QC 小組)常用工具。
  - 附 Word 2010 畫流程圖步驟(要先插入「繪圖畫布」,連接線才接得起來)。
  - 優點:直觀、不易有歧義、容易轉成程式;缺點:佔版面、流程線太自由會讓程式難讀難改。

### 什麼是數據流圖? — Visual Paradigm(簡中)
- 網址:https://www.visual-paradigm.com/cn/guide/data-flow-diagram/what-is-data-flow-diagram/ ｜狀態:已讀
- 重點:
  - DFD(Data Flow Diagram)畫的是「資料」在系統裡怎麼流:輸入 → 處理 → 儲存 → 輸出。
  - 4 個元素:**處理(process)**(圓角矩形,動詞＋名詞命名,如「計算佣金」)、**資料流(data flow)**(有標籤的箭頭)、**資料儲存(data store)**、**外部實體(external entity)**(只提供/接收資料,不處理)。
  - 分層:Context diagram(第 0 層,整個系統只畫 1 個處理、不畫資料儲存)→ Level 1 → Level 2 逐層拆。
  - 規則:資料不能自己變形,一定要經過處理;實體↔實體、實體↔儲存、儲存↔儲存不能直接連;上下層輸入輸出要平衡(balancing)。
  - 常見錯誤:黑洞(只有輸入沒輸出)、奇蹟(只有輸出沒輸入)、灰洞(輸出多於輸入能產生的)。每張下層圖處理數別超過約 9 個(7±2 原則)。
  - 邏輯 DFD(講業務功能)vs 實體 DFD(講怎麼實作,含硬體、檔案、人工步驟);範例是超市結帳。
  - 頁面夾帶 Visual Paradigm 工具廣告。
- 對作業:**AT2「分析系統架構」最適合用 DFD 畫**(資料從哪來、經過哪些處理、存在哪、輸出給誰)。

### 數據流圖(Data Flow Diagram)— 百度百科
- 網址:https://baike.baidu.com/item/%E6%95%B0%E6%8D%AE%E6%B5%81%E5%9B%BE/4136477 ｜狀態:已讀(WebFetch 403,改用瀏覽器)
- 重點(與上一篇互補的部分):
  - 強調 DFD **不是**流程圖:資料流不是控制流,不畫執行順序、不畫時間、不畫條件。
  - 歷史:1970 年代 Larry Constantine 提出;有 Yourdon/DeMarco 與 Gane & Sarson 兩套符號。
  - 兩種典型結構:變換型(輸入 → 主處理 → 輸出,呈線性)、事務型(一束資料流平行流入/流出)。
  - 分層:頂層圖(1 個加工代表整個系統)→ 中層 → 底層(不能再拆的「原子加工」);子圖從 0 開始編號。
  - 單張圖原則:輸出流不能和輸入流同名、資料守恆、每個加工都要有進有出、外部實體之間不畫資料流。
  - 畫法三步:先確定系統輸入輸出 → 由外向內畫頂層 → 自頂向下逐層分解。範例:機票預訂系統、企業銷售管理系統。

### 實體關係圖(Entity Relationship Diagram)— BeginnersBook
- 網址:https://beginnersbook.com/2015/04/e-r-model-in-dbms ｜狀態:已讀
- 重點:
  - ER 圖畫資料庫的邏輯結構:實體(長方形)、屬性(橢圓)、關係(菱形)。
  - 弱實體(weak entity)靠別的實體才能識別(例:銀行帳戶依附銀行),畫雙框長方形。
  - 屬性 4 種:主鍵(底線)、複合(地址 = 郵遞區號＋州＋國家)、多值(電話,雙橢圓)、衍生(年齡由生日算出,虛線橢圓)。
  - 基數:一對一、一對多、多對一、多對多(例:人↔護照、客戶↔訂單、學生↔學院、學生↔專案)。
  - 參與:全部參與(雙線)vs 部分參與(單線)。範例:學生(多)— 就讀 — 學院(一)。
- 對作業:AT3「數據介面」若要建資料庫(例如把萃取結果存成表),報告可以附一張 ER 圖說明資料表關係。

### 設計師的色彩理論(三):建立自己的配色 — Smashing Magazine
- 網址:https://www.smashingmagazine.com/2010/02/color-theory-for-designer-part-3-creating-your-own-color-palettes ｜狀態:已讀(第一次 DNS 失敗,重試成功)
- 作者 Cameron Chapman,原刊 2010 年 2 月,2021 年更新。
- 重點:
  - 傳統配色:單色(同一色相的深淺)、類似色(色環相鄰 3 色)、互補色(對面 2 色,並排會「震動」,中間要留白或過渡色)、分裂互補、三角(triadic)、雙互補(tetradic,最難駕馭)、自訂。
  - 不要只用純色:加入 tint/shade/tone(加白/加黑/加灰)把一個色相擴成一整組可用的顏色。
  - 一組變化色＋**一個亮色當強調色(accent)**;中性色(灰、黑、白、米色、棕)負責背景與文字。冷灰顯現代、暖灰與棕顯傳統。
  - 可以從照片取色(Adobe Capture、Coolors、Paletton 等工具);整體控制在約 5 個顏色。
- 對作業:AT3 介面與圖表配色可直接套「中性色底＋1 個強調色標重點」;也符合 2.8 頁「技術報告用穩重配色、避免粉彩與刺眼顏色」的提醒。

---

## #11 2.9 什麼是良好的數據可視化(8 個連結)

> 工具首頁一行版(授權資訊頁面沒寫的,標「一般知識」)。

| 工具 | 是什麼 | 免費? | 什麼時候用 |
|---|---|---|---|
| **D3.js** https://d3js.org/ | JavaScript 低階視覺化函式庫(頁面顯示 v7.9.0),把資料綁到網頁元素,可做任何客製圖(力導向圖、Sankey、地圖…) | 開源免費(ISC 授權,頁面有寫) | 要做高度客製的網頁互動圖、且組裡有前端能力時;只想快速出圖,頁面自己也推薦改用 Observable Plot |
| **Gephi** https://gephi.org/ | 網路/關係圖的視覺分析軟體,內建社群偵測、中心性、ForceAtlas2 排版;另有瀏覽器版 Gephi Lite | 開源免費(GPL) | 資料是「節點＋連線」時(社群網路、共現關係、交易網路) |
| **Matplotlib** https://matplotlib.org/ | Python 最基礎的繪圖庫(頁面顯示 3.11.0,2026-06),靜態/動畫/互動圖都能做 | 開源免費(BSD 相容授權,一般知識) | 報告用的靜態圖、所有 Python 繪圖的底層 |
| **Seaborn** https://seaborn.pydata.org | 建在 Matplotlib 上的統計圖表庫(頁面顯示 0.13.2),一行畫出分布、類別、迴歸、多圖格 | 開源免費(BSD,一般知識) | EDA(探索性資料分析)快速出漂亮統計圖 |
| **Plotly Python** https://plotly.com/python | Python 互動圖表庫,縮放/滑桿/下拉選單/動畫/3D/地圖 | plotly.py 免費開源(頁面寫 free and open source;MIT 為一般知識);Plotly Studio、Plotly Cloud、Dash Enterprise 付費 | **AT3 互動式介面首選之一**(可搭 Dash 或 Streamlit 做網頁) |
| **Tableau** https://www.tableau.com/ | Salesforce 旗下商業 BI 平台;2026 年主打「agentic analytics」與 AI 寫分析(Tableau Studio、Tableau Next) | 商業軟體;**首頁寫 Tableau Desktop「now free」**,另有 Tableau Public(公開分享)與免費試用 | 不寫程式快速做儀表板;AT3 若要互動 UI 但組員程式弱,可考慮 |

### NYC Taxis: A Day in the Life — Chris Whong
- 網址:https://chriswhong.github.io/nyctaxi/ ｜狀態:已讀
- 重點:
  - 隨機挑一台紐約黃色計程車,在深色地圖上用動畫重播它 2013 年某一天 24 小時的行程。
  - 資料:Chris Whong 透過資訊公開請求(FOIL)向紐約計程車與禮車管理局(TLC)取得 2013 年約 1.7 億趟行程,從中隨機抽 30 個「車-日」。
  - 介面:Begin 按鈕、播放速度滑桿、圖例(載客/空車、上下車點、路線)、「再載一台」按鈕,旁邊即時累計車資、附加費、小費、過路費、總收入、乘客數。
  - 原始資料只有上下車點,路線是用 Google Directions API 推估的;小費只記到刷卡付款的部分(作者在 Asterisks 頁誠實列出限制)。
  - 技術:MapLibre GL JS(早期版本用 D3＋Leaflet)、OpenFreeMap 底圖;程式碼在 GitHub,作者有寫兩篇製作過程文章。
- 課程為什麼放:同一套紐約計程車資料正是單元一/二「乘客需求分析」案例的資料來源類型,示範「用一台車的故事讓龐大資料變得有感」。
- 對作業:AT3 展示可借這招 —— 用一個具體個案(一位使用者、一天)帶出系統價值;也示範了「誠實標註資料限制」的寫法。

### The 30+ Best Data Visualizations of 2026 — Visme 部落格
- 網址:https://visme.co/blog/best-data-visualizations/ ｜狀態:已讀
- 2026-02-19 更新,Anna Glivinska 撰文,共 33 個作品(編號 1–34,跳過 #5)。
- 重點:
  - 題材涵蓋太空(NASA 小行星即時 3D)、選舉(六角格地圖)、人口(全球出生數、各國人口排名 Sankey 流向)、能源(資料中心周邊電價地圖)、調查報導(暗底 Sankey 追油輪轉運)、音樂趨勢(The Pudding 的情歌消長)等。
  - 作者歸納的共通點:簡潔清楚、配色有系統(冷到暖色階、高對比底色)、互動(篩選、時間軸、縮放)、有故事與脈絡(資料來源、說明)、地圖與流向圖適合地理/移動資料、藝術化風格吸睛但可能犧牲精確度。
  - 文章穿插大量 Visme 工具廣告;文末免責聲明日期寫 2024、跟文章日期對不上,細節引用前要再查。
- 課程為什麼放:擴展學生對「好視覺化」的眼界。
- 對作業:找 AT3 展示的視覺風格靈感用;要評「好不好」仍以 2.9 頁的 ACCENT 原則為準。

---

## #12 案例研究:乘客需求(1 個連結)

### Shapefile 輸出的地理處理注意事項 — Esri ArcGIS Pro 文件(簡中)
- 網址:https://doc.esri.com/zh-cn/arcgis-pro/latest/tool-reference/appendices/geoprocessing-considerations-for-shapefile-output.html ｜狀態:已讀
- 重點:
  - Shapefile 是一組同名、放在同一資料夾的檔案:必備 `.shp`(幾何)、`.shx`(索引)、`.dbf`(屬性表);常見選配 `.prj`(座標系統)、`.sbn/.sbx`(空間索引)、`.xml`(metadata)。
  - 大小限制:每個組成檔最多 2 GB;比 geodatabase 多佔 3–5 倍空間;大資料空間查詢比較慢。
  - 欄位限制:欄名最多 10 個字元;最多 255 個欄位;文字欄寬 254 且按**位元組**算(中文一個字約 3 bytes,容易被截斷或亂碼)。
  - 日期欄**只存日期、不存時間** —— 做時間分析(例如按小時看需求)是大問題。
  - 不支援 null:轉檔時會被換成代替值(0、空白、極大負數),之後分不出真值和缺值。
  - 不支援拓撲、子類型、屬性網域等進階功能;曲線會被轉成折線。
  - 建議:只拿來跟非 Esri 軟體交換資料;中間與輸出資料優先用 file geodatabase。
- 課程為什麼放:計程車區域(Taxi Zone)資料就是 shapefile,案例要做「點落在多邊形內(Point-in-Polygon)」疊加分析。
- 對作業:若 AT2/AT3 用到地理區域資料,「數據預處理」可提:用 GeoPandas 讀 shapefile 後轉成 GeoJSON/GeoParquet,避免欄名截斷、時間遺失、null 被取代的問題。

---

## #17 2.12 決策樹(2 個連結)

### 圖解機器學習 — R2D3.us(簡中版)
- 網址:https://r2d3.us/%E5%9B%BE%E8%A7%A3%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/ ｜狀態:已讀
- R2D3(Stephanie Yee、Tony Chu)的經典捲動式互動教學第一部分,中文由志工翻譯。
- 重點(照教學順序):
  1. 任務:根據房屋資料判斷房子在舊金山還是紐約 —— 這是**分類(classification)**。資料有 7 個特徵。
  2. 先看海拔:舊金山多丘陵,海拔高於約 73 公尺(約 240 英尺)的房子猜舊金山。
  3. 加第二個特徵「每平方單位價格」:低海拔裡,紐約房價明顯更貴。
  4. 決策樹用一連串 if-else 判斷;每個判斷是一個分岔(fork),在「分割點(split point)」把資料切兩邊,最好的切法讓兩邊各自越純越好;任何切法都要在偽陰性與偽陽性之間取捨。
  5. **遞迴(recursion)**:在每個分支上重複找最佳特徵與分割點;樹長越深,訓練準確率越高(多一層約 84%,再多幾層約 96%,一直切可到 100%)。
  6. 拿沒見過的**測試資料**驗證,準確率掉下來(轉載版寫 89.7%)—— 這就是**過擬合(overfitting)**:樹把雜訊也學進去了。
- 課程為什麼放:用視覺動畫直觀解釋決策樹怎麼長、為什麼會過擬合。
- 對作業:AT2「實驗與評估方法」要寫清楚訓練/測試切分,這篇是最好懂的理由說明。

### 機器學習可視化演示 — 騰訊雲開發者社群
- 網址:https://cloud.tencent.com/developer/article/1072706 ｜狀態:已讀(第一次 DNS 失敗,重試成功)
- 新智元 2018-03-26 轉載(原刊 2016-11-03),是上一篇 R2D3 第一部分的中文改寫版,內容幾乎相同。
- 補充的具體數字:海拔分割約 240 英尺、每平方英尺價格分割 1,776 美元、低海拔分支再以 1,061 美元/平方英尺切、高海拔分支以房價 514,500 美元切;訓練 100% vs 測試 89.7%。
- 課程為什麼放:R2D3 的備用中文版本(R2D3 原站在中國可能不好連)。

---

## #18 2.13 集成(1 個連結)

### Bagging and Boosting — Medium(Posam Sai Teja)
- 網址:https://medium.com/@saitejaposam9/bagging-and-boosting-2b6cd4a6bda1 ｜狀態:已讀(WebFetch 403,改用瀏覽器)
- 2019-08-07,2 分鐘短文。
- 重點:
  - 同一份資料訓練的多個模型容易給出一樣的答案,所以要用**自助抽樣(bootstrapping)**:有放回地抽出跟原資料一樣大的子集。
  - **Bagging(Bootstrap Aggregating)**:每個子集各訓練一個弱模型 → 模型之間**平行、互相獨立** → 最後合併(投票/平均)。代表:Bagging meta-estimator、隨機森林(Random Forest)。
  - **Boosting**:**依序**訓練,後一個模型專門修正前一個的錯誤;一開始所有樣本權重相同,預測錯的樣本之後權重加大。代表:AdaBoost、GBM、XGBoost、LightGBM、CatBoost。
  - 提到 Freund 與 Schapire 因 AdaBoost 在 2004 年獲 ACM Paris Kanellakis 獎。
  - 文章的 boosting 步驟只寫到第 5 步(算誤差)就結束,不完整;要深入請另找教材。
- 課程為什麼放:頁面那張「Bagging(parallel)vs Boosting(sequential)」示意圖就是改編自這篇。
- 對作業:結構化/表格資料的預測任務,AT2 可把 XGBoost/LightGBM 列為強基準(baseline),再和深度學習或 LLM 方法比較。

---

## #20 2.15 深度學習(3 列,共 7 個網址)

### 60 分鐘快速入門 PyTorch — 訓練分類器(騰訊雲)
- 網址:https://cloud.tencent.com/developer/article/1631768 ｜狀態:已讀(第一次 DNS 失敗,重試成功)
- 作者 kbsc13(專欄「AI 算法筆記」),2020-05,翻譯自 PyTorch 官方教學「Deep Learning with PyTorch: A 60 Minute Blitz」第 4 節。
- 重點:
  1. 用 torchvision 載入 **CIFAR-10**(10 類、32×32 彩色圖),轉 tensor 並把像素從 [0,1] 正規化到 [-1,1];batch size 4。
  2. 定義 CNN:2 個卷積層＋最大池化,接 3 個全連接層(第一層輸入 3 通道 = RGB)。
  3. 損失函數交叉熵(CrossEntropy)、優化器 SGD(lr = 0.001、momentum = 0.9)。
  4. 訓練 2 個 epoch,loss 從約 2.23 降到約 1.31(作者機器約 77 秒)。
  5. 測試 1 萬張圖:整體準確率 **55%**(官方約 51%,作者說隨初始化不同會有差);各類別最好卡車 72%、最差貓 33%。
  6. 示範移到 GPU,但網路太小,作者的筆電 GPU 沒變快。
- 課程為什麼放:最短路徑體驗「載資料 → 定義網路 → 訓練迴圈 → 評估」的完整深度學習流程。
- 對作業:若 AT3 有影像分類需求,這是最小可行骨架;報告要像它一樣附「各類別準確率」,不要只報總準確率。

### 時間序列預測 — TensorFlow 官方中文教程
- 網址:https://tensorflow.google.cn/tutorials/structured_data/time_series?hl=zh-cn ｜狀態:已讀
- 重點:
  - 資料:德國馬克斯普朗克生物地球化學研究所的 **Jena 氣候資料**,14 個特徵(氣溫、氣壓、濕度…),原本每 10 分鐘一筆,教程取 2009–2016 年並降採樣成每小時。
  - 前處理:把 -9999 的錯誤風速改 0;風速＋風向轉成 x/y 向量;時間轉成每日/每年的 sin/cos 週期訊號(用 FFT 確認日、年週期);依時間順序切 70/20/10(**不打亂**);只用訓練集的平均與標準差做標準化。
  - `WindowGenerator` 類別:用輸入寬度、標籤寬度、位移量切出(輸入, 標籤)視窗並轉成 `tf.data.Dataset`。
  - 比較的模型:baseline(直接用目前值當預測)、線性、Dense、多步 Dense、CNN、LSTM;多輸出版本加殘差 LSTM;多步(預測未來 24 小時)版本加自迴歸 LSTM。指標 MAE。
  - 結果:單步 LSTM 最好(MAE 0.053,baseline 0.085);預測 24 小時時 CNN、Dense、LSTM 差不多(約 0.274–0.278),自迴歸 LSTM 反而較差;作者坦言換成複雜模型只多賺幾個百分點甚至沒有。
- 課程為什麼放:RNN/CNN 在序列資料的實作範例。
- 對作業:**跟計程車需求預測案例完全同型**(按小時預測需求);AT2「實驗設計」可照抄它的做法 —— 時間順序切分、先定 baseline、再比 Dense/CNN/LSTM,並誠實報告「複雜模型不一定值得」。

### 深度學習框架首頁(5 個,一行版)
- 狀態:5 個都已讀(Keras、JAX 第一次 DNS 失敗,重試成功;jax.readthedocs.io 會轉址到 docs.jax.dev)

| 框架 | 一行 |
|---|---|
| **PyTorch** https://pytorch.org/ | Linux Foundation 旗下 PyTorch Foundation 管理的深度學習框架,免費開源(BSD,一般知識);最新穩定版需 Python 3.10+;學界與業界最主流,**AT3 自己訓練模型的預設選擇**。 |
| **TensorFlow** https://tensorflowcn.cn/ | Google 的端到端機器學習平台(含 Keras、LiteRT/TF Lite 行動端、TF.js 瀏覽器端、TFX 生產管線);這個中文站顯示 v2.16.1,**沒寫是否官方** → 查文件建議用 tensorflow.google.cn 或 tensorflow.org。適合要部署到手機/瀏覽器時。 |
| **Keras** https://keras.io/ | 高階深度學習 API,Keras 3 可切換 JAX/TensorFlow/PyTorch 三種後端;KerasHub 提供預訓練模型(含 Gemma、Qwen 等);免費開源(Apache 2.0,一般知識);想用最少程式碼快速建模時用。 |
| **MXNet** https://mxnet.apache.org/ | Apache 的深度學習框架(最後版本 1.9.1,Apache 2.0);**官網明寫專案已退役(retired)** → 只當歷史知識,**不要選來做作業**。 |
| **JAX** https://jax.readthedocs.io/ | NumPy 風格的加速運算庫,核心是可組合的轉換:`jit` 編譯、`grad` 自動微分、`vmap` 批次化、sharding 平行化;同一份程式跑 CPU/GPU/TPU;生態有 Flax、Optax;免費開源(Google 開發、Apache 2.0,一般知識);偏研究/大規模訓練,課程作業一般用不到。 |

---

## #21 2.16 大語言模型(16 個連結)

### 提示工程最佳實踐 — OpenAI Help Center
- 網址:https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api ｜狀態:已讀(WebFetch 403,改用瀏覽器;頁面顯示 4 天前更新)
- 9 條經驗法則(每條原文都有「較差 vs 較好」對照):
  1. 用最新、最強的模型(新模型比較好下提示;推理模型與 GPT 模型下提示的方式有差)。
  2. 指令放最前面,用 `###` 或 `"""` 把指令和內容隔開。
  3. 具體寫出情境、目標、長度、格式、風格。
  4. 用範例「示範」想要的輸出格式(方便程式解析)。
  5. 先 zero-shot,不行再 few-shot(給幾個例子),都不行才微調(fine-tune)。
  6. 少用模糊形容(「短一點」→ 改成「3 到 5 句」)。
  7. 不要只說「不要做什麼」,要說「改做什麼」(例:客服不要問帳密 → 改成「遇到要帳密的情況,引導使用者看說明頁」)。
  8. 寫程式時用「引導字」(例如先寫 `import` 讓模型接著寫 Python,`SELECT` 接 SQL)。
  9. 可用平台的「Generate Anything」功能自動產生提示。
- 參數:最常調的是 model 和 temperature;**資料萃取、事實問答這類任務 temperature 設 0 最好**;max_completion_tokens 是硬上限不是長度控制;stop 是停止序列。
- 課程為什麼放:提示工程段落的延伸閱讀。⚠️ 課程頁 RAG 段落也連到這篇,但這篇沒有 RAG 內容(見文首)。
- 對作業:AT3 報告「技術創新」可以寫出你們的提示設計原則(分隔符、格式範例、temperature 0),並附提示版本比較。

### LoRA 微調技術的應用與優化 — 騰訊雲
- 網址:https://cloud.tencent.com/developer/article/2672597 ｜狀態:已讀(第一次 DNS 失敗,重試成功)
- 作者索旭東,2026-05(專欄「具身小站」,偏機器人應用)。
- 重點:
  - LoRA(Low-Rank Adaptation,微軟 2021)屬參數高效微調(PEFT):凍結原模型,在層裡插入兩個小矩陣 A、B,只訓練它們,訓練完把 B×A 併回原權重 → 推論速度不變。
  - 參數量從 d×k 降到 r×(d+k):例如 1000×1000 矩陣、r = 2,只要訓練約 4,000 個參數(約 0.4%)。
  - 跟全量微調比:可訓練參數 0.1–5%;7B 模型約需 27 GB GPU 記憶體(VRAM),全量微調要 60 GB 以上;存檔只要幾 MB;效果約達全量的 95–97%;比較不會「災難性遺忘」;不同任務的 LoRA 可以像外掛一樣抽換。
  - 變體:QLoRA(配 4-bit 量化,最省 GPU 記憶體)、AdaLoRA(依重要性分配 rank)、DoRA(拆成大小與方向)。
  - 調參建議:r 從 8 或 16 開始(複雜任務 32);alpha ≈ 2r;學習率從 2e-4 起,在 1e-5 到 5e-4 之間找;先只掛 q、v 投影層,不夠再加 k、o、MLP;小資料集 dropout 0.1–0.2。
  - 診斷:訓練與驗證 loss 都高 → 欠擬合(加大 r);訓練低驗證高 → 過擬合(降 r、加 dropout、補資料);loss 震盪 → 降學習率。
- 課程為什麼放:說明「微調很貴 → 用 LoRA 省成本」。

### 大模型微調實戰:從原理到落地的完整指南 — 火山引擎開發者社群
- 網址:https://developer.volcengine.com/articles/7605549043544965158 ｜狀態:已讀
- 作者「小劉的大模型筆記」,頁面無日期;**文中有一段標明是「軟廣植入」**,推銷 LLaMA-Factory Online 低程式碼微調平台。
- 重點:
  - 通用模型在垂直領域(電商、教育、法律)常不夠好 → 用領域資料微調。
  - 全量微調貴且會遺忘;LoRA 只訓練插入的小矩陣,消費級 GPU 就能跑,權重檔只有幾十 MB。
  - 資料格式:JSON,含 `instruction` 與 `output`;入門約 50–200 筆高品質樣本即可;要檢查亂碼與重複。
  - 建議設定:LoRA rank 8 或 16、學習率 1e-4 到 1e-5、3–5 個 epoch,看 loss 曲線平穩下降。
  - 評估:主觀(拿 10–20 題比較微調前後的相關性、正確性、風格)＋客觀(困惑度 perplexity、標註任務準確率);過擬合就加資料、減 epoch、降學習率。
  - 工具:LLaMA-Factory Online(廣告)、開源 `peft` ＋ `transformers`;模型例:Llama-2-7B-Chat、Qwen-7B-Chat。
- 對作業:AT2 若想把「微調」寫進方法,要附成本/資料量估算;一般課程專案用 **提示工程＋RAG** 就夠,微調可以寫成「未來改進」並說明為什麼現在不做(資料不足、成本)。

### LLM API 快速入門(3 個)

| API | 重點(依 2026-10-24 頁面) | 狀態 |
|---|---|---|
| **OpenAI** https://developers.openai.com/api/docs/quickstart | 建 API key → 設環境變數 `OPENAI_API_KEY` → `pip install openai`;第一個範例用 **Responses API**(`client.responses.create`),示範模型 `gpt-6-astra`;後續範例:圖片/PDF 輸入、內建工具(web search、file search、Code Interpreter)、function calling、遠端 MCP、串流、Agents SDK 多代理分流。新用戶有一次免費測試請求,之後要儲值。 | 已讀 |
| **Gemini** https://ai.google.dev/gemini-api/docs/quickstart?lang=python | 在 Google AI Studio 建 key → 環境變數 `GEMINI_API_KEY` → `pip install -U google-genai`;快速入門現在用 **Interactions API**(`client.interactions.create`),示範模型 `gemini-3.8-flash`;付費層要開 Cloud Billing、預付至少 5 美元提高速率上限。⚠️ 下面的 cookbook notebook 用的是另一種寫法 `client.models.generate_content`,兩種都在同一個 SDK。 | 已讀 |
| **阿里雲百煉 Model Studio(通義千問 Qwen)** https://www.alibabacloud.com/help/en/model-studio/first-api-call-to-qwen | 開通 Model Studio → 建 API key → 環境變數 `DASHSCOPE_API_KEY`;可用 DashScope SDK 或 **OpenAI 相容介面**(OpenAI SDK 改 `base_url` 為 `.../compatible-mode/v1`);第一個範例模型 `qwen3.8-max`;**新加坡、美國(維吉尼亞)、北京三區的 key 不能互通**,端點網址含 Workspace ID;頁面沒提新用戶免費額度。 | 已讀 |

- 對作業:AT3 程式碼建議用「OpenAI 相容介面」寫,一份程式可以切換 OpenAI/Qwen(只換 `base_url` 與 key),報告可把「模型可替換」寫成架構優點。

### OpenAI / Gemini Cookbook 範例(10 個)

> ⚠️ 6 個 OpenAI cookbook 網址都 308 轉址到 `developers.openai.com/cookbook/...`,而且頁面都標示**已封存(archived),可能引用過時模型或 API**(多半用 gpt-4o / gpt-4o-mini)。照著做時把模型換成現行型號,概念與流程仍然適用。

#### 1. Classification using embeddings(用 embedding 做分類)
- 網址:https://cookbook.openai.com/examples/classification_using_embeddings ｜狀態:已讀(封存版)
- 目標:用評論文字的 embedding 預測食品評論的星等(1–5 星)。
- 資料:約 1,000 筆食品評論(檔名 `fine_food_reviews_with_embeddings_1k.csv`,embedding 在另一本 notebook 先算好),80/20 切分。
- 方法:embedding 當特徵 → 隨機森林(100 棵樹)分類 → `classification_report` ＋ PR 曲線。
- 結果:準確率 0.78,但**類別極不平衡**(測試 200 筆中 134 筆是 5 星);macro recall 只有 0.45,2–4 星幾乎抓不到。作者也提到 OpenAI 認為這類任務微調模型通常比 embedding 好。
- AT3 用法:**低成本的文字分類功能**(客訴分類、工單分流、評論情緒);報告記得照它的教訓報 macro 指標與各類別結果,不要只報準確率。

#### 2. Context Summarization with Realtime API(即時語音對話的上下文摘要)
- 網址:https://cookbook.openai.com/examples/context_summarization_with_realtime_api ｜狀態:已讀(封存版)
- 目標:語音聊天機器人對話越來越長時,把舊的對話自動壓縮成摘要,避免上下文塞爆、品質下降。
- 架構:麥克風 24 kHz PCM-16 音訊切 40 ms 小塊,經 WebSocket 送 `gpt-realtime`;`gpt-4o-transcribe` 轉文字;`gpt-4o-mini` 當便宜的摘要模型;從每次 `response.done` 事件讀 token 數決定要不要摘要。
- 策略:token 超過門檻(示範 2,000,正式建議 20k–32k)就把較舊的回合摘要成一段,以 **system** 訊息放回對話開頭(用 assistant 角色可能讓模型改用文字回覆),只保留最後 2 回合原文,並刪掉伺服器端的舊項目。
- 觀察:同樣內容,音訊比文字多吃約 10 倍 token;notebook 部分程式碼有小錯(作者頁面也指出)。
- AT3 用法:做「語音客服/語音助理」才用得到;一般專案可借它的「長對話自動摘要」概念。

#### 3. Data Extraction and Transformation in ELT Workflows(用 GPT-4o 取代 OCR 做資料萃取)
- 網址:https://cookbook.openai.com/examples/data_extraction_transformation ｜狀態:已讀(封存版)
- 目標:把格式不一、德英混雜的 2019 年德國飯店發票 PDF,變成可查詢的資料庫。
- 流程:PDF 每頁轉 PNG → **Extract**:GPT-4o 看圖輸出原始 JSON(保留原語言鍵名、空欄填 null、不准捏造)→ **Transform**:第二次呼叫把原始 JSON 對應到目標 schema、翻成英文、統一日期格式 → **Load**:寫進 SQLite 4 張表(飯店、發票、費用、稅)。
- 設定:JSON 模式、temperature 0;非即時的大量工作可改用 Batch API 省錢。
- 限制:沒報準確率;不同發票/不同次執行的原始鍵名會變;載入時飯店會重複建檔。
- AT3 用法:**很適合當「數據介面」模組** —— 把非結構化文件(發票、報表、合約、PDF)自動轉成結構化表格,再接後面的分析與儀表板。「萃取與轉換分兩步」的設計也很好寫進架構圖。

#### 4. Doing RAG on PDFs using File Search in the Responses API
- 網址:https://cookbook.openai.com/examples/file_search_responses ｜狀態:已讀(封存版)
- 目標:用 OpenAI 託管的 `file_search` 工具,一次 API 呼叫就完成 PDF 的 RAG,不用自己做切塊、embedding、向量庫。
- 流程:建 vector store → 平行上傳 21 份 PDF → 可單獨做向量搜尋 → 在 `responses.create` 掛 `file_search` 回答問題,回應附檔案註記(來源)。
- **評估(最值得學)**:用 gpt-4o 從每份 PDF 生成一題「只有該文件答得出來」的問題 → 強制檢索、取前 5 筆 → 算 **Recall@5 = 0.905、Precision@5 = 0.905、MRR = 0.905、MAP = 0.895**;失敗多出在太籠統的問題。作者建議正式使用要有人工驗證的題庫。
- AT3 用法:**最直接的「知識庫問答助理」功能模板**;AT2「實驗與評估方法」可以照它定義檢索指標(Recall@k、MRR)作為評估設計,符合 HD「前沿基準方法」的要求。

#### 5. How to parse PDF docs for RAG
- 網址:https://cookbook.openai.com/examples/parse_pdf_docs_for_rag ｜狀態:已讀(封存版)
- 目標:簡報、網頁匯出這類圖表很多的 PDF,純文字萃取會漏掉圖表內容 → 讓 RAG 也能搜到圖裡的資訊。
- 流程:pdfminer 抽文字 → pdf2image 把每頁轉圖 → GPT-4o 描述每頁(含圖表、表格)→ 文字與圖片描述合併、**一頁一塊** → embedding 後檢索。8 執行緒平行處理,約 2 分鐘。
- 限制:一頁一塊太陽春;用標題比對描述與文字很脆弱;每份簡報第一頁直接丟掉是硬假設;模型描述沒有驗證。
- AT3 用法:若你們的知識庫文件圖表多(年報、產業報告),在 #4 前面加這一層前處理。

#### 6. Introduction to deep research in the OpenAI API
- 網址:https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api ｜狀態:已讀(封存版)
- 目標:用 API 讓模型自己拆子問題、上網搜尋、彙整成**附引用來源的結構化報告**。
- 模型:`o3-deep-research`(品質高)、`o4-mini-deep-research`(較快);工具:`web_search_preview`(必要)、`code_interpreter`(選用)、MCP(接私有資料)。
- 一次研究常要好幾分鐘 → 用 `background=True` 背景模式避免逾時。
- API 版**不會先追問釐清**,所以建議先用便宜模型做「釐清問題」與「把需求改寫成詳細研究指令」兩步;改寫得太籠統會更慢更貴。
- 輸出的 annotations 有每個引用的文字位置、標題、網址,也能看到中間的搜尋與推理步驟。範例:司美格魯肽(semaglutide)的健康經濟影響報告、旅遊規劃。
- AT3 用法:「自動市場/競品研究報告」功能;也可以拿來幫 AT2 背景章節找文獻(但引用前要自己核對來源)。

#### 7. Marketing Campaign(Gemini cookbook:從產品草圖生成行銷文案)
- 網址:https://cdn.jsdelivr.net/gh/google-gemini/cookbook@main/examples/Market_a_Jet_Backpack.ipynb ｜狀態:已讀(完整 notebook)
- 流程:上傳一張「噴射背包」手繪草圖 →
  1. 請模型描述產品,用 `response_mime_type="application/json"` ＋ `TypedDict` schema 拿到 `{description, features[]}`;
  2. 請模型想 10 個產品名(回傳 `list[str]`),做成下拉選單讓人挑;
  3. 用 few-shot(給兩組 H1/H2 範例)生成 10 組網頁主副標題(回傳 `list[Headings]`);
  4. 最後請模型直接產生 HTML＋CSS 的產品 landing page。
- 模型:`gemini-3.8-flash`(預設,可切換);SDK `google-genai`。
- AT3 用法:**示範「結構化輸出(structured output)」最乾淨的範本** —— 讓 LLM 回固定 JSON 格式,前端/資料庫才接得住;「AI 給選項、人來選」也是很好的人機協作介面設計。

#### 8. Generation for Story Writing(連結是 SourceForge 鏡像)
- 網址:https://sourceforge.net/projects/cookbook-google-gemini.mirror/ ｜狀態:已讀(鏡像頁＋另讀 GitHub 官方 notebook)
- **連結本身**:SourceForge 對 google-gemini/cookbook 的非官方鏡像首頁(聲明與官方無關),Apache 2.0;頁面只有 cookbook 總介紹(quickstart、多模態、Veo、Lyria、Live API…),**沒有任何 story writing 內容**。
- **實際對應的 notebook**:官方 repo 的 `examples/Story_Writing_with_Prompt_Chaining.ipynb`,重點:
  - **提示鏈(prompt chaining)**:大任務拆成串接的小提示 —— 前提(premise)→ 大綱(outline)→ 開頭 → 續寫;前一步輸出當下一步輸入。好處:每步更準、出錯好除錯、能做單次做不到的複雜任務。
  - **迭代生成(iterative generation)**:每次把「前提＋大綱＋目前全文」餵回去續寫至少 1,000 字,直到模型輸出 `IAMDONE` 停止 → 突破單次輸出長度上限,也方便人在每一步介入修正。
  - 每個提示都放同一段角色設定(persona)與寫作守則,用 f-string 重複帶入。
- AT3 用法:**自動生成長篇分析報告**的模式(例:資料 → 重點 → 大綱 → 分章撰寫);報告也可以把「提示鏈」寫成系統設計的一部分。

#### 9. Video Analysis – Event Recognition(影片辨識歷史事件)
- 網址:https://nbviewer.org/urls/cdn.jsdelivr.net/gh/google-gemini/cookbook/examples/Analyze_a_Video_Historic_Event_Recognition.ipynb ｜狀態:已讀(nbviewer 回 429,改讀 jsDelivr 上同一份原檔)
- 流程:下載美國國家檔案館的公有領域影片(雷根 1987-06-12 柏林圍牆演說,約 600 MB)→ `client.files.upload` 上傳 → 輪詢等狀態從 PROCESSING 變可用 → 系統提示設定「專精影像史料的歷史學家」,請它回答「何時發生、最重要人物、事件名稱」→ 用完刪檔。
- 結果:模型正確答出日期、雷根、「推倒這道牆」演說。
- notebook 為了避免歷史題材被誤擋,把安全設定全調成 BLOCK_NONE —— 做給一般使用者的產品**不建議照抄**。
- AT3 用法:影片/監視畫面/教學影片的內容理解(例:自動產生影片摘要、標籤)。

#### 10. 3D Spatial understanding(3D 空間理解)
- 網址:https://nbviewer.org/github/google-gemini/cookbook/blob/main/examples/Spatial_understanding_3d.ipynb ｜狀態:已讀(nbviewer 429,改讀 jsDelivr 原檔)
- 標示**實驗性功能**;官方建議要準確度就改用 2D bounding box。
- 能力:
  - **指點(pointing)**:回傳物件座標 `[y, x]`,正規化到 0–1000;可結合推理(例:標出每個零件並說明用途、廚房安全隱患、辦公室改善建議、預測移動軌跡)。
  - **多視角對應**:先在一個角度標點(用 a、b、c 代號避免模型靠語意猜),換角度後找同一點;建議用 `gemini-2.5-pro`。
  - **3D bounding box**:9 個數字 = 物體中心(公尺)＋尺寸(公尺)＋翻滾/俯仰/偏航角(度),可投影回圖上與俯視圖。
  - 建議 temperature 0.5、限制最多 10 個物件,避免模型重複或打轉。
- AT3 用法:比較冷門(零售貨架、倉儲、機器人、室內設計才用得到);一般資料分析專案不必選。

### Cookbook × AT3 功能對照(挑 1–2 個做成系統模組)

| 專案情境 | 推薦範例 | 可對應的 AT3 評分項 |
|---|---|---|
| 公司內部文件問答、客服知識庫 | #4 File Search RAG(＋#5 圖表 PDF 前處理) | 分析介面＋技術創新;評估可用 Recall@k、MRR |
| 一堆 PDF/發票/報表要變成可分析的表 | #3 資料萃取 ELT | 數據介面 |
| 評論、客訴、工單自動分類 | #1 Embedding 分類 | 分析介面;用 macro 指標評估 |
| AI 產生建議/文案,讓使用者挑選 | #7 結構化 JSON 輸出 | 使用者介面＋可行動的功能 |
| 自動產出分析報告或研究摘要 | #8 提示鏈、#6 Deep Research | 發現與建議、業務影響 |
| 語音助理、影片理解 | #2、#9 | 技術創新(加分但門檻高) |

---

## 狀態總表(45 列)

| inventory 列 | 位置 | 連結 | 狀態 |
|---|---|---|---|
| 173 | M352284#7 | Discover 30% 大腦皮層 | 已讀 |
| 174 | M352284#7 | Driven by Data | 已讀 |
| 175 | M352284#7 | 運動員出生國堆疊面積圖 | 部分(細節在 NYT 付費原文) |
| 176 | M352284#7 | NYC Open Data 視覺化工具 | 已讀(可見部分) |
| 177 | M352284#7 | NYC 車禍資料集 | 已讀(授權頁面未列) |
| 178 | M352284#8 | from Data to Viz | 已讀 |
| 134 | M352284#10 | sequencediagram.org | 已讀 |
| 135 | M352284#10 | Yonyx 流程圖一致性 | 已讀 |
| 136 | M352284#10 | TechTerms 流程圖定義 | 已讀 |
| 137 | M352284#10 | 百度百科 流程圖 | 已讀(瀏覽器) |
| 138 | M352284#10 | Visual Paradigm DFD | 已讀 |
| 139 | M352284#10 | 百度百科 數據流圖 | 已讀(瀏覽器) |
| 140 | M352284#10 | BeginnersBook ER 圖 | 已讀 |
| 141 | M352284#10 | Smashing 色彩理論 | 已讀 |
| 142–147 | M352284#11 | D3 / Gephi / Matplotlib / Seaborn / Plotly / Tableau | 已讀 |
| 148 | M352284#11 | NYC Taxi 一天 | 已讀 |
| 149 | M352284#11 | Visme 最佳視覺化 | 已讀 |
| 150 | M352284#12 | Esri shapefile 注意事項 | 已讀 |
| 151 | M352284#17 | R2D3 圖解機器學習 | 已讀 |
| 152 | M352284#17 | 騰訊雲 機器學習可視化 | 已讀 |
| 153 | M352284#18 | Medium Bagging & Boosting | 已讀(瀏覽器) |
| 154 | M352284#20 | PyTorch 60 分鐘 | 已讀 |
| 155 | M352284#20 | TF 時間序列 | 已讀 |
| 156 | M352284#20 | 5 個框架首頁 | 已讀 |
| 157 | M352284#21 | 提示工程最佳實踐 | 已讀(瀏覽器) |
| 158 | M352284#21 | LoRA(騰訊雲) | 已讀 |
| 159 | M352284#21 | 微調實戰(火山引擎) | 已讀 |
| 160–162 | M352284#21 | OpenAI / Gemini / Qwen 快速入門 | 已讀 |
| 163–168 | M352284#21 | 6 個 OpenAI cookbook | 已讀(封存版) |
| 169 | M352284#21 | 行銷案 notebook | 已讀 |
| 170 | M352284#21 | Story Writing(鏡像頁) | 已讀(另讀官方 notebook) |
| 171–172 | M352284#21 | 影片辨識、3D 空間 | 已讀(改讀原檔) |
