# 課程導學＋單元一｜外部延伸閱讀整理(20 個連結)

> **範圍**:素材盤點 `notes/raw/inventory_2026-10-24.tsv` 中,位置在 M352280(課程導學)與 M352282(單元一)的全部 `link` 列,共 20 筆。順序照盤點檔。
> **位置代碼**:`M352280#5` = 課程導學第 5 項 → 對應 `notes/00_課程導學.md` 的「## 5.」;`M352282#10` = 單元一第 10 項 → 對應 `notes/01_單元一_數據分析項目簡介.md` 的「## 10.」。
> **抓取日期**:2026-10-24。抓取方式每節都有寫(WebFetch／curl 不帶 cookie／Claude 內建瀏覽器只讀)。
> **用詞**:課程原文用「數據／項目／利益相關者」,本檔用台灣用語「資料／專案／利害關係人」,意思相同。第三方文章都是用自己的話摘要,沒有整段翻譯。
> **狀態**:✅ 已讀完整｜🟡 部分(原頁已搬走,用官方替代頁補)｜⚪ 工具型連結(一行帶過)

---

## 0. 一眼看完

| # | 位置 | 來源(課程連結文字) | 狀態 | 一句話重點 |
|---|---|---|---|---|
| 1 | M352280#2 | ask-librarian(UTS 圖書館) | ⚪ | 圖書館線上諮詢、FAQ(引用格式、版權) |
| 2 | M352280#5 | Tuckman 團隊發展階段(West Chester Univ.) | ✅ | 形成→風暴→規範→執行→解散;傾聽是跨過衝突期的關鍵 |
| 3 | M352280#5 | Canvas Inbox 使用說明 | ⚪ | 怎麼在 Canvas 收發站內信(組隊聯繫要用) |
| 4 | M352282#10 | 範圍蔓延(百度百科) | ✅ | 沒走正式變更流程的範圍擴大;用範圍說明書＋WBS＋變更控制擋 |
| 5 | M352282#10 | 《人工智能項目的敏捷框架》(Medium/TDS) | ✅ | AI 專案也要短迭代;四階段:需求、開發、QA、部署維護;標準＝敏捷的前提 |
| 6 | M352282#10 | 《使用 CRISP-DM 時的四個問題及其解決方法》(KDnuggets) | ✅ | 缺乏明確性、盲目返工、盲目丟給 IT、不迭代;解法＝聚焦「決策」 |
| 7 | M352282#10 | 重新發現數據科學流程(KDnuggets) | ✅ | Harvard 五步流程＝KDD/CRISP-DM 換包裝,但仍有價值 |
| 8 | M352282#10 | 為什麼敏捷方法無法滿足 AI 與 ML 專案(Cognitive World) | ✅ | AI 由資料驅動、交付物模糊;建議「敏捷＋CRISP-DM 雙迴圈」或 CPMAI |
| 9 | M352282#10 | 機器學習專家講解資料科學中的敏捷(iunera) | ✅ | 假設驅動實驗、使用者故事、backlog;MLOps＝敏捷落地;文化最重要 |
| 10 | M352282#10 | 什麼是 TDSP?(datascience-pm.com) | ✅ | Microsoft 的團隊版 CRISP-DM:5 階段、6 角色、加上「客戶驗收」 |
| 11 | M352282#12 | 15 個資料與 AI 專案需求收集問題(AI Consulting Group) | ✅ | 一份可直接拿來寫 AT2 的需求訪談清單 |
| 12 | M352282#12 | 如何把業務問題轉成資料問題(Analytics Vidhya) | ✅ | 把質性需求量化;錯誤成本決定指標;標註品質要量測 |
| 13 | M352282#13 | MLOps(百度百科) | ✅ | DevOps 用在 ML:資料、模型、程式碼都要版本控制與監控 |
| 14 | M352282#13 | 利害關係人分析(Mind Tools) | ✅ | 辨識→權力/興趣方格排序→理解動機;四象限各有對應做法 |
| 15 | M352282#13 | 利害關係人參與 10 項原則(APM) | ✅ | 及早且常常諮詢、建立信任、把人當風險、了解各方的「成功」 |
| 16 | M352282#15 | 敏捷開發中專案計畫的角色(Wrike) | ✅ | 敏捷也要計畫:活文件、第一個衝刺寫細、之後逐輪規劃 |
| 17 | M352282#18 | Oxford Languages | ⚪ | 「research」字典定義的出處(Google 英文字典的資料來源) |
| 18 | M352282#18 | 澳大利亞卓越研究 ERA(ARC) | ✅ | ERA 已於 2023 停辦、改做新評鑑;「研究」的正式定義另外找到 |
| 19 | M352282#4 | 《澳大利亞數據戰略》 | 🟡 | 2021 年願景:2030 成為資料驅動社會;三主題;2023-12 已被新策略取代 |
| 20 | M352282#4 | 數據質量(百度百科) | ✅ | 資料品質＝符合用途的程度;準確、完整、一致、時效;改善六步 |

---

## 0.1 跨來源整合:寫 AT2/AT3 時去哪裡找

**AT2 計畫報告 12 節 → 可用的來源**

| AT2 章節 | 可以用的來源(本檔節號) | 怎麼用 |
|---|---|---|
| 背景 | #19 澳洲資料策略、#18 ERA 研究定義 | 政策脈絡;說明本專案的「研究成分」在哪 |
| 業務目標 | #6 聚焦決策、#12 質性→量化、#11 Q5–Q7 | 寫成「要改善哪個決策＋怎麼衡量＋值多少錢」 |
| 分析目標和任務 | #12、#9(假設、使用者故事)、#18 | 研究問題寫成可檢驗的假設 |
| 資料與資源 | #20 資料品質、#11 Q12、#12 資料探索 | 列資料集、欄位、品質維度、理想 vs 實際的落差 |
| 分析系統架構 | #13 MLOps、#11 Q11、#8 雙迴圈 | 畫出資料→模型→介面→監控的流水線 |
| 分析方法 | #7 方法論比較、#10 TDSP、#8 | 說明選 CRISP-DM／TDSP／混合的理由 |
| 實驗與評估方法 | #12 錯誤成本→指標、#5 實驗管理、#11 Q2 人工基準 | 指標要對到業務;記錄資料與超參數版本 |
| 實施設計 | #10 TDSP 角色、#5 四階段、#16 | 角色對應課程 5 個主要職責 |
| 預期成果 | #8 交付物定義、#11 Q15 範圍外 | 明講交付的是模型、功能還是系統 |
| 時間表＋里程碑 | #16 衝刺規劃、#5 | 第 8–12 週切成幾個衝刺,每輪有可展示的成果 |
| 風險管理 | #4 範圍蔓延、#15 利害關係人風險、#20 資料品質、#5 技術債、#8 模型偏誤、#2 團隊衝突 | 每個風險配對策 |
| 參考文獻 | 見 §21 引用草稿 | 百度百科不建議當學術引用 |

