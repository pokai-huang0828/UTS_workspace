# 外部參考檔下載紀錄(2026-11-17)

> Kenny 2026-11-17 同意下載(「好,下載 14 個」)。清單來自隊友鹤舞的「悉尼 Airbnb 数据缺口补充与下载清单」;哪些要下載的判斷在 `teammate_download_list_check_2026-11-17.md` 表 1。
> **檔案放在 `Innovation Studio/refs/external_2026-11-17/`,只留本機、不進版控**(第三方的 PDF 與 Excel;`.gitignore` 已加)。換一台電腦要用,照下面的網址重抓,再對 sha256。
> ⚠️ **內容還沒核對。** 這裡只確認了「檔案抓到了、大小對、開頭是 PDF 或 Excel 的格式」。隊友清單裡寫的數字(例如保險 A$525、市政費 A$970.72、建材 3.7%)都還沒有人翻開檔案對過,**先不要引用**。

## 結果

14 個都抓到了:12 個 PDF、2 個 Excel,合計 31,248,786 位元組(約 29.8 MB)。

| 編號 | 本機檔名 | 大小(位元組 / MB) | 格式檢查 | 怎麼抓的 | sha256 前 16 碼 | 補我們哪個缺口 |
|---|---|---|---|---|---|---|
| 1.01 | `1.01_AER_final_determination_DMO_2026-27.pdf` | 4,212,410 / 4.02 | PDF | Chrome | 8c062224dbfc43e3 | 電費最終版(優先) |
| 1.01 | `1.01_AER_information_kit_DMO_2026-27.pdf` | 3,859,233 / 3.68 | PDF | Chrome | 386e4b434c6bae59 | 電費最終版(優先) |
| 1.02 | `1.02_IPART_gas_data_appendix_2024-25.xlsx` | 2,487,822 / 2.37 | Excel | Chrome | 01b3b57200f2508a | 瓦斯年帳單(優先) |
| 1.03 | `1.03_Archicentre_CostGuide_2026.pdf` | 873,259 / 0.83 | PDF | curl | d29a106ea59f8c31 | 裝修(次要) |
| 1.04 | `1.04_MartinaHayes_Sydney_Renovation_Cost_2026.pdf` | 995,850 / 0.95 | PDF | curl | e573db4796f8ddbe | 廚房浴室裝修(次要) |
| 1.05 | `1.05_ABS_PPI_Table18_sep_2026.xlsx` | 195,616 / 0.19 | Excel | curl | 4ce2eb3a35b95470 | 建材價格指數(次要) |
| 1.06 | `1.06_Vivin_furniture_packages_2025.pdf` | 7,868,221 / 7.50 | PDF | curl | cd054cb6f0629b48 | 家具套裝(次要) |
| 1.07 | `1.07_TerriScheer_holiday_rental_insurance.pdf` | 392,565 / 0.37 | PDF | curl(伺服器送來是 gzip 壓縮的 214,915 位元組,已解開) | 9464cc3864c4fb21 | 短租保險(優先) |
| 1.08 | `1.08_amaysim_home_internet_CIS.pdf` | 132,144 / 0.13 | PDF | curl | 15e73531a1aed5f2 | 網路月費(優先) |
| 1.09 | `1.09_IPART_North_Sydney_final_report_2026-27.pdf` | 1,834,899 / 1.75 | PDF | Chrome | 36c93afb0fa42730 | 市政費(優先) |
| 1.11 | `1.11_SQM_vacancy_rates_october_2026.pdf` | 792,325 / 0.76 | PDF | curl | 20c6a2269e228a90 | 長租對照 |
| 1.12 | `1.12_Cotality_housing_chart_pack_2026-11.pdf` | 4,833,826 / 4.61 | PDF | curl | 9faaf8de0edef8d8 | 長租對照 |
| 1.14 | `1.14_TRA_ATDD_october_2026.pdf` | 2,583,139 / 2.46 | PDF | curl | 0b25c06afaf5da7f | 淡旺季(優先) |
| 1.15 | `1.15_NSW_STRA_FAQ.pdf` | 187,477 / 0.18 | PDF | curl | 49e93972d62441ab | 短租天數規定(優先) |

- 「格式檢查」= 檔案開頭 4 個位元組:PDF 是 `25504446`(%PDF),Excel 是 `504b0304`。
- 「Chrome」的 4 個:程式(curl)連 aer.gov.au、ipart.nsw.gov.au 都逾時,改用 Kenny 的 Chrome 開官方頁面再下載。下載前在頁面上先問過伺服器,四個網址都回 200,大小和抓到的一樣。
- AER 那一頁(最終決定頁)上還有另外 8 個附件(ACIL Allen 報告、成本評估模型等),**沒有抓**;隊友清單只點名這兩個 PDF。清單說「附件包含成本模型 Excel」,那個 Excel 這次沒抓。

## 來源網址

| 編號 | 網址 |
|---|---|
| 1.01 | https://www.aer.gov.au/system/files/2026-05/AER%20-%20Final%20determination%20-%20Default%20market%20offer%202026%E2%80%9327.pdf |
| 1.01 | https://www.aer.gov.au/system/files/2026-05/Information%20Kit%20-%20Default%20Market%20Offer%20-%202026-27_0.pdf |
| 1.02 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Data-appendix-Monitoring-the-NSW-retail-gas-market-2024-25-November-2025.XLSX |
| 1.03 | https://www.archicentreaustralia.com.au/wp-content/uploads/CostGuide-2026.pdf |
| 1.04 | https://www.martinahayes.com.au/wp-content/uploads/6202YENDYSTSOCNOITAVONER.pdf |
| 1.05 | https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/sep-2026/6427018.xlsx |
| 1.06 | https://vivinfurnishings.com.au/wp-content/uploads/2025/07/Vivin-Furnishings-Just-Furniture-Packages-Brochure-2025_compressed.pdf |
| 1.07 | https://www.terrischeer.com.au/assets/documents/terrischeer/terri-scheer-holiday-rental-insurance-english.pdf |
| 1.08 | https://www.amaysim.com.au/content/dam/amaysim/documents/terms-conditions/Critical-Info-Summary-amaysim-Home-Internet-Plans.pdf |
| 1.09 | https://www.ipart.nsw.gov.au/sites/default/files/cm9_documents/Final-Report-North-Sydney-Council-Special-Variation-and-Minimum-Rate-2026-27-%281%29.PDF |
| 1.11 | https://sqmresearch.com.au/uploads/SQM-National-Vacancy-Rates-October-2026-17-11-2044.pdf |
| 1.12 | https://discover.cotality.com/hubfs/Article-Reports/202611%20Cotality%20Monthly%20Housing%20Chart%20Pack%20-%20November.pdf |
| 1.14 | https://www.tra.gov.au/content/dam/austrade-assets/global/wip/tra/documents/atdd/atdd-october-2026.pdf |
| 1.15 | https://www.planning.nsw.gov.au/sites/default/files/2024-09/faq-short-term-rental-accommodation.pdf |

## 還沒做的

1. **開檔核對數字**:每個檔翻到隊友引用的那一頁,對數字、年度、適用範圍(例如 DMO 是基準用電量算的、家具價格另加 GST、保費是 NSW 新業務)。對過才能寫進簡報或報告。
2. 兩個 Excel 還沒打開看工作表(IPART 瓦斯、ABS Table 18)。
3. 沒抓的:1.10 NSW 租金表、TRA 的 DoTS(都只有「下載入口頁」,要進去挑檔);1.13 RBA 房貸利率(這次題目用不到)。
4. `teammate_download_list_check_2026-11-17.md` 表 3 的 8 處筆記更正還沒改。
