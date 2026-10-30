# 421048 企業數據分析專案 — IT 運維/雲端/機房側候選題(O1–O5)

> scope IS-T2-ops · 核對日 2026-10-30 · 隊員只用代號(Kenny、隊友 A/B/C)。標記:(未確認)=沒核對到;(推論)=我的判斷;(實算)=我用 pandas 親自算出。
> 「中國大陸可直連?」全部是推論,沒有人在大陸實測。授權欄寫的是原文,找不到就寫未確認。
> 資料結論:**O1 可用有但書 · O2 可用有但書 · O3 可用有但書(Azure 檔案結構不利) · O4 可用有但書(無文字欄) · O5 可用有但書(最重,資料量小)**

## O1 AIOps 日誌異常偵測＋LLM 根因說明(用 Loghub 的 BGL/HDFS 做「告警→證據→說明」)
- **一句話**:從數百萬行系統日誌找出異常時段,並由 LLM 用引用的原始日誌行寫出白話根因與建議動作。
- **業務情境**:企業=有網管中心(NOC, Network Operations Center)的 IT 部門,痛點=告警疲勞、值班人員看不完日誌、事後找根因耗時;成功標準=告警視窗 F1 高於基準、每日誤報數下降、LLM 說明被運維人員評為「可採用」比例(目標值待實驗後訂,不先承諾數字)。
  - BO1 縮短故障定位時間 → AG1 讓值班者 5 分鐘內看到可疑視窗與證據行 → T1 視窗級異常偵測+證據擷取。
  - BO2 減少誤報造成的人力浪費 → AG2 誤報可回饋、可抑制 → T2 回饋標記+閾值調整,報告每日誤報數。
- **資料(2026-10-30 核對)**:

| 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|
| BGL.zip(Loghub) | https://zenodo.org/records/8196385/files/BGL.zip?download=1 | 200(已下載) | zip 57,489,019 B;解壓 BGL.log 743,185,031 B | 4,747,963 行;2005-06-03~2006-01-04(214.7 天);警報行 348,460=7.34%(皆實算) | Zenodo 欄位標 CC BY 4.0;但 README 寫「freely available for research or academic work」,兩者口徑不同 | 否 | 推論:Zenodo 多半可連但慢(未確認) |
| Loghub 紀錄(含 HDFS_v1.zip 177 MB、OpenStack 5 MB) | https://zenodo.org/api/records/8196385 | 200 | HDFS_v1 177 MB(未下載) | README 表:HDFS_v1 11,175,629 行/38.7 小時/有標註;OpenStack 207,820 行/有標註 | 同上 | 否 | 同上 |
| Loghub-2.0(解析模板標註) | https://zenodo.org/api/records/8275861 | 200 | 14 個資料集(HDFS 307 MB、BGL 82 MB…) | 筆數(未確認) | Zenodo 標 CC BY 4.0 | 否 | 同上 |
| Loghub README | https://raw.githubusercontent.com/logpai/loghub/master/README.md | 200 | 6,954 B | — | 見上 | 否 | 推論:raw.githubusercontent 在大陸常不穩 |

- **重要欄位**:BGL 一行=警報標籤(`-`=非警報,其餘如 KERNDTLB/APPSEV=警報類別)、Unix 時間、日期、節點位置(機櫃-中板-節點)、完整時間戳、型別(RAS)、元件(KERNEL/APP…)、等級(INFO/FATAL/ERROR/WARNING/SEVERE/FAILURE)、訊息文字。
- **EDA 可以看什麼**:分布①每日行數極度偏態:215 天有資料,中位數 4,947 行/天、單日最高 381,827(約 77 倍,實算);②警報只佔 7.34%,且前 3 類(KERNDTLB 152,734、KERNSTOR 63,491、APPSEV 49,651)佔警報 76.3%(實算)。
  相關性③等級×警報標籤:FATAL 行 855,195 遠多於警報行 348,460(實算),看「FATAL≠警報」交叉表;④警報爆量日 vs 日誌量暴增日、警報是否集中在特定機櫃/節點(待算)。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 日誌解析成模板 | Drain(ICWS 2017,無 arXiv,連結未核對) | 小型 LLM 少樣本解析(評測見 Loghub-2.0 論文) | 解析/分群準確率 |
