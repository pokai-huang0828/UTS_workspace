# review_analysis:評論分析(試跑)

這個資料夾放「讓 AI 讀住客評論」這一塊的資料、程式和紀錄。結構和 `model_training/` 一樣。

```
review_analysis/
  README.md                 這一頁
  data/
    DATA_MANIFEST.md         資料從哪來、怎麼抽的、排除了什麼
    sample_stats.json        抽樣時算的統計(只有彙總數字)
    sample_50.csv            抽出的 50 條評論(含原文)          ← 只留本機
    sample_50_input.csv      給 AI 讀的版本(只有編號和原文)    ← 只留本機
  src/
    prompt_aspect_v1.md      給 AI 的閱讀規則(7 個方面、4 種標籤)
    01_sample.py             抽 50 條(規則寫死、種子 42)
    02_keyword_baseline.py   對照組:最簡單的關鍵字法
    03_compare.py            比對 Claude、GPT、關鍵字法三邊
  runs/
    run_2026-11-21_pilot50/  這一次試跑的紀錄和結果
      REPORT.md              白話報告
      agreement.json         三邊比對的彙總數字
      aspect_counts.csv      每個方面被標成好評/負評的條數
      cost_estimate.json     全部評論都讀一次大概多少錢(粗估)
      labels_*.json          每一條的標籤                       ← 只留本機
      *_local.*              含原文或逐條內容的檔                ← 只留本機
```

## 為什麼有些檔只留本機

這個 repo 是公開的。評論原文、評論編號對應的逐條標註,不上傳。上傳的只有彙總數字、程式和規則。

## 怎麼重跑

在 repo 根目錄:

```
python "Innovation Studio/review_analysis/src/01_sample.py"
python "Innovation Studio/review_analysis/src/02_keyword_baseline.py"
python "Innovation Studio/review_analysis/src/03_compare.py"
```

- `01_sample.py` 要讀 `scratchpad/insideairbnb_sydney/2026-09-16/data/reviews.csv.gz`(230 MB,沒有複製進來)和 `model_training/data/` 裡的房源清單。
- 兩個 AI 的標註不是程式自動呼叫的:Claude 是用 Claude Code 的分身讀,GPT 是用 Codex 指令讀,兩邊拿到同一份規則和同一份 50 條。之後要自動化,需要 API 金鑰,現在沒有。
