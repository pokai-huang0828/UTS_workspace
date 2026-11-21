"""共用函式:篩選、清洗、設施解析、特徵矩陣、基準 B1、誤差指標。

清洗與篩選規則照抄自 Innovation Studio/analysis/sydney/syd_b_positioning.py(下面每個函式都註明原行號),
刻意不 import 它,讓 model_training/ 這個資料夾可以獨立重跑。
"""
import json
import os
import re
from pathlib import Path

os.environ.setdefault('LOKY_MAX_CPU_COUNT', '24')  # 只為了關掉 joblib 找不到實體核心數的警告

import numpy as np
import pandas as pd

SEED = 42
HERE = Path(__file__).resolve().parent
BASE = HERE.parent                      # Innovation Studio/model_training
RAW = BASE / 'data' / 'raw'
PROC = BASE / 'data' / 'processed'
RUNS = BASE / 'runs'

MAIN, PREV = '2026-09-16', '2026-06-16'
EXTREME_CAP = 2000      # syd_b 第 45 行:每晚 > 2,000 澳元視為極端值,不進模型
MIN_GROUP = 30          # syd_b 第 41 行:組太小的門檻
K_NEAR = 30             # syd_b 第 42 行:退回規則,同臥室數、最近的 30 間
TOP_N_AMEN = 40         # syd_b 第 43 行:設施旗標數(依出現比例取前 N,不看價格)

# syd_b 第 46–48 行(多讀 host_id 做分組;calculated_host_listings_count 是禁用特徵,這裡不讀)
USECOLS = ['id', 'host_id', 'room_type', 'property_type', 'accommodates', 'bedrooms', 'beds', 'bathrooms_text',
           'neighbourhood_cleansed', 'latitude', 'longitude', 'minimum_nights', 'price', 'amenities']

# syd_b 第 49–58 行
FEATURES_ALLOWED = ['neighbourhood_cleansed(區)', 'latitude/longitude', 'property_type(房型細類)', 'bedrooms',
                    'accommodates', 'beds', 'bathrooms_text(解析成浴室數)', 'amenities(設施數 + 前 40 項旗標)',
                    'minimum_nights']
FEATURES_BANNED = {
    'number_of_reviews*, review_scores_*, first_review, last_review, reviews_per_month': '新房東上架前沒有評論',
    'estimated_occupancy_l365d, estimated_revenue_l365d': 'revenue = price × occupancy,直接洩漏答案;occupancy 由評論推算',
    'availability_*': '是上架後的行事曆結果,新房東沒有',
    'price_quote_*': '跟價格直接相關(報價本身)',
    'host_is_superhost, host_listings_count 等房東經營資料': '新房東沒有',
}

# 處理後訓練表要留的欄(不含房東姓名、網址、描述、評論)
PROC_COLS = ['id', 'host_id', 'nb', 'property_type', 'bedrooms', 'lat', 'lon', 'bed_n', 'acc', 'beds_n',
             'beds_missing', 'baths', 'baths_missing', 'min_n', 'amen_n', 'amenities', 'price_num']


# 新增兩群房源用的欄位與設定(預設群 entire_1_2 = 第一次訓練,行為不變)
PROC_COLS_EXT = PROC_COLS + ['bed_missing', 'acc_missing', 'min_missing', 'in_run01']
FLAG_NAMES = {'bed_missing': '臥室數缺值旗標', 'acc_missing': '可住人數缺值旗標', 'min_missing': '最少入住晚數缺值旗標'}
GROUPS = {
    'entire_1_2': dict(run_default='run_2026-11-21_01', table='train_table_2026-09.csv', ext='extremes_dropped_24.csv',
                       cap=2000, flags=[], title='整套 1–2 臥', desc='篩選',
                       scope_text='整套出租、臥室 1–2、可住 2–4 人、最少 1–7 晚;範圍外的房子不要用這個模型'),
    'private_room': dict(run_default='run_2026-11-21_02_private_room', table='train_table_2026-09_private_room.csv',
                         ext='extremes_dropped_private_room.csv', cap=2000, flags=['bed_missing'], title='獨立房間',
                         desc='獨立房間(Private room)、可住 1–4 人、最少 1–7 晚',
                         scope_text='獨立房間(Private room)、可住 1–4 人、最少 1–7 晚、每晚 2,000 以下;整套出租和範圍外的不要用這個模型',
                         impute='臥室數空的補 1 並加缺值旗標(0 間臥室照原值 0)'),
    'entire_home_all': dict(run_default='run_2026-11-21_03_entire_home_all', table='train_table_2026-09_entire_home_all.csv',
                            ext='extremes_dropped_entire_home_all.csv', cap=3000,
                            flags=['bed_missing', 'acc_missing', 'min_missing'], title='全部整套房',
                            desc='整套出租(Entire home/apt,臥室、人數、最少晚數都不設範圍)',
                            scope_text='整套出租(不限臥室數、人數、最少晚數)、每晚 3,000 以下;獨立房間、飯店房等其他房型不要用這個模型',
                            impute='臥室數、可住人數、最少入住晚數缺值補中位數(用該群有價的全部列算)並各加缺值旗標'),
}