**AT3 分析報告/展示 → 可用的來源**
- **部署計畫**:#13 MLOps、#6 問題 3「盲目丟給 IT」與問題 4「不迭代」→ 寫清楚誰部署、怎麼監控、何時重訓。
- **使用者介面**(HD 要互動式):#11 Q9(篩選、時間趨勢、下鑽)。
- **業務影響**:#6「改善了哪個決策」、#10 TDSP「客戶驗收」。
- **與 AT2 一致性＋說明變更(10 分)**:#4 變更控制 → 每個變更都要有紀錄和理由。
- **系統運行流暢(展示 12 分)**:#9 不要把 notebook 直接當成品。

**AT1 週報/AT4 反思**:#2 Tuckman 階段(描述團隊狀態)、#9 backlog／回顧(retrospective)、#16 衝刺。

---

## 1. ask-librarian(M352280#2)⚪

- **URL**:https://www.lib.uts.edu.au/help/ask-librarian → 轉址到 https://www.lib.uts.edu.au/get-help/contact-us(UTS Library「Contact Us」)
- **抓取**:WebFetch 失敗(DNS 解析不到);改用 curl(不帶 cookie)成功。
- **一行**:UTS 圖書館聯絡頁,有線上聊天(開館時間內,可問找文獻、使用圖書館、引用格式、作業)與 FAQ(引用到版權都有);實體館在 UTS Central 7–9 樓。課程放在「教學團隊」頁,告訴學生要找圖書館員時去這裡。對 Kenny:寫 AT2/AT3 遇到 UTS APA 引用問題,可以用線上聊天問。

---

## 2. Tuckman's Stages of Group Development - West Chester University(M352280#5)✅

- **URL**:https://www.wcupa.edu/coral/tuckmanStagesGroupDelvelopment.aspx
- **實際標題/作者**:Tuckman's Stages of Group Development;West Chester University CORAL(線上協作研究與學習計畫);Thomas Treadwell、Evan Leach(West Chester)、Donna Ashcraft(Clarion);最後更新 2024-12-04。
- **抓取**:WebFetch 成功。

**重點**
- 團隊會經過五個階段:**形成(Forming)→ 風暴(Storming)→ 規範(Norming)→ 執行(Performing)→ 解散(Adjourning)**。過程中領導方式會從「一個人帶」慢慢變成「大家共同領導(shared leadership)」。
- **形成期**:大家客氣、避免衝突、等領導者給方向。這時最需要清楚的任務、角色、基本規則(ground rules)。想往下一階段走,成員要願意冒一點衝突的風險。
- **風暴期**:搶主導權、角色不清、目標不切實際、進度卡住。需要處理衝突、重新釐清目的和規則。**傾聽**是跨過這個階段最重要的能力。
- **規範期**:建立共同流程、用共識做決定、互相信任;資訊流通、創意高。缺點是成員怕團隊結束,開始抗拒改變。
- **執行期**:角色清楚、自我組織,可以各做各的、分小組或一起做。**不是每個團隊都走得到這裡**。
- **解散期**:收尾、評估團隊表現、肯定成果。有計畫的結束(正式收尾、互相道別)能減少失落感。
- 團隊會**倒退**:有新成員加入或有人常缺席,就可能回到前面階段,要準備好快速拉回正軌。

**課程為什麼連這個**:課程導學「5. 團隊組建」頁的「教學資源 1」,要求在第 1 週第一次 Zoom(10/29 組隊工作坊)之前讀,用來理解組隊過程和團隊動態。

**對作業的用處**
- **AT4 自我反思**(「團隊協作經驗」):可以用 Tuckman 階段描述團隊怎麼一路走過來,並引用這份資料。
- **AT1 週報**:用階段語言寫團隊狀態(例如「第 3 週進入規範期,定好每週例會與分工」),之後 AT4 要引用週報當證據時比較好用。
- **AT2 風險管理**:把「團隊衝突、成員缺席」列為風險,對策＝一開始就定好角色與基本規則(對應課程 5 個主要職責)。

---

## 3. Canvas Inbox(M352280#5)⚪

- **URL**:https://community.canvaslms.com/t5/Student-Guide/How-do-I-use-the-Inbox-as-a-student/ta-p/532 → 301 轉到 community.instructure.com → 最後落在 https://community.instructure.com/en/kb/articles/662865-how-do-i-use-the-inbox(How do I use the Inbox? - Instructure Community)
- **抓取**:WebFetch 對新網域 DNS 失敗;改用 curl 下載 HTML,從頁面內容抽出說明文字。
- **一行**:Canvas 站內信的使用說明:從左側全域導覽列點 Inbox 進入(數字＝未讀數);可依課程與類型(Inbox、Unread、Starred、Sent、Archived、Submission Comments)篩選;用 Compose 寫新信,在對話中可 Reply、Reply-all、Archive、Delete、加星號。課程在「團隊組建」頁放這個連結,是告訴學生可以用 Canvas Inbox 私下聯絡潛在隊友。⚠️ 提醒:組隊相關的申請**只能**用 Canvas Message 寄給 Dr. Li Guan,主旨寫「团队组建 Team Formation」。

---

## 4. 範圍蔓延(M352282#10)✅

- **URL**:https://baike.baidu.com/item/%E9%A1%B9%E7%9B%AE%E8%8C%83%E5%9B%B4%E8%94%93%E5%BB%B6/6937255
- **實際標題**:項目範圍蔓延_百度百科(英文 Project scope creep;條目最近更新 2026-09-15)
- **抓取**:WebFetch 與 curl 都被擋(403/百度安全驗證頁);用 Claude 內建瀏覽器正常開啟後讀取文字(沒有出現驗證碼,也沒有做任何互動)。

**重點**
- **定義**:專案範圍在執行過程中**不受控制地**擴大,超出原本的範圍、資源和時程。也叫範圍膨脹、需求蔓延、功能蔓延(feature creep)。
- **判斷關鍵**:如果範圍變大,同時也相應增加了預算、資源和時間,就**不算**範圍蔓延。重點在「沒有經過正式的變更管理」。
- **成因**:需求定義模糊、利害關係人一直改需求、沒有變更控制流程、溝通不良,還有團隊自己加沒人要的功能(稱為「鍍金 gold plating」)。
- **後果**:延期、超支、品質下降、成員過勞、成果跟期待不符。條目舉丹佛國際機場行李系統為例:約 2,100 次設計變更,超支 300%,延誤 16 個月。
- **預防**:啟動時和利害關係人一起寫好範圍說明書(scope statement)、建工作分解結構(WBS)、寫需求文件、用 SMART 目標、設階段驗收。
- **控制**:正式的變更控制流程,可設變更控制委員會(CCB)審查;所有變更都要評估對範圍、時間、成本、品質的影響;用核准過的基準計畫(baseline)比對進度;用甘特圖追蹤。
- **技巧**:對不合理的變更學會說「不」並說明影響;用「影響-努力矩陣」(Impact vs. Effort Matrix)排需求優先順序;遵守 KISS 原則,保持簡單。

