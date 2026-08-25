# Bank X Notebook 拆解 —— `AT3_TeleMarketing.ipynb`

> 2026-08-25 逐 cell 實查。全 77 cell（code 53 / markdown 24），26 個 code cell 已附輸出。

---

## 🔴 最重要的發現：這是一份 **Google Colab** Notebook，不是本機 Notebook

```python
[2]  !pip install ydata-profiling
[5]  from google.colab import drive
[9]  data = read_data(path='/content/drive/MyDrive/TeleMarketing.csv')
```

Notebook metadata 還寫著 `accelerator: GPU`。

### 這代表什麼（好消息）

**先前擔心的 `ydata_profiling` 裝不了，在 Colab 上根本不是問題。**
Colab 每次開機都是乾淨環境，第 2 個 cell 的 `!pip install ydata-profiling` 會自己裝好，
**完全不會碰到你本機被 `pycaret` 鎖住 pandas/numpy/scipy 的問題**。

| | 用 Colab（官方預設） | 改本機跑 |
|---|---|---|
| ydata_profiling | ✅ 自動裝好 | 🔴 要處理版本衝突或開 venv |
| 環境風險 | ✅ 零，動不到你的機器 | ⚠️ 可能弄壞 A2b 環境 |
| GPU | ✅ 免費（房仲情境才需要） | ❌ 看你的顯卡 |
| 要改幾行 | **0 行**（把 CSV 傳到 Google Drive 即可） | **3 處**（拿掉 drive mount、改路徑、處理 pip） |
| 缺點 | 閒置會斷線、要傳檔到 Drive | 檔案都在本地、可版控 |

> 💡 **建議：用 Colab 跑，本機只留 Notebook 副本做版控。** 這是官方設定的路，阻力最小。
> 房仲情境更是非 Colab 不可（172 MB 圖 + CNN 訓練要 GPU）。

---

## 8 個填空 —— 但其實**只有 4 個是必做的**

> ⭐ **關鍵區分**：4 個標了 `Tech Focus Only`，**只有選「技術路徑」才要做**。
> 選商業路徑的話，實際要動手的只有 4 處，而且 3 處是一行的事。

### A. 所有人都要做（4 處）

#### TODO 1 — cell [13]｜補缺失值 · 難度 ⭐（一行）

```python
data["contact"].fillna("Not Applicable", inplace = True)

# TODO 1: fill the null values in variables "month" and "days_of_week" with "Not Applicable"
data["month"]._________
data["day_of_week"]._________
```

上一行已經示範完了，照抄即可。
> 📌 這正是資料偵察報告裡「結構性缺失」那 23,546 筆 —— 對照組沒被打電話，所以沒有月份/星期。

---

#### TODO 2 — cell [30]｜對測試集做同樣的 Label 編碼 · 難度 ⭐（一行）

```python
label_encoder = LabelEncoder()
train_data['response'] = label_encoder.fit_transform(train_data['y'].to_numpy().reshape(-1,1))

# TODO 2: use LabelEncode() function and transform test_data["response"]
test_data['response'] = _____________________
```

> ⚠️ **這裡有個觀念考點**：訓練集用 `fit_transform`，測試集**只能用 `transform`**（不能再 fit）。
> 寫錯不會報錯，但等於資料洩漏。這一點值得在報告裡點出來。

---

#### TODO 3 — cell [46]+[47]｜換成邏輯迴歸再跑一次特徵選擇 · 難度 ⭐⭐（填 3 個參數）

```python
selected_feature_LR = feature_selection_model(dataset=train_data,
                   features=num_features_tfm+num_features_scl+int_features+oh_features,
                   label=_______,
                   model=_____,
                   k=____)
```

上面 cell [45] 已經有隨機森林（`'RF'`）的完整範例，照著改成 `'LR'` 即可。

---

#### 第 4 處 — cell [58]｜幫 GridSearch 加超參數值 · 難度 ⭐（填數字，但會跑很久）

```python
# TODO: add more hyper parameter valus for max_depth and n_estimators
rf_parameters = {'max_depth':[3,5,___],
                 'criterion':['gini', 'entropy'] ,
                 'n_estimators':[100,200,___]
                }
```

> ⚠️ **時間陷阱**：這是 `GridSearchCV(cv=5)`。目前組合數 = 3 × 2 × 3 = 18，×5 折 = **90 次訓練**。
> 每多填一個值組合數就爆增。**填數字很快，等它跑完很慢。**

---

### B. 只有「技術路徑」要做（4 處，全是開放題，沒有填空底線）

