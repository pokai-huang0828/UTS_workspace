"""雪梨 A/B/C 獨立驗算(IS-1111-SYD-VERIFY)。從原始 csv.gz 自己重算,不 import 產出者腳本。
執行:python -I "Innovation Studio/analysis/sydney/syd_verify.py"  → 印 JSON 到 stdout(不寫其他檔)。
輸出只有彙總數字,不含個別房東/房源資料。
"""
import site, sys
sys.path.append(site.getusersitepackages())
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'scratchpad' / 'insideairbnb_sydney'
P12, P03, P06, P09 = '2025-12-12', '2026-03-21', '2026-06-16', '2026-09-16'


def rd(p, usecols=None):
    return pd.read_csv(BASE / p / 'data' / 'listings.csv.gz', dtype=str, keep_default_na=False,
                       usecols=usecols)


def pnum(s):
    return pd.to_numeric(s.str.replace(r'[,$\s]', '', regex=True), errors='coerce')


def scope_mask(d):
    acc, mn = d.accommodates, d.minimum_nights
    return ((d.room_type == 'Entire home/apt') & d.bedrooms.isin(['1', '2'])
            & acc.str.isdigit() & mn.str.isdigit()
            & pd.to_numeric(acc, errors='coerce').between(2, 4)
            & pd.to_numeric(mn, errors='coerce').between(1, 7))


R = {}
L = rd(P09)
L['price_v'] = pnum(L.price)
L['has_price'] = L.price.str.strip() != ''
L['scope'] = scope_mask(L)
sp = L[L.scope & L.has_price].copy()
N = len(L)

# ---- A1 ----
R['A1'] = {'rows': N, 'scope': int(L.scope.sum()), 'scope_priced': len(sp), 'all_priced': int(L.has_price.sum()),
           'priced_but_unparseable': int((L.has_price & L.price_v.isna()).sum())}

# ---- A2 ----
P = L[L.has_price]
ent = P[P.room_type == 'Entire home/apt']
R['A2'] = {'all_priced_median': float(P.price_v.median()),
           'entire_1br': [float(ent[ent.bedrooms == '1'].price_v.median()), int((ent.bedrooms == '1').sum())],
           'entire_2br': [float(ent[ent.bedrooms == '2'].price_v.median()), int((ent.bedrooms == '2').sum())]}

# ---- A3 ----
nb = L.neighbourhood_cleansed.value_counts()
R['A3'] = {'top': nb.index[0], 'n': int(nb.iloc[0]), 'share_pct': round(100 * nb.iloc[0] / N, 2),
           'Sydney_n': int(nb.get('Sydney', 0))}

# ---- A4 ----
hc = pd.to_numeric(L.calculated_host_listings_count, errors='coerce')
cnt_in_file = L.groupby('host_id').id.transform('size')
R['A4'] = {'col_calculated_host_listings_count_ge5_pct': round(100 * (hc >= 5).sum() / N, 2),
           'alt_count_by_host_id_in_file_ge5_pct': round(100 * (cnt_in_file >= 5).sum() / N, 2),
           'alt_host_total_listings_count_ge5_pct': round(100 * (pd.to_numeric(L.host_total_listings_count, errors='coerce') >= 5).sum() / N, 2),
           'host_level_share_of_hosts_with_ge5_pct': round(100 * (L.groupby('host_id').calculated_host_listings_count.first().astype(float) >= 5).mean(), 2)}

# ---- A5 calendar ----
cal = {}
for p in (P12, P03, P06, P09):
    ls = rd(p, ['id', 'calendar_last_scraped'])
    tot = None
    for ch in pd.read_csv(BASE / p / 'data' / 'calendar.csv.gz', usecols=['listing_id', 'date', 'available'],
                          dtype=str, chunksize=2_000_000):
        g = ch.assign(b=(ch.available == 'f').astype(int)).groupby('date').b.agg(['size', 'sum'])
        tot = g if tot is None else tot.add(g, fill_value=0)
    tot = tot.sort_index()
    dts = pd.to_datetime(pd.Series(tot.index), format='%Y-%m-%d').values
    out = {'min_date': str(tot.index[0]), 'max_date': str(tot.index[-1])}
    bases = {'min_date': pd.Timestamp(tot.index[0]),
             'listings_calendar_last_scraped_mode': pd.Timestamp(ls.calendar_last_scraped.mode().iloc[0])}
    for bn, base in bases.items():
        for n in (30, 90):
            m = (dts >= np.datetime64(base)) & (dts < np.datetime64(base + pd.Timedelta(days=n)))
            out[f'{bn}_{n}d_blocked_pct'] = round(100 * float(tot['sum'].values[m].sum() / tot['size'].values[m].sum()), 2)
    cal[p] = out
