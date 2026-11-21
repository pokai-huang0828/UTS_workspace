"""讀資料。房源一律從 model_training/data/ 讀(raw 與 processed);路徑都從這個檔的位置往上算。

評論檔只讀 listing_id、date 兩欄(算月份指數用);日曆檔只讀 listing_id、date、available。
這兩個大檔算出的彙總表存在 app_prototype/data/(不進版控),第二次起直接讀彙總表。
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

APP = Path(__file__).resolve().parents[1]           # Innovation Studio/app_prototype
IS = APP.parent                                     # Innovation Studio
REPO = IS.parent                                    # repo 根目錄
MT = IS / 'model_training'
MT_SRC = MT / 'src'
RAW = MT / 'data' / 'raw'
PROC = MT / 'data' / 'processed'
RUN_DIR = MT / 'runs' / 'run_2026-11-21_01'
SNAP = REPO / 'scratchpad' / 'insideairbnb_sydney' / '2026-09-16' / 'data'
REVIEWS = SNAP / 'reviews.csv.gz'
CALENDAR = SNAP / 'calendar.csv.gz'
HOLIDAYS = IS / 'refs' / 'external_2026-11-18' / '3_australian_public_holidays_combined_2021-2025.csv'
APP_DATA = APP / 'data'

N_POOL = 6639          # 篩選且有價(含 > 2,000 的 24 間);同類統計一律用這個
N_TRAIN = 6615         # 模型訓練用(去掉 > 2,000)

# 借用 model_training 的清洗與特徵函式(只 import,不改它)
if str(MT_SRC) not in sys.path:
    sys.path.insert(0, str(MT_SRC))
import common as C  # noqa: E402


@lru_cache(maxsize=1)
def load_pool():
    """6,639 間:processed 的 6,615 間 + 被拿掉的 24 間極端值;再從 raw 補上 estimated_occupancy_l365d(T6 用)。"""
    d = pd.concat([C.load_processed('train_table_2026-09.csv'), C.load_processed('extremes_dropped_24.csv')],
                  ignore_index=True)
    assert len(d) == N_POOL, f'同類母體應為 {N_POOL} 間,實際 {len(d)}'
    occ = pd.read_csv(RAW / 'listings_2026-09-16.csv.gz', usecols=['id', 'estimated_occupancy_l365d'],
                      dtype={'id': str})
    d = d.merge(occ, on='id', how='left', validate='one_to_one')
    d['occ365'] = pd.to_numeric(d.estimated_occupancy_l365d, errors='coerce')
    d = d.drop(columns=['estimated_occupancy_l365d'])
    return d.sort_values('id').reset_index(drop=True)


@lru_cache(maxsize=1)
def load_model():
    """載入存好的模型與 model_card.json。"""
    import joblib
    bundle = joblib.load(RUN_DIR / 'model_final.joblib')
    card = json.load(open(RUN_DIR / 'model_card.json', encoding='utf-8'))
    return bundle, card


def nb_center(nb):
    """沒給經緯度 → 該區房源經緯度的中位數(用 6,639 間算)。"""
    p = load_pool()
    g = p[p.nb == nb]
    if g.empty:
        raise ValueError(f'區「{nb}」不在資料裡')
    return float(g.lat.median()), float(g.lon.median())


@lru_cache(maxsize=1)
def review_month_counts():
    """每間房(只限 6,639 間)在 2024、2025 年各月的評論數。只讀 listing_id、date。"""
    f = APP_DATA / 'review_month_counts_2024_2025.csv'
    if not f.exists():
        ids = set(load_pool().id)
        r = pd.read_csv(REVIEWS, usecols=['listing_id', 'date'], dtype={'listing_id': str, 'date': str})
        r = r[r.listing_id.isin(ids)]
        r['year'] = r.date.str[:4].astype(int)
        r['month'] = r.date.str[5:7].astype(int)
        r = r[r.year.isin([2024, 2025])]
        out = r.groupby(['listing_id', 'year', 'month']).size().rename('n').reset_index()
        APP_DATA.mkdir(exist_ok=True)
        out.to_csv(f, index=False)
    return pd.read_csv(f, dtype={'listing_id': str})


@lru_cache(maxsize=1)
def calendar_month_unavail():
    """每間房(只限 6,639 間)每個月:日曆天數、不可訂天數。只讀 listing_id、date、available。"""
    f = APP_DATA / 'calendar_month_unavail_2026-09-16.csv'
    if not f.exists():
        ids = set(load_pool().id)
        parts = []
        for ch in pd.read_csv(CALENDAR, usecols=['listing_id', 'date', 'available'],
                              dtype={'listing_id': str, 'date': str, 'available': str}, chunksize=2_000_000):
            ch = ch[ch.listing_id.isin(ids)]
            ch['ym'] = ch.date.str[:7]
            ch['unavail'] = (ch.available == 'f').astype(int)
            parts.append(ch.groupby(['listing_id', 'ym']).agg(days=('unavail', 'size'), unavail=('unavail', 'sum')))
        out = pd.concat(parts).groupby(level=[0, 1]).sum().reset_index()
        APP_DATA.mkdir(exist_ok=True)
        out.to_csv(f, index=False)
    return pd.read_csv(f, dtype={'listing_id': str})


@lru_cache(maxsize=1)
def nsw_holidays():
    """NSW 公眾假期(檔案只有 2021–2025)。只回傳日期與名稱,不帶網址。"""
    h = pd.read_csv(HOLIDAYS, dtype=str)
    h = h[h.Jurisdiction.str.lower() == 'nsw'][['Date', 'Holiday Name']].copy()
    h['date'] = pd.to_datetime(h.Date, format='%Y%m%d')
    h['name'] = h['Holiday Name'].str.strip()
    return h[['date', 'name']].drop_duplicates().sort_values('date').reset_index(drop=True)


def jaccard(a, b):
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def km(lat0, lon0, lat, lon):
    return C.km(lat0, lon0, np.asarray(lat), np.asarray(lon))