# ---------------- 讀檔與清洗 ----------------
def load_raw(period):
    """syd_b 第 64–65 行(檔名改成 data/raw/listings_<期別>.csv.gz)。"""
    return pd.read_csv(RAW / f'listings_{period}.csv.gz', dtype=str, keep_default_na=False, usecols=USECOLS)


def scope(df):
    """syd_b 第 68–72 行:整套、臥室 1 或 2、可住 2–4 人、最少 1–7 晚。"""
    acc = pd.to_numeric(df.accommodates.where(df.accommodates.str.isdigit()), errors='coerce')
    mn = pd.to_numeric(df.minimum_nights.where(df.minimum_nights.str.isdigit()), errors='coerce')
    m = (df.room_type == 'Entire home/apt') & df.bedrooms.isin(['1', '2']) & acc.between(2, 4) & mn.between(1, 7)
    return df[m].copy()


def _num(s):
    """純數字字串 → 數字;其餘(空、含字母)→ NaN。"""
    return pd.to_numeric(s.where(s.str.isdigit()), errors='coerce')


def scope_private(df):
    """02 獨立房間:Private room、可住 1–4 人(純數字)、最少 1–7 晚(純數字)。"""
    return df[(df.room_type == 'Private room') & _num(df.accommodates).between(1, 4)
              & _num(df.minimum_nights).between(1, 7)].copy()


def scope_entire_all(df):
    """03 全部整套房:Entire home/apt,其他不設限。"""
    return df[df.room_type == 'Entire home/apt'].copy()


def parse_bath(s):
    """syd_b 第 75–82 行。"""
    s = s.strip().lower()
    if not s:
        return np.nan
    if 'half' in s:
        return 0.5
    m = re.search(r'(\d+(\.\d+)?)', s)
    return float(m.group(1)) if m else np.nan


def parse_amen(s):
    """syd_b 第 85–89 行。"""
    try:
        return frozenset(a.strip() for a in json.loads(s) if isinstance(a, str) and a.strip())
    except (ValueError, TypeError):
        return frozenset()


def amen_counts(sets):
    """syd_b 第 92–95 行:設施出現次數;同次數依名稱排序。"""
    c = pd.Series([a for s in sets for a in sorted(s)]).value_counts()
    return c.iloc[np.lexsort((c.index.values, -c.values))]


def prep(sc, mode='default'):
    """syd_b 第 98–119 行(拿掉 hostcnt:房東名下房源數是禁用特徵)。mode 不是 default → 走 prep_ext(新增兩群)。"""
    if mode != 'default':
        return prep_ext(sc, mode)
    d = sc[sc.price != ''].copy()
    d['price_num'] = d.price.str.replace(r'[,$\s]', '', regex=True).astype(float)
    assert (d.price_num > 0).all()
    d['bed_n'] = d.bedrooms.astype(int)
    d['acc'] = d.accommodates.astype(int)
    d['min_n'] = d.minimum_nights.astype(int)
    d['lat'] = d.latitude.astype(float)
    d['lon'] = d.longitude.astype(float)
    beds = pd.to_numeric(d.beds, errors='coerce')
    d['beds_missing'] = beds.isna().astype(int)
    d['beds_n'] = beds.fillna(d.bed_n)            # 床數缺 → 用臥室數補 + 缺值旗標
    d['baths'] = d.bathrooms_text.map(parse_bath)
    d['baths_missing'] = d.baths.isna().astype(int)
    d['baths'] = d.baths.fillna(1.0)
    d['amen'] = d.amenities.map(parse_amen)
    d['amen_n'] = d.amen.map(len)
    d['nb'] = d.neighbourhood_cleansed
    return d.reset_index(drop=True)


LAST_FILLS = {}   # prep_ext 最近一次用的補值(給 01 印出來)