**課程為什麼連這個**:在 1.6「項目管理方法論」的敏捷方法段落:敏捷能彈性處理變化,但代價可能是範圍蔓延(客戶常改主意),所以要小心管理。

**對作業的用處**
- **AT2 風險管理**:直接列「範圍蔓延」為風險,對策＝定範圍凍結點、變更要全隊同意並記錄、用影響-努力矩陣排優先。
- **AT2 預期成果**:寫清楚「做什麼」和「不做什麼」(out of scope)。
- **AT3「與 AT2 一致性＋說明變更」(10 分)**:這就是變更控制的實際應用,每個變更都要有紀錄和理由。
- ⚠️ 百度百科不適合放進學術參考文獻;要引用請改用 PMI 或教科書。

---

## 5. 《人工智能項目的敏捷框架》(M352282#10)✅

- **URL**:https://medium.com/data-science/an-agile-framework-for-ai-projects-6b5a1bb41ce4
- **實際標題/作者**:An Agile Framework for AI Projects;Jenny Abramov(與 Idan Bassuk 合著);刊在 Medium「TDS Archive」(原 Towards Data Science);2019-12-31;系列第一篇。
- **抓取**:WebFetch 與 curl 都回 403(Cloudflare 檢查頁);用 Claude 內建瀏覽器開啟後讀到全文。

**重點**
- 軟體界已經有共識:要用**迭代生命週期**(iterative lifecycle)。版本上線後才會拿到真實使用者回饋,所以迭代要短,而且要聚焦在弄懂使用者要什麼。
- 很多 AI 團隊正在重複軟體界以前的錯:花幾個月做功能,結果使用者用不到;或過度追求系統擴充性。AI 沒有改變「做出好產品」的本質,只是有些細節讓現有方法不好直接套用。
- **為什麼要迭代**:創新產品很難事先定對需求(連帶演算法需求也很難定)。盡快交到使用者手上,看回饋和數據決定下一步,可以降低 AI 特有的風險:做錯模型、優化錯指標、某個指標做過頭。
- 提出的框架有**四個階段:需求(Requirements)、開發(Development)、品質保證(QA)、部署與維護(Deployment & Maintenance)**。本篇只講動機和總覽,各階段細節在後續文章。Canvas 1.6 那張敏捷圖就是改編自這裡(需求:產品(演算法包)、需求、可行性與複雜度評估;開發:設計資料收集與標註方法、收集與標註、演算法開發與訓練、測試與評估)。
- **標準是保持敏捷的前提**:迭代之間會暫停(例如等客戶回饋),標準低的專案很難重新上手。軟體工程標準、實驗管理系統、資料收集與模型開發流程,可以減少每次新迭代前要先還的**技術債**(technical debt)。
- 「機器學習的意外」(Machine Learning Surprise):大家以為調演算法最花力氣,實際上資料收集、基礎設施、系統整合花的力氣多得多。
- **內部品質**(internal quality)常見的缺口:沒記錄上線模型用的確切資料或資料前處理程式、沒記錄訓練用的超參數(hyperparameters)、程式碼重複或把數值寫死。這些讓這一輪變快,但下一輪可能要花好幾週重找。

**課程為什麼連這個**:1.6「項目管理方法論」中敏捷方法那張圖的標註寫「改編自」這篇。

**對作業的用處**
- **AT2 實施設計/時間表**:用四階段＋短迭代規劃第 8–12 週。
- **AT2 實驗與評估方法**:寫明會記錄資料版本、程式版本、超參數(實驗管理),AT3 也比較容易重現結果。
- **AT2 風險管理**:「資料收集與處理比預期久」(ML 意外)＋技術債。時間表要替資料處理留足時間(呼應 1.11「80% 的工作在把資料處理到可用」)。

---

## 6. 《使用 CRISP-DM 時的四個問題及其解決方法》(M352282#10)✅

- **URL**:https://www.kdnuggets.com/2017/01/four-problems-crisp-dm-fix.html
- **實際標題/作者**:Four Problems in Using CRISP-DM and How To Fix Them;James Taylor(Decision Management Solutions);KDnuggets,2017-01-18。
- **抓取**:WebFetch 成功。

**重點**
- CRISP-DM 是最普及的資料探勘方法論,好處是可重複;但實務上常被簡化成「走樣版」。
- **問題 1 缺乏明確性**(lack of clarity):只停在高層的業務目標和成功指標,沒深挖具體業務問題就急著碰資料,結果模型很有趣但沒解決真正的需求。
- **問題 2 盲目返工**(mindless rework):只用分析指標評估,以為預測準就有用;不達標時去找新資料、新技術,而不是回頭跟利害關係人重新檢視業務問題。
- **問題 3 盲目丟給 IT**(blind hand-off to IT):沒規劃部署,或很晚才找 IT;部署被當成純工程工作,模型被「丟過牆」→ 部署又貴又慢,很多模型最後對業務沒影響。
- **問題 4 沒有迭代**(failure to iterate):明知模型會隨環境老化,卻一直延後監控和維護。
- **解法核心＝聚焦「決策」**:要改善哪個決策?改善的定義是什麼?分析真的有改善這個決策嗎?哪些系統和流程承載這個決策?環境出現什麼變化時要重新評估?工具是決策建模與決策管理(decision modeling / decision management)。本篇只概述,細節在後續兩篇。
- 四個問題會互相加重,所以團隊可能做出很厲害的分析,業務價值卻很少。

**課程為什麼連這個**:1.6「項目管理方法論」的「最常見的錯誤」四個加號(缺乏明確性、盲目返工、盲目移交給信息技術團隊、未能進行迭代)就是改編自這篇。

**對作業的用處**
- **AT2 業務目標**:寫成「要改善的決策＋怎麼衡量」,不要只寫「預測 X」。
- **AT2 實驗與評估**:除了 F1/AUC,也要有業務指標。
- **AT3 部署計畫＋業務影響(30 分)**:避開問題 3、4,寫清楚誰部署、怎麼整合進現有流程、怎麼監控與重訓。
- **AT2/AT3 簡報**:準備好回答「這個模型改善了哪個決策」。

---

## 7. 重新發現數據科學流程(M352282#10)✅

- **URL**:https://www.kdnuggets.com/2016/03/data-science-process-rediscovered.html
- **實際標題/作者**:The Data Science Process, Rediscovered;Matthew Mayo(KDnuggets 主編);2016-03-09。
- **抓取**:WebFetch 成功。

