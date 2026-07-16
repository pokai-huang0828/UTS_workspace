# handoff — session 交接(append-only;新 session 只讀最後一個 entry)

---

## 2026-07-16 · fable skill 移植 + Codex 升級(本 entry 同時總結 7/06–7/16 的課程作業脈絡)

### 一、這台環境現在的樣子(實查過,可直接信)

| 項目 | 狀態 |
|------|------|
| 治理框架 | `.claude/skills/frugal-fable/`(`/frugal-fable` 可載入;2026-07-16 自 fable 改名)= VMX 移植的指揮官手冊 + Agent×Codex 兩腦驗證架構;根目錄 CLAUDE.md 已路由 |
| Codex CLI | **0.144.5,model `gpt-5.6-sol`,effort xhigh**(config `~/.codex/config.toml`,備份 `.bak.2026-07-16`)。smoke test EXIT=0(2026-07-16) |
| Codex 陷阱 | 裸名 `gpt-5.6` 在 ChatGPT 帳號下 400;5.6 系列 = `-sol`(旗艦)/`-terra`/`-luna`。駕駛配方(PowerShell tool + stdin + `-o` 落檔 + read-only)見 `.claude/skills/frugal-fable/references/codex-collab.md` |
| git | main = `6978470`,全部已 push(github.com/pokai-huang0828/UTS_workspace);Kenny 靠 push main 跨裝置追蹤,**成果完成就 commit+push** |
| Kenny 偏好 | 回覆一律繁體中文(memory 已存);交付要附證據(R-完成);發文/送出類動作 Kenny 自己做,agent 只備好內容 |

### 二、課程現況(421104 企業 AI,Session 4 2026)

- **A1(15%,7/12 截止)**:CBA 案例報告已定稿於 `Artificial Intelligence for Enterprises/Assessment1/Huang_26254793_421104_Assessment1.docx`(+PDF)。730 中文字/863 Word 計法、APA 7、目錄已更新、對齊五項 rubric「優異」要件、數字全數對過公開來源。7/11 已備妥交件;⚠️假設:Kenny 已於期限內上傳,未向我確認過。
- **接下來的截止日**:A2a **7/26**(監督式學習 coding,資料集課程提供)→ A2b **8/2**(非監督)→ A3 **8/17**(AI 路線圖)。
- **A3 重要策略**:與 A1 用**同一案例(CBA)**;A1 的三軸框架(效率/速度/風險)、IBISWorld K6221A 與 CBA FY25 數據(存於 `Foundation Studio/CBA_Report/data/`)可直接沿用擴寫。
- **Unit 1 參與狀態**(7/10 用 Chrome 逐頁實查):所有內嵌思考練習已發 ✅(1.1/1.1.1/1.1.3/1.1.4/1.2/1.3/1.3.1/1.3.2)、1.1.2 與 1.4 討論區主貼已發 ✅。**缺**:①「認識你的同學」= 必修投寄,未發(草稿已擬,只差 Kenny 填興趣愛好);②1.5 未發問(問題已擬好);③1.1.2 的「回覆兩位同學」寫在自己主貼內,建議補成真正的 threaded 回覆。三者內容都在 7/10 前後的 session 訊息裡,Kenny 說「那些不用」= 他自己決定要不要貼,**不要催**。
- **之後的必修投寄討論**(到該週要主動提醒):3.2.4 混淆矩陣、3.3.1 理解文本、4.2.1 趨勢分析、4.2.4 快速塗鴉、5.1.2 Slim Jims。
- **Zoom**:每週兩場同內容(李春平/管濟偉),北京時間 19:00;週五場擬改週三,**以 Canvas 公告為準**(行事曆不可靠)。老師明示:格式錯扣分、用 Word 不用 WPS、多用 UTS Library、遲交寬限 3 個自然日。

### 三、待辦(下個 session 的合理起點)

1. **A2a(7/26)是下一個硬截止**:先去 Canvas 讀題目與資料集、看 A3 示例一/二,規劃 Python(監督式學習)作業;Kenny 是 coder,重點在符合 rubric 與概念正確。
2. Unit 2(資料/統計/視覺化)的內嵌練習與 2.2.2、2.7 討論——照 Unit 1 模式協助擬答。
3. 若 Kenny 提「認識你的同學」:草稿在,只差興趣愛好一句。
4. fable skill 尚未在實戰任務中全流程走過(派工→Codex 複核)——A2a 是好機會(程式產出 → Codex read-only 驗證)。

### 四、本 session 教訓(值得延續的做法)

- 型號/工具報錯 → 照 R-漂移:實查(撈 CLI 二進位的型號表:`grep -oaE "gpt-5[a-z0-9.\-]*" codex.exe | sort -u`)、更新實查表、附日期,不瞎猜重試。
- Canvas 內嵌練習(Atomic Discussions iframe)get_page_text 讀不到,要**截圖**;頁面有影片時截圖會 timeout,等 6–8 秒重試或開新分頁。
- Canvas 模組頁(/modules)會顯示每項「已查看/投寄」完成狀態,是盤點參與度的最快入口。