R['A5'] = cal

# ---- A6 ----
occ = pd.to_numeric(sp.estimated_occupancy_l365d, errors='coerce')
rt_sc = pd.to_numeric(sp.review_scores_rating, errors='coerce')
rt_all = pd.to_numeric(L.review_scores_rating, errors='coerce')
R['A6'] = {'occ_median_scope_priced': float(occ.median()), 'occ_n': int(occ.notna().sum()),
           'rating_median_all_rated': float(rt_all.median()), 'rating_n_all': int(rt_all.notna().sum()),
           'rating_median_scope_priced': float(rt_sc.median()), 'rating_n_scope_priced': int(rt_sc.notna().sum())}

# ---- B1 / B2 / B3 ----
sp['bed'] = sp.bedrooms.astype(int)
R['B1'] = {'over_2000': int((sp.price_v > 2000).sum()), 'model_sample': int((sp.price_v <= 2000).sum())}
c1, c2 = sp[sp.bed == 1], sp[sp.bed == 2]
R['B2'] = {'scope_1br_median': float(c1.price_v.median()), 'n1': len(c1),
           'scope_2br_median': float(c2.price_v.median()), 'n2': len(c2)}
d2 = c2.groupby('neighbourhood_cleansed').price_v.agg(['median', 'size'])
d2 = d2[d2['size'] >= 30].sort_values('median', ascending=False)
R['B2']['top_districts_2br_n_ge30'] = [[k, float(v['median']), int(v['size'])] for k, v in d2.head(3).iterrows()]
R['B3'] = {'A2_population': 'room_type=Entire home/apt, 有價, bedrooms=1/2(不限人數、最低晚數)',
           'B2_population': 'A1 的篩選且有價 6,639 間(整套, 2-4 人, 最低1-7晚)',
           'A2_n': [R['A2']['entire_1br'][1], R['A2']['entire_2br'][1]], 'B2_n': [len(c1), len(c2)],
           'A2_medians': [R['A2']['entire_1br'][0], R['A2']['entire_2br'][0]],
           'B2_medians': [R['B2']['scope_1br_median'], R['B2']['scope_2br_median']]}

# ---- B4 設施同組比較 ----
def parse_amen(s):
    try:
        return frozenset(a.strip() for a in json.loads(s) if isinstance(a, str) and a.strip())
    except (ValueError, TypeError):
        return frozenset()


sp['amen'] = sp.amenities.map(parse_amen)
sp['grp'] = sp.neighbourhood_cleansed + '|' + sp.bedrooms
gsz = sp.grp.map(sp.grp.value_counts())
dg = sp[gsz >= 30].copy()
dg['rel'] = np.log(dg.price_v) - dg.groupby('grp').price_v.transform(lambda x: np.log(x).median())
res = {}
for a in ('Kitchenette', 'Kayak'):
    w = dg.amen.map(lambda s: a in s).values
    res[a] = {'n_with_in_dg': int(w.sum()), 'n_with_all_scope_priced': int(sp.amen.map(lambda s: a in s).sum()),
              'within_group_pct': round(100 * (np.exp(np.median(dg.rel.values[w]) - np.median(dg.rel.values[~w])) - 1), 2)}
# 簡化比較:不取 log 中位的版本(價格除以組內中位)
dg['ratio'] = dg.price_v / dg.groupby('grp').price_v.transform('median')
for a in ('Kitchenette', 'Kayak'):
    w = dg.amen.map(lambda s: a in s).values
    res[a]['alt_ratio_median_pct'] = round(100 * (np.median(dg.ratio.values[w]) / np.median(dg.ratio.values[~w]) - 1), 2)
R['B4'] = {'dg_rows': len(dg), **res}

# ---- B5 ② 全樣本中位數當預測的 MAE ----
ms = sp[sp.price_v <= 2000]
y = ms.price_v.values
R['B5'] = {'n': len(y), 'mae_full_sample_median': round(float(np.abs(y - np.median(y)).mean()), 2)}
# 依 host_id 分組 5 折(訓練折中位數 → 測試折)
hosts = ms.host_id.values
rng = np.random.RandomState(0)
uh = np.unique(hosts)
fold_of = dict(zip(uh, rng.randint(0, 5, len(uh))))
fo = np.array([fold_of[h] for h in hosts])
err = np.zeros(len(y))
for k in range(5):
    te = fo == k
    err[te] = np.abs(y[te] - np.median(y[~te]))