| cell | 要求 | 對應 rubric |
|---|---|---|
| **[38]** | 「再加一到兩種特徵選擇方法，並呈現特徵重要性」 | **變數識別 20 分** |
| **[48]** | 「評估前面兩種方法（單變量 + 模型式）選出的特徵，提出訓練該用哪些」 | **變數識別 20 分** |
| **[52]** | 「對上面的模型加更多超參數並迭代，看模型行為變化，選出更好的模型」 | **超參數選擇 20 分** + **模型比較 10 分** |
| **[60]** | 「在 pipeline 裡試 `roc_auc` 以外的指標並比較結果」 | **模型評估與選擇 30 分** |

> 這 4 個沒有標準答案，是要你寫分析。**它們直接對應技術路徑 rubric 的 80/100 分。**

---

## 📊 工作量結論

| | 商業路徑 | 技術路徑 |
|---|---|---|
| 要填的空 | **4 處**（3 處一行 + 1 處填數字） | **8 處**（4 處填空 + 4 處開放分析） |
| 寫程式的時間 | 約 **30 分鐘** | 數小時～數天 |
| 主要工作在哪 | **把結果講成商業故事**（rubric 40 分那項） | **調參、比模型、寫論證** |
| 跑模型的時間 | GridSearch 要等（可調小） | 要跑很多輪 |

> **商業路徑的程式工作量非常小。** rubric 也誠實反映這點：程式碼只佔 30 分，
> 「將結果轉化為商業價值」佔 40 分。**分數在報告裡，不在程式裡。**

---

## 🔍 Notebook 本身的兩個可寫之處（拿來當「未來改進」）

### 1. `duration` 的用法比我原先判斷的更精緻 —— 但仍有問題

Notebook 的「客戶評分」段（cell [62]、[64]）做了一件聰明的事：

```python
# 把 duration 分成 11 個桶
duration_df['buk_duration'] = KBinsDiscretizer(n_bins=11, ...)

# 對每個客戶,模擬「如果通話長度是各種值」時的接受機率
for k, v in duration.items():
    sample_customer['duration'] = duration[k]
    sample_customer['pr'+str(int(k))] = ml_pipe.predict_proba(X=sample_customer)[:,1]

# 加權:通話越短權重越高(短通話成本低)
sample_customer['score'] = sum([200*...pr0 if k==0 else (100-k*2)*...]) / 11
```

**它把 `duration` 當成「可控制的槓桿」（我們打算聊多久），不是「已知的特徵」。**
這是為了同時最佳化**轉換率**與**呼叫中心成本** —— 正好對應題目說的兩個目標。

> ✅ **所以不能簡單說「duration 是洩漏、要刪掉」。** 更準確的說法是：
> **拿 `duration` 直接當預測特徵是洩漏；但把它當成成本模擬的槓桿是合理設計。**
> 在報告裡把這個區分講清楚，是很強的論述。

**但仍然有真正的問題**：對照組（campaign=0）的 `duration` 結構性全為 0，
模型在訓練時會把「duration=0」學成「這是對照組」。這個交互作用 Notebook 沒有處理。

### 2. cell [58] 的 `duration` 被放進 ColumnTransformer **兩次**

```python
prep = ColumnTransformer(
    transformers=[('dur',    num_transformer, ['duration']),                                    # ← 第一次
                  ('scaler', num_scaler, ['age','cons.price.idx','cons.conf.idx','duration']),  # ← 第二次
                  ('encoder',cat_encoder,  cat_features)])
```

`duration` 同時被 PowerTransformer 和 StandardScaler 各處理一次，**產生兩個重複欄位**。

> 這可能是刻意的（兩種尺度都給模型），也可能是筆誤。
> 不論何者，**在報告裡指出來並說明影響**，就是商業路徑「未來改進」（10 分）
> 或技術路徑「變數識別」（20 分）的現成材料。

---

## 完整章節地圖

| cell | 章節 | 內容 |
|---|---|---|
| 0–11 | 實驗 / 針對優惠和呼叫成本的最佳化 | 裝套件、掛 Drive、讀檔、ydata profiling 報告 |
| 12–13 | **資料清洗** | 去重、補缺失值 ← **TODO 1** |
| 14–18 | 資料探索 | countplot / boxplot / distplot 三個繪圖函式 |
| 19–33 | **特徵工程** | 切分、PowerTransform、StandardScaler、LabelEncoder ← **TODO 2**、OneHot |
| 34–36 | 二維視覺化 | t-SNE 降維 |
| 37–48 | **特徵選擇** | 單變量（f_classif）+ 模型式（RF/LR）← **TODO 3**、Tech[38]、Tech[48] |
| 49–52 | 建模 | RandomForest + XGBoost，GridSearch / RandomizedSearch ← Tech[52] |
| 54–60 | **最終流程** | 完整 sklearn Pipeline + RFE + GridSearch，存成 `ml_pipe.joblib` ← 超參數填空、Tech[60] |
| 61–65 | **客戶評分** | duration 分桶 + 成本加權評分，輸出可排序的客戶名單 |
| 66–76 | 分群分析（**可選**） | KMeans 8 群 + 7 張視覺化圖 |
