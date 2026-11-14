"""雪梨四期資料清點 + 照既有清洗邏輯整理後做四期對照(IS-1114-inventory-01)。
可重跑:python -I syd_w_inventory_clean.py(約數分鐘,calendar 與 reviews 分塊讀,不另外解壓縮存檔)。
讀:scratchpad/insideairbnb_sydney/(唯讀)。寫:notes/raw/syd_w_inventory_clean_2026-11-14.json、.md。
清洗規則一律照既有四支腳本;能 import 的 import(airbnb_ab_field_inventory 的 is_scope、num),其餘照抄並在 RULES 註明出處行號。
不寫個別房源編號、名稱、房東名進輸出。
"""
import site
import sys
sys.path.append(site.getusersitepackages())
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from airbnb_ab_field_inventory import is_scope as AB_IS_SCOPE, num as AB_NUM  # noqa: E402  syd_y_2024_2026.py L25 同一份定義

sys.stdout.reconfigure(encoding='utf-8')
DATA = ROOT / 'scratchpad/insideairbnb_sydney'
RAW = ROOT / 'Innovation Studio/notes/raw'
DATE = '2026-11-14'
OUT_JSON = RAW / f'syd_w_inventory_clean_{DATE}.json'
OUT_MD = RAW / f'syd_w_inventory_clean_{DATE}.md'
PERIODS = ['2025-12-12', '2026-03-21', '2026-06-16', '2026-09-16']
MAIN = '2026-09-16'
EXTREME_CAP = 2000  # syd_b_positioning.py L45:每晚 > 2,000 澳幣不進模型樣本
CAL_DAYS = 30       # syd_a_market.py L31 CAL_WIN 之一
FILES7 = [('data', 'listings.csv.gz'), ('data', 'calendar.csv.gz'), ('data', 'reviews.csv.gz'),
          ('visualisations', 'listings.csv'), ('visualisations', 'reviews.csv'),
          ('visualisations', 'neighbourhoods.csv'), ('visualisations', 'neighbourhoods.geojson')]
WHAT = {
    'listings.csv.gz': '每間房一列的完整資料(房型、價格、房東、評分、設施…)',
    'calendar.csv.gz': '每間房未來約一年、每天一列:這天能不能訂、當天價格',
    'reviews.csv.gz': '每則評論一列(含評論全文)',
    'visualisations/listings.csv': '精簡版房源表(欄位少很多)',
    'visualisations/reviews.csv': '精簡版評論表(只有房號和日期)',
    'neighbourhoods.csv': '區名清單',
    'neighbourhoods.geojson': '各區邊界的地圖檔',
}
USED = {
    ('listings.csv.gz', '2025-12-12'): '用了:syd_a(日曆房號)、syd_c(新手與跨期)',
    ('listings.csv.gz', '2026-03-21'): '用了:syd_a(日曆房號)、syd_c(新手與跨期)',
    ('listings.csv.gz', '2026-06-16'): '用了:syd_a、syd_b(6 月訓練、測 9 月新房源)、syd_c',
    ('listings.csv.gz', '2026-09-16'): '用了:主力。syd_a 市場概況、syd_b 定價模型、syd_c 新手、syd_y 評論時間',
    ('calendar.csv.gz', '*'): '用了:syd_a 算抓取日後 30/60/90 天不能訂的比例(四期都算)',
    ('reviews.csv.gz', '2026-09-16'): '用了:syd_y 只讀房號和日期兩欄,算每月評論數、新上架',
    ('neighbourhoods.geojson', '2026-09-16'): '用了:syd_a 畫地圖、核對區名',
}

