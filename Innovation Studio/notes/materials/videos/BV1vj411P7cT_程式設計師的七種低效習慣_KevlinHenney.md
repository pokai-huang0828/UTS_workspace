# BV1vj411P7cT — Seven Ineffective Coding Habits of Many Programmers(許多程式設計師的七種低效編程習慣,Kevlin Henney)

## 在課程哪裡用到
- 位置:M352282#23 → 單元一 1.17「風險考量」頁末「更多資源」(見 `notes/01_單元一_數據分析項目簡介.md` 的 `## 23.`)
- 頁面寫法:「以下視頻則介紹了一些具有風險的編程方式:許多程序員的七種低效編程習慣」。同頁的「關鍵考量」要求研究程式碼**易懂且正確**:用縮排與空白顯示區塊結構、描述性的方法與變數名稱、蛇形命名(snake_case)、有用的註解。
- 連結(link-video):`https://www.bilibili.com/video/BV1vj411P7cT/`

## 基本資料
| 欄位 | 內容 |
|---|---|
| 原標題 | 🚀 Seven Ineffective Coding Habits of Many Programmers (Kevlin Henney) |
| UP 主 | dailyrain(轉載,copyright=2;簡介只有 YouTube 影片 ID `SUIUZ09mnwM`) |
| 長度 | 54:28(3268 秒),單一分 P |
| 上傳日 | 2023-02-21 |
| 原始場合 | DevTernity 研討會(講台有 DevTernity 標誌) |
| 講者 | Kevlin Henney(《97 Things Every Programmer Should Know》編者 — 演講中有出現各語言版書封) |
| 語言 | 英文演講,投影片多為程式碼與引言 |
| 字幕 | 無(未登入時字幕清單為空) |

## 怎麼看的(方法與限制)
- 命令列被 B 站風控擋,改用內建瀏覽器每 80 秒截一張,再補抓章節標題頁,共 45 張。
- **沒有音訊逐字稿**。七個習慣中,「Unsustainable Spacing」「Underabstraction」「Unencapsulated State」三張標題頁有直接截到;其餘四個(Noisy Code、Lego Naming、Getters and Setters、Uncohesive Tests)是依該段投影片內容與這場演講的公開題綱推定,標為「推定」。第三方演講,用自己的話摘要。

## 內容大綱(依時間)
| 時間 | 段落 | 投影片重點 |
|---|---|---|
| 0:30–3:10 | 開場 | 講者介紹;《97 Things Every Programmer Should Know》多語版本;字典裡 code 的三個意思(給電腦的指令、程式、用來代表其他東西的符號系統 — 尤其是為了保密) |
| 5:50–6:30 | 用 user story 格式定調 | 「身為程式設計師,我想要有效的寫程式習慣,這樣就能少花時間猜程式碼的意思、多花時間寫有意義的程式」 |
| 7:10–13:50 | **1. Noisy Code(雜訊太多的程式碼)**(推定) | 訊噪比(signal-to-noise ratio)的定義;用一段刻意寫得冗長的官腔英文(把一句名言改寫成一大串商業術語)比喻囉嗦的程式;引用 Rob Pike 對**註解**的看法 — 程式清楚、命名好就該自己說明自己,註解沒經過編譯器檢查、改程式後容易過時誤導,也會讓畫面變雜;不必要的依賴(left-pad 惡搞書封「Taking on Needless Dependencies」)、一大段註解比程式還長的例子 |
| 15:10–26:10 | **2. Unsustainable Spacing(難以維持的排版)** | 「Mind the gap」;大多數人排版的方式 vs 人眼閱讀的方式(閱讀是由上往下、窄欄位);乾淨的設計是讓人用最少的力氣取得需要的資訊;程式碼範例:方法參數要嘛全部對齊換行、要嘛整組放一起,**不要跟著很長的方法名稱對齊**(改名就整個要重排,不穩定) |
| 26:30–34:30 | **3. Lego Naming(樂高式命名)**(推定) | 黏著語(agglutination)的定義與超長德文／挪威文單字例子;《A Theory of Objects》書在樂高背景上;漫畫「物件導向程式設計師眼中的世界」(每樣東西都被叫成 XxxManager、XxxController);ConditionChecker 介面;批評在名稱後面硬接 Object、Thing、Component、Part、Manager、Entity、Item 這類聽起來很專業但沒意義的字;.NET 例外名稱一大串都以 Exception 結尾 — 去掉也看得懂 |
| 37:25–40:30 | **4. Underabstraction(抽象化不足)** | 一段 Java 程式的文字雲:最大的字是 public、import、string、return — 都是語言關鍵字,看不到業務領域的詞;Dan North〈Code in the Language of the Domain〉的例子:`portfolioIdsByTraderId.get(trader.getId()).containsKey(portfolio.getId())` 應改寫成讀得懂的領域語言(如「trader 能不能看這個 portfolio」) |
| 41:50–43:10 | **5. Unencapsulated State(狀態未封裝)** | BankAccount 類別直接開放 Balance 的 get／set(畫面背景是鎖鏈)— 任何人都能直接改餘額,物件無法保護自己的規則 |
| 45:50–48:30 | **6. Getters and Setters(濫用 getter／setter)**(推定) | 字典裡 get、set 兩個字有幾十種意思(太模糊);「有 getter 不代表就該有 setter」 |
| 49:50–54:10 | **7. Uncohesive Tests(不內聚的測試)**(推定) | Nat Pryce 與 Steve Freeman:大家都知道 TDD 是測試驅動開發,卻常忽略「驅動」的意義;Stack 類別範例 → 測試寫成規格:「新的 stack 是空的」「空 stack 被查詢頂端或 pop 時要丟例外」「push 之後頂端就是剛放的元素」「多次 pop 的順序和 push 相反」;left-pad 的測試案例一行一句描述行為(紅綠標示通過／失敗) |

