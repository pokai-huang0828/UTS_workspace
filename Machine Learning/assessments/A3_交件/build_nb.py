"""build_nb.py -- A3 submission notebook generator
Po-Kai Huang (26254793) - 321513 Machine Learning - Assessment 3 - Business focus (Bank X telemarketing)

Run with the isolated venv (never the global Python):
    "<Machine Learning>/.venv/Scripts/python.exe" build_nb.py [--runs 2] [--exec-dir DIR]

What it does
 1. reads the OFFICIAL notebook data/bank_x/AT3_TeleMarketing.ipynb (read-only) and strips its stored outputs;
 2. applies the allowed edits to official cells, each marked with a comment line "# [A3 修正] ...";
 3. inserts the "[A3 新增]" cells (A3 說明, Part A analysis after the official outputs) and appends Part B
    (business evaluation against A2 table 4) after the last official cell;
 4. probes the a3venv kernel (must be the venv python), then executes the notebook with nbclient
    (kernel a3venv, cwd = exec dir, env TELEMARKETING_CSV) --runs times; the KPI JSON printed by the final
    code cell must be identical across runs (clustering excluded);
 5. post-processes the last run: kernelspec -> python3 (Colab), scrubs local absolute paths from outputs,
    fills the {{...}} number placeholders of the markdown cells from the notebook's own KPI JSON,
    checks the qualitative claims written in the markdown against that JSON, extracts the figures of the
    cells tagged metadata.a3_fig, and writes
        Huang_26254793_321513_A3.ipynb, a3_kpi_results.json, figs/fig*.png   (next to this script).
    a3_kpi_results.json is the exact text the saved notebook printed between the two markers (UTF-8, LF).

Revision fix-r1 (review round 1): (cpi, cci) period robustness for business criterion 2, ML2 and the cost curve;
bias-corrected (basic) intervals and a seed check; month-matched confusion matrix; XGB diagnostics (Part A) and an
XGB challenger compared on training folds only (Part B); A2 table-1 objective table; error-cost table; Part B summary.

Revision fix-r2 (review round 2): criterion-2 gate back to the planned bootstrap (B = 1,000, seed 123, percentile CI;
B = 5,000 / basic / other seeds kept as disclosed robustness); A2 table-7 replacement rule applied literally
(margin vs seed-to-seed variation, 5 seeds) and the winner (XGB) evaluated on all ten criteria next to the RF;
nested-CV size of the RFE bias; LR-RFE control runs; CIs for the period-stratified uplift, the would-buy share and the
below-threshold difference; error costs at D = A$10/36/100; judgement labels without "部分" plus a yes/no column;
Fig 6 (confusion matrix) and Fig 7 (cost per round); Colab hardening of the Drive mount / CSV path; local paths are
no longer printed at all (quiet pip, fixed kernel cell name) instead of being scrubbed afterwards.

Revision hd (HD review): money view in B-13 (random calling with the mobile-rule month mix, the most the list could
save vs the mobile rule even at the A2 target, would-buy discount per round at the example D = A$36) + Fig 7 bar and
new Fig 8; Fig 9 (AUC decomposition, numbers from B-2 only); B-14 batch-scoring time (hardware-dependent, excluded from
the run-to-run check); all Part B figure text >= 9 pt; one "# [A3]" comment line on the four comment-only
"TODO: Tech Focus Only" cells; B3 / B4 summary cell. No existing number changes.
"""
import argparse
import base64
import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import nbformat
import opencc                       # 官方 markdown 簡體 → 繁體（只在 venv 執行產生器時用；notebook 本身不需要）
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent                      # .../assessments/A3_交件
ML_ROOT = HERE.parents[1]                                    # .../Machine Learning
OFFICIAL = ML_ROOT / 'data' / 'bank_x' / 'AT3_TeleMarketing.ipynb'
CSV = ML_ROOT / 'data' / 'bank_x' / 'TeleMarketing.csv'
VENV = ML_ROOT / '.venv'
VENV_PY = VENV / 'Scripts' / 'python.exe'
# execution folder (ml_pipe.joblib, EDA.html, test.png, cluster_data.csv land here): --exec-dir, else $A3_EXEC_DIR,
# else <system temp>/a3_exec. No machine-specific path is written in this file.
DEFAULT_EXEC_DIR = Path(os.environ.get('A3_EXEC_DIR') or (Path(tempfile.gettempdir()) / 'a3_exec'))
OUT_NB = HERE / 'Huang_26254793_321513_A3.ipynb'
OUT_JSON = HERE / 'a3_kpi_results.json'
FIG_DIR = HERE / 'figs'
KERNEL = 'a3venv'
BEGIN, END = '===A3_KPI_JSON_BEGIN===', '===A3_KPI_JSON_END==='


# ----------------------------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------------------------
def src_lines(src):
    """cell source as one string (nbformat splits it into lines when writing)"""
    return src.strip(chr(10))


def replace_once(cell, old, new):
    s = ''.join(cell['source'])
    assert s.count(old) == 1, ('edit anchor not unique / not found', old[:60], s.count(old))
    cell['source'] = src_lines(s.replace(old, new))


def md(src, cid):
    c = nbformat.v4.new_markdown_cell(source=src.strip('\n'), metadata={'id': cid})
    c.pop('id', None)       # the official notebook is nbformat 4.0 (no cell-level id); Colab uses metadata.id
    return c


def code(src, cid, fig=None):
    meta = {'id': cid}
    if fig:
        meta['a3_fig'] = fig
    c = nbformat.v4.new_code_cell(source=src.strip('\n'), metadata=meta)
    c.pop('id', None)
    return c


# ----------------------------------------------------------------------------------------------------------------
# 1) edits to OFFICIAL cells (only these; official markdown is only converted from Simplified to Traditional script in build())
# ----------------------------------------------------------------------------------------------------------------
def edit_official(cells):
    # cell-2: install into the running kernel's environment
    c = cells[2]
    assert ''.join(c['source']).strip() == '!pip install ydata-profiling'
    c['source'] = src_lines('# [A3 修正] 用 %pip 而不是 !pip：%pip 會裝進目前 kernel 所在的環境（Colab 支援），避免裝到別的 Python\n'
                            '%pip install ydata-profiling')

    # cell-3: guard the optional ydata_profiling import so a failed install never stops the other imports in this cell
    replace_once(cells[3], 'from ydata_profiling import ProfileReport\n',
                 '# [A3 修正] ydata-profiling 只用來產生 EDA 報告；若安裝失敗或與 Colab 版本衝突，不讓整格 import 中斷（後面的 sklearn 等照常匯入）\n'
                 '# [A3 修正] 新版 ydata-profiling 匯入時會印「已改名」的 DeprecationWarning（不影響功能），只在這一行匯入時不顯示（warnings 已在本格第一行匯入）\n'
                 'try:\n'
                 '    with warnings.catch_warnings():\n'
                 "        warnings.simplefilter('ignore', DeprecationWarning)\n"
                 '        from ydata_profiling import ProfileReport\n'
                 'except Exception as e:\n'
                 '    ProfileReport = None\n'
                 "    print('ydata-profiling unavailable, the EDA report will be skipped:', type(e).__name__)\n")

    # cell-11: skip the EDA report when ydata_profiling is unavailable
    c = cells[11]
    assert ''.join(c['source']).strip() == "prof = ProfileReport(data)\nprof.to_file(output_file='EDA.html')"
    c['source'] = src_lines(
        "# [A3 修正] ydata-profiling 不可用時略過 EDA 報告（只少了 EDA.html，不影響後面任何一格）\n"
        "if ProfileReport is not None:\n"
        "    prof = ProfileReport(data)\n"
        "    prof.to_file(output_file='EDA.html')\n"
        "else:\n"
        "    print('skip the EDA report (ydata-profiling unavailable)')")

    # cell-5: Colab-only drive mount
    c = cells[5]
    assert ''.join(c['source']).strip() == "from google.colab import drive\ndrive.mount('/content/drive')"
    c['source'] = src_lines(
        "# [A3 修正] 非 Colab 環境沒有 google.colab → 略過掛載；在 Colab 若拒絕或取消 Drive 授權，drive.mount 會丟其他例外，\n"
        "# 也只印訊息、不中斷「全部執行」（下面讀檔那一格會改找 /content 下的 TeleMarketing.csv）。Colab 上正常授權時行為不變\n"
        "try:\n"
        "    from google.colab import drive\n"
        "    drive.mount('/content/drive')\n"
        "except ImportError:\n"
        "    print('Not running in Colab: skip Google Drive mount')\n"
        "except Exception as e:\n"
        "    print('skip Drive mount:', repr(e))")

    # cell-9: keep official path, fall back to TELEMARKETING_CSV / working directory, clear error otherwise
    c = cells[9]
    assert ''.join(c['source']).strip() == "data = read_data(path='/content/drive/MyDrive/TeleMarketing.csv')\nprint(data.shape)"
    c['source'] = src_lines(
        "# [A3 修正] 保留官方 Colab 路徑；該路徑不存在時改讀環境變數 TELEMARKETING_CSV 指定的檔案，預設為工作目錄下的 TeleMarketing.csv\n"
        "# （Colab 的工作目錄是 /content，所以直接上傳到 /content 也可以）；都找不到時丟出說明清楚的錯誤\n"
        "import os\n"
        "csv_path = '/content/drive/MyDrive/TeleMarketing.csv'\n"
        "if not os.path.exists(csv_path):\n"
        "    csv_path = os.environ.get('TELEMARKETING_CSV', 'TeleMarketing.csv')\n"
        "if not os.path.exists(csv_path):\n"
        "    raise FileNotFoundError('TeleMarketing.csv not found: put it in the My Drive root (and allow the Drive mount) '\n"
        "                            'or upload it to /content, or set TELEMARKETING_CSV to its path')\n"
        "data = read_data(path=csv_path)\n"
        "print(data.shape)")

    # cell-13: TODO 1
    replace_once(cells[13], 'data["month"]._________',
                 '# [A3 修正] 補完 TODO 1：month 的缺值是結構性的（對照組沒被打電話），補固定字串，不用到任何統計量\n'
                 'data["month"].fillna("Not Applicable", inplace = True)')
    replace_once(cells[13], 'data["day_of_week"]._________',
                 '# [A3 修正] 補完 TODO 1：day_of_week 同上（題目註解寫 days_of_week 是筆誤，CSV 欄名是 day_of_week）\n'
                 'data["day_of_week"].fillna("Not Applicable", inplace = True)')

    # cell-15: seaborn >= 0.13 countplot label misalignment -> pair bars via ax.containers
    old15 = """        bars = ax.patches
        half = int(len(bars)/2)
        left_bars = bars[:half]
        right_bars = bars[half:]

        for left, right in zip(left_bars, right_bars):
            height_l = left.get_height()
            height_r = right.get_height()
            total = height_l + height_r

            ax.text(left.get_x() + left.get_width()/2., height_l + 40, '{0:.0%}'.format(height_l/total), ha="center")
            ax.text(right.get_x() + right.get_width()/2., height_r + 40, '{0:.0%}'.format(height_r/total), ha="center")"""
    new15 = """        # [A3 修正] seaborn >= 0.13 會把圖例的代理矩形也放進 ax.patches，且計數為 0 的組合不畫柱，
        # 原本「前半 / 後半」切 ax.patches 的配對會錯位、百分比標錯（不會報錯）。
        # 改用 ax.containers（每個 hue 一組柱），依柱子所在的類別位置配對加總，再標各柱佔該類別的比例。
        totals = {}
        for container in ax.containers:
            for bar in container:
                pos = int(round(bar.get_x() + bar.get_width()/2.))
                totals[pos] = totals.get(pos, 0) + bar.get_height()
        for container in ax.containers:
            for bar in container:
                pos = int(round(bar.get_x() + bar.get_width()/2.))
                height = bar.get_height()
                if totals[pos] > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + 40, '{0:.0%}'.format(height/totals[pos]), ha="center")"""
    replace_once(cells[15], old15, new15)

    # cell-30: TODO 2
    replace_once(cells[30], "test_data['response'] = _____________________",
                 "# [A3 修正] 補完 TODO 2：測試集只用訓練集擬合好的 label_encoder 做 transform，不重新 fit（防洩漏）\n"
                 "test_data['response'] = label_encoder.transform(test_data['y'].to_numpy().reshape(-1,1))")

    # cell-44: dict -> list (pandas >= 2.1 refuses a dict as column indexer in cells 45/47/50)
    replace_once(cells[44], "    return selected_features",
                 "    # [A3 修正] 回傳 list 而不是 dict：pandas >= 2.1 不准用 dict 當欄位索引，cell-45/47/50 的 train_data[...] 會 TypeError（Colab 也會）\n"
                 "    return list(selected_features)")

    # cell-47: TODO 3
    replace_once(cells[47], "label=_______,", "label='response',   # [A3 修正] 補完 TODO 3：與上一格 RF 相同的數值標籤")
    replace_once(cells[47], "model=_____,", "model='LR',         # [A3 修正] 補完 TODO 3：邏輯迴歸")
    replace_once(cells[47], "k=____)", "k=10)               # [A3 修正] 補完 TODO 3：與 RF 相同選 10 個")

    # cell-58: grid third values
    replace_once(cells[58], "rf_parameters = {'max_depth':[3,5,___],",
                 "# [A3 修正] 補完超參數：max_depth 第三值 9、n_estimators 第三值 300（理由見最終 pipeline 之後的解讀，依本次 CV 結果）\n"
                 "rf_parameters = {'max_depth':[3,5,9],")
    replace_once(cells[58], "'n_estimators':[100,200,___]", "'n_estimators':[100,200,300]")

    # cells 38 / 48 / 52 / 60: "TODO: Tech Focus Only" open questions (technical focus). Comment-only cells; one comment line
    # is added on top so that a marker does not read them as unfinished code. Nothing executable changes.
    for i in (38, 48, 52, 60):
        s = ''.join(cells[i]['source'])
        assert s.startswith('# TODO: Tech Focus Only'), (i, s[:40])
        assert all(ln.strip() == '' or ln.lstrip().startswith('#') for ln in s.splitlines()), ('not comment-only', i)
        cells[i]['source'] = src_lines('# [A3] 技術重點（Tech Focus Only）的開放題；本作業選商業重點，依作業說明不處理\n' + s)

    for i, c in enumerate(cells):
        if c['cell_type'] == 'code':
            assert '___' not in ''.join(c['source']), ('blank left', i)


# ----------------------------------------------------------------------------------------------------------------
# 2) Part A inserted cells (code)
# ----------------------------------------------------------------------------------------------------------------
A_GUARD = r'''
# [A3 新增] 防呆檢查：確認 TODO 1 的三個欄位已沒有空值（印出各欄空值數）
# pandas 2.x 的鏈式 inplace fillna 仍有效；若在 pandas 3.0（Copy-on-Write）下靜默失效，這裡先補救再檢查
a3_na = campaign_data[['contact', 'month', 'day_of_week']].isnull().sum()
if a3_na.sum() > 0:
    print('chained inplace fillna had no effect -> repaired with DataFrame.fillna', a3_na.to_dict())
    campaign_data = campaign_data.fillna({'contact': 'Not Applicable', 'month': 'Not Applicable', 'day_of_week': 'Not Applicable'})
    data = campaign_data.copy(deep=True)
    a3_na = campaign_data[['contact', 'month', 'day_of_week']].isnull().sum()
print(a3_na)
assert a3_na.sum() == 0


def a3_r(x, nd=4):
    """numpy 數字 -> JSON 可存的 Python 數字（四捨五入）"""
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    return round(float(x), nd)


A3_KPI = {'part_a': {}, 'part_b': {}}   # 收集報告會引用的數字；最後一格程式把它印成 JSON
A3_KPI['part_a']['rows_after_dedup'] = len(campaign_data)
'''

A_EDA = r'''
# [A3 新增] EDA 數字摘要：上面三格只有圖，這裡把解讀要引用的數字印成表（只讀 campaign_data，不改動它）
def a3_conv(s):
    return round(100 * (s == 'yes').mean(), 2)

a3_T = campaign_data[campaign_data['campaign'] == '1']
a3_eda_grp = campaign_data.groupby('campaign').agg(rows=('y', 'size'), conv_pct=('y', a3_conv),
                                                   duration0_pct=('duration', lambda s: round(100 * (s == 0).mean(), 2)))
a3_eda_pout = campaign_data.groupby('poutcome')['y'].agg(rows='size', conv_pct=a3_conv)
a3_eda_contact = a3_T.groupby('contact')['y'].agg(rows='size', conv_pct=a3_conv)
a3_eda_month = a3_T.groupby('month')['y'].agg(rows='size', conv_pct=a3_conv).sort_values('conv_pct', ascending=False)
a3_eda_num = campaign_data.groupby('y')[['age', 'cons.price.idx', 'cons.conf.idx']].mean().round(2)
a3_eda_num['duration_target'] = a3_T.groupby('y')['duration'].mean().round(1)
print('[1] control (0) vs target (1): rows, conversion %, share with duration = 0\n', a3_eda_grp, '\n')
print('[2] conversion % by previous campaign outcome (all rows)\n', a3_eda_pout, '\n')
print('[3] target group: conversion % by contact channel\n', a3_eda_contact, '\n')
print('[4] target group: conversion % by month (sorted)\n', a3_eda_month, '\n')
print('[5] mean of numeric features by y (duration_target: target group only, the control group is all 0)\n', a3_eda_num, '\n')
# 計數圖上其他類別欄位（全部列）與星期（只有目標組有值）的成交率；只列 500 列以上的類別才比較高低
a3_eda_cat = {c: campaign_data.groupby(c)['y'].agg(rows='size', conv_pct=a3_conv) for c in ['job', 'education', 'default', 'housing', 'loan']}
a3_eda_dow = a3_T.groupby('day_of_week')['y'].agg(rows='size', conv_pct=a3_conv)
print('[6] conversion % by job / education / default / housing / loan (all rows) and by day of week (target group)')
for c, t in a3_eda_cat.items():
    print(t.sort_values('conv_pct', ascending=False).T.to_string(), '\n')
print(a3_eda_dow.T.to_string())
a3_base = a3_conv(campaign_data['y'])
print('\n[7] overall share of "yes" after deduplication: %.2f%% (class imbalance, about 1 in %.0f)' % (a3_base, 100 / a3_base))
# poutcome = success 依組別（A2 附錄 A 的 67.3%／62.7% 是原始全檔的目標組／對照組，母體不同）
a3_ps = campaign_data[campaign_data['poutcome'] == 'success'].groupby('campaign')['y'].agg(rows='size', conv_pct=a3_conv)
print('[8] poutcome = success by group (deduplicated; 0 = control, 1 = target)\n', a3_ps)

A3_KPI['part_a']['eda'] = {
    'base_conv_pct': a3_base,
    'cat_conv_pct': {c: {k: a3_r(v, 2) for k, v in t['conv_pct'].items()} for c, t in a3_eda_cat.items()},
    'cat_rows': {c: {k: a3_r(v) for k, v in t['rows'].items()} for c, t in a3_eda_cat.items()},
    'cat_conv_range_n500': {c: [a3_r(t.loc[t['rows'] >= 500, 'conv_pct'].min(), 2), a3_r(t.loc[t['rows'] >= 500, 'conv_pct'].max(), 2)]
                            for c, t in a3_eda_cat.items()},
    'cat_best_n500': {c: t.loc[t['rows'] >= 500, 'conv_pct'].idxmax() for c, t in a3_eda_cat.items()},
    'cat_worst_n500': {c: t.loc[t['rows'] >= 500, 'conv_pct'].idxmin() for c, t in a3_eda_cat.items()},
    'dow_conv_range': [a3_r(a3_eda_dow['conv_pct'].min(), 2), a3_r(a3_eda_dow['conv_pct'].max(), 2)],
    'rows': {k: a3_r(v) for k, v in a3_eda_grp['rows'].items()},
    'conv_pct': {k: a3_r(v, 2) for k, v in a3_eda_grp['conv_pct'].items()},
    'duration0_pct': {k: a3_r(v, 2) for k, v in a3_eda_grp['duration0_pct'].items()},
    'target_duration0_rows': a3_r((a3_T['duration'] == 0).sum()),
    'poutcome_conv_pct': {k: a3_r(v, 2) for k, v in a3_eda_pout['conv_pct'].items()},
    'poutcome_rows': {k: a3_r(v) for k, v in a3_eda_pout['rows'].items()},
    'target_contact_conv_pct': {k: a3_r(v, 2) for k, v in a3_eda_contact['conv_pct'].items()},
    'target_contact_rows': {k: a3_r(v) for k, v in a3_eda_contact['rows'].items()},
    'target_month_conv_pct': {k: a3_r(v, 2) for k, v in a3_eda_month['conv_pct'].items()},
    'target_month_rows': {k: a3_r(v) for k, v in a3_eda_month['rows'].items()},
    'mean_by_y': {c: {k: a3_r(v, 2) for k, v in a3_eda_num[c].items()} for c in a3_eda_num.columns},
    'target_duration_max': a3_r(a3_T['duration'].max()),
    'poutcome_success_by_group': {k: {'rows': int(r['rows']), 'conv_pct': a3_r(r['conv_pct'], 2)} for k, r in a3_ps.iterrows()},
}
'''

A_TSNE = r'''
# [A3 新增] t-SNE 的輸入規模與成交比例（TODO 2 補完後 test_data['response'] 才存在）
a3_tsne_inputs = num_features_scl + num_features_tfm + oh_features
A3_KPI['part_a']['tsne'] = {
    'train_rows': len(train_data), 'test_rows': len(test_data),
    'n_inputs': len(a3_tsne_inputs), 'n_onehot': len(oh_features),
    'onehot_group_flags': [f for f in oh_features if f.startswith('campaign') or 'Not Applicable' in f],
    'train_pos_pct': a3_r(100 * train_data['response'].mean(), 2),
    'test_pos_pct': a3_r(100 * test_data['response'].mean(), 2),
    'label_classes': [str(c) for c in label_encoder.classes_],
}
# 量化圖上看到的結構：在測試集的 t-SNE 平面上，每個點最近的 10 個鄰居有多少比例與它「同組」（對照 / 目標）、多少比例「同結果」
from sklearn.neighbors import NearestNeighbors
a3_nb = NearestNeighbors(n_neighbors=11).fit(tnse_data).kneighbors(tnse_data, return_distance=False)[:, 1:]
a3_g = (test_data['campaign'] == '1').to_numpy()
a3_y = test_data['response'].to_numpy()
a3_same_g, a3_same_y = (a3_g[a3_nb] == a3_g[:, None]).mean(), (a3_y[a3_nb] == a3_y[:, None]).mean()
a3_base_g = a3_g.mean() ** 2 + (1 - a3_g.mean()) ** 2
a3_base_y = a3_y.mean() ** 2 + (1 - a3_y.mean()) ** 2
A3_KPI['part_a']['tsne'].update({'knn_same_group_pct': a3_r(100 * a3_same_g, 1), 'knn_same_group_random_pct': a3_r(100 * a3_base_g, 1),
                                 'knn_same_outcome_pct': a3_r(100 * a3_same_y, 1), 'knn_same_outcome_random_pct': a3_r(100 * a3_base_y, 1)})
# 官方 cell-23／24 的冪變換分布圖：訓練集 duration 變換前後的偏度
from scipy.stats import skew
A3_KPI['part_a']['tsne'].update({'duration_skew_train': a3_r(skew(train_data['duration']), 2),
                                 'duration_tfm_skew_train': a3_r(skew(train_data['duration_tfm']), 2)})
print(A3_KPI['part_a']['tsne'])
print('10 nearest neighbours on the test-set map: same group %.1f%% (random %.1f%%), same outcome %.1f%% (random %.1f%%)'
      % (100 * a3_same_g, 100 * a3_base_g, 100 * a3_same_y, 100 * a3_base_y))
'''

A_UNI = r'''
# [A3 新增] 兩種單變量方法選出的前 10 名（上面的圖由下往上排，這裡印成清單並比對重疊）
def a3_tag(f):
    """依「撥號前能不能知道」替特徵貼標籤（商業解讀用）"""
    if f.startswith('duration'):
        return 'post-call (duration)'
    if f.startswith('campaign') or 'Not Applicable' in f:
        return 'group flag (control vs target)'
    if f.startswith(('contact', 'month', 'day_of_week')):
        return 'scheduling (Not Applicable for control)'
    return 'pre-call'

a3_uni = pd.DataFrame({'f_classif top10': selected_features_f_classif, 'chi2 top10': selected_features_chi2})
a3_uni['f_classif tag'] = a3_uni['f_classif top10'].map(a3_tag)
a3_uni['chi2 tag'] = a3_uni['chi2 top10'].map(a3_tag)
print(a3_uni.to_string())
a3_overlap = [f for f in selected_features_f_classif if f in selected_features_chi2]
print('\noverlap (%d):' % len(a3_overlap), a3_overlap)
A3_KPI['part_a']['univariate'] = {
    'f_classif_top10': list(selected_features_f_classif), 'chi2_top10': list(selected_features_chi2),
    'overlap': a3_overlap, 'n_overlap': len(a3_overlap), 'n_features_tested': len(features),
    'f_classif_group_or_post_call': sum(a3_tag(f) != 'pre-call' for f in selected_features_f_classif),
    'chi2_group_or_post_call': sum(a3_tag(f) != 'pre-call' for f in selected_features_chi2),
}
'''

A_MFS = r'''
# [A3 新增] 四種特徵選擇方法的比較表（cell-41 兩種單變量、cell-45 RF-RFE、cell-47 LR-RFE）＋商業標籤
a3_all = sorted(set(selected_features_f_classif) | set(selected_features_chi2) | set(selected_feature_RF) | set(selected_feature_LR))
a3_fs = pd.DataFrame({'feature': a3_all})
for name, lst in [('f_classif', selected_features_f_classif), ('chi2', selected_features_chi2),
                  ('RF-RFE', selected_feature_RF), ('LR-RFE', selected_feature_LR)]:
    a3_fs[name] = a3_fs['feature'].isin(lst).map({True: 'x', False: ''})
a3_fs['n_methods'] = (a3_fs[['f_classif', 'chi2', 'RF-RFE', 'LR-RFE']] == 'x').sum(axis=1)
a3_fs['tag'] = a3_fs['feature'].map(a3_tag)
print(a3_fs.sort_values(['n_methods', 'feature'], ascending=[False, True]).to_string(index=False))
a3_tag_counts = {name: pd.Series([a3_tag(f) for f in lst]).value_counts().to_dict()
                 for name, lst in [('RF-RFE', selected_feature_RF), ('LR-RFE', selected_feature_LR)]}
print('\ntags of the RFE selections:', a3_tag_counts)
A3_TAG_CODE = {'pre-call': 'pre_call', 'post-call (duration)': 'post_call',
               'group flag (control vs target)': 'group_flag', 'scheduling (Not Applicable for control)': 'scheduling'}

# 熱圖（官方 cell-45、47）上的數字：RF 選中欄位兩兩之間最大的 |r|；LR 選中欄位與 response 的相關
def a3_dense(cols):
    return pd.DataFrame(np.asarray(train_data[cols], dtype=float), columns=cols, index=train_data.index)


a3_rf_c = a3_dense(list(selected_feature_RF)).corr()
a3_pairs = a3_rf_c.where(np.triu(np.ones(a3_rf_c.shape, dtype=bool), 1)).stack().abs().sort_values(ascending=False)
print('\nlargest |r| between RF-selected columns:', {'%s ~ %s' % k: round(v, 3) for k, v in a3_pairs.head(3).items()})
a3_lr_cols = list(selected_feature_LR)
a3_lr_resp = a3_dense(a3_lr_cols + ['response']).corr()['response'].drop('response')
print('correlation of each LR-RFE column with response:', a3_lr_resp.round(3).to_dict())
a3_flags = [f for f in a3_lr_cols if a3_tag(f) == 'group flag (control vs target)']
a3_g0 = np.asarray(train_data['campaign_0'], dtype=float)
a3_collinear = {'campaign_0 + campaign_1 = 1': bool(np.all(a3_g0 + np.asarray(train_data['campaign_1'], dtype=float) == 1)),
                'campaign_int = campaign_1': bool(np.all(np.asarray(train_data['campaign_int'], dtype=float) == np.asarray(train_data['campaign_1'], dtype=float)))}
for f in ['contact_Not Applicable', 'month_Not Applicable', 'day_of_week_Not Applicable']:
    a3_collinear[f + ' = campaign_0'] = bool(np.all(np.asarray(train_data[f], dtype=float) == a3_g0))
print('exact collinearity among the group flags:', a3_collinear)
# 用與 RFE 相同設定的 LR（C = 1000、balanced）在這 10 欄上重新擬合，只為了看係數大小（說明 RFE 為什麼留下這些欄位；不影響官方流程）
a3_lr_fit = LogisticRegression(C=1000, class_weight='balanced', max_iter=10000).fit(np.asarray(train_data[a3_lr_cols], dtype=float),
                                                                                     train_data['response'])
a3_lr_coef = pd.Series(a3_lr_fit.coef_[0], index=a3_lr_cols).sort_values(key=abs, ascending=False)
print('LR coefficients on the LR-RFE columns (C = 1000):', a3_lr_coef.round(2).to_dict())

# 對照實驗（各重跑一次與官方 cell-44 相同的 LR-RFE，只改一個條件）：(1) C = 1；(2) 拿掉兩個 duration 欄
a3_fs_cols = num_features_tfm + num_features_scl + int_features + oh_features
def a3_lr_rfe(cols, C):
    r_ = RFE(LogisticRegression(C=C, class_weight='balanced', max_iter=10000), n_features_to_select=10)
    r_.fit(np.asarray(train_data[cols]), np.asarray(train_data['response']))
    return [f for f, s in zip(cols, r_.support_) if s]


a3_lr_c1 = a3_lr_rfe(a3_fs_cols, 1)
a3_lr_nodur = a3_lr_rfe([f for f in a3_fs_cols if not f.startswith('duration')], 1000)
a3_ctl = pd.DataFrame({'official (C = 1000)': pd.Series([a3_tag(f) for f in a3_lr_cols]).value_counts(),
                       'control 1: C = 1': pd.Series([a3_tag(f) for f in a3_lr_c1]).value_counts(),
                       'control 2: no duration columns': pd.Series([a3_tag(f) for f in a3_lr_nodur]).value_counts()}).fillna(0).astype(int)
print('\nLR-RFE control runs: tags of the 10 selected columns')
print(a3_ctl.to_string())
print('control 1 selects the same columns as the official run:', sorted(a3_lr_c1) == sorted(a3_lr_cols))
print('control 2 selection:', a3_lr_nodur)
a3_dtfm_c = train_data.loc[train_data['campaign'] == '0', 'duration_tfm']
print('duration_tfm in the control group: one constant value %.3f (target group minimum %.3f)'
      % (a3_dtfm_c.iloc[0], train_data.loc[train_data['campaign'] == '1', 'duration_tfm'].min()))

A3_KPI['part_a']['model_fs'] = {
    'rf_rfe': list(selected_feature_RF), 'lr_rfe': list(selected_feature_LR),
    'rf_lr_overlap': [f for f in selected_feature_RF if f in selected_feature_LR],
    'tag_counts': {k.replace('-', '_'): {A3_TAG_CODE[t]: int(n) for t, n in v.items()} for k, v in a3_tag_counts.items()},
    'in_all_four': a3_fs.loc[a3_fs['n_methods'] == 4, 'feature'].tolist(),
    'rf_max_pair_text': '%s 與 %s 的 |r| = %.3f' % (a3_pairs.index[0][0], a3_pairs.index[0][1], a3_pairs.iloc[0]),
    'rf_max_pair_abs_r': a3_r(a3_pairs.iloc[0], 3),
    'rf_dur_pair_abs_r': a3_r(abs(a3_rf_c.loc['duration_tfm', 'duration_scl']), 3)
    if {'duration_tfm', 'duration_scl'} <= set(a3_rf_c.columns) else None,
    'lr_flags': a3_flags,
    'lr_flag_max_abs_corr_with_response': a3_r(a3_lr_resp[a3_flags].abs().max(), 3) if a3_flags else None,
    'collinear': a3_collinear,
    'lr_coef_top_text': '、'.join('%s %+.2f' % (k, v) for k, v in a3_lr_coef.head(6).items()),
    'lr_flag_coef_abs_max': a3_r(a3_lr_coef[a3_flags].abs().max(), 2) if a3_flags else None,
    'lr_ctl_c1_same': sorted(a3_lr_c1) == sorted(a3_lr_cols),
    'lr_ctl_c1_flags': sum(a3_tag(f) == 'group flag (control vs target)' for f in a3_lr_c1),
    'lr_ctl_nodur_flags': sum(a3_tag(f) == 'group flag (control vs target)' for f in a3_lr_nodur),
    'lr_ctl_nodur_tags': {A3_TAG_CODE[t]: int(n) for t, n in pd.Series([a3_tag(f) for f in a3_lr_nodur]).value_counts().items()},
    'lr_ctl_nodur': a3_lr_nodur,
    'control_duration_tfm': a3_r(a3_dtfm_c.iloc[0], 3), 'control_duration_tfm_constant': bool(a3_dtfm_c.nunique() == 1),
    'target_duration_tfm_min': a3_r(train_data.loc[train_data['campaign'] == '1', 'duration_tfm'].min(), 3),
}
'''

A_PROBA = r'''
# [A3 新增] cell-50 用 .predict() 的 0/1 標籤算 AUC，那衡量不到「排序」能力；這裡用 predict_proba 重算（只讀 rf、gb，不重新訓練）
a3_Xte = test_data[selected_feature_RF]
a3_auc_rf = roc_auc_score(test_data['response'], rf.best_estimator_.predict_proba(a3_Xte)[:, 1])
a3_auc_gb = roc_auc_score(test_data['response'], gb.best_estimator_.predict_proba(a3_Xte)[:, 1])
a3_ratio = (train_data['response'] == 0).sum() / (train_data['response'] == 1).sum()
a3_gb_pos = (gb.best_estimator_.predict(a3_Xte) == 1).mean()
a3_rf_pos = (rf.best_estimator_.predict(a3_Xte) == 1).mean()
print(pd.DataFrame({
    'official (predict labels)': [auc_score['rf'], auc_score['gb']],
    'predict_proba AUC (test)': [a3_auc_rf, a3_auc_gb],
    '5-fold CV AUC (train)': [rf.best_score_, gb.best_score_],
    'share predicted "yes" (test)': [a3_rf_pos, a3_gb_pos]}, index=['RF', 'XGB']).round(4))
print('\nnegative / positive ratio in the deduplicated training data: %.2f (XGB uses scale_pos_weight = 87)' % a3_ratio)

# cell-26 在測試集上重新擬合冪變換（power_transform 每次呼叫都重新 fit）：比較 λ，並量它對 RF 測試 AUC 的影響
a3_pt_train = PowerTransformer().fit(train_data[['duration']])
a3_pt_test = PowerTransformer().fit(test_data[['duration']])
a3_auc_rf_fix = None
if 'duration_tfm' in a3_Xte.columns:
    a3_Xte_fix = a3_Xte.copy()
    a3_Xte_fix['duration_tfm'] = a3_pt_train.transform(test_data[['duration']]).ravel()   # 正確做法：用訓練集擬合的轉換器
    a3_auc_rf_fix = roc_auc_score(test_data['response'], rf.best_estimator_.predict_proba(a3_Xte_fix)[:, 1])
print('Yeo-Johnson lambda fitted on train %.4f vs on test %.4f' % (a3_pt_train.lambdas_[0], a3_pt_test.lambdas_[0]))
print('RF test AUC with the train-fitted transform %.4f vs as run (test-fitted) %.4f: train-fitted minus as-run = %+.5f'
      % (a3_auc_rf_fix or float('nan'), a3_auc_rf, (a3_auc_rf_fix or float('nan')) - a3_auc_rf))

A3_KPI['part_a']['model_compare'] = {
    'official_predict_auc': {'rf': a3_r(auc_score['rf']), 'gb': a3_r(auc_score['gb'])},
    'proba_auc_test': {'rf': a3_r(a3_auc_rf), 'gb': a3_r(a3_auc_gb)},
    'cv_auc_train': {'rf': a3_r(rf.best_score_), 'gb': a3_r(gb.best_score_)},
    'share_predicted_yes': {'rf': a3_r(a3_rf_pos), 'gb': a3_r(a3_gb_pos)},
    'share_predicted_yes_pct': {'rf': a3_r(100 * a3_rf_pos, 1), 'gb': a3_r(100 * a3_gb_pos, 1)},
    'proba_gap_rf_minus_gb': a3_r(a3_auc_rf - a3_auc_gb),
    'neg_pos_ratio_train': a3_r(a3_ratio, 2), 'scale_pos_weight_used': 87,
    'lambda_train': a3_r(a3_pt_train.lambdas_[0]), 'lambda_test': a3_r(a3_pt_test.lambdas_[0]),
    'rf_auc_train_fitted_transform': None if a3_auc_rf_fix is None else a3_r(a3_auc_rf_fix),
    'rf_auc_trainfit_minus_asrun': None if a3_auc_rf_fix is None else a3_r(a3_auc_rf_fix - a3_auc_rf, 5),
    'rf_cv_sd': a3_r(rf.cv_results_['std_test_score'][rf.best_index_]),
    'features': list(selected_feature_RF),
}
'''

A_XGB = r'''
# [A3 新增] 純診斷：官方 cell-50 的 XGB 只改一兩個參數重跑，檢查官方 cell-53「RF 優於 XGB」是否成立（官方 rf、gb 物件都不動）
# 同樣 10 欄（RF 選的）、同樣 5 折 CV（cv=5）、同樣的測試集；XGB 用 n_jobs=1 讓結果可重現
from sklearn.model_selection import cross_val_score
a3_xgb_base = dict(learning_rate=0.01, n_estimators=100, max_depth=5, colsample_bytree=0.1, subsample=0.1,
                   random_state=RANDOM_SATE, n_jobs=1)
a3_xgb_cfg = [('official: scale_pos_weight = 87', dict(scale_pos_weight=87)),
              ('scale_pos_weight = %.2f (actual neg/pos)' % a3_ratio, dict(scale_pos_weight=a3_ratio)),
              ('scale_pos_weight = 87, subsample = colsample = 1.0', dict(scale_pos_weight=87, subsample=1.0, colsample_bytree=1.0)),
              ('scale_pos_weight = 87, learning_rate = 0.1', dict(scale_pos_weight=87, learning_rate=0.1))]
a3_Xtr = train_data[selected_feature_RF]
a3_rows = [{'model': 'RF (official cell-50, as run)', 'cv_auc': rf.best_score_, 'cv_sd': rf.cv_results_['std_test_score'][rf.best_index_],
            'test_auc_proba': a3_auc_rf, 'share_pred_yes_pct': 100 * a3_rf_pos, 'test_auc_labels': auc_score['rf']}]
for a3_name, a3_kw in a3_xgb_cfg:
    a3_m = XGBClassifier(**{**a3_xgb_base, **a3_kw})
    a3_cv = cross_val_score(a3_m, a3_Xtr, train_data['response'], cv=5, scoring='roc_auc')
    a3_m.fit(a3_Xtr, train_data['response'])
    a3_lab = a3_m.predict(a3_Xte)
    a3_rows.append({'model': 'XGB ' + a3_name, 'cv_auc': a3_cv.mean(), 'cv_sd': a3_cv.std(),
                    'test_auc_proba': roc_auc_score(test_data['response'], a3_m.predict_proba(a3_Xte)[:, 1]),
                    'share_pred_yes_pct': 100 * (a3_lab == 1).mean(), 'test_auc_labels': roc_auc_score(test_data['response'], a3_lab)})
a3_xgb = pd.DataFrame(a3_rows).set_index('model')
print(a3_xgb.round(4).to_string())
a3_fixd = a3_xgb.iloc[2]
print('\nXGB with the actual ratio minus RF: CV %+.4f, test %+.4f (RF CV fold sd %.4f)'
      % (a3_fixd['cv_auc'] - rf.best_score_, a3_fixd['test_auc_proba'] - a3_auc_rf, a3_rows[0]['cv_sd']))
print('official XGB settings re-run here with n_jobs = 1: CV %.4f; the official object (n_jobs = 8) reported %.4f'
      % (a3_xgb.iloc[1]['cv_auc'], gb.best_score_))
A3_KPI['part_a']['xgb_diag'] = {
    'rows': [{'model': k, **{c: a3_r(v) for c, v in r.items()}} for k, r in a3_xgb.iterrows()],
    'official_cv_reproduced': bool(abs(a3_xgb.iloc[1]['cv_auc'] - gb.best_score_) < 1e-6),
    'ratio': a3_r(a3_ratio, 2),
    'fixed_cv_auc': a3_r(a3_fixd['cv_auc']), 'fixed_cv_sd': a3_r(a3_fixd['cv_sd']),
    'fixed_test_auc': a3_r(a3_fixd['test_auc_proba']), 'fixed_label_auc': a3_r(a3_fixd['test_auc_labels']),
    'fixed_share_yes_pct': a3_r(a3_fixd['share_pred_yes_pct'], 1),
    'official_share_yes_pct': a3_r(a3_xgb.iloc[1]['share_pred_yes_pct'], 1),
    'subcol1_share_yes_pct': a3_r(a3_xgb.iloc[3]['share_pred_yes_pct'], 1),
    'lr01_share_yes_pct': a3_r(a3_xgb.iloc[4]['share_pred_yes_pct'], 1),
    'xgb_minus_rf_cv': a3_r(a3_fixd['cv_auc'] - rf.best_score_), 'xgb_minus_rf_test': a3_r(a3_fixd['test_auc_proba'] - a3_auc_rf),
}
'''

A_FINAL = r'''
# [A3 新增] 最終 pipeline 的補充診斷：只用 predict_proba / transform，不對 ml_pipe、prep、rfe、clf_cv 呼叫 fit
from sklearn.model_selection import cross_val_score
a3_gs = ml_pipe.named_steps['clf']
a3_cvres = pd.DataFrame(a3_gs.cv_results_)[['param_criterion', 'param_max_depth', 'param_n_estimators',
                                             'mean_test_score', 'std_test_score', 'rank_test_score']]
print('[1] 5-fold CV AUC of the 18 grid settings (cell-58), best first')
print(a3_cvres.sort_values('rank_test_score').round(4).to_string(index=False))
a3_best = a3_gs.best_params_
a3_by_depth = a3_cvres.groupby('param_max_depth')['mean_test_score'].max()
a3_by_nest = a3_cvres[(a3_cvres['param_criterion'] == a3_best['criterion']) &
                      (a3_cvres['param_max_depth'] == a3_best['max_depth'])].set_index('param_n_estimators')['mean_test_score']
print('\nbest CV AUC by max_depth:', a3_by_depth.round(4).to_dict())
print('CV AUC by n_estimators at the best criterion/depth:', a3_by_nest.round(4).to_dict())

# [2] 9 在網格邊界：用同一份（已擬合的）前處理 + RFE 輸出，掃 max_depth 7 / 9 / 11（其餘超參數同最佳組；同樣 5 折）
a3_Xtr_rfe = ml_pipe[:-1].transform(train_data)
a3_Xte_rfe = ml_pipe[:-1].transform(test_data)
a3_ytr, a3_yte = (train_data['y'] == 'yes').to_numpy(), (test_data['y'] == 'yes').to_numpy()
a3_sweep = []
for d in (7, 9, 11):
    m = RandomForestClassifier(max_depth=d, criterion=a3_best['criterion'], n_estimators=a3_best['n_estimators'],
                               class_weight='balanced', random_state=RANDOM_SATE, n_jobs=8)
    cv = cross_val_score(m, a3_Xtr_rfe, train_data['y'], cv=5, scoring='roc_auc').mean()
    m.fit(a3_Xtr_rfe, train_data['y'])
    tr = roc_auc_score(a3_ytr, m.predict_proba(a3_Xtr_rfe)[:, 1])
    te = roc_auc_score(a3_yte, m.predict_proba(a3_Xte_rfe)[:, 1])
    a3_sweep.append({'max_depth': d, 'cv_auc': cv, 'train_auc': tr, 'test_auc': te, 'train_minus_test': tr - te})
a3_sweep = pd.DataFrame(a3_sweep)
print('\n[2] depth sweep on the same RFE features (diagnostic only; the official grid is not changed)')
print(a3_sweep.round(4).to_string(index=False))

# [2b] RFE 在整個訓練集上擬合後才進 GridSearchCV 的 5 折：驗證折的標籤參與了特徵篩選。量偏誤大小：
#      最佳設定（criterion / max_depth / n_estimators 同上）在同樣的 cv=5 折上比較
#      非巢狀（RFE 用整個訓練集擬合一次）vs 巢狀（每一折只用訓練折重做 RFE）。
#      前處理（無監督、不用標籤）沿用已擬合的官方 prep；為了速度轉成密集矩陣（官方是稀疏矩陣，樹的分割細節略有不同，
#      所以兩邊都用密集矩陣重算，只看兩者的差）。
a3_Xp = ml_pipe.named_steps['prep'].transform(train_data)
a3_Xp = a3_Xp.toarray() if hasattr(a3_Xp, 'toarray') else np.asarray(a3_Xp)
def a3_rfe_new(n_jobs):
    return RFE(RandomForestClassifier(n_estimators=50, class_weight='balanced', random_state=123, n_jobs=n_jobs), n_features_to_select=10)
def a3_rf_best(n_jobs):
    return RandomForestClassifier(class_weight='balanced', random_state=RANDOM_SATE, n_jobs=n_jobs, **a3_best)
a3_rfe_full = a3_rfe_new(8).fit(a3_Xp, train_data['y'])
a3_cv_flat = cross_val_score(a3_rf_best(8), a3_rfe_full.transform(a3_Xp), train_data['y'], cv=5, scoring='roc_auc')
a3_cv_nest = cross_val_score(Pipeline([('rfe', a3_rfe_new(4)), ('clf', a3_rf_best(4))]), a3_Xp, train_data['y'],
                             cv=5, scoring='roc_auc', n_jobs=5)
print('\n[2b] RFE selection bias, best setting, same 5 folds (dense copy of the prep output)')
print('     non-nested (RFE fitted once on all training rows) CV AUC %.4f | nested (RFE refitted inside each fold) %.4f'
      ' | difference %+.4f' % (a3_cv_flat.mean(), a3_cv_nest.mean(), a3_cv_flat.mean() - a3_cv_nest.mean()))
print('     per fold, non-nested:', np.round(a3_cv_flat, 4), ' nested:', np.round(a3_cv_nest, 4))
print('     same RFE columns as the official run:', bool(np.array_equal(a3_rfe_full.support_, ml_pipe.named_steps['rfe'].support_)))

# [3] AUC：整體（= cell-59）以及只看目標組 / 只看對照組
a3_p_tr = ml_pipe.predict_proba(train_data)[:, 1]
a3_p_te = ml_pipe.predict_proba(test_data)[:, 1]
a3_auc_tr, a3_auc_te = roc_auc_score(a3_ytr, a3_p_tr), roc_auc_score(a3_yte, a3_p_te)
a3_tmask = (test_data['campaign'] == '1').to_numpy()
a3_auc_te_T = roc_auc_score(a3_yte[a3_tmask], a3_p_te[a3_tmask])
a3_auc_te_C = roc_auc_score(a3_yte[~a3_tmask], a3_p_te[~a3_tmask])
print('\n[3] AUC train %.4f | test %.4f | test target group only %.4f | test control group only %.4f'
      % (a3_auc_tr, a3_auc_te, a3_auc_te_T, a3_auc_te_C))
print('    mean predicted probability on test %.3f vs actual share of "yes" %.3f (class_weight=balanced: scores are not calibrated)'
      % (a3_p_te.mean(), a3_yte.mean()))

# [4] RFE 選到的 10 欄（把 one-hot 欄名解碼回類別）與最終 RF 的重要度
a3_prep = ml_pipe.named_steps['prep']
a3_names = a3_prep.get_feature_names_out()[ml_pipe.named_steps['rfe'].support_]
a3_cats = a3_prep.named_transformers_['encoder'].named_steps['order'].categories_

def a3_decode(n):
    if not n.startswith('encoder__'):
        return n
    col, val = n[len('encoder__'):].rsplit('_', 1)
    return '%s = %s' % (col, a3_cats[cat_features.index(col)][int(float(val))])

a3_imp = pd.Series(a3_gs.best_estimator_.feature_importances_, index=[a3_decode(n) for n in a3_names]).sort_values(ascending=False)
print('\n[4] the 10 RFE-selected columns and their importance in the final RF')
print(a3_imp.round(4).to_string())
a3_dur_share = a3_imp[[i for i in a3_imp.index if i.endswith('duration')]].sum()
print('duration enters twice (dur__ and scaler__); combined importance share %.3f' % a3_dur_share)

# [5] 切分沒有分層（stratify）：訓練 / 測試的成交比例
a3_pos_tr, a3_pos_te = a3_ytr.mean(), a3_yte.mean()
print('\n[5] share of "yes": train %.4f | test %.4f (no stratify)' % (a3_pos_tr, a3_pos_te))

A3_KPI['part_a']['final_pipeline'] = {
    'best_params': {k: (v if isinstance(v, str) else int(v)) for k, v in a3_best.items()},
    'best_cv_auc': a3_r(a3_gs.best_score_),
    'cv_auc_by_depth': {int(k): a3_r(v) for k, v in a3_by_depth.items()},
    'cv_auc_by_n_estimators_at_best': {int(k): a3_r(v) for k, v in a3_by_nest.items()},
    'n_grid': len(a3_cvres),
    'depth_sweep': [{k: (int(v) if k == 'max_depth' else a3_r(v)) for k, v in r.items()} for r in a3_sweep.to_dict('records')],
    'auc_train': a3_r(a3_auc_tr), 'auc_test': a3_r(a3_auc_te), 'gap_train_minus_test': a3_r(a3_auc_tr - a3_auc_te),
    'auc_test_target_only': a3_r(a3_auc_te_T), 'auc_test_control_only': a3_r(a3_auc_te_C),
    'rfe_features': list(a3_imp.index),
    'rfe_importance': {k.replace(' = ', '_eq_').replace('.', '_'): a3_r(v) for k, v in a3_imp.items()},
    'duration_importance_share': a3_r(a3_dur_share, 3),
    'pos_share_train_pct': a3_r(100 * a3_pos_tr, 2), 'pos_share_test_pct': a3_r(100 * a3_pos_te, 2),
    'pos_share_diff_pp': a3_r(100 * (a3_pos_te - a3_pos_tr), 2),
    'mean_pred_prob_test': a3_r(a3_p_te.mean(), 3), 'actual_yes_share_test': a3_r(a3_yte.mean(), 3),
    'rfe_has_group_columns': [n for n in a3_names if any(k in n for k in ('campaign', 'contact', 'month', 'day_of_week'))],
    'cv_minus_test': a3_r(a3_gs.best_score_ - a3_auc_te),
    'rfe_bias': {'nonnested_cv_auc': a3_r(a3_cv_flat.mean()), 'nested_cv_auc': a3_r(a3_cv_nest.mean()),
                 'nonnested_minus_nested': a3_r(a3_cv_flat.mean() - a3_cv_nest.mean()),
                 'fold_diff_min': a3_r((a3_cv_flat - a3_cv_nest).min()), 'fold_diff_max': a3_r((a3_cv_flat - a3_cv_nest).max()),
                 'same_columns_as_official': bool(np.array_equal(a3_rfe_full.support_, ml_pipe.named_steps['rfe'].support_))},
}
'''

A_SCORE = r'''
# [A3 新增] 客戶評分（cell-62～65）的診斷：只用 sample_customer 的複本，不改官方物件
from scipy.stats import spearmanr
a3_sc = sample_customer.copy()
a3_bucket_sec = {int(k): float(v) for k, v in duration.items()}
a3_bucket_cost = {k: round(v / 3600 * 50, 2) for k, v in a3_bucket_sec.items()}   # A2 時薪 A$50 下，該桶平均秒數的通話成本
print('bucket mean seconds:', a3_bucket_sec)
print('bucket call cost at A$50/h (A$):', a3_bucket_cost)
print('cost units used by the official score (100 - 2k):', {k: 100 - 2 * k for k in a3_bucket_sec if k > 0})
# 把官方的「單位」換成 A$ 才能比較（假設的換算）：官方分數「不打也買」= 200 單位、「打了才買」= 100 − 2k 單位，
# 對應 A2 的 2:1 → 200 單位 = 收益 2D，1 單位 = D / 100；D 取 A2 附錄 A 的示例 A$36 → 第 k 桶的通話成本 = 2k 單位 ≈ A$0.72k
a3_D = 36.0
a3_unit_aud = {k: round(2 * k * a3_D / 100, 2) for k in a3_bucket_sec if k > 0}
a3_cross = min([k for k in a3_unit_aud if a3_bucket_cost[k] > a3_unit_aud[k]], default=None)
print('official call cost per bucket converted to A$ (1 unit = D/100, D = A$36):', a3_unit_aud)
print('first bucket where the A2-wage call cost exceeds the official cost: %s' % a3_cross)

# cell-64 讓每位客戶都回答 11 個情境，但 campaign 不切換：訓練資料裡有沒有這些組合？
a3_supp_T0 = int(((train_data['campaign'] == '1') & (train_data['duration'] == 0)).sum())
a3_supp_Cpos = int(((train_data['campaign'] == '0') & (train_data['duration'] > 0)).sum())
a3_nT = int((a3_sc['campaign'] == '1').sum())
print('\nsample of 200: %d target-group customers, %d control-group customers' % (a3_nT, 200 - a3_nT))
print('training rows with campaign=1 and duration=0: %d ; with campaign=0 and duration>0: %d' % (a3_supp_T0, a3_supp_Cpos))

# 分數中「200·pr0」（不打也會買）這一項的佔比
a3_part0_share = float((200 * a3_sc['pr0'] / 11).sum() / a3_sc['score'].sum())
print('share of the total score coming from the 200 * pr0 term: %.3f' % a3_part0_share)

# RFE 選出的 10 欄有沒有組別欄位？沒有的話，模型分辨「打 / 沒打」只能靠 duration = 0
print('group / scheduling columns among the 10 RFE-selected columns:', A3_KPI['part_a']['final_pipeline']['rfe_has_group_columns'])
# 把目標組客戶的 pr0 改用「對照組樣貌」重算（campaign='0'、三欄 Not Applicable、duration=0），看排名變多少
a3_cols = list(campaign_data.columns)
a3_sw = a3_sc.loc[a3_sc['campaign'] == '1', a3_cols].copy()
a3_sw['campaign'] = '0'
a3_sw[['contact', 'month', 'day_of_week']] = 'Not Applicable'
a3_sw['duration'] = 0
a3_pr0_sw = pd.Series(ml_pipe.predict_proba(a3_sw)[:, 1], index=a3_sw.index)
a3_score_sw = a3_sc['score'].copy()
a3_score_sw.loc[a3_sw.index] += 200 * (a3_pr0_sw - a3_sc.loc[a3_sw.index, 'pr0']) / 11
a3_rho = spearmanr(a3_sc['score'], a3_score_sw).correlation
a3_top = set(a3_sc['score'].nlargest(20).index)
a3_top_sw = set(a3_score_sw.nlargest(20).index)
print('target-group customers: mean pr0 as run %.3f -> with a control-group profile %.3f'
      % (a3_sc.loc[a3_sw.index, 'pr0'].mean(), a3_pr0_sw.mean()))
print('Spearman rank correlation official vs switched score: %.3f ; top-20 overlap: %d / 20' % (a3_rho, len(a3_top & a3_top_sw)))

# 分數排序與實際結果（只是 200 人的小樣本）
a3_top40 = a3_sc.nlargest(40, 'score')
a3_top10 = a3_sc.nlargest(10, 'score')
print('conversion in the top 40 by score %.1f%% (%d of 40) vs all 200 %.1f%% ; target-group share in the top 40: %.0f%%'
      % (100 * (a3_top40['y'] == 'yes').mean(), (a3_top40['y'] == 'yes').sum(), 100 * (a3_sc['y'] == 'yes').mean(),
         100 * (a3_top40['campaign'] == '1').mean()))
print('top 10 by score: %d target-group / %d control-group customers, %d bought, %d with poutcome = success, mean age %.0f'
      % ((a3_top10['campaign'] == '1').sum(), (a3_top10['campaign'] == '0').sum(), (a3_top10['y'] == 'yes').sum(),
         (a3_top10['poutcome'] == 'success').sum(), a3_top10['age'].mean()))
A3_KPI['part_a']['scoring'] = {
    'bucket_mean_seconds': a3_bucket_sec, 'bucket_call_cost_aud': a3_bucket_cost,
    'sample_target_n': a3_nT, 'sample_control_n': 200 - a3_nT,
    'train_rows_campaign1_duration0': a3_supp_T0, 'train_rows_campaign0_duration_pos': a3_supp_Cpos,
    'pr0_term_share_of_score': a3_r(a3_part0_share, 3),
    'target_mean_pr0_as_run': a3_r(a3_sc.loc[a3_sw.index, 'pr0'].mean(), 3),
    'target_mean_pr0_control_profile': a3_r(a3_pr0_sw.mean(), 3),
    'spearman_official_vs_switched': a3_r(a3_rho, 3), 'top20_overlap': len(a3_top & a3_top_sw),
    'top40_conv_pct': a3_r(100 * (a3_top40['y'] == 'yes').mean(), 1),
    'sample_conv_pct': a3_r(100 * (a3_sc['y'] == 'yes').mean(), 1),
    'top40_target_share_pct': a3_r(100 * (a3_top40['campaign'] == '1').mean(), 0),
    'top40_yes': int((a3_top40['y'] == 'yes').sum()), 'sample_yes': int((a3_sc['y'] == 'yes').sum()),
    'top10_target_n': int((a3_top10['campaign'] == '1').sum()), 'top10_control_n': int((a3_top10['campaign'] == '0').sum()),
    'top10_yes': int((a3_top10['y'] == 'yes').sum()), 'top10_prev_success': int((a3_top10['poutcome'] == 'success').sum()),
    'pr0_term_share_pct': a3_r(100 * a3_part0_share, 1),
    'official_cost_aud_at_D36': a3_unit_aud, 'crossover_bucket': a3_cross,
    'bucket10_understate_x': a3_r(a3_bucket_cost[10] / a3_unit_aud[10], 1),
}
'''

A_INLINE = r'''
# [A3 新增] ydata-profiling 產生報告時會把 matplotlib 換成不互動的 Agg 畫布（matplotlib.is_interactive() 變 False），
# 之後官方 cell 的圖全部不會顯示，也不會報錯。這裡切回 notebook 內嵌顯示（Colab 預設也是 inline），並關掉報告留下的圖。
%matplotlib inline
plt.close('all')
'''

A_SEED = r'''
# [A3 新增] 分群（cell-67、68）的 KMeans 沒有設 random_state，會用 numpy 的全域亂數；先固定種子，讓同一環境重跑結果一致。
# 不同套件版本的群號仍可能不同，所以下面的解讀只用「依成交率排名」，不引用群號。
np.random.seed(RANDOM_SATE)
'''

A_CLUSTER = r'''
# [A3 新增] 分群剖面表：依成交率排序、用名次表示（不用群號）；欄位對應官方 cell-69～76 的圖
def a3_share(v, col):
    return lambda s: 100 * (s == v).mean()


a3_cl = cluster_data.groupby('cluster').agg(
    rows=('y', 'size'), conv_pct=('y', a3_share('yes', 'y')),
    target_share_pct=('campaign', a3_share('1', 'campaign')),
    mean_age=('age', 'mean'), mean_cpi=('cons.price.idx', 'mean'), mean_cci=('cons.conf.idx', 'mean'),
    mean_duration=('duration', 'mean'), prev_success_pct=('poutcome', a3_share('success', 'poutcome')),
    married_pct=('marital', a3_share('married', 'marital')), single_pct=('marital', a3_share('single', 'marital')),
    housing_yes_pct=('housing', a3_share('yes', 'housing')), default_unknown_pct=('default', a3_share('unknown', 'default')),
)
# 官方 cell-74、76 只畫成交者：成交者中 default = unknown、poutcome = success 的比例
a3_yes = cluster_data[cluster_data['y'] == 'yes'].groupby('cluster')
a3_cl['yes_default_unknown_pct'] = a3_yes['default'].apply(lambda s: 100 * (s == 'unknown').mean())
a3_cl['yes_prev_success_pct'] = a3_yes['poutcome'].apply(lambda s: 100 * (s == 'success').mean())
a3_cl = a3_cl.sort_values('conv_pct', ascending=False).reset_index(drop=True)
a3_cl.index = ['rank%d' % (i + 1) for i in range(len(a3_cl))]
print(a3_cl.round(1).to_string())
a3_overall = {'married_pct': 100 * (cluster_data['marital'] == 'married').mean(), 'single_pct': 100 * (cluster_data['marital'] == 'single').mean(),
              'housing_yes_pct': 100 * (cluster_data['housing'] == 'yes').mean(), 'prev_success_pct': 100 * (cluster_data['poutcome'] == 'success').mean(),
              'default_unknown_pct': 100 * (cluster_data['default'] == 'unknown').mean(),
              'mean_age': cluster_data['age'].mean(), 'mean_cpi': cluster_data['cons.price.idx'].mean(), 'mean_cci': cluster_data['cons.conf.idx'].mean(),
              'yes_prev_success_pct': 100 * (cluster_data.loc[cluster_data['y'] == 'yes', 'poutcome'] == 'success').mean()}
print('all training rows:', {k: round(v, 2) for k, v in a3_overall.items()})
# 手肘圖（官方 cell-67）用的是 RFE 輸出 10 欄中的第 1、2、3、5～9 欄；最終分群（cell-68）用全部 10 欄
a3_elbow_cols = [a3_decode(a3_names[i]) for i in (1, 2, 3, 5, 6, 7, 8, 9)]
a3_elbow_out = [a3_decode(a3_names[i]) for i in (0, 4)]
print('elbow uses 8 columns; left out:', a3_elbow_out)
print('inertia by k:', {k: round(v) for k, v in rss.items()})
A3_KPI['clustering'] = {   # KMeans 無 random_state：此區不列入跨次執行一致性比對
    'profile': {i: {k: a3_r(v, 2) for k, v in r.items()} for i, r in a3_cl.iterrows()},
    'overall': {k: a3_r(v, 2) for k, v in a3_overall.items()},
    'elbow_inertia': {int(k): int(round(v)) for k, v in rss.items()},
    'elbow_left_out': a3_elbow_out, 'elbow_n_columns': len(a3_elbow_cols),
    'elbow_n_increase': int(sum(rss[k + 1] > rss[k] for k in range(1, 19))),
    'overall_conv_pct': a3_r(100 * (cluster_data['y'] == 'yes').mean(), 2),
    'rest_conv_min': a3_r(a3_cl['conv_pct'].iloc[2:].min(), 1), 'rest_conv_max': a3_r(a3_cl['conv_pct'].iloc[2:].max(), 1),
    'n_clusters': len(a3_cl), 'n_rest': len(a3_cl) - 2,
    'n_all_target': int((a3_cl['target_share_pct'] >= 99).sum()),
    'n_mostly_control': int((a3_cl['target_share_pct'] <= 10).sum()),
}
'''

# ----------------------------------------------------------------------------------------------------------------
# 3) Part B code cells
# ----------------------------------------------------------------------------------------------------------------
B_SETUP = r'''
# [Part B-0] 資料口徑對照：A2 正文（原始 41,188 列）vs A3（notebook 去重後、與 cell-56 相同的切分）
import json, sys
import scipy, sklearn, matplotlib, xgboost
from IPython.display import display
from scipy.stats import rankdata
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_score, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
from sklearn.inspection import permutation_importance

pd.set_option('display.html.use_mathjax', False)    # 表格裡的 A$ 不要被當成數學式
pd.set_option('styler.html.mathjax', False)
pd.set_option('display.max_colwidth', None)          # 表格內的文字（區間、理由、設定）不截斷
PB_SEED = RANDOM_SATE                                # 123，與官方 notebook 同一個種子
PB_HOURLY = 50.0                                     # A2 假設時薪 A$50（A2 表 1 下方「主要假設與限制」框、附錄 A）
PB_ACCENT, PB_GREY, PB_LIGHT = '#1f5fa8', '#555555', '#b4b4b4'


def pb_clean(df):
    """與 cell-13 相同的清理，但不去重：三欄補 'Not Applicable'、previous / campaign 轉字串"""
    d = df.copy()
    d[['contact', 'month', 'day_of_week']] = d[['contact', 'month', 'day_of_week']].fillna('Not Applicable')
    d['previous'] = d['previous'].apply(str)
    d['campaign'] = d['campaign'].apply(str)
    return d


def pb_conv(df):
    return float((df['y'] == 'yes').mean())


def pb_pct(x, nd=2):
    return round(100 * float(x), nd)


pb_raw = pb_clean(read_data(path=csv_path))      # A2 正文口徑：原始 41,188 列（不去重）
pb_data = campaign_data.copy(deep=True)          # A3 主口徑：cell-13 去重後 35,438 列
pb_train, pb_test = train_test_split(pb_data, test_size=0.4, random_state=RANDOM_SATE)
assert (len(pb_train), len(pb_test)) == (21262, 14176)
assert pb_train.index.equals(train_data.index) and pb_test.index.equals(test_data.index)   # 與 cell-56 完全同一批列

# A2 表 4 ① 的成本公式：每通成本 c(r) = (r x 成交平均秒數 + (1 - r) x 未成交平均秒數) / 3600 x 時薪；每筆成交成本 = c(r) / r
pb_rawT, pb_rawC = pb_raw[pb_raw['campaign'] == '1'], pb_raw[pb_raw['campaign'] == '0']
PB_SEC_YES = float(pb_rawT.loc[pb_rawT['y'] == 'yes', 'duration'].mean())
PB_SEC_NO = float(pb_rawT.loc[pb_rawT['y'] == 'no', 'duration'].mean())


def pb_call_cost(r):
    return (r * PB_SEC_YES + (1 - r) * PB_SEC_NO) / 3600 * PB_HOURLY


def pb_cost_per_conv(r):
    return pb_call_cost(r) / r


PB_CALL_NO = PB_SEC_NO / 3600 * PB_HOURLY             # 未成交電話每通成本（未取整，約 A$3.07）
PB_CALL_YES = PB_SEC_YES / 3600 * PB_HOURLY           # 成交電話每通成本（未取整，約 A$6.90）


def pb_actual_cost_per_conv(df):
    """輔助口徑：所選列的實際通話秒數換成 A$ 再除以成交數（duration 只當事後成本帳，不當特徵）"""
    return float(df['duration'].sum() / 3600 * PB_HOURLY / (df['y'] == 'yes').sum())


rows = []
for name, d in [('A2 text: raw file', pb_raw), ('A3: deduplicated file', pb_data),
                ('A3: train split', pb_train), ('A3: test split', pb_test)]:
    t, c = d[d['campaign'] == '1'], d[d['campaign'] == '0']
    m = t[t['contact'] == 'cellular']
    rows.append({'data': name, 'rows': len(d), 'target_n': len(t), 'target_conv_pct': pb_pct(pb_conv(t)),
                 'control_n': len(c), 'control_conv_pct': pb_pct(pb_conv(c)),
                 'diff_pp': round(100 * (pb_conv(t) - pb_conv(c)), 2),
                 'mobile_n': len(m), 'mobile_conv_pct': pb_pct(pb_conv(m))})
pb_reconcile = pd.DataFrame(rows)
display(pb_reconcile.rename(columns={'target_n': 'target n', 'target_conv_pct': 'target conv %', 'control_n': 'control n',
                                     'control_conv_pct': 'control conv %', 'diff_pp': 'target - control (pp)',
                                     'mobile_n': 'mobile-rule n', 'mobile_conv_pct': 'mobile-rule conv %'}))

pb_r_pilot, pb_r_ctrl_raw = pb_conv(pb_rawT), pb_conv(pb_rawC)
PB_PILOT_COST = float(pb_rawT['duration'].sum() / 3600 * PB_HOURLY)   # 試點每輪通話成本（未取整，約 A$62,905）
pb_a2 = {
    'raw_rows': len(pb_raw), 'dedup_rows': len(pb_data), 'removed_rows': len(pb_raw) - len(pb_data),
    'removed_control': int(len(pb_rawC) - (pb_data['campaign'] == '0').sum()),
    'removed_target': int(len(pb_rawT) - (pb_data['campaign'] == '1').sum()),
    'sec_yes': round(PB_SEC_YES, 2), 'sec_no': round(PB_SEC_NO, 2),
    'call_cost_yes': round(PB_SEC_YES / 3600 * PB_HOURLY, 2), 'call_cost_no': round(PB_SEC_NO / 3600 * PB_HOURLY, 2),
    'pilot_target_n': len(pb_rawT), 'pilot_target_conv_pct': pb_pct(pb_r_pilot),
    'pilot_control_n': len(pb_rawC), 'pilot_control_conv_pct': pb_pct(pb_r_ctrl_raw),
    'pilot_uplift_pp': round(100 * (pb_r_pilot - pb_r_ctrl_raw), 2),
    'pilot_incremental_sales': round(len(pb_rawT) * (pb_r_pilot - pb_r_ctrl_raw), 1),
    'pilot_would_buy_share_pct': pb_pct(pb_r_ctrl_raw / pb_r_pilot, 1),
    'pilot_total_call_cost': round(pb_rawT['duration'].sum() / 3600 * PB_HOURLY, 0),
    'cost_per_conv_pilot': round(pb_cost_per_conv(pb_r_pilot), 2),
    'cost_per_conv_target_18pct': round(pb_cost_per_conv(0.18), 2),
    'mobile_raw_n': int((pb_rawT['contact'] == 'cellular').sum()),
    'mobile_raw_conv_pct': pb_pct(pb_conv(pb_rawT[pb_rawT['contact'] == 'cellular'])),
    # 兩組組成：前次行銷成功者的比例（原始全檔 vs 去重後）
    'prev_success_share_pct': {'raw_target': pb_pct((pb_rawT['poutcome'] == 'success').mean(), 2),
                               'raw_control': pb_pct((pb_rawC['poutcome'] == 'success').mean(), 2),
                               'dedup_target': pb_pct((pb_data.loc[pb_data['campaign'] == '1', 'poutcome'] == 'success').mean(), 2),
                               'dedup_control': pb_pct((pb_data.loc[pb_data['campaign'] == '0', 'poutcome'] == 'success').mean(), 2)},
}
assert (pb_a2['cost_per_conv_pilot'], pb_a2['cost_per_conv_target_18pct']) == (27.35, 20.87)   # 與 A2 表 4 ① 一致
for k, v in pb_a2.items():
    print('%-28s %s' % (k, v))
A3_KPI['part_b']['a2_recomputed'] = pb_a2
A3_KPI['part_b']['reconcile'] = [{k: (a3_r(v, 2) if not isinstance(v, str) else v) for k, v in r.items()} for r in rows]
'''

B_TRAIN = r'''
# [Part B-1] 撥號前模型：11 個撥號前欄位；只用「訓練集目標組」訓練；超參數與挑戰者比較都只用訓練資料（此格完全不碰測試集）
PB_NUM = ['age', 'cons.price.idx', 'cons.conf.idx']
PB_CAT = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'previous', 'poutcome']
PB_FEATURES = PB_NUM + PB_CAT                      # 11 欄 = A2 表 5 標「可」的欄位
PB_FEATURES_CT = PB_FEATURES + ['contact']         # 敏感度版本「+contact」
display(pd.DataFrame([
    ('duration', '通話結束才知道；對照組全為 0（duration = 0 ⇔ 沒被打），放進去等於告訴模型組別（A2 表 5 duration 列：預測當下可得＝否）'),
    ('campaign', '是「要不要打」的分組決策本身，不是客戶屬性（A2 表 5 分組列）'),
    ('contact', '本次活動實際使用的管道、對照組全空，且是比較組「手機規則」的定義欄位 → 主版本不放，另做 +contact 敏感度版（A2 表 5：條件式，排程後才知）'),
    ('month', '排程變數：同一外撥日的候選人月份相同，對當日排序沒有資訊；離線只會把時期效應灌進 AUC；對照組全空。只用來定義「同期」'),
    ('day_of_week', '排程變數，理由同 month；對照組全空'),
], columns=['excluded column', '理由']))

pb_trT = pb_train[pb_train['campaign'] == '1']
pb_y_trT = (pb_trT['y'] == 'yes').astype(int)
pb_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=PB_SEED)


def pb_pipeline(model, cat, num=None):
    """前處理包在 Pipeline 裡，只在（CV 的）訓練折上擬合"""
    prep_ = ColumnTransformer([('num', StandardScaler(), PB_NUM if num is None else num),
                               ('cat', OneHotEncoder(handle_unknown='ignore'), cat)])
    return Pipeline([('prep', prep_), ('clf', model)])


def pb_rf(n_jobs=1, **kw):
    # 重現性：樹的建立各有種子，多執行緒訓練結果固定；但多執行緒 predict_proba 的加總順序不固定（約 1e-16 的差），
    # 而 11 個撥號前欄位下有很多完全相同的客戶（同分），先後一變，名單就不同。所以預測一律用單執行緒。
    return RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=PB_SEED, n_jobs=n_jobs, **kw)


def pb_select_rf(X, y, cat, label):
    """A3 自訂、只看訓練資料的選模規則（用來代理 A2 的 ML③；A2 只規定『訓練與測試 AUC 差 ≤ 0.05』，沒有這條）：
    在『in-sample 訓練 AUC − 平均 CV AUC ≤ 0.05』的設定中，取平均 CV AUC 最高者"""
    grid = GridSearchCV(pb_pipeline(pb_rf(n_jobs=1), cat), {'clf__max_depth': [5, 7, 9], 'clf__min_samples_leaf': [1, 20]},
                        scoring='roc_auc', cv=pb_cv, n_jobs=-1, refit=False).fit(X, y)
    rows_, fitted = [], {}
    for p, cv_m, cv_s in zip(grid.cv_results_['params'], grid.cv_results_['mean_test_score'], grid.cv_results_['std_test_score']):
        key = (p['clf__max_depth'], p['clf__min_samples_leaf'])
        m = pb_pipeline(pb_rf(n_jobs=-1, max_depth=key[0], min_samples_leaf=key[1]), cat).fit(X, y)
        m.set_params(clf__n_jobs=1)   # 多執行緒 predict_proba 的加總順序不固定，同分客戶的先後會變；預測一律單執行緒
        tr = roc_auc_score(y, m.predict_proba(X)[:, 1])
        fitted[key] = m
        rows_.append({'model': label, 'max_depth': key[0], 'min_samples_leaf': key[1], 'cv_auc': cv_m, 'cv_sd': cv_s,
                      'train_auc_in_sample': tr, 'train_minus_cv': tr - cv_m})
    tab = pd.DataFrame(rows_)
    tab['gap_ok'] = tab['train_minus_cv'] <= 0.05
    pool = tab[tab['gap_ok']] if tab['gap_ok'].any() else tab.nsmallest(1, 'train_minus_cv')
    best = pool.sort_values(['cv_auc', 'max_depth'], ascending=[False, True]).iloc[0]
    key = (int(best['max_depth']), int(best['min_samples_leaf']))
    tab['selected'] = (tab['max_depth'] == key[0]) & (tab['min_samples_leaf'] == key[1])
    i = [k for k, p in enumerate(grid.cv_results_['params']) if (p['clf__max_depth'], p['clf__min_samples_leaf']) == key][0]
    folds = np.array([grid.cv_results_['split%d_test_score' % f][i] for f in range(pb_cv.get_n_splits())])
    return tab, fitted[key], {'max_depth': key[0], 'min_samples_leaf': key[1], 'n_estimators': 300}, folds


pb_main_tab, pb_main, pb_main_params, pb_main_folds = pb_select_rf(pb_trT[PB_FEATURES], pb_y_trT, PB_CAT, 'RF pre-call 11 (main)')
pb_ct_tab, pb_ct, pb_ct_params, _ = pb_select_rf(pb_trT[PB_FEATURES_CT], pb_y_trT, PB_CAT + ['contact'], 'RF +contact (sensitivity)')
pb_lr = pb_pipeline(LogisticRegression(class_weight='balanced', max_iter=2000), PB_CAT)
pb_lr_cv = cross_val_score(pb_lr, pb_trT[PB_FEATURES], pb_y_trT, cv=pb_cv, scoring='roc_auc')
pb_lr.fit(pb_trT[PB_FEATURES], pb_y_trT)
pb_lr_train = roc_auc_score(pb_y_trT, pb_lr.predict_proba(pb_trT[PB_FEATURES])[:, 1])

# A2 表 7（XGBoost 列）：挑戰者要「與隨機森林用同一批驗證折、同一指標重比；勝出幅度大於不同隨機種子間的波動才替換」。
# 照字面執行（只用訓練資料）：XGB 先在同樣 5 折上從 4 組設定選一組；再用 5 個隨機種子（123–127，每個種子同時改變
# 5 折的切法與模型的 random_state）重比 RF 選定設定與 XGB 選定設定。替換條件：5 個種子的平均勝出幅度
# 大於 RF 的 CV AUC 在種子之間的最大差距（max − min），而且每個種子都勝出。
from xgboost import XGBClassifier
pb_ratio = float((pb_y_trT == 0).sum() / (pb_y_trT == 1).sum())
pb_xgb_grid = GridSearchCV(pb_pipeline(XGBClassifier(n_estimators=200, scale_pos_weight=pb_ratio, random_state=PB_SEED, n_jobs=1), PB_CAT),
                           {'clf__max_depth': [3, 5], 'clf__learning_rate': [0.05, 0.1]},
                           scoring='roc_auc', cv=pb_cv, n_jobs=-1, refit=False).fit(pb_trT[PB_FEATURES], pb_y_trT)
pb_xi = int(np.argmax(pb_xgb_grid.cv_results_['mean_test_score']))
pb_xgb_cv, pb_xgb_sd = float(pb_xgb_grid.cv_results_['mean_test_score'][pb_xi]), float(pb_xgb_grid.cv_results_['std_test_score'][pb_xi])
pb_xgb_params = {k.replace('clf__', ''): v for k, v in pb_xgb_grid.cv_results_['params'][pb_xi].items()}
pb_xgb_folds = np.array([pb_xgb_grid.cv_results_['split%d_test_score' % f][pb_xi] for f in range(pb_cv.get_n_splits())])
pb_main_cv = float(pb_main_tab.loc[pb_main_tab['selected'], 'cv_auc'].iloc[0])
pb_main_sd = float(pb_main_tab.loc[pb_main_tab['selected'], 'cv_sd'].iloc[0])
print('same 5 folds, XGB minus RF per fold:', np.round(pb_xgb_folds - pb_main_folds, 4))
pb_seed_rows = []
for s_ in range(PB_SEED, PB_SEED + 5):
    cv_ = StratifiedKFold(n_splits=5, shuffle=True, random_state=s_)
    rf_ = pb_pipeline(RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=s_, n_jobs=1,
                                             max_depth=pb_main_params['max_depth'], min_samples_leaf=pb_main_params['min_samples_leaf']), PB_CAT)
    xg_ = pb_pipeline(XGBClassifier(n_estimators=200, scale_pos_weight=pb_ratio, random_state=s_, n_jobs=1, **pb_xgb_params), PB_CAT)
    a_ = cross_val_score(rf_, pb_trT[PB_FEATURES], pb_y_trT, cv=cv_, scoring='roc_auc', n_jobs=-1).mean()
    b_ = cross_val_score(xg_, pb_trT[PB_FEATURES], pb_y_trT, cv=cv_, scoring='roc_auc', n_jobs=-1).mean()
    pb_seed_rows.append({'seed': s_, 'RF CV AUC': a_, 'XGB CV AUC': b_, 'XGB - RF': b_ - a_})
pb_seed_tab = pd.DataFrame(pb_seed_rows)
pb_margin = float(pb_seed_tab['XGB - RF'].mean())
pb_rf_seed_range = float(pb_seed_tab['RF CV AUC'].max() - pb_seed_tab['RF CV AUC'].min())
pb_xgb_replace = bool(pb_margin > pb_rf_seed_range and (pb_seed_tab['XGB - RF'] > 0).all())
assert abs(pb_seed_tab.loc[0, 'RF CV AUC'] - pb_main_cv) < 1e-9          # 種子 123 = 上面選模用的同一批折
# 依表 7 勝出的挑戰者在整個訓練集目標組上擬合一次；B-2 起每一條都與 RF 並列，B-11 對十條標準做完整的平行評估
pb_xgb = pb_pipeline(XGBClassifier(n_estimators=200, scale_pos_weight=pb_ratio, random_state=PB_SEED, n_jobs=1, **pb_xgb_params), PB_CAT)
pb_xgb.fit(pb_trT[PB_FEATURES], pb_y_trT)

display(pd.concat([pb_main_tab, pb_ct_tab], ignore_index=True).round(4))
display(pd.DataFrame([('LR baseline (balanced)', pb_lr_cv.mean(), pb_lr_cv.std(), '-'),
                      ('RF main (selected)', pb_main_cv, pb_main_sd, str(pb_main_params)),
                      ('XGB challenger (best of 4, scale_pos_weight = %.2f)' % pb_ratio, pb_xgb_cv, pb_xgb_sd, str(pb_xgb_params))],
                     columns=['model (same 5 folds, training target group only)', 'CV AUC', 'fold sd', 'settings']).round(4))
print('A2 table 7 replacement check: RF vs XGB (selected settings) over 5 random seeds')
display(pb_seed_tab.round(4))
print('training target group: %d rows, %d conversions (%.2f%%)' % (len(pb_trT), pb_y_trT.sum(), 100 * pb_y_trT.mean()))
print('LR baseline (balanced): CV AUC %.4f (sd %.4f), train in-sample %.4f' % (pb_lr_cv.mean(), pb_lr_cv.std(), pb_lr_train))
print('A2 table 7: mean margin XGB - RF over 5 seeds %+.4f vs RF seed-to-seed range %.4f; XGB ahead on every seed: %s '
      '-> XGB replaces RF as the candidate: %s' % (pb_margin, pb_rf_seed_range, bool((pb_seed_tab['XGB - RF'] > 0).all()), pb_xgb_replace))
print('selected main:', pb_main_params, '| selected +contact:', pb_ct_params)


def pb_tab_records(tab):
    return [{k: (a3_r(v) if not isinstance(v, str) else v) for k, v in r.items()} for r in tab.to_dict('records')]


A3_KPI['part_b']['models'] = {
    'features_main': PB_FEATURES, 'features_sensitivity': PB_FEATURES_CT,
    'train_target_rows': len(pb_trT), 'train_target_conversions': int(pb_y_trT.sum()),
    'train_target_conv_pct': a3_r(100 * pb_y_trT.mean(), 2),
    'main_params': pb_main_params, 'contact_params': pb_ct_params,
    'main_grid': pb_tab_records(pb_main_tab), 'contact_grid': pb_tab_records(pb_ct_tab),
    'main_selected': pb_tab_records(pb_main_tab[pb_main_tab['selected']])[0],
    'main_best_cv_overall': pb_tab_records(pb_main_tab.sort_values('cv_auc', ascending=False).head(1))[0],
    'main_rejected_by_gap': pb_tab_records(pb_main_tab[~pb_main_tab['gap_ok']]),
    'contact_selected': pb_tab_records(pb_ct_tab[pb_ct_tab['selected']])[0],
    'rf_minus_lr_cv': a3_r(pb_main_cv - pb_lr_cv.mean()),
    'lr_cv_auc': a3_r(pb_lr_cv.mean()), 'lr_cv_sd': a3_r(pb_lr_cv.std()), 'lr_train_auc': a3_r(pb_lr_train),
    'rf_cv_sd': a3_r(pb_main_sd), 'xgb_cv_auc': a3_r(pb_xgb_cv), 'xgb_cv_sd': a3_r(pb_xgb_sd),
    'xgb_params': {k: (float(v) if isinstance(v, float) else int(v)) for k, v in pb_xgb_params.items()},
    'xgb_scale_pos_weight': a3_r(pb_ratio, 2), 'xgb_minus_rf_cv': a3_r(pb_xgb_cv - pb_main_cv), 'xgb_replace': pb_xgb_replace,
    'xgb_minus_rf_by_fold': [a3_r(v) for v in pb_xgb_folds - pb_main_folds],
    'xgb_folds_better': int((pb_xgb_folds > pb_main_folds).sum()),
    'xgb_minus_rf_fold_min': a3_r((pb_xgb_folds - pb_main_folds).min()), 'xgb_minus_rf_fold_max': a3_r((pb_xgb_folds - pb_main_folds).max()),
    'table7_rule': {'seeds': [int(v) for v in pb_seed_tab['seed']], 'rf_cv': [a3_r(v) for v in pb_seed_tab['RF CV AUC']],
                    'xgb_cv': [a3_r(v) for v in pb_seed_tab['XGB CV AUC']], 'margin_mean': a3_r(pb_margin),
                    'margin_min': a3_r(pb_seed_tab['XGB - RF'].min()), 'margin_max': a3_r(pb_seed_tab['XGB - RF'].max()),
                    'rf_seed_range': a3_r(pb_rf_seed_range), 'rf_seed_sd': a3_r(pb_seed_tab['RF CV AUC'].std(ddof=1)),
                    'xgb_ahead_every_seed': bool((pb_seed_tab['XGB - RF'] > 0).all()), 'replace': pb_xgb_replace},
}
'''

B_SCORE = r'''
# [Part B-2] 從這裡開始用測試集：模型與超參數都已固定，之後的數字都是對這些固定模型的報告（含敏感度與診斷），不回頭改模型。
# 業務②的判準（B = 1,000、種子 123、percentile 區間下限 > 0）是評估計畫原本訂的；B-3 另加的 B = 5,000、basic 區間與換種子
# 是看過第一次結果之後才加的穩健性檢查，不改判準。報 ML①（概念驗證）、ML②（撥號前）、ML③（過擬合差）
pb_teT = pb_test[pb_test['campaign'] == '1'].copy()
pb_teC = pb_test[pb_test['campaign'] == '0'].copy()
pb_y_teT = (pb_teT['y'] == 'yes').astype(int).to_numpy()
pb_teT['s'] = pb_main.predict_proba(pb_teT[PB_FEATURES])[:, 1]
pb_teC['s'] = pb_main.predict_proba(pb_teC[PB_FEATURES])[:, 1]
pb_teT['s_ct'] = pb_ct.predict_proba(pb_teT[PB_FEATURES_CT])[:, 1]
pb_teT['s_lr'] = pb_lr.predict_proba(pb_teT[PB_FEATURES])[:, 1]
pb_teT['s_x'] = pb_xgb.predict_proba(pb_teT[PB_FEATURES])[:, 1]          # XGB（依 A2 表 7 勝出的候選）
pb_teC['s_x'] = pb_xgb.predict_proba(pb_teC[PB_FEATURES])[:, 1]
# (cpi, cci) 時期：兩個指標每月公布一次，同一組 (cpi, cci) ＝ 同一個年月；資料跨年，所以同一個「月份」可能包含好幾個時期
for d_ in (pb_teT, pb_teC):
    d_['period'] = d_['cons.price.idx'].map('{:.3f}'.format) + ' | ' + d_['cons.conf.idx'].map('{:.1f}'.format)


def pb_auc(y, s):
    """ROC-AUC 的秩公式（同分取平均秩；與 sklearn roc_auc_score 相同，但快，供 bootstrap 用）"""
    y = np.asarray(y).astype(bool)
    r = rankdata(s)
    n1 = y.sum()
    n0 = len(y) - n1
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def pb_within_auc(df, key, col='s'):
    """每一層（月份或時期）內各算 AUC，再依該層列數加權；只有一種結果的層不計"""
    w = []
    for k, g in df.groupby(key):
        yy = (g['y'] == 'yes').to_numpy()
        if 0 < yy.sum() < len(yy):
            w.append((k, len(g), pb_auc(yy, g[col])))
    return sum(n * a for _, n, a in w) / sum(n for _, n, _ in w), w


pb_poc = A3_KPI['part_a']['final_pipeline']           # ML①：官方 ml_pipe（cell-59 的值，含 duration）
pb_auc_te = pb_auc(pb_y_teT, pb_teT['s'])
assert abs(pb_auc_te - roc_auc_score(pb_y_teT, pb_teT['s'])) < 1e-12
pb_auc_tr = roc_auc_score(pb_y_trT, pb_main.predict_proba(pb_trT[PB_FEATURES])[:, 1])
pb_auc_ct = pb_auc(pb_y_teT, pb_teT['s_ct'])
pb_auc_lr = pb_auc(pb_y_teT, pb_teT['s_lr'])
pb_auc_wm, pb_wm = pb_within_auc(pb_teT, 'month')       # 月內 AUC（扣掉「不同月份轉換率不同」）
pb_auc_wp, pb_wp = pb_within_auc(pb_teT, 'period')      # 時期內 AUC（扣掉「不同年月轉換率不同」）
pb_ppm = pb_teT.groupby('month')['period'].nunique()
pb_auc_x = pb_auc(pb_y_teT, pb_teT['s_x'])
pb_auc_x_tr = roc_auc_score(pb_y_trT, pb_xgb.predict_proba(pb_trT[PB_FEATURES])[:, 1])
pb_auc_x_wm, _ = pb_within_auc(pb_teT, 'month', 's_x')
pb_auc_x_wp, _ = pb_within_auc(pb_teT, 'period', 's_x')

# 受控診斷：同樣設定的撥號前 RF 只多加 duration（量 duration 的份量；不是候選模型）
pb_dur = pb_pipeline(pb_rf(n_jobs=-1, max_depth=pb_main_params['max_depth'], min_samples_leaf=pb_main_params['min_samples_leaf']),
                     PB_CAT, PB_NUM + ['duration']).fit(pb_trT[PB_FEATURES + ['duration']], pb_y_trT)
pb_dur.set_params(clf__n_jobs=1)
pb_auc_dur = pb_auc(pb_y_teT, pb_dur.predict_proba(pb_teT[PB_FEATURES + ['duration']])[:, 1])

pb_ml_tab = pd.DataFrame([
    ('ML① proof of concept (official ml_pipe, with duration)', 'all test rows (14,176)', pb_poc['auc_train'], pb_poc['auc_test'], None),
    ('ML② pre-call RF (main)', 'test target group (7,094)', pb_auc_tr, pb_auc_te, pb_main_cv),
    ('   within-month AUC, weighted by rows', 'test target group', None, pb_auc_wm, None),
    ('   within-period AUC ((cpi, cci) = one year-month), weighted', 'test target group', None, pb_auc_wp, None),
    ('   LR baseline (same 11 features)', 'test target group', pb_lr_train, pb_auc_lr, float(pb_lr_cv.mean())),
    ('   RF +contact (sensitivity)', 'test target group', None, pb_auc_ct, float(pb_ct_tab.loc[pb_ct_tab['selected'], 'cv_auc'].iloc[0])),
    ('   XGB (A2 table 7 winner)', 'test target group', pb_auc_x_tr, pb_auc_x, pb_xgb_cv),
    ('   XGB: within-month AUC', 'test target group', None, pb_auc_x_wm, None),
    ('   XGB: within-period AUC', 'test target group', None, pb_auc_x_wp, None),
    ('   diagnostic: same RF + duration', 'test target group', None, pb_auc_dur, None),
], columns=['model', 'evaluated on', 'train AUC (in-sample)', 'test AUC', 'CV AUC (train)'])
pb_ml_tab['train - test'] = pb_ml_tab['train AUC (in-sample)'] - pb_ml_tab['test AUC']
display(pb_ml_tab.round(4).astype(object).where(pb_ml_tab.notna(), '-'))   # '-' = 不適用
print('within-month AUC by month:', {m: round(a, 3) for m, _, a in pb_wm})
print('(cpi, cci) periods in the test target group: %d; periods per month: %s' % (pb_teT['period'].nunique(), pb_ppm.to_dict()))
print('test target group: %d rows, %d conversions (%.2f%%)' % (len(pb_teT), pb_y_teT.sum(), 100 * pb_y_teT.mean()))

A3_KPI['part_b']['ml'] = {
    'ml1_poc_train_auc': pb_poc['auc_train'], 'ml1_poc_test_auc': pb_poc['auc_test'],
    'ml1_poc_gap': pb_poc['gap_train_minus_test'],
    'ml1_poc_target_only_auc': pb_poc['auc_test_target_only'], 'ml1_poc_control_only_auc': pb_poc['auc_test_control_only'],
    'ml2_test_auc': a3_r(pb_auc_te), 'ml2_within_month_auc': a3_r(pb_auc_wm), 'ml2_within_period_auc': a3_r(pb_auc_wp),
    'ml2_cv_auc': a3_r(pb_main_cv),
    'ml1_target_only_minus_ml2': a3_r(pb_poc['auc_test_target_only'] - pb_auc_te),
    'ml2_with_duration_auc': a3_r(pb_auc_dur), 'duration_gain_controlled': a3_r(pb_auc_dur - pb_auc_te),
    'poc_minus_controlled_other': a3_r(pb_poc['auc_test_target_only'] - pb_auc_dur),
    'ml2_rf_minus_lr_test': a3_r(pb_auc_te - pb_auc_lr),
    'ml2_minus_within_month': a3_r(pb_auc_te - pb_auc_wm), 'ml2_minus_within_period': a3_r(pb_auc_te - pb_auc_wp),
    'ml2_lr_test_auc': a3_r(pb_auc_lr), 'ml2_contact_test_auc': a3_r(pb_auc_ct),
    'ml2_within_month_by_month': {m: a3_r(a, 3) for m, _, a in pb_wm},
    'xgb_test_auc': a3_r(pb_auc_x), 'xgb_train_auc': a3_r(pb_auc_x_tr), 'xgb_gap': a3_r(pb_auc_x_tr - pb_auc_x),
    'xgb_within_month_auc': a3_r(pb_auc_x_wm), 'xgb_within_period_auc': a3_r(pb_auc_x_wp),
    'n_periods_test_target': int(pb_teT['period'].nunique()),
    'periods_per_month_min': int(pb_ppm.min()), 'periods_per_month_max': int(pb_ppm.max()),
    'ml3_precall_train_auc': a3_r(pb_auc_tr), 'ml3_precall_gap': a3_r(pb_auc_tr - pb_auc_te),
    'ml3_precall_cv_minus_test': a3_r(pb_main_cv - pb_auc_te),
    'test_target_rows': len(pb_teT), 'test_target_conversions': int(pb_y_teT.sum()),
    'test_target_conv_pct': a3_r(100 * pb_y_teT.mean(), 2),
    'test_control_rows': len(pb_teC), 'test_control_conv_pct': a3_r(100 * pb_conv(pb_teC), 2),
}
'''

B_B2 = r'''
# [Part B-3] 業務②（上線硬門檻）：同期、同通數下，ML 名單 vs 手機規則
# 主結果：同期＝同月份。每月 K_m = 該月手機通數；ML 名單 = 該月撥號前分數最高的 K_m 人（可以包含市話客戶）
# 穩健性：同期＝同一 (cpi, cci) 時期（同一個年月），做法相同
# 判準（評估計畫原本訂的）：各月內 bootstrap B = 1,000、種子 123，差 > 0 且 95% percentile 區間下限 > 0 才算通過
# 看過第一次結果後才加的穩健性檢查（不改判準，細節見附錄 A）：B = 5,000、偏差校正的 basic 區間、另外 10 個種子
PB_B2_B = 1000
PB_B2_B_CHECK = 5000


def pb_matched_idx(df, col, key='month'):
    idx = []
    for _, g in df.groupby(key):
        k = int((g['contact'] == 'cellular').sum())
        idx.extend(g.sort_values(col, ascending=False, kind='mergesort').index[:k])
    return pd.Index(idx)


def pb_boot_matched(df, col, key='month', B=PB_B2_B, seed=PB_SEED, chunk=1000):
    """各層（月份或時期）內有放回重抽列（以多項分配計數實作，等同逐列重抽），每次依重抽後的手機通數重選名單；
    回傳 B 個「ML − 手機」轉換率差。ML 名單與手機組大量重疊，不能用獨立兩比例檢定。同分時沿用點估計的排序。"""
    rng = np.random.default_rng(seed)
    out = []
    groups = []
    for _, g in df.groupby(key):
        g = g.sort_values(col, ascending=False, kind='mergesort')
        groups.append(((g['y'] == 'yes').to_numpy(dtype=float), (g['contact'] == 'cellular').to_numpy()))
    for b0 in range(0, B, chunk):
        nb = min(chunk, B - b0)
        ml, mob, n = np.zeros(nb), np.zeros(nb), np.zeros(nb)
        for y, c in groups:
            m = len(y)
            cnt = rng.multinomial(m, np.full(m, 1.0 / m), size=nb)
            k = cnt[:, c].sum(axis=1)
            take = np.clip(k[:, None] - (np.cumsum(cnt, axis=1) - cnt), 0, cnt)   # 依分數由高往低取，取滿 k 為止
            ml += take @ y
            mob += cnt[:, c] @ y[c]
            n += k
        out.append((ml - mob) / n)
    return np.concatenate(out)


def pb_ci(boot, est):
    """percentile 區間，以及偏差校正的 basic 區間（2θ − 上界, 2θ − 下界）；重抽會複製高分成交者，bootstrap 分布往上偏"""
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {'pct_lo': lo, 'pct_hi': hi, 'basic_lo': 2 * est - hi, 'basic_hi': 2 * est - lo, 'boot_mean': float(boot.mean())}


def pb_compare(key, col):
    L = pb_teT.loc[pb_matched_idx(pb_teT, col, key)]
    d = pb_conv(L) - pb_conv(pb_mob)
    ci = pb_ci(pb_boot_matched(pb_teT, col, key, B=PB_B2_B), d)
    ok = bool(d > 0 and ci['pct_lo'] > 0)                  # 判準：差 > 0 且 95% percentile 區間下限 > 0（B = 1,000）
    return L, d, ci, ok


pb_mob = pb_teT[pb_teT['contact'] == 'cellular']
pb_K = len(pb_mob)
pb_L, pb_diff, pb_ci_m, pb_b2_pass = pb_compare('month', 's')
pb_Lct, pb_diff_ct, pb_ci_ct, pb_b2_ct_pass = pb_compare('month', 's_ct')
pb_Lp, pb_diff_p, pb_ci_p, pb_b2_p_pass = pb_compare('period', 's')
pb_Lpct, pb_diff_pct, pb_ci_pct, pb_b2_pct_pass = pb_compare('period', 's_ct')
pb_Lx, pb_diff_x, pb_ci_x, pb_b2_x_pass = pb_compare('month', 's_x')          # XGB（依 A2 表 7 勝出的候選）
pb_Lpx, pb_diff_px, pb_ci_px, pb_b2_px_pass = pb_compare('period', 's_x')
assert len(pb_L) == pb_K == len(pb_Lct) == len(pb_Lp) == len(pb_Lpct) == len(pb_Lx) == len(pb_Lpx)
# 穩健性檢查（事後加、不改判準）：同月配對的 RF、+contact、XGB 三份名單，(a) B = 5,000；(b) 另外 10 個種子（B = 1,000）的 percentile 下限
pb_ci5k = {c: pb_ci(pb_boot_matched(pb_teT, c, 'month', B=PB_B2_B_CHECK), d)
           for c, d in (('s', pb_diff), ('s_ct', pb_diff_ct), ('s_x', pb_diff_x))}
pb_seed_lo = {c: [float(np.percentile(pb_boot_matched(pb_teT, c, 'month', B=PB_B2_B, seed=PB_SEED + i), 2.5)) for i in range(1, 11)]
              for c in ('s', 's_ct', 's_x')}
pb_ci_main = {'s': pb_ci_m, 's_ct': pb_ci_ct, 's_x': pb_ci_x}


def pb_borderline(c):
    """下限在 0 附近：11 個種子（123 與另外 10 個）有的 > 0、有的 ≤ 0，或種子 123 的下限離 0 不到 0.05 pp"""
    lows = pb_seed_lo[c] + [pb_ci_main[c]['pct_lo']]
    return bool((min(lows) <= 0 < max(lows)) or abs(pb_ci_main[c]['pct_lo']) < 0.0005)


pb_ct_borderline, pb_x_borderline = pb_borderline('s_ct'), pb_borderline('s_x')

pb_r_mob, pb_r_L, pb_r_Lct, pb_r_Lp, pb_r_Lpct = map(pb_conv, (pb_mob, pb_L, pb_Lct, pb_Lp, pb_Lpct))
pb_r_rand = pb_conv(pb_teT)


def pb_mix_random(key):
    """依手機規則在各層（月份或時期）的通數組成隨機抽的期望轉換率"""
    g = pb_teT.groupby(key)
    return float(sum(int((x['contact'] == 'cellular').sum()) * pb_conv(x) for _, x in g) / pb_K)


pb_r_rand_mm, pb_r_rand_pm = pb_mix_random('month'), pb_mix_random('period')
pb_month_rows = []
for m, g in pb_teT.groupby('month'):
    gm = g[g['contact'] == 'cellular']
    pb_month_rows.append({'month': m, 'rows': len(g), 'K_m (mobile calls)': len(gm), 'month conv %': 100 * pb_conv(g),
                          'mobile rule conv %': 100 * pb_conv(gm) if len(gm) else np.nan,
                          'ML list conv %': 100 * pb_conv(pb_L[pb_L['month'] == m]) if len(gm) else np.nan,
                          'ML +contact conv %': 100 * pb_conv(pb_Lct[pb_Lct['month'] == m]) if len(gm) else np.nan,
                          '(cpi, cci) periods': g['period'].nunique()})
pb_month_tab = pd.DataFrame(pb_month_rows)
pb_month_tab['_o'] = pb_month_tab['month'].map({m: i for i, m in enumerate(['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])})
pb_month_tab = pb_month_tab.sort_values('_o').drop(columns='_o').reset_index(drop=True)
pb_r_pooled = pb_conv(pb_teT.sort_values('s', ascending=False, kind='mergesort').head(pb_K))
display(pb_month_tab.round(2))


def pb_iv(lo, hi):
    return '[%+.2f, %+.2f]' % (100 * lo, 100 * hi)


def pb_row(name, r, n=None, d=None, ci=None, ok=None, ci5=None):
    n = pb_K if n is None else n
    if d is None:
        return (name, n, 100 * r, '', '', '', '', '')
    return (name, n, 100 * r, '%+.2f' % (100 * d), pb_iv(ci['pct_lo'], ci['pct_hi']), 'yes' if ok else 'no',
            pb_iv(ci['basic_lo'], ci['basic_hi']), '' if ci5 is None else pb_iv(ci5['pct_lo'], ci5['pct_hi']))


display(pd.DataFrame([
    pb_row('Random calling (all 7,094, unmatched)', pb_r_rand, len(pb_teT)),
    pb_row('Random with the mobile-rule month mix (expected)', pb_r_rand_mm),
    pb_row('Random with the mobile-rule (cpi, cci) period mix (expected)', pb_r_rand_pm),
    pb_row('Mobile rule (contact = cellular)', pb_r_mob),
    pb_row('RF list, same calls per month (MAIN)', pb_r_L, None, pb_diff, pb_ci_m, pb_b2_pass, pb_ci5k['s']),
    pb_row('RF list, same calls per month, +contact', pb_r_Lct, None, pb_diff_ct, pb_ci_ct, pb_b2_ct_pass, pb_ci5k['s_ct']),
    pb_row('XGB list (A2 table 7 winner), same calls per month', pb_conv(pb_Lx), None, pb_diff_x, pb_ci_x, pb_b2_x_pass, pb_ci5k['s_x']),
    pb_row('RF list, same calls per period (robustness)', pb_r_Lp, None, pb_diff_p, pb_ci_p, pb_b2_p_pass),
    pb_row('RF list, same calls per period, +contact', pb_r_Lpct, None, pb_diff_pct, pb_ci_pct, pb_b2_pct_pass),
    pb_row('XGB list, same calls per period', pb_conv(pb_Lpx), None, pb_diff_px, pb_ci_px, pb_b2_px_pass),
    pb_row('Counter-example: pooled top-K, no matching', pb_r_pooled),
], columns=['list', 'calls', 'conversion %', 'list - mobile (pp)', '95% CI, B = 1,000 (plan)', 'gate passed (plan rule)',
            'basic CI, B = 1,000 (check)', '95% CI, B = 5,000 (check)']).round(2))
print('plan rule: difference > 0 and lower bound of the 95% percentile CI (B = 1,000, seed 123) > 0')
print('bootstrap mean vs point estimate (RF month): %+.3f vs %+.3f pp' % (100 * pb_ci_m['boot_mean'], 100 * pb_diff))
for c_, lab_ in (('s', 'RF'), ('s_ct', 'RF +contact'), ('s_x', 'XGB')):
    print('%-12s percentile lower bound, seed 123: %+.3f pp; 10 other seeds: [%+.3f, %+.3f] pp, %d of 10 above 0'
          % (lab_, 100 * pb_ci_main[c_]['pct_lo'], 100 * min(pb_seed_lo[c_]), 100 * max(pb_seed_lo[c_]), sum(v > 0 for v in pb_seed_lo[c_])))

# 同層同深度曲線（圖 1、圖 2 與業務①用）：每月（或每個時期）都只打分數前 d 比例
pb_depths = np.round(np.arange(0.05, 1.0001, 0.05), 2)


def pb_depth_curve(df, col, key='month'):
    tot = int((df['y'] == 'yes').sum())
    out = []
    for d in pb_depths:
        sel = pd.concat([g.sort_values(col, ascending=False, kind='mergesort').head(int(round(d * len(g))))
                         for _, g in df.groupby(key)])
        r = pb_conv(sel)
        out.append({'depth': d, 'called': len(sel), 'called_share': len(sel) / len(df), 'conv': r,
                    'captured_share': (sel['y'] == 'yes').sum() / tot,
                    'cost_formula': pb_cost_per_conv(r), 'cost_actual': pb_actual_cost_per_conv(sel)})
    return pd.DataFrame(out)


pb_curve = pb_depth_curve(pb_teT, 's', 'month')
pb_curve_p = pb_depth_curve(pb_teT, 's', 'period')


def pb_ci_rec(d, ci, prefix='', ci5=None):
    out = {prefix + 'diff_pp': a3_r(100 * d, 2), prefix + 'ci_low_pp': a3_r(100 * ci['pct_lo'], 2), prefix + 'ci_high_pp': a3_r(100 * ci['pct_hi'], 2),
           prefix + 'basic_low_pp': a3_r(100 * ci['basic_lo'], 2), prefix + 'basic_high_pp': a3_r(100 * ci['basic_hi'], 2),
           prefix + 'boot_mean_pp': a3_r(100 * ci['boot_mean'], 2)}
    if ci5 is not None:
        out.update({prefix + 'b5k_ci_low_pp': a3_r(100 * ci5['pct_lo'], 2), prefix + 'b5k_ci_high_pp': a3_r(100 * ci5['pct_hi'], 2),
                    prefix + 'b5k_basic_low_pp': a3_r(100 * ci5['basic_lo'], 2), prefix + 'b5k_basic_high_pp': a3_r(100 * ci5['basic_hi'], 2)})
    return out


A3_KPI['part_b']['b2'] = {
    'K_mobile_calls': pb_K, 'mobile_conv_pct': a3_r(100 * pb_r_mob, 2), 'ml_conv_pct': a3_r(100 * pb_r_L, 2),
    'ml_contact_conv_pct': a3_r(100 * pb_r_Lct, 2), 'random_conv_pct': a3_r(100 * pb_r_rand, 2),
    'random_month_matched_conv_pct': a3_r(100 * pb_r_rand_mm, 2), 'random_period_matched_conv_pct': a3_r(100 * pb_r_rand_pm, 2),
    'pooled_topK_conv_pct': a3_r(100 * pb_r_pooled, 2),
    'pooled_minus_mobile_pp': a3_r(100 * (pb_r_pooled - pb_r_mob), 2), 'pooled_minus_ml_pp': a3_r(100 * (pb_r_pooled - pb_r_L), 2),
    'called_share_pct': a3_r(100 * pb_K / len(pb_teT), 1),
    'ml_captured_pct': a3_r(100 * (pb_L['y'] == 'yes').sum() / pb_y_teT.sum(), 1),
    'ml_period_captured_pct': a3_r(100 * (pb_Lp['y'] == 'yes').sum() / pb_y_teT.sum(), 1),
    'mobile_captured_pct': a3_r(100 * (pb_mob['y'] == 'yes').sum() / pb_y_teT.sum(), 1),
    'random_mm_captured_pct': a3_r(100 * pb_r_rand_mm * pb_K / pb_y_teT.sum(), 1),
    'random_pm_captured_pct': a3_r(100 * pb_r_rand_pm * pb_K / pb_y_teT.sum(), 1),
    **pb_ci_rec(pb_diff, pb_ci_m, ci5=pb_ci5k['s']), 'pass': pb_b2_pass,
    **pb_ci_rec(pb_diff_ct, pb_ci_ct, 'contact_', pb_ci5k['s_ct']), 'contact_pass': pb_b2_ct_pass, 'contact_borderline': pb_ct_borderline,
    'seed_low_min_pp': a3_r(100 * min(pb_seed_lo['s']), 2), 'seed_low_max_pp': a3_r(100 * max(pb_seed_lo['s']), 2),
    'seed_n_above0': int(sum(v > 0 for v in pb_seed_lo['s'])),
    'contact_seed_low_min_pp': a3_r(100 * min(pb_seed_lo['s_ct']), 2), 'contact_seed_low_max_pp': a3_r(100 * max(pb_seed_lo['s_ct']), 2),
    'contact_seed_n_above0': int(sum(v > 0 for v in pb_seed_lo['s_ct'])), 'n_seeds_extra': 10,
    'period': {'ml_conv_pct': a3_r(100 * pb_r_Lp, 2), 'ml_contact_conv_pct': a3_r(100 * pb_r_Lpct, 2),
               **pb_ci_rec(pb_diff_p, pb_ci_p), 'pass': pb_b2_p_pass,
               **pb_ci_rec(pb_diff_pct, pb_ci_pct, 'contact_'), 'contact_pass': pb_b2_pct_pass},
    'xgb': {'ml_conv_pct': a3_r(100 * pb_conv(pb_Lx), 2), **pb_ci_rec(pb_diff_x, pb_ci_x, ci5=pb_ci5k['s_x']), 'pass': pb_b2_x_pass,
            'borderline': pb_x_borderline, 'seed_low_min_pp': a3_r(100 * min(pb_seed_lo['s_x']), 2),
            'seed_low_max_pp': a3_r(100 * max(pb_seed_lo['s_x']), 2), 'seed_n_above0': int(sum(v > 0 for v in pb_seed_lo['s_x'])),
            'captured_pct': a3_r(100 * (pb_Lx['y'] == 'yes').sum() / pb_y_teT.sum(), 1),
            'period_ml_conv_pct': a3_r(100 * pb_conv(pb_Lpx), 2), **pb_ci_rec(pb_diff_px, pb_ci_px, 'period_'), 'period_pass': pb_b2_px_pass},
    'mobile_yes': int((pb_mob['y'] == 'yes').sum()), 'ml_yes': int((pb_L['y'] == 'yes').sum()),
    'ml_cellular_share_pct': a3_r(100 * (pb_L['contact'] == 'cellular').mean(), 1),
    'month_share_of_mobile_advantage_pp': a3_r(100 * (pb_r_rand_mm - pb_r_rand), 2),
    'period_extra_over_month_pp': a3_r(100 * (pb_r_rand_pm - pb_r_rand_mm), 2),
    'within_month_mobile_advantage_pp': a3_r(100 * (pb_r_mob - pb_r_rand_mm), 2),
    'within_period_mobile_advantage_pp': a3_r(100 * (pb_r_mob - pb_r_rand_pm), 2),
    'ml_period_minus_random_period_pp': a3_r(100 * (pb_r_Lp - pb_r_rand_pm), 2),
    'by_month': [{k: (v if isinstance(v, str) else a3_r(v, 2)) for k, v in r.items()} for r in pb_month_tab.to_dict('records')],
    'months_ml_better': int((pb_month_tab['ML list conv %'] > pb_month_tab['mobile rule conv %']).sum()),
    'months_ml_worse': int((pb_month_tab['ML list conv %'] < pb_month_tab['mobile rule conv %']).sum()),
    'bootstrap_B': PB_B2_B, 'bootstrap_B_check': PB_B2_B_CHECK,
    'ci_low_sales': int(round(pb_K * pb_ci_m['pct_lo'])), 'ci_high_sales': int(round(pb_K * pb_ci_m['pct_hi'])),
}
'''

B_FIG1 = r'''
# [Fig 1] 上：同月同深度累積增益；下：與手機規則同通數時各名單的轉換率（圖中文字用英文；字級 >= 9 pt）
pb_tot_yes = int(pb_y_teT.sum())
fig = plt.figure(figsize=(6.6, 9.0), dpi=150)
ax = fig.add_axes([0.12, 0.555, 0.85, 0.395])
ax2 = fig.add_axes([0.42, 0.115, 0.55, 0.34])
ax.plot(100 * np.r_[0, pb_curve['called_share']], 100 * np.r_[0, pb_curve['captured_share']], color=PB_ACCENT, lw=2,
        marker='o', ms=3, label='ML list, same depth per month')
ax.plot(100 * np.r_[0, pb_curve_p['called_share']], 100 * np.r_[0, pb_curve_p['captured_share']], color=PB_GREY, lw=1.3,
        ls='-.', label='ML list, same depth per period')
ax.plot([0, 100], [0, 100], color=PB_LIGHT, ls='--', lw=1.3, label='Random calling (expected)')
pb_x = 100 * pb_K / len(pb_teT)
ax.axvline(pb_x, color=PB_LIGHT, lw=0.8, ls=':')
ax.text(pb_x - 1, 97, 'mobile-rule call count\n(%s calls, %.0f%%)' % (format(pb_K, ','), pb_x), fontsize=9, color=PB_GREY,
        ha='right', va='top')
pb_mob_cap = 100 * (pb_mob['y'] == 'yes').sum() / pb_tot_yes
pb_ml_cap = 100 * (pb_L['y'] == 'yes').sum() / pb_tot_yes
ax.scatter([pb_x], [pb_mob_cap], s=70, marker='D', facecolor='white', edgecolor=PB_GREY, lw=1.4, zorder=5,
           label='Mobile rule: %.1f%% of conversions' % pb_mob_cap)
ax.scatter([pb_x], [pb_ml_cap], s=22, color=PB_ACCENT, zorder=6,
           label='ML list, same calls per month: %.1f%%' % pb_ml_cap)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_xlabel('Customers called (%% of the test target group, n = %s)' % format(len(pb_teT), ','), fontsize=10)
ax.set_ylabel('Conversions captured (%% of all %s)' % format(pb_tot_yes, ','), fontsize=10)
ax.set_title('Fig 1. Pre-call list vs mobile rule (deduplicated test data)', loc='left', fontsize=11)
ax.tick_params(labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(color='#ececec', lw=0.8)
ax.legend(frameon=False, fontsize=9, loc='lower right', borderaxespad=0.2, handlelength=1.8)

pb_pts = [('Random, all customers', pb_r_rand, None, PB_LIGHT),
          ('Random, mobile-rule month mix', pb_r_rand_mm, None, PB_LIGHT),
          ('Random, mobile-rule period mix', pb_r_rand_pm, None, PB_LIGHT),
          ('Mobile rule', pb_r_mob, None, PB_GREY),
          ('RF list, same calls per period', pb_r_Lp, pb_ci_p, PB_ACCENT),
          ('RF list, same calls per month (main)', pb_r_L, pb_ci_m, PB_ACCENT),
          ('XGB list, same calls per month', pb_conv(pb_Lx), pb_ci_x, PB_ACCENT)]
for i, (lab, r, ci, colr) in enumerate(pb_pts):
    if ci is not None:   # 誤差線 = 手機規則轉換率 + (ML − 手機) 的 95% percentile 區間（B = 1,000，計畫判準用的區間）
        ax2.plot([100 * (pb_r_mob + ci['pct_lo']), 100 * (pb_r_mob + ci['pct_hi'])], [i, i], color=PB_ACCENT, lw=1.2, alpha=0.5)
    ax2.scatter([100 * r], [i], s=40, color=colr, zorder=3, edgecolor='white')
    ax2.text(100 * r + 0.12, i + 0.2, '%.2f%%' % (100 * r), fontsize=9, color='black')
ax2.axvline(100 * pb_r_mob, color=PB_GREY, lw=0.8, ls='--')
ax2.set_yticks(range(len(pb_pts)))
ax2.set_yticklabels([p[0] for p in pb_pts], fontsize=9)
ax2.set_ylim(-0.6, len(pb_pts) - 0.3)
ax2.set_xlabel('Conversion rate at %s calls (%%)\nbars: mobile-rule rate + 95%% CI of (list - mobile), B = 1,000;\n'
               'a list passes only if its whole bar is right of the dashed line' % format(pb_K, ','), fontsize=9)
ax2.tick_params(axis='x', labelsize=9)
ax2.spines[['top', 'right']].set_visible(False)
ax2.grid(axis='x', color='#ececec', lw=0.8)
ax2.set_axisbelow(True)
plt.show()
'''

B_B1 = r'''
# [Part B-4] 業務①：每筆成交的通話成本（A2 目標 ≤ A$20.87，即名單轉換率 ≥ 18%；A2 把它列為 A/B 列報項，不是硬門檻）
pb_cost_tab = pd.DataFrame([
    ('Random calling (test target group, all)', pb_r_rand, pb_actual_cost_per_conv(pb_teT)),
    ('Random, mobile-rule month mix (expected)', pb_r_rand_mm, np.nan),
    ('Mobile rule', pb_r_mob, pb_actual_cost_per_conv(pb_mob)),
    ('ML list, same calls per month (pre-call 11)', pb_r_L, pb_actual_cost_per_conv(pb_L)),
    ('ML list, same calls per month (+contact)', pb_r_Lct, pb_actual_cost_per_conv(pb_Lct)),
    ('ML list, same calls per period (robustness)', pb_r_Lp, pb_actual_cost_per_conv(pb_Lp)),
], columns=['list', 'conv', 'cost per conversion, actual seconds (A$)'])
pb_cost_tab.insert(2, 'cost per conversion, A2 formula c(r)/r (A$)', pb_cost_tab['conv'].map(pb_cost_per_conv))
PB_TARGET_COST = pb_cost_per_conv(0.18)     # A2 目標 A$20.87 的未取整值；差值都用未取整的數字相減後才取整
pb_cost_tab['vs A2 target 20.87'] = pb_cost_tab['cost per conversion, A2 formula c(r)/r (A$)'] - PB_TARGET_COST
pb_cost_tab['conv'] = 100 * pb_cost_tab['conv']
display(pb_cost_tab.rename(columns={'conv': 'conversion %'}).round(2).astype(object).where(pb_cost_tab.rename(columns={'conv': 'conversion %'}).notna(), '-'))

# 描述性：成本 vs 名單深度（不拿來挑截斷點）；同月配對與同時期配對並列
display(pd.DataFrame({'depth %': 100 * pb_curve['depth'], 'month: conv %': 100 * pb_curve['conv'], 'month: c(r)/r': pb_curve['cost_formula'],
                      'month: actual': pb_curve['cost_actual'], 'period: conv %': 100 * pb_curve_p['conv'],
                      'period: c(r)/r': pb_curve_p['cost_formula']}).round(2).T)


def pb_deepest_ok(curve, col='cost_formula'):
    ok = curve[curve[col] <= pb_a2['cost_per_conv_target_18pct']]
    return float(ok['called_share'].max()) if len(ok) else None


pb_dstar, pb_dstar_act, pb_dstar_p = pb_deepest_ok(pb_curve), pb_deepest_ok(pb_curve, 'cost_actual'), pb_deepest_ok(pb_curve_p)
# 單次測試樣本的雜訊：同月配對 50% 深度那一點，轉換率 ± 1.96 個標準誤換算成的成本範圍
pb_r50, pb_n50 = float(pb_curve.loc[pb_curve['depth'] == 0.5, 'conv'].iloc[0]), int(pb_curve.loc[pb_curve['depth'] == 0.5, 'called'].iloc[0])
pb_se50 = np.sqrt(pb_r50 * (1 - pb_r50) / pb_n50)
pb_cost50_rng = (pb_cost_per_conv(pb_r50 + 1.96 * pb_se50), pb_cost_per_conv(pb_r50 - 1.96 * pb_se50))
print('deepest depth with c(r)/r <= A$%.2f: same depth per month %s, per period %s (actual seconds, per month: %s)'
      % (pb_a2['cost_per_conv_target_18pct'], *['%.0f%%' % (100 * v) if v else 'none' for v in (pb_dstar, pb_dstar_p, pb_dstar_act)]))
print('month-matched 50%% depth: conversion %.2f%% (n = %d), cost A$%.2f, 95%% range from sampling noise A$%.2f to A$%.2f'
      % (100 * pb_r50, pb_n50, pb_cost_per_conv(pb_r50), *pb_cost50_rng))


# 外推到 A2 的「一輪」（同樣 2,300 筆成交）：外撥 N = 2,300 / r，整輪成本 = 2,300 x c(r) / r；只能外推，不是測得的
def pb_round_cost(r):
    calls = 2300 / r
    return {'calls': round(calls), 'call_cost': round(2300 * pb_cost_per_conv(r)), 'call_cost_exact': round(2300 * pb_cost_per_conv(r), 2),
            'fewer_calls_vs_pilot_pct': round(100 * (1 - calls / pb_a2['pilot_target_n']), 1)}


pb_ext = {'ml_list': pb_round_cost(pb_r_L), 'ml_list_period': pb_round_cost(pb_r_Lp), 'mobile': pb_round_cost(pb_r_mob),
          'a2_target_18pct': pb_round_cost(0.18)}
print('one A2 round (2,300 conversions):', pb_ext)
A3_KPI['part_b']['b1'] = {
    'rows': [{'list': r['list'], 'conv_pct': a3_r(r['conv'], 2),
              'cost_formula': a3_r(r['cost per conversion, A2 formula c(r)/r (A$)'], 2),
              'cost_actual': None if pd.isna(r['cost per conversion, actual seconds (A$)']) else a3_r(r['cost per conversion, actual seconds (A$)'], 2)}
             for _, r in pb_cost_tab.iterrows()],
    'ml_cost_formula': a3_r(pb_cost_per_conv(pb_r_L), 2), 'ml_cost_actual': a3_r(pb_actual_cost_per_conv(pb_L), 2),
    'ml_period_cost_formula': a3_r(pb_cost_per_conv(pb_r_Lp), 2),
    'ml_minus_target': a3_r(pb_cost_per_conv(pb_r_L) - PB_TARGET_COST, 2),
    'mobile_minus_target': a3_r(pb_cost_per_conv(pb_r_mob) - PB_TARGET_COST, 2),
    'random_minus_ml': a3_r(pb_cost_per_conv(pb_r_rand) - pb_cost_per_conv(pb_r_L), 2),
    'mobile_minus_ml': a3_r(pb_cost_per_conv(pb_r_mob) - pb_cost_per_conv(pb_r_L), 2),
    'mobile_cost_formula': a3_r(pb_cost_per_conv(pb_r_mob), 2), 'mobile_cost_actual': a3_r(pb_actual_cost_per_conv(pb_mob), 2),
    'random_cost_formula': a3_r(pb_cost_per_conv(pb_r_rand), 2), 'random_mm_cost_formula': a3_r(pb_cost_per_conv(pb_r_rand_mm), 2),
    'target': pb_a2['cost_per_conv_target_18pct'], 'pass': bool(pb_cost_per_conv(pb_r_L) <= pb_a2['cost_per_conv_target_18pct']),
    'deepest_ok_depth_pct': None if pb_dstar is None else a3_r(100 * pb_dstar, 1),
    'deepest_ok_depth_actual_pct': None if pb_dstar_act is None else a3_r(100 * pb_dstar_act, 1),
    'deepest_ok_depth_period_pct': None if pb_dstar_p is None else a3_r(100 * pb_dstar_p, 1),
    'depth50_conv_pct': a3_r(100 * pb_r50, 2), 'depth50_n': pb_n50, 'depth50_cost': a3_r(pb_cost_per_conv(pb_r50), 2),
    'depth50_cost_low': a3_r(pb_cost50_rng[0], 2), 'depth50_cost_high': a3_r(pb_cost50_rng[1], 2),
    'curve': [{'depth_pct': a3_r(100 * r['called_share'], 1), 'conv_pct': a3_r(100 * r['conv'], 2),
               'captured_pct': a3_r(100 * r['captured_share'], 1),
               'cost_formula': a3_r(r['cost_formula'], 2), 'cost_actual': a3_r(r['cost_actual'], 2)} for _, r in pb_curve.iterrows()],
    'curve_period': [{'depth_pct': a3_r(100 * r['called_share'], 1), 'conv_pct': a3_r(100 * r['conv'], 2),
                      'captured_pct': a3_r(100 * r['captured_share'], 1), 'cost_formula': a3_r(r['cost_formula'], 2)}
                     for _, r in pb_curve_p.iterrows()],
    'one_round_extrapolation': pb_ext,
}
'''

B_FIG2 = r'''
# [Fig 2] 每筆成交的通話成本 vs 名單深度（描述性；不拿來挑截斷點）
fig, ax = plt.subplots(figsize=(6.6, 5.0), dpi=150)
ax.plot(100 * pb_curve['called_share'], pb_curve['cost_formula'], color=PB_ACCENT, lw=2, marker='o', ms=3,
        label='ML list per month, A2 formula c(r)/r')
ax.plot(100 * pb_curve['called_share'], pb_curve['cost_actual'], color=PB_ACCENT, lw=1, ls='--', label='ML list per month, actual seconds')
ax.plot(100 * pb_curve_p['called_share'], pb_curve_p['cost_formula'], color=PB_GREY, lw=1.6, ls='-.', marker='s', ms=2.5,
        label='ML list per period, c(r)/r')
for yv, lab, ls in [(pb_a2['cost_per_conv_pilot'], 'A2 baseline (random)', ':'),
                    (pb_cost_per_conv(pb_r_mob), 'mobile rule', (0, (6, 2, 1, 2))),
                    (pb_a2['cost_per_conv_target_18pct'], 'A2 target (18%)', '-')]:
    ax.axhline(yv, color=PB_GREY if ls != '-' else 'black', ls=ls, lw=0.9, label=r'A\$%.2f  %s' % (yv, lab))
ax.scatter([100 * pb_K / len(pb_teT)], [pb_cost_per_conv(pb_r_L)], s=55, color=PB_ACCENT, edgecolor='white', zorder=6,
           label=r'ML list at mobile-rule calls: A\$%.2f' % pb_cost_per_conv(pb_r_L))
ax.set_xlim(0, 100)
ax.set_ylim(0, max(30, float(pb_curve_p['cost_formula'].max()) + 2))
ax.set_xlabel('Customers called (% of the test target group)', fontsize=10)
ax.set_ylabel(r'Call cost per conversion (A\$)', fontsize=10)
ax.set_title('Fig 2. Call cost per conversion vs list depth (descriptive)', loc='left', fontsize=11)
ax.tick_params(labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(color='#ececec', lw=0.8)
ax.legend(frameon=False, fontsize=9, loc='lower right', borderaxespad=0.2, handlelength=1.8, labelspacing=0.35)
plt.show()
'''

B_CM = r'''
# [Part B-5] 混淆矩陣（測試集目標組，K = 手機通數 4,752）
# 主表：B-3 的同月同通數名單（外撥日不能換月份，這是實際做得到的名單）
# 參考：全體單一門檻 t（分數第 K 名）。它含月份組成（B-3 的反例），只因為對照組沒有月份，B-6 的增量比較必須用它
pb_t = float(np.sort(pb_teT['s'].to_numpy())[::-1][pb_K - 1])
pb_yes = pb_y_teT.astype(bool)


def pb_confusion(called):
    tp, fp = int((called & pb_yes).sum()), int((called & ~pb_yes).sum())
    fn, tn = int((~called & pb_yes).sum()), int((~called & ~pb_yes).sum())
    return {'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn, 'list_size': int(called.sum()),
            'precision_pct': a3_r(100 * tp / (tp + fp), 2), 'recall_pct': a3_r(100 * tp / (tp + fn), 2),
            'fp_cost_aud': round(fp * PB_CALL_NO), 'tn_saving_aud': round(tn * PB_CALL_NO)}


pb_cm_m = pb_confusion(pb_teT.index.isin(pb_L.index))
pb_cm_p = pb_confusion((pb_teT['s'] >= pb_t).to_numpy())
pb_mob_rec = (pb_mob['y'] == 'yes').sum() / pb_y_teT.sum()
display(pd.DataFrame([
    ('TP: on the list, bought', pb_cm_m['TP'], pb_cm_p['TP'], '成交電話每通約 A$%.2f＋一份折扣；其中多少人「不打也會買」看 B-6、B-8' % PB_CALL_YES),
    ('FP: on the list, did not buy', pb_cm_m['FP'], pb_cm_p['FP'], '白打一通，每通約 A$%.2f（主表合計約 A$%s）' % (PB_CALL_NO, format(pb_cm_m['fp_cost_aud'], ','))),
    ('FN: not on the list, bought', pb_cm_m['FN'], pb_cm_p['FN'], '試點裡他們有被打；不打時可能仍會買，損失只有「打了才會買」的那部分（B-8）'),
    ('TN: not on the list, did not buy', pb_cm_m['TN'], pb_cm_p['TN'], '省下的電話，每通約 A$%.2f（主表合計約 A$%s）' % (PB_CALL_NO, format(pb_cm_m['tn_saving_aud'], ','))),
    ('precision % (= list conversion)', pb_cm_m['precision_pct'], pb_cm_p['precision_pct'], ''),
    ('recall %% (mobile rule: %.1f%%)' % (100 * pb_mob_rec),pb_cm_m['recall_pct'], pb_cm_p['recall_pct'], ''),
], columns=['cell', 'same calls per month (main)', 'pooled cut-off t (reference)', '商業意義（A2 假設：時薪 A$50、只計通話時間）']))
print('pooled cut-off score t = %.4f; both lists have %d customers' % (pb_t, pb_K))
A3_KPI['part_b']['confusion'] = {'K': pb_K, 'threshold': a3_r(pb_t), 'month_matched': pb_cm_m, 'pooled': pb_cm_p,
                                 'mobile_recall_pct': a3_r(100 * pb_mob_rec, 2),
                                 'pooled_minus_month_precision_pp': a3_r(pb_cm_p['precision_pct'] - pb_cm_m['precision_pct'], 2),
                                 'call_cost_no_exact': a3_r(PB_CALL_NO, 4)}
'''

B_B3 = r'''
# [Part B-6] 業務③（上線硬門檻）、④（列報）：同門檻對照組比較
# 用同一個撥號前模型替「沒被打」的對照組評分（模型不用 duration / contact / month，對照組也能評分）。
# 入選門檻 t = 測試集目標組第 K 名的分數，K = 測試集目標組的手機通數；對照組沒有月份，所以只能用全體單一門檻。
# 門檻同時作用在兩組，增量不受月份挑選影響；但名單轉換率 r 含月份組成而偏高（B-5），⑤ 的絕對值因此只作示算。
# bootstrap：名單與同門檻對照組各自有放回重抽（B = 1,000），門檻固定為 t；同一批重抽也給出④（對照 ÷ 名單）的區間。
# 時期分層（穩健性）：門檻仍用全體 t；在每個 (cpi, cci) 時期內比較名單與對照組（兩邊都至少 20 人的時期才納入），
# 再依名單人數加權；另報不設 20 人下限的版本。分層增量的區間：各時期內兩組各自重抽（B = 1,000），再同樣加權。
def pb_uplift(teT, teC, K, B=1000):
    t = float(np.sort(teT['s'].to_numpy())[::-1][K - 1])
    L, Cc = teT[teT['s'] >= t], teC[teC['s'] >= t]
    yL, yC = (L['y'] == 'yes').to_numpy(), (Cc['y'] == 'yes').to_numpy()
    rng = np.random.default_rng(PB_SEED)
    bL, bC = np.zeros(B), np.zeros(B)
    for b in range(B):
        bL[b] = yL[rng.integers(0, len(yL), len(yL))].mean()
        bC[b] = yC[rng.integers(0, len(yC), len(yC))].mean()
    lo, hi = np.percentile(bL - bC, [2.5, 97.5])
    wlo, whi = np.percentile(bC / bL, [2.5, 97.5])

    def strat(min_n):
        num = den = 0
        cells = []
        for p, gT in L.groupby('period'):
            gC = Cc[Cc['period'] == p]
            if len(gT) >= min_n and len(gC) >= min_n:
                num += len(gT) * (pb_conv(gT) - pb_conv(gC))
                den += len(gT)
                cells.append((len(gT), pb_conv(gT), len(gC), pb_conv(gC)))
        return (num / den if den else None), den, cells
    ps, pden, pcells = strat(20)
    ps0, pden0, _ = strat(1)
    rng2 = np.random.default_rng(PB_SEED)
    sb = np.zeros(B)
    for nT_, rT_, nC_, rC_ in pcells:     # 一個比例的有放回重抽 = 二項分配
        sb += nT_ * (rng2.binomial(nT_, rT_, B) / nT_ - rng2.binomial(nC_, rC_, B) / nC_)
    slo, shi = np.percentile(sb / pden, [2.5, 97.5]) if pden else (np.nan, np.nan)
    rL, rC = yL.mean(), yC.mean()
    rT_all, rC_all = pb_conv(teT), pb_conv(teC)
    rep = {'threshold': a3_r(t), 'K': int(K), 'list_n': len(L), 'control_above_n': len(Cc),
           'target_above_share_pct': a3_r(100 * len(L) / len(teT), 1), 'control_above_share_pct': a3_r(100 * len(Cc) / len(teC), 1),
           'list_conv_pct': a3_r(100 * rL, 2), 'control_above_conv_pct': a3_r(100 * rC, 2),
           'uplift_pp': a3_r(100 * (rL - rC), 2), 'uplift_ci_low_pp': a3_r(100 * lo, 2), 'uplift_ci_high_pp': a3_r(100 * hi, 2),
           'uplift_per_1000_calls': a3_r(1000 * (rL - rC), 1),
           'would_buy_share_pct': a3_r(100 * rC / rL, 1),
           'would_buy_ci_low_pct': a3_r(100 * wlo, 1), 'would_buy_ci_high_pct': a3_r(100 * whi, 1),
           'period_stratified_uplift_pp': None if ps is None else a3_r(100 * ps, 2),
           'period_stratified_ci_low_pp': a3_r(100 * slo, 2), 'period_stratified_ci_high_pp': a3_r(100 * shi, 2),
           'period_coverage_pct': a3_r(100 * pden / len(L), 1),
           'period_stratified_uplift_nomin_pp': None if ps0 is None else a3_r(100 * ps0, 2),
           'period_coverage_nomin_pct': a3_r(100 * pden0 / len(L), 1),
           'overall_target_conv_pct': a3_r(100 * rT_all, 2), 'overall_control_conv_pct': a3_r(100 * rC_all, 2),
           'overall_uplift_pp': a3_r(100 * (rT_all - rC_all), 2),
           'overall_would_buy_share_pct': a3_r(100 * rC_all / rT_all, 1),
           'test_target_n': len(teT), 'test_control_n': len(teC)}
    ex = {'t': t, 'r': rL, 'rC': rC, 'u': rL - rC, 'u_period': ps, 'rT_all': rT_all, 'rC_all': rC_all, 'n_list': len(L),
          'teT': teT, 'teC': teC}
    return rep, ex


pb_up, pb_upx = pb_uplift(pb_teT, pb_teC, pb_K)

# 敏感度：原始資料（不去重）用同樣的清理、同樣 0.4 / 123 切分、同樣固定的超參數，只用原始訓練集目標組重訓
pb_rtr, pb_rte = train_test_split(pb_raw, test_size=0.4, random_state=RANDOM_SATE)
pb_rtrT = pb_rtr[pb_rtr['campaign'] == '1']
pb_raw_model = pb_pipeline(pb_rf(n_jobs=-1, max_depth=pb_main_params['max_depth'],
                                 min_samples_leaf=pb_main_params['min_samples_leaf']), PB_CAT)
pb_raw_model.fit(pb_rtrT[PB_FEATURES], (pb_rtrT['y'] == 'yes').astype(int))
pb_raw_model.set_params(clf__n_jobs=1)
pb_rteT = pb_rte[pb_rte['campaign'] == '1'].copy()
pb_rteC = pb_rte[pb_rte['campaign'] == '0'].copy()
for d_ in (pb_rteT, pb_rteC):
    d_['s'] = pb_raw_model.predict_proba(d_[PB_FEATURES])[:, 1]
    d_['period'] = d_['cons.price.idx'].map('{:.3f}'.format) + ' | ' + d_['cons.conf.idx'].map('{:.1f}'.format)
pb_K_raw = int((pb_rteT['contact'] == 'cellular').sum())
pb_up_raw, pb_upx_raw = pb_uplift(pb_rteT, pb_rteC, pb_K_raw)
pb_up_raw['raw_test_target_auc'] = a3_r(pb_auc((pb_rteT['y'] == 'yes').to_numpy(), pb_rteT['s']))
pb_up_raw['raw_train_target_rows'] = len(pb_rtrT)

pb_up_show = pd.DataFrame({'deduplicated (main)': pd.Series(pb_up, dtype=object),
                           'raw data (sensitivity)': pd.Series(pb_up_raw, dtype=object)})
display(pb_up_show.where(pb_up_show.notna(), '-'))   # '-' = 只有原始資料版才有的欄位
A3_KPI['part_b']['b3b4'] = {'dedup': pb_up, 'raw': pb_up_raw,
                             'raw_minus_raw_strat_pp': a3_r(100 * (pb_upx_raw['u'] - pb_upx_raw['u_period']), 2),
                             'strat_raw_minus_dedup_pp': a3_r(100 * (pb_upx_raw['u_period'] - pb_upx['u_period']), 2)}
'''

B_FIG3 = r'''
# [Fig 3] 名單 vs 同門檻對照組的轉換率（去重 vs 原始資料）；A2 試點全體當參考（字級 >= 9 pt）
fig, ax = plt.subplots(figsize=(6.6, 5.2), dpi=150)
pb_groups = ['A2 pilot, all customers\n(raw, no score cut-off)', 'A3 deduplicated\n(score >= cut-off)', 'A3 raw data\n(score >= cut-off)']
pb_called_v = [pb_a2['pilot_target_conv_pct'], pb_up['list_conv_pct'], pb_up_raw['list_conv_pct']]
pb_ctrl_v = [pb_a2['pilot_control_conv_pct'], pb_up['control_above_conv_pct'], pb_up_raw['control_above_conv_pct']]
pb_notes = ['uplift %+.2f pp' % pb_a2['pilot_uplift_pp']] + [
    'uplift %+.2f pp\n[%+.2f, %+.2f]\nwithin periods %+.2f\n[%+.2f, %+.2f]' % (u_['uplift_pp'], u_['uplift_ci_low_pp'], u_['uplift_ci_high_pp'],
                                                                         u_['period_stratified_uplift_pp'], u_['period_stratified_ci_low_pp'],
                                                                         u_['period_stratified_ci_high_pp']) for u_ in (pb_up, pb_up_raw)]
xg = np.arange(3)
w = 0.36
b1 = ax.bar(xg - w / 2, pb_called_v, w, color=PB_ACCENT, label='Called: target group')
b2 = ax.bar(xg + w / 2, pb_ctrl_v, w, color=PB_LIGHT, label='Not called: control group (same cut-off)')
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.3, '%.1f%%' % b.get_height(), ha='center', fontsize=9)
ymax = max(pb_called_v + pb_ctrl_v)
for i, note in enumerate(pb_notes):
    ax.text(i, ymax + 2.0, note, ha='center', fontsize=9, color='#333333', va='bottom', linespacing=1.15)
ax.set_xticks(xg)
ax.set_xticklabels(pb_groups, fontsize=9)
ax.set_ylim(0, ymax + 10.5)
ax.set_ylabel('Conversion rate (%)', fontsize=10)
ax.set_title('Fig 3. Call + offer vs no call, same score cut-off', loc='left', fontsize=11)
ax.tick_params(axis='y', labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', color='#ececec', lw=0.8)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9, loc='upper left', bbox_to_anchor=(0, -0.15), ncol=2)
ax.text(0, -0.25, 'Brackets: 95% bootstrap CI (B = 1,000).\nWithin periods: list vs control compared inside each (cpi, cci) period.',
        transform=ax.transAxes, fontsize=9, color=PB_GREY, va='top')
plt.show()
'''

B_B5 = r'''
# [Part B-7] 業務⑤（上線硬門檻）只能示算：式 1 每通淨值（相對於不外撥）= D x (2u - r) - c(r)
# u = 增量（名單轉換率 − 同門檻對照轉換率），r = 名單轉換率，收益 = 2D（A2 的 2:1 假設），c(r) = 每通通話成本
# 全部用未取整的 u、r 計算，只在顯示時取整
PB_D = 36.0     # A2 附錄 A 的「兩平折扣額」約 A$36，只是示例，不是真實折扣


def pb_net(u, r):
    k = 2 * u - r
    return {'u_pp': a3_r(100 * u, 2), 'r_pct': a3_r(100 * r, 2), 'net_D_per_call_excl_call_cost': a3_r(k, 4),
            'net_D_per_1000_calls': a3_r(1000 * k, 1), 'call_cost_per_call': a3_r(pb_call_cost(r), 2),
            'net_aud_per_call_at_D36': a3_r(PB_D * k - pb_call_cost(r), 2),
            'net_aud_per_1000_calls_at_D36': a3_r(1000 * (PB_D * k - pb_call_cost(r)), 0),
            'break_even_D': a3_r(pb_call_cost(r) / k, 2) if k > 0 else None,
            'revenue_multiple_needed': a3_r(r / u, 1) if u > 0 else None}


pb_b5 = {
    'dedup_ml_list': pb_net(pb_upx['u'], pb_upx['r']),
    'dedup_random': pb_net(pb_upx['rT_all'] - pb_upx['rC_all'], pb_upx['rT_all']),
    'raw_ml_list': pb_net(pb_upx_raw['u'], pb_upx_raw['r']),
    'raw_random': pb_net(pb_upx_raw['rT_all'] - pb_upx_raw['rC_all'], pb_upx_raw['rT_all']),
    'a2_pilot_all': pb_net(pb_r_pilot - pb_r_ctrl_raw, pb_r_pilot),
}
pb_b5_show = pd.DataFrame(pb_b5).T
pb_b5_show['break_even_D'] = pb_b5_show['break_even_D'].map(lambda v: 'none (2u - r < 0)' if pd.isna(v) else v)
pb_b5_show['revenue_multiple_needed'] = pb_b5_show['revenue_multiple_needed'].map(lambda v: 'none (u <= 0)' if pd.isna(v) else v)
display(pb_b5_show.rename(columns={
    'u_pp': 'uplift u (pp)', 'r_pct': 'conversion r (%)', 'net_D_per_call_excl_call_cost': '2u - r (D per call)',
    'net_D_per_1000_calls': '2u - r per 1,000 calls (D)', 'call_cost_per_call': 'call cost c(r) (A$)',
    'net_aud_per_call_at_D36': 'net per call at D = A$36 (A$)', 'net_aud_per_1000_calls_at_D36': 'net per 1,000 calls at D = A$36 (A$)',
    'break_even_D': 'break-even D (2:1)', 'revenue_multiple_needed': 'revenue / discount needed, r / u (no 2:1)'}))
print('2u - r >= 0  <=>  (would-buy share) <= 50%: the A2 formula-2 break-even, before call cost')
print('mobile rule: its net value needs its own uplift, i.e. un-called mobile customers; the control group has no contact '
      'field, so it cannot be computed offline (A2 places the check in the A/B stage)')
A3_KPI['part_b']['b5'] = pb_b5
'''

B_ERR = r'''
# [Part B-8] 三種錯誤的代價（A2 表 4 註）與「漏掉的是誰」（A2 表 8 註）；門檻與 B-6 相同（全體單一門檻 t）
# 錯誤 A 打給本來就會買的人：白送一份折扣 D，再加一通成交電話；人數 ≈ 名單人數 × 同門檻對照組轉換率
# 錯誤 B 漏掉打了才會買的人：少一份淨收益（收益 − 折扣 = D），扣掉省下的一通成交電話；人數 ≈ 未入選目標組人數 × 未入選者的增量
#    （增量的點估計 ≤ 0 時「估計不出」，不截成 0；另用 95% 區間上限換算人數上限）
# 錯誤 C 打給不會買的人：每通約 A$3.07；人數 = 名單中未成交者（FP）
# （KPI JSON 的 'largest' 仍記 '1' / '2' / '3' ＝ 錯誤 A / B / C）
# D 是示例折扣額（A2 未定，由財務提供）：A$36 是 A2 附錄 A 的兩平示例，另列 A$10、A$100 看排序是否改變
PB_D_LIST = (10.0, 36.0, 100.0)


def pb_errors(ex, B=1000):
    teT_, teC_, t = ex['teT'], ex['teC'], ex['t']
    T_lo, C_lo = teT_[teT_['s'] < t], teC_[teC_['s'] < t]
    yT, yC = (T_lo['y'] == 'yes').to_numpy(), (C_lo['y'] == 'yes').to_numpy()
    rT_lo, rC_lo = yT.mean(), yC.mean()
    rng = np.random.default_rng(PB_SEED)
    bd = np.zeros(B)
    for b in range(B):
        bd[b] = yT[rng.integers(0, len(yT), len(yT))].mean() - yC[rng.integers(0, len(yC), len(yC))].mean()
    dlo, dhi = np.percentile(bd, [2.5, 97.5])
    u_lo = rT_lo - rC_lo
    n1 = ex['n_list'] * min(ex['rC'], ex['r'])
    n2 = len(T_lo) * u_lo if u_lo > 0 else None
    n2_hi = len(T_lo) * max(dhi, 0.0)
    n3 = ex['n_list'] * (1 - ex['r'])
    by_D = {}
    for D in PB_D_LIST:
        unit = (D + PB_CALL_YES, D - PB_CALL_YES, PB_CALL_NO)
        tot = [n1 * unit[0], None if n2 is None else n2 * unit[1], n3 * unit[2]]
        tot2_hi = n2_hi * unit[1]
        largest = int(np.argmax([v if v is not None else -1 for v in tot]))
        by_D['%d' % D] = {'unit': [a3_r(v, 2) for v in unit], 'total': [None if v is None else int(round(v)) for v in tot],
                          'total_2_upper': int(round(tot2_hi)), 'largest': ['1', '2', '3'][largest]}
    return {'below_target_n': len(T_lo), 'below_control_n': len(C_lo),
            'below_target_conv_pct': a3_r(100 * rT_lo, 2), 'below_control_conv_pct': a3_r(100 * rC_lo, 2),
            'below_uplift_pp': a3_r(100 * u_lo, 2), 'below_uplift_ci_low_pp': a3_r(100 * dlo, 2), 'below_uplift_ci_high_pp': a3_r(100 * dhi, 2),
            'n_wouldbuy_on_list': int(round(n1)), 'n_missed_incremental': None if n2 is None else int(round(n2)),
            'n_missed_upper': int(round(n2_hi)), 'n_fp': int(round(n3)),
            'unit_cost_at_D36': by_D['36']['unit'], 'total_at_D36': by_D['36']['total'], 'by_D': by_D}


pb_err = {'dedup': pb_errors(pb_upx), 'raw': pb_errors(pb_upx_raw)}
display(pd.DataFrame([
    ('not selected (score < t): target group conversion %', pb_err['dedup']['below_target_conv_pct'], pb_err['raw']['below_target_conv_pct']),
    ('not selected (score < t): control group conversion %', pb_err['dedup']['below_control_conv_pct'], pb_err['raw']['below_control_conv_pct']),
    ('difference (pp) = uplift among the not selected', pb_err['dedup']['below_uplift_pp'], pb_err['raw']['below_uplift_pp']),
    ('95% bootstrap CI of the difference (pp)', '[%+.2f, %+.2f]' % (pb_err['dedup']['below_uplift_ci_low_pp'], pb_err['dedup']['below_uplift_ci_high_pp']),
     '[%+.2f, %+.2f]' % (pb_err['raw']['below_uplift_ci_low_pp'], pb_err['raw']['below_uplift_ci_high_pp'])),
], columns=['A2 table 8 note: who is missed', 'deduplicated', 'raw data']))


def pb_n2_txt(e):
    if e['n_missed_incremental'] is None:
        return 'not estimable (uplift < 0); upper bound %d' % e['n_missed_upper']
    return '%d (upper bound %d)' % (e['n_missed_incremental'], e['n_missed_upper'])


def pb_tot_txt(v):
    return 'not estimable' if v is None else v


pb_err_tab = pd.DataFrame([
    ('A: calls a would-buy customer (discount given away + call)', 'D + A$%.2f' % PB_CALL_YES, pb_err['dedup']['unit_cost_at_D36'][0],
     pb_err['dedup']['n_wouldbuy_on_list'], pb_err['dedup']['total_at_D36'][0], pb_err['raw']['n_wouldbuy_on_list'], pb_err['raw']['total_at_D36'][0]),
    ('B: misses a customer who buys only if called (net revenue lost - call saved)', 'D - A$%.2f' % PB_CALL_YES, pb_err['dedup']['unit_cost_at_D36'][1],
     pb_n2_txt(pb_err['dedup']), pb_tot_txt(pb_err['dedup']['total_at_D36'][1]), pb_n2_txt(pb_err['raw']), pb_tot_txt(pb_err['raw']['total_at_D36'][1])),
    ('C: calls a customer who does not buy', 'A$%.2f' % PB_CALL_NO, pb_err['dedup']['unit_cost_at_D36'][2],
     pb_err['dedup']['n_fp'], pb_err['dedup']['total_at_D36'][2], pb_err['raw']['n_fp'], pb_err['raw']['total_at_D36'][2]),
], columns=['error (A2 table 4 note)', 'cost per person', 'per person at D = A$36 (illustrative)', 'people (dedup)', 'total A$ (dedup)',
            'people (raw)', 'total A$ (raw)'])
display(pb_err_tab)
pb_dtab = []
for v_ in ('dedup', 'raw'):
    for D_, r_ in pb_err[v_]['by_D'].items():
        pb_dtab.append((v_, 'A$' + D_, r_['total'][0], pb_tot_txt(r_['total'][1]), r_['total_2_upper'], r_['total'][2],
                        'error ' + {'1': 'A', '2': 'B', '3': 'C'}[r_['largest']]))
print('Illustrative discount amounts D (A2 has not fixed D; finance to supply): total cost of each error, test target group')
display(pd.DataFrame(pb_dtab, columns=['data', 'D', 'A total A$', 'B total A$', 'B upper bound A$', 'C total A$', 'largest total']))
print('per person: A - B = 2 x A$%.2f > 0 for any D; B > C only when D > A$%.2f' % (PB_CALL_YES, PB_CALL_YES + PB_CALL_NO))
print('scale: one test target group (%d customers, list of %d) under the A2 2:1 assumption' % (len(pb_teT), pb_K))
A3_KPI['part_b']['errors'] = {**pb_err, 'D_where_2_exceeds_3': a3_r(PB_CALL_YES + PB_CALL_NO, 2), 'D_list': list(PB_D_LIST)}
'''

B_ML4 = r'''
# [Part B-9] ML④ 分群一致性：測試集目標組上，各群 AUC（附 bootstrap 95% 區間）與入選比例
# 入選比例兩種：主欄 = B-3 同月同通數名單（實際可行的名單）；參考欄 = 全體單一門檻 t（B-6 用的門檻，含月份組成）
pb_teT['age_band'] = pd.cut(pb_teT['age'], [0, 29, 39, 49, 59, 200], labels=['<30', '30-39', '40-49', '50-59', '60+'])
pb_teT['on_list'] = pb_teT.index.isin(pb_L.index)
PB_ORDER = {'age_band': ['<30', '30-39', '40-49', '50-59', '60+'], 'marital': ['divorced', 'married', 'single', 'unknown'],
            'month': ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']}
PB_RULE = {'age_band': lambda g, n1: True,                      # 年齡層：全部納入判定
           'marital': lambda g, n1: g != 'unknown',              # 婚姻 unknown 只有十幾列：只列報
           'month': lambda g, n1: n1 >= 30}                      # 成交少於 30 筆的月份：只列報
pb_seg_rows = []
rng_seg = np.random.default_rng(PB_SEED)
for dim, order in PB_ORDER.items():
    for gname in order:
        g = pb_teT[pb_teT[dim].astype(str) == gname]
        y = (g['y'] == 'yes').to_numpy()
        s = g['s'].to_numpy()
        n1 = int(y.sum())
        auc = pb_auc(y, s) if 0 < n1 < len(y) else np.nan
        bs = []
        for _ in range(500):
            i = rng_seg.integers(0, len(y), len(y))
            if 0 < y[i].sum() < len(y):
                bs.append(pb_auc(y[i], s[i]))
        lo, hi = np.percentile(bs, [2.5, 97.5]) if bs else (np.nan, np.nan)
        pb_seg_rows.append({'dimension': dim, 'group': gname, 'n': len(g), 'conversions': n1, 'conv_pct': 100 * y.mean(),
                            'auc': auc, 'ci_low': lo, 'ci_high': hi, 'selected_pct': 100 * g['on_list'].mean(),
                            'selected_pct_pooled': 100 * (s >= pb_t).mean(), 'in_gate': bool(PB_RULE[dim](gname, n1))})
pb_seg = pd.DataFrame(pb_seg_rows)
display(pb_seg.rename(columns={'conv_pct': 'conv %', 'auc': 'AUC', 'ci_low': 'CI low', 'ci_high': 'CI high',
                               'selected_pct': 'selected % (month-matched list)', 'selected_pct_pooled': 'selected % (pooled cut-off t)',
                               'in_gate': 'in gate'}).round(3))
pb_gap = {}
for dim in PB_ORDER:
    e = pb_seg[(pb_seg['dimension'] == dim) & pb_seg['in_gate']]
    pb_gap[dim] = {'max_minus_min': a3_r(e['auc'].max() - e['auc'].min()), 'pass': bool(e['auc'].max() - e['auc'].min() <= 0.05),
                   'lowest': e.loc[e['auc'].idxmin(), 'group'], 'highest': e.loc[e['auc'].idxmax(), 'group'],
                   'lowest_auc': a3_r(e['auc'].min(), 3), 'highest_auc': a3_r(e['auc'].max(), 3),
                   'groups_in_gate': int(len(e)),
                   'three_lowest': e.nsmallest(3, 'auc')['group'].tolist()}
print('AUC gap (max - min over groups in the gate):', pb_gap)
A3_KPI['part_b']['ml4'] = {'gaps': pb_gap, 'overall_test_auc': a3_r(pb_auc_te),
                           'segments': [{k: (v if isinstance(v, (str, bool)) else a3_r(v, 3)) for k, v in r.items()} for r in pb_seg_rows],
                           'bootstrap_B': 500}
'''

B_FIG4 = r'''
# [Fig 4] 分群 AUC 點圖：實心 = 納入判定的群、空心 = 只列報；淺色帶 = 從該維度最低 AUC 起算 0.05 的容許寬度
pb_dim_lab = {'age_band': 'Age band', 'marital': 'Marital status', 'month': 'Month (proxy for period)'}
fig, ax = plt.subplots(figsize=(7.0, 7.8), dpi=150)
fig.subplots_adjust(left=0.31, right=0.97, top=0.95, bottom=0.15)
ypos, ylabels, y = [], [], 0
for dim in PB_ORDER:
    seg = pb_seg[pb_seg['dimension'] == dim]
    y0 = y
    for _, r in seg.iterrows():
        filled = r['in_gate']
        ax.plot([r['ci_low'], r['ci_high']], [y, y], color=PB_LIGHT, lw=1.2, zorder=2)
        ax.scatter([r['auc']], [y], s=34, zorder=3, color=PB_ACCENT if filled else 'white',
                   edgecolor=PB_ACCENT if filled else PB_GREY)
        ylabels.append('%s  (n=%s, %d conv.)' % (r['group'], format(int(r['n']), ','), r['conversions']))
        ypos.append(y)
        y += 1
    e = seg[seg['in_gate']]
    lo_auc = e['auc'].min()
    ax.fill_betweenx([y0 - 0.45, y - 0.55], lo_auc, lo_auc + 0.05, color=PB_ACCENT, alpha=0.10, lw=0)
    gap = pb_gap[dim]['max_minus_min']
    ax.text(0.01, y0 - 0.75, '%s: max - min = %.3f %s 0.05' % (pb_dim_lab[dim], gap, '<=' if gap <= 0.05 else '>'),
            transform=ax.get_yaxis_transform(), ha='left', fontsize=9, color='black')
    y += 1.2
ax.axvline(pb_auc_te, color=PB_GREY, ls='--', lw=0.9)
ax.set_yticks(ypos)
ax.set_yticklabels(ylabels, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('ROC-AUC within the group (bars: 95%% bootstrap CI; dashed: overall %.3f)' % pb_auc_te, fontsize=9.5)
ax.set_xlim(0.1, 1.0)
ax.set_title('Fig 4. Segment AUC (gate: max - min <= 0.05)', loc='left', fontsize=11)
ax.tick_params(axis='x', labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', color='#ececec', lw=0.8)
ax.set_axisbelow(True)
fig.text(0.01, 0.072, 'Test target group. Filled = in the gate; hollow = reported only (marital unknown,\n'
         'months with < 30 conversions). Shaded = 0.05 tolerance from the lowest gated group:\n'
         'a dimension passes only if all filled dots fall inside.',
         fontsize=9, color=PB_GREY, va='top')
plt.show()
'''

B_PERM = r'''
# [Part B-10] 撥號前模型的 permutation importance（測試集目標組；把某欄打亂後 ROC-AUC 下降多少；n_repeats = 10）
pb_pi = permutation_importance(pb_main, pb_teT[PB_FEATURES], pb_y_teT, scoring='roc_auc', n_repeats=10,
                               random_state=PB_SEED, n_jobs=-1)
pb_pi_tab = pd.DataFrame({'feature': PB_FEATURES, 'mean AUC drop': pb_pi.importances_mean,
                          'sd': pb_pi.importances_std}).sort_values('mean AUC drop', ascending=False).reset_index(drop=True)
display(pb_pi_tab.round(4))
# 拿掉年齡、婚姻（法遵可能不准用，A2 表 9 階段 0）後重訓：同樣固定的超參數、同樣只用訓練集目標組；測試 AUC 只當敏感度
pb_drop = {}
for drop in (['age'], ['marital'], ['age', 'marital']):
    num_, cat_ = [c for c in PB_NUM if c not in drop], [c for c in PB_CAT if c not in drop]
    m_ = pb_pipeline(pb_rf(n_jobs=-1, max_depth=pb_main_params['max_depth'], min_samples_leaf=pb_main_params['min_samples_leaf']),
                     cat_, num_).fit(pb_trT[num_ + cat_], pb_y_trT)
    m_.set_params(clf__n_jobs=1)
    pb_drop['_'.join(drop)] = pb_auc(pb_y_teT, m_.predict_proba(pb_teT[num_ + cat_])[:, 1])
display(pd.DataFrame({'test AUC after retraining': pb_drop, 'change vs all 11 features': {k: v - pb_auc_te for k, v in pb_drop.items()}}).round(4))
A3_KPI['part_b']['perm_importance'] = {r['feature'].replace('.', '_'): {'mean_auc_drop': a3_r(r['mean AUC drop']), 'sd': a3_r(r['sd'])}
                                       for _, r in pb_pi_tab.iterrows()}
A3_KPI['part_b']['perm_importance_rank'] = list(pb_pi_tab['feature'])
A3_KPI['part_b']['drop_retrain'] = {k: {'test_auc': a3_r(v), 'change': a3_r(v - pb_auc_te)} for k, v in pb_drop.items()}
'''

B_FIG5 = r'''
# [Fig 5] permutation importance 長條圖（關聯，不是因果）
fig, ax = plt.subplots(figsize=(6.6, 4.6), dpi=150)
t_ = pb_pi_tab.iloc[::-1]
ax.barh(t_['feature'], t_['mean AUC drop'], xerr=t_['sd'], color=PB_ACCENT, height=0.6,
        error_kw=dict(ecolor=PB_GREY, lw=0.8, capsize=2))
ax.axvline(0, color=PB_GREY, lw=0.8)
ax.set_xlabel('Drop in ROC-AUC when the column is shuffled (mean of 10 repeats, +/- sd)', fontsize=9.5)
ax.set_title('Fig 5. Permutation importance, pre-call model (test target group)', loc='left', fontsize=11)
ax.tick_params(labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', color='#ececec', lw=0.8)
ax.set_axisbelow(True)
fig.text(0.01, -0.02, 'Association with the model score, not a causal effect of the feature on buying.', fontsize=9, color=PB_GREY, va='top')
plt.show()
'''

B_XGB = r'''
# [Part B-11] 依 A2 表 7 勝出的 XGB：十條標準做與 RF 完全相同的評估（同樣的名單規則、門檻、bootstrap、資料口徑與判定規則）
# ①：同月同通數名單的 c(r)/r；②、ML②、ML③：B-2、B-3 已算；③④：同門檻對照組，去重與原始兩口徑（原始口徑在原始訓練集目標組上
# 用同樣固定的超參數重訓 XGB，scale_pos_weight 同樣取該訓練資料的負／正比）；⑤：2u − r；ML④：與 B-9 相同的分群與納入規則
pb_teTx, pb_teCx = pb_teT.assign(s=pb_teT['s_x']), pb_teC.assign(s=pb_teC['s_x'])
pb_upX, pb_upxX = pb_uplift(pb_teTx, pb_teCx, pb_K)
pb_rtrT_y = (pb_rtrT['y'] == 'yes').astype(int)
pb_raw_xgb = pb_pipeline(XGBClassifier(n_estimators=200, scale_pos_weight=float((pb_rtrT_y == 0).sum() / (pb_rtrT_y == 1).sum()),
                                       random_state=PB_SEED, n_jobs=1, **pb_xgb_params), PB_CAT).fit(pb_rtrT[PB_FEATURES], pb_rtrT_y)
pb_rteTx = pb_rteT.assign(s=pb_raw_xgb.predict_proba(pb_rteT[PB_FEATURES])[:, 1])
pb_rteCx = pb_rteC.assign(s=pb_raw_xgb.predict_proba(pb_rteC[PB_FEATURES])[:, 1])
pb_upX_raw, pb_upxX_raw = pb_uplift(pb_rteTx, pb_rteCx, pb_K_raw)
pb_b5X = {'dedup_ml_list': pb_net(pb_upxX['u'], pb_upxX['r']), 'raw_ml_list': pb_net(pb_upxX_raw['u'], pb_upxX_raw['r'])}
pb_segX = []
for dim, order in PB_ORDER.items():
    for gname in order:
        g = pb_teT[pb_teT[dim].astype(str) == gname]
        y = (g['y'] == 'yes').to_numpy()
        n1 = int(y.sum())
        pb_segX.append({'dimension': dim, 'group': gname, 'auc': pb_auc(y, g['s_x']) if 0 < n1 < len(y) else np.nan,
                        'in_gate': bool(PB_RULE[dim](gname, n1))})
pb_segX = pd.DataFrame(pb_segX)
pb_gapX = {dim: float(e['auc'].max() - e['auc'].min()) for dim, e in pb_segX[pb_segX['in_gate']].groupby('dimension')}


def pb_judge(m):
    """同一套判定規則（RF 與 XGB 共用）；m = 該模型的各項結果"""
    j = {'b1': '達標' if m['cost'] <= pb_a2['cost_per_conv_target_18pct'] else '未達',
         'b2': '達標' if m['b2_pass'] else ('未達' if m['b2_diff'] <= 0 else '未證實')}
    ud, ur = m['up_dedup'], m['up_raw']
    lows = [ud['uplift_ci_low_pp'], ur['uplift_ci_low_pp'], ud['period_stratified_ci_low_pp'], ur['period_stratified_ci_low_pp']]
    highs = [ud['uplift_ci_high_pp'], ur['uplift_ci_high_pp'], ud['period_stratified_ci_high_pp'], ur['period_stratified_ci_high_pp']]
    j['b3'] = '達標' if min(lows) > 0 else ('未達' if max(highs) < 0 else '未證實')
    wl, wh = min(ud['would_buy_ci_low_pct'], ur['would_buy_ci_low_pct']), max(ud['would_buy_ci_high_pct'], ur['would_buy_ci_high_pct'])
    j['b4'] = '未達' if wl > 50 else ('達標' if wh < 50 else '未證實')          # 對照 A2 式 2 的 50% 兩平參考
    j['b5'] = '示算'
    j['ml1'] = '達標' if pb_poc['auc_test'] >= 0.80 else '未達'
    j['ml2'] = '未達' if (m['auc'] < 0.75 or j['b2'] == '未達') else ('達標' if j['b2'] == '達標' else '未證實')
    j['ml3'] = '達標' if (pb_poc['gap_train_minus_test'] <= 0.05 and m['gap'] <= 0.05) else '未達'
    j['ml4'] = '達標' if all(v <= 0.05 for v in m['ml4_gaps'].values()) else '未達'
    j['ml5'] = '不可離線驗'
    return j


pb_m_rf = {'cost': pb_cost_per_conv(pb_r_L), 'b2_pass': pb_b2_pass, 'b2_diff': pb_diff, 'up_dedup': pb_up, 'up_raw': pb_up_raw,
           'auc': pb_auc_te, 'gap': pb_auc_tr - pb_auc_te, 'ml4_gaps': {d: v['max_minus_min'] for d, v in pb_gap.items()}}
pb_m_x = {'cost': pb_cost_per_conv(pb_conv(pb_Lx)), 'b2_pass': pb_b2_x_pass, 'b2_diff': pb_diff_x, 'up_dedup': pb_upX, 'up_raw': pb_upX_raw,
          'auc': pb_auc_x, 'gap': pb_auc_x_tr - pb_auc_x, 'ml4_gaps': pb_gapX}
pb_j_rf, pb_j_x = pb_judge(pb_m_rf), pb_judge(pb_m_x)


def pb_ud_txt(u):
    return '%+.2f [%+.2f, %+.2f]; within periods %+.2f [%+.2f, %+.2f]' % (
        u['uplift_pp'], u['uplift_ci_low_pp'], u['uplift_ci_high_pp'], u['period_stratified_uplift_pp'],
        u['period_stratified_ci_low_pp'], u['period_stratified_ci_high_pp'])


pb_cmp_rows = [
    ('① cost per conversion, month-matched list (A$)', '%.2f' % pb_m_rf['cost'], '%.2f' % pb_m_x['cost']),
    ('② list - mobile, same calls per month (pp), 95% CI B = 1,000', '%+.2f %s' % (100 * pb_diff, pb_iv(pb_ci_m['pct_lo'], pb_ci_m['pct_hi'])),
     '%+.2f %s' % (100 * pb_diff_x, pb_iv(pb_ci_x['pct_lo'], pb_ci_x['pct_hi']))),
    ('③ uplift, dedup (pp)', pb_ud_txt(pb_up), pb_ud_txt(pb_upX)),
    ('③ uplift, raw data (pp)', pb_ud_txt(pb_up_raw), pb_ud_txt(pb_upX_raw)),
    ('④ would-buy share, dedup / raw (%)', '%.1f / %.1f' % (pb_up['would_buy_share_pct'], pb_up_raw['would_buy_share_pct']),
     '%.1f / %.1f' % (pb_upX['would_buy_share_pct'], pb_upX_raw['would_buy_share_pct'])),
    ('⑤ 2u - r per call (D), dedup / raw', '%+.3f / %+.3f' % (pb_b5['dedup_ml_list']['net_D_per_call_excl_call_cost'], pb_b5['raw_ml_list']['net_D_per_call_excl_call_cost']),
     '%+.3f / %+.3f' % (pb_b5X['dedup_ml_list']['net_D_per_call_excl_call_cost'], pb_b5X['raw_ml_list']['net_D_per_call_excl_call_cost'])),
    ('ML② test AUC / within-period AUC', '%.4f / %.4f' % (pb_auc_te, pb_auc_wp), '%.4f / %.4f' % (pb_auc_x, pb_auc_x_wp)),
    ('ML③ train - test AUC', '%.4f' % (pb_auc_tr - pb_auc_te), '%.4f' % (pb_auc_x_tr - pb_auc_x)),
    ('ML④ AUC gap age / marital / month', ' / '.join('%.3f' % pb_m_rf['ml4_gaps'][d] for d in PB_ORDER),
     ' / '.join('%.3f' % pb_gapX[d] for d in PB_ORDER)),
]
display(pd.DataFrame(pb_cmp_rows, columns=['criterion', 'RF (main, pre-specified)', 'XGB (A2 table 7 winner)']))
pb_j_tab = pd.DataFrame({'RF': pb_j_rf, 'XGB': pb_j_x})
pb_j_tab['same'] = pb_j_tab['RF'] == pb_j_tab['XGB']
display(pb_j_tab.T)
print('judgements identical for all ten criteria:', bool(pb_j_tab['same'].all()))
A3_KPI['part_b']['xgb_eval'] = {
    'cost_formula': a3_r(pb_m_x['cost'], 2), 'b3b4_dedup': pb_upX, 'b3b4_raw': pb_upX_raw, 'b5': pb_b5X,
    'ml4_gaps': {d: a3_r(v) for d, v in pb_gapX.items()}, 'judgement': pb_j_x,
    'same_judgement_as_rf': bool(pb_j_tab['same'].all()), 'differs_on': [k for k, v in pb_j_tab['same'].items() if not v],
}
'''

B_KPI = r'''
# [Part B-12] A2 表 4 十條標準的紅綠燈總表（判定文字本身就是結論；顏色只是輔助）。主模型 RF；XGB 欄 = B-11 的同規則判定
pb_b1, pb_b2, pb_ml = A3_KPI['part_b']['b1'], A3_KPI['part_b']['b2'], A3_KPI['part_b']['ml']
pb_b34d, pb_b34r, pb_xe = pb_up, pb_up_raw, A3_KPI['part_b']['xgb_eval']


def pb_yes(k, v):
    """『是否達 A2 門檻』：是／否／離線無法判定"""
    if k in ('b3', 'b5', 'ml5'):
        return '離線無法判定' if v != '未達' else '否'
    if k == 'b4':
        return {'未達': '否（區間高於 50% 兩平參考）', '達標': '是（區間低於 50%）'}.get(v, '離線無法判定')
    return '是' if v == '達標' else '否'


pb_jr = pb_j_rf
pb_zero = [lab for lab, lo, hi in (('去重', pb_b34d['uplift_ci_low_pp'], pb_b34d['uplift_ci_high_pp']),
                                   ('原始', pb_b34r['uplift_ci_low_pp'], pb_b34r['uplift_ci_high_pp']),
                                   ('去重分時期', pb_b34d['period_stratified_ci_low_pp'], pb_b34d['period_stratified_ci_high_pp']),
                                   ('原始分時期', pb_b34r['period_stratified_ci_low_pp'], pb_b34r['period_stratified_ci_high_pp'])) if lo <= 0 <= hi]
pb_zero_txt = '、'.join(pb_zero) if pb_zero else '無'
pb_kpi = pd.DataFrame([
    ('業務① 每筆成交通話成本', '≤ A$%.2f（名單轉換率 18%%）；A/B 列報項' % pb_a2['cost_per_conv_target_18pct'], '表 4 業務①（草稿第 225 行）',
     '月配對名單 A$%.2f（實際秒數 A$%.2f；同時期配對 A$%.2f）；手機規則 A$%.2f；隨機 A$%.2f' % (pb_b1['ml_cost_formula'], pb_b1['ml_cost_actual'], pb_b1['ml_period_cost_formula'], pb_b1['mobile_cost_formula'], pb_b1['random_cost_formula']),
     pb_jr['b1'], pb_yes('b1', pb_jr['b1']), '%s（A$%.2f）' % (pb_j_x['b1'], pb_xe['cost_formula']),
     '名單變淺成本會降，但能降多少取決於時期（同月與同時期配對差很多）；深度要由 A/B 校準'),
    ('業務② 名單轉換率（上線硬門檻）', '高於同期手機規則組', '表 4 業務②（草稿第 226 行）',
     '月配對名單 %.2f%% vs 手機 %.2f%%：差 %+.2f pp，95%% 區間 [%+.2f, %+.2f]（percentile，B = 1,000）' % (pb_b2['ml_conv_pct'], pb_b2['mobile_conv_pct'], pb_b2['diff_pp'], pb_b2['ci_low_pp'], pb_b2['ci_high_pp']),
     pb_jr['b2'], pb_yes('b2', pb_jr['b2']), '%s（%+.2f pp [%+.2f, %+.2f]）' % (pb_j_x['b2'], pb_b2['xgb']['diff_pp'], pb_b2['xgb']['ci_low_pp'], pb_b2['xgb']['ci_high_pp']),
     '同時期配對：差 %+.2f pp，percentile [%+.2f, %+.2f]；+contact 同月 %+.2f pp [%+.2f, %+.2f]；B = 5,000、basic 區間與換種子見附錄 A' % (pb_b2['period']['diff_pp'], pb_b2['period']['ci_low_pp'], pb_b2['period']['ci_high_pp'], pb_b2['contact_diff_pp'], pb_b2['contact_ci_low_pp'], pb_b2['contact_ci_high_pp'])),
    ('業務③ 增量成交（上線硬門檻）', '為正：名單轉換率 > 同門檻對照組', '表 4 業務③（草稿第 227 行）',
     '單一門檻名單：去重 %+.2f pp [%+.2f, %+.2f]；原始 %+.2f pp [%+.2f, %+.2f]；分時期 %+.2f [%+.2f, %+.2f]／%+.2f [%+.2f, %+.2f]' % (pb_b34d['uplift_pp'], pb_b34d['uplift_ci_low_pp'], pb_b34d['uplift_ci_high_pp'], pb_b34r['uplift_pp'], pb_b34r['uplift_ci_low_pp'], pb_b34r['uplift_ci_high_pp'], pb_b34d['period_stratified_uplift_pp'], pb_b34d['period_stratified_ci_low_pp'], pb_b34d['period_stratified_ci_high_pp'], pb_b34r['period_stratified_uplift_pp'], pb_b34r['period_stratified_ci_low_pp'], pb_b34r['period_stratified_ci_high_pp']),
     pb_jr['b3'], pb_yes('b3', pb_jr['b3']), '%s（去重 %+.2f、原始 %+.2f；分時期 %+.2f／%+.2f）' % (pb_j_x['b3'], pb_xe['b3b4_dedup']['uplift_pp'], pb_xe['b3b4_raw']['uplift_pp'], pb_xe['b3b4_dedup']['period_stratified_uplift_pp'], pb_xe['b3b4_raw']['period_stratified_uplift_pp']),
     '兩組不是隨機分派、無客戶編號、去重不對稱；含 0 的區間：%s（共 4 個）→ 離線無法判定為正，確認排在 A/B' % pb_zero_txt),
    ('業務④ 本來就會買的比例（列報）', 'A/B 量出各組比例；兩平參考 50%', '表 4 業務④（草稿第 228 行）',
     '單一門檻名單：去重 %.1f%% [%.1f, %.1f]；原始 %.1f%% [%.1f, %.1f]（試點全體 %.1f%%）' % (pb_b34d['would_buy_share_pct'], pb_b34d['would_buy_ci_low_pct'], pb_b34d['would_buy_ci_high_pct'], pb_b34r['would_buy_share_pct'], pb_b34r['would_buy_ci_low_pct'], pb_b34r['would_buy_ci_high_pct'], pb_a2['pilot_would_buy_share_pct']),
     pb_jr['b4'], pb_yes('b4', pb_jr['b4']), '%s（%.1f%%／%.1f%%）' % (pb_j_x['b4'], pb_xe['b3b4_dedup']['would_buy_share_pct'], pb_xe['b3b4_raw']['would_buy_share_pct']),
     'A2 不設硬門檻；以式 2 的 50% 兩平點判讀：兩個口徑都高於 50%，即 2:1 下名單每多打一通都虧（與⑤一致）'),
    ('業務⑤ 式 1 淨值（上線硬門檻）', '不低於同期手機規則組', '表 4 業務⑤（草稿第 229 行）',
     '單一門檻名單 2u−r = %+.3f D／通（去重）、%+.3f D／通（原始）；隨機 %+.3f／%+.3f' % (pb_b5['dedup_ml_list']['net_D_per_call_excl_call_cost'], pb_b5['raw_ml_list']['net_D_per_call_excl_call_cost'], pb_b5['dedup_random']['net_D_per_call_excl_call_cost'], pb_b5['raw_random']['net_D_per_call_excl_call_cost']),
     pb_jr['b5'], pb_yes('b5', pb_jr['b5']), '%s（%+.3f／%+.3f D）' % (pb_j_x['b5'], pb_xe['b5']['dedup_ml_list']['net_D_per_call_excl_call_cost'], pb_xe['b5']['raw_ml_list']['net_D_per_call_excl_call_cost']),
     '2:1 假設下的示算；手機規則組的增量離線量不到（對照組沒有 contact）'),
    ('ML① 概念驗證 AUC', '≥ 0.80（只當樂觀參考）', '表 4 ML 第 1 列（草稿第 230 行）',
     '測試 %.4f／訓練 %.4f（全部測試列）' % (pb_ml['ml1_poc_test_auc'], pb_ml['ml1_poc_train_auc']),
     pb_jr['ml1'], pb_yes('ml1', pb_jr['ml1']), '（同一個官方模型）', '含 duration（通話後才知），測試集也被官方 cell-53 拿來選模'),
    ('ML② 撥號前 AUC', '≥ 0.75，且 ② 勝過同期手機規則組', '表 4 ML 第 2 列（草稿第 231 行）',
     'AUC %.4f（測試集目標組；≥ 0.75：%s）；② %s' % (pb_ml['ml2_test_auc'], '是' if pb_ml['ml2_test_auc'] >= 0.75 else '否', pb_jr['b2']),
     pb_jr['ml2'], pb_yes('ml2', pb_jr['ml2']), '%s（AUC %.4f；② %s）' % (pb_j_x['ml2'], pb_ml['xgb_test_auc'], pb_j_x['b2']),
     '同一 (cpi, cci) 時期內 AUC 只有 %.4f（XGB %.4f）；LR 基準 %.4f' % (pb_ml['ml2_within_period_auc'], pb_ml['xgb_within_period_auc'], pb_ml['ml2_lr_test_auc'])),
    ('ML③ 過擬合（訓練−測試 AUC）', '≤ 0.05', '表 4 ML 第 3 列（草稿第 232 行）',
     '概念驗證 %+.4f；撥號前 %+.4f' % (pb_ml['ml1_poc_gap'], pb_ml['ml3_precall_gap']),
     pb_jr['ml3'], pb_yes('ml3', pb_jr['ml3']), '%s（%+.4f）' % (pb_j_x['ml3'], pb_ml['xgb_gap']),
     '撥號前版本的超參數只用訓練資料選出；設計階段曾預跑同一測試集，屬樂觀估計'),
    ('ML④ 分群一致性', '各群 AUC 差 ≤ 0.05', '表 4 ML 第 4 列（草稿第 233 行）',
     '年齡 %.3f；婚姻 %.3f；月份（代理時期）%.3f' % (pb_gap['age_band']['max_minus_min'], pb_gap['marital']['max_minus_min'], pb_gap['month']['max_minus_min']),
     pb_jr['ml4'], pb_yes('ml4', pb_jr['ml4']), '%s（%.3f／%.3f／%.3f）' % (pb_j_x['ml4'], pb_xe['ml4_gaps']['age_band'], pb_xe['ml4_gaps']['marital'], pb_xe['ml4_gaps']['month']),
     '舊資格母體；小群樣本不足（區間寬）；入選比例另列報給法遵'),
    ('ML⑤ 增量排序模型', '名單內平均增量 > 全體', '表 4 ML 第 5 列（草稿第 234 行）', '未建（依 A2 設計，12 週後才有資料）',
     pb_jr['ml5'], pb_yes('ml5', pb_jr['ml5']), pb_j_x['ml5'], '需要常設對照組＋隨機外撥組；試點沒有客戶編號'),
], columns=['標準', 'A2 門檻', 'A2 出處（表號／草稿行）', 'A3 結果（RF 主模型；標明名單口徑）', '判定', '是否達 A2 門檻', 'XGB（表 7 勝出者）', '說明'])
PB_COLOR = {'達標': '#d9ead3', '未達': '#f4cccc', '未證實': '#fff2cc', '示算': '#e8e8e8', '不可離線驗': '#e8e8e8'}
display(pb_kpi.style.apply(lambda col: ['background-color: %s; font-weight: bold' % PB_COLOR[v] for v in col], subset=['判定'])
        .set_properties(**{'text-align': 'left'}).hide(axis='index'))
print('RF judgements:', pb_kpi['判定'].value_counts().to_dict(), '| XGB judgements identical:', bool(pb_j_tab['same'].all()))
A3_KPI['part_b']['kpi_counts'] = {k: int((pb_kpi['判定'] == k).sum()) for k in PB_COLOR}
A3_KPI['part_b']['kpi_judgement'] = dict(zip(['b1', 'b2', 'b3', 'b4', 'b5', 'ml1', 'ml2', 'ml3', 'ml4', 'ml5'], pb_kpi['判定']))
A3_KPI['part_b']['kpi_meets_a2'] = dict(zip(['b1', 'b2', 'b3', 'b4', 'b5', 'ml1', 'ml2', 'ml3', 'ml4', 'ml5'], pb_kpi['是否達 A2 門檻']))
A3_KPI['part_b']['kpi_business_pass'] = int(sum(A3_KPI['part_b']['kpi_judgement'][k] == '達標' for k in ['b1', 'b2', 'b3', 'b4', 'b5']))
A3_KPI['part_b']['b3_ci_include_zero'] = pb_zero
'''

B_GOALS = r'''
# [Part B-13] A2 表 1 的商業目標（目標層級）：現況 → 目標 → A3 離線結果（金額都用未取整的數字相減後才取整）
pb_ext = A3_KPI['part_b']['b1']['one_round_extrapolation']
pb_save_target = PB_PILOT_COST - pb_ext['a2_target_18pct']['call_cost_exact']          # A2：每輪約省 A$14,900
pb_save_ml = PB_PILOT_COST - pb_ext['ml_list']['call_cost_exact']
pb_save_ml_vs_mob = pb_ext['mobile']['call_cost_exact'] - pb_ext['ml_list']['call_cost_exact']
pb_save_ml_p = PB_PILOT_COST - pb_ext['ml_list_period']['call_cost_exact']
# 金額視角（hd 修訂新增；全部示算，都用未取整的數字相減後才取整）
# (1) 依手機規則的月份組成隨機外撥（B-3 的轉換率）外推一輪：現況是全體隨機外撥、沒有控制月份，這一列把月份組成的功勞分出來
pb_ext_rmm = pb_round_cost(pb_r_rand_mm)
pb_save_rmm = PB_PILOT_COST - pb_ext_rmm['call_cost_exact']
pb_save_ml_vs_rmm = pb_ext_rmm['call_cost_exact'] - pb_ext['ml_list']['call_cost_exact']
pb_save_mob_vs_rmm = pb_ext_rmm['call_cost_exact'] - pb_ext['mobile']['call_cost_exact']
# (2) 名單就算達到 A2 目標（轉換率 18%），每輪最多比手機規則多省多少通話費
pb_save_tgt_vs_mob = pb_ext['mobile']['call_cost_exact'] - pb_ext['a2_target_18pct']['call_cost_exact']
# (3) 折扣外溢：同樣 2,300 筆成交，送給本來就會買者的折扣 = 2,300 x 本來就會買的比例 x D（示例 D = A$36、收益：折扣 = 2:1）
#     本來就會買的比例 = 同門檻對照組轉換率 / 名單轉換率（B-6，未取整）；試點用 A2 全體 13.04% 對 9.94%
PB_ROUND_CONV = 2300
pb_wb = {'pilot': pb_r_ctrl_raw / pb_r_pilot, 'raw': pb_upx_raw['rC'] / pb_upx_raw['r'], 'dedup': pb_upx['rC'] / pb_upx['r']}
pb_spill = {k: PB_ROUND_CONV * v * PB_D for k, v in pb_wb.items()}
pb_D_star = {k: pb_save_tgt_vs_mob / (PB_ROUND_CONV * pb_wb[k]) for k in ('raw', 'dedup')}   # 白送的折扣 > (2) 所需的 D


def pb_spend(r, share):
    # 一輪（2,300 筆成交）的支出拆成三段：未成交電話、成交電話（兩段相加 = 2,300 x c(r)/r）、送給本來就會買者的折扣
    calls = PB_ROUND_CONV / r
    return {'calls': int(round(calls)), 'unconverted_calls_aud': int(round((calls - PB_ROUND_CONV) * PB_CALL_NO)),
            'converted_calls_aud': int(round(PB_ROUND_CONV * PB_CALL_YES)),
            'wouldbuy_discount_aud': int(round(PB_ROUND_CONV * share * PB_D)), 'would_buy_share_pct': a3_r(100 * share, 1)}


pb_spend_rows = {'pilot': pb_spend(pb_r_pilot, pb_wb['pilot']), 'ml_list_raw_share': pb_spend(pb_r_L, pb_wb['raw']),
                 'ml_list_dedup_share': pb_spend(pb_r_L, pb_wb['dedup'])}


def pb_mult(u, r):
    return '%.1f×' % (r / u) if u > 0 else '無（增量 ≤ 0）'


pb_goal = pd.DataFrame([
    ('增量成交（外撥＋優惠帶來）', '每千名外撥約 %.0f 人' % (10 * pb_a2['pilot_uplift_pp']), '為正（同門檻對照組）',
     '每千通：去重 %+.1f、原始 %+.1f；控制時期後 %+.1f／%+.1f（區間都含 0）' % (pb_up['uplift_per_1000_calls'], pb_up_raw['uplift_per_1000_calls'], 10 * pb_up['period_stratified_uplift_pp'], 10 * pb_up_raw['period_stratified_uplift_pp']),
     A3_KPI['part_b']['kpi_judgement']['b3']),
    ('成交者中本來就會買的比例（折扣外溢）', '約 %.0f%%' % pb_a2['pilot_would_buy_share_pct'], 'A/B 量出（第一步可能升高；兩平 50%）',
     '去重 %.1f%%、原始 %.1f%%（兩者的區間都高於 50%%）' % (pb_up['would_buy_share_pct'], pb_up_raw['would_buy_share_pct']),
     A3_KPI['part_b']['kpi_judgement']['b4']),
    ('每輪通話成本（同樣 2,300 筆成交）', 'A$%s' % format(int(round(PB_PILOT_COST)), ','),
     '約 A$%s，每輪省約 A$%s' % (format(pb_ext['a2_target_18pct']['call_cost'], ','), format(int(round(pb_save_target)), ',')),
     'ML 名單外推 A$%s：比現況省 A$%s（目標節省的 %.0f%%），但比同月組成的隨機外撥（A$%s）只省 A$%s（目標的 %.0f%%）、'
     '比手機規則（A$%s）只省 A$%s；同時期配對 A$%s' % (
         format(pb_ext['ml_list']['call_cost'], ','), format(int(round(pb_save_ml)), ','), 100 * pb_save_ml / pb_save_target,
         format(pb_ext_rmm['call_cost'], ','), format(int(round(pb_save_ml_vs_rmm)), ','), 100 * pb_save_ml_vs_rmm / pb_save_target,
         format(pb_ext['mobile']['call_cost'], ','), format(int(round(pb_save_ml_vs_mob)), ','), format(pb_ext['ml_list_period']['call_cost'], ',')),
     '未達' if pb_save_ml < pb_save_target else '達標'),
    ('外撥量', '%s 通' % format(pb_a2['pilot_target_n'], ','), '少約 %.0f%%' % pb_ext['a2_target_18pct']['fewer_calls_vs_pilot_pct'],
     'ML 名單少 %.1f%%（手機規則 %.1f%%）' % (pb_ext['ml_list']['fewer_calls_vs_pilot_pct'], pb_ext['mobile']['fewer_calls_vs_pilot_pct']),
     '未達' if pb_ext['ml_list']['fewer_calls_vs_pilot_pct'] < pb_ext['a2_target_18pct']['fewer_calls_vs_pilot_pct'] else '達標'),
    ('不依 2:1 的兩平：每張卡收益 ÷ 折扣至少要幾倍（r ÷ u，未計通話費）', '%s（試點）' % pb_mult(pb_r_pilot - pb_r_ctrl_raw, pb_r_pilot), '越低越好（A2 假設框）',
     'ML 名單：原始 %s、去重 %s；控制時期後 原始 %s、去重 %s' % (pb_mult(pb_upx_raw['u'], pb_upx_raw['r']), pb_mult(pb_upx['u'], pb_upx['r']),
                                                 pb_mult(pb_upx_raw['u_period'], pb_upx_raw['r']), pb_mult(pb_upx['u_period'], pb_upx['r'])),
     '示算'),
], columns=['A2 表 1 目標', '現況（試點）', 'A2 目標', 'A3 離線結果', '判定'])
display(pb_goal.style.apply(lambda col: ['background-color: %s; font-weight: bold' % PB_COLOR[v] for v in col], subset=['判定'])
        .set_properties(**{'text-align': 'left'}).hide(axis='index'))
print('Money view per round of 2,300 conversions (illustrative; A$50 per hour, call time only; discount D = A$36, revenue : discount = 2:1)')
display(pd.DataFrame([
    ('依手機規則月份組成的隨機外撥（%.2f%%）外推一輪' % (100 * pb_r_rand_mm), 'A$%s' % format(pb_ext_rmm['call_cost'], ','),
     '比現況（全體隨機外撥）省 A$%s：只靠月份組成' % format(int(round(pb_save_rmm)), ',')),
    ('同月配對名單 vs 同月組成的隨機外撥', '省 A$%s' % format(int(round(pb_save_ml_vs_rmm)), ','),
     'A2 目標節省的 %.0f%%；手機規則 vs 同月組成的隨機外撥：省 A$%s' % (100 * pb_save_ml_vs_rmm / pb_save_target, format(int(round(pb_save_mob_vs_rmm)), ','))),
    ('名單達 A2 目標（18%）時，相對手機規則最多多省', 'A$%s' % format(int(round(pb_save_tgt_vs_mob)), ','),
     '目前同月配對名單實際多省 A$%s' % format(int(round(pb_save_ml_vs_mob)), ',')),
    ('每輪送給本來就會買者的折扣（D = A$36）', '試點 A$%s；名單 原始 A$%s／去重 A$%s' % tuple(format(int(round(pb_spill[k])), ',') for k in ('pilot', 'raw', 'dedup')),
     '本來就會買的比例 %.1f%%／%.1f%%／%.1f%%' % tuple(100 * pb_wb[k] for k in ('pilot', 'raw', 'dedup'))),
    ('白送的折扣超過上上列「最多多省」所需的 D', 'A$%.2f（原始）／A$%.2f（去重）' % (pb_D_star['raw'], pb_D_star['dedup']),
     '每張卡折扣高於此值，白送的折扣就超過名單最多能多省的通話費'),
], columns=['項目（每輪 2,300 筆成交）', '金額', '說明']))
A3_KPI['part_b']['goals'] = {
    'pilot_call_cost_aud': int(round(PB_PILOT_COST)),
    'saving_target_aud': int(round(pb_save_target)), 'saving_ml_vs_pilot_aud': int(round(pb_save_ml)),
    'saving_ml_share_of_target_pct': a3_r(100 * pb_save_ml / pb_save_target, 1), 'saving_ml_vs_mobile_aud': int(round(pb_save_ml_vs_mob)),
    'saving_ml_period_vs_pilot_aud': int(round(pb_save_ml_p)),
    'fewer_calls_ml_pct': pb_ext['ml_list']['fewer_calls_vs_pilot_pct'], 'fewer_calls_mobile_pct': pb_ext['mobile']['fewer_calls_vs_pilot_pct'],
    'fewer_calls_target_pct': pb_ext['a2_target_18pct']['fewer_calls_vs_pilot_pct'],
    'multiple_pilot': a3_r(pb_r_pilot / (pb_r_pilot - pb_r_ctrl_raw), 1),
    'multiple_ml_raw': a3_r(pb_upx_raw['r'] / pb_upx_raw['u'], 1) if pb_upx_raw['u'] > 0 else None,
    'multiple_ml_dedup': a3_r(pb_upx['r'] / pb_upx['u'], 1) if pb_upx['u'] > 0 else None,
    'multiple_ml_raw_period': a3_r(pb_upx_raw['r'] / pb_upx_raw['u_period'], 1) if (pb_upx_raw['u_period'] or 0) > 0 else None,
    'multiple_ml_dedup_period': a3_r(pb_upx['r'] / pb_upx['u_period'], 1) if (pb_upx['u_period'] or 0) > 0 else None,
    'judgement': dict(zip(['incremental', 'spillover', 'round_cost', 'fewer_calls', 'revenue_multiple'], pb_goal['判定'])),
}
# hd 修訂新增的鍵（上面的鍵一個都不改）
A3_KPI['part_b']['goals'].update({
    'random_mm_round': pb_ext_rmm,
    'saving_random_mm_vs_pilot_aud': int(round(pb_save_rmm)),
    'saving_ml_vs_random_mm_aud': int(round(pb_save_ml_vs_rmm)),
    'saving_ml_vs_random_mm_share_of_target_pct': a3_r(100 * pb_save_ml_vs_rmm / pb_save_target, 1),
    'saving_mobile_vs_random_mm_aud': int(round(pb_save_mob_vs_rmm)),
    'saving_target_vs_mobile_aud': int(round(pb_save_tgt_vs_mob)),
    'spillover_discount_per_round_D36_aud': {k: int(round(v)) for k, v in pb_spill.items()},
    'D_spill_exceeds_target_vs_mobile_saving_aud': {k: a3_r(v, 2) for k, v in pb_D_star.items()},
    'round_spend_D36': pb_spend_rows,
})
'''

B_FIG7 = r'''
# [Fig 7] 每輪通話成本（同樣 2,300 筆成交；A2 表 1 的目標層級）：現況、同月組成的隨機外撥、手機規則、ML 名單、A2 目標（外推值，不是測得的）
pb_bars = [('Pilot today (random calling)', PB_PILOT_COST, PB_LIGHT, None),
           ('Random, mobile-rule month mix', pb_ext_rmm['call_cost_exact'], '#dcdcdc', None),
           ('Mobile rule', pb_ext['mobile']['call_cost_exact'], PB_GREY, None),
           ('ML list, month-matched', pb_ext['ml_list']['call_cost_exact'], PB_ACCENT, None),
           ('ML list, period-matched', pb_ext['ml_list_period']['call_cost_exact'], PB_ACCENT, None),
           ('A2 target (18% conversion)', pb_ext['a2_target_18pct']['call_cost_exact'], 'white', '///')]
fig, ax = plt.subplots(figsize=(6.8, 4.8), dpi=150)
fig.subplots_adjust(left=0.36, right=0.97, top=0.92, bottom=0.25)
for i, (lab, v, col, hat) in enumerate(pb_bars):
    ax.barh(i, v, color=col, edgecolor='black' if col == 'white' else col, lw=0.9, height=0.62, hatch=hat)
    note = '' if i == 0 else r'  (%sA\$%s vs today)' % ('−' if v < PB_PILOT_COST else '+', format(int(round(abs(PB_PILOT_COST - v))), ','))
    ax.text(v + 600, i, r'A\$%s%s' % (format(int(round(v)), ','), note), va='center', fontsize=9)
ax.set_yticks(range(len(pb_bars)))
ax.set_yticklabels([b[0] for b in pb_bars], fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, PB_PILOT_COST * 1.8)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: format(int(v), ',')))
ax.set_xlabel(r'Call cost per round of 2,300 conversions (A\$)', fontsize=10)
ax.set_title('Fig 7. Call cost per round (2,300 conversions)', loc='left', fontsize=11)
ax.tick_params(axis='x', labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', color='#ececec', lw=0.8)
ax.set_axisbelow(True)
fig.text(0.01, 0.135, r'Month-matched ML list: A\$%s less than the mobile rule and A\$%s less than random calling' '\n'
         r'with the same month mix. Extrapolated from test-set conversion rates; A\$50 per hour, call time only.'
         % (format(int(round(pb_save_ml_vs_mob)), ','), format(int(round(pb_save_ml_vs_rmm)), ',')), fontsize=9, color='black', va='top')
plt.show()
'''

B_FIG6 = r'''
# [Fig 6] 混淆矩陣（B-5 主表：同月同通數名單）畫成 2×2；格內是人數與通話成本（A2 假設：時薪 A$50、只計通話時間）
from matplotlib.colors import LinearSegmentedColormap
pb_cmg = np.array([[pb_cm_m['TP'], pb_cm_m['FN']], [pb_cm_m['FP'], pb_cm_m['TN']]])
fig, ax = plt.subplots(figsize=(6.6, 5.0), dpi=150)
ax.imshow(pb_cmg / pb_cmg.max(), cmap=LinearSegmentedColormap.from_list('a3', ['#ffffff', '#9fbfe3']), vmin=0, vmax=1, aspect='auto')
pb_cm_txt = [[('TP  %s' % format(pb_cm_m['TP'], ','), 'bought, on the list\nA\\$%.2f call + one discount each\n(some would buy anyway)' % PB_CALL_YES),
              ('FN  %s' % format(pb_cm_m['FN'], ','), 'bought, not on the list\nsome still buy without a call;\nloss = only those who need it')],
             [('FP  %s' % format(pb_cm_m['FP'], ','), 'did not buy, on the list\nwasted calls: A\\$%.2f each\n= about A\\$%s' % (PB_CALL_NO, format(pb_cm_m['fp_cost_aud'], ','))),
              ('TN  %s' % format(pb_cm_m['TN'], ','), 'did not buy, not on the list\ncalls saved: about A\\$%s' % format(pb_cm_m['tn_saving_aud'], ','))]]
for i in range(2):
    for j in range(2):
        head, body = pb_cm_txt[i][j]
        ax.text(j, i - 0.25, head, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(j, i + 0.13, body, ha='center', va='center', fontsize=9.5, linespacing=1.2)
ax.set_xticks([0, 1])
ax.set_xticklabels(['On the list (called)', 'Not on the list (not called)'], fontsize=10)
ax.set_yticks([0, 1])
ax.set_yticklabels(['Bought', 'Did not buy'], fontsize=10)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_title('Fig 6. Confusion matrix, month-matched list (%s calls)' % format(pb_K, ','), loc='left', fontsize=11)
fig.text(0.01, -0.01, 'Precision %.1f%%, recall %.1f%% (mobile rule recall %.1f%%). Shading = count.\n'
         'Costs use the A2 assumptions (A\\$50 per hour, call time only).'
         % (pb_cm_m['precision_pct'], pb_cm_m['recall_pct'], 100 * pb_mob_rec), fontsize=9, color=PB_GREY, va='top')
plt.show()
'''

B_FIG8 = r'''
# [Fig 8] 每輪的錢花在哪（示算）：同樣 2,300 筆成交時的未成交電話、成交電話，與送給本來就會買者的折扣（示例 D = A$36、收益：折扣 = 2:1）
# 數字都是 B-13 已算好的（pb_wb、pb_r_pilot、pb_r_L）；名單的通話段用同月配對名單（同 Fig 7）
pb_sp_rows = [('Pilot today (random calling)\nwould-buy share %.1f%% (A2)' % (100 * pb_wb['pilot']), pb_r_pilot, pb_wb['pilot']),
              ('ML list, month-matched\nwould-buy share %.1f%% (raw data)' % (100 * pb_wb['raw']), pb_r_L, pb_wb['raw']),
              ('ML list, month-matched\nwould-buy share %.1f%% (dedup)' % (100 * pb_wb['dedup']), pb_r_L, pb_wb['dedup'])]
pb_sp_cols = [('Calls that did not convert', PB_LIGHT, 'black'), ('Calls that converted', PB_GREY, 'white'),
              (r'Discount given to customers who would buy anyway (D = A\$36)', PB_ACCENT, 'white')]
fig = plt.figure(figsize=(6.8, 5.4), dpi=150)
ax = fig.add_axes([0.36, 0.42, 0.61, 0.50])
pb_sp_max = 0.0
for i, (lab, r_, sh_) in enumerate(pb_sp_rows):
    calls_ = PB_ROUND_CONV / r_
    seg_ = [(calls_ - PB_ROUND_CONV) * PB_CALL_NO, PB_ROUND_CONV * PB_CALL_YES, PB_ROUND_CONV * sh_ * PB_D]
    left_ = 0.0
    for v_, (lab_k, col_k, txt_k) in zip(seg_, pb_sp_cols):
        ax.barh(i, v_, left=left_, color=col_k, height=0.62, edgecolor='white', lw=1, label=lab_k if i == 0 else None)
        ax.text(left_ + v_ / 2, i, '%.1fk' % (v_ / 1000), ha='center', va='center', fontsize=9, color=txt_k)
        left_ += v_
    pb_sp_max = max(pb_sp_max, left_)
ax.set_yticks(range(len(pb_sp_rows)))
ax.set_yticklabels([r_[0] for r_ in pb_sp_rows], fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, pb_sp_max * 1.04)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: format(int(v), ',')))
ax.set_xlabel(r'A\$ per round of 2,300 conversions (bar labels in thousands)', fontsize=10)
ax.set_title('Fig 8. Where the money goes per round (illustrative)', loc='left', fontsize=11)
ax.tick_params(axis='x', labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', color='#ececec', lw=0.8)
ax.set_axisbelow(True)
fig.legend(frameon=False, fontsize=9, loc='upper left', bbox_to_anchor=(0.005, 0.315), ncol=1)
fig.text(0.01, 0.185, r'Illustrative: D = A\$36 is the A2 example discount (revenue : discount = 2:1), not a real figure.' '\n'
         r'Calls: A\$50 per hour, call time only; the ML list uses the month-matched list (as in Fig 7).' '\n'
         'Would-buy share = control conversion / list conversion above the same score cut-off (B-6).\n'
         r'Even at the A2 target, the list would save at most A\$%s per round vs the mobile rule.'
         % format(int(round(pb_save_tgt_vs_mob)), ','), fontsize=9, color=PB_GREY, va='top')
plt.show()
'''

B_FIG9 = r'''
# [Fig 9] 撥號前 AUC 從哪來：概念驗證（含 duration）→ 撥號前（全部月份）→ 月內 → 同一 (cpi, cci) 時期內。只畫 B-2 已算好的數字
pb_ml_k = A3_KPI['part_b']['ml']
pb_auc_bars = [('Proof of concept, official model\n(with duration; all test rows)', pb_ml_k['ml1_poc_test_auc'], PB_LIGHT),
               ('Pre-call RF, all months', pb_ml_k['ml2_test_auc'], PB_ACCENT),
               ('Pre-call RF, within month', pb_ml_k['ml2_within_month_auc'], PB_ACCENT),
               ('Pre-call RF, within (cpi, cci) period', pb_ml_k['ml2_within_period_auc'], PB_ACCENT)]
fig = plt.figure(figsize=(6.6, 4.2), dpi=150)
ax = fig.add_axes([0.37, 0.27, 0.60, 0.62])
for i, (lab, v, col) in enumerate(pb_auc_bars):
    ax.barh(i, v, color=col, height=0.58)
    ax.text(0.015, i, '%.4f' % v, va='center', ha='left', fontsize=10, fontweight='bold',
            color='black' if col == PB_LIGHT else 'white')
ax.axvline(0.75, color='black', ls='--', lw=1.1)
ax.axvline(0.5, color='black', ls=':', lw=1.4)
ax.text(0.75, -0.62, 'A2 gate 0.75', ha='center', va='bottom', fontsize=9)
ax.text(0.5, -0.62, 'random 0.5', ha='center', va='bottom', fontsize=9)
ax.set_yticks(range(len(pb_auc_bars)))
ax.set_yticklabels([b[0] for b in pb_auc_bars], fontsize=9.5)
ax.set_ylim(len(pb_auc_bars) - 0.5, -0.95)
ax.set_xlim(0, 1)
ax.set_xlabel('Test ROC-AUC', fontsize=10)
ax.set_title('Fig 9. Where the pre-call AUC comes from', loc='left', fontsize=11)
ax.tick_params(axis='x', labelsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', color='#ececec', lw=0.8)
ax.set_axisbelow(True)
fig.text(0.01, 0.15, 'Dashed: A2 gate for ML2 (0.75); dotted: random ranking (0.5). Pre-call RF: 11 pre-call columns,\n'
         'test target group (%s customers). Within month / period: AUC inside each month / (cpi, cci) period,\n'
         'weighted by rows; one period is about one year-month.'
         % format(len(pb_teT), ','), fontsize=9, color=PB_GREY, va='top')
plt.show()
'''

B_LAT = r'''
# [Part B-14] 批次評分耗時（A2 表 8 可擴展性／延遲）：硬體相依、只當量級；不進判定，也不列入跨次執行的一致性比對
# 撥號前 RF（主模型）與 XGB（表 7 勝出者）替整個測試集（目標組＋對照組）單執行緒批次評分，重複 5 次取中位數；不改任何模型或資料
import time
pb_X_all = pd.concat([pb_teT[PB_FEATURES], pb_teC[PB_FEATURES]])


def pb_time(m, n=5):
    t_ = []
    for _ in range(n):
        t0_ = time.perf_counter()
        m.predict_proba(pb_X_all)
        t_.append(time.perf_counter() - t0_)
    return float(np.median(t_))


pb_lat_rf, pb_lat_x = pb_time(pb_main), pb_time(pb_xgb)
print('batch scoring of %s customers, single thread, median of 5 runs: RF %.3f s, XGB %.3f s (hardware-dependent)'
      % (format(len(pb_X_all), ','), pb_lat_rf, pb_lat_x))
A3_KPI['part_b']['scoring_latency'] = {
    'rows': len(pb_X_all), 'repeats': 5, 'threads': 1, 'rf_median_s': a3_r(pb_lat_rf, 3), 'xgb_median_s': a3_r(pb_lat_x, 3),
    'rf_ms_per_1000_rows': a3_r(1000 * pb_lat_rf / len(pb_X_all) * 1000, 1),
    'note': 'wall-clock time on the build machine; hardware-dependent; excluded from the run-to-run check'}
'''

B_JSON = r'''
# [附錄] 本次執行的數字總表（JSON）。markdown 中的數字都由它填入；第一、二層每個鍵各佔一行，以免輸出過長
A3_KPI['meta'] = {
    'student': 'Po-Kai Huang 26254793', 'subject': '321513 Machine Learning AT3 (business focus)',
    'versions': {'python': sys.version.split()[0], 'numpy': np.__version__, 'pandas': pd.__version__,
                 'scikit-learn': sklearn.__version__, 'xgboost': xgboost.__version__, 'scipy': scipy.__version__,
                 'matplotlib': matplotlib.__version__, 'seaborn': sns.__version__},
    'rows': {'raw': pb_a2['raw_rows'], 'dedup': pb_a2['dedup_rows'], 'train': len(pb_train), 'test': len(pb_test),
             'test_target': len(pb_teT), 'test_control': len(pb_teC), 'train_target': len(pb_trT)},
    'split': {'test_size': 0.4, 'random_state': RANDOM_SATE, 'stratify': None},
    'poc_grid': {'max_depth': [3, 5, 9], 'criterion': ['gini', 'entropy'], 'n_estimators': [100, 200, 300]},
    'poc_best_params': A3_KPI['part_a']['final_pipeline']['best_params'],
    'precall_main_params': pb_main_params, 'precall_contact_params': pb_ct_params,
    'precall_grid': {'max_depth': [5, 7, 9], 'min_samples_leaf': [1, 20], 'n_estimators': 300, 'cv': 'StratifiedKFold(5, shuffle, 123)'},
    'xgb_challenger_grid': {'max_depth': [3, 5], 'learning_rate': [0.05, 0.1], 'n_estimators': 200, 'scale_pos_weight': 'neg/pos of the training target group'},
    'xgb_challenger_params': A3_KPI['part_b']['models']['xgb_params'],
    'bootstrap': {'b2_B_plan': PB_B2_B, 'b2_B_check': PB_B2_B_CHECK, 'b2_extra_seeds': 10, 'b3_B': 1000, 'b3_period_B': 1000,
                  'b8_B': 1000, 'ml4_B': 500, 'seed': PB_SEED},
    'b2_gate_rule': 'difference > 0 and 95% percentile CI lower bound > 0 (B = 1,000, seed 123)',
    'xgb_replacement_rule': 'A2 table 7: mean CV-AUC margin over 5 seeds (123-127) > RF seed-to-seed range, and ahead on every seed',
    'cost_assumptions': {'hourly_aud': PB_HOURLY, 'sec_yes': pb_a2['sec_yes'], 'sec_no': pb_a2['sec_no'], 'D_example_aud': PB_D,
                         'revenue_to_discount': '2:1'},
}


def pb_clean_json(o):
    if isinstance(o, dict):
        return {str(k): pb_clean_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [pb_clean_json(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (int, np.integer)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return None if np.isnan(o) else round(float(o), 6)
    return o


def pb_dump(o):
    """合法 JSON；第一、二層的鍵各佔一行，更深的內容壓成一行"""
    out = ['{']
    keys = list(o)
    for i, k in enumerate(keys):
        tail = ',' if i < len(keys) - 1 else ''
        v = o[k]
        if isinstance(v, dict) and v:
            out.append(' %s: {' % json.dumps(k, ensure_ascii=False))
            sub = list(v)
            for j, kk in enumerate(sub):
                out.append('  %s: %s%s' % (json.dumps(kk, ensure_ascii=False), json.dumps(v[kk], ensure_ascii=False),
                                           ',' if j < len(sub) - 1 else ''))
            out.append(' }' + tail)
        else:
            out.append(' %s: %s%s' % (json.dumps(k, ensure_ascii=False), json.dumps(v, ensure_ascii=False), tail))
    out.append('}')
    return '\n'.join(out)


pb_json_txt = pb_dump(pb_clean_json(A3_KPI))
assert json.loads(pb_json_txt) == pb_clean_json(A3_KPI)
print('===A3_KPI_JSON_BEGIN===')
print(pb_json_txt)
print('===A3_KPI_JSON_END===')
'''

# ----------------------------------------------------------------------------------------------------------------
# 4) markdown (Traditional Chinese). {{path}} / {{path|fmt}} are filled from the notebook's own KPI JSON
# ----------------------------------------------------------------------------------------------------------------
MD = {}

MD['intro'] = r'''
<a id="a3-top" name="a3-top"></a>
# A3 說明

**學生**：黃柏凱（Po-Kai Huang，26254793）｜321513 Machine Learning｜Assessment 3｜**選擇的方向：商業（Business focus）**，情境為 Bank X 信用卡電話行銷。

**目錄**（Colab 左側的「目錄」面板也可以依標題跳轉）
- [Part A｜官方流程與解讀](#part-a)：官方 cell 依原順序執行，每段輸出後插一格「解讀」。
- [Part B｜商業評估：對照 A2 成功標準](#part-b)：開頭先給答案 → [十條標準一覽](#part-b-summary) → B-0～B-14 逐條證據 → [結論](#conclusion) → [B3、B4 摘要](#b3-b4-summary) → 附錄 A（業務② 區間的穩健性）與數字總表。

本 notebook 以官方 `AT3_TeleMarketing.ipynb` 為底：官方 cell 依原順序全部保留，官方 markdown 原為簡體中文，只用 OpenCC 轉成繁體字（只轉字形，用語維持官方原文）；只在下表的地方修改官方程式碼，每處都以 `# [A3 修正]` 註明（四格 Tech Focus Only 只加一行 `# [A3]` 說明註解）。我新增的 cell 以 `[A3 新增]`（Part A）或 `[Part B-n]`、`[Fig n]`（Part B）開頭，說明用繁體中文；圖內文字用英文（Colab 沒有中文字型）。文中「官方 cell-N」指官方原檔的第 N 格（從 0 起算）；Colab 不顯示格號，所以引用時都會附上那一格在做什麼。

**官方 cell 的修改（全部）**

| 官方 cell | 修改 | 理由 |
|---|---|---|
| cell-2 安裝 ydata-profiling | `!pip` 改成 `%pip install ydata-profiling` | `%pip` 會裝進目前 kernel 的環境；`!pip` 可能裝到別的 Python |
| cell-3 匯入套件 | `from ydata_profiling import ProfileReport` 包 `try / except`；只在這一行匯入時隱藏 DeprecationWarning | ydata-profiling 只用於 EDA 報告；安裝失敗時不讓同格的 sklearn 等匯入一起中斷；新版匯入時會印「已改名」提示，不影響功能 |
| cell-11 產生 EDA 報告 | `ProfileReport` 不可用時印訊息並略過 | 只少了 EDA.html，後面每一格照常執行 |
| cell-5 掛載 Google Drive | 包 `try / except`：沒有 `google.colab`（非 Colab）就略過；Colab 上拒絕或取消授權時只印訊息 | 「全部執行」不會停在掛載；Colab 正常授權時行為不變 |
| cell-9 讀取 CSV | 保留官方路徑；不存在時改讀環境變數 `TELEMARKETING_CSV`，預設為工作目錄（Colab 是 `/content`）下的 `TeleMarketing.csv`；都找不到時丟出說明清楚的錯誤 | 本機、或把 CSV 直接上傳到 `/content`，都能執行 |
| cell-13 資料清洗（TODO 1） | `month`、`day_of_week` 補 `"Not Applicable"` | 補完 TODO；缺值是結構性的（對照組沒被打電話） |
| cell-15 計數圖 `countplot` | 改用 `ax.containers` 配對長條 | seaborn 0.13 起把圖例代理也放進 `ax.patches`，原本前後半配對會錯位、百分比標錯（不報錯）；函式介面與圖不變 |
| cell-30 目標變數編碼（TODO 2） | `label_encoder.transform(...)` | 測試集只 transform、不重新 fit（防洩漏） |
| cell-44 `feature_selection_model` | 回傳 `list(selected_features)` | pandas 2.1 起不准用 dict 當欄位索引，cell-45／47／50 在 Colab 會 TypeError |
| cell-47 LR 特徵選擇（TODO 3） | `label='response'`、`model='LR'`、`k=10` | 補完 TODO，與上一格 RF 的寫法一致 |
| cell-58 最終 pipeline 超參數 | `max_depth` 第三值 9、`n_estimators` 第三值 300 | 依本次 CV 結果（見最終 pipeline 之後的解讀） |
| cell-38、48、52、60（`# TODO: Tech Focus Only`） | 第一行加一行註解 `# [A3] 技術重點（Tech Focus Only）的開放題…`；這四格原本就只有註解，程式不變 | 這四題屬技術重點（Tech Focus）；本作業選商業重點，依作業說明不處理，原題保留 |

另有三格執行所需的新增（都不是修改官方 cell）：產生 EDA 報告（官方 cell-11）後把 matplotlib 切回 inline（ydata-profiling 會讓之後所有圖都不顯示，而且不報錯）、TODO 1 之後檢查空值、分群前固定亂數種子。

**怎麼執行**
- **Colab**：把 `TeleMarketing.csv` 放在 My Drive 根目錄 → 執行階段 → 全部執行，並授權掛載 Drive（不想授權時，把 CSV 上傳到左側檔案區的 `/content` 也可以）。第一格會安裝 ydata-profiling；它要求 pandas < 3、matplotlib ≤ 3.10、scipy < 1.17、numpy < 2.4，若 Colab 內建版本較新，pip 會降版並提示重新啟動執行階段 —— 重新啟動後從第二格起全部執行即可（第一格可略過）。免費版只有 2 個 vCPU，最終 pipeline、t-SNE、巢狀交叉驗證與 bootstrap 會比本機慢數倍，整份預計 15 分鐘以上。
- **Colab 實測**：尚未在 Colab 實測；本檔存著的輸出是本機從頭執行的結果（見下一點）。
- **本機**：設定環境變數 `TELEMARKETING_CSV` 指向 CSV（或把 CSV 放在工作目錄）。
- **本檔存著的輸出**：在 2026-10 建置當下的本機環境從頭執行（約 {{run.minutes}} 分鐘）：Python {{meta.versions.python}}、numpy {{meta.versions.numpy}}、pandas {{meta.versions.pandas}}、scikit-learn {{meta.versions.scikit-learn}}、xgboost {{meta.versions.xgboost}}、seaborn {{meta.versions.seaborn}}、matplotlib {{meta.versions.matplotlib}}；Colab 當下的套件版本未核對，可能不同。本機執行時 pip 用安靜模式，所以第一格只印出一行提示。**我沒有在 Colab 上存輸出。** markdown 裡的數字都由最後一格程式印出的數字總表自動填入，與存著的輸出一致；在其他環境重跑，少數數字（KMeans 分群、LR 的 RFE）可能略有不同。

**結構**
- **Part A｜官方流程＋分析**：在 EDA、t-SNE、兩種特徵選擇、模型比較、最終 pipeline、客戶評分、分群的輸出之後，各插一格「解讀」（需要時先插一小格程式印出要引用的數字），並指出官方流程的方法問題與影響大小。
- **Part B｜商業評估**：接在官方最後一格之後，用撥號前模型逐條檢驗我在 A2 表 4 寫下的 10 條成功標準（業務①–⑤、ML①–⑤；業務②③⑤ 為上線硬門檻）與 A2 表 1 的商業目標，附 9 張圖（Fig 1–9）、總表與結論；最後是 B3（未來改進與新產品）、B4（放寬資格後能否沿用）的摘要，完整版在 PDF 報告。
'''

MD['part_a'] = r'''
<a id="part-a" name="part-a"></a>
# Part A｜官方流程與解讀

以下是官方 notebook 的完整流程（讀資料 → EDA → 前處理 → t-SNE → 特徵選擇 → 模型比較 → 最終 pipeline → 客戶評分 → 分群），官方 cell 依原順序執行。我在 8 個地方的輸出之後插入「解讀」：EDA、t-SNE、單變量特徵選擇、模型式特徵選擇、模型比較、最終 pipeline、客戶評分、分群。每格解讀依序寫觀察（本次執行的數字）、商業意義與注意事項；官方流程的方法問題也在對應位置量出影響大小。
'''

MD['eda'] = r'''
### 解讀：EDA（計數圖、箱形圖、分布圖與上方數字摘要）

**結論：撥號前看得到、又有區分力的訊號是前次行銷結果、時期與少數職業；duration 是洩漏，不是商業槓桿。**

- **基準與類別不平衡**：去重後全體成交 {{part_a.eda.base_conv_pct}}%（約 8 人中 1 人），所以後面都用 AUC 與轉換率，不用準確率。對照組 {{part_a.eda.rows.0}} 列、目標組 {{part_a.eda.rows.1}} 列，轉換率 {{part_a.eda.conv_pct.0}}% 對 {{part_a.eda.conv_pct.1}}%，幾乎一樣；A2 用原始資料是 {{part_b.a2_recomputed.pilot_control_conv_pct}}% 對 {{part_b.a2_recomputed.pilot_target_conv_pct}}%，差別來自去重刪掉的列幾乎全在對照組（Part B-0）。
- **前次行銷與時期**：poutcome = success 在去重後全體（含對照組，{{part_a.eda.poutcome_rows.success}} 列）成交 {{part_a.eda.poutcome_conv_pct.success}}%；分組看，目標組 {{part_a.eda.poutcome_success_by_group.1.conv_pct}}%、對照組 {{part_a.eda.poutcome_success_by_group.0.conv_pct}}%（A2 附錄 A 的 67.3%／62.7% 是原始全檔的目標組／對照組，母體不同）。無前次紀錄者只有 {{part_a.eda.poutcome_conv_pct.nonexistent}}%。目標組 3 月 {{part_a.eda.target_month_conv_pct.mar}}%（{{part_a.eda.target_month_rows.mar}} 通）、5 月只有 {{part_a.eda.target_month_conv_pct.may}}%（{{part_a.eda.target_month_rows.may}} 通）—— 通數最多的月份轉換率最低；手機 {{part_a.eda.target_contact_conv_pct.cellular}}% 對市話 {{part_a.eda.target_contact_conv_pct.telephone}}%。
- **客戶屬性**：學生 {{part_a.eda.cat_conv_pct.job.student}}%、退休 {{part_a.eda.cat_conv_pct.job.retired}}% 最高，藍領 {{part_a.eda.cat_conv_pct.job.blue-collar}}% 最低（下面 chi2 也選到 job_retired、job_student）；default = unknown {{part_a.eda.cat_conv_pct.default.unknown}}%，低於 no 的 {{part_a.eda.cat_conv_pct.default.no}}%（default = yes 只有 {{part_a.eda.cat_rows.default.yes}} 列）。教育程度以 {{part_a.eda.cat_best_n500.education}} 最高（{{part_a.eda.cat_conv_range_n500.education.1}}%）、{{part_a.eda.cat_worst_n500.education}} 最低（{{part_a.eda.cat_conv_range_n500.education.0}}%，只比 500 列以上的類別）；房貸（{{part_a.eda.cat_conv_range_n500.housing.0}}%–{{part_a.eda.cat_conv_range_n500.housing.1}}%）、信貸（{{part_a.eda.cat_conv_range_n500.loan.0}}%–{{part_a.eda.cat_conv_range_n500.loan.1}}%）與星期幾（{{part_a.eda.dow_conv_range.0}}%–{{part_a.eda.dow_conv_range.1}}%）差距小；年齡、cpi、cci 的平均在成交與否之間很接近（年齡 {{part_a.eda.mean_by_y.age.yes}} 對 {{part_a.eda.mean_by_y.age.no}} 歲）。
- **duration 是洩漏**：對照組 {{part_a.eda.duration0_pct.0}}% 的列 duration = 0，目標組 {{part_a.eda.target_duration0_rows}} 列 →「duration = 0」等於「沒被打」。通話要打完才知道長短；成交者平均 {{part_a.eda.mean_by_y.duration_target.yes}} 秒、未成交 {{part_a.eda.mean_by_y.duration_target.no}} 秒，比較可能是「願意辦卡才會講久」，不是「講久就會買」。
- **商業意義與注意**：月份差這麼大，任何「名單 vs 手機規則」都要同期比（Part B 業務②）。計數圖的百分比是每個類別內 no／yes 的比例，對照組與目標組混在一起；官方原本的標籤配對在 seaborn 0.13 會標錯，本檔已修正（見 A3 說明）。
'''

MD['tsne'] = r'''
### 解讀：t-SNE 二維圖（訓練集、測試集各一張）

**結論：二維結構主要把「有沒有被打」分開，對「會不會買」只多一點資訊。**

- **輸入**：{{part_a.tsne.n_inputs}} 欄 = 4 個標準化數值（含 duration）＋ 1 個冪變換 duration ＋ {{part_a.tsne.n_onehot}} 個獨熱欄，其中 5 個是組別旗標（campaign_0／1，以及 contact、month、day_of_week 的 Not Applicable）。冪變換（官方 cell-23、24 的分布圖）把訓練集 duration 的偏度從 {{part_a.tsne.duration_skew_train}} 降到 {{part_a.tsne.duration_tfm_skew_train}}，但對照組全是 0，變換後仍是一根獨立的柱。
- **量化**：在測試集的平面上，每個點最近的 10 個鄰居有 {{part_a.tsne.knn_same_group_pct}}% 與它同組（隨機 {{part_a.tsne.knn_same_group_random_pct}}%），但只有 {{part_a.tsne.knn_same_outcome_pct}}% 與它同樣成交／未成交（隨機 {{part_a.tsne.knn_same_outcome_random_pct}}%）。
- **解讀**：不先拿掉組別旗標與 duration，模型學到的大半是組別（呼應 EDA）。
- **注意**：t-SNE 不保留距離與密度，只能看鄰近關係，不能拿來挑客戶；訓練、測試是兩次獨立的嵌入，座標不能互相對照。測試集的冪變換是在測試集上重新擬合的（官方 cell-26）：它對 RF 測試 AUC 的影響約 {{part_a.model_compare.rf_auc_trainfit_minus_asrun|+.4f}}（見模型比較的解讀）；對這張 t-SNE 版面的影響沒有量化。
'''

MD['uni'] = r'''
### 解讀：單變量特徵選擇（f_classif、chi2）

**結論：兩種方法都把「前次行銷成功」排第一；它是撥號前最強的單一訊號，但也最容易把折扣送給本來就會買的人。**

- **觀察**：在 {{part_a.univariate.n_features_tested}} 個序數／獨熱欄中，兩種方法的前 10 名重疊 {{part_a.univariate.n_overlap}} 個；前幾名都是前次行銷紀錄（poutcome、previous）。chi2 另外選到 job_retired、job_student（EDA 中成交率最高的兩個職業）。f_classif 前 10 名有 {{part_a.univariate.f_classif_group_or_post_call}} 個是排程變數（month_oct），chi2 有 {{part_a.univariate.chi2_group_or_post_call}} 個（month_oct、month_mar）。
- **商業意義**：A2 表 2 註 1 已指出，前次成功者在對照組（沒被打）也有 62.7% 會買（原始全檔）—— 只依接受機率排名單，會把折扣送給本來就會買的人（業務④）。
- **注意**：這兩種方法只比序數／獨熱欄，duration 與數值欄沒有一起比；兩萬列下 p < 0.01 幾乎必然成立，「顯著」不等於「有商業價值」，也看不到欄位之間的交互作用。
'''

MD['mfs'] = r'''
### 解讀：模型式特徵選擇（RF 與 LR 的 RFE）

**結論：RF 的 RFE 以撥號前欄位為主，但含兩個 duration；LR 的 RFE 留下一組完全共線、與成交幾乎無關的組別旗標。對照實驗顯示，這些旗標是被 duration 的洩漏帶進來的：不是 C = 1000 造成的，也不是 LR 學到了「先排除對照組」。**

- **RF 的 RFE**：10 欄 = {{part_a.model_fs.tag_counts.RF_RFE.pre_call}} 欄撥號前可得、{{part_a.model_fs.tag_counts.RF_RFE.post_call}} 欄 duration（冪變換與標準化兩種版本）、{{part_a.model_fs.tag_counts.RF_RFE.scheduling}} 欄月份。熱圖上相關最高的一對是 {{part_a.model_fs.rf_max_pair_text}}：對照組的 duration 都是 0、月份都是 Not Applicable，兩欄都帶著「是不是對照組」的資訊；duration_tfm 與 duration_scl 是同一欄的兩種轉換（|r| = {{part_a.model_fs.rf_dur_pair_abs_r}}），RFE 也照樣兩個都留下。官方說熱圖是為了「確保特徵之間不存在高度相關」，但選完並沒有處理。
- **LR 的 RFE（TODO 3）**：{{part_a.model_fs.tag_counts.LR_RFE.group_flag}} 欄組別旗標、{{part_a.model_fs.tag_counts.LR_RFE.scheduling}} 欄月份、{{part_a.model_fs.tag_counts.LR_RFE.post_call}} 欄 duration，撥號前的客戶欄位只有 {{part_a.model_fs.tag_counts.LR_RFE.pre_call}} 欄（poutcome_success）。這些旗標與 response 的相關最大只有 {{part_a.model_fs.lr_flag_max_abs_corr_with_response}}（去重後兩組轉換率只差 0.3 個百分點），而且彼此完全共線：campaign_0 = 1 − campaign_1、campaign_int = campaign_1，contact 與 day_of_week 的 Not Applicable 就是 campaign_0。
- **為什麼會被留下（兩個對照實驗）**：用與 RFE 相同的設定在這 10 欄上重新擬合，係數絕對值最大的是 {{part_a.model_fs.lr_coef_top_text}}。對照組的 duration_tfm 全部是同一個值 {{part_a.model_fs.control_duration_tfm}}（目標組最低也有 {{part_a.model_fs.target_duration_tfm_min}}）：線性模型用 duration 描述「講越久越會買」時，會把對照組預測成幾乎不買，但對照組的實際轉換率和目標組差不多，旗標就被用來把對照組的預測拉回來。(1) 把 C 從 1000 改成 1，選出的 10 欄完全相同 —— 不是正則化太弱造成的；(2) 拿掉兩個 duration 欄（C 仍為 1000），組別旗標從 {{part_a.model_fs.tag_counts.LR_RFE.group_flag}} 個變成 {{part_a.model_fs.lr_ctl_nodur_flags}} 個，改選 {{part_a.model_fs.lr_ctl_nodur_tags.scheduling}} 個月份／管道欄與 {{part_a.model_fs.lr_ctl_nodur_tags.pre_call}} 個撥號前欄位。旗標彼此完全共線，所以留下哪一個不穩定，但「留下旗標」本身是 duration 洩漏的副產品。四種方法都選到的只有 poutcome_success。
- **商業意義**：上線版必須先拿掉 duration、campaign 與排程欄（撥號前不可用），Part B 的撥號前模型就是這樣建的。
- **注意**：LR 的 RFE 吃的是未標準化的序數碼與獨熱欄混合，數值收斂可能隨套件版本略有不同，所以這裡用標籤計數描述。
'''

MD['proba'] = r'''
### 解讀：模型比較（RF vs XGB）與上方診斷

**結論：官方「RF 優於 XGB」的比較不成立 —— 把 XGB 的 scale_pos_weight 改成實際比例後，XGB 的 CV 與測試 AUC 都比 RF 高。最終 pipeline 用 RF，是沿用官方流程，不是這次比較的結果。**

- **口徑**：官方 `modeling()`（cell-50、51）用 `.predict()` 的 0／1 標籤算 AUC，得到 RF {{part_a.model_compare.official_predict_auc.rf}}、XGB {{part_a.model_compare.official_predict_auc.gb}}；改用 `predict_proba`，測試 AUC 是 RF {{part_a.model_compare.proba_auc_test.rf}}、XGB {{part_a.model_compare.proba_auc_test.gb}}，訓練集 5 折 CV 是 {{part_a.model_compare.cv_auc_train.rf}} 對 {{part_a.model_compare.cv_auc_train.gb}}。
- **純診斷（只改 XGB 參數，官方物件不動）**：scale_pos_weight 由 87 改成去重訓練集的實際負／正比 {{part_a.xgb_diag.ratio}}，XGB 的 CV AUC {{part_a.xgb_diag.fixed_cv_auc}}（RF {{part_a.model_compare.cv_auc_train.rf}}，高 {{part_a.xgb_diag.xgb_minus_rf_cv|.4f}}，RF 折間標準差 {{part_a.model_compare.rf_cv_sd}}）、測試 AUC {{part_a.xgb_diag.fixed_test_auc}}（RF {{part_a.model_compare.proba_auc_test.rf}}）；預測「會買」的比例由 {{part_a.xgb_diag.official_share_yes_pct}}% 降到 {{part_a.xgb_diag.fixed_share_yes_pct}}%。
- **XGB 的 0.5 怎麼來的**：主因是 scale_pos_weight = 87（實際只有 {{part_a.xgb_diag.ratio}}）加上學習率 0.01 × 100 棵樹 —— 模型離不開加權後的先驗，{{part_a.xgb_diag.official_share_yes_pct}}% 的人都被預測成「會買」，0／1 標籤的 AUC 必然是 0.5。subsample、colsample_bytree 只有 0.1 不是主因：兩者改成 1.0 時仍有 {{part_a.xgb_diag.subcol1_share_yes_pct}}% 被預測成會買；學習率改 0.1 則降到 {{part_a.xgb_diag.lr01_share_yes_pct}}%。
- **用測試集選模**：官方 cell-53 依測試集下結論，同一份測試集之後又報最終 AUC，所以最終 AUC 只能當樂觀估計（A2 表 4 的 ML① 本來就定為「只當樂觀參考」）。A2 表 7 把 XGB 定為挑戰者、勝出幅度大於種子間波動才替換；Part B 的撥號前模型照這條規則只在訓練資料上重比（B-1），並對勝出的 XGB 做完整的十條評估（B-11）。
- **官方 cell-26 在測試集上重新擬合冪變換**：λ 訓練 {{part_a.model_compare.lambda_train}}、測試 {{part_a.model_compare.lambda_test}}。它影響測試集的 t-SNE（cell-36）與 cell-50／51 的測試 AUC：改用訓練集擬合的轉換器，RF 測試 AUC 為 {{part_a.model_compare.rf_auc_train_fitted_transform}}（比原值高 {{part_a.model_compare.rf_auc_trainfit_minus_asrun}}，可忽略）。兩種 RFE 只用訓練集、最終 pipeline 在 cell-56 重新切分，都不受影響。
'''

MD['final'] = r'''
### 解讀：最終 pipeline 與超參數補值的理由（GridSearchCV 18 組、訓練／測試 AUC）

**結論：補值取 max_depth 9、n_estimators 300（CV 最高）；測試 AUC {{part_a.final_pipeline.auc_test}} 達 A2 ML① 門檻，但它回答的是「電話打完後，猜他買了沒」，不能當上線依據。**

- **補值理由（依本次 CV）**：18 組中 CV 最高的是 criterion = {{part_a.final_pipeline.best_params.criterion}}、max_depth = {{part_a.final_pipeline.best_params.max_depth}}、n_estimators = {{part_a.final_pipeline.best_params.n_estimators}}（CV {{part_a.final_pipeline.best_cv_auc}}）。各深度最佳 CV：3 → {{part_a.final_pipeline.cv_auc_by_depth.3}}、5 → {{part_a.final_pipeline.cv_auc_by_depth.5}}、9 → {{part_a.final_pipeline.cv_auc_by_depth.9}}；最佳設定下樹數 100／200／300 為 {{part_a.final_pipeline.cv_auc_by_n_estimators_at_best.100}}／{{part_a.final_pipeline.cv_auc_by_n_estimators_at_best.200}}／{{part_a.final_pipeline.cv_auc_by_n_estimators_at_best.300}}，300 最高但差距已小於 0.001。9 在網格邊界，所以另掃深度 7／9／11（只是診斷，官方網格沒改）：CV {{part_a.final_pipeline.depth_sweep.0.cv_auc}}／{{part_a.final_pipeline.depth_sweep.1.cv_auc}}／{{part_a.final_pipeline.depth_sweep.2.cv_auc}}，訓練 − 測試差 {{part_a.final_pipeline.depth_sweep.0.train_minus_test|.4f}}／{{part_a.final_pipeline.depth_sweep.1.train_minus_test|.4f}}／{{part_a.final_pipeline.depth_sweep.2.train_minus_test|.4f}}：9 是 CV 峰值，11 的差超過 A2 的 0.05。
- **結果**：訓練 AUC {{part_a.final_pipeline.auc_train}}、測試 {{part_a.final_pipeline.auc_test}}，差 {{part_a.final_pipeline.gap_train_minus_test}}（A2 表 4 引用的 0.843／0.845 是官方檔原本存著的 8 組網格輸出）。只看測試集目標組 AUC = {{part_a.final_pipeline.auc_test_target_only}}、只看對照組 = {{part_a.final_pipeline.auc_test_control_only}}：在目標組，模型可以用「講了多久」把成交者挑出來。duration 進了兩次（ColumnTransformer 同時放進冪變換 `dur` 與標準化 `scaler`），合計佔重要度 {{part_a.final_pipeline.duration_importance_share}}；RFE 沒選到 campaign、contact、month、day_of_week，模型分辨「打／沒打」只靠 duration = 0。
- **方法偏誤與影響大小**：(1) RFE 先用整個訓練集擬合，才進 GridSearchCV 的 5 折，驗證折的標籤參與了特徵篩選 → CV 偏樂觀。上方 [2b] 量了大小：最佳設定在同樣 5 折上，RFE 只擬合一次的 CV AUC {{part_a.final_pipeline.rfe_bias.nonnested_cv_auc}}、每折重做 RFE（巢狀）{{part_a.final_pipeline.rfe_bias.nested_cv_auc}}，差 {{part_a.final_pipeline.rfe_bias.nonnested_minus_nested|+.4f}}（逐折 {{part_a.final_pipeline.rfe_bias.fold_diff_min|+.4f}} 到 {{part_a.final_pipeline.rfe_bias.fold_diff_max|+.4f}}）—— 偏誤約千分之一，可忽略。所以官方 CV（{{part_a.final_pipeline.best_cv_auc}}）比測試（{{part_a.final_pipeline.auc_test}}）低 {{part_a.final_pipeline.cv_minus_test|abs.4f}}，是切分的抽樣差異，不是偏誤方向相反。這項比較用前處理輸出的密集矩陣重算（官方是稀疏矩陣，樹的分割細節略有不同，密集版 RFE 選出的 10 欄也與官方不完全相同），只看兩個密集版本的差；前處理本身（不用標籤）沿用官方已擬合的版本。(2) 切分沒有 stratify：成交比例訓練 {{part_a.final_pipeline.pos_share_train_pct}}% 對測試 {{part_a.final_pipeline.pos_share_test_pct}}%，差 {{part_a.final_pipeline.pos_share_diff_pp}} 個百分點，影響很小。(3) class_weight = 'balanced'：測試集平均預測 {{part_a.final_pipeline.mean_pred_prob_test}}，實際成交比例只有 {{part_a.final_pipeline.actual_yes_share_test}}，分數只能排序、不能當機率。
- **上線風險**：官方前處理的 `OrdinalEncoder()` 用預設 `handle_unknown='error'`，評分時遇到訓練沒見過的類別值會直接報錯 —— 上線前要先做資料驗證（A2 表 10 的 schema 檢查）。
- **商業意義**：達到 A2 的 ML①（≥ 0.80，只當樂觀參考），但不能當上線依據；上線版要用撥號前欄位重建（Part B）。
'''

MD['score'] = r'''
### 解讀：客戶評分（duration 分桶、11 種情境與分數排序）

**結論：官方分數同時獎勵「不打也會買」與「打了才會買」，通話成本又按桶號而不是秒數計，只能當排序參考，不能當期望收益。**

- **桶與成本**：duration 冪變換後等寬切 11 桶（官方 cell-62），各桶平均 {{part_a.scoring.bucket_mean_seconds.1|.0f}} 秒到 {{part_a.scoring.bucket_mean_seconds.10|,.0f}} 秒。官方分數（cell-64）用「單位」計：不打也買 200、打了才買 100 − 2k。要和通話成本比，得先把單位換成 A\$（這是假設的換算）：200 單位對應 A2 的收益 2D，所以 1 單位 = D／100；取 A2 附錄 A 的示例 D = A\$36，第 k 桶的官方通話成本 2k 單位約 A\$0.72k。依 A2 時薪 A\$50 算的實際通話成本：第 1 桶約 A\${{part_a.scoring.bucket_call_cost_aud.1}}（官方 A\${{part_a.scoring.official_cost_aud_at_D36.1}}）、第 7 桶約 A\${{part_a.scoring.bucket_call_cost_aud.7}}（官方 A\${{part_a.scoring.official_cost_aud_at_D36.7}}）、第 10 桶約 A\${{part_a.scoring.bucket_call_cost_aud.10}}（官方 A\${{part_a.scoring.official_cost_aud_at_D36.10}}，低估約 {{part_a.scoring.bucket10_understate_x}} 倍）。從第 {{part_a.scoring.crossover_bucket}} 桶起實際成本高於官方：官方分數高估短通話、低估長通話的成本。
- **排名前段是誰**（200 人隨機樣本，目標組 {{part_a.scoring.sample_target_n}}、對照組 {{part_a.scoring.sample_control_n}} 人）：分數前 10 名中目標組 {{part_a.scoring.top10_target_n}} 人、對照組 {{part_a.scoring.top10_control_n}} 人，實際成交 {{part_a.scoring.top10_yes}} 人，前次行銷成功 {{part_a.scoring.top10_prev_success}} 人；前 40 名成交率 {{part_a.scoring.top40_conv_pct}}%（{{part_a.scoring.top40_yes}}／40），全部 200 人 {{part_a.scoring.sample_conv_pct}}%（{{part_a.scoring.sample_yes}}／200）—— 樣本很小，只能當方向。
- **cell-64 沒有切換 campaign，影響大小為 0**：最終模型的 10 個 RFE 欄位沒有 campaign、contact、month、day_of_week。把目標組客戶的 pr0 改用對照組樣貌重算，平均 pr0 {{part_a.scoring.target_mean_pr0_as_run}} → {{part_a.scoring.target_mean_pr0_control_profile}}，排名的 Spearman 相關 {{part_a.scoring.spearman_official_vs_switched}}、前 20 名 {{part_a.scoring.top20_overlap}}／20 相同。但評分本身是外推：訓練資料中「campaign = 1 且 duration = 0」有 {{part_a.scoring.train_rows_campaign1_duration0}} 列、「campaign = 0 且 duration > 0」有 {{part_a.scoring.train_rows_campaign0_duration_pos}} 列，都是模型沒看過的組合；duration 也不是行員能事先決定的槓桿。
- **分數組成**：「200 × pr0」（不打也會買）佔總分的 {{part_a.scoring.pr0_term_share_pct}}%；pr 來自 class_weight = 'balanced' 的模型，未校準（平均預測 {{part_a.final_pipeline.mean_pred_prob_test}} 對實際 {{part_a.final_pipeline.actual_yes_share_test}}），「收益 × 機率」的期望值解讀不成立。
- **商業意義**：A2 表 4 註指出，2:1 下每人代價最高的錯誤是把折扣送給本來就會買的人；A2 的兩步走（先排接受機率、12 週後改排增量）就是為此。Part B 改用撥號前模型，並用對照組量增量。
'''

MD['cluster'] = r'''
### 解讀：分群（手肘圖、8 群剖面與各群的圖）

**結論：8 群主要被「有沒有打、講多久」與時期切開；成交率最高的一群是「講很久的目標組客戶」，不是能在撥號前鎖定的客群。**

- **手肘圖**（官方 cell-67）：inertia 整體隨 k 下降（k = 4／5／6：{{clustering.elbow_inertia.4|,}}／{{clustering.elbow_inertia.5|,}}／{{clustering.elbow_inertia.6|,}}；k = 9／10：{{clustering.elbow_inertia.9|,}}／{{clustering.elbow_inertia.10|,}}），有 {{clustering.elbow_n_increase}} 處 k 加 1 時反而略升（KMeans 起始點不同），沒有單一明顯拐點；k = 8 是官方指定，不是資料選出來的。手肘圖只用 RFE 輸出 10 欄中的 {{clustering.elbow_n_columns}} 欄（沒有兩個 duration 欄），最終分群（cell-68）卻用全部 10 欄，兩者不完全對應。
- **成交率排名（不引用群號）**：第 1 名 {{clustering.profile.rank1.rows|,.0f}} 人、成交 {{clustering.profile.rank1.conv_pct}}%，目標組佔 {{clustering.profile.rank1.target_share_pct|.0f}}%，平均通話 {{clustering.profile.rank1.mean_duration|,.0f}} 秒；第 2 名 {{clustering.profile.rank2.rows|,.0f}} 人、{{clustering.profile.rank2.conv_pct}}%。其餘 {{clustering.n_rest}} 群只有 {{clustering.rest_conv_min}}%–{{clustering.rest_conv_max}}%（全體 {{clustering.overall_conv_pct}}%）；8 群中 {{clustering.n_all_target}} 群全是目標組、{{clustering.n_mostly_control}} 群的目標組不到 10%。
- **小提琴圖（cci、cpi、年齡依成交與否分開）**：第 2 名的平均 cci {{clustering.profile.rank2.mean_cci}}、cpi {{clustering.profile.rank2.mean_cpi}}（全體 {{clustering.overall.mean_cci}}、{{clustering.overall.mean_cpi}}），是被時期切出來的一群；平均年齡 {{clustering.profile.rank2.mean_age}} 歲（全體 {{clustering.overall.mean_age}}）。
- **計數圖（marital、default、housing、poutcome）**：第 2 名的前次行銷成功比例 {{clustering.profile.rank2.prev_success_pct}}%（全體 {{clustering.overall.prev_success_pct}}%），default = unknown 只有 {{clustering.profile.rank2.default_unknown_pct}}%（全體 {{clustering.overall.default_unknown_pct}}%）；第 1 名的成交者中前次成功只佔 {{clustering.profile.rank1.yes_prev_success_pct}}%（全體成交者 {{clustering.overall.yes_prev_success_pct}}%）—— 它的高成交率來自講得久，不是前次紀錄。第 3、7 名年紀較大（平均 {{clustering.profile.rank3.mean_age}}、{{clustering.profile.rank7.mean_age}} 歲），已婚 {{clustering.profile.rank3.married_pct}}%、{{clustering.profile.rank7.married_pct}}%（全體 {{clustering.overall.married_pct}}%），成交率偏低。housing 的比例各群差距不大，對區分成交幫助小。
- **商業意義與注意**：撥號前能用的客群訊號是時期與前次行銷成功，可以做成不同話術或聯絡時機的實驗，但應先拿掉 duration 與組別欄位重新分群。KMeans 沒有 random_state；本檔分群前固定了 numpy 種子，同一環境可重現，但換套件版本時群的切法可能改變，所以只用排名描述，數字為本次儲存的結果。
'''

MD['b_head'] = r'''
<a id="part-b" name="part-b"></a>
# Part B｜商業評估：對照 A2 成功標準

這一部分接在官方最後一格之後，官方流程完全不動。問題只有一個：**這個模型能不能照 A2 的計畫往下走？**

> **先給答案**
> 1. 模型比隨機外撥好：與手機規則同樣通數時，名單轉換率 {{part_b.b2.ml_conv_pct}}%；全體隨機外撥 {{part_b.b2.random_conv_pct}}%，依手機規則的月份組成隨機外撥 {{part_b.b2.random_month_matched_conv_pct}}%。
> 2. 但和現行手機規則（{{part_b.b2.mobile_conv_pct}}%）同月、同通數比，只高 {{part_b.b2.diff_pp|.2f}} 個百分點，95% 區間含 0 —— 看不出比手機規則好。排序力大多來自認出外撥時期：同一 (cpi, cci) 時期內 AUC 只有 {{part_b.ml.ml2_within_period_auc}}（圖 9）。
> 3. 三條上線硬門檻（業務②③⑤）沒有一條能離線判定為通過；十條中只有 ML①、ML③ 達標。
> 4. 依 A2 表 7 勝出的 XGB，十條判定與 RF 完全相同。
> 5. 錢的缺口主要在優惠設計，不在名單（示算）：名單相對手機規則每輪只多省 A\${{part_b.goals.saving_ml_vs_mobile_aud|,}} 通話費，即使達到 A2 目標也最多多省 A\${{part_b.goals.saving_target_vs_mobile_aud|,}}；每張折扣只要高於約 A\${{part_b.goals.D_spill_exceeds_target_vs_mobile_saving_aud.raw|.2f}}（原始）／A\${{part_b.goals.D_spill_exceeds_target_vs_mobile_saving_aud.dedup|.2f}}（去重），每輪白送給本來就會買者的折扣就超過這個數，名單也沒有讓這筆變少。以示例折扣 D = A\$36 算，這筆約 A\${{part_b.goals.spillover_discount_per_round_D36_aud.raw|,}}–{{part_b.goals.spillover_discount_per_round_D36_aud.dedup|,}}（B-13、圖 8）。
> 6. 建議：依 A2 表 9 階段 0，**不進影子模式**；先補撥號前的客戶特徵與有日期、客戶編號的資料，再用新的時間段重測。

**名詞**（Part B 反覆用到）
- **時期**：一組 (cpi, cci) 值。這兩個指標每月公布一次，同一組值大致是同一個年月；資料跨年，所以一個「月份」裡混有 2–3 個時期。
- **同月配對名單**：每個月打的通數與手機規則相同、取該月分數最高的人 —— 外撥日不能換月份，這是實際做得到的名單（業務①②與混淆矩陣用它）。**單一門檻名單**：全體分數 ≥ 門檻 t 的人；對照組沒有月份，業務③④⑤ 只能用它。
- **percentile 區間**：bootstrap 重抽結果的 2.5%–97.5% 分位，是評估計畫訂的判準區間。**basic 區間**：偏差校正版（2 × 點估計 − 上、下界），只當檢查（附錄 A）。
- **本來就會買**：不打電話也會買的人；用「分數同樣達門檻、但沒被打的對照組」的轉換率估計（業務④）。

**做法**
1. **資料**：notebook 去重後的 `campaign_data`，切分與官方最終流程（cell-56）相同（test_size = 0.4、random_state = 123；訓練 21,262 列、測試 14,176 列）。A2 正文用的是原始 41,188 列，兩個口徑在 B-0 並列。
2. **模型**：只用 A2 表 5 標「可」的 11 欄、只用訓練集的目標組（campaign = '1'）訓練，前處理包在 Pipeline 內。RF 是評估計畫事先指定的主模型，超參數用一條只看訓練資料、A3 自訂的規則選（in-sample AUC − CV AUC ≤ 0.05 的設定中取 CV 最高者，代理 A2 的 ML③）。XGBoost 依 A2 表 7 當挑戰者，同樣只在訓練資料上比（B-1）；它勝出，所以 B-11 對它做完整的十條評估。
3. **測試集**：模型與超參數在評分前固定，之後不回頭改。業務②的判準（B = 1,000、種子 123、95% percentile 區間下限 > 0）是計畫原本訂的；B = 5,000、basic 區間與換種子是看過第一次結果之後才加的檢查，不改判準（附錄 A）。設計階段我曾用同一份測試集預跑過，所以測試數字仍屬樂觀估計；乾淨的做法是保留一段較晚的時間當全新的驗證集（資料沒有日期，做不到；A2 已請求補日期）。
4. **同期**：A2 表 9 定義為「同一段期間、同樣通數」。主結果以同月份操作化，另以同時期做穩健性檢查。增量只和對照組中分數同樣達門檻的客戶比（A2 表 4 ③）。
5. **假設**（沿用 A2 表 1 下方假設框與附錄 A）：時薪 A\$50、只計通話時間、成交 496.8 秒／未成交 220.7 秒；收益：折扣 = 2:1。

**判定用語**（每個只有一種意思）：**達標**＝達到 A2 門檻；**未達**＝證據落在門檻錯的一邊（點估計在錯的一邊，或整個區間都在錯的一邊）；**未證實**＝點估計方向對，但 95% 區間跨過門檻，不能說已達到；**示算**＝只能在假設下試算；**不可離線驗**＝試點資料無法檢驗。另一欄「是否達 A2 門檻」只填 是／否／離線無法判定。
'''

MD['b_summary'] = r'''
<a id="part-b-summary" name="part-b-summary"></a>
## Part B 十條成功標準一覽（A2 表 4；業務②③⑤ 是上線硬門檻）

| A2 表 4 標準 | A2 門檻 | A3 結果（RF 主模型） | 判定 | 是否達 A2 門檻 | XGB（表 7 勝出者） |
|---|---|---|---|---|---|
| 業務① 每筆成交通話成本 | ≤ A\$20.87 | 同月配對名單 A\${{part_b.b1.ml_cost_formula}}（手機規則 A\${{part_b.b1.mobile_cost_formula}}） | **{{part_b.kpi_judgement.b1}}** | {{part_b.kpi_meets_a2.b1}} | {{part_b.xgb_eval.judgement.b1}} |
| 業務② 名單轉換率（硬門檻） | 高於同期手機規則組 | 同月 {{part_b.b2.diff_pp|+.2f}} pp，95% 區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}]；同時期 {{part_b.b2.period.diff_pp|+.2f}} pp | **{{part_b.kpi_judgement.b2}}** | {{part_b.kpi_meets_a2.b2}} | {{part_b.xgb_eval.judgement.b2}} |
| 業務③ 增量成交（硬門檻） | 為正（同門檻對照組） | 去重 {{part_b.b3b4.dedup.uplift_pp|+.2f}}、原始 {{part_b.b3b4.raw.uplift_pp|+.2f}} pp；分時期 {{part_b.b3b4.dedup.period_stratified_uplift_pp|+.2f}}／{{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}} pp（區間都含 0） | **{{part_b.kpi_judgement.b3}}** | {{part_b.kpi_meets_a2.b3}} | {{part_b.xgb_eval.judgement.b3}} |
| 業務④ 本來就會買的比例 | A/B 列報；兩平參考 50% | 去重 {{part_b.b3b4.dedup.would_buy_share_pct}}%、原始 {{part_b.b3b4.raw.would_buy_share_pct}}%（區間都高於 50%） | **{{part_b.kpi_judgement.b4}}** | {{part_b.kpi_meets_a2.b4}} | {{part_b.xgb_eval.judgement.b4}} |
| 業務⑤ 式 1 淨值（硬門檻） | 不低於同期手機規則組 | 2:1 示算為負：{{part_b.b5.dedup_ml_list.net_D_per_call_excl_call_cost|+.3f}}／{{part_b.b5.raw_ml_list.net_D_per_call_excl_call_cost|+.3f}} D 每通 | **{{part_b.kpi_judgement.b5}}** | {{part_b.kpi_meets_a2.b5}} | {{part_b.xgb_eval.judgement.b5}} |
| ML① 概念驗證 AUC | ≥ 0.80（樂觀參考） | {{part_b.ml.ml1_poc_test_auc}} | **{{part_b.kpi_judgement.ml1}}** | {{part_b.kpi_meets_a2.ml1}} | {{part_b.xgb_eval.judgement.ml1}} |
| ML② 撥號前 AUC | ≥ 0.75，且 ② 通過 | {{part_b.ml.ml2_test_auc}}（同一時期內 {{part_b.ml.ml2_within_period_auc}}）；② 未通過 | **{{part_b.kpi_judgement.ml2}}** | {{part_b.kpi_meets_a2.ml2}} | {{part_b.xgb_eval.judgement.ml2}} |
| ML③ 過擬合 | 訓練 − 測試 ≤ 0.05 | 概念驗證 {{part_b.ml.ml1_poc_gap}}、撥號前 {{part_b.ml.ml3_precall_gap}} | **{{part_b.kpi_judgement.ml3}}** | {{part_b.kpi_meets_a2.ml3}} | {{part_b.xgb_eval.judgement.ml3}} |
| ML④ 分群一致性 | 各群 AUC 差 ≤ 0.05 | 年齡 {{part_b.ml4.gaps.age_band.max_minus_min|.3f}}、婚姻 {{part_b.ml4.gaps.marital.max_minus_min|.3f}}、月份 {{part_b.ml4.gaps.month.max_minus_min|.3f}} | **{{part_b.kpi_judgement.ml4}}** | {{part_b.kpi_meets_a2.ml4}} | {{part_b.xgb_eval.judgement.ml4}} |
| ML⑤ 增量排序模型 | 名單內平均增量 > 全體 | 未建（12 週後才有資料） | **{{part_b.kpi_judgement.ml5}}** | {{part_b.kpi_meets_a2.ml5}} | {{part_b.xgb_eval.judgement.ml5}} |

ML①–⑤ 是 A2 表 4 五個 ML 列的依序編號。業務①② 用同月配對名單，業務③④⑤ 用單一門檻名單。每條的 A2 草稿行號、完整區間與說明在 B-12 的總表。
'''

MD['b0'] = r'''
### B-0 解讀：資料口徑（A2 原始 vs A3 去重）

**結論：A2 的基準在這裡全部重算吻合；去重幾乎只刪對照組的列，所以凡是用到對照組的 ③④⑤ 兩個口徑都報。**

- **觀察**：notebook 的 `drop_duplicates()` 刪掉 {{part_b.a2_recomputed.removed_rows}} 列，其中對照組 {{part_b.a2_recomputed.removed_control}} 列、目標組只有 {{part_b.a2_recomputed.removed_target}} 列。對照組轉換率因此從 {{part_b.reconcile.0.control_conv_pct}}% 升到 {{part_b.reconcile.1.control_conv_pct}}%，「目標組 − 對照組」從 A2 的 {{part_b.reconcile.0.diff_pp}} 個百分點縮成 {{part_b.reconcile.1.diff_pp}}；測試集只剩 {{part_b.reconcile.3.diff_pp}}。手機規則幾乎不受影響（原始 {{part_b.a2_recomputed.mobile_raw_conv_pct}}%、測試集 {{part_b.reconcile.3.mobile_conv_pct}}%）。
- **兩組組成**：前次行銷成功者的比例，原始全檔目標組 {{part_b.a2_recomputed.prev_success_share_pct.raw_target|.2f}}% 對對照組 {{part_b.a2_recomputed.prev_success_share_pct.raw_control|.2f}}%，去重後 {{part_b.a2_recomputed.prev_success_share_pct.dedup_target|.2f}}% 對 {{part_b.a2_recomputed.prev_success_share_pct.dedup_control|.2f}}% —— 去重讓兩組較接近，但仍不同；兩組不是隨機分派。
- **A2 基準重算**：每筆成交通話成本 A\${{part_b.a2_recomputed.cost_per_conv_pilot}}、轉換率 18% 時 A\${{part_b.a2_recomputed.cost_per_conv_target_18pct}}；增量約 {{part_b.a2_recomputed.pilot_incremental_sales|.0f}} 人；成交者中本來就會買 {{part_b.a2_recomputed.pilot_would_buy_share_pct}}%；成交／未成交平均通話 {{part_b.a2_recomputed.sec_yes}}／{{part_b.a2_recomputed.sec_no}} 秒（每通約 A\${{part_b.a2_recomputed.call_cost_yes|.2f}}／A\${{part_b.a2_recomputed.call_cost_no}}）。
- **商業意義**：沒有客戶編號，無法判斷那 {{part_b.a2_recomputed.removed_control}} 列是真的重複，還是屬性剛好相同的不同客戶（對照組少了 contact、month、day_of_week、duration 四欄，本來就容易「相同」）；A2 附錄 A 把去重版定為極端情境。只用目標組的指標（①②、ML①–④）兩個口徑幾乎一樣，用主口徑即可。
- **注意**：A2 的 13.04%、16.6%、A\$27.35 是原始全檔數字；以下 A3 的數字是去重後測試集（目標組 7,094 人），兩者可以並列，不可直接相減。
'''

MD['b1'] = r'''
### B-1 解讀：撥號前模型的訓練、選模與 A2 表 7 的挑戰者規則（只用訓練資料）

**結論：RF 選定深度 {{part_b.models.main_params.max_depth}}、葉節點至少 {{part_b.models.main_params.min_samples_leaf}} 人（CV {{part_b.models.main_selected.cv_auc}}）。依 A2 表 7 的規則，XGBoost 勝出：5 個隨機種子平均高 {{part_b.models.table7_rule.margin_mean|.4f}}，遠大於 RF 在種子之間的波動（最大差距 {{part_b.models.table7_rule.rf_seed_range|.4f}}），而且每個種子都較高 → XGB 取代 RF，成為往下一階段的候選模型。B-2 起每一條以事先指定的 RF 呈現、XGB 並列，B-11 對 XGB 做完整的十條評估。**

- **訓練資料**：訓練集目標組 {{part_b.models.train_target_rows}} 人、成交 {{part_b.models.train_target_conv_pct}}%。
- **選模（A3 代理規則）**：6 組 RF 設定中，深度 {{part_b.models.main_rejected_by_gap.0.max_depth}}、葉節點 {{part_b.models.main_rejected_by_gap.0.min_samples_leaf}} 的「in-sample − CV」差 {{part_b.models.main_rejected_by_gap.0.train_minus_cv}} 超過 0.05 而被排除；選中者的差為 {{part_b.models.main_selected.train_minus_cv}}，它同時也是 CV 最高的設定。這條規則是 A3 自訂的訓練端代理，不能保證 ML③，ML③ 仍要看 B-2 的測試結果。
- **基準與挑戰者**：LR 基準 CV {{part_b.models.lr_cv_auc}}，比 RF 低 {{part_b.models.rf_minus_lr_cv}}。XGBoost（scale_pos_weight = 實際負／正比 {{part_b.models.xgb_scale_pos_weight}}；4 組設定中最佳為 learning_rate {{part_b.models.xgb_params.learning_rate}}、max_depth {{part_b.models.xgb_params.max_depth}}）在選模用的同一批 5 折上 CV {{part_b.models.xgb_cv_auc}}，{{part_b.models.xgb_folds_better}} 折全部較高（逐折差 {{part_b.models.xgb_minus_rf_fold_min|+.4f}} 到 {{part_b.models.xgb_minus_rf_fold_max|+.4f}}）。＋contact 版 RF 的 CV {{part_b.models.contact_selected.cv_auc}}。
- **A2 表 7 的替換規則（照字面執行）**：表 7 寫「與隨機森林用同一批驗證折、同一指標重比；勝出幅度大於不同隨機種子間的波動才替換」。用種子 123–127（每個種子同時改變 5 折的切法與模型的隨機種子）重比兩個選定設定：XGB − RF 的 CV AUC 差介於 {{part_b.models.table7_rule.margin_min|+.4f}} 到 {{part_b.models.table7_rule.margin_max|+.4f}}；RF 自己在 5 個種子間的 CV AUC 最大差距只有 {{part_b.models.table7_rule.rf_seed_range|.4f}}（標準差 {{part_b.models.table7_rule.rf_seed_sd|.4f}}）→ 依表 7 應替換。
- **為什麼仍以 RF 為主呈現**：RF 是 A3 評估計畫在比較挑戰者之前就指定的主模型，也是 Part A 官方流程的模型；看到挑戰者的結果之後才換主角，容易變成挑結果。所以兩個模型都完整評估：十條判定完全相同（B-11），「停在階段 0」不受模型選擇影響。日後補資料重建、通過階段 0 時，依表 7 應以 XGB 進入影子模式。
- **注意**：葉節點至少 20 位客戶，分數不會因個別客戶而跳動；class_weight = 'balanced' 與 scale_pos_weight 的分數只用來排序，不能當機率。年齡、婚姻能否用於評分要法遵確認（A2 表 9 階段 0），拿掉它們重訓的代價在 B-10。撥號前模型的獨熱編碼設 `handle_unknown='ignore'`：評分時遇到訓練沒見過的類別會靜默編成全 0、照常評分（官方 pipeline 的 `OrdinalEncoder` 則會中斷），上線前一樣要先做 schema 檢查（A2 表 10）。
'''

MD['b2'] = r'''
### B-2 解讀：ML① ② ③（AUC 與過擬合）

**結論：兩個 AUC 門檻都過了，但撥號前模型在同一 (cpi, cci) 時期內的排序能力只有 {{part_b.ml.ml2_within_period_auc}}，接近亂猜 —— AUC {{part_b.ml.ml2_test_auc}} 大半來自認出時期。**

- **ML① 概念驗證**（≥ 0.80，只當樂觀參考）：測試 AUC {{part_b.ml.ml1_poc_test_auc}}（訓練 {{part_b.ml.ml1_poc_train_auc}}）→ 達標。在同一批 {{part_b.ml.test_target_rows}} 位測試集目標組客戶上，它的 AUC 是 {{part_b.ml.ml1_poc_target_only_auc}}，撥號前模型 {{part_b.ml.ml2_test_auc}}，差 {{part_b.ml.ml1_target_only_minus_ml2}}。受控比較（同樣的撥號前 RF、只多加 duration）AUC 為 {{part_b.ml.ml2_with_duration_auc}}：約 {{part_b.ml.duration_gain_controlled}}（受控比較）到 {{part_b.ml.ml1_target_only_minus_ml2}}（與概念驗證比較）的差距主要來自 duration（事後資訊），其餘約 {{part_b.ml.poc_minus_controlled_other}} 來自訓練母體、特徵與超參數不同。
- **ML② 撥號前**（≥ 0.75，且 ② 勝過同期手機規則組）：測試集目標組 AUC {{part_b.ml.ml2_test_auc}}、CV {{part_b.ml.ml2_cv_auc}}，兩者一致 → AUC 這半條達標，但 ② 未通過（B-3），所以 ML② 整條是未證實；LR 基準 {{part_b.ml.ml2_lr_test_auc}} 未達 0.75；XGB {{part_b.ml.xgb_test_auc}}（訓練 − 測試 {{part_b.ml.xgb_gap}}）。
- **時期**：月內 AUC {{part_b.ml.ml2_within_month_auc}}；但資料跨年，每個月份內有 {{part_b.ml.periods_per_month_min}}–{{part_b.ml.periods_per_month_max}} 個時期（測試集目標組共 {{part_b.ml.n_periods_test_target}} 個），cpi、cci 只在同一時期內才是常數，所以月內 AUC 仍含跨年的時期訊號。同一時期內的加權 AUC 只有 {{part_b.ml.ml2_within_period_auc}}（比全體低 {{part_b.ml.ml2_minus_within_period}}；XGB {{part_b.ml.xgb_within_period_auc}}）。外撥日的候選人都在同一時期，這才是名單排序實際能用的能力。
- **ML③ 過擬合**（≤ 0.05）：概念驗證 {{part_b.ml.ml1_poc_gap}}、撥號前 {{part_b.ml.ml3_precall_gap}} → 達標；撥號前的 CV − 測試只有 {{part_b.ml.ml3_precall_cv_minus_test}}。
- **商業意義**：A2 階段 1 的影子模式只有 3 週，大約落在一個時期內，在那裡量到的 AUC 會比較接近時期內的數字，很可能低於 0.75；AUC 過門檻也還不代表名單比手機規則好（B-3）。
- **圖 9**（下一格）把概念驗證、撥號前、月內、時期內四個 AUC 畫在一起。
'''

MD['b3'] = r'''
### B-3 解讀：業務② 名單轉換率 vs 同期手機規則（上線硬門檻）

**結論：與手機規則同通數、同月份比，RF 名單只高 {{part_b.b2.diff_pp|.2f}} 個百分點，95% 區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}] 含 0 → 未證實；改成同一時期比，點估計為 {{part_b.b2.period.diff_pp|+.2f}} 個百分點，95% 區間 [{{part_b.b2.period.ci_low_pp|+.2f}}, {{part_b.b2.period.ci_high_pp|+.2f}}] 同樣含 0。XGB 名單高 {{part_b.b2.xgb.diff_pp|.2f}} 個百分點，但區間下限是 {{part_b.b2.xgb.ci_low_pp|+.2f}}，沒有大於 0，同樣未通過。業務② 離線不通過。**

- **同月（主結果，計畫判準）**：手機 {{part_b.b2.K_mobile_calls}} 通、轉換率 {{part_b.b2.mobile_conv_pct}}%；每月取同樣通數、分數最高的人，RF 名單 {{part_b.b2.ml_conv_pct}}%，差 {{part_b.b2.diff_pp|+.2f}} pp；各月內 bootstrap（B = 1,000、種子 123）的 95% percentile 區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}]。逐月看名單勝 {{part_b.b2.months_ml_better}} 個月、輸 {{part_b.b2.months_ml_worse}} 個月。B = 5,000、basic 區間與另外 10 個種子都不改變判定（附錄 A）。
- **同時期（穩健性）**：每個 (cpi, cci) 時期取同樣通數，RF 名單 {{part_b.b2.period.ml_conv_pct}}%，差 {{part_b.b2.period.diff_pp|+.2f}} pp，95% 區間 [{{part_b.b2.period.ci_low_pp|+.2f}}, {{part_b.b2.period.ci_high_pp|+.2f}}]。
- **手機規則的優勢從哪來**：隨機外撥 {{part_b.b2.random_conv_pct}}% → 依手機規則的月份組成隨機抽 {{part_b.b2.random_month_matched_conv_pct}}% → 依時期組成 {{part_b.b2.random_period_matched_conv_pct}}% → 手機規則 {{part_b.b2.mobile_conv_pct}}%：同一時期內只剩 {{part_b.b2.within_period_mobile_advantage_pp|+.2f}} pp，手機規則的優勢大半也是時期組成。反例：不配對、直接取全體分數前 {{part_b.b2.K_mobile_calls}} 名是 {{part_b.b2.pooled_topK_conv_pct}}%，看起來「贏」{{part_b.b2.pooled_minus_mobile_pp}} pp —— 那是挑到轉換率高的月份，外撥日不能換月份。
- **敏感度**：(a) ＋contact（假設撥號前已知有無手機，A2 表 2、附錄 A）：同月 {{part_b.b2.ml_contact_conv_pct}}%，差 {{part_b.b2.contact_diff_pp|+.2f}} pp，區間 [{{part_b.b2.contact_ci_low_pp|+.2f}}, {{part_b.b2.contact_ci_high_pp|+.2f}}] → 未通過；換種子時下限在 0 上下（另外 10 個種子中 {{part_b.b2.contact_seed_n_above0}} 個 > 0），處在統計邊界；同時期比 {{part_b.b2.period.contact_diff_pp|+.2f}} pp。(b) XGB（表 7 勝出者）：同月 {{part_b.b2.xgb.diff_pp|+.2f}} pp，區間 [{{part_b.b2.xgb.ci_low_pp|+.2f}}, {{part_b.b2.xgb.ci_high_pp|+.2f}}]，下限沒有大於 0；另外 10 個種子的下限介於 {{part_b.b2.xgb.seed_low_min_pp|+.2f}} 到 {{part_b.b2.xgb.seed_low_max_pp|+.2f}}，沒有一個 > 0；同時期 {{part_b.b2.xgb.period_diff_pp|+.2f}} pp。主版本名單有 {{part_b.b2.ml_cellular_share_pct}}% 本來就是手機客戶，兩份名單大量重疊。
- **商業意義**：A2 第 1–4 週離線回測的結論是「看不出比手機規則好」：同月差的區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}] 個百分點，以 {{part_b.b2.K_mobile_calls}} 通計，約從少 {{part_b.b2.ci_low_sales|abs}} 筆到多 {{part_b.b2.ci_high_sales}} 筆成交。這裡沒有做等效性檢定，所以不能說「兩者一樣好」，只能說沒有證據顯示名單較好。依 A2 表 9 階段 0，不進影子模式。限制：候選池只有本次被打過的客戶；contact 是本次活動實際使用的管道。
'''

MD['f1'] = r'''
### B-3 圖 1 解讀：名單 vs 手機規則

**結論：模型確實把會買的人往前排，但「往前排」有一大部分是時期；在手機規則的通數上，名單與手機規則看不出差別（RF 名單的差，95% 區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}] 個百分點；未做等效性檢定，不能說兩者一樣好）。**

- **上圖**：每個月都只打分數前 d%，前 20% 抓到 {{part_b.b1.curve.3.captured_pct}}% 的成交、前 50% 抓到 {{part_b.b1.curve.9.captured_pct}}%；改成每個時期都只打前 d%，前 20% 只抓到 {{part_b.b1.curve_period.3.captured_pct}}%、前 50% {{part_b.b1.curve_period.9.captured_pct}}% —— 同月曲線左半段的陡峭，有不少來自時期。在手機規則的通數上（{{part_b.b2.called_share_pct}}% 的客戶），手機規則抓到 {{part_b.b2.mobile_captured_pct}}% 的成交（菱形），同月配對名單 {{part_b.b2.ml_captured_pct}}%（實心點；XGB {{part_b.b2.xgb.captured_pct}}%），兩點幾乎重疊。
- **下圖**：同樣 {{part_b.b2.K_mobile_calls}} 通，隨機 {{part_b.b2.random_conv_pct}}%、依月份組成 {{part_b.b2.random_month_matched_conv_pct}}%、依時期組成 {{part_b.b2.random_period_matched_conv_pct}}%、手機規則 {{part_b.b2.mobile_conv_pct}}%、RF 同時期 {{part_b.b2.period.ml_conv_pct}}%、RF 同月 {{part_b.b2.ml_conv_pct}}%、XGB 同月 {{part_b.b2.xgb.ml_conv_pct}}%。誤差線 = 手機規則轉換率 + 差的 95% 區間；名單要整條在虛線右邊才算通過，三條都碰到或跨過虛線。
- **商業意義**：這就是業務②「未證實」在圖上的樣子。
'''

MD['b4'] = r'''
### B-4 解讀：業務① 每筆成交的通話成本（A2 目標 ≤ A\$20.87）

**結論：與手機規則同通數的名單每筆成交 A\${{part_b.b1.ml_cost_formula}}，未達 A\$20.87；名單變淺成本會下降，但能降多少取決於時期，截斷深度必須由 A/B 校準，不能從這份離線資料挑。**

- **觀察**：同月配對名單 A\${{part_b.b1.ml_cost_formula}}（A2 情境公式 c(r)/r）、A\${{part_b.b1.ml_cost_actual}}（實際秒數）；同時期配對 A\${{part_b.b1.ml_period_cost_formula}}；手機規則 A\${{part_b.b1.mobile_cost_formula}}、隨機外撥 A\${{part_b.b1.random_cost_formula}}（A2 全檔為 A\$27.35）；XGB 名單 A\${{part_b.xgb_eval.cost_formula}}。RF 名單比隨機省 A\${{part_b.b1.random_minus_ml}}、比手機規則只省 A\${{part_b.b1.mobile_minus_ml}}，比目標高 A\${{part_b.b1.ml_minus_target}}（手機規則高 A\${{part_b.b1.mobile_minus_target}}）→ 未達。
- **描述性曲線（不拿來挑截斷點）**：同月配對時，每月只打前 50% 的成本 A\${{part_b.b1.depth50_cost}}（轉換率 {{part_b.b1.depth50_conv_pct}}%）；但同時期配對時要淺到約 {{part_b.b1.deepest_ok_depth_period_pct|.0f}}% 才低於 A\$20.87，50% 時是 A\${{part_b.b1.curve_period.9.cost_formula}}。兩種配對差這麼多，表示「淺一點就達標」的離線證據大半靠時期挑選。單次測試樣本本身也有雜訊：50% 那一點只有 {{part_b.b1.depth50_n|,}} 人，轉換率的 95% 範圍換算成本約 A\${{part_b.b1.depth50_cost_low}}–A\${{part_b.b1.depth50_cost_high}}，跨過目標。
- **外推一輪**（同樣 2,300 筆成交）：同月配對名單約 {{part_b.b1.one_round_extrapolation.ml_list.calls|,}} 通、A\${{part_b.b1.one_round_extrapolation.ml_list.call_cost|,}}（A2：現況 A\$62,905、目標約 A\$48,000），目標層級的對照見 B-13 與圖 7。
- **商業意義與注意**：① 在 A2 是 A/B 列報項，不是硬門檻；名單變淺會漏掉更多成交，是產能與營收的取捨，深度要在 A/B 中校準。時薪 A\$50、每通時長維持試點平均都是 A2 的假設；實際秒數用到 duration，只當事後成本帳。
'''

MD['f2'] = r'''
### B-4 圖 2 解讀：每筆成交成本 vs 名單深度

**結論：名單越深成本越高；同時期配對的成本線整條在同月配對之上，所以「多淺才達標」沒有可靠的離線答案。**

- 同月配對：前 20% 約 A\${{part_b.b1.curve.3.cost_formula}}、與手機同通數時 A\${{part_b.b1.ml_cost_formula}}，全部都打回到 A\${{part_b.b1.curve.19.cost_formula}}（測試集的隨機外撥；A2 全檔 A\$27.35）。實際秒數（虛線）略低於 A2 公式：名單裡成交者的實際通話比 A2 的平均短一些。
- 同時期配對：前 20% 已是 A\${{part_b.b1.curve_period.3.cost_formula}}、前 50% A\${{part_b.b1.curve_period.9.cost_formula}}。
- 這張圖只描述成本隨深度上升；截斷點不由它決定。
'''

MD['b5'] = r'''
### B-5 解讀：混淆矩陣（上表與圖 6）

**結論：在實際做得到的同月配對名單上，精確率 {{part_b.confusion.month_matched.precision_pct}}%、召回率 {{part_b.confusion.month_matched.recall_pct}}%，和手機規則的召回率 {{part_b.confusion.mobile_recall_pct}}% 相近；混淆矩陣看不到「打給本來就會買的人」這種錯誤，它藏在 TP 裡（B-8 估算）。**

- **主表與圖 6（同月同通數名單，{{part_b.confusion.K}} 人）**：成交（TP）{{part_b.confusion.month_matched.TP}}、白打（FP）{{part_b.confusion.month_matched.FP}}；名單外仍成交（FN）{{part_b.confusion.month_matched.FN}}、名單外未成交（TN）{{part_b.confusion.month_matched.TN}}。
- **參考（單一門檻名單）**：TP {{part_b.confusion.pooled.TP}}、FP {{part_b.confusion.pooled.FP}}、FN {{part_b.confusion.pooled.FN}}、TN {{part_b.confusion.pooled.TN}}，精確率 {{part_b.confusion.pooled.precision_pct}}%、召回率 {{part_b.confusion.pooled.recall_pct}}%。這份名單含月份組成（B-3 的反例），精確率比同月配對高 {{part_b.confusion.pooled_minus_month_precision_pp}} pp；只因為對照組沒有月份，B-6 的增量比較必須用它：門檻同時作用在兩組，增量不受月份挑選影響，但名單轉換率 r 偏高，所以 ⑤ 的絕對值只作示算。
- **錢花在哪**（A2 假設）：FP 每通約 A\$3.07，主表合計約 A\${{part_b.confusion.month_matched.fp_cost_aud|,}}；TN 是省下的電話，約 A\${{part_b.confusion.month_matched.tn_saving_aud|,}}。
- **看不到的錯誤**：A2 表 4 註指出，2:1 下每人代價最高的是「打給本來就會買的人」（白送一份折扣，再加一通約 A\$6.90 的成交電話）—— 它藏在 TP 裡；FN 也分不出是不是本來就會買。B-8 用對照組估算，並看折扣額 D 改變時排序會不會變。
- **商業意義**：調低門檻可以少漏成交，但每多一人就多一通約 A\$3.07 的電話，還可能多送折扣給本來就會買的人；門檻是成本決策，不是統計決策。
'''

MD['b6'] = r'''
### B-6 解讀：業務③ 增量（上線硬門檻）與業務④ 本來就會買的比例（列報）

**結論：不控制時期時，增量隨重複列的處理落在 {{part_b.b3b4.dedup.uplift_pp|+.2f}} 到 {{part_b.b3b4.raw.uplift_pp|+.2f}} 個百分點；控制 (cpi, cci) 時期後兩個口徑分別為 {{part_b.b3b4.dedup.period_stratified_uplift_pp|+.2f}} 與 {{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}}，兩個區間都含 0。離線無法判定增量為正（未證實）。④ 兩個口徑的區間都高於 50% 兩平點（未達）。**

- **去重（主口徑）**：分數 ≥ 門檻的目標組名單 {{part_b.b3b4.dedup.list_n}} 人、轉換率 {{part_b.b3b4.dedup.list_conv_pct}}%；對照組中分數同樣 ≥ 門檻的 {{part_b.b3b4.dedup.control_above_n}} 人、{{part_b.b3b4.dedup.control_above_conv_pct}}% → 增量 {{part_b.b3b4.dedup.uplift_pp|+.2f}} pp（95% 區間 [{{part_b.b3b4.dedup.uplift_ci_low_pp|+.2f}}, {{part_b.b3b4.dedup.uplift_ci_high_pp|+.2f}}]，含 0）；成交者中本來就會買 {{part_b.b3b4.dedup.would_buy_share_pct}}%（區間 {{part_b.b3b4.dedup.would_buy_ci_low_pct}}%–{{part_b.b3b4.dedup.would_buy_ci_high_pct}}%）。
- **原始資料（敏感度）**：同樣流程，名單 {{part_b.b3b4.raw.list_conv_pct}}% 對 {{part_b.b3b4.raw.control_above_conv_pct}}% → 增量 {{part_b.b3b4.raw.uplift_pp|+.2f}} pp [{{part_b.b3b4.raw.uplift_ci_low_pp|+.2f}}, {{part_b.b3b4.raw.uplift_ci_high_pp|+.2f}}]；本來就會買 {{part_b.b3b4.raw.would_buy_share_pct}}%（區間 {{part_b.b3b4.raw.would_buy_ci_low_pct}}%–{{part_b.b3b4.raw.would_buy_ci_high_pct}}%），和 A2 試點全體的 {{part_b.a2_recomputed.pilot_would_buy_share_pct}}% 相近，沒有看到 A2 擔心的「第一步會升高」。
- **控制時期之後**：門檻仍用全體 t，在每個 (cpi, cci) 時期內比較名單與對照組（兩邊都至少 20 人的時期才納入，涵蓋名單的 {{part_b.b3b4.dedup.period_coverage_pct}}%／{{part_b.b3b4.raw.period_coverage_pct}}%），再依名單人數加權：去重 {{part_b.b3b4.dedup.period_stratified_uplift_pp|+.2f}} pp（區間 [{{part_b.b3b4.dedup.period_stratified_ci_low_pp|+.2f}}, {{part_b.b3b4.dedup.period_stratified_ci_high_pp|+.2f}}]）、原始 {{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}} pp（區間 [{{part_b.b3b4.raw.period_stratified_ci_low_pp|+.2f}}, {{part_b.b3b4.raw.period_stratified_ci_high_pp|+.2f}}]）；不設 20 人下限時 {{part_b.b3b4.dedup.period_stratified_uplift_nomin_pp|+.2f}}／{{part_b.b3b4.raw.period_stratified_uplift_nomin_pp|+.2f}}。點估計都在 ±1 個百分點內，但區間寬，無法判定正負。
- **原始口徑的 +4 pp 從哪來：兩件事都有份**。(1) 時期組成：原始口徑在各時期內比只剩 {{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}}，比未分層少了 {{part_b.b3b4.raw_minus_raw_strat_pp}} 個百分點 —— 大部分來自兩組在各時期的人數組成不同。(2) 重複列的處理：分層後兩個口徑仍差 {{part_b.b3b4.strat_raw_minus_dedup_pp}} 個百分點（{{part_b.b3b4.dedup.period_stratified_uplift_pp|+.2f}} 對 {{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}}）：被刪的列幾乎全在對照組，去重同時改變了對照組的轉換率與它在各時期的組成。兩個分層區間部分重疊，這 {{part_b.b3b4.strat_raw_minus_dedup_pp}} 個百分點的差本身也還不確定。
- **組成與方法**：分數 ≥ 門檻的比例，目標組 {{part_b.b3b4.dedup.target_above_share_pct}}%、對照組 {{part_b.b3b4.dedup.control_above_share_pct}}%（去重），兩組並非完全可比。bootstrap：名單與同門檻對照組各自有放回重抽（B = 1,000），門檻固定為 t；分時期的區間是在每個時期內兩組各自重抽後再加權。
- **商業意義**：③ 是上線硬門檻，但離線只能看方向，方向又取決於資料版本與是否控制時期 —— 這正是 A2 把 ③ 的確認排在 A/B（常設對照組同樣評分、不外撥）的理由。④ 高於 50% 表示 2:1 下名單每多打一通都虧（與 B-7 一致）。
'''

MD['f3'] = r'''
### B-6 圖 3 解讀：打電話＋優惠 vs 不打（同一分數門檻）

**結論：被模型排到前面的人，不打也差不多會買 —— 名單轉換率高不等於打電話有用。**

- 左：A2 試點全體（原始資料、沒有門檻）{{part_b.a2_recomputed.pilot_target_conv_pct}}% 對 {{part_b.a2_recomputed.pilot_control_conv_pct}}%，增量 {{part_b.a2_recomputed.pilot_uplift_pp|.2f}} pp。中：去重後名單與對照組幾乎一樣高。右：原始資料下名單高約 {{part_b.b3b4.raw.uplift_pp|.0f}} pp（區間不含 0），但在各時期內只剩 {{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}}，區間含 0（圖上的 within periods）。
- 中、右兩組的藍柱都比左邊的全體高，表示模型確實把「會買的人」往前排；A2 的第二步（增量模型）就是要把「會買」和「打了才會買」分開。
'''

MD['b7'] = r'''
### B-7 解讀：業務⑤ 式 1 淨值（只能示算）

**結論：在 2:1 假設下，名單、隨機外撥與 A2 試點的每通淨值全部為負，名單比隨機更負；⑤ 的門檻（不低於手機規則組）離線無法判定。**

- **公式**：每通淨值（相對於不外撥）= D ×（2u − r）− c(r)；u = 增量、r = 名單轉換率、收益 = 2D、c(r) = 每通通話成本。2u − r ≥ 0 ⇔ 本來就會買的比例 ≤ 50%（A2 式 2）。全部用未取整的 u、r 計算。
- **結果（每通，以折扣 D 為單位、未計通話成本）**：去重名單 {{part_b.b5.dedup_ml_list.net_D_per_call_excl_call_cost|+.3f}} D、隨機 {{part_b.b5.dedup_random.net_D_per_call_excl_call_cost|+.3f}} D；原始名單 {{part_b.b5.raw_ml_list.net_D_per_call_excl_call_cost|+.3f}} D、隨機 {{part_b.b5.raw_random.net_D_per_call_excl_call_cost|+.3f}} D；A2 試點全體 {{part_b.b5.a2_pilot_all.net_D_per_call_excl_call_cost|+.3f}} D；XGB 名單 {{part_b.xgb_eval.b5.dedup_ml_list.net_D_per_call_excl_call_cost|+.3f}}／{{part_b.xgb_eval.b5.raw_ml_list.net_D_per_call_excl_call_cost|+.3f}} D。2u − r 全部小於 0，所以 2:1 下任何折扣都沒有兩平點（表中 break-even D 為 none），與 A2「1.31 倍 < 2 倍」一致。以 A2 的示例 D = A\$36、計入通話成本，RF 名單每通約 −A\${{part_b.b5.dedup_ml_list.net_aud_per_call_at_D36|abs.2f}}（去重）、−A\${{part_b.b5.raw_ml_list.net_aud_per_call_at_D36|abs.2f}}（原始），每千通約 −A\${{part_b.b5.dedup_ml_list.net_aud_per_1000_calls_at_D36|abs,.0f}}（去重）。
- **為什麼名單更負**：模型把本來就會買的人排在前面（業務④），每通送出更多白給的折扣；而且 r 用的是單一門檻名單，含月份組成而偏高（B-5），絕對值只作示算。
- **為什麼只能示算**：⑤ 的門檻是「不低於同期手機規則組」，需要手機規則組自己的增量 ——「沒被打的手機客戶」的轉換率；對照組沒有 contact，離線算不出來。折扣與收益的實際金額 A2 也還未定（由財務提供）。
- **商業意義**：第一步名單上線不會讓淨值轉正；它的價值是少打電話（業務①）與替第二步累積資料，必須在 A/B 中以 ⑤ 把關（A2 表 9 階段 2）。
'''

MD['b_err'] = r'''
### B-8 解讀：三種錯誤的代價（A2 表 4 註、表 8 註）

**結論：以示例折扣額 D = A\$36，「打給本來就會買的人」每人約 A\${{part_b.errors.dedup.unit_cost_at_D36.0}}，合計也最大；但排序取決於 D —— D = A\$10 時，原始口徑下「打給不會買的人」的合計反而最大。「打了才會買」卻被漏掉的人，離線估不出來。**

- **漏掉的是誰（A2 表 8 註）**：分數低於門檻、沒被選上的人裡，有被打的目標組轉換率 {{part_b.errors.dedup.below_target_conv_pct}}%、沒被打的對照組 {{part_b.errors.dedup.below_control_conv_pct}}%：去重口徑差 {{part_b.errors.dedup.below_uplift_pp|+.2f}} pp，95% 區間 [{{part_b.errors.dedup.below_uplift_ci_low_pp|+.2f}}, {{part_b.errors.dedup.below_uplift_ci_high_pp|+.2f}}]，整個區間都在 0 以下 —— 被打的反而比沒被打的低。打電話不太可能讓人更不想買，比較合理的解釋是兩組不可比：去重只刪了對照組的列（不對稱），對照組的組成因此和目標組不同。所以這不是「名單外的成交者本來就會買」的證據。原始口徑 {{part_b.errors.raw.below_target_conv_pct}}% 對 {{part_b.errors.raw.below_control_conv_pct}}%，差 {{part_b.errors.raw.below_uplift_pp|+.2f}} pp（區間 [{{part_b.errors.raw.below_uplift_ci_low_pp|+.2f}}, {{part_b.errors.raw.below_uplift_ci_high_pp|+.2f}}]），才接近 A2 規則說的「相近」。
- **三種錯誤（測試集目標組規模，D = A\$36）**：錯誤 A 打給本來就會買的人 每人 A\${{part_b.errors.dedup.unit_cost_at_D36.0}}，約 {{part_b.errors.dedup.n_wouldbuy_on_list|,}} 人、A\${{part_b.errors.dedup.total_at_D36.0|,}}（原始 {{part_b.errors.raw.n_wouldbuy_on_list|,}} 人、A\${{part_b.errors.raw.total_at_D36.0|,}}）。錯誤 B 漏掉打了才會買的人 每人 A\${{part_b.errors.dedup.unit_cost_at_D36.1}}：去重口徑的增量為負，人數估計不出來（區間上限換算也是 {{part_b.errors.dedup.n_missed_upper}} 人）；原始口徑約 {{part_b.errors.raw.n_missed_incremental}} 人、A\${{part_b.errors.raw.total_at_D36.1|,}}（區間上限 {{part_b.errors.raw.n_missed_upper}} 人、A\${{part_b.errors.raw.by_D.36.total_2_upper|,}}）。這些都是用不可比的對照組估的（去重口徑的對照組轉換率反而較高，可能低估），只作示算。錯誤 C 打給不會買的人 每人 A\${{part_b.errors.dedup.unit_cost_at_D36.2}}，約 {{part_b.errors.dedup.n_fp|,}} 人、A\${{part_b.errors.dedup.total_at_D36.2|,}}。
- **排序取決於 D（示例折扣額，A2 未定）**：每人代價：錯誤 A 永遠比錯誤 B 高 2 × A\$6.90；錯誤 B 只有在 D 高於約 A\${{part_b.errors.D_where_2_exceeds_3}} 時才比錯誤 C 貴。合計金額：D = A\$36 或 A\$100 時兩個口徑都是錯誤 A 最大；D = A\$10 時，去重口徑仍是錯誤 A（A\${{part_b.errors.dedup.by_D.10.total.0|,}} 對錯誤 C 的 A\${{part_b.errors.dedup.by_D.10.total.2|,}}），原始口徑則是錯誤 C（A\${{part_b.errors.raw.by_D.10.total.2|,}}）大於錯誤 A（A\${{part_b.errors.raw.by_D.10.total.0|,}}）。A2「最貴的錯誤是打給本來就會買的人」在 D 不太小時成立；D 要由財務提供。
- **對門檻的含意**：調低門檻是為了減少錯誤 B，但離線看不到錯誤 B，多打的人主要會落在錯誤 A 與錯誤 C；接受機率模型分不出錯誤 A 與錯誤 B，所以 A2 的第二步改排增量。這些人數假設兩組可比（B-6 已說明它們並非完全可比），只作示算。
'''

MD['b8'] = r'''
### B-9 解讀：ML④ 分群一致性（年齡層、婚姻、月份）

**結論：只有婚姻達標；年齡層與月份的 AUC 差都超過 0.05 → ML④ 未達。**

- **年齡層**：AUC 最低是 {{part_b.ml4.gaps.age_band.lowest}}（{{part_b.ml4.gaps.age_band.lowest_auc}}）、最高是 {{part_b.ml4.gaps.age_band.highest}}（{{part_b.ml4.gaps.age_band.highest_auc}}），差 {{part_b.ml4.gaps.age_band.max_minus_min|.3f}} > 0.05；60 歲以上只有 {{part_b.ml4.segments.4.n}} 人（{{part_b.ml4.segments.4.conversions}} 筆成交），區間很寬。
- **婚姻**：divorced／married／single 差 {{part_b.ml4.gaps.marital.max_minus_min|.3f}} → 達標（unknown 只有 {{part_b.ml4.segments.8.n}} 人，只列報）。
- **月份（A2 表 4 寫的是「時期」，這裡以月份代理）**：成交至少 30 筆的 {{part_b.ml4.gaps.month.groups_in_gate}} 個月份差 {{part_b.ml4.gaps.month.max_minus_min|.3f}}；AUC 最低的三個月是 {{part_b.ml4.gaps.month.three_lowest.0}}、{{part_b.ml4.gaps.month.three_lowest.1}}、{{part_b.ml4.gaps.month.three_lowest.2}}，原因不明（轉換率高、樣本小、月內混有不同時期都可能）。XGB 的三個差為 {{part_b.xgb_eval.ml4_gaps.age_band|.3f}}／{{part_b.xgb_eval.ml4_gaps.marital|.3f}}／{{part_b.xgb_eval.ml4_gaps.month|.3f}}，判定相同。
- **入選比例**（實際可行的同月配對名單）：60 歲以上 {{part_b.ml4.segments.4.selected_pct|.0f}}%、30 歲以下 {{part_b.ml4.segments.0.selected_pct|.0f}}%，40–49、50–59 歲 {{part_b.ml4.segments.2.selected_pct|.0f}}%、{{part_b.ml4.segments.3.selected_pct|.0f}}%；單身 {{part_b.ml4.segments.7.selected_pct|.0f}}%、已婚 {{part_b.ml4.segments.6.selected_pct|.0f}}%。用單一門檻名單時方向相同、幅度較大（60 歲以上 {{part_b.ml4.segments.4.selected_pct_pooled|.0f}}%、30 歲以下 {{part_b.ml4.segments.0.selected_pct_pooled|.0f}}%）。60 歲以上的轉換率 {{part_b.ml4.segments.4.conv_pct|.1f}}%，入選比例的差異可能部分反映時期組成；這正是 A2 要求入選比例交法遵複核的原因。
- **注意**：各群轉換率本來就不同，AUC 差不全是模型問題；這是舊資格標準下的母體。
'''

MD['f4'] = r'''
### B-9 圖 4 解讀：分群 AUC

**結論：婚姻三群都落在 0.05 的容許帶內；年齡的兩端與月份散得最開。**

- 淺色帶是從各維度最低 AUC 起算 0.05 的寬度，實心點全落在帶內，該維度才算達標。
- 小群（3 月、10 月、60 歲以上）的區間寬度都超過 0.05，單輪資料本來就量不準 —— A2 表 10 用「連續 2 輪」才觸發重驗，就是這個原因。
'''

MD['b9'] = r'''
### B-10 解讀：permutation importance 與拿掉年齡、婚姻的代價

**結論：模型最依賴 cci、cpi（時期），其次是前次行銷結果；拿掉年齡或婚姻重訓，AUC 幾乎不變。**

- **permutation importance**：打亂 cci 時測試 AUC 平均掉 {{part_b.perm_importance.cons_conf_idx.mean_auc_drop}}；cpi {{part_b.perm_importance.cons_price_idx.mean_auc_drop}}、poutcome {{part_b.perm_importance.poutcome.mean_auc_drop}}；其餘欄位都在 0.01 以下（婚姻 {{part_b.perm_importance.marital.mean_auc_drop}}、年齡 {{part_b.perm_importance.age.mean_auc_drop}}）。這與同一時期內 AUC 只有 {{part_b.ml.ml2_within_period_auc}} 一致：時期內 cpi、cci 不變，可用的只剩客戶欄位。
- **拿掉欄位重訓**（同樣固定的超參數、只用訓練集目標組；測試 AUC 只當敏感度）：拿掉年齡 {{part_b.drop_retrain.age.test_auc}}（{{part_b.drop_retrain.age.change|+.4f}}）、拿掉婚姻 {{part_b.drop_retrain.marital.test_auc}}（{{part_b.drop_retrain.marital.change|+.4f}}）、兩者都拿掉 {{part_b.drop_retrain.age_marital.test_auc}}（{{part_b.drop_retrain.age_marital.change|+.4f}}）。
- **這是關聯，不是因果**：不能說「消費者信心高，客戶就會因此辦卡」；cpi 與 cci 都是時期代理，彼此相關，重要度會互相分攤。
- **商業意義**：(1) 上線評分時 cpi、cci 用最新已公布值，超出訓練範圍（A2 表 10：cpi 92.2–94.8、cci −50.8 至 −26.9）就要觸發重驗；(2) 若法遵不准用年齡、婚姻，拿掉的代價很小。
'''

MD['f5'] = r'''
### B-10 圖 5 解讀

長條是打亂該欄後 AUC 的平均下降（誤差線為 10 次重複的標準差）。前三名（cci、cpi、poutcome）遠高於其他欄位；loan、housing、marital 的下降與 0 無法區分。圖只說明模型依賴哪些欄位，不代表這些欄位「造成」購買。
'''

MD['b10'] = r'''
### ML⑤ 增量排序模型：不可離線驗（A2 表 4 ML 第 5 列）

- **A2 表 4 的標準**：名單內客戶的平均增量 > 全體平均增量（＝隨機外撥組轉換率 − 對照組轉換率）；資料來源是 12 週後累積的常設對照組（5–10% 不外撥、照樣評分）＋隨機外撥組（A2 表 9 的常設列）。
- **試點資料做不到**：沒有客戶編號、兩組組成不同（前次行銷成功者：原始全檔目標組 {{part_b.a2_recomputed.prev_success_share_pct.raw_target|.2f}}% 對對照組 {{part_b.a2_recomputed.prev_success_share_pct.raw_control|.2f}}%；去重後 {{part_b.a2_recomputed.prev_success_share_pct.dedup_target|.2f}}% 對 {{part_b.a2_recomputed.prev_success_share_pct.dedup_control|.2f}}%）、去重不對稱；而 B-6 已經顯示，連「全體平均增量」本身在去重測試集上都只有 {{part_b.b3b4.dedup.overall_uplift_pp|+.2f}} 個百分點。
- 所以本檔不建增量模型、不作達標判定；做法（目標組、對照組各建一個模型，分數相減前先校準）留在報告的未來改進。
'''

MD['xgb'] = r'''
### B-11 解讀：依 A2 表 7 勝出的 XGB，十條標準的平行評估

**結論：XGB 的十條判定與 RF 完全相同。它的 AUC 較高（{{part_b.ml.xgb_test_auc}} 對 {{part_b.ml.ml2_test_auc}}），但同一時期內只有 {{part_b.ml.xgb_within_period_auc}}；② 差 {{part_b.b2.xgb.diff_pp|+.2f}} pp、區間下限沒有大於 0，仍未通過；去重口徑的增量甚至是 {{part_b.xgb_eval.b3b4_dedup.uplift_pp|+.2f}} pp。換成較強的模型不改變「停在階段 0」—— 瓶頸在資料（缺撥號前的客戶特徵、時期與組別不可比），不在演算法。**

- **①**：同月配對名單 A\${{part_b.xgb_eval.cost_formula}}（RF A\${{part_b.b1.ml_cost_formula}}），仍高於 A\$20.87。
- **③④**：去重 {{part_b.xgb_eval.b3b4_dedup.uplift_pp|+.2f}} pp [{{part_b.xgb_eval.b3b4_dedup.uplift_ci_low_pp|+.2f}}, {{part_b.xgb_eval.b3b4_dedup.uplift_ci_high_pp|+.2f}}]、原始 {{part_b.xgb_eval.b3b4_raw.uplift_pp|+.2f}} pp [{{part_b.xgb_eval.b3b4_raw.uplift_ci_low_pp|+.2f}}, {{part_b.xgb_eval.b3b4_raw.uplift_ci_high_pp|+.2f}}]；分時期 {{part_b.xgb_eval.b3b4_dedup.period_stratified_uplift_pp|+.2f}}／{{part_b.xgb_eval.b3b4_raw.period_stratified_uplift_pp|+.2f}} pp（區間都含 0）；本來就會買 {{part_b.xgb_eval.b3b4_dedup.would_buy_share_pct}}%／{{part_b.xgb_eval.b3b4_raw.would_buy_share_pct}}%。
- **⑤**：2u − r = {{part_b.xgb_eval.b5.dedup_ml_list.net_D_per_call_excl_call_cost|+.3f}}／{{part_b.xgb_eval.b5.raw_ml_list.net_D_per_call_excl_call_cost|+.3f}} D 每通，2:1 下仍為負。
- **ML②③④**：測試 AUC {{part_b.ml.xgb_test_auc}}、訓練 − 測試 {{part_b.ml.xgb_gap}}；分群 AUC 差：年齡 {{part_b.xgb_eval.ml4_gaps.age_band|.3f}}、婚姻 {{part_b.xgb_eval.ml4_gaps.marital|.3f}}、月份 {{part_b.xgb_eval.ml4_gaps.month|.3f}}。
'''

MD['b11'] = r'''
### B-12 解讀：A2 表 4 十條標準的總表

**結論：兩條「達標」都是 ML 指標，業務指標沒有一條達標；三條上線硬門檻（業務②③⑤）沒有一條能離線判定為通過。**

- 10 條中：達標 {{part_b.kpi_counts.達標}}（ML①、ML③）、未證實 {{part_b.kpi_counts.未證實}}（業務②、業務③、ML②）、未達 {{part_b.kpi_counts.未達}}（業務①、業務④、ML④）、示算 {{part_b.kpi_counts.示算}}（業務⑤）、不可離線驗 {{part_b.kpi_counts.不可離線驗}}（ML⑤）。XGB 欄的判定逐條相同。業務①④ 是 A2 的列報項（不作關卡），仍依門檻標達／未達。
- 業務②：同月配對名單看不出比手機規則好（差的 95% 區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}]，未做等效性檢定），同時期點估計為負、區間同樣含 0；業務③：方向取決於資料版本與是否控制時期；業務④：兩個口徑都高於 50% 兩平參考；業務⑤：只能示算，而且為負。
'''

MD['goals'] = r'''
### B-13 解讀：A2 表 1 的商業目標（上面兩張表與圖 7）

**結論：以 A2 表 1 的目標看，離線結果沒有一項達標。相對現行手機規則，名單每輪只省約 A\${{part_b.goals.saving_ml_vs_mobile_aud|,}}；控制月份組成後，相對隨機外撥也只省 A\${{part_b.goals.saving_ml_vs_random_mm_aud|,}}，是 A2 目標節省的 {{part_b.goals.saving_ml_vs_random_mm_share_of_target_pct|.0f}}%（圖 7）。**

- **每輪通話成本**：A2 目標是每輪省約 A\${{part_b.goals.saving_target_aud|,}}。同月配對名單外推比現況省 A\${{part_b.goals.saving_ml_vs_pilot_aud|,}}（目標的 {{part_b.goals.saving_ml_share_of_target_pct|.0f}}%），但現況是全體隨機外撥、沒有控制月份：依手機規則的月份組成隨機外撥（{{part_b.b2.random_month_matched_conv_pct}}%）外推，就已比現況省 A\${{part_b.goals.saving_random_mm_vs_pilot_aud|,}}；名單相對它只省 A\${{part_b.goals.saving_ml_vs_random_mm_aud|,}}（手機規則 A\${{part_b.goals.saving_mobile_vs_random_mm_aud|,}}）。同時期配對的名單只比現況省 A\${{part_b.goals.saving_ml_period_vs_pilot_aud|,}}。外撥量少 {{part_b.goals.fewer_calls_ml_pct}}%（手機規則 {{part_b.goals.fewer_calls_mobile_pct}}%，目標約 {{part_b.goals.fewer_calls_target_pct|.0f}}%）。
- **模型最多能動到多少通話費**：名單就算達到 A2 目標（轉換率 18%），每輪也只比手機規則多省 A\${{part_b.goals.saving_target_vs_mobile_aud|,}}；目前實際多省 A\${{part_b.goals.saving_ml_vs_mobile_aud|,}}。
- **收益倍數（不依 2:1）**：A2 試點每張卡收益至少要是折扣的 {{part_b.goals.multiple_pilot}} 倍才不虧；名單在原始口徑要 {{part_b.goals.multiple_ml_raw}} 倍（與試點相近）、去重口徑要 {{part_b.goals.multiple_ml_dedup}} 倍（增量區間含 0，倍數不穩）—— 第一步名單沒有讓這個門檻降低。
- **增量與外溢**：增量為正與外溢比例都要等 A/B 的常設對照組才量得到（B-6、B-8）；外溢的金額量級見圖 8。
- **商業意義**：A2 寫的「每輪省約 A\$14,900」是以名單轉換率 18% 推得的；離線證據顯示，在與手機規則同通數下達不到 18%，而節省的大部分不需要 ML 也拿得到。圖 7 的金額都是用測試集轉換率外推的，不是測得的。
'''

MD['concl'] = r'''
<a id="conclusion" name="conclusion"></a>
## 結論

1. **AUC 達標 ≠ 商業達標。** 撥號前 AUC {{part_b.ml.ml2_test_auc}} 過了 0.75，但同一時期內只有 {{part_b.ml.ml2_within_period_auc}}（圖 9）；業務指標 {{part_b.kpi_business_pass}}／5 達標（B-2、B-12）。
2. **業務② 可以離線判定：未通過。** 同月只比手機規則高 {{part_b.b2.diff_pp|.2f}} pp，區間 [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}] 含 0；同時期點估計 {{part_b.b2.period.diff_pp|+.2f}} pp，區間同樣含 0（B-3）。
3. **業務③⑤ 離線無法判定，要等 A/B。** 業務③ 控制時期後 {{part_b.b3b4.dedup.period_stratified_uplift_pp|+.2f}}／{{part_b.b3b4.raw.period_stratified_uplift_pp|+.2f}} pp，區間都含 0；業務⑤ 缺手機規則組的增量，2:1 示算為負（B-6、B-7）。
4. **換模型不是解方。** 依 A2 表 7 勝出的 XGB，十條判定與 RF 相同（B-11）。
5. **錢的缺口主要在優惠設計，不在名單（示算）。** 名單相對手機規則每輪只多省 A\${{part_b.goals.saving_ml_vs_mobile_aud|,}}，即使達到 A2 目標也最多多省 A\${{part_b.goals.saving_target_vs_mobile_aud|,}}；每張折扣只要高於約 A\${{part_b.goals.D_spill_exceeds_target_vs_mobile_saving_aud.raw|.2f}}（原始）／A\${{part_b.goals.D_spill_exceeds_target_vs_mobile_saving_aud.dedup|.2f}}（去重），每輪白送給本來就會買者的折扣就超過這個數，名單也沒有讓這筆變少（以示例折扣 D = A\$36 算約 A\${{part_b.goals.spillover_discount_per_round_D36_aud.raw|,}}–{{part_b.goals.spillover_discount_per_round_D36_aud.dedup|,}}；B-13、圖 7、圖 8）。
6. **建議：照 A2 的 12 週計畫，停在第 1–4 週。** 階段 0 未過，不進第 5–7 週影子模式；先補撥號前客戶特徵、外撥日期與客戶編號，用新的時間段重測（年齡、婚姻先交法遵，拿掉它們 AUC 幾乎不變）。下一輪即可先做、不需模型的準備：照現行做法外撥時記錄外撥日期與客戶編號（A2 請求 ②），並請財務提供每張卡的收益與折扣金額。
'''

MD['f9'] = r'''
### B-2 圖 9 解讀：撥號前 AUC 從哪來

**結論：AUC 從 {{part_b.ml.ml1_poc_test_auc}}（概念驗證，含通話後才知道的 duration）降到 {{part_b.ml.ml2_test_auc}}（撥號前）、{{part_b.ml.ml2_within_month_auc}}（月內）、{{part_b.ml.ml2_within_period_auc}}（同一 (cpi, cci) 時期內）；只有前兩條在 A2 門檻 0.75 的右邊，時期內接近亂猜的 0.5。**

- **第一段落差是 duration**（事後資訊）：同樣的撥號前 RF 只多加 duration，AUC 就升到 {{part_b.ml.ml2_with_duration_auc}}（B-2 的受控比較）。
- **後兩段落差是時期**：外撥日的候選人都在同一時期，名單排序實際能用的是最下面那條。
- **讀法**：長條越往右排序越準；虛線 0.75 是 A2 的 ML② 門檻，點線 0.5 是亂猜。
- **注意**：概念驗證是在全部 {{meta.rows.test|,}} 筆測試列上算的（含對照組），其餘三條只在測試集目標組 {{part_b.ml.test_target_rows|,}} 人上算；在同一批目標組上，概念驗證的 AUC 是 {{part_b.ml.ml1_poc_target_only_auc}}。
'''

MD['f8'] = r'''
### B-13 圖 8 解讀：每輪的錢花在哪（示算）

**結論：錢的缺口主要在優惠設計（白送給本來就會買的人），不在名單。以收益：折扣 = 2:1、示例折扣 D = A\$36 示算，同樣 2,300 筆成交，每輪送給本來就會買者的折扣：試點約 A\${{part_b.goals.spillover_discount_per_round_D36_aud.pilot|,}}，名單 A\${{part_b.goals.spillover_discount_per_round_D36_aud.raw|,}}（原始口徑）到 A\${{part_b.goals.spillover_discount_per_round_D36_aud.dedup|,}}（去重口徑），與整輪通話成本同一量級或更大；名單即使達到 A2 目標，相對手機規則每輪最多也只多省 A\${{part_b.goals.saving_target_vs_mobile_aud|,}} 通話費。**

- **三段**：未成交電話（每通約 A\${{part_b.a2_recomputed.call_cost_no}}）、成交電話（每通約 A\${{part_b.a2_recomputed.call_cost_yes|.2f}}）、送給本來就會買者的折扣（2,300 × 本來就會買的比例 × D）。名單把未成交電話從 A\${{part_b.goals.round_spend_D36.pilot.unconverted_calls_aud|,}} 降到 A\${{part_b.goals.round_spend_D36.ml_list_raw_share.unconverted_calls_aud|,}}；折扣那一段在原始口徑幾乎不動，在去重口徑反而更高。
- **損益平衡的 D**：每張卡折扣只要高於約 A\${{part_b.goals.D_spill_exceeds_target_vs_mobile_saving_aud.raw|.2f}}（原始）／A\${{part_b.goals.D_spill_exceeds_target_vs_mobile_saving_aud.dedup|.2f}}（去重），每輪白送的折扣就超過名單最多能多省的通話費（A\${{part_b.goals.saving_target_vs_mobile_aud|,}}）。
- **讀法與限制**：D = A\$36 是 A2 附錄 A 的兩平折扣額（試點整輪通話費 ÷ 本來就會買的人數），不是實際折扣（金額由財務提供），所以試點那一列的折扣段約等於試點通話費是定義使然；判斷用的是上一點的門檻，與 D 取多少無關；本來就會買的比例取自單一門檻名單對同門檻對照組（B-6，兩組不完全可比）；名單的通話段用同月配對名單（同圖 7）。這張圖只說明量級：要省錢，下一步要處理的是「誰該拿到優惠」（A2 第二步、「打電話不給優惠」組），而不只是把名單排得更準。
'''

MD['lat'] = r'''
### B-14 解讀：批次評分耗時（A2 表 8 可擴展性／延遲；硬體相依）

**結論：撥號前模型替整個測試集 {{part_b.scoring_latency.rows|,}} 人單執行緒批次評分，中位數 RF 約 {{part_b.scoring_latency.rf_median_s|.3f}} 秒、XGB 約 {{part_b.scoring_latency.xgb_median_s|.3f}} 秒。名單只需在外撥日前批次產生，不需即時評分，延遲不是瓶頸。**

- 這是建置本檔的電腦上量到的時間，換硬體就會不同，只當量級；不進十條判定，也不列入跨次執行的一致性比對。
- 正式的可擴展性要在 A2 表 9 階段 1（影子評分）以實際名單量測。
'''

MD['b34'] = r'''
<a id="b3-b4-summary" name="b3-b4-summary"></a>
## B3、B4 摘要（完整版見 PDF 報告第 3、4 節）

**B3｜未來改進、新增功能與新產品構想（只列優先序 1）**
- **改進**：補撥號前客戶特徵與外撥日期後重建，依 A2 表 7 以 XGB 進影子模式；分群公平修正（60 歲以上另設切點或分群校準）。
- **新增功能**：每位入選客戶附前三項入選原因（reason codes），給話務員與法遵，兌現 A2 表 8 的可解釋性承諾。
- **新產品**：「打電話不給優惠」組 —— 不依賴模型、下一輪即可做，量出優惠本身的效果；之後再發展成個人化折扣額度。

**B4｜放寬信用卡資格後，模型能否原封不動套用？**
- **(a) 不能**：訓練資料只含舊資格內被隨機外撥的客戶，新客戶落在訓練範圍外，分數、切點與評估證據都不能沿用，只能先影子評分（只記錄、不決定外撥）；何況模型連舊客群的階段 0 都未通過。
- **(b) 為什麼要調整**：資料漂移（輸入分布改變）、概念漂移（「特徵 → 接受」的關係改變）、評估證據斷層、分數未校準、商業前提改變（新客群的違約風險與用卡收益可能不同，接受不等於獲利）。
- **(b) 怎麼調整**：比對分布 → 影子評分 → 隨機抽樣外撥取得新標籤 → 分群驗證 → 重訓、校準、重選切點 → A/B 與核准後上線 → 監控；新版未勝出或上線後變差即回退舊版。
'''

MD['appendix_a'] = r'''
## 附錄 A：業務② 區間的穩健性檢查（看過第一次結果之後才加，不改判準）

判準是評估計畫原本訂的：同月配對名單 − 手機規則的差 > 0，且各月內 bootstrap（B = 1,000、種子 123）的 95% percentile 區間下限 > 0。下表的其他欄位都是看過第一次結果後才加的，只用來確認判定不是抽樣運氣；任何一欄都不改判準。數字與 B-3 第二張表相同。

| 名單（同月、{{part_b.b2.K_mobile_calls}} 通） | 差（pp） | 判準：percentile，B = 1,000 | basic，B = 1,000 | percentile，B = 5,000 | basic，B = 5,000 | 另外 10 個種子的 percentile 下限（B = 1,000） |
|---|---|---|---|---|---|---|
| RF（主） | {{part_b.b2.diff_pp|+.2f}} | [{{part_b.b2.ci_low_pp|+.2f}}, {{part_b.b2.ci_high_pp|+.2f}}] | [{{part_b.b2.basic_low_pp|+.2f}}, {{part_b.b2.basic_high_pp|+.2f}}] | [{{part_b.b2.b5k_ci_low_pp|+.2f}}, {{part_b.b2.b5k_ci_high_pp|+.2f}}] | [{{part_b.b2.b5k_basic_low_pp|+.2f}}, {{part_b.b2.b5k_basic_high_pp|+.2f}}] | {{part_b.b2.seed_low_min_pp|+.2f}} 到 {{part_b.b2.seed_low_max_pp|+.2f}}（{{part_b.b2.seed_n_above0}} 個 > 0） |
| RF ＋contact | {{part_b.b2.contact_diff_pp|+.2f}} | [{{part_b.b2.contact_ci_low_pp|+.2f}}, {{part_b.b2.contact_ci_high_pp|+.2f}}] | [{{part_b.b2.contact_basic_low_pp|+.2f}}, {{part_b.b2.contact_basic_high_pp|+.2f}}] | [{{part_b.b2.contact_b5k_ci_low_pp|+.2f}}, {{part_b.b2.contact_b5k_ci_high_pp|+.2f}}] | [{{part_b.b2.contact_b5k_basic_low_pp|+.2f}}, {{part_b.b2.contact_b5k_basic_high_pp|+.2f}}] | {{part_b.b2.contact_seed_low_min_pp|+.2f}} 到 {{part_b.b2.contact_seed_low_max_pp|+.2f}}（{{part_b.b2.contact_seed_n_above0}} 個 > 0） |
| XGB（表 7 勝出者） | {{part_b.b2.xgb.diff_pp|+.2f}} | [{{part_b.b2.xgb.ci_low_pp|+.2f}}, {{part_b.b2.xgb.ci_high_pp|+.2f}}] | [{{part_b.b2.xgb.basic_low_pp|+.2f}}, {{part_b.b2.xgb.basic_high_pp|+.2f}}] | [{{part_b.b2.xgb.b5k_ci_low_pp|+.2f}}, {{part_b.b2.xgb.b5k_ci_high_pp|+.2f}}] | [{{part_b.b2.xgb.b5k_basic_low_pp|+.2f}}, {{part_b.b2.xgb.b5k_basic_high_pp|+.2f}}] | {{part_b.b2.xgb.seed_low_min_pp|+.2f}} 到 {{part_b.b2.xgb.seed_low_max_pp|+.2f}}（{{part_b.b2.xgb.seed_n_above0}} 個 > 0） |

- **為什麼另報 basic 區間**：RF 名單的 bootstrap 平均 {{part_b.b2.boot_mean_pp|+.2f}} 高於點估計 {{part_b.b2.diff_pp|+.2f}}（重抽會複製高分成交者，分布往上偏），偏差校正的 basic 區間（2 × 點估計 − 上、下界）會往下移。RF 主名單不論用哪一種區間、B 用 1,000 或 5,000、換哪個種子，下限都 < 0，判定不變。
- **＋contact 與 XGB 處在邊界**：＋contact 在種子 123 的下限是 {{part_b.b2.contact_ci_low_pp|+.2f}}，另外 10 個種子中有 {{part_b.b2.contact_seed_n_above0}} 個 > 0；XGB 在種子 123 的下限恰好是 {{part_b.b2.xgb.ci_low_pp|+.2f}}，另外 10 個種子都沒有 > 0。依判準兩者都不算通過；就算採用某個下限 > 0 的種子，basic 區間的下限仍 < 0，同時期配對也為負 —— 不足以支持「名單比手機規則好」。
'''

MD['appendix'] = r'''
## 附錄：數字總表（KPI JSON）

下一格把本次執行中報告會引用的數字印成一個 JSON：上面 markdown 中的數字都由它填入，報告也引用它。`clustering` 一節因 KMeans 沒有 random_state，不列入跨次執行的一致性比對；`meta` 記錄套件版本、列數、選定的超參數、bootstrap 次數與兩條判準（業務②、A2 表 7）。
'''


# ----------------------------------------------------------------------------------------------------------------
# assemble
# ----------------------------------------------------------------------------------------------------------------
def build():
    nb = nbformat.read(str(OFFICIAL), as_version=4)          # read-only
    nb.metadata.pop('widgets', None)
    cells = nb.cells
    assert len(cells) == 77
    for c in cells:
        c.metadata = nbformat.from_dict({k: v for k, v in c.metadata.items() if k == 'id'})
        if c.cell_type == 'code':
            c.outputs = []
            c.execution_count = None
    edit_official(cells)
    # 官方 markdown 是簡體中文：只做字形轉換（OpenCC s2tw，台灣繁體），文字內容不改
    s2tw = opencc.OpenCC('s2tw')
    for c in cells:
        if c.cell_type == 'markdown':
            c['source'] = src_lines(s2tw.convert(''.join(c['source'])).replace('併為', '並為'))   # OpenCC 把連接詞「并為」誤轉成「併為」

    after = {
        0: [md(MD['intro'], 'a3-intro'), md(MD['part_a'], 'a3-part-a')],
        11: [code(A_INLINE, 'a3-inline-backend')],
        13: [code(A_GUARD, 'a3-na-check')],
        18: [code(A_EDA, 'a3-eda-numbers'), md(MD['eda'], 'a3-eda-read')],
        36: [code(A_TSNE, 'a3-tsne-numbers'), md(MD['tsne'], 'a3-tsne-read')],
        41: [code(A_UNI, 'a3-univariate'), md(MD['uni'], 'a3-univariate-read')],
        47: [code(A_MFS, 'a3-model-fs'), md(MD['mfs'], 'a3-model-fs-read')],
        51: [code(A_PROBA, 'a3-proba-auc'), code(A_XGB, 'a3-xgb-diag'), md(MD['proba'], 'a3-proba-auc-read')],
        59: [code(A_FINAL, 'a3-final-diag'), md(MD['final'], 'a3-final-read')],
        65: [code(A_SCORE, 'a3-scoring-diag'), md(MD['score'], 'a3-scoring-read')],
        66: [code(A_SEED, 'a3-kmeans-seed')],
        76: [code(A_CLUSTER, 'a3-cluster-profile'), md(MD['cluster'], 'a3-cluster-read'),
             # ---------------- Part B: appended after the last official cell ----------------
             md(MD['b_head'], 'b-head'), md(MD['b_summary'], 'b-summary'),
             code(B_SETUP, 'b0-setup'), md(MD['b0'], 'b0-read'),
             code(B_TRAIN, 'b1-train'), md(MD['b1'], 'b1-read'),
             code(B_SCORE, 'b2-ml-auc'), md(MD['b2'], 'b2-read'),
             code(B_FIG9, 'fig9', fig='fig9_auc_decomposition'), md(MD['f9'], 'fig9-read'),
             code(B_B2, 'b3-mobile-rule'), md(MD['b3'], 'b3-read'),
             code(B_FIG1, 'fig1', fig='fig1_gains'), md(MD['f1'], 'fig1-read'),
             code(B_B1, 'b4-cost'), md(MD['b4'], 'b4-read'),
             code(B_FIG2, 'fig2', fig='fig2_cost_vs_depth'), md(MD['f2'], 'fig2-read'),
             code(B_CM, 'b5-confusion'), code(B_FIG6, 'fig6', fig='fig6_confusion_matrix'), md(MD['b5'], 'b5-read'),
             code(B_B3, 'b6-uplift'), md(MD['b6'], 'b6-read'),
             code(B_FIG3, 'fig3', fig='fig3_uplift'), md(MD['f3'], 'fig3-read'),
             code(B_B5, 'b7-net-value'), md(MD['b7'], 'b7-read'),
             code(B_ERR, 'b8-error-costs'), md(MD['b_err'], 'b8-read'),
             code(B_ML4, 'b9-segments'), md(MD['b8'], 'b9-read'),
             code(B_FIG4, 'fig4', fig='fig4_segment_auc'), md(MD['f4'], 'fig4-read'),
             code(B_PERM, 'b10-perm'), md(MD['b9'], 'b10-read'),
             code(B_FIG5, 'fig5', fig='fig5_perm_importance'), md(MD['f5'], 'fig5-read'),
             md(MD['b10'], 'b10-ml5'),
             code(B_XGB, 'b11-xgb'), md(MD['xgb'], 'b11-read'),
             code(B_KPI, 'b12-kpi-table'), md(MD['b11'], 'b12-read'),
             code(B_GOALS, 'b13-goals'), code(B_FIG7, 'fig7', fig='fig7_round_cost'), md(MD['goals'], 'b13-read'),
             code(B_FIG8, 'fig8', fig='fig8_round_spend'), md(MD['f8'], 'fig8-read'),
             code(B_LAT, 'b14-latency'), md(MD['lat'], 'b14-read'),
             md(MD['concl'], 'b-conclusion'),
             md(MD['b34'], 'b3-b4-summary'),
             md(MD['appendix_a'], 'appendix-a'),
             md(MD['appendix'], 'appendix-head'), code(B_JSON, 'appendix-kpi-json')],
    }
    out = []
    for i, c in enumerate(cells):
        out.append(c)
        out.extend(after.get(i, []))
    nb.cells = out
    nb.metadata['kernelspec'] = {'name': KERNEL, 'display_name': 'Python 3 (a3venv)', 'language': 'python'}
    return nb


# ----------------------------------------------------------------------------------------------------------------
# execution
# ----------------------------------------------------------------------------------------------------------------
def ensure_kernel():
    assert os.path.normcase(os.path.realpath(sys.prefix)) == os.path.normcase(os.path.realpath(VENV)), \
        'run this script with the venv python: %s' % VENV_PY
    from jupyter_client.kernelspec import KernelSpecManager
    if KERNEL not in KernelSpecManager().find_kernel_specs():
        subprocess.run([str(VENV_PY), '-m', 'ipykernel', 'install', '--prefix', str(VENV), '--name', KERNEL,
                        '--display-name', 'Python 3 (a3venv)'], check=True)


def kernel_env(exec_dir):
    os.environ['TELEMARKETING_CSV'] = str(CSV)
    os.environ['YDATA_PROFILING_NO_ANALYTICS'] = '1'      # no usage analytics from the local run
    os.environ['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'
    os.environ['PIP_NO_INDEX'] = '1'                      # %pip may only confirm what is installed; never download
    # keep local absolute paths out of the outputs at the source (instead of rewriting outputs afterwards):
    os.environ['PIP_QUIET'] = '1'                         # %pip: no "Requirement already satisfied ... in <site-packages path>" lines
    os.environ['PYTHONWARNINGS'] = 'ignore:IProgress not found'   # tqdm warning that only appears without ipywidgets (not in Colab)
    os.environ['IPYKERNEL_CELL_NAME'] = '<ipython-input>'  # warnings show this cell name instead of a temp-file path
    exec_dir.mkdir(parents=True, exist_ok=True)


def probe(exec_dir):
    p = nbformat.v4.new_notebook()
    p.cells = [nbformat.v4.new_code_cell('import sys, os\nprint(sys.executable)\nprint(os.getcwd())')]
    NotebookClient(p, kernel_name=KERNEL, timeout=120, resources={'metadata': {'path': str(exec_dir)}}).execute()
    exe, cwd = p.cells[0].outputs[0]['text'].strip().splitlines()
    ok = os.path.normcase(os.path.realpath(exe)) == os.path.normcase(os.path.realpath(VENV_PY))
    print('[probe] kernel python is the venv python:', ok, '| cwd is exec dir:',
          os.path.normcase(os.path.realpath(cwd)) == os.path.normcase(os.path.realpath(exec_dir)))
    assert ok, 'kernel a3venv does not run the venv python'


def execute(nb, exec_dir):
    client = NotebookClient(nb, kernel_name=KERNEL, timeout=1800, record_timing=True, allow_errors=False,
                            resources={'metadata': {'path': str(exec_dir)}})
    t0 = time.time()
    client.execute()
    return time.time() - t0


def extract_kpi_text(nb):
    """the exact text the notebook printed between the two markers (without the line breaks next to the markers)"""
    for c in reversed(nb.cells):
        if c.cell_type == 'code':
            txt = ''.join(o.get('text', '') for o in c.get('outputs', []) if o.get('output_type') == 'stream')
            if BEGIN in txt:
                return txt.split(BEGIN, 1)[1].split(END, 1)[0].strip('\n')
    raise RuntimeError('KPI JSON markers not found')


def extract_kpi(nb):
    return json.loads(extract_kpi_text(nb))


def part_timings(nb):
    """seconds per part from nbclient's execution timestamps; the timestamps are removed afterwards"""
    from datetime import datetime
    tot = {'part_a': 0.0, 'part_b': 0.0}
    part = 'part_a'
    slow = []
    for c in nb.cells:
        if c.metadata.get('id') == 'b-head':
            part = 'part_b'
        ex = c.metadata.pop('execution', None)
        if ex and 'iopub.execute_input' in ex and 'shell.execute_reply' in ex:
            t = lambda k: datetime.fromisoformat(ex[k].replace('Z', '+00:00'))
            secs = (t('shell.execute_reply') - t('iopub.execute_input')).total_seconds()
            tot[part] += secs
            slow.append((round(secs, 1), c.metadata.get('id')))
    return {k: round(v, 1) for k, v in tot.items()}, sorted(slow, reverse=True)[:8]


def count_errors(nb):
    return sum(1 for c in nb.cells if c.cell_type == 'code' for o in c.get('outputs', []) if o.get('output_type') == 'error')


# ----------------------------------------------------------------------------------------------------------------
# post-processing
# ----------------------------------------------------------------------------------------------------------------
def path_variants(p):
    s = str(p)
    return {s, s.replace('\\', '/'), s.replace('\\', '\\\\')}


def make_scrubber(exec_dir):
    reps = []
    for p, ph in [(VENV, '<venv>'), (CSV, 'TeleMarketing.csv'), (exec_dir, '.'), (ML_ROOT, '<project>'), (HERE, '<project>')]:
        for v in path_variants(p):
            reps.append((v, ph))
    reps.sort(key=lambda t: -len(t[0]))
    kernel_tmp = re.compile(r'(?i)[a-z]:[\\/]+users[\\/]+[^\\/]+[\\/]+appdata[\\/]+local[\\/]+temp[\\/]+ipykernel_\d+[\\/]+\d+\.py')
    generic = re.compile(r'(?i)[a-z]:[\\/]+(?:users|kennycode)[\\/][^\s\'"<>]*')
    counter = {'n': 0}

    def scrub(s):        # safety net only: kernel_env() keeps paths out of the outputs, so this should change nothing
        s0 = s
        for v, ph in reps:
            s = re.sub(re.escape(v), lambda m: ph, s, flags=re.I)
        s = kernel_tmp.sub('<ipython-input>', s)
        s = generic.sub('<local-path>', s)
        counter['n'] += s != s0
        return s
    scrub.counter = counter
    return scrub


def scrub_outputs(nb, scrub):
    for c in nb.cells:
        if c.cell_type != 'code':
            continue
        for o in c.get('outputs', []):
            if 'text' in o:
                o['text'] = scrub(o['text'])
            if 'traceback' in o:
                o['traceback'] = [scrub(t) for t in o['traceback']]
            for mime, val in list(o.get('data', {}).items()):
                if mime.startswith('text/') or mime.endswith('json') and isinstance(val, str):
                    o['data'][mime] = scrub(val) if isinstance(val, str) else val


def leftover_paths(nb):
    bad = re.compile(r'(?i)([a-z]:[\\/]+users[\\/]|[a-z]:[\\/]+kennycode|appdata[\\/]+local)')
    hits = []

    def walk(x, where):
        if isinstance(x, str):
            if bad.search(x):
                hits.append((where, bad.search(x).group(0)))
        elif isinstance(x, dict):
            for k, v in x.items():
                if k != 'image/png':
                    walk(v, where)
        elif isinstance(x, list):
            for v in x:
                walk(v, where)
    for i, c in enumerate(nb.cells):
        walk(c.get('outputs', []), 'outputs of cell %d' % i)
        walk(c.get('source', ''), 'source of cell %d' % i)
    walk(nb.metadata, 'metadata')
    return hits


TOKEN = re.compile(r'\{\{([^{}|]+)(?:\|([^{}]*))?\}\}')


def lookup(d, path):
    for p in path.split('.'):
        d = d[int(p)] if isinstance(d, list) else d[p]
    return d


def fmt(v, spec, path=''):
    if spec and spec.startswith('abs'):          # {{x|abs.2f}}: absolute value (the sign is written in the text as −A$)
        v, spec = abs(v), spec[3:]
    if not spec and isinstance(v, float):        # default display: AUC 4 decimals, money and pp 2 decimals
        leaf = path.lower()
        if 'auc' in leaf:
            spec = '.4f'
        elif any(t in leaf for t in ('cost', 'aud', '_pp')):
            spec = '.2f'
    if spec:
        return format(v, spec)
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return format(v, ',')
    return str(v)


def fill_markdown(nb, kpi, extra=None):
    """fills {{path|fmt}} from the notebook's own KPI JSON; `extra` only carries the measured run time ({{run.minutes}})"""
    src = {**kpi, **(extra or {})}
    missing = []
    for c in nb.cells:
        if c.cell_type == 'markdown' and '{{' in c.source:
            def rep(m):
                try:
                    return fmt(lookup(src, m.group(1)), m.group(2), m.group(1))
                except (KeyError, IndexError, TypeError, ValueError):
                    missing.append(m.group(1))
                    return m.group(0)
            c.source = TOKEN.sub(rep, c.source)
    assert not missing, ('placeholders not found in KPI JSON', missing)


def check_claims(kpi):
    """every qualitative statement written in the markdown is checked against the run's own numbers;
    returns the list of statements that the numbers do not support"""
    A, B = kpi['part_a'], kpi['part_b']
    C = kpi.get('clustering', {})
    seg = {(r['dimension'], r['group']): r for r in B['ml4']['segments']}
    fp, mc, xd, ml, b2, b1, b34, b5, g = (A['final_pipeline'], A['model_compare'], A['xgb_diag'], B['ml'], B['b2'], B['b1'],
                                          B['b3b4'], B['b5'], B['ml4']['gaps'])
    eda, mfs, er, go, cm, xe, t7 = A['eda'], A['model_fs'], B['errors'], B['goals'], B['confusion'], B['xgb_eval'], B['models']['table7_rule']
    sweep = fp['depth_sweep']
    perm = B['perm_importance']
    job = eda['cat_conv_pct']['job']
    p2, x2 = b2['period'], b2['xgb']
    d34, r34 = b34['dedup'], b34['raw']
    sc = A['scoring']
    ps = B['a2_recomputed']['prev_success_share_pct']
    sp, rs, rnd = go['spillover_discount_per_round_D36_aud'], go['round_spend_D36'], B['b1']['one_round_extrapolation']

    def inc0(lo, hi):
        return lo <= 0 <= hi

    claims = {
        # Part A
        'EDA: duration = 0 <=> control group': eda['duration0_pct']['0'] == 100.0 and eda['target_duration0_rows'] == 0,
        'EDA: busiest month (may) has the lowest conversion':
            min(eda['target_month_conv_pct'], key=eda['target_month_conv_pct'].get) == 'may'
            and max(eda['target_month_rows'], key=eda['target_month_rows'].get) == 'may',
        'EDA: dedup control vs target nearly equal': abs(eda['conv_pct']['0'] - eda['conv_pct']['1']) < 0.5,
        'EDA: base rate about 1 in 8': 11 <= eda['base_conv_pct'] <= 14,
        'EDA: student and retired highest, blue-collar lowest job':
            set(sorted(job, key=job.get, reverse=True)[:2]) == {'student', 'retired'} and min(job, key=job.get) == 'blue-collar',
        'EDA: default unknown below default no': eda['cat_conv_pct']['default']['unknown'] < eda['cat_conv_pct']['default']['no'],
        'EDA: housing / loan / day-of-week gaps small (< 3 pp)':
            all(eda['cat_conv_range_n500'][c][1] - eda['cat_conv_range_n500'][c][0] < 3 for c in ('housing', 'loan'))
            and eda['dow_conv_range'][1] - eda['dow_conv_range'][0] < 3,
        'EDA: mean age close for yes / no': abs(eda['mean_by_y']['age']['yes'] - eda['mean_by_y']['age']['no']) < 2,
        't-SNE: neighbours mostly same group, outcome barely above random':
            A['tsne']['knn_same_group_pct'] >= A['tsne']['knn_same_group_random_pct'] + 25
            and A['tsne']['knn_same_outcome_pct'] - A['tsne']['knn_same_outcome_random_pct'] < 10,
        't-SNE: power transform reduces skew': abs(A['tsne']['duration_tfm_skew_train']) < abs(A['tsne']['duration_skew_train']),
        'univariate: poutcome_success first in both':
            A['univariate']['f_classif_top10'][0] == 'poutcome_success' == A['univariate']['chi2_top10'][0],
        'univariate: scheduling counts are month_oct / month_oct+month_mar':
            [f for f in A['univariate']['f_classif_top10'] if f.startswith('month')] == ['month_oct']
            and sorted(f for f in A['univariate']['chi2_top10'] if f.startswith('month')) == ['month_mar', 'month_oct'],
        'univariate: chi2 picks job_retired and job_student': {'job_retired', 'job_student'} <= set(A['univariate']['chi2_top10']),
        'model FS: only poutcome_success in all four': mfs['in_all_four'] == ['poutcome_success'],
        'model FS: LR mostly group flags, one pre-call (poutcome_success)':
            mfs['tag_counts']['LR_RFE'].get('group_flag', 0) >= 4 and mfs['tag_counts']['LR_RFE'].get('pre_call', 0) == 1
            and 'poutcome_success' in mfs['lr_rfe'],
        'model FS: RF has two duration columns': mfs['tag_counts']['RF_RFE'].get('post_call', 0) == 2,
        'model FS: top RF pair is duration_tfm ~ month_int (|r| > 0.7); duration twins also highly correlated (> 0.7)':
            'duration_tfm' in mfs['rf_max_pair_text'] and 'month_int' in mfs['rf_max_pair_text'] and mfs['rf_max_pair_abs_r'] > 0.7
            and (mfs['rf_dur_pair_abs_r'] or 0) > 0.7,
        'model FS: flags barely correlated with response (< 0.02)': mfs['lr_flag_max_abs_corr_with_response'] < 0.02,
        'model FS: flags exactly collinear (campaign_0/1, campaign_int, contact & day_of_week NA)':
            all(mfs['collinear'][k] for k in ['campaign_0 + campaign_1 = 1', 'campaign_int = campaign_1',
                                              'contact_Not Applicable = campaign_0', 'day_of_week_Not Applicable = campaign_0']),
        'model FS: flag coefficients large (|coef| > 1); duration_tfm has the largest |coef|':
            mfs['lr_flag_coef_abs_max'] > 1 and mfs['lr_coef_top_text'].startswith('duration_tfm +'),
        'model FS: control duration_tfm is one constant below the target minimum':
            mfs['control_duration_tfm_constant'] and mfs['control_duration_tfm'] < mfs['target_duration_tfm_min'],
        'model FS control 1: C = 1 selects exactly the same columns': mfs['lr_ctl_c1_same'],
        'model FS control 2: no group flag once duration is removed': mfs['lr_ctl_nodur_flags'] == 0
            and set(mfs['lr_ctl_nodur_tags']) <= {'scheduling', 'pre_call'},
        'proba: official XGB predicts yes for everyone':
            mc['share_predicted_yes_pct']['gb'] == 100.0 and xd['official_share_yes_pct'] == 100.0,
        'proba: XGB with the actual ratio beats RF on CV and test': xd['xgb_minus_rf_cv'] > 0 and xd['xgb_minus_rf_test'] > 0,
        'proba: subsample / colsample = 1.0 still predicts mostly yes (>= 90%)': xd['subcol1_share_yes_pct'] >= 90,
        'proba: learning_rate 0.1 lowers the yes share more than subsample / colsample':
            xd['lr01_share_yes_pct'] < xd['subcol1_share_yes_pct'],
        'proba: cell-26 refit negligible (< 0.005 AUC) and train-fit higher': 0 < mc['rf_auc_trainfit_minus_asrun'] < 0.005,
        'final: CV improves 3 < 5 < 9': fp['cv_auc_by_depth']['3'] < fp['cv_auc_by_depth']['5'] < fp['cv_auc_by_depth']['9'],
        'final: 300 trees best, < 0.001 above 100':
            max(fp['cv_auc_by_n_estimators_at_best'], key=fp['cv_auc_by_n_estimators_at_best'].get) == '300'
            and fp['cv_auc_by_n_estimators_at_best']['300'] - fp['cv_auc_by_n_estimators_at_best']['100'] < 0.001,
        'final: depth 9 is the CV peak, 11 lower and gap > 0.05':
            sweep[1]['cv_auc'] > sweep[0]['cv_auc'] and sweep[1]['cv_auc'] > sweep[2]['cv_auc'] and sweep[2]['train_minus_test'] > 0.05,
        'final: sweep depth 9 reproduces the grid CV': abs(sweep[1]['cv_auc'] - fp['best_cv_auc']) < 1e-4,
        'final: gap <= 0.05 and AUC >= 0.80': fp['gap_train_minus_test'] <= 0.05 and fp['auc_test'] >= 0.80,
        'final: no group columns among RFE': fp['rfe_has_group_columns'] == [],
        'final: CV lower than test': fp['cv_minus_test'] < 0,
        'final: RFE selection bias about one thousandth (0 < non-nested - nested < 0.003)':
            0 < fp['rfe_bias']['nonnested_minus_nested'] < 0.003,
        'final: target-only AUC > control-only AUC': fp['auc_test_target_only'] > fp['auc_test_control_only'],
        'scoring: switching campaign changes nothing':
            sc['spearman_official_vs_switched'] == 1.0 and sc['top20_overlap'] == 20,
        'scoring: unseen combinations have 0 training rows':
            sc['train_rows_campaign1_duration0'] == 0 and sc['train_rows_campaign0_duration_pos'] == 0,
        'scoring: official cost overstates short calls and understates long calls':
            sc['official_cost_aud_at_D36']['1'] > sc['bucket_call_cost_aud']['1'] and sc['crossover_bucket'] is not None
            and sc['bucket_call_cost_aud']['10'] > sc['official_cost_aud_at_D36']['10'] and sc['bucket10_understate_x'] > 1,
        # Part B
        'B0: removed rows almost all control': B['a2_recomputed']['removed_target'] < 20,
        'B0: dedup brings the groups closer in previous-success share but they still differ':
            abs(ps['dedup_target'] - ps['dedup_control']) < abs(ps['raw_target'] - ps['raw_control'])
            and abs(ps['dedup_target'] - ps['dedup_control']) > 0.2,
        'B1: selected config is also the best CV': B['models']['main_selected'] == B['models']['main_best_cv_overall'],
        'B1: exactly one config rejected by the gap rule': len(B['models']['main_rejected_by_gap']) == 1,
        'B1: A2 table 7 rule: XGB ahead on all 5 folds and all 5 seeds, margin far above the RF seed range (> 3x)':
            t7['replace'] and t7['xgb_ahead_every_seed'] and B['models']['xgb_folds_better'] == 5
            and t7['margin_mean'] > 3 * t7['rf_seed_range'] and t7['margin_min'] > 0,
        'B11: XGB has the same ten judgements as RF': xe['same_judgement_as_rf'] and xe['judgement'] == B['kpi_judgement'],
        'B11: XGB higher AUC; within-period < 0.6; dedup uplift negative; stratified CIs include 0; cost above target':
            ml['xgb_test_auc'] > ml['ml2_test_auc'] and ml['xgb_within_period_auc'] < 0.6 and xe['b3b4_dedup']['uplift_pp'] < 0
            and inc0(xe['b3b4_dedup']['period_stratified_ci_low_pp'], xe['b3b4_dedup']['period_stratified_ci_high_pp'])
            and inc0(xe['b3b4_raw']['period_stratified_ci_low_pp'], xe['b3b4_raw']['period_stratified_ci_high_pp'])
            and xe['cost_formula'] > b1['target'] and all(v['net_D_per_call_excl_call_cost'] < 0 for v in xe['b5'].values()),
        'B11/B9: XGB segment gaps: age and month fail, marital passes':
            xe['ml4_gaps']['age_band'] > 0.05 and xe['ml4_gaps']['marital'] <= 0.05 and xe['ml4_gaps']['month'] > 0.05,
        'B2/B3: XGB month list not passing: lower bound <= 0 (displayed as +0.00), no other seed above 0, period negative':
            (not x2['pass']) and x2['diff_pp'] > 0 and x2['ci_low_pp'] <= 0 and abs(x2['ci_low_pp']) < 0.005
            and x2['seed_n_above0'] == 0 and x2['period_diff_pp'] < 0 and x2['basic_low_pp'] < 0 and ml['xgb_gap'] <= 0.05,
        'ML: LR below 0.75, RF above': ml['ml2_lr_test_auc'] < 0.75 <= ml['ml2_test_auc'],
        'ML: within-month AUC below 0.75; within-period near random (< 0.6)':
            ml['ml2_within_month_auc'] < 0.75 and ml['ml2_within_period_auc'] < 0.6,
        'ML: 2-3 (cpi, cci) periods per month': ml['periods_per_month_min'] == 2 and ml['periods_per_month_max'] == 3,
        'ML1: most of the PoC advantage is duration (controlled gain > 0.1)':
            ml['duration_gain_controlled'] > 0.1 and ml['poc_minus_controlled_other'] < ml['duration_gain_controlled'],
        'ML3: both gaps <= 0.05': ml['ml1_poc_gap'] <= 0.05 and ml['ml3_precall_gap'] <= 0.05,
        'B2 month: diff > 0, plan CI and all check CIs include 0, gate not passed':
            b2['diff_pp'] > 0 and inc0(b2['ci_low_pp'], b2['ci_high_pp']) and inc0(b2['basic_low_pp'], b2['basic_high_pp'])
            and inc0(b2['b5k_ci_low_pp'], b2['b5k_ci_high_pp']) and inc0(b2['b5k_basic_low_pp'], b2['b5k_basic_high_pp']) and not b2['pass'],
        'B2 month: bootstrap mean above the point estimate': b2['boot_mean_pp'] > b2['diff_pp'],
        'B2 month: all extra seeds keep the lower bound below 0': b2['seed_low_max_pp'] < 0 and b2['seed_n_above0'] == 0,
        'B2 period: list below the mobile rule; CI includes 0': p2['diff_pp'] < 0 and inc0(p2['ci_low_pp'], p2['ci_high_pp']),
        'B2 +contact: wider gap, borderline (some seeds above 0), not passed, basic lows < 0':
            b2['contact_diff_pp'] > b2['diff_pp'] and b2['contact_borderline'] and not b2['contact_pass']
            and b2['contact_seed_n_above0'] >= 1 and b2['contact_basic_low_pp'] < 0 and b2['contact_b5k_basic_low_pp'] < 0,
        'B2: pooled top-K above the mobile rule': b2['pooled_minus_mobile_pp'] > 0.5,
        'B2: mobile advantage mostly period mix':
            b2['within_period_mobile_advantage_pp'] < b2['within_month_mobile_advantage_pp']
            and b2['within_period_mobile_advantage_pp'] < b2['month_share_of_mobile_advantage_pp'] + b2['period_extra_over_month_pp'],
        'Fig1: period curve captures less at 20% and 50%':
            b1['curve_period'][3]['captured_pct'] < b1['curve'][3]['captured_pct']
            and b1['curve_period'][9]['captured_pct'] < b1['curve'][9]['captured_pct'],
        'Fig1: mobile-rule and month-matched list capture almost the same share (within 2 pp)':
            abs(b2['ml_captured_pct'] - b2['mobile_captured_pct']) < 2,
        'Fig1: all three list bars touch or cross the dashed line (CI lows <= 0)':
            b2['ci_low_pp'] <= 0 and p2['ci_low_pp'] <= 0 and x2['ci_low_pp'] <= 0,
        'B1: ML cost above target, below random': b1['ml_cost_formula'] > b1['target'] and b1['random_minus_ml'] > 0,
        'B1: period-matched needs a much shallower list':
            b1['deepest_ok_depth_period_pct'] is not None and b1['deepest_ok_depth_period_pct'] < b1['deepest_ok_depth_pct']
            and b1['curve_period'][9]['cost_formula'] > b1['target'],
        'B1: 50% depth noise range straddles the target': b1['depth50_cost_low'] < b1['target'] < b1['depth50_cost_high'],
        'B1: actual-seconds line below the formula line': all(r['cost_actual'] <= r['cost_formula'] for r in b1['curve']),
        'Fig2: period cost line above the month line (depth < 100%)':
            all(p['cost_formula'] > m['cost_formula'] for p, m in zip(b1['curve_period'][:-1], b1['curve'][:-1])),
        'confusion: month-matched recall comparable to the mobile rule (within 2 pp)':
            abs(cm['month_matched']['recall_pct'] - cm['mobile_recall_pct']) < 2,
        'confusion: pooled precision above month-matched': cm['pooled_minus_month_precision_pp'] > 0,
        'B3: dedup CI includes 0, raw CI above 0':
            inc0(d34['uplift_ci_low_pp'], d34['uplift_ci_high_pp']) and r34['uplift_ci_low_pp'] > 0,
        'B3: raw uplift about +4 pp; period composition takes most of it; dedup handling still moves the stratified value by > 1 pp':
            3.5 <= r34['uplift_pp'] <= 4.5 and b34['raw_minus_raw_strat_pp'] > r34['uplift_pp'] / 2
            and b34['strat_raw_minus_dedup_pp'] > 1,
        'B3: both period-stratified uplifts within +/- 1 pp, both CIs include 0 and overlap':
            abs(d34['period_stratified_uplift_pp']) <= 1 and abs(r34['period_stratified_uplift_pp']) <= 1
            and inc0(d34['period_stratified_ci_low_pp'], d34['period_stratified_ci_high_pp'])
            and inc0(r34['period_stratified_ci_low_pp'], r34['period_stratified_ci_high_pp'])
            and min(d34['period_stratified_ci_high_pp'], r34['period_stratified_ci_high_pp'])
            > max(d34['period_stratified_ci_low_pp'], r34['period_stratified_ci_low_pp']),
        'B3/B-3 text: CI of the month difference spans a loss and a gain in sales (low < 0 < high)':
            b2['ci_low_sales'] < 0 < b2['ci_high_sales'],
        'final: dense RFE columns differ from the official sparse run (as written)': not fp['rfe_bias']['same_columns_as_official'],
        'B4: raw would-buy share close to the pilot (within 3 pp); both CIs above 50%':
            abs(r34['would_buy_share_pct'] - B['a2_recomputed']['pilot_would_buy_share_pct']) < 3
            and d34['would_buy_ci_low_pct'] > 50 and r34['would_buy_ci_low_pct'] > 50,
        'B5: all net values negative; ML list more negative than random; no break-even D':
            all(v['net_D_per_call_excl_call_cost'] < 0 and v['break_even_D'] is None for v in b5.values())
            and b5['dedup_ml_list']['net_D_per_call_excl_call_cost'] < b5['dedup_random']['net_D_per_call_excl_call_cost']
            and b5['raw_ml_list']['net_D_per_call_excl_call_cost'] < b5['raw_random']['net_D_per_call_excl_call_cost'],
        'errors: dedup below-threshold difference significantly negative; raw CI includes 0':
            er['dedup']['below_uplift_ci_high_pp'] < 0 and inc0(er['raw']['below_uplift_ci_low_pp'], er['raw']['below_uplift_ci_high_pp']),
        'errors: missed-incremental not estimable in dedup (upper bound 0), estimable in raw':
            er['dedup']['n_missed_incremental'] is None and er['dedup']['n_missed_upper'] == 0
            and er['raw']['n_missed_incremental'] is not None,
        'errors: per person 1 > 2 > 3 at D = 36; 2 > 3 needs D > ~A$10':
            er['dedup']['unit_cost_at_D36'][0] > er['dedup']['unit_cost_at_D36'][1] > er['dedup']['unit_cost_at_D36'][2]
            and 9 < er['D_where_2_exceeds_3'] < 11,
        'errors: largest total = error 1 at D = 36 and 100 (both); at D = 10 dedup 1, raw 3':
            all(er[v]['by_D'][d]['largest'] == '1' for v in ('dedup', 'raw') for d in ('36', '100'))
            and er['dedup']['by_D']['10']['largest'] == '1' and er['raw']['by_D']['10']['largest'] == '3',
        'ML4: age and month fail, marital passes': (not g['age_band']['pass']) and g['marital']['pass'] and (not g['month']['pass']),
        'ML4: young and old selected more than 40-59 (both lists); pooled amplifies':
            all(min(seg[('age_band', '<30')][c], seg[('age_band', '60+')][c])
                > max(seg[('age_band', '40-49')][c], seg[('age_band', '50-59')][c]) for c in ('selected_pct', 'selected_pct_pooled'))
            and seg[('age_band', '60+')]['selected_pct_pooled'] > seg[('age_band', '60+')]['selected_pct']
            and seg[('age_band', '<30')]['selected_pct_pooled'] > seg[('age_band', '<30')]['selected_pct'],
        'ML4: small groups have CI wider than 0.05':
            all(seg[k]['ci_high'] - seg[k]['ci_low'] > 0.05 for k in [('month', 'mar'), ('month', 'oct'), ('age_band', '60+')]),
        'perm: top 3 are cci, cpi, poutcome; rest < 0.01; marital ~ 0':
            B['perm_importance_rank'][:3] == ['cons.conf.idx', 'cons.price.idx', 'poutcome']
            and all(perm[k.replace('.', '_')]['mean_auc_drop'] < 0.01 for k in B['perm_importance_rank'][3:])
            and abs(perm['marital']['mean_auc_drop']) < 0.002,
        'drop: removing age / marital changes AUC by < 0.005': all(abs(v['change']) < 0.005 for v in B['drop_retrain'].values()),
        'KPI: business rows none pass; ML1 and ML3 pass':
            B['kpi_business_pass'] == 0 and B['kpi_judgement']['ml1'] == B['kpi_judgement']['ml3'] == '達標',
        'KPI: judgements as written in the text': B['kpi_judgement'] == {
            'b1': '未達', 'b2': '未證實', 'b3': '未證實', 'b4': '未達', 'b5': '示算',
            'ml1': '達標', 'ml2': '未證實', 'ml3': '達標', 'ml4': '未達', 'ml5': '不可離線驗'},
        'goals: saving vs mobile small (< A$1,000), below the A2 saving target, fewer calls below target':
            go['saving_ml_vs_mobile_aud'] < 1000 and go['saving_ml_share_of_target_pct'] < 100
            and go['fewer_calls_ml_pct'] < go['fewer_calls_target_pct'],
        'goals: revenue multiple higher for the ML list than the pilot':
            go['multiple_ml_raw'] is not None and go['multiple_ml_dedup'] is not None
            and go['multiple_pilot'] < go['multiple_ml_raw'] < go['multiple_ml_dedup'],
        'goals: no objective reached': all(v != '達標' for v in go['judgement'].values()),
        # hd revision (B-13 money view, Fig 8, Fig 9, B-14)
        'goals: raw revenue multiple close to the pilot (within 1)': abs(go['multiple_ml_raw'] - go['multiple_pilot']) < 1,
        'goals: month mix alone saves vs the pilot; list vs month-mix random below list vs pilot and < 60% of target; mobile vs month-mix random below the list':
            go['saving_random_mm_vs_pilot_aud'] > 0 and go['saving_ml_vs_random_mm_aud'] < go['saving_ml_vs_pilot_aud']
            and go['saving_ml_vs_random_mm_share_of_target_pct'] < 60
            and 0 < go['saving_mobile_vs_random_mm_aud'] < go['saving_ml_vs_random_mm_aud'],
        'goals: even at the A2 target the extra saving vs the mobile rule is small (A$480 < x < A$5,000)':
            go['saving_ml_vs_mobile_aud'] < go['saving_target_vs_mobile_aud'] < 5000,
        'Fig8: would-buy discount per round >= 90% of the round call cost (pilot, list); raw within 5% of the pilot; dedup above raw':
            sp['pilot'] >= 0.9 * go['pilot_call_cost_aud'] and sp['raw'] >= 0.9 * rnd['ml_list']['call_cost']
            and abs(sp['raw'] - sp['pilot']) <= 0.05 * sp['pilot'] and sp['dedup'] > sp['raw'],
        'Fig8: D at which the would-buy discount exceeds the most the list could save is small (< A$5)':
            all(v < 5 for v in go['D_spill_exceeds_target_vs_mobile_saving_aud'].values()),
        'Fig8: list cuts the unconverted-call part; call parts add up to the round call cost (within A$2)':
            rs['ml_list_raw_share']['unconverted_calls_aud'] < rs['pilot']['unconverted_calls_aud']
            and abs(rs['ml_list_raw_share']['unconverted_calls_aud'] + rs['ml_list_raw_share']['converted_calls_aud'] - rnd['ml_list']['call_cost']) <= 2
            and abs(rs['pilot']['unconverted_calls_aud'] + rs['pilot']['converted_calls_aud'] - go['pilot_call_cost_aud']) <= 2,
        'Fig9: PoC > pre-call > within month > within period; only the first two >= 0.75; within period < 0.6':
            ml['ml1_poc_test_auc'] > ml['ml2_test_auc'] > ml['ml2_within_month_auc'] > ml['ml2_within_period_auc']
            and ml['ml2_test_auc'] >= 0.75 > ml['ml2_within_month_auc'] and ml['ml2_within_period_auc'] < 0.6,
        'B14: batch scoring of the whole test set well under 5 s (RF and XGB)':
            B['scoring_latency']['rf_median_s'] < 5 and B['scoring_latency']['xgb_median_s'] < 5,
    }
    if C:
        prof, ov = C['profile'], C['overall']
        claims['clustering: top cluster all target with long calls'] = (prof['rank1']['target_share_pct'] == 100.0
                                                                         and prof['rank1']['mean_duration'] > 500)
        claims['clustering: rank 2 is a different period (cci differs by > 3)'] = abs(prof['rank2']['mean_cci'] - ov['mean_cci']) > 3
        claims['clustering: rank 2 has a much higher previous-success share'] = prof['rank2']['prev_success_pct'] > 2 * ov['prev_success_pct']
        claims['clustering: rank 1 converters rarely previous-success'] = prof['rank1']['yes_prev_success_pct'] < ov['yes_prev_success_pct']
        claims['clustering: rank 2 rarely default unknown'] = prof['rank2']['default_unknown_pct'] < ov['default_unknown_pct'] / 3
        claims['clustering: ranks 3 and 7 older, more married, low conversion'] = all(
            prof[r]['mean_age'] > ov['mean_age'] + 8 and prof[r]['married_pct'] > ov['married_pct'] + 8 and prof[r]['conv_pct'] < 15
            for r in ('rank3', 'rank7'))
        hs = [r['housing_yes_pct'] for r in prof.values()]
        claims['clustering: housing share similar across clusters (range < 15 pp)'] = max(hs) - min(hs) < 15
        claims['clustering: inertia falls overall'] = C['elbow_inertia']['19'] < C['elbow_inertia']['1'] / 2
        claims['clustering: elbow leaves out the two duration columns'] = (len(C['elbow_left_out']) == 2
                                                                            and all('duration' in c for c in C['elbow_left_out']))
    return [k for k, ok in claims.items() if not ok]


def extract_figs(nb):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for c in nb.cells:
        tag = c.metadata.get('a3_fig')
        if not tag:
            continue
        pngs = [o['data']['image/png'] for o in c.get('outputs', [])
                if o.get('output_type') in ('display_data', 'execute_result') and 'image/png' in o.get('data', {})]
        assert len(pngs) == 1, (tag, len(pngs))
        p = FIG_DIR / ('%s.png' % tag)
        p.write_bytes(base64.b64decode(pngs[0]))
        written.append(str(p))
    return written


def diff_paths(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b), key=str):
            out += diff_paths(a.get(k), b.get(k), '%s.%s' % (path, k) if path else str(k))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff_paths(x, y, '%s.%d' % (path, i))
        return out
    return [] if a == b else ['%s: %r -> %r' % (path, a, b)]


def strip_clustering(k):
    # clustering: KMeans has no random_state in the official cells; scoring_latency: wall-clock time (hardware-dependent)
    k = copy.deepcopy(k)
    k.pop('clustering', None)
    k.get('part_b', {}).pop('scoring_latency', None)
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=int, default=2)
    ap.add_argument('--exec-dir', default=str(DEFAULT_EXEC_DIR))
    a = ap.parse_args()
    exec_dir = Path(a.exec_dir)

    ensure_kernel()
    kernel_env(exec_dir)
    probe(exec_dir)

    base = build()
    nbformat.validate(base)
    kpis, nb_run, times = [], None, []
    for r in range(a.runs):
        nb_run = copy.deepcopy(base)
        secs = execute(nb_run, exec_dir)
        parts, slow = part_timings(nb_run)
        times.append({'total': round(secs, 1), **parts})
        kpis.append(extract_kpi(nb_run))
        (exec_dir / ('kpi_run%d.json' % (r + 1))).write_text(json.dumps(kpis[-1], ensure_ascii=False, indent=1), encoding='utf-8')
        print('[run %d] %.1f s (part A %.1f s, part B %.1f s), error outputs: %d'
              % (r + 1, secs, parts['part_a'], parts['part_b'], count_errors(nb_run)))
        print('        slowest cells:', slow)
    deterministic = all(strip_clustering(k) == strip_clustering(kpis[0]) for k in kpis[1:])
    if a.runs > 1:
        print('[determinism] KPI JSON identical across %d runs (clustering excluded): %s' % (a.runs, deterministic))
        if not deterministic:
            for path in diff_paths(strip_clustering(kpis[0]), strip_clustering(kpis[-1]))[:25]:
                print('   differs:', path)
    kpi = kpis[-1]

    nb_run.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
    nb_run.metadata.pop('widgets', None)
    scrubber = make_scrubber(exec_dir)
    scrub_outputs(nb_run, scrubber)
    print('[scrub] outputs changed by the safety-net scrubber:', scrubber.counter['n'], '(expected 0: paths are not printed at all)')
    fill_markdown(nb_run, kpi, extra={'run': {'minutes': '%.0f' % max(1, round(times[-1]['total'] / 60))}})
    problems = check_claims(kpi)
    hits = leftover_paths(nb_run)
    nbformat.validate(nb_run)
    nbformat.write(nb_run, str(OUT_NB))
    # a3_kpi_results.json = the exact text the saved notebook printed between the markers (UTF-8, LF line ends)
    kpi_text = extract_kpi_text(nbformat.read(str(OUT_NB), as_version=4))
    assert json.loads(kpi_text) == kpi
    OUT_JSON.write_bytes((kpi_text + '\n').encode('utf-8'))
    assert OUT_JSON.read_bytes().decode('utf-8').rstrip('\n') == kpi_text
    figs = extract_figs(nb_run)
    print('[write]', OUT_NB.name, OUT_JSON.name, [Path(f).name for f in figs], '| JSON file = printed block byte for byte')
    print('[runtime s]', times, '| errors in last run:', count_errors(nb_run), '| deterministic:', deterministic)
    print('[local paths left in notebook]', hits[:5] if hits else 'none')
    print('[claim check problems]', problems if problems else 'none')
    summary = {'runtime_s': times, 'errors': count_errors(nb_run), 'deterministic': deterministic,
               'paths_left': len(hits), 'scrubbed_outputs': scrubber.counter['n'], 'claim_problems': problems,
               'figs': [Path(f).name for f in figs]}
    (exec_dir / 'build_summary.json').write_text(json.dumps(summary, indent=1), encoding='utf-8')
    if hits or problems:
        sys.exit(2)


if __name__ == '__main__':
    main()