| 異常偵測 | 模板計數向量+Isolation Forest;DeepLog 式 LSTM(連結未核對) | LogBERT、LogLLM | 視窗級 P/R/F1、每日誤報數 |
| 根因說明 | 規則/關鍵字範本 | LogPrompt 式提示、RCACopilot 式「檢索相似事故+LLM」 | 人評 1–5 分、與警報標籤一致率、幻覺率 |

  選擇標準:準確度、每千行成本、延遲、可解釋(必須附證據行)、能否本機小模型跑完。前沿文獻(標題已打開核對):Loghub(https://arxiv.org/abs/2008.06448)、Loghub-2.0 評測 "A Large-Scale Evaluation for Log Parsing Techniques: How Far Are We?"(https://arxiv.org/abs/2308.10828)、LogBERT(https://arxiv.org/abs/2103.04475)、LogPrompt(https://arxiv.org/abs/2308.07610)、LogLLM(https://arxiv.org/abs/2411.08561)、RCACopilot(https://arxiv.org/abs/2305.15778)。
- **AT3 系統長什麼樣**:網頁介面(Streamlit/Gradio 類,推論可行):時間軸+節點熱度圖,點異常視窗側欄顯示「LLM 說明+引用的 5 行日誌+相似歷史視窗」。按鈕:「產生根因說明」「建立工單草稿」「標為誤報(回饋)」「匯出事故摘要」。Demo 劇本:①挑一段 6 小時 BGL 視窗,系統標紅並排序;②按「產生根因說明」→ 顯示證據行與建議動作 → 按「建立工單草稿」。
- **4 人分工**:專案管理=C(備援 Kenny);利害關係人管理=A(備援 C);方法論=Kenny(備援 B);業務理解=B(備援 A);軟體工程=Kenny(備援 B)。
  Kenny 做資料管線、模型比較、介面;A 以運維總監視角定義「什麼叫可行動的告警」並審 LLM 說明;B 提供機房值班流程與工單欄位並標註 50–100 個視窗;C 管進度、整合 AT2/AT3 文件、設計 demo 劇本與簡報。**C 的主場:技術面弱**,貢獻在專案管理、報告/簡報、誤報成本與環境社會影響章節。
- **風險與備案**:BGL 是 2005 年超算日誌,不像現代雲;Zenodo 授權口徑不一(學術作業可用,商用部署未確認);4.7M 行丟 LLM 太貴 → 先用模板+異常視窗縮到幾百個再給 LLM。備案:改用 HDFS_v1(有塊級標註)或 OpenStack(5 MB 小檔)。
- **最大缺點**:資料是舊的超算日誌,「真實企業」說服力偏弱,且 LLM 說明沒有標準答案、只能靠人評。

## O2 機房硬碟故障預測 → 預測性維護與備品排程(Backblaze Drive Stats)
- **一句話**:用每日 SMART(硬碟自我監測)讀數預測未來 30 天會壞的碟,並換算成備品採購與換碟排程。
- **業務情境**:企業=管理雲端機房的 IT 部門(以 Backblaze 公開資料代理),痛點=硬碟突發故障造成重建、停機與備品缺貨;成功標準=預警召回率、每日警報量、模擬備品成本(目標值待實驗後訂)。
  - BO1 降低非計畫性硬碟故障 → AG1 在故障前 N 天預警高風險碟 → T1 逐日輸出 Top-k 風險清單。
  - BO2 降低備品庫存成本又不缺料 → AG2 依預測故障量決定備品量與補貨時點 → T2 補貨策略模擬(固定安全庫存 vs 預測驅動)。
- **資料(2026-10-30 核對)**:

| 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|
| 說明頁+下載清單 | https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data | WebFetch 成功取回(未回報碼) | — | 2013 起;Q2 2026:354,415 顆、1,498 故障、31,553,350 drive-days、AFR 1.73%;累計 558,148,607 drive-days/21,609 故障/1.41%(頁面數字,未用原檔重算) | 自訂條款(原文):須標示 Backblaze 為來源、自負使用責任、可賣衍生作品、不可賣資料本身 | 否 | 未確認(推論:可連但不保證) |
| data_Q2_2026.zip | https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q2_2026.zip | 206(Range 讀前 4 MB 成功,匿名) | 2,092,757,685 B;頁面稱解壓 11.7 GB、91 檔 | 一天一檔(例 2026-05-20.csv);僅讀開頭 61,012 列:69 種型號,故障 0(前段樣本,不能代表全體) | 同上 | 否 | 未確認(推論:B2 網域可能慢/不穩) |

  其他季度 zip 約 1.0–2.1 GB(頁面表列 2025 Q1 1.02 GB … 2026 Q2 2.1 GB),專案只需取 4–6 季(約 5–8 GB,推論),全量不要碰。
- **重要欄位**(實際讀 Q2 2026 檔頭,共 197 欄):11 個基本欄=date, serial_number, model, capacity_bytes, failure, datacenter, cluster_id, vault_id, pod_id, pod_slot_num, is_legacy_format;其餘 186 欄=smart_N_normalized/smart_N_raw。每列=一顆碟的一天。有 vault/pod 欄,可做「同機櫃/同批連續故障」分析。
- **EDA 可以看什麼**:分布①故障極端不平衡:Q2 2026 約 0.0047%/碟日(1,498/31,553,350,實算);②各型號 AFR(年化故障率)長尾、SMART raw 欄多零膨脹(推論,待 EDA 驗證)。相關性③SMART 5/187/188/197/198 與「未來 7/14/30 天故障」的關係與領先時間;④型號/容量/使用年數/vault 與故障的關聯。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 30 天內故障預測 | 邏輯迴歸;XGBoost+7 日差分特徵 | TabPFN(表格基礎模型,需下採樣);MOMENT 時間序列基礎模型對 30 日 SMART 序列取嵌入 | PR-AUC、Recall@Top1%、平均提前天數 |
| 備品需求與補貨 | 固定安全庫存規則 | 以預測故障量+不確定度做蒙地卡羅補貨模擬 | 缺料次數、庫存成本、停機小時(皆模擬值) |
| 維護工單文字 | 範本字串 | 本機小 LLM 把風險數字轉成工單/備品建議(必附證據欄位) | 人評可行度、數字捏造率 |

  選擇標準:極度不平衡 → 看 PR-AUC 與 Recall@K,不看 accuracy;按時間切分避免洩漏;模型要能在筆電上跑。前沿文獻(標題已核對):TabPFN(https://arxiv.org/abs/2207.01848)、TabPFN 新版 Nature 論文 "Accurate predictions on small data with a tabular foundation model"(https://doi.org/10.1038/s41586-024-08328-6,Crossref 查到)、MOMENT(https://arxiv.org/abs/2402.03885)、XGBoost(https://arxiv.org/abs/1603.02754)。搜尋另見 Ahmed & Green 2024(Backblaze+存活分析 DeepNet,https://link.springer.com/article/10.1007/s00521-024-10479-6,只看到搜尋結果標題,未打開核對)。
- **AT3 系統長什麼樣**:儀表板:日期滑桿→當日 Top-k 高風險碟(型號、vault、關鍵 SMART、風險分數、不確定度),右側備品模擬(補貨策略切換)。按鈕:「產生換碟工單」「加入備品採購單」「回測此門檻」。Demo:①選一個歷史日期,系統列出 Top-20 並標示事後哪幾顆真的壞了;②拖「警報量上限」滑桿→ 即時顯示召回率與備品成本變化 → 按「匯出採購單」。
- **4 人分工**:專案管理=C(備援 Kenny);利害關係人管理=A(備援 C);方法論=Kenny(備援 B);業務理解=B(備援 A);軟體工程=Kenny(備援 B)。
  Kenny 做特徵、模型、模擬;A 審「警報量上限、換碟 SOP」是否現實;B 提供自家機房備品/換碟流程與成本假設(最關鍵);C 管進度、整理成本與環境(電子廢棄物)章節。**C 的主場:弱**(技術與資料味重),僅能做專案管理、成本情境整理、簡報。
- **風險與備案**:資料太大(單季 2 GB zip、12 GB 解壓)→ 只取故障碟+分層抽樣的健康碟;Backblaze 的碟與 B 的企業機房未必同型(遷移性風險);條款是自訂條款,引用需標來源。備案:縮小到單一型號族群。
- **最大缺點**:故障太稀少且資料量大,筆電處理吃力;且「LLM/前沿 AI」在這題偏邊角,主角其實是表格模型。

## O3 雲端資源用量預測 → 自動擴縮容與成本優化(時間序列基礎模型 vs ARIMA/Prophet)
- **一句話**:預測未來 1–6 小時的 CPU 用量帶(P10–P90),據此決定擴縮容水位,並算出省多少、超載風險多少。
- **業務情境**:企業=跑雲端 VM/容器叢集的 IT 部門,痛點=過度配置浪費錢、尖峰又怕超載違反 SLA;成功標準=回測中超載分鐘數與閒置核心小時同時下降(目標值待回測後訂)。
  - BO1 降低雲端閒置成本 → AG1 依預測水位而非固定閾值配置 → T1 預測+擴縮建議。
  - BO2 避免尖峰超載 → AG2 尖峰前預先擴容 → T2 P90 分位數預測+預警。
- **資料(2026-10-30 核對)**(種子三選一:**主推 Azure V2,備援 Alibaba v2018**,Google cluster data 要 BigQuery/GCP 帳號,不選):

| 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|
| Azure V2 說明 | https://raw.githubusercontent.com/Azure/AzurePublicDataset/master/AzurePublicDatasetV2.md | 200 | 1,947 B | 2,695,548 台 VM、6,687 訂閱、連續 30 天、1,942,780,023 筆 5 分鐘 CPU 讀數;全套 235 GB(壓縮 156 GB)、198 檔(文件數字) | repo LICENSE 原文首行 "Attribution 4.0 International"(CC BY 4.0) | 否 | 推論:raw.githubusercontent 大陸常不穩 |
| vm_cpu_readings-file-1-of-195.csv.gz | https://github.com/Azure/AzurePublicDataset/releases/download/dataset-v2/trace_data_vm_cpu_readings_vm_cpu_readings-file-1-of-195.csv.gz | 302→206(Range 讀 3 MB 成功) | 856,259,637 B/檔 | 前 35,194 列的 timestamp 全是 0 → 依時間排序(推論),單台 VM 的序列散在全部 195 檔 | 同上 | 否 | 推論:GitHub release 在大陸慢且易中斷 |
| 舊官方 blob 網址(vmtable 等) | https://azurepublicdatasetv2.blob.core.windows.net/azurepublicdatasetv2/trace_data/vmtable/vmtable.csv.gz | 此環境經代理回 502 | 未確認 | 未確認 | 同上 | 未確認 | 未確認 |
| Alibaba v2018 說明 | https://raw.githubusercontent.com/alibaba/clusterdata/master/cluster-trace-v2018/trace_2018.md | 200 | machine_usage.tar.gz 1.7 GB(文件);全套 49 GB | 約 4,000 台機器、8 天;取樣間隔(未確認) | **未確認**(LICENSE 檔 404、README 無授權字樣) | 下載連結前有問卷但文件說可不填 | 文件稱另有「Chinese users」下載連結(未打開) |

- **重要欄位**:Azure 讀數檔 5 欄=timestamp、vmid(加密)、min/max/avg CPU%;Alibaba machine_usage=machine_id、time_stamp、cpu_util_percent、mem_util_percent、mem_gps、mkpi、net_in、net_out、disk_io_percent(schema.txt 已讀);machine_meta 有 failure_domain_1/2、cpu_num。
- **EDA 可以看什麼**:分布①CPU 平均值右偏:Azure 檔 1 的 35,194 筆(僅 ts=0)中位數 5.15%、平均 9.68%、最大 99.3%(實算,只是 1 個時間點);②日/週週期與尖峰分布(Alibaba 8 天看日週期,週期需 30 天的 Azure,待算)。相關性③CPU 與記憶體/網路/磁碟 IO(Alibaba 有欄位);④同 failure domain 機器的負載相關、自相關(24 小時滯後)。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| CPU 預測(1–6 h) | 季節性 naive、ARIMA、Prophet(Taylor & Letham,連結未核對) | Chronos、TimesFM、Moirai:零樣本 vs 微調 | MASE、加權分位數損失 WQL、區間涵蓋率 |
| 擴縮決策模擬 | 固定閾值(例:>70% 擴) | 用 P90 預測+預留水位 | 超載分鐘數、閒置核心小時、成本 |
| 容量週報 | 範本 | LLM 把預測+決策轉成白話建議 | 人評 |

  選擇標準:零樣本是否打得過調參的 ARIMA、推論時間、是否給分位數(決策要用)。前沿文獻(標題已核對):Chronos(https://arxiv.org/abs/2403.07815)、TimesFM "A decoder-only foundation model for time-series forecasting"(https://arxiv.org/abs/2310.10688)、Moirai "Unified Training of Universal Time Series Forecasting Transformers"(https://arxiv.org/abs/2402.02592)。
- **AT3 系統長什麼樣**:選機器/叢集→畫歷史+未來 6 小時預測帶,可切換模型(ARIMA/Chronos/TimesFM),成本單價與目標使用率滑桿。按鈕:「套用擴容建議」(輸出 scaling plan 草稿)「回測此策略」「產生週報」。Demo:①挑一台尖峰機器,並排看三個模型誰先預警;②拖成本滑桿 → 顯示省多少錢/超載風險 → 匯出計畫。
- **4 人分工**:專案管理=C(備援 Kenny);利害關係人管理=A(備援 C);方法論=Kenny(備援 B);業務理解=B(備援 A);軟體工程=Kenny(備援 B)。
  Kenny 做資料管線與模型比較;A 定義容量/成本決策規則;B 提供擴縮容與 FinOps(雲端成本管理)實務假設;C 管進度並寫成本與環境(閒置資源→用電/碳排情境)章節。**C 的主場:弱**。
- **風險與備案**:Azure 全套 156 GB 且依時間排序 → 單機做每台 VM 序列幾乎不可行,只能取叢集彙總或少數檔(推論);Alibaba 只有 8 天且授權未確認。A 要下載 GitHub 大檔恐中斷。備案:只用 Alibaba machine_usage 一個子集,或把 Azure 預先彙整成小檔給 A。
- **最大缺點**:資料取得與前處理成本最高(大檔、授權、大陸下載),會吃掉大半開發時間。

## O4 IT 服務台事件工單 Copilot(SLA 逾時預測＋分類/相似事件)
- **一句話**:服務台人員開單後,系統給出 SLA 逾時風險、建議分派群組與相似歷史事件。
- **業務情境**:企業=有 ITSM(IT 服務管理)服務台的公司,痛點=重新分派來回、SLA 逾時被罰、新人查不到類似案例;成功標準=逾時預警 AUC/PR-AUC、重新分派次數下降、相似事件命中率(目標值待實驗後訂)。
  - BO1 降低 SLA 逾時率 → AG1 開單時就標出高風險單並提早升級 → T1 SLA 逾時預測。
  - BO2 降低重新分派 → AG2 第一次就派對群組 → T2 分類+分派建議+相似事件檢索。
- **資料(2026-10-30 核對)**:

| 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|
| UCI #498 資料頁 | https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log | 200 | 83,612 B | 141,712 事件×36 欄、24,918 件事故(頁面+實算);opened_at 2016-02-29~2017-02-16(實算) | CC BY 4.0(頁面原文) | 否 | 推論:UCI 大陸多半可連(未確認) |
| incident_event_log.csv(zip) | https://archive.ics.uci.edu/static/public/498/incident+management+process+enriched+event+log.zip | 200(已下載) | zip 2,400,214 B;CSV 46,212,397 B | 同上 | 同上 | 否 | 同上 |
| HF tasksource/it-support-tickets(文字) | https://huggingface.co/api/datasets/tasksource/it-support-tickets | 200(只打 API,資料頁未開) | parquet 訓練/測試檔(大小未確認) | 2,229 則真實工單文字,人工分 7 類;英/德/葡/西;卡片更新 2026-09-23 | CC BY 4.0(API cardData) | 否(非 gated) | 推論:huggingface.co 大陸常被擋,需鏡像(未核對) |

- **重要欄位**:UCI 每列=事故的一次狀態變更;number、incident_state(New/Active/Awaiting…/Resolved/Closed)、made_sla、priority(impact×urgency)、category/subcategory/u_symptom/cmdb_ci、assignment_group、reassignment_count、reopen_count、opened_at/resolved_at/closed_at、contact_type、location。**全是匿名代號(如 "Category 55"),沒有任何自由文字欄**(實算:無欄位超過 60 字)。注意 reassignment_count、sys_mod_count 會隨事件累積,預測時是資料洩漏。
- **EDA 可以看什麼**:分布①解決時間重尾:開單→解決 中位 22.1 小時、P90 381.5、P99 2,843(n=23,362,實算);②優先序 94.2% 是 Moderate(23,466/24,918),Critical 僅 270;made_sla=False 約 36.6%(以每件最後一筆計,實算)。相關性③重新分派次數(平均 0.94,最多 27)與解決時間/逾時;④逾時與 category、assignment_group(72 組)、location、開單時段的關係(待算)。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| SLA 逾時預測 | 邏輯迴歸、XGBoost(只用開單當下可得欄位) | TabPFN;LSTM 預測式流程監控(深度基準) | AUC、PR-AUC、提前量 |
| 工單分類/分派 | TF-IDF+邏輯迴歸 | BGE-M3 多語嵌入+LLM 少樣本(在 HF 文字集上) | macro-F1、Top-k |
| 相似事件+處置建議 | BM25 檢索 | RAG(檢索增強生成)+LLM 並附引用 | hit@k、人評 |

  選擇標準:不洩漏、多語(中文團隊要能處理)、可在筆電跑。UCI 無文字 → 文字模型只能在 HF 2,229 筆上展示,兩份資料無法互相對應。前沿文獻(標題已核對):TabPFN(https://arxiv.org/abs/2207.01848)、"Predictive Business Process Monitoring with LSTM Neural Networks"(https://arxiv.org/abs/1612.02130)、M3-Embedding/BGE-M3(https://arxiv.org/abs/2402.03216)、RAG(https://arxiv.org/abs/2005.11401)、XGBoost(https://arxiv.org/abs/1603.02754)。
- **AT3 系統長什麼樣**:服務台工作台:分頁 1「重播」按時間重播 UCI 事故,即時顯示逾時機率燈號;分頁 2「新工單」貼入文字→分類、建議分派、3 筆相似案例+建議回覆。按鈕:「接受分派」「升級」「套用建議回覆」「標記建議錯誤(回饋)」。Demo:①重播到一張高風險單,系統提前亮紅並顯示主要原因;②貼一則新工單文字→ 顯示分類+相似案例 → 按「接受分派」。
- **4 人分工**:專案管理=C(備援 Kenny);利害關係人管理=A(備援 C);方法論=Kenny(備援 B);業務理解=B(備援 A);軟體工程=Kenny(備援 B)。
  Kenny 做模型與介面(這題最貼 Kenny「AI＋數據分析優化客訴/產品管理」的目標);A 審 SLA 與升級規則;B 熟 ITSM/ITIL 流程,定義分類與分派規則;C 管進度,並設計回覆範本與使用者測試。**C 的主場:中**(服務台=客戶服務流程、SLA/客訴體驗、回覆話術、使用者測試,與 C 的俱樂部客服經驗相近,推論)。
- **風險與備案**:UCI 無文字、欄位匿名,Copilot 的 LLM 成分單薄;文字集只有 2,229 筆且分 7 大類太粗;HF 對 A 可能連不上。備案:用 LLM 把結構化欄位合成「工單敘述」(必須標明是合成、不能當真實證據),或改用同為合成的 HF 工單集(ameau01/synthetic-it-support-tickets,MIT,內容未核對)。
- **最大缺點**:最核心的 UCI 資料沒有文字,「Copilot」的 LLM 亮點得靠另一個小資料集拼湊,兩者無法對上。

## O5 雲端事故事後檢討(postmortem)→ 根因分類與風險雷達
- **一句話**:把公開的雲端事故報告轉成結構化欄位(根因、觸發、偵測、緩解、影響範圍),再依自家架構給出「哪些事故模式最可能打到我們」的風險排序。
- **業務情境**:企業=依賴公有雲的 IT 部門,痛點=重大事故一再重演、缺乏系統性學習他人教訓;成功標準=欄位抽取 F1、風險排序與專家一致程度(門檻待標註後訂)。
  - BO1 避免重蹈他人事故 → AG1 把公開事故轉成可檢查清單 → T1 LLM 結構化抽取+根因分類。
  - BO2 快速判斷自家暴露度 → AG2 依架構問卷排序風險 → T2 風險雷達打分+理由。
- **資料(2026-10-30 核對)**:

| 檔案/API | 連結 | HTTP | 大小 | 筆數與時間範圍 | 授權 | 要帳號? | 中國大陸可直連? |
|---|---|---|---|---|---|---|---|
| danluu/post-mortems(索引) | https://raw.githubusercontent.com/danluu/post-mortems/master/README.md | 200 | 96,615 B、620 行 | 240 則分類事故(Config Errors 59、Hardware/Power 15、Conflicts 11、Time 5、Database 12、Uncategorized 138,實算);每則=公司+外連原文+1–2 句摘要;年份(推論:約 2009–2026) | **未確認**(LICENSE 檔 404;各原文版權另算) | 否 | 推論:raw.githubusercontent 不穩;外連原文站(AWS 等)未逐一打開 |
| Google Cloud 狀態頁 | https://status.cloud.google.com/incidents.json | 200(含 206) | 251,117 B | **只有 8 則**,begin 2026-02-27~2026-10-20(實算)→ 是近期視窗,不是歷史庫;每則平均約 2 萬字,7/8 含 Root Cause 章節 | 未確認 | 否 | 推論:Google 網域大陸不可直連 |
| VOID(公開事故庫) | https://www.thevoid.community/ | WebFetch 只回傳標題 | 未確認 | 未確認(筆數、下載方式皆未讀到) | 未確認 | 未確認 | 未確認 |

- **重要欄位**:GCP:id、begin/end/created/modified、external_desc、updates[].text(Markdown,含 Summary/Root Cause)、severity(low/medium/high)、status_impact、service_name、affected_products(54 種)、受影響地區。danluu:公司、原文 URL、摘要、分類章節。
- **EDA 可以看什麼**:分布①240 則的根因類別佔比(Uncategorized 佔 57.5%=138/240,要靠 LLM 重標);②公司/雲廠分布與年份分布(需先抽取)。相關性③根因類型×緩解時長(GCP 8 則太少,要補爬;例:2026-10-20 事故內文稱約 6 小時 8 分緩解);④服務/地區×影響面。
- **方法**:

| 子任務 | 基準 | 前沿 AI | 評估指標 |
|---|---|---|---|
| 根因分類/欄位抽取 | 關鍵字+TF-IDF+邏輯迴歸;BERTopic 分群 | LLM 結構化抽取(固定 JSON 欄位,零/少樣本) | macro-F1、欄位 F1(對 100 筆人工標註) |
| 相似事故檢索 | BM25 | 嵌入+RAG | hit@k |
| 風險雷達 | 人工權重評分表 | LLM 依架構描述比對事故模式並寫理由 | 與 A/B 專家排序的 Spearman 相關 |

  選擇標準:抽取是否忠於原文(不捏造)、成本、可重現。前沿文獻(標題已核對):RCACopilot "Automatic Root Cause Analysis via Large Language Models for Cloud Incidents"(https://arxiv.org/abs/2305.15778)、"Recommending Root-Cause and Mitigation Steps for Cloud Incidents using Large Language Models"(https://arxiv.org/abs/2301.03797)、BERTopic(https://arxiv.org/abs/2203.05794)、RAG(https://arxiv.org/abs/2005.11401)。
- **AT3 系統長什麼樣**:左欄填自家架構問卷(雲廠、區域、是否多可用區、變更流程…),中間是風險雷達圖+Top 事故模式,右欄是相似事故卡片(含原文連結與 LLM 摘要)。按鈕:「產生自查清單」「匯出風險報告」「標記抽取錯誤(回饋)」。Demo:①勾選「單一可用區、手動變更」→ 雷達亮出設定錯誤與電力類風險;②點最高風險 → 顯示 3 個相似事故與對應自查項目 → 匯出清單。
- **4 人分工**:專案管理=C(備援 Kenny);利害關係人管理=A(備援 C);方法論=Kenny(備援 B);業務理解=A(備援 B);軟體工程=Kenny(備援 B)。
  Kenny 做爬取、抽取管線、介面;A、B 以運維經驗當「標準答案」人工標註並審風險雷達;C 設計事故影響面/風險矩陣的分類框架,並做部分標註。**C 的主場:中到強**(閱讀長文、風險分類、類比賽事「應變預案」,非技術也能貢獻標註與 taxonomy)。
- **風險與備案**:沒有現成大型、乾淨、授權明確的事故資料集;要自己爬 AWS/Azure/Cloudflare 等公開報告(各站條款與版權未確認),爬取+標註工時大。備案:只用 danluu 的 240 則摘要+手動補 60–100 篇全文,範圍寫明「抽樣」。
- **最大缺點**:資料量小又零散,「特徵、分布、相關性」的統計厚度不足,AT3 容易淪為 LLM 摘要器。

## 沒涵蓋/換掉的種子
- **種子都保留,未換掉**。調整兩處:O1 主資料用原版 Loghub 的 BGL/HDFS(有標註,可做異常偵測),Loghub-2.0 只作解析模板用;O3 三選一改為 Azure V2 為主、Alibaba v2018 為備援(理由:Azure 授權明確但檔案結構不利、Alibaba 單機序列直接但授權未確認、Google 需 GCP 帳號且大陸不可連)。
- 排序(推論,僅供參考):O4 最貼 Kenny 目標但資料有缺;O1、O2 資料最扎實;O5 最適合 C 但資料最薄;O3 取得成本最高。
- **沒涵蓋**:HDFS_v1(177 MB)與 Loghub-2.0 沒下載,只讀 Zenodo/README 數字(HDFS 標註塊數(未確認));Backblaze 只讀 zip 前 4 MB,全量故障比、各型號 AFR、零膨脹都沒算;Azure vmtable/deployments 沒下載,VM 壽命等數字(未確認);Alibaba 資料檔未下載、授權/取樣間隔(未確認);danluu 外連的 240 篇原文與 AWS/Azure/Cloudflare 事後報告頁沒打開;VOID 未確認;TFBEST、Ahmed & Green 2024 只見搜尋結果、DeepLog/Drain/Prophet 無 arXiv 連結都沒核對;大陸可直連性全為推論;Kaggle 類工單資料集與其他 ITSM 公開集沒查;LLM 在這些資料上的實際成效數字一律沒核對。
- 用量:網路請求 29/30 次(curl 類 26、WebFetch 2、WebSearch 1;其中 arXiv 301 重試與 Azure blob 502 各佔 1 次);下載約 68 MB/300 MB。暫存分析檔在 /tmp/claude-0/-home-user-UTS-workspace/f8b006a1-70a9-5566-b25d-ad6e4248c086/scratchpad/ops/。