## 七個習慣速查
| # | 習慣 | 問題 | 改法 |
|---|---|---|---|
| 1 | Noisy Code 雜訊 | 冗長、重複、過多註解,真正的邏輯被淹沒 | 刪掉沒有資訊量的程式和註解,讓程式自己說明 |
| 2 | Unsustainable Spacing 難維持的排版 | 跟著長名稱對齊、一行塞太寬,改一點就要重排 | 用穩定的縮排(換行後固定縮排),窄欄位好閱讀 |
| 3 | Lego Naming 樂高命名 | 名稱一直往後接 Manager、Object、Impl 等空洞字 | 用精準、簡短、有意義的名稱 |
| 4 | Underabstraction 抽象不足 | 程式碼全是語言細節,看不到業務概念 | 把常用操作包成領域語言的方法／類別 |
| 5 | Unencapsulated State 未封裝狀態 | 物件內部資料任人修改 | 只開放有意義的操作(如存款、提款),不要直接開放 set |
| 6 | Getters and Setters | 反射式地每個欄位都配 get/set | 想清楚哪些資料真的要被讀、哪些不該被改 |
| 7 | Uncohesive Tests 不內聚的測試 | 測試按方法分、名稱看不出在測什麼 | 依「行為」寫測試,測試名稱就是一句規格 |

## 和課程頁面的關係
- 1.17 頁的建議幾乎一一對應:
  - 「用縮排和空白突出區塊結構」↔ 習慣 2(排版)。
  - 「優先使用描述性的方法與變數名稱」↔ 習慣 3、4(命名、領域語言)。
  - 「加有幫助的註解,說明方法意圖」↔ 習慣 1 的提醒:註解要有用、不要重複程式本身、要跟著程式更新。
  - 「應優先在方法之間使用不可變資料結構,避免傳遞可變結構」↔ 習慣 5、6(封裝狀態、不要隨便給 setter)。
  - 「考慮單元測試、迴歸測試、程式碼審查」↔ 習慣 7(用測試描述行為)。
- 注意:講者的例子多是 Java／C# 的物件導向程式,但原則同樣適用 Python 資料分析腳本(例如 pandas 程式也該用有意義的變數名、把重複的清理步驟包成函式)。
- AT 交付若含程式碼(notebook／腳本),可以用上面的速查表當自我檢查清單,也能寫進團隊的程式碼審查規範。
