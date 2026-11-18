# 外部參考檔下載紀錄(2026-11-18)

> Kenny 2026-11-18 同意下載(「好,下載 2 個」)。來源是 Stanly 的「悉尼 Airbnb 额外数据源推荐」第 3、9 項(整理見 `teammate_stanly_sources_check_2026-11-18.md`)。
> 檔案放在 `Innovation Studio/refs/external_2026-11-18/`,**只留本機、不進版控**(`.gitignore` 已加)。換電腦要用,照下面網址重抓再對 sha256。

## 結果

2 個都抓到了,也開檔看過欄位與日期範圍。

| # | 本機檔名 | 大小(位元組) | 格式 | sha256 前 16 碼 | 來源網址 |
|---|---|---|---|---|---|
| 3 | `3_australian_public_holidays_combined_2021-2025.csv` | 88,999 | CSV(開頭 `ID,D`) | 4126fe21c5c96994 | https://data.gov.au/data/dataset/b1bc6077-dadd-4f61-9f8c-002ab2cdff10/resource/33673aca-0857-42e5-b8f0-9981b4755686/download/australian-public-holidays-combined-2021-2025.csv |
| 9 | `9_ABS_OAD_table11_visitors_by_state_sep_2026.xlsx` | 81,269 | Excel(開頭 `504b0304`) | ecf215355135fe1b | https://www.abs.gov.au/statistics/industry/tourism-and-transport/overseas-arrivals-and-departures-australia/sep-2026/3401011.xlsx |

## 開檔看到的

### 公眾假期 CSV(data.gov.au)

- 資料集名稱:Australian Public Holidays Dates Machine Readable Dataset **[INACTIVE]**(頁面標示不再更新;授權 CC BY 3.0 AU)。資料集裡另有 2014–2025 各年分檔,這次只抓 Stanly 點名的「2021–2025 合併版」。
- 欄位:`ID`、`Date`、`Holiday Name`、`Information`、`More Information`、`Jurisdiction`。
- 532 列;日期 2021-01-01 到 2025-12-31;NSW 65 列(2025 年 12 列,例如 2025-01-01 New Year's Day、2025-01-27 Australia Day、2025-04-18 Good Friday)。
- **沒有 2026、2027 的日期。** 只能拿來對過去的評論月份;未來的假期提醒要用我們 11/14 手查的官方日期。

### ABS 出入境 Table 11(2026 年 9 月那一期)

- 表名:Short-term movement, visitors arriving – state of intended stay: original(短期入境旅客,按打算停留的州,原始值)。入口頁上共有 16 張表與一個全部資料的 zip;這次只抓第 11 張(有 NSW 一欄的那張)。
- 工作表:Index、Data1、Enquiries。Data1 有 10 個序列(NSW、Vic、Qld、SA、WA、Tas、NT、ACT、Other Territories、Total),單位 Number、Original、每月。
- NSW(Series ID A85247916X):1991-01 到 2026-09,共 429 個月。
- 近 15 個月(人):2025-07 257,410;2025-08 293,030;2025-09 256,380;2025-10 284,370;2025-11 325,340;2025-12 389,290;2026-01 272,980;2026-02 367,220;2026-03 314,260;2026-04 242,650;2026-05 225,350;2026-06 200,580;2026-07 247,410;2026-08 289,970;2026-09 255,130。
- 2025 全年:最高 12 月 389,290;最低 6 月 217,640。
- ⚠️ **這是進 NSW 的國際短期旅客人數**:不是雪梨、不是住宿晚數、不含國內旅客。只能看淡旺季的走勢,不能當 Airbnb 入住率。

## 沒做的

- Stanly 清單第 8 個(雪梨機場每月客流)沒下載:要從新聞稿一則一則抄,還沒整理。
- 第 1(短租登記冊 API)、4(車站資料)、11(Ticketmaster)要申請帳號或權限,沒有申請。
- 其餘來源(5、6、7、10、12、13)沒下載;第 6 個的連結是 404。
- 這兩個檔的數字只有主腦用腳本讀過,沒有第二個人核對。