**重點**
- 介紹「資料科學流程」(Data Science Process),由 Joe Blitzstein 與 Hanspeter Pfister 為 Harvard CS 109 課設計,共五步:**提出問題 → 取得資料 → 探索資料 → 建模 → 溝通結果**。
- 每一步需要的技能與工具(引 Ryan Fox Squire 的整理):提問靠領域知識與好奇心;取得資料＝爬蟲、清理、資料庫查詢(Python、pandas);探索＝形成假設、找模式與異常(matplotlib、NumPy、SciPy);建模＝迴歸、機器學習、驗證(scikit-learn);溝通＝視覺化、寫作、簡報。
- 這個流程**非線性、可迭代**,強調用問題引導工作,並隨著對資料越熟悉而修正問題。
- 對照 **CRISP-DM**(6 階段,業界事實標準;已不再積極維護但仍很流行)和 **KDD**(Fayyad 等:選擇 → 前處理 → 轉換 → 資料探勘 → 解讀)。三者都從問題開始、要資料、要準備、要建模、最後採取行動。
- 作者結論:新流程大致是 KDD/CRISP-DM 的更新版或換包裝;但新說法能讓新手更容易接受、重新引起注意。只要能產出正確結果,哪種流程都值得用。
- 其他提到的流程:SEMMA(SAS 公司)、Guerrilla Analytics(偏敏捷)、各團隊自己的內部流程。

**課程為什麼連這個**:1.6「項目管理方法論」的「想了解更多」延伸閱讀,補充 CRISP-DM 的來龍去脈和同類流程。

**對作業的用處**
- **AT2 分析方法/實施設計**:要說明為什麼選某個方法論,可引用這篇做 CRISP-DM、KDD、資料科學流程的比較。
- 第五步「溝通結果」對應 AT2/AT3 的簡報,而且聽眾要假設有非技術的利害關係人。

---

## 8. 為什麼敏捷方法無法滿足人工智能與機器學習項目的需求(M352282#10)✅

- **URL**:https://cognitiveworld.com/articles/2020/5/16/why-agile-methodologies-miss-the-mark-for-ai-amp-ml-projects
- **實際標題/作者**:Why Agile Methodologies Miss The Mark For AI & ML Projects;Kathleen Walch;Cognitive World 轉載自 Forbes(Forbes 原文 2020-01-19;頁面顯示日期 2021-03-10)。
- **抓取**:WebFetch 成功。

**重點**
- 敏捷很適合一般應用程式開發,但 **AI 專案是由資料驅動,不是由程式碼驅動**。以應用、架構或軟硬體為中心的既有方法論,都沒有好好處理資料這件事。
- **交付物不清楚**:訓練好的模型本身不提供功能,而是讓產品功能「變得可能」;模型又是演算法、訓練資料、參數、支援程式碼的組合,所以很難說清楚交付的到底是什麼。
- **角色和語言不同**:敏捷圍繞專案經理、功能、衝刺;資料團隊圍繞資料科學家、資料工程師、分析師,談的是資料來源、清理、模型。
- KDD 太僵化抽象;CRISP-DM 比較能迭代,但發展停滯,IBM、Microsoft 的版本又綁自家產品。
- 作者建議「**敏捷 CRISP-DM**」:跑兩個平行的迭代迴圈,一個是應用開發的敏捷迴圈、一個是資料方法論迴圈,兩者都從共同的業務需求出發。
- 也介紹 **CPMAI**(Cognitive Project Management for AI):加上 AI 專用的強化,可以放進已有敏捷團隊和資料團隊的組織。本文沒有列出 CPMAI 的階段。
- 敏捷和 CRISP-DM 都沒處理好的地方:對話式應用與模型、**辨識並逐步降低模型偏誤(bias)**、以硬體為中心的部署、同時評估與集成(ensemble)多個演算法。
- 結論:用混合做法,在既有流程上加一層低風險的 AI 迭代框架;硬推一套全新流程通常會遇到抵抗。

**課程為什麼連這個**:1.6 延伸閱讀;呼應課文「這不是非此即彼的選擇,要取適合資料分析專案的元素」。

**對作業的用處**
- **AT2 分析方法/實施設計**:可以寫「雙迴圈」:資料／模型迴圈(CRISP-DM)＋應用／介面迴圈(Scrum)並行。這剛好對上 AT3 要同時做「分析系統」和「互動式使用者介面」。
- **AT2 風險管理**:加「模型偏誤」。
- **AT2 預期成果**:先講清楚交付的是模型、功能還是整套系統。

---

## 9. 新方法:機器學習專家講解數據科學中的敏捷方法(M352282#10)✅

- **URL**:https://www.iunera.com/kraken/big-data-science-strategy/the-agile-approach-in-data-science-explained-by-an-ml-expert
- **實際標題/作者**:The Agile approach in data science explained by an ML expert;iunera 訪談文(署名 Dhanhyaa),受訪者 Christos Hadjinikolis(Data Reply UK 首席 ML 工程師);頁面沒寫日期,內容來自他 2018 年在 Mcubed London 的演講。
- **抓取**:WebFetch 成功。

**重點**
- 資料科學本質上是實驗、需求常變,所以適合敏捷。資料科學家在敏捷團隊的角色,是幫團隊**從失敗的實驗中快速學到東西**。
- 但敏捷不是唯一正確的做法:硬推敏捷(他稱為「敏捷產業複合體」Agile Industrial Complex)反而違背敏捷本意。應該挑適合自己情況的做法,重視背後的價值觀。
- **可以直接搬來用的做法**:假設驅動實驗(hypothesis-driven:提假設、定變數、收資料分析、不理想就調整重測)、使用者故事(user stories)與拆分、待辦清單(backlog)、時間盒(timeboxing)、回顧會議(retrospective)、適應性規劃、及早交付、持續改進。
- 相關框架:敏捷宣言(Agile Manifesto)12 原則;Scrum、Kanban、XP、FDD、DSDM 可以用但不必死守;瀑布式在某些專案仍然適合,也可以混用。
- **MLOps 是敏捷在資料科學的具體實踐**;工具例:Kubeflow、AWS SageMaker、Google AI Platform。
- **軟體工程 vs 資料科學**:資料科學傳統上偏研究、常在 notebook 裡做;現在模型上線要版本控制、測試、程式覆蓋率、管理技術債。兩邊各有盲點,因此出現兼具兩者的 ML 工程師(ML engineer)。**把 notebook 直接放上線是壞做法**;推薦延伸閱讀 2014 年 NIPS 論文〈Hidden Technical Debt in Machine Learning Systems〉。
- 結論:文化最重要,需要資料科學家和工程師合作,也需要利害關係人支持實驗;遇到抵抗很正常。

**課程為什麼連這個**:1.6 延伸閱讀。

**對作業的用處**
- **AT1 週報/團隊運作**:用 backlog、時間盒、每輪回顧來管理團隊。
- **AT2 分析目標和任務**:用使用者故事寫(以使用者角度);研究問題寫成可檢驗的假設(呼應 1.15.1「研究問題和技術目標」)。
- **AT3 系統**:不要拿 notebook 當成品,要做成能穩定運作的應用(展示評分「系統運行流暢」12 分)。

---

## 10. 什麼是 TDSP?(M352282#10)✅

