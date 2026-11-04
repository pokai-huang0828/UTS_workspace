# 即時資料來源核對(2026-11-04)

> Kenny 貼了別的 AI 整理的「即時資料來源」清單(3 張圖),隊友提出「公交服務可靠性預警系統」→ 派 1 個 sonnet 助手實際呼叫接口、讀官方文件與條款(沒註冊、沒用任何帳密)。樣本回應存在 session scratchpad `realtime/`(不進 repo)。

## 結論先看

- **香港巴士(九巴 KMB/LWB、城巴 Citybus)到站預計時間**:不用金鑰、現在就回 200、約每 1 分鐘更新;DATA.GOV.HK 條款「both commercial and non-commercial purposes on a free-of-charge basis」,要清楚註明來源、資料「AS IS」。**沒有歷史檔,要自己定時抓。**
- **香港官方時刻表(GTFS)**:<https://static.data.gov.hk/td/pt-headway-en/gtfs.zip>(13.7 MB,檔案日期 2026-11-02,交通署「Regular/Specified schedule data of public transport services」,約每兩週更新),含 `frequencies.txt`、`stop_times.txt`、`trips`、`routes`、`stops`、`calendar`。可以當「規定班距」基準。⚠️ 還沒確認有沒有涵蓋九巴路線、`stop_times` 是逐班時刻還是班距制。→ ✅ **同日指揮官下載確認**:`agency.txt` 有 KMB;九巴 578 個路線號中 396 個在 `frequencies.txt` 有分時段規定班距(`headway_secs`,例:1A 線 7–20 分鐘),也就是班距制(按 `route_id` 記錄算是 783 筆中 459 筆;同一路線號的變體會分成多筆)。
- **哪裡都沒有「實際到站」紀錄**(九巴、城巴、交通署、新加坡都沒有)→「延誤/可靠度」要靠反覆抓預計到站時間自己推算:班距過大(長時間等車)、串車(兩班擠在一起)、預計時間突然跳動。
- **新加坡 LTA DataMall**:要申請 AccountKey;Bus Arrival 每 20 秒更新,每班車有 `EstimatedArrival`、`Monitored`(1 = 依車輛定位、0 = 依時刻表)、`Load`(SEA/SDA/LSD 擁擠度)、`Type`、經緯度;Singapore Open Data Licence 可商業與非商業使用、要醒目註明來源;另有每月各站上下車人數、OD、`Bus Routes` 的規定班次頻率(例如 `AM_Peak_Freq` = 「14-17」分鐘)。免費額度沒寫明。

## 逐項

| 來源 | 現在能用 | 金鑰 | 更新頻率 | 重點欄位 | 限制 | 條款 | 歷史資料 | 風險 |
|---|---|---|---|---|---|---|---|---|
| 九巴 KMB/LWB ETA(data.etabus.gov.hk) | ✅ `/route/`、`/stop-eta/<stop>` 200 | 不用 | 約 1 分鐘 | route、dir、seq、eta、rmk、data_timestamp | 沒寫;`Cache-Control: max-age=300`(路線清單) | DATA.GOV.HK(可商用,註明來源) | 要自己抓 | 每站只給最近 3 班;`/route-stop` 用 HEAD 回 403,要用 GET 再測 |
| 城巴 Citybus v2(rt.data.gov.hk) | ✅ `/route/ctb`、`/eta/CTB/002403/1` 200 | 不用 | 約 1 分鐘 | 同上 | 沒寫 | 同上 | 要自己抓 | — |
| 新大嶼山巴士 NLB、專線小巴 GMB | ❓ 沒確認 | — | — | — | — | — | — | NLB 回空清單、GMB 猜的網址回 422 |
| 香港天文台(HKO)天氣 | ✅ `rhrread` 200 | 不用 | 約每小時 | 各站氣溫、雨量、濕度 | 沒寫 | 同上 | 要自己抓 | 不是真正即時 |
| 雪梨 TfNSW Open Data Hub | ❌ 401 | 要(註冊後建 API token) | Trip updates 約 10–15 秒(論壇說法) | — | 沒寫 | 資料頁寫 Creative Commons Attribution | 要自己抓 | 免費與額度沒確認 |
| 新加坡 LTA DataMall | 沒測(要金鑰) | 要 | 20 秒 | 見上 | 沒寫 | Singapore Open Data Licence | 每月上下車人數/OD(下載連結 15 分鐘失效);規定班次頻率 | 收班時沒有回應 |
| Xotelo 酒店房價 | ✅ `/api/rates` 200(Trip.com、Booking、Agoda、Vio 美元價) | 不用 | 查詢當下 | 各平台房價、`/heatmap` | 沒寫 | **沒有條款頁**,只寫「based on TripAdvisor」 | heatmap 有價格歷史 | 個人開發的非官方接口;`/api/search` 只給 RapidAPI |
| SerpApi Google Hotels | 沒測 | 要 | — | — | 免費 250 次/月、50 次/小時 | 沒有學術方案 | 要自己抓 | — |
| Makcorps | 沒測 | 要 | — | — | 搜尋結果說 30 次示範、付費 $350/月起(未核實) | — | — | 未核實 |
| Hotelbeds | 沒測 | 要 | — | — | 測試金鑰 50 次/天 | — | — | 只有測試環境 |
| 澳洲電力市場 AEMO NEMWeb | ✅ `/Reports/Current/` 200 | 不用 | 5 分鐘(zip/CSV) | 電價、用電需求 | 沒寫 | 「general permission… for any purpose, but only with accurate and appropriate attribution」(搜尋摘要) | 有 Data_Archive | 舊檔說明寫不供商業用途 |
| Open-Meteo 天氣 | ✅ 200 | 不用 | 15 分鐘步長(沒測) | 氣溫、風 | 600/分、5,000/時、10,000/天、30 萬/月 | CC BY 4.0;免費版限非商業 | Archive API(沒測) | — |
| OpenSky 航班位置 | ✅ 200 但雪梨範圍 `states: null` | 匿名可用(2025-03 後新帳號要 OAuth2) | 10 秒 | state vectors | 匿名 400 點/天 | 文件頁沒有條款 | 匿名只有最新 | 額度容易用完 |
| OpenAQ v3 空氣品質 | ❌ 401 | 要(免費註冊) | — | — | 60/分、2,000/時 | 要註明來源 | — | — |

- 澳洲氣象局 BOM、加密貨幣、股票:沒查。
- 大陸能不能連 data.gov.hk、LTA:沒測。