# ---- 清洗規則(每條:白話規則、為什麼、出處)----
RULES = [
    ('價格字串去掉「,」「$」空白後轉成數字;轉不出來的當缺值', '原始 price 是像 $1,200.00 的字串,不轉不能算',
     'syd_a_market.py L68-L69(num);airbnb_ab_field_inventory.py L40-L45;syd_b_positioning.py L100;syd_c_hosts_time.py L63'),
    ('讀檔一律當字串、空白不當缺值(再自己轉數字)', '避免 pandas 把「1」「01」或空字串亂轉',
     'syd_a_market.py L61;syd_b_positioning.py L65'),
    ('「有開價」= price 欄不是空白', '價格空白的房子沒有可比的價錢;2025-12 整欄空白所以那期沒有有開價的',
     'syd_a_market.py L359;syd_b_positioning.py L99'),
    ('只留整套出租(room_type = Entire home/apt)', '整套和只租一間房間的價錢不能直接比', 'syd_a_market.py L75;airbnb_ab_field_inventory.py L49'),
    ('只留 1 到 2 房(bedrooms 是 1 或 2)', '新房東多半是小房子;房間數空白或 0 的不留', 'syd_a_market.py L75;airbnb_ab_field_inventory.py L49'),
    ('只留住 2 到 4 人(accommodates 2 到 4)', '同樣大小的房子才比得起來', 'syd_a_market.py L73、L76;airbnb_ab_field_inventory.py L50'),
    ('只留最少住 1 到 7 晚(minimum_nights 1 到 7)', '最少住很久的是長租,不是一般短租', 'syd_a_market.py L74、L76;airbnb_ab_field_inventory.py L51'),
    ('模型樣本再拿掉一晚超過 2,000 澳幣的(剛好 2,000 保留)', '極端高價會把模型拉歪;中間價、分位數類統計不受影響所以其他地方仍用全部',
     'syd_b_positioning.py L45(EXTREME_CAP)、L479(dm = d[d.price_num <= EXTREME_CAP])'),
    ('新手 = 當房東年資(hosts_time_as_host_years × 12 + hosts_time_as_host_months)不超過 12 個月(含剛好 12)',
     '用平台給的年資欄推算;每期用自己那期的欄位值', 'syd_c_hosts_time.py L101(t_host)、L167(n12);notes/20 L158'),
    ('30 天不能訂的比例 = 抓取日(日曆最早那天)起 30 天內,available = f 的房源日 ÷ 全部房源日',
     '不能訂可能是被訂走,也可能是房東自己關掉,分不出來,只能當作需求的參考', 'syd_a_market.py L109-L135(calendar_blocked)、L117(blk)'),
    ('評分中間值:review_scores_rating 轉數字、空白的不算', '沒有評論的房子沒有分數', 'syd_a_market.py L415、L483'),
]

# ---- 建議但沒做 ----
SUGGEST = [
    '價格是 0、負數、或低到不合理(例如一晚個位數)的檢查。現有規則只看有沒有開價。',
    'accommodates 和 bedrooms 對不上的檢查(例如 1 房卻寫住 10 人)。',
    'amenities 寫成空清單「[]」要不要當缺值。現在只有空白才算缺值。',
    '座標超出雪梨範圍、或座標落的區和 neighbourhood_cleansed 對不上的檢查。',
    'price 含不含清潔費、稅:資料說明沒寫清楚,沒查。',
    '同一房東開了一模一樣的多間(疑似重複上架)的檢查。',
    'calendar 裡每天的價格和 listings 的 price 對一下,看是不是同一個價。',
    '抓取日(last_scraped)同一期內是否都是同一天;現在只靠日曆最早日期當抓取日。',
    '最少住超過 7 晚被排除的房子,有多少其實是 8 到 30 晚的短長租,可以另算。',
    'reviews 檔含已下架房源的評論;「四期都出現的同一間房」不含中途下架又上架的情況,沒細查。',
    '價格上限 2,000 對 1 房與 2 房用同一個數字;有沒有該分開,沒檢查。',
]


def pct(n, d, k=1):
    return None if not d else round(100.0 * n / d, k)


def num_series(s):  # syd_a_market.py L68-L69
    return pd.to_numeric(s.str.replace(r'[,$\s]', '', regex=True), errors='coerce')


def sha256_of(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 23), b''):
            h.update(b)
    return h.hexdigest()


def read_manifest():
    m = {}
    for line in (DATA / 'manifest.tsv').read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        p, size, sha = line.split('\t')
        m[p.lstrip('./')] = (int(size), sha)
    return m


def blank(s):
    return s.str.strip() == ''


# ---------------- listings:讀、清洗、漏斗 ----------------
def load_listings(p):
    return pd.read_csv(DATA / p / 'data/listings.csv.gz', dtype=str, keep_default_na=False)


def masks(df):
    ent = df['room_type'] == 'Entire home/apt'
    bed = ent & df['bedrooms'].isin(['1', '2'])                    # syd_a L75
    acc = pd.to_numeric(df['accommodates'], errors='coerce')
    mn = pd.to_numeric(df['minimum_nights'], errors='coerce')
    s3 = bed & acc.between(2, 4)                                    # syd_a L73、L76
    s4 = s3 & mn.between(1, 7)                                      # syd_a L74、L76
    has = ~blank(df['price'])                                       # syd_a L359
    pv = num_series(df['price'])
    s5 = s4 & has
    s6 = s5 & (pv <= EXTREME_CAP)                                   # syd_b L479
    return dict(ent=ent, bed=bed, s3=s3, scope=s4, scope_priced=s5, clean=s6, has_price=has, pv=pv)