- **URL**:https://www.datascience-pm.com/tdsp
- **實際標題/來源**:What is TDSP?(Team Data Science Process);Data Science Process Alliance 網站。
- **抓取**:WebFetch 成功。

**重點**
- TDSP 是 Microsoft 在 2016 年推出的敏捷、迭代方法論,用來交付預測分析和智慧應用;這個網站把它形容成「Scrum＋CRISP-DM」。
- **五個階段**:業務理解 → 資料取得與理解(把 CRISP-DM 的資料理解＋資料準備合併)→ 建模(含特徵工程、訓練、評估)→ 部署 → **客戶驗收**(Customer Acceptance,CRISP-DM 沒有明列)。
- **六個角色**(補 CRISP-DM 沒有團隊指引的缺口):解決方案架構師、專案經理、資料工程師、資料科學家、應用程式開發者、專案負責人;Microsoft 有寫各角色在各階段的任務與產出。
- **四個組成**:生命週期定義、標準化專案結構、建議的基礎設施與資源、建議的工具;標準產出包括專案章程(project charter)、資料報告(data report)。GitHub 有免費範本;常配 Azure,但不綁定。
- **優點**:增量交付;沿用軟體團隊熟悉的 backlog、使用者故事、衝刺、Git;承認資料科學跟軟體工程不同;可以單獨用或搭配 CRISP-DM;文件完整,是最成熟的 CRISP 衍生方法之一。
- **缺點**:固定長度的衝刺不一定適合資料科學工作;Microsoft 的文件有些地方前後不一致。
- 適合要上線的團隊專案;不適合單人或純探索、不打算上線的專案。

**課程為什麼連這個**:1.6 延伸閱讀,提供 CRISP-DM 的「團隊版、敏捷版」替代方案。

**對作業的用處**
- **團隊分工**:TDSP 角色可以對應課程 5 個主要職責(專案經理 ↔ 專案管理、資料科學家 ↔ 方法論、應用開發者 ↔ 軟體工程、專案負責人／架構師 ↔ 業務理解與利害關係人管理)。
- **AT2 實施設計/時間表**:借用五階段,每階段列出產出。
- **AT3**:「客戶驗收」正好對應成果展示建議的「向客戶展示成果」情境,以及業務影響章節。
- 專案章程可以當 AT2「背景＋業務目標」的骨架。

---

## 11. 15 個數據與 AI 項目需求收集的技巧與問題(M352282#12)✅

- **URL**:https://www.aiconsultinggroup.com.au/15-tips-questions-for-requirements-gathering-on-data-ai-projects/
- **實際標題/來源**:15 Tips & Questions for Requirements Gathering on Data & AI Projects;AI Consulting Group(雪梨);沒寫作者與日期。
- **抓取**:WebFetch 成功。

**重點**
- **原則**:一開始先假設什麼都可能;先不要談技術方案;替功能排重要性;先問利害關係人再問開發者;用訪談、工作坊、腦力激盪、書面等方式收集。
- **現況類問題**:專案概述與期望時程;現在人工怎麼做、做得多好(人工基準);組織或專家已經知道什麼、預期什麼結果;做了哪些假設、驗證過沒。
- **價值類問題**:專案目標是什麼、成功和「價值證明」怎麼定義(業務端和分析師都要同意);預期回報大約多少錢;結果會怎麼用(業務決策、投資、選供應商、找風險)。
- **使用者類問題**:誰會用(姓名、角色、專業程度);使用者要怎麼操作結果(篩選、看時間趨勢、下鑽 drill-down);誰可以看、有什麼保密或資安顧慮。
- **技術與資料類問題**:現有技術架構長怎樣、有沒有架構圖;需要的資料是否存在(哪些表、欄位、型別、數量、品質,要怎麼清理轉換)。
- **執行與後續類問題**:有哪些簡單、有順序的檢查點確認進度;上線後誰維護;利害關係人認為什麼**不在範圍內**。
- 結論:需求由利害關係人主導、成功指標大家同意、及早檢查資料和資安,就能降低專案風險。

**課程為什麼連這個**:1.8「界定業務問題的範圍」的延伸閱讀;該頁的活動要學生定出專案的總體目標、具體目標和可交付成果。

**對作業的用處**(這份幾乎就是 AT2 的檢查表)
- 專案概述、目標與成功定義、預期回報 → **背景與業務目標**。
- 資料是否存在與品質 → **資料與資源**;現有架構 → **分析系統架構**。
- 人工基準 → **實驗的基準方法**(baseline)。
- 使用者怎麼操作(篩選、下鑽)→ **AT3 使用者介面**(HD 要互動式 UI)。
- 檢查點 → **里程碑**;上線後誰維護 → **AT3 部署計畫**;不在範圍內 → 防範圍蔓延;保密與資安 → **風險管理**。

---

## 12. 如何將業務問題轉化為數據問題?一份成功數據科學領導者的指南(M352282#12)✅

- **URL**:https://www.analyticsvidhya.com/blog/2019/08/data-science-leader-how-effectively-transition-business-requirements-data-driven-solutions/(課程連結後面另帶 utm 追蹤參數)
- **實際標題/作者**:How can you Convert a Business Problem into a Data Problem? A Successful Data Science Leader's Guide;作者 Om Deshmukh(帳號 odeshmukh);Analytics Vidhya,2019-08-22(2019-09-12 更新);四篇系列的第二篇。
- **抓取**:WebFetch 成功。

**重點**
- **核心**:業務需求通常用質性方式描述,資料科學系統卻需要可以量測的定義。這個轉譯很難、要多方合作,但做好之後,大家對「成功」有共同定義,也有追蹤進度的依據。
- **把「最好」量化**:精確率(precision)、召回率(recall)、準確率、速度哪個最重要?怎麼判斷達標、差距多大?「相似」用哪些維度衡量?需要的資料存在嗎、拿得到嗎?
- **資料探索階段**(data discovery):反覆進行;結合領域知識和初步日誌分析,列出問題的可能原因;比較「理想資料」和「實際資料」的落差。
- **往下找根本原因**:把大原因拆成可檢驗的小問題,依出現頻率排序;靠證據,而不是靠職位最高的人的意見。
- **問對建模問題**:看起來類似的問題會導向不同模型,例如「來電者是誰」是 N 類分類,「來電者是不是 Y 小姐」是 N 個二元分類。由領域專家判斷哪種錯誤最貴(財務、聲譽、法律),法規要求可能比模型信心更優先。
- **標註資料要一致**:用分層抽樣挑樣本;用下拉選單、統一定義減少主觀差異;量測**重複性**(同一人不同時間標得一樣嗎)和**再現性**(不同人標得一樣嗎);用主動學習(active learning)把人力集中在模型最沒把握的樣本。
- **團隊組成**:資料科學家＋大數據工程師＋領域專家。也要先問:這個問題真的需要機器學習嗎?
- 案例:聊天機器人轉真人客服太多 → 拆出意圖誤判、知識庫連線失敗、逾時、資訊不足等可能原因再逐一追查。

