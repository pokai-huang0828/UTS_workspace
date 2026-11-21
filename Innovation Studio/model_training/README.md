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

## 另外兩群房源(2026-11-21 追加,工單 IS-1121-TRAIN-B)

組長要求房源資料全部都要訓練。第一次訓練(run_01)只涵蓋「整套、1–2 臥、可住 2–4 人、最少 1–7 晚」,另外兩群各用同一套流程再訓練一次:

| 群 | 定義 | 表 | 訓練紀錄 |
|---|---|---|---|
| 整套 1–2 臥(預設,第一次訓練) | 整套、臥室 1–2、可住 2–4 人、最少 1–7 晚、每晚 ≤ 2,000 | `train_table_2026-09.csv`(6,615) | `runs/run_2026-11-21_01/` |
| 獨立房間(`private_room`) | Private room、可住 1–4 人、最少 1–7 晚、每晚 ≤ 2,000;臥室空的補 1 並加旗標 | `train_table_2026-09_private_room.csv`(2,915) | `runs/run_2026-11-21_02_private_room/` |
| 全部整套房(`entire_home_all`) | Entire home/apt 全部、每晚 ≤ 3,000;臥室/人數/最少晚數缺值補中位數並加旗標 | `train_table_2026-09_entire_home_all.csv`(13,685) | `runs/run_2026-11-21_03_entire_home_all/` |

```
python "Innovation Studio/model_training/src/01_build_dataset.py" --group private_room        # 每一步剩幾列會印出來
python "Innovation Studio/model_training/src/01_build_dataset.py" --group entire_home_all
python "Innovation Studio/model_training/src/02_train.py" run_2026-11-21_02_private_room private_room
python "Innovation Studio/model_training/src/02_train.py" run_2026-11-21_03_entire_home_all entire_home_all
python "Innovation Studio/model_training/src/predict_one.py" --group private_room --nb Sydney --bedrooms 1 --acc 2 --beds 1 --baths 1 --amen "Kitchen,Wifi"
```

- 不加 `--group`、不加第二個參數 = 第一次訓練那一群,行為和以前完全一樣(重跑後 metrics、cv_results、learning_curve、feature_importance、error_by_segment、split_summary 與 run_01 逐位元相同)。
- 新增兩群**不做**「時間外驗證(6 月 → 9 月)」和「和舊數字對帳」;另外給一份「全部資料、依房東 5 折」的出袋預測(`predictions_oof.csv`),只是額外的看法,沒用來選模型。
- 各群的白話報告:該 run 資料夾裡的 `REPORT.md`(有一節「和第一次訓練(整套 1–2 臥)比」)。
