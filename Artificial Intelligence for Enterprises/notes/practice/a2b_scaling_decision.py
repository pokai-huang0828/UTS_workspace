# -*- coding: utf-8 -*-
"""A2b 標準化決策的實跑驗證(對應學習記錄 §4.5)。

用途:重現 §4.5「要做標準化」這個裁決背後的每一個數字。
執行:python a2b_scaling_decision.py
相依:pandas, numpy, scikit-learn
資料:../../Assessment2b/BigBlue.csv

⚠️ 這是**決策驗證腳本,不是交件用的分析**。交件 notebook 要自己重寫一份。

產出六段:
  A 各欄佔歐氏距離的比重        → 不標準化時 Recognition 佔 79.6%
  B 分群 vs 單欄分組的 ARI       → 原始尺度 k=4 的 ARI=0.99(等於沒用到另兩欄)
  C 那 10 位被錯置的員工         → 推翻「照範本不標準化」的決定性證據
  D 質心表對照                   → 86/9/9/3 vs 70/25/8/4
  E Codex 質疑一:去掉 Leader     → 核心結論不依賴 Leader 放大(ARI=0.859)
  F Codex 質疑二:秩轉換          → ARI=0.380,序位當等距的影響是真的(限制段要寫)
"""
import os

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler

SEED, N_INIT = 42, 10
CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "Assessment2b", "BigBlue.csv")


def km(X, k, seed=SEED):
    return KMeans(n_clusters=k, random_state=seed, n_init=N_INIT).fit(X)


def head(t):
    print("\n" + "=" * 74 + "\n" + t + "\n" + "=" * 74)


df = pd.read_csv(CSV)
X = df.drop(columns=["EmployeeID"])          # EmployeeID 是標稱識別碼,rubric 第 1 條要排除
cols = list(X.columns)
Z = StandardScaler().fit_transform(X)
M = MinMaxScaler().fit_transform(X)
SCALES = {"原始": X.values, "標準化 z": Z, "MinMax": M}

# 那 10 位「高使用率但零認可」的員工 —— 整個裁決的關鍵證據
stranded = ((X["UsageRate"] >= 0.6) & (X["Recognition"] == 0)).values

head("A. 各欄佔歐氏距離的比重(= 誰在主宰分群)")
for name, Xd in SCALES.items():
    v = np.var(np.asarray(Xd, float), axis=0)
    print("  %-9s %s" % (name, "  ".join(
        "%s %5.1f%%" % (c, 100 * v[i] / v.sum()) for i, c in enumerate(cols))))

head("B. 分群是不是只把 Recognition 重講一遍?(ARI=1.0 代表完全沒用到另兩欄)")
print("  %-3s %14s %14s" % ("k", "原始", "標準化 z"))
for k in (3, 4, 5):
    a = [adjusted_rand_score(X["Recognition"], km(Xd, k).labels_)
         for Xd in (X.values, Z)]
    print("  %-3d %14.3f %14.3f" % (k, a[0], a[1]))

head("C. 決定性證據:%d 位高使用率(>=0.6)但零認可的員工被丟到哪?" % stranded.sum())
print("  ID: %s" % df.loc[stranded, "EmployeeID"].tolist())
for name, Xd in SCALES.items():
    lab = km(Xd, 4).labels_
    grp = sorted(set(lab[stranded]))
    m = np.isin(lab, grp)
    print("  [%-9s] → 群 %s,共 %3d 人,UsageRate 範圍 %.2f-%.2f%s"
          % (name, grp, m.sum(), X["UsageRate"][m].min(), X["UsageRate"][m].max(),
             "   ← 與『從未使用』者同群,商業上無法辯護" if m.sum() > 50 else ""))

head("D. k=4 質心表對照(兩者都還原成原始單位,高階讀者才看得懂)")
for name, Xd in (("原始", X.values), ("標準化 z", Z)):
    lab = km(Xd, 4).labels_
    t = X.copy()
    t["群"] = lab
    g = t.groupby("群")[cols].mean().round(3)
    g.insert(0, "人數", t.groupby("群").size())
    print("\n  [%s] silhouette=%.4f" % (name, silhouette_score(Xd, lab)))
    print(g.sort_values("UsageRate").to_string().replace("\n", "\n  "))

head("E. Codex 質疑①:標準化放大 96%% 為 0 的 Leader,會扭曲結果嗎?")
print("  測法:整欄拿掉 Leader 重跑,看核心結論(那 10 人自成一群)還在不在。\n")
Z2 = StandardScaler().fit_transform(X[["UsageRate", "Recognition"]])
for name, Xd in (("含 Leader", Z), ("去掉 Leader", Z2)):
    lab = km(Xd, 4).labels_
    m = np.isin(lab, list(set(lab[stranded])))
    print("  [%-11s] 群size=%-18s 那 10 人 → %d 人群(%.2f-%.2f)"
          % (name, str(np.bincount(lab).tolist()), m.sum(),
             X["UsageRate"][m].min(), X["UsageRate"][m].max()))
print("\n  兩者 ARI = %.3f → 結論不依賴 Leader 放大,質疑不成立。"
      % adjusted_rand_score(km(Z, 4).labels_, km(Z2, 4).labels_))

head("F. Codex 質疑②:序位當等距(Recognition 0→1 與 3→4 被視為等距)")
print("  測法:改用秩轉換(只保留順序、丟掉間距)重跑。\n")
ZR = StandardScaler().fit_transform(X.rank(method="average"))
for name, Xd in (("z 標準化", Z), ("秩轉換", ZR)):
    lab = km(Xd, 4).labels_
    print("  [%-8s] 群size=%-18s 那 10 人仍同群? %s"
          % (name, str(np.bincount(lab).tolist()), len(set(lab[stranded])) == 1))
print("\n  z vs 秩轉換 ARI = %.3f" % adjusted_rand_score(km(Z, 4).labels_, km(ZR, 4).labels_))
print("  → 質疑成立:結論方向不變,但群組成會變動。報告限制段必須揭露。")

head("G. 選 k:silhouette 與肘部在標準化尺度下不一致,用業務理由裁決")
prev = None
print("  %-3s %11s %11s %-22s" % ("k", "silhouette", "inertia降幅", "各群人數"))
for k in range(2, 10):
    f = km(Z, k)
    drop = "" if prev is None else "%9.1f%%" % (100 * (prev - f.inertia_) / prev)
    sizes = sorted(np.bincount(f.labels_).tolist(), reverse=True)
    flag = "  ← 有 2 人的群,無法設獎金級距" if min(sizes) <= 2 else ""
    print("  %-3d %11.4f %11s %-22s%s"
          % (k, silhouette_score(Z, f.labels_), drop, str(sizes), flag))
    prev = f.inertia_
print("\n  silhouette 最高 k=5;肘部膝蓋 k=4(降幅 44.0% → 29.3%)。")
print("  k=5 產生兩個各 2 人的群 → 選 k=4(且與老師範本示範的 k 一致)。")