**課程為什麼連這個**:1.8「界定業務問題的範圍」的延伸閱讀(從業務問題走到資料問題)。

**對作業的用處**
- **AT2「背景與目標」(18 分,最重的一項)＋「分析目標和任務」**:把業務目標翻成量化的分析目標和評估指標;用錯誤成本決定要看哪個指標(呼應 1.10「定義成功標準」)。
- **AT2 資料與資源**:寫出理想資料和實際資料的落差;HD 要求講資料特徵、分布、相關性,做法就是資料探索。
- 有標註需求時,寫出標註品質怎麼量測。

---

## 13. MLOps(M352282#13)✅

- **URL**:https://baike.baidu.com/item/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%BF%90%E8%90%A5/57691368
- **實際標題**:機器學習運營_百度百科(MLOps)
- **抓取**:WebFetch 與 curl 被擋(403);用 Claude 內建瀏覽器開啟讀取。

**重點**
- **定義**:MLOps 是把 DevOps 原則用到 AI 的一套做法,處理機器學習模型從開發到上線的整個生命週期,被視為大規模運營 AI 的必備能力。
- 涵蓋工具、技術和實務,讓企業能在正式環境部署、監測和管理機器學習模型與其他分析模型(條目引 Forrester)。
- **技術手段**:版本控制、環境隔離、自動化測試,讓模型訓練和部署標準化;核心模組包括持續整合(CI)、監控預警等,能提高模型迭代效率、降低維運風險。
- **MLOps 是 ModelOps 的子集**:MLOps 專注在機器學習模型的規模化營運,ModelOps 涵蓋所有類型 AI 模型的營運化(條目引 Gartner)。
- 業界例子:Microsoft 等已有含資源管理、自動部署、事件驅動架構的完整方案;也有平台廠商在金融、公部門落地。
- ⚠️ 條目偏短,「應用」段落比較像新聞評論拼貼,深度有限;要深入請看 #9 提到的 NIPS 技術債論文。

**課程為什麼連這個**:1.9「與利益相關者合作」:機器學習專案和一般軟體專案不同,模型上線時除了程式碼,資料和模型也要做版本控制,這個流程叫 MLOps(也是利害關係人容易搞混的地方)。

