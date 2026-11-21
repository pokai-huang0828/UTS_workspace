# model_training:雪梨民宿「參考價」模型的訓練資料夾

這個資料夾放三樣東西:

1. **訓練要用的資料**(`data/`):從 Inside Airbnb 雪梨原始檔整理出來的訓練表。原始檔和整理好的表都只留在本機、不進版控;每個檔的來源、列數、sha256、清洗規則寫在 [data/DATA_MANIFEST.md](data/DATA_MANIFEST.md)。
2. **程式**(`src/`):`common.py`(清洗和特徵,規則照抄 `analysis/sydney/syd_b_positioning.py`)、`01_build_dataset.py`(原始檔 → 訓練表)、`02_train.py`(訓練 + 考試 + 畫圖)、`predict_one.py`(輸入一間房 → 參考價)。
3. **每次訓練的紀錄和結果**(`runs/`):一次一個子資料夾。先看 [runs/run_2026-11-21_01/REPORT.md](runs/run_2026-11-21_01/REPORT.md)(白話報告)。

模型的工作:給一間房「上架前就知道的條件」(區、位置、房型、臥室、人數、床、浴室、最少住幾晚、有哪些設施),猜它一晚的掛牌價。

## 怎麼重跑(在 repo 根目錄)

```
# 0. 把原始檔放進 data/raw/(檔名見 DATA_MANIFEST.md)
python "Innovation Studio/model_training/src/01_build_dataset.py"     # 幾秒;會檢查 6,639 / 6,615 / 6,747 / 821
python "Innovation Studio/model_training/src/02_train.py"             # 24 核約幾分鐘;產出到 runs/run_2026-11-21_01/
python "Innovation Studio/model_training/src/predict_one.py" --nb Sydney --bedrooms 1 --acc 2 --beds 1 --baths 1 --amen "Kitchen,Washer,Wifi"
```

想另開一次訓練不蓋掉舊的:`python .../02_train.py run_<日期>_02`。

需要:python 3.11、scikit-learn 1.4.2、xgboost 3.2.0、lightgbm 4.6.0、pandas 2.1.4、matplotlib 3.7.5、joblib 1.3.2;字型 Microsoft JhengHei。隨機種子固定 42。

## 不進版控的東西

`data/raw/`、`data/processed/`、`runs/**/*.joblib`、`runs/**/predictions_*.csv`(逐房資料)。其餘彙總檔只有統計數字,沒有逐房資料、房東姓名或網址。