def funnel(df, m):
    steps = [('全部', pd.Series(True, index=df.index)), ('只留整套出租', m['ent']), ('只留 1 到 2 房', m['bed']),
             ('只留住 2 到 4 人', m['s3']), ('只留最少住 1 到 7 晚', m['scope']), ('只留有開價的', m['scope_priced']),
             ('再拿掉一晚 2,000 澳幣以上的', m['clean'])]
    out, prev = [], None
    for name, mk in steps:
        n = int(mk.sum())
        out.append({'step': name, 'remaining': n, 'removed': None if prev is None else prev - n})
        prev = n
    return out


def newbie(df):  # syd_c_hosts_time.py L101、L167
    y = pd.to_numeric(df['hosts_time_as_host_years'], errors='coerce') if 'hosts_time_as_host_years' in df else pd.Series(np.nan, index=df.index)
    mo = pd.to_numeric(df['hosts_time_as_host_months'], errors='coerce') if 'hosts_time_as_host_months' in df else pd.Series(np.nan, index=df.index)
    return (y * 12 + mo) <= 12


def med(s):
    s = s.dropna()
    return None if len(s) == 0 else round(float(s.median()), 2)


def rating(df, mask=None):
    r = pd.to_numeric(df['review_scores_rating'], errors='coerce')
    if mask is not None:
        r = r[mask]
    r = r.dropna()
    return {'n_rated': int(len(r)), 'median': None if len(r) == 0 else round(float(r.median()), 3)}


# ---------------- 大檔:分塊讀 ----------------
def scan_calendar(p, clean_ids):
    """照 syd_a_market.py L109-L135:先按日期彙總,再取日曆最早日期起 30 天 [base, base+30)。"""
    path = DATA / p / 'data/calendar.csv.gz'
    t0 = time.time()
    cols = list(pd.read_csv(path, nrows=0).columns)
    tot, nrows, ids = None, 0, set()
    for ch in pd.read_csv(path, usecols=['listing_id', 'date', 'available'], dtype=str, chunksize=2_000_000):
        nrows += len(ch)
        ids.update(ch['listing_id'].unique())
        ins = ch['listing_id'].isin(clean_ids)
        blk = ch['available'] == 'f'
        g = pd.DataFrame({'date': ch['date'], 'n': 1, 'b': blk.astype(int), 'cn': ins.astype(int), 'cb': (ins & blk).astype(int)}).groupby('date').sum()
        tot = g if tot is None else tot.add(g, fill_value=0)
    tot = tot.sort_index()
    base = pd.Timestamp(tot.index[0])
    end = (base + pd.Timedelta(days=CAL_DAYS)).strftime('%Y-%m-%d')
    w = tot[tot.index < end]
    r = {'rows': nrows, 'cols': len(cols), 'min_date': tot.index[0], 'max_date': tot.index[-1], 'n_listings_in_calendar': len(ids),
         'window_days': int(len(w)),
         'all': {'listing_days': int(w['n'].sum()), 'blocked_days': int(w['b'].sum()), 'blocked_pct': pct(w['b'].sum(), w['n'].sum())},
         'clean': {'listing_days': int(w['cn'].sum()), 'blocked_days': int(w['cb'].sum()), 'blocked_pct': pct(w['cb'].sum(), w['cn'].sum())},
         'seconds': round(time.time() - t0, 1)}
    print('calendar', p, r['rows'], r['all']['blocked_pct'], r['seconds'], 's', flush=True)
    return r


def scan_reviews(p):
    path = DATA / p / 'data/reviews.csv.gz'
    t0 = time.time()
    cols = list(pd.read_csv(path, nrows=0).columns)
    n = 0
    for ch in pd.read_csv(path, usecols=['listing_id'], dtype=str, chunksize=1_000_000):
        n += len(ch)
    print('reviews', p, n, round(time.time() - t0, 1), 's', flush=True)
    return {'rows': n, 'cols': len(cols)}


def shape_small(path):
    if path.suffix == '.geojson':
        g = json.loads(path.read_text(encoding='utf-8'))
        feats = g['features']
        return {'rows': len(feats), 'cols': len(feats[0]['properties']) if feats else 0, 'note': 'geojson:列 = 區的個數(features),欄 = 每區屬性個數'}
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return {'rows': int(len(df)), 'cols': int(df.shape[1])}