**對作業的用處**
- **AT3 部署計畫**:寫出資料、模型、程式碼的版本控制、監控方式、何時重訓。
- **AT2 分析系統架構**:可以畫出 MLOps 流水線。
- 跟利害關係人溝通「模型會老化、需要維護」(呼應 #6 問題 4)。
- ⚠️ 百度百科不建議當學術引用。

---

## 14. 利益相關者分析:為你的項目贏得支持(M352282#13)✅

- **URL**:https://www.mindtools.com/pages/article/newPPM_07.htm → 已轉址到 https://www.mindtools.com/aol0rms/stakeholder-analysis/
- **實際標題/來源**:Stakeholder Analysis;Mind Tools,2025-04-10 版本。頁面有會員註冊提示,但文章內容完整可讀。
- **抓取**:原網址的轉址目標(members.mindtools.com)WebFetch 解析不到;用 curl 找到新網址後,WebFetch 讀取成功。

**重點**
- 利害關係人分析是利害關係人管理的第一步:找出誰能支持或阻擋你的工作、力氣該花在誰身上、各自需要什麼。
- **好處**:早點拿到有權力者的意見,專案會更好,他們也更願意支持;比較容易爭取資源;持續溝通讓他們了解好處;能預測他們的反應。
- **步驟 1 辨識**:腦力激盪出所有受影響、有影響力、或在意結果的人(老闆、同事、團隊、客戶、供應商、股東、監管機關、媒體等);對象是組織時,也要找到裡面具體要溝通的人。
- **步驟 2 排序:權力/興趣方格**(Power/Interest Grid,改編自 Mendelow 1981):
  - 高權力、高興趣 → **密切管理**(Manage Closely):全力投入、盡量讓他們滿意。
  - 高權力、低興趣 → **使其滿意**(Keep Satisfied):讓他們滿意就好,不要訊息轟炸。
  - 低權力、高興趣 → **保持告知**(Keep Informed):持續告知、留意問題,他們常能幫忙處理細節。
  - 低權力、低興趣 → **監看**(Monitor):注意即可,不必過度溝通。
- **步驟 3 理解**:他們在財務或情感上有什麼利害、是正面還是負面?最在意什麼?想要什麼資訊、用什麼管道?現在的看法是否基於正確資訊?誰影響他們?怎麼把懷疑的人變成支持者?贏不了的話怎麼管理反對?
- **技巧**:直接問對方通常最快;用顏色標記立場(支持＝綠、反對＝紅、中立＝橘);畫成視覺地圖並定期更新,因為立場會隨專案改變。

**課程為什麼連這個**:1.9「與利益相關者合作」:頁面活動要學生完成利害關係人分析(例如最後一位「市場營銷創新經理」);這篇是延伸閱讀。

**對作業的用處**
- 課程 5 個主要職責之一就是「**利害關係人管理**」,要做的正是利害關係人分析。
- **AT2**:背景或實施設計可以附一張權力/興趣方格。
- **AT2 簡報**:要假設台下有非技術的利害關係人,依象限決定講多深。
- **AT3 部署與業務影響**:點名誰受益、誰要配合。

---

## 15. 利益相關者參與的 10 項關鍵原則(M352282#13)✅

- **URL**:https://www.apm.org.uk/resources/find-a-resource/stakeholder-engagement/key-principles
- **實際標題/來源**:10 Key Principles of Stakeholder Engagement;Association for Project Management(APM,英國專案管理協會)。
- **抓取**:WebFetch 成功。

**重點**(10 項原則,兩兩合併說明)
- **溝通**:先了解利害關係人再分享資訊;**及早且經常諮詢**(consult early and often),一起談定需求和可行方案。
- **人性**:人不一定理性,了解他們的動機和感受才好合作;**關係是關鍵**,有信任才容易一起解決問題、做決定。
- **規劃**:接觸利害關係人之前先好好規劃;「簡單但不容易」——預先想到可能的麻煩、及時採取簡單的行動,效果常勝過傳統規劃。
- **風險**:利害關係人管理是風險管理的一部分,他們既可能是風險來源,也可能是機會。
- **妥協**:在不同期待之間找出大家可接受的基線,依各方重要性加權,並跟專案贊助者(sponsor)確認。
- **成功與責任**:搞清楚每一群利害關係人眼中的「成功」是什麼;利害關係人參與是每個人的責任,治理架構要定清角色與期待。

**課程為什麼連這個**:1.9「與利益相關者合作」的延伸閱讀。

**對作業的用處**
- **AT2 風險管理**:加入「利害關係人」相關風險(需求改變、期待不一致)。
- **AT2 業務目標**:按利害關係人群組列出各自的成功指標(呼應 1.10「定義成功標準」)。
- AT2 報告要回應簡報收到的回饋、AT3 報告要回應展示收到的回饋,就是「及早且經常諮詢」的實際做法。

---

## 16. 項目計劃在敏捷開發中發揮什麼作用?(M352282#15)✅

- **URL**:https://www.wrike.com/project-management-guide/faq/what-role-does-the-project-plan-play-in-agile-development
- **實際標題/來源**:What Role Does the Project Plan Play in Agile Development?;Wrike 專案管理指南 FAQ。
- **抓取**:WebFetch 成功。

**重點**
- 敏捷專案**仍然需要計畫**,只是計畫是「活文件」(living document),會隨專案進展更新。
- **前置規劃**:定願景和需求、指派成員、做時間/預算/範圍的高層級估算;決定要幾個衝刺(sprint)、每個多長、各交付什麼。
- **只有第一個衝刺要詳細規劃**,之後每個衝刺在前一個結束後,依學到的東西再規劃。
- 敏捷不是不規劃:每個衝刺都要仔細規劃,而且每次迭代都要產出可運作的成果。
- 每輪的回饋(包括客戶意見)會影響下一輪計畫。
- **實務建議**:選一個框架(Scrum 或 Kanban);組跨職能團隊、角色明確;用產品路線圖(roadmap)和待辦清單(backlog)定義需求;短衝刺交付;每日站會和回顧;依回饋持續更新計畫。

**課程為什麼連這個**:1.11「項目規劃」:課文說「以為敏捷不用計畫是誤解,敏捷只是改成圍繞衝刺來規劃」,並請學生參閱這篇。

**對作業的用處**
- **AT2「含里程碑的時間表」**:把第 8–12 週規劃成幾個衝刺,每個衝刺都有可展示的成果;第一個衝刺寫細,後面寫到高層級即可,但要說明會依回饋調整。
- **AT1 週報**:可以對應衝刺進度來寫。

---

## 17. Oxford Languages(M352282#18)⚪

- **URL**:https://languages.oup.com/google-dictionary-en/
- **抓取**:WebFetch 成功。
- **一行**:Oxford Languages 說明自己是 Google 英文字典的資料來源(超過 35 萬個詞與片語、以真實語料為依據、俚語和冒犯性詞彙會加標示、例句取自真實來源)。課程在 1.13「企業數據科學/分析方法論」引用「research」的字典定義(名詞:為確立事實、得出新結論而對材料與來源做系統性調查;動詞:系統性地調查),這個連結只是標出處。

---

## 18. 澳大利亞卓越研究 Excellence in Research for Australia (ERA)(M352282#18)✅

- **URL**:https://www.arc.gov.au/evaluating-research/new-approach-research-evaluation
- **實際標題/來源**:A new approach to research evaluation — The ARC's Research Insights Capability;Australian Research Council(ARC,澳洲研究理事會)。
- **抓取**:WebFetch 兩次逾時、本機 curl 解析不到網域;用 Claude 內建瀏覽器讀到。另外讀了同站的 ERA 介紹頁,以及 ARC Data Portal 的 ERA 2018 國家報告引言(找「研究」的定義)。

**重點**
- **頁面現況**:ARC 正在開發新的研究評鑑方式,叫「研究洞察能力」(Research Insights Capability),目標是建立理解、肯定卓越、表揚澳洲研究成就。
- **形式**:有彈性、以資料驅動,包括互動式儀表板、深度報告、研究環境現況報告;希望推動好的實務、連結研究界、政府和終端使用者,又不要增加大學太多報告負擔。
- **2025 年諮詢**:7 月到 11 月辦了 50 多場諮詢、收到 30 多份書面意見;已公布回饋摘要和諮詢版框架草案(草案不是最終設計),後續還會再諮詢。
- **ERA 的歷史**:2010 年辦第一輪(2011 年初公布結果),之後 2012、2015、2018 年各辦一次;2023 年那輪沒有舉行,ERA 在 2023 年由教育部長停辦,ERA 期刊清單也已失效;配套的 Engagement and Impact(EI)評估同樣停止。歷史結果仍可在 ARC Data Portal 查詢。
- **ERA 原本的目標**:推動各領域研究卓越、提供大學研究表現的資訊給各方做決策、向政府和大眾證明研究品質、讓澳洲大學之間以及和國際標準比較。
- ⚠️ **課程說點這個連結可以看 ARC 對「研究」更完整的定義,但這頁現在已經沒有定義了。** 定義可在 ERA 2018 國家報告引言找到(https://dataportal.arc.gov.au/ERA/NationalReport/2018/pages/introduction/index.html),意思是:**研究＝創造新知識,和/或用新穎、有創意的方式運用既有知識,產生新的概念、方法、發明與理解**;整理、分析前人研究,只有在「新穎且有創意」的範圍內才算研究。ERA 要求送審的成果都要符合這個定義。

**課程為什麼連這個**:1.13「企業數據科學/分析方法論」:先給 Oxford 字典的「research」定義,再談命題知識(propositional knowledge,也就是關於事實的知識),然後請學生看 ARC 對研究更完整的定義。

**對作業的用處**
- **AT2 分析目標和任務**(呼應 1.15.1「研究問題和技術目標」):用 ERA 定義檢查專案的研究成分——是產生新知識,還是用新方法運用既有知識?
- **AT2 HD**:要談「前沿 AI」和「前沿基準方法」,可以用這個定義說明創新在哪裡。
- **AT2 背景**:文獻回顧要做到有新的整合觀點,不只是摘要堆疊。

---

## 19. 《澳大利亞數據戰略》(M352282#4)🟡

- **URL**:https://ausdatastrategy.pmc.gov.au/ → 301 轉到 https://www.finance.gov.au/publications/strategy/australian-data-strategy → 再被轉到財政部「Whole of government data governance groups」頁(只介紹政府資料治理組織,**沒有策略內容**)。
- **抓取**:WebFetch 對 finance.gov.au 逾時、本機 curl 解析不到網域;內建瀏覽器跟著轉址只看到上述治理組織頁;官方 PDF 在瀏覽器裡被當成下載檔,沒有讀到。改用:澳洲政府架構網站(Australian Government Architecture,https://architecture.digital.gov.au/strategy/australian-data-strategy,官方)＋CyberDaily 發布當天的新聞(2021-12-14)＋搜尋結果中官方 PDF 的摘錄。
- **缺口**:策略全文(PDF)沒有逐頁讀過;以下是官方摘要頁＋新聞報導的內容。

**重點**
- 澳洲**第一份**國家資料策略,2021-12-14 由聯邦政府發布,總理內閣部(PM&C)負責;背景是 COVID-19 期間政府運用公私資料因應衝擊。
- **願景**:2030 年成為現代化、資料驅動的社會,把公部門資料當成未來經濟的重要動力。
- **三大主題**:(1)**最大化資料價值**:資料的經濟和社會價值、用來處理優先議題、安全分享的好處;(2)**信任與保護**:資料安全、保護澳洲人的資料、整個資料生命週期的倫理使用框架;(3)**促成資料使用**:能力、法規、資料管理與整合、國際參與。
- **政府承諾**:在安全、合法、合乎倫理時開放資料;建立讓資料更好用的基礎設施;投資公務體系(APS)的資料成熟度與技能,落實「資料可用性與透明度計畫」(Data Availability and Transparency Scheme)。
- **配套**:一份會持續更新的行動計畫(Action Plan);要和隱私法(Privacy Act 1988)、資訊自由法(FOI Act 1982)、資料可用性與透明度法案、消費者資料權(Consumer Data Right)等既有法規政策對齊。
- **時程與現況**:策略本身看到 2025 年,之後檢討再訂通往 2030 年的新策略。⚠️ **2023-12-15 已被「資料與數位政府策略」(Data and Digital Government Strategy)取代**,官方標為封存(archived),只供參考。

**課程為什麼連這個**:1.2「大數據」:舉各國重視大數據為例,引用了這份策略的願景句。

**對作業的用處**
- **AT2 背景**:如果主題跟澳洲或政府資料有關,可以引用作政策脈絡;但要註明它已被 2023 年新策略取代,引用新版比較穩。
- 「信任與保護」主題 → **AT2 風險管理**的隱私與倫理段落可以參考。

---

## 20. 數據質量(M352282#4)✅

- **URL**:https://baike.baidu.com/item/%E6%95%B0%E6%8D%AE%E8%B4%A8%E9%87%8F(課程連結後面另帶 `?fromModule=lemma_search-box`)
- **實際標題**:數據質量_百度百科
- **抓取**:WebFetch 與 curl 被擋(403);用 Claude 內建瀏覽器開啟讀取。

**重點**
- **定義**:在業務情境下,資料符合使用者用途、能滿足特定業務需求的程度。這是**相對的概念**,同一份資料在不同情境下品質評價可能不同;資料品質必須**可以量測**,轉成可理解、可重複比較的數字。
- **評估維度**:準確性、完整性、一致性、時效性等;電腦科學的定義另外列了正確性、適時性、精確性、完備性、相關性、可存取性。
- **歷史**:1957 年就有「垃圾進、垃圾出」(Garbage In, Garbage Out)的警告;1988 年 MIT 推出全面資料品質管理計畫(TDQM);2001 年美國通過資料品質法案;國際標準有 ISO 8000 系列。
- **為什麼重要**:資料品質是可靠營運、分析和 AI 的基礎;品質差 → 錯誤洞察、錯誤決策、法規或聲譽風險、大量修錯工作。
- **例子**:病患血壓記錯可能誤診;缺庫存資訊導致訂單出錯;不同資料庫裡同一商品的名稱或編碼不一致;股票交易資料延遲導致投資判斷失誤。
- **改善六步**:訂出符合業務需求的資料標準 → 評估現有資料找出落差 → 清理(去重複、修錯、統一格式)→ 自動化驗證規則 → 建立資料治理(指派資料管理員 data steward)→ 持續監控(儀表板、警示)。
- **常見挑戰**:資料孤島、人工輸入錯誤、舊系統沒有內建品質控管、缺乏治理造成不一致和重複。

**課程為什麼連這個**:1.2「大數據」講五個 V 的「真實性」(Veracity)時連到這個條目:收集到的資料品質可能差很多,會影響分析的準確度。

**對作業的用處**
- **AT2 資料與資源**:針對選定的資料集逐項評估品質(缺值、一致性、時效性);HD 要講資料特徵、分布、相關性,可以加一段資料品質稽核(data quality audit,也就是 CRISP-DM「資料理解」階段的工作)。
- **AT2 風險管理**:把資料品質列為風險並寫對策。
- **AT3 實驗/資料介面**:把清理步驟和清理前後的差異呈現出來。
- ⚠️ 百度百科不建議當學術引用。

---

## 21. 參考文獻草稿(APA 7,交件前請照 UTS APA 指南再核對一次)

> 只列適合放進學術報告的來源。百度百科(#4、#13、#20)、工具型連結(#1、#3、#17)沒有列入。

- Abramov, J. (2019, December 31). *An agile framework for AI projects*. Towards Data Science (TDS Archive), Medium. https://medium.com/data-science/an-agile-framework-for-ai-projects-6b5a1bb41ce4
- AI Consulting Group. (n.d.). *15 tips & questions for requirements gathering on data & AI projects*. https://www.aiconsultinggroup.com.au/15-tips-questions-for-requirements-gathering-on-data-ai-projects/
- Association for Project Management. (n.d.). *10 key principles of stakeholder engagement*. https://www.apm.org.uk/resources/find-a-resource/stakeholder-engagement/key-principles
- Australian Government. (2021). *Australian data strategy*. Department of the Prime Minister and Cabinet.(原網址 https://ausdatastrategy.pmc.gov.au/ 已轉址;2023-12-15 已被 Data and Digital Government Strategy 取代)
- Australian Research Council. (n.d.). *ERA 2018 national report: Introduction*. https://dataportal.arc.gov.au/ERA/NationalReport/2018/pages/introduction/index.html
- Data Science Process Alliance. (n.d.). *What is TDSP?* https://www.datascience-pm.com/tdsp
- Deshmukh, O. (2019, August 22). *How can you convert a business problem into a data problem? A successful data science leader's guide*. Analytics Vidhya. https://www.analyticsvidhya.com/blog/2019/08/data-science-leader-how-effectively-transition-business-requirements-data-driven-solutions/
- Mayo, M. (2016, March 9). *The data science process, rediscovered*. KDnuggets. https://www.kdnuggets.com/2016/03/data-science-process-rediscovered.html
- Mind Tools. (2025, April 10). *Stakeholder analysis*. https://www.mindtools.com/aol0rms/stakeholder-analysis/
- Taylor, J. (2017, January 18). *Four problems in using CRISP-DM and how to fix them*. KDnuggets. https://www.kdnuggets.com/2017/01/four-problems-crisp-dm-fix.html
- Treadwell, T., Leach, E., & Ashcraft, D. (2024, December 4). *Tuckman's stages of group development*. West Chester University CORAL. https://www.wcupa.edu/coral/tuckmanStagesGroupDelvelopment.aspx
- Walch, K. (2020, January 19). *Why agile methodologies miss the mark for AI & ML projects*. Forbes.(Cognitive World 轉載:https://cognitiveworld.com/articles/2020/5/16/why-agile-methodologies-miss-the-mark-for-ai-amp-ml-projects)
- Wrike. (n.d.). *What role does the project plan play in agile development?* https://www.wrike.com/project-management-guide/faq/what-role-does-the-project-plan-play-in-agile-development
- (iunera 訪談文沒有日期,署名 Dhanhyaa,受訪者 Christos Hadjinikolis;要引用時寫 n.d.。)