def prep_ext(sc, mode):
    """新增兩群房源:臥室/可住人數/最少晚數缺值補值並加旗標;其餘欄位處理同 prep。
    private_room:臥室數空的補 1(0 照原值);entire_home_all:三欄缺值補中位數(用有價的全部列)。"""
    d = sc[sc.price != ''].copy()
    d['price_num'] = d.price.str.replace(r'[,$\s]', '', regex=True).astype(float)
    assert (d.price_num > 0).all()
    bed, acc, mn = _num(d.bedrooms), _num(d.accommodates), _num(d.minimum_nights)
    d['bed_missing'], d['acc_missing'], d['min_missing'] = (bed.isna().astype(int), acc.isna().astype(int),
                                                           mn.isna().astype(int))
    fills = {'bed': 1.0 if mode == 'private_room' else float(bed.median()),
             'acc': float(acc.median()), 'min': float(mn.median())}
    LAST_FILLS.clear()
    LAST_FILLS.update(fills)
    d['bed_n'] = bed.fillna(fills['bed'])
    d['acc'] = acc.fillna(fills['acc'])
    d['min_n'] = mn.fillna(fills['min'])
    d['bedrooms'] = d.bed_n.map(lambda v: str(int(v)) if float(v).is_integer() else str(v))   # B1 分組用
    d['lat'] = d.latitude.astype(float)
    d['lon'] = d.longitude.astype(float)
    beds = pd.to_numeric(d.beds, errors='coerce')
    d['beds_missing'] = beds.isna().astype(int)
    d['beds_n'] = beds.fillna(d.bed_n)
    d['baths'] = d.bathrooms_text.map(parse_bath)
    d['baths_missing'] = d.baths.isna().astype(int)
    d['baths'] = d.baths.fillna(1.0)
    d['amen'] = d.amenities.map(parse_amen)
    d['amen_n'] = d.amen.map(len)
    d['nb'] = d.neighbourhood_cleansed
    return d.reset_index(drop=True)


def load_processed(name):
    """讀 data/processed/ 的表,補回分析用欄位(amen 集合、grp、y)。"""
    d = pd.read_csv(PROC / name, dtype={'id': str, 'host_id': str, 'bedrooms': str}, keep_default_na=False)
    d['amen'] = d.amenities.map(parse_amen)
    d['grp'] = d.nb + '|' + d.bedrooms           # syd_b 第 117 行
    d['y'] = np.log(d.price_num)                 # syd_b 第 118 行
    return d


# ---------------- 特徵 ----------------
class Spec:
    """syd_b 第 155–161 行:設施名單、區清單、房型細類清單,只能用傳入的(訓練)資料決定。"""
    def __init__(self, d, flags=()):
        self.flags = list(flags)     # 缺值旗標欄(只有新增兩群會有;預設群為空 → 特徵矩陣和原本逐欄相同)
        cnt = amen_counts(d.amen)
        self.top_amen = list(cnt.index[:TOP_N_AMEN])
        self.nb_levels = sorted(d.nb.unique())
        ptc = d.property_type.value_counts()
        self.pt_levels = sorted(ptc.index[ptc >= 30]) + ['Other']

    def to_dict(self):
        out = {'top_amen': self.top_amen, 'nb_levels': self.nb_levels, 'pt_levels': self.pt_levels}
        if self.flags:
            out['flags'] = self.flags
        return out

    @classmethod
    def from_dict(cls, dd):
        s = cls.__new__(cls)
        s.top_amen, s.nb_levels, s.pt_levels = dd['top_amen'], dd['nb_levels'], dd['pt_levels']
        s.flags = dd.get('flags', [])
        return s


NUM_COLS = ['lat', 'lon', 'bed_n', 'acc', 'beds_n', 'baths', 'min_n', 'amen_n']
BASE_NAMES = ['區', '房型細類', '緯度', '經度', '臥室數', '可住人數', '床數', '浴室數', '最少入住晚數', '設施數']


def make_X(d, spec):
    """syd_b 第 180–192 行 X_tree(host=False):區、房型細類為整數代碼,其後 8 個數值欄、40 個設施旗標。
    與原版唯一差別:訓練時沒見過的區代碼設為 -1(原版為 NaN;HistGradientBoosting 兩者都當缺值)。"""
    nbmap = {v: i for i, v in enumerate(spec.nb_levels)}
    ptmap = {v: i for i, v in enumerate(spec.pt_levels)}
    nb = d.nb.map(lambda v: nbmap.get(v, -1)).astype(float).values
    pt = d.property_type.map(lambda v: ptmap.get(v, ptmap['Other'])).astype(float).values
    num = d[NUM_COLS + spec.flags].values.astype(float)
    fl = np.array([[a in s for a in spec.top_amen] for s in d.amen], float).reshape(len(d), len(spec.top_amen))
    X = np.hstack([nb[:, None], pt[:, None], num, fl])
    names = BASE_NAMES + [FLAG_NAMES[f] for f in spec.flags] + [f'設施:{a}' for a in spec.top_amen]
    return X, names