# ---------------- 主程式 ----------------
def main():
    t_start = time.time()
    man = read_manifest()
    L, M, S = {}, {}, {}
    for p in PERIODS:
        L[p] = load_listings(p)
        M[p] = masks(L[p])
        # 對照既有 import 進來的 is_scope(syd_y_2024_2026.py L25):兩種寫法的 scope 必須一模一樣
        recs = L[p][['room_type', 'bedrooms', 'accommodates', 'minimum_nights']].to_dict('records')
        ab = np.array([AB_IS_SCOPE(r) for r in recs])
        assert (ab == M[p]['scope'].values).all(), ('is_scope 與本檔寫法不一致', p)
        prc = M[p]['pv'][M[p]['scope_priced']]
        assert prc.notna().all(), ('有開價列有無法解析的 price', p)
        assert all(AB_NUM(v) is not None for v in L[p]['price'][M[p]['scope_priced']].head(200))
        print('listings', p, L[p].shape, 'scope', int(M[p]['scope'].sum()), flush=True)

    # ---- 1. 28 個檔 ----
    cal, rev = {}, {}
    for p in PERIODS:
        clean_ids = set(L[p].loc[M[p]['clean'], 'id'])
        cal[p] = scan_calendar(p, clean_ids)
        rev[p] = scan_reviews(p)
    files = []
    for p in PERIODS:
        for sub, name in FILES7:
            path = DATA / p / sub / name
            rel = f'{p}/{sub}/{name}'
            size = path.stat().st_size
            sha = sha256_of(path)
            if sub == 'data' and name == 'listings.csv.gz':
                rc = {'rows': int(len(L[p])), 'cols': int(L[p].shape[1])}
            elif sub == 'data' and name == 'calendar.csv.gz':
                rc = {'rows': cal[p]['rows'], 'cols': cal[p]['cols']}
            elif sub == 'data' and name == 'reviews.csv.gz':
                rc = rev[p]
            else:
                rc = shape_small(path)
            key = name if sub == 'data' else (f'{sub}/{name}' if name in ('listings.csv', 'reviews.csv') else name)
            used = USED.get((name, p)) or USED.get((name, '*'))
            msize, msha = man.get(rel, (None, None))
            files.append({'period': p, 'folder': sub, 'file': name, 'bytes': size, 'rows': rc['rows'], 'cols': rc['cols'],
                          'rc_note': rc.get('note'), 'what': WHAT[key], 'used': used or '還沒用到',
                          'manifest_bytes': msize, 'size_ok': msize == size, 'sha256': sha, 'manifest_sha256': msha, 'sha_ok': msha == sha})
    in_28 = {f"{f['period']}/{f['folder']}/{f['file']}" for f in files}
    extras = []
    for rel, (msize, _) in sorted(man.items()):
        if rel in in_28:
            continue
        fp = DATA / rel
        extras.append({'file': rel, 'manifest_bytes': msize, 'on_disk_bytes': fp.stat().st_size if fp.exists() else None,
                       'size_ok': fp.exists() and fp.stat().st_size == msize})
    on_disk = {str(x.relative_to(DATA)).replace('\\', '/') for x in DATA.rglob('*') if x.is_file()} - {'manifest.tsv'}
    not_in_manifest = sorted(on_disk - set(man))
    print('files done', len(files), flush=True)

    # ---- 3/4/5 每期數字 ----
    FUN, CMP, HEALTH = {}, {}, {}
    HCOLS = ['price', 'bedrooms', 'beds', 'bathrooms_text', 'amenities', 'review_scores_rating', 'host_since',
             'hosts_time_as_host_years', 'hosts_time_as_host_months', 'latitude', 'longitude', 'neighbourhood_cleansed', 'neighbourhood']
    for p in PERIODS:
        df, m = L[p], M[p]
        n = len(df)
        FUN[p] = funnel(df, m)
        pv = m['pv']
        sp, cl = m['scope_priced'], m['clean']
        nw = newbie(df)
        top_all = df['neighbourhood_cleansed'].value_counts().head(5)
        top_cl = df.loc[cl, 'neighbourhood_cleansed'].value_counts().head(5)
        bd = df['bedrooms']
        CMP[p] = {
            'n_all': n,
            'n_has_price': int(m['has_price'].sum()), 'has_price_pct': pct(m['has_price'].sum(), n),
            'n_scope': int(m['scope'].sum()), 'n_scope_priced': int(sp.sum()), 'n_clean': int(cl.sum()), 'n_removed_by_cap': int(sp.sum() - cl.sum()),
            'median_all_priced': med(pv[m['has_price']]),
            'bed1_before_cap': {'n': int((sp & (bd == '1')).sum()), 'median': med(pv[sp & (bd == '1')])},
            'bed2_before_cap': {'n': int((sp & (bd == '2')).sum()), 'median': med(pv[sp & (bd == '2')])},
            'bed1_clean': {'n': int((cl & (bd == '1')).sum()), 'median': med(pv[cl & (bd == '1')])},
            'bed2_clean': {'n': int((cl & (bd == '2')).sum()), 'median': med(pv[cl & (bd == '2')])},
            'entire_share_pct': pct(m['ent'].sum(), n), 'n_entire': int(m['ent'].sum()),
            'n_neighbourhoods': int(df['neighbourhood_cleansed'].nunique()),
            'top5_all': [{'name': k, 'n': int(v)} for k, v in top_all.items()],
            'top5_clean': [{'name': k, 'n': int(v)} for k, v in top_cl.items()],
            'newbie_all': int(nw.sum()), 'newbie_scope_priced_before_cap': int((nw & sp).sum()), 'newbie_clean': int((nw & cl).sum()),
            'rating_all': rating(df), 'rating_clean': rating(df, cl),
            'cal30_all_pct': cal[p]['all']['blocked_pct'], 'cal30_clean_pct': cal[p]['clean']['blocked_pct'],
            'cal_base_date': cal[p]['min_date'], 'cal_n_listings': cal[p]['n_listings_in_calendar'],
            'reviews_rows': rev[p]['rows'],
        }
        h = {}
        for c in HCOLS:
            if c in df.columns:
                nm = int(blank(df[c]).sum())
                h[c] = {'missing_n': nm, 'missing_pct': pct(nm, n), 'column_exists': True}
            else:
                h[c] = {'missing_n': n, 'missing_pct': 100.0, 'column_exists': False}
        mnn = pd.to_numeric(df['minimum_nights'], errors='coerce')
        bn = pd.to_numeric(df['bedrooms'], errors='coerce')
        HEALTH[p] = {'missing': h, 'id_duplicates': int(df['id'].duplicated().sum()),
                     'weird': {'price_gt_2000': int((pv > EXTREME_CAP).sum()), 'price_eq_2000': int((pv == EXTREME_CAP).sum()),
                               'min_nights_gt_365': int((mnn > 365).sum()), 'bedrooms_zero': int((bn == 0).sum()),
                               'bedrooms_blank': int(blank(df['bedrooms']).sum())},
                     'n_columns': int(df.shape[1])}
    ids = [set(L[p]['id']) for p in PERIODS]
    all4 = set.intersection(*ids)
    same_id = {'all_four': len(all4), 'in_clean_2026_09': len(all4 & set(L[MAIN].loc[M[MAIN]['clean'], 'id'])),
               'pairs_with_2026_09': {p: len(set(L[p]['id']) & set(L[MAIN]['id'])) for p in PERIODS[:3]}}

    # ---- 對賬 ----
    recon = []

    def chk(item, expected, got):
        recon.append({'item': item, 'expected': expected, 'got': got, 'ok': bool(expected == got)})
    for p, e in zip(PERIODS, (20436, 13563, 20573, 20833)):
        chk(f'{p} 全部間數', e, CMP[p]['n_all'])
    chk('2025-12-12 有開價 0 間', 0, CMP['2025-12-12']['n_has_price'])
    for p, pc, nn in (('2026-03-21', 99.4, 13484), ('2026-06-16', 86.5, 17786), ('2026-09-16', 85.1, 17721)):
        chk(f'{p} 有開價比例', pc, CMP[p]['has_price_pct'])
        chk(f'{p} 有開價間數', nn, CMP[p]['n_has_price'])
    c9 = CMP[MAIN]
    chk('2026-09-16 清洗後(整套、1–2 房、2–4 人、最少住 1–7 晚)', 7565, c9['n_scope'])
    chk('2026-09-16 其中有開價', 6639, c9['n_scope_priced'])
    chk('2026-09-16 拿掉一晚 2,000 以上', 24, c9['n_removed_by_cap'])
    chk('2026-09-16 拿掉後', 6615, c9['n_clean'])
    chk('2026-09-16 1 房間數(有開價、拿掉高價前)', 4029, c9['bed1_before_cap']['n'])
    chk('2026-09-16 1 房中間價(同上)', 299, round(c9['bed1_before_cap']['median']))
    chk('2026-09-16 2 房間數(同上)', 2610, c9['bed2_before_cap']['n'])
    chk('2026-09-16 2 房中間價(同上)', 414, round(c9['bed2_before_cap']['median']))
    chk('2026-09-16 全部有開價房源中間價', 338, round(c9['median_all_priced']))
    chk('2026-09-16 整套出租占全部(%)', 78.9, c9['entire_share_pct'])
    chk('2026-09-16 新手(有開價、拿掉高價前)', 960, c9['newbie_scope_priced_before_cap'])
    for p, e in zip(PERIODS, (62.6, 55.0, 48.7, 58.5)):
        chk(f'{p} 抓取日後 30 天不能訂(%,全部房源)', e, CMP[p]['cal30_all_pct'])
    chk('2026-09-16 reviews 檔列數', 829163, CMP[MAIN]['reviews_rows'])
    chk('2026-09-16 區的個數(listings 的 neighbourhood_cleansed)', 38, c9['n_neighbourhoods'])
    chk('2026-09-16 neighbourhoods.csv 列數', 38, next(f['rows'] for f in files if f['period'] == MAIN and f['file'] == 'neighbourhoods.csv'))
    chk('2026-06-16 模型訓練樣本(清洗後有開價、拿掉高價)', 6747, CMP['2026-06-16']['n_clean'])

    result = {'scope_id': 'IS-1114-inventory-01', 'date': DATE, 'periods': PERIODS, 'main_period': MAIN,
              'files': files, 'extra_files_in_manifest': extras, 'files_on_disk_not_in_manifest': not_in_manifest,
              'manifest_lines': len(man), 'rules': [{'rule': a, 'why': b, 'source': c} for a, b, c in RULES],
              'funnel': FUN, 'compare': CMP, 'health': HEALTH, 'same_id': same_id, 'calendar_detail': cal,
              'reconciliation': recon, 'suggested_not_done': SUGGEST, 'seconds_total': round(time.time() - t_start, 1)}
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)), encoding='utf-8')
    OUT_MD.write_text(build_md(result), encoding='utf-8')
    bad = [r for r in recon if not r['ok']]
    print('對賬', len(recon) - len(bad), '/', len(recon), '不對:', [(r['item'], r['expected'], r['got']) for r in bad], flush=True)
    print('sha/size 不符:', [f['period'] + '/' + f['file'] for f in files if not (f['size_ok'] and f['sha_ok'])], flush=True)