R['B5']['mae_hostgroup_5fold_median'] = round(float(err.mean()), 2)

# ---- C1 / C2 / C3 ----
D = {}
C1 = {}
for p in (P12, P03, P06, P09):
    d = rd(p) if p == P09 else rd(p)
    D[p] = d
    C1[p] = {'rows': len(d), 'cols': d.shape[1], 'priced': int((d.price.str.strip() != '').sum()),
             'host_since_nonempty': int((d.host_since.str.strip() != '').sum())}
R['C1_C2'] = C1
d12 = D[P12]
hsd = pd.to_datetime(d12.host_since, errors='coerce')
lsd = pd.to_datetime(d12.last_scraped)
whole = (lsd.dt.year - hsd.dt.year) * 12 + (lsd.dt.month - hsd.dt.month) - (lsd.dt.day < hsd.dt.day).astype(int)
c3 = {}
for k in ('user', 'host'):
    t = pd.to_numeric(d12[f'hosts_time_as_{k}_years'], errors='coerce') * 12 + pd.to_numeric(d12[f'hosts_time_as_{k}_months'], errors='coerce')
    ok = whole.notna() & t.notna()
    diff = (t - whole)[ok]
    c3[k] = {'n_compared': int(ok.sum()), 'exact_pct': round(100 * (diff == 0).mean(), 2),
             'within1_pct': round(100 * (diff.abs() <= 1).mean(), 2),
             'exact_pct_over_all_rows': round(100 * (diff == 0).sum() / len(d12), 2)}
R['C3'] = c3

# ---- C4 / C5 ----
d9 = L.copy()
fr = pd.to_datetime(d9.first_review.replace('', np.nan), errors='coerce')
m = d9.scope & d9.has_price
R['C4'] = {'first_review_ge_2025-09-17': int((m & (fr >= '2025-09-17')).sum()), 'no_review': int((m & fr.isna()).sum()),
           'before': int((m & (fr < '2025-09-17')).sum())}
ls = pd.to_datetime(d9.last_scraped)
R['C5_base'] = {'last_scraped_min': str(ls.min().date()), 'last_scraped_max': str(ls.max().date())}
mi = lambda s: s.dt.year * 12 + s.dt.month
tmonths = pd.to_numeric(d9.hosts_time_as_host_years, errors='coerce') * 12 + pd.to_numeric(d9.hosts_time_as_host_months, errors='coerce')
start = mi(ls) - tmonths
BIDX = 2026 * 12 + 9
new = start >= BIDX - 12
s2 = d9[m].copy()
s2['new'] = new[m]
s2['p'] = s2.price_v
s2['sup'] = np.where(s2.host_is_superhost.isin(['t', 'f']), (s2.host_is_superhost == 't').astype(float), np.nan)
R['C5'] = {'new_n': int(s2.new.sum()), 'old_n': int((~s2.new).sum()),
           'price_median_new': float(s2[s2.new].p.median()), 'price_median_old': float(s2[~s2.new].p.median()),
           'superhost_pct_new': round(100 * float(s2[s2.new].sup.mean()), 2),
           'superhost_pct_old': round(100 * float(s2[~s2.new].sup.mean()), 2),
           'superhost_pct_new_denom_all': round(100 * float((s2[s2.new].host_is_superhost == 't').mean()), 2),
           'superhost_pct_old_denom_all': round(100 * float((s2[~s2.new].host_is_superhost == 't').mean()), 2)}

# ---- C6 ----
pr = {}
for p in (P03, P06, P09):
    d = D[p]
    pr[p] = pd.Series(pnum(d.price).values, index=d.id.values)
    pr[p] = pr[p][pr[p].notna()]
c = pr[P03].index.intersection(pr[P06].index).intersection(pr[P09].index)
ch = (pr[P09].loc[c] / pr[P03].loc[c] - 1) * 100
c39 = pr[P03].index.intersection(pr[P09].index)
ch39 = (pr[P09].loc[c39] / pr[P03].loc[c39] - 1) * 100
R['C6'] = {'three_period_common_priced': len(c), 'median_change_3to9_pct': round(float(ch.median()), 3),
           'two_period_03_and_09_priced': len(c39), 'median_change_3to9_two_period_pct': round(float(ch39.median()), 3),
           'ids_unique_per_period': {p: bool(D[p].id.is_unique) for p in D}}

print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