def feature_groups(names):
    """排列重要性的「整組一起打亂」分組(欄位索引)。"""
    idx = {n: i for i, n in enumerate(names)}
    size = [idx['臥室數'], idx['可住人數'], idx['床數'], idx['浴室數']] + \
        [idx[n] for n in ('臥室數缺值旗標', '可住人數缺值旗標') if n in idx]       # 缺值旗標跟著本欄的組
    mn = [idx['最少入住晚數']] + [idx[n] for n in ('最少入住晚數缺值旗標',) if n in idx]
    return {
        '位置(區+經緯度)': [idx['區'], idx['緯度'], idx['經度']],
        '大小(臥室、人數、床、浴室)': size,
        '設施(設施數+40 個旗標)': [idx['設施數']] + [i for n, i in idx.items() if n.startswith('設施:')],
        '房型細類': [idx['房型細類']],
        '最少入住晚數': mn,
    }


# ---------------- 基準 ----------------
def km(lat0, lon0, lat, lon):
    """syd_b 第 134–135 行。"""
    return np.hypot((lat - lat0) * 111.0, (lon - lon0) * 111.0 * np.cos(np.radians(lat0)))


def b1_predict(tr, te):
    """syd_b 第 138–151 行:區×臥室數 訓練集中位數;該組不足 30 間 → 同臥室數、最近 30 間的中位數。"""
    st = tr.groupby('grp').price_num.agg(['median', 'size'])
    pools = {b: (tr.lat.values[tr.bed_n.values == b], tr.lon.values[tr.bed_n.values == b],
                 tr.price_num.values[tr.bed_n.values == b]) for b in np.unique(tr.bed_n.values)}   # 預設群只有 1、2
    allp = (tr.lat.values, tr.lon.values, tr.price_num.values)   # 訓練集沒見過的臥室數 → 用全部
    out, lvl = np.empty(len(te)), np.empty(len(te), int)
    for i, (g, b, la, lo) in enumerate(zip(te.grp.values, te.bed_n.values, te.lat.values, te.lon.values)):
        if g in st.index and st.at[g, 'size'] >= MIN_GROUP:
            out[i], lvl[i] = st.at[g, 'median'], 1
        else:
            pla, plo, pp = pools.get(b, allp)
            if len(pp) <= K_NEAR:   # 該臥室數不足 30 間(預設群不會發生)→ 全部取中位數
                out[i], lvl[i] = np.median(pp), 2
                continue
            idx = np.argpartition(km(la, lo, pla, plo), K_NEAR)[:K_NEAR]
            out[i], lvl[i] = np.median(pp[idx]), 2
    return out, lvl


def peers(pool, nb, bed_n, lat, lon):
    """同類:同區×同臥室數;不足 30 間 → 同臥室數、距離最近 30 間(定義同 B1)。回傳 (價格陣列, 用了哪一層)。"""
    g = pool[(pool.nb == nb) & (pool.bed_n == bed_n)]
    if len(g) >= MIN_GROUP:
        return g.price_num.values, '同區同臥室數'
    p = pool[pool.bed_n == bed_n]
    if len(p) <= K_NEAR:
        return p.price_num.values, '同臥室數全部(不足 30 間)'
    idx = np.argpartition(km(lat, lon, p.lat.values, p.lon.values), K_NEAR)[:K_NEAR]
    return p.price_num.values[idx], '同臥室數最近 30 間'


# ---------------- 指標 ----------------
def metrics(y_aud, p_aud):
    """誤差都在澳元尺度算;R² 在 ln 尺度算。"""
    y_aud, p_aud = np.asarray(y_aud, float), np.asarray(p_aud, float)
    ae = np.abs(p_aud - y_aud)
    ape = ae / y_aud
    ly, lp = np.log(y_aud), np.log(p_aud)
    r2 = 1 - np.sum((ly - lp) ** 2) / np.sum((ly - ly.mean()) ** 2)
    return {'n': int(len(y_aud)), 'MAE_aud': round(float(ae.mean()), 1),
            'MdAPE_pct': round(float(100 * np.median(ape)), 1),
            'within20_pct': round(float(100 * np.mean(ape <= 0.2)), 1),
            'RMSE_aud': round(float(np.sqrt(np.mean((p_aud - y_aud) ** 2))), 1),
            'R2_log': round(float(r2), 3)}


def mae_aud(y_log, p_log):
    return float(np.mean(np.abs(np.exp(p_log) - np.exp(y_log))))