# ---------------- 筆記 ----------------
def f_int(v):
    return '—' if v is None else f'{v:,}'


def f_pct(v):
    return '—' if v is None else f'{v:.1f}%'


def f_mon(v):
    return '—' if v is None else f'{v:,.0f}'


def f_rate(r):
    return '—' if r['median'] is None else f'{r["median"]}({r["n_rated"]:,} 間有評分)'


def tbl(head, rows):
    o = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
    o += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(o)


def mb(b):
    return f'{b / 1048576:,.1f} MB' if b >= 1048576 else f'{b / 1024:,.1f} KB' if b >= 1024 else f'{b} B'


def build_md(R):
    P, C, H, FUN = R['periods'], R['compare'], R['health'], R['funnel']
    bad = [r for r in R['reconciliation'] if not r['ok']]
    badfile = [f for f in R['files'] if not (f['size_ok'] and f['sha_ok'])]
    unused = [f for f in R['files'] if f['used'] == '還沒用到']
    o = [f'# 雪梨四期資料清點與清洗後對照({R["date"]})', '',
         '## 重點', '']
    if bad:
        o.append('**對賬有不對的項目:' + ';'.join(f'{r["item"]}(之前 {r["expected"]},這次 {r["got"]})' for r in bad) + '。原因見下方標注,未自己挑一個。**')
    else:
        o.append(f'- 之前算過的 {len(R["reconciliation"])} 個數字全部對上。')
    o.append(f'- 28 個檔都讀得進來;大小與 sha256 跟 manifest {"全部一致" if not badfile else "有 " + str(len(badfile)) + " 個對不上"}。manifest 另有 12 個已解壓的 .csv,沒算在 28 個內。')
    o.append(f'- 28 個檔裡 {len(unused)} 個我們還沒用到(主要是精簡版 visualisations 檔和三期的 reviews)。')
    o.append('- 清洗後有開價、拿掉一晚 2,000 澳幣以上的:' + '、'.join(f'{p} {C[p]["n_clean"]:,} 間' for p in P) + '。(2025-12 價格整欄空白,沒有開價的。)')
    o.append(f'- 四期都出現的同一間房(同一個 id)有 {R["same_id"]["all_four"]:,} 間。')
    o.append('')
    o += ['名詞:**中間價**(中間值)= 把所有價格由小排到大,站在正中間的那一個,比平均不容易被極貴的房子拉走。**房東開的價** = 房東掛在網站上的每晚價錢,不是客人真的付的價。', '']
    # 1
    o += ['## 1. 28 個檔的清單', '',
          '「壓縮後大小」就是檔案放在硬碟上的大小(.gz 是壓縮過的;非 .gz 的檔沒有壓縮)。.gz 直接用程式讀,沒有另外解壓縮存檔。', '']
    rows = []
    for f in R['files']:
        chk = '對' if (f['size_ok'] and f['sha_ok']) else '不對:' + ('大小 ' if not f['size_ok'] else '') + ('sha256' if not f['sha_ok'] else '')
        rc = f'{f["rows"]:,} 列、{f["cols"]} 欄' + ('(地圖檔:列 = 區數,欄 = 每區屬性數)' if f['rc_note'] else '')
        rows.append([f['period'], f['folder'], f['file'], mb(f['bytes']), rc, f['what'], f['used'], chk])
    o.append(tbl(['期別', '資料夾', '檔名', '壓縮後大小', '讀進來幾列、幾欄', '這個檔是什麼', '我們之前用它做了什麼', '跟 manifest 的大小與 sha256 對不對'], rows))
    o.append('')
    o.append(f'- sha256 是我自己重算的。對不上的:{"沒有" if not badfile else "、".join(f["period"] + "/" + f["file"] for f in badfile)}。')
    o.append(f'- manifest.tsv 共 {R["manifest_lines"]} 行;28 個之外還有 {len(R["extra_files_in_manifest"])} 個已解壓的 .csv(listings、calendar、reviews 各四期),只比對檔案大小:'
             + ('全部一致' if all(e['size_ok'] for e in R['extra_files_in_manifest']) else '有不一致:' + '、'.join(e['file'] for e in R['extra_files_in_manifest'] if not e['size_ok'])) + '。沒算 sha256(省時間)。')
    o.append(f'- 硬碟上有、manifest 沒列的檔:{"沒有" if not R["files_on_disk_not_in_manifest"] else "、".join(R["files_on_disk_not_in_manifest"])}。')
    o.append('- 「用了什麼」是到 syd_a_market.py、syd_b_positioning.py、syd_c_hosts_time.py、syd_y_2024_2026.py 四支裡找檔名確認的;其他腳本(例如 syd_verify.py)不算。')
    o.append('')
    # 2
    o += ['## 2. 清洗規則表', '', '規則一律照既有腳本,沒有新增。行號是那支腳本的行號。', '']
    o.append(tbl(['規則', '為什麼', '出自哪支腳本第幾行'], [[r['rule'], r['why'], r['source']] for r in R['rules']]))
    o.append('')
    # 3
    o += ['## 3. 清洗漏斗', '', '每格寫「剩幾間(這一步拿掉幾間)」。每一步都是在上一步剩下的房子裡再篩。', '']
    rows = []
    for i, st in enumerate(FUN[P[0]]):
        row = [st['step']]
        for p in P:
            s = FUN[p][i]
            row.append(f'{s["remaining"]:,}' + ('' if s['removed'] is None else f'(−{s["removed"]:,})'))
        rows.append(row)
    o.append(tbl(['步驟'] + P, rows))
    o.append('')
    o.append('2025-12-12 那期價格欄整欄空白,所以「只留有開價的」那一步剩 0 間。')
    o.append('')
    # 4
    o += ['## 4. 四期對照', '',
          '「全部」= 該期 listings 檔的全部房源。「清洗後有開價」= 整套、1–2 房、2–4 人、最少住 1–7 晚、有開價(還沒拿掉高價)。「模型樣本」= 再拿掉一晚 2,000 澳幣以上的。每列都寫了算的是哪一群。', '']
    def row(label, fn):
        return [label] + [fn(C[p]) for p in P]
    rows = [
        row('全部間數(全部)', lambda c: f_int(c['n_all'])),
        row('有開價的間數(全部)', lambda c: f_int(c['n_has_price'])),
        row('有開價的比例(全部)', lambda c: f_pct(c['has_price_pct'])),
        row('清洗後(整套、1–2 房、2–4 人、最少住 1–7 晚)間數', lambda c: f_int(c['n_scope'])),
        row('清洗後有開價的間數(拿掉高價前)', lambda c: f_int(c['n_scope_priced'])),
        row('模型樣本間數(再拿掉一晚 2,000 以上)', lambda c: f_int(c['n_clean'])),
        row('全部有開價房源的中間價(澳幣/晚)', lambda c: f_mon(c['median_all_priced'])),
        row('1 房中間價(清洗後有開價,拿掉高價前)', lambda c: f'{f_mon(c["bed1_before_cap"]["median"])}({c["bed1_before_cap"]["n"]:,} 間)'),
        row('2 房中間價(同上)', lambda c: f'{f_mon(c["bed2_before_cap"]["median"])}({c["bed2_before_cap"]["n"]:,} 間)'),
        row('1 房中間價(模型樣本)', lambda c: f'{f_mon(c["bed1_clean"]["median"])}({c["bed1_clean"]["n"]:,} 間)'),
        row('2 房中間價(模型樣本)', lambda c: f'{f_mon(c["bed2_clean"]["median"])}({c["bed2_clean"]["n"]:,} 間)'),
        row('整套出租占全部的比例(全部)', lambda c: f'{f_pct(c["entire_share_pct"])}({c["n_entire"]:,} 間)'),
        row('區的個數(全部,neighbourhood_cleansed)', lambda c: str(c['n_neighbourhoods'])),
    ]
    for i in range(5):
        rows.append([f'房源最多的第 {i + 1} 區(全部)'] + [f'{C[p]["top5_all"][i]["name"]} {C[p]["top5_all"][i]["n"]:,} 間' for p in P])
    rows += [
        row('新手 = 當房東年資不超過 12 個月(全部)', lambda c: f_int(c['newbie_all'])),
        row('新手(清洗後有開價,拿掉高價前)', lambda c: f_int(c['newbie_scope_priced_before_cap'])),
        row('新手(模型樣本)', lambda c: f_int(c['newbie_clean'])),
        row('評分中間值(全部有評分的)', lambda c: f_rate(c['rating_all'])),
        row('評分中間值(模型樣本有評分的)', lambda c: f_rate(c['rating_clean'])),
        row('抓取日後 30 天不能訂的比例(日曆內全部房源)', lambda c: f_pct(c['cal30_all_pct'])),
        row('抓取日後 30 天不能訂的比例(模型樣本)', lambda c: f_pct(c['cal30_clean_pct'])),
        row('日曆最早日期(當抓取日)', lambda c: c['cal_base_date']),
        row('日曆裡有幾間房', lambda c: f_int(c['cal_n_listings'])),
        row('reviews 檔有幾列評論', lambda c: f_int(c['reviews_rows'])),
    ]
    o.append(tbl(['項目(算的是哪一群)'] + P, rows))
    o.append('')
    s = R['same_id']
    o.append(f'- 四期都出現的同一間房(同一個 id,比的是全部房源):**{s["all_four"]:,} 間**;其中 {s["in_clean_2026_09"]:,} 間在 2026-09-16 的模型樣本裡。')
    o.append('- 2026-09-16 那期的 id 跟前三期各重疊:' + '、'.join(f'{p} {v:,} 間' for p, v in s['pairs_with_2026_09'].items()) + '。')
    o.append('- 「不能訂」可能是被客人訂走,也可能是房東自己關掉,分不出來,只能當作需求的參考,不是真實入住。')
    o.append('- 新手的算法:每期用自己那期的年資欄(年 × 12 + 月 ≤ 12),所以不同期的新手不是同一批人。')
    o.append('')
    # 5
    o += ['## 5. 資料體檢', '', '缺值 = 欄位是空白。分母都是該期全部房源。欄位在檔案裡不存在會標「欄位不存在」。', '']
    labels = {'price': 'price(房東開的價)', 'bedrooms': 'bedrooms(房間數)', 'beds': 'beds(床數)', 'bathrooms_text': 'bathrooms_text(衛浴)',
              'amenities': 'amenities(設施)', 'review_scores_rating': 'review_scores_rating(評分)', 'host_since': 'host_since(房東註冊日)',
              'hosts_time_as_host_years': 'hosts_time_as_host_years(當房東年資:年)', 'hosts_time_as_host_months': 'hosts_time_as_host_months(當房東年資:月)',
              'latitude': 'latitude', 'longitude': 'longitude', 'neighbourhood_cleansed': 'neighbourhood_cleansed(區)', 'neighbourhood': 'neighbourhood(原始區欄)'}
    rows = []
    for c, lab in labels.items():
        rows.append([lab] + [('欄位不存在' if not H[p]['missing'][c]['column_exists'] else f_pct(H[p]['missing'][c]['missing_pct'])) for p in P])
    o.append('**缺值比例**')
    o.append('')
    o.append(tbl(['欄位'] + P, rows))
    o.append('')
    wr = [['listings 欄數'] + [str(H[p]['n_columns']) for p in P],
          ['id 重複的列數'] + [f_int(H[p]['id_duplicates']) for p in P],
          ['一晚超過 2,000 澳幣(間)'] + [f_int(H[p]['weird']['price_gt_2000']) for p in P],
          ['一晚剛好 2,000 澳幣(間,保留)'] + [f_int(H[p]['weird']['price_eq_2000']) for p in P],
          ['最少住超過 365 晚(間)'] + [f_int(H[p]['weird']['min_nights_gt_365']) for p in P],
          ['房間數是 0(間)'] + [f_int(H[p]['weird']['bedrooms_zero']) for p in P],
          ['房間數是空白(間)'] + [f_int(H[p]['weird']['bedrooms_blank']) for p in P]]
    o.append('**id 重複與怪值**')
    o.append('')
    o.append(tbl(['項目'] + P, wr))
    o.append('')
    o.append('**對賬(之前算過、也驗過的數字)**')
    o.append('')
    o.append(tbl(['項目', '之前的數字', '這次算出來', '對不對'], [[r['item'], r['expected'], r['got'], '對' if r['ok'] else '不對'] for r in R['reconciliation']]))
    o.append('')
    o += ['## 建議但沒做', '']
    o += [f'{i}. {t}' for i, t in enumerate(R['suggested_not_done'], 1)]
    o.append('')
    return '\n'.join(o)


if __name__ == '__main__':
    main()
