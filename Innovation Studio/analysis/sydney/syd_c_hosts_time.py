"""雪梨 C 分支:新手房東驗證與跨期變化(IS-1111-SYD-C),邏輯與定義照墨爾本版 mel_c_hosts_time.py。可重跑:python -I syd_c_hosts_time.py
讀:scratchpad/insideairbnb_sydney/<期別>/data/listings.csv.gz(唯讀)。
寫:notes/raw/syd_c_hosts_time_2026-11-11.json、notes/figures/syd_c_*.png。
只輸出彙總,不輸出房東姓名、房源名稱、描述、評論文字、個別 host_id / id。
篩選樣本定義照 airbnb_ab_field_inventory.py(整套/1-2房/2-4人/最低1-7晚;有價=price 欄非空)。
年資月數 = years*12 + months;房東開始月 = 該列 last_scraped 的月份序號 - 年資月數(月粒度,誤差約一個月)。
"""
import json
import site
import sys
from pathlib import Path

# python -I 會關掉 user site-packages,這台的 dateutil 裝在那裡;只補回套件目錄,資料夾與 cwd 仍不在 sys.path
sys.path.append(site.getusersitepackages())

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'scratchpad/insideairbnb_sydney'
OUT_JSON = ROOT / 'Innovation Studio/notes/raw/syd_c_hosts_time_2026-11-11.json'
FIG = ROOT / 'Innovation Studio/notes/figures'
P = ['2025-12-12', '2026-03-21', '2026-06-16', '2026-09-16']
P12, P03, P06, P09 = P
SHORT = {P12: '2025-12', P03: '2026-03', P06: '2026-06', P09: '2026-09'}
COLS = {'id', 'host_id', 'last_scraped', 'price', 'room_type', 'bedrooms', 'accommodates', 'minimum_nights',
        'neighbourhood_cleansed', 'first_review', 'host_since', 'hosts_time_as_host_years',
        'hosts_time_as_host_months', 'hosts_time_as_user_years', 'hosts_time_as_user_months',
        'calculated_host_listings_count', 'review_scores_rating', 'amenities', 'number_of_reviews_ltm',
        'host_is_superhost', 'source', 'has_availability', 'availability_365', 'price_quote_checkin_date',
        'price_quote_checkout_date', 'price_quote_price_per_night'}
BATCH = '2026-09-17'  # 2026-09 期 last_scraped 最大值(雪梨實算;沿用舊程式的基準日定義)
BIDX = 2026 * 12 + 9  # 雪梨 BATCH 仍在 2026-09,與墨爾本相同
CUT12 = '2025-09-17'  # 基準日往前 12 個月的同一天(首評代理用,含當天)
EXPECT = {'rows': [20436, 13563, 20573, 20833], 'cols': [85, 90, 90, 90]}  # 雪梨實算
BLUE, ORANGE, GRAY, DARK = '#1f5fa8', '#e07b1a', '#9aa0a6', '#222222'


def midx(s):
    d = pd.to_datetime(s)
    return d.dt.year * 12 + d.dt.month


def pct(a):
    a = np.asarray(a, float)
    return {'n': int(len(a)), **{f'p{q}': round(float(np.percentile(a, q)), 2) for q in (10, 25, 50, 75, 90)}} if len(a) else {'n': 0}


def iqr(s):
    s = pd.Series(s).dropna()
    if not len(s):
        return {'n': 0}
    return {'n': int(len(s)), 'median': round(float(s.median()), 2), 'p25': round(float(s.quantile(.25)), 2),
            'p75': round(float(s.quantile(.75)), 2)}


def load(p):
    df = pd.read_csv(BASE / p / 'data' / 'listings.csv.gz', usecols=lambda c: c in COLS, low_memory=False)
    assert df.id.is_unique
    if 'price' in df:
        df['p'] = pd.to_numeric(df.price.astype(str).str.replace(r'[,$\s]', '', regex=True), errors='coerce')
        assert df.p.notna().sum() == df.price.notna().sum()
    return df


def is_scope(d):
    return ((d.room_type == 'Entire home/apt') & d.bedrooms.isin([1, 2]) & d.accommodates.between(2, 4)
            & d.minimum_nights.between(1, 7))


# ---------------- 讀資料 + 初查重算 ----------------
raw_shape = {}
D = {}
for p in P:
    D[p] = load(p)
    full_cols = len(pd.read_csv(BASE / p / 'data' / 'listings.csv.gz', nrows=0).columns)
    raw_shape[p] = (len(D[p]), full_cols)
assert [raw_shape[p][0] for p in P] == EXPECT['rows'], raw_shape
assert [raw_shape[p][1] for p in P] == EXPECT['cols'], raw_shape
d12, d03, d06, d09 = (D[p] for p in P)
scope09 = d09[is_scope(d09)]
sp = d09[is_scope(d09) & d09.price.notna()].copy()
fr = pd.to_datetime(d09.first_review)
new_proxy_mask = (fr >= CUT12) & is_scope(d09) & d09.price.notna()
assert str(d09.last_scraped.max()) == BATCH, d09.last_scraped.max()
assert len(scope09) == 7565 and len(sp) == 6639 and int(new_proxy_mask.sum()) == 2028, (len(scope09), len(sp), int(new_proxy_mask.sum()))
R = {'meta': {'scope_id': 'IS-1111-SYD-C', 'periods': P, 'batch_date_2026-09': BATCH,
              'scope_def': '整套/1-2房/2-4人/最低1-7晚;有價=price 非空',
              'caveat': '掛牌價(price 欄)不是成交價;年資欄官方說明未查,欄義由資料行為推斷'}}
R['recheck_initial'] = {SHORT[p]: {
    'rows': raw_shape[p][0], 'cols': raw_shape[p][1],
    'host_since_nonnull_pct': round(100 * D[p].host_since.notna().mean(), 1),
    'hosts_time_as_host_years_nonnull_pct': round(100 * D[p].hosts_time_as_host_years.notna().mean(), 1),
    'price_nonnull_pct': round(100 * D[p].price.notna().mean(), 1)} for p in P}
R['recheck_initial']['2026-09_counts'] = {'scope': len(scope09), 'scope_with_price': len(sp), 'first_review_12m_proxy': int(new_proxy_mask.sum())}
single = d09.calculated_host_listings_count == 1
d09['t_host'] = d09.hosts_time_as_host_years * 12 + d09.hosts_time_as_host_months
R['recheck_initial']['2026-09_counts']['proxy_and_single'] = int((new_proxy_mask & single).sum())
R['recheck_initial']['2026-09_counts']['proxy_single_host_months_le_12'] = int((new_proxy_mask & single & (d09.t_host <= 12)).sum())
R['recheck_initial']['dates_last_scraped'] = {SHORT[p]: [D[p].last_scraped.min(), D[p].last_scraped.max()] for p in P}

# ---------------- a. 驗證年資欄 ----------------
ls12 = pd.to_datetime(d12.last_scraped)
hs = pd.to_datetime(d12.host_since)
whole_m = (ls12.dt.year - hs.dt.year) * 12 + (ls12.dt.month - hs.dt.month) - (ls12.dt.day < hs.dt.day).astype(int)
A = {'n_2025-12_rows_with_host_since': int(hs.notna().sum())}
for k in ('host', 'user'):
    t = d12[f'hosts_time_as_{k}_years'] * 12 + d12[f'hosts_time_as_{k}_months']
    diff = (t - whole_m).dropna()
    A[f'vs_host_since_{k}'] = {
        'exact_pct': round(100 * (diff == 0).mean(), 2), 'within_1m_pct': round(100 * (diff.abs() <= 1).mean(), 2),
        'more_than_1m_pct': round(100 * (diff.abs() > 1).mean(), 2),
        'field_shorter_than_1m_pct': round(100 * (diff < -1).mean(), 2), 'field_longer_than_1m_pct': round(100 * (diff > 1).mean(), 2),
        'diff_months_p5_p50_p95': [float(diff.quantile(q)) for q in (.05, .5, .95)], 'diff_months_min': float(diff.min()),
        'years_exact_pct': round(100 * (d12[f'hosts_time_as_{k}_years'] == whole_m // 12).mean(), 2),
        'months_exact_pct': round(100 * (d12[f'hosts_time_as_{k}_months'] == whole_m % 12).mean(), 2)}
th = d12.hosts_time_as_host_years * 12 + d12.hosts_time_as_host_months
tu = d12.hosts_time_as_user_years * 12 + d12.hosts_time_as_user_months
A['host_vs_user_2025-12'] = {'host_le_user_pct': round(100 * (th <= tu).mean(), 2), 'host_eq_user_pct': round(100 * (th == tu).mean(), 2),
                             'host_eq_0_pct': round(100 * (th == 0).mean(), 2), 'gap_user_minus_host_months': pct((tu - th).dropna())}
# 跨期:2026-09 的房東在 2025-12 找得到嗎
h0 = d12.drop_duplicates('host_id').set_index('host_id')
hx = d09.drop_duplicates('host_id').copy()
found = hx.host_id.isin(h0.index)
A['cross_period'] = {'hosts_2026-09': int(len(hx)), 'found_in_2025-12': int(found.sum()), 'found_pct': round(100 * found.mean(), 2),
                     'listing_level_found_pct': round(100 * d09.host_id.isin(h0.index).mean(), 2)}
f = hx[found].copy()
f['hs_idx'] = midx(h0.loc[f.host_id, 'host_since']).values
f['ls_idx'] = midx(f.last_scraped)
for k in ('host', 'user'):
    t = f[f'hosts_time_as_{k}_years'] * 12 + f[f'hosts_time_as_{k}_months']
    dm = (f.ls_idx - t) - f.hs_idx  # 2026-09 年資欄回推的開始月 - 2025-12 host_since 的月
    A['cross_period'][f'{k}_fields_start_month_minus_host_since_month'] = {
        'exact_pct': round(100 * (dm == 0).mean(), 2), 'within_1m_pct': round(100 * (dm.abs() <= 1).mean(), 2),
        'more_than_1m_pct': round(100 * (dm.abs() > 1).mean(), 2), 'p5_p50_p95': [float(dm.quantile(q)) for q in (.05, .5, .95)]}
t9 = f.hosts_time_as_host_years * 12 + f.hosts_time_as_host_months
t0 = (h0.loc[f.host_id, 'hosts_time_as_host_years'] * 12 + h0.loc[f.host_id, 'hosts_time_as_host_months']).values
A['cross_period']['host_field_change_2025-12_to_2026-09_months(實隔約9個月)'] = {str(int(k)): int(v) for k, v in (t9 - t0).value_counts().items()}
A['conclusion'] = ('是別的意思:host_since 對得上 hosts_time_as_user_*(帳號年資),hosts_time_as_host_* 比 host_since 算出的年資短、'
                   '且跨期隨時間同步增加,最可能是「開始當房東以來」的時間;官方說明未查,屬資料行為推斷')
R['a_validate_tenure_fields'] = A

# ---------------- b. 2026-09 每間房補房東開始月 ----------------
d09['ls_idx'] = midx(d09.last_scraped)
d09['start_T'] = d09.ls_idx - d09.t_host  # 當房東起算(hosts_time_as_host_*)
d09['t_user'] = d09.hosts_time_as_user_years * 12 + d09.hosts_time_as_user_months
hs_map = midx(h0.host_since).rename('hs')
d09['hs_idx'] = d09.host_id.map(hs_map)
d09['start_H'] = d09.hs_idx.fillna(d09.ls_idx - d09.t_user)  # 任務單口徑:2025-12 host_since 優先,沒有的用年資欄回推
d09['src_H'] = np.where(d09.hs_idx.notna(), 'host_since(2025-12)', '年資欄回推(約±1個月)')
sc_mask = is_scope(d09)
spm = sc_mask & d09.price.notna()
R['b_start_date_source_H'] = {
    'note': 'H 口徑=任務單版本。年資欄回推用 hosts_time_as_user_*(因 a 證明它才對得上 host_since)',
    'all': d09.src_H.value_counts().to_dict(), 'scope': d09[sc_mask].src_H.value_counts().to_dict(),
    'scope_with_price': d09[spm].src_H.value_counts().to_dict(),
    'T_definition': f'T 口徑=hosts_time_as_host_*(當房東起算),四期 100% 有值,全部 {len(d09):,} 間都用年資欄回推(約±1個月)'}

# ---------------- c. 新手房東定義 ----------------
C = {'window': f'房東開始月 >= 2026-09 往前 12 個月(月粒度);24 個月版同理', 'definitions': {}}
d09['fr_cat'] = np.where(fr.isna(), '無評論', np.where(fr >= CUT12, '12個月內', '12個月前'))
for name, col in (('T_當房東起算(hosts_time_as_host,主口徑)', 'start_T'), ('H_host_since優先(任務單口徑)', 'start_H')):
    n12 = d09[col] >= BIDX - 12
    n24 = d09[col] >= BIDX - 24
    g = {}
    for lab, m in (('all', d09.id.notna()), ('scope', sc_mask), ('scope_with_price', spm)):
        g[lab] = {'new12': int((m & n12).sum()), 'new24': int((m & n24).sum()), 'new12_and_single': int((m & n12 & single).sum()),
                  'new24_and_single': int((m & n24 & single).sum()), 'base': int(m.sum())}
    x = d09[spm].assign(real=n12[spm])
    ct = pd.crosstab(x.fr_cat, x.real).reindex(index=['12個月內', '12個月前', '無評論'], columns=[True, False], fill_value=0)
    both = int(ct.loc['12個月內', True]); proxy_yes = int(ct.loc['12個月內'].sum()); real_yes = int(ct[True].sum())
    C['definitions'][name] = {'counts': g, 'crosstab_scope_price(列=首評分類,欄=真新手12個月)': {k: {'真新手': int(ct.loc[k, True]), '非新手': int(ct.loc[k, False])} for k in ct.index},
                              'proxy_precision_pct(代理說新的裡面真新手)': round(100 * both / proxy_yes, 1),
                              'proxy_recall_pct(真新手裡被代理抓到)': round(100 * both / real_yes, 1),
                              'proxy_yes': proxy_yes, 'real_yes': real_yes, 'both': both}
R['c_new_host_definition'] = C

# ---------------- d. 新手 vs 老手(2026-09 篩選且有價,主口徑 T) ----------------
sp = d09[spm].copy()
sp['new'] = sp.start_T >= BIDX - 12
sp['grp'] = sp.neighbourhood_cleansed + '|' + sp.bedrooms.astype(int).astype(str)
sz = sp.groupby('grp').p.transform('size')
sp['prank'] = np.where(sz >= 20, sp.groupby('grp').p.rank(pct=True) * 100, np.nan)
sp['n_amen'] = sp.amenities.map(lambda s: len(json.loads(s)) if isinstance(s, str) and s.startswith('[') else np.nan)
sp['super'] = np.where(sp.host_is_superhost.isin(['t', 'f']), (sp.host_is_superhost == 't').astype(float), np.nan)
sp['rated'] = sp.review_scores_rating.notna().astype(float)
METRICS = [('price', 'p', '掛牌價中位數(澳幣/晚)'), ('prank', 'prank', '同組價格百分位中位數'), ('rating', 'review_scores_rating', '評分中位數(有評分者)'),
           ('rated_share', 'rated', '有評分比例'), ('amenities', 'n_amen', '設施數中位數'), ('reviews_ltm', 'number_of_reviews_ltm', '近一年評論數中位數'),
           ('min_nights', 'minimum_nights', '最少入住晚數中位數'), ('superhost_share', 'super', '超讚房東比例')]
Dd = {'sample': {'new': int(sp.new.sum()), 'old': int((~sp.new).sum()), 'group_min_size': 20,
                 'in_group_n_listings': int(sp.prank.notna().sum()), 'groups_ge_20': int((sp.groupby('grp').size() >= 20).sum())}, 'metrics': {}}
for key, col, label in METRICS:
    Dd['metrics'][key] = {'label': label, 'new': iqr(sp.loc[sp.new, col]), 'old': iqr(sp.loc[~sp.new, col])}
    if key in ('rated_share', 'superhost_share'):
        for s, m in (('new', sp.new), ('old', ~sp.new)):
            v = sp.loc[m, col].dropna(); Dd['metrics'][key][s]['share_pct'] = round(100 * float(v.mean()), 1)
R['d_new_vs_veteran'] = Dd
R['d_new_vs_veteran']['sensitivity_H'] = {'new_n': int((sp.start_H >= BIDX - 12).sum()),
                                           'price_median_new': round(float(sp.loc[sp.start_H >= BIDX - 12, 'p'].median()), 1),
                                           'price_median_old': round(float(sp.loc[sp.start_H < BIDX - 12, 'p'].median()), 1),
                                           'prank_median_new': round(float(sp.loc[sp.start_H >= BIDX - 12, 'prank'].median()), 1),
                                           'prank_median_old': round(float(sp.loc[sp.start_H < BIDX - 12, 'prank'].median()), 1)}

# ---------------- e. 四期進出 + 3 月為何少 ----------------
ids = {p: set(D[p].id) for p in P}
E = {'flows': {}}
for a, b in zip(P[:-1], P[1:]):
    E['flows'][f'{SHORT[a]}到{SHORT[b]}'] = {'stay': len(ids[a] & ids[b]), 'gone': len(ids[a] - ids[b]), 'new': len(ids[b] - ids[a])}
absent = (ids[P12] & ids[P06]) - ids[P03]
present = ids[P12] & ids[P03] & ids[P06]


def prof06(idset):
    x = d06[d06.id.isin(idset)]
    return {'n': int(len(x)), 'price_nonnull_pct': round(100 * x.price.notna().mean(), 1),
            'has_availability': {str(k): round(100 * v, 1) for k, v in x.has_availability.value_counts(normalize=True, dropna=False).items()},
            'availability_365_eq_0_pct': round(100 * (x.availability_365 == 0).mean(), 1),
            'source': {str(k) if pd.notna(k) else '(空白)': int(v) for k, v in x.source.value_counts(dropna=False).items()},
            'reviews_ltm_eq_0_pct': round(100 * (x.number_of_reviews_ltm == 0).mean(), 1)}


def prof12(idset):
    x = d12[d12.id.isin(idset)]
    return {'n': int(len(x)), 'availability_365_eq_0_pct': round(100 * (x.availability_365 == 0).mean(), 1),
            'has_availability': {str(k): round(100 * v, 1) for k, v in x.has_availability.value_counts(normalize=True, dropna=False).items()},
            'reviews_ltm_eq_0_pct': round(100 * (x.number_of_reviews_ltm == 0).mean(), 1)}


E['march_absent_but_in_12_and_06'] = {'n': len(absent), 'in_06': prof06(absent), 'in_12': prof12(absent)}
E['march_present_and_in_12_and_06'] = {'n': len(present), 'in_06': prof06(present), 'in_12': prof12(present)}
gone03 = ids[P12] - ids[P03]
E['gone_in_03_returned_in_06_pct'] = round(100 * len(gone03 & ids[P06]) / len(gone03), 1)
E['gone_in_03_n'] = len(gone03)
E['source_distribution_all_rows'] = {SHORT[p]: {str(k) if pd.notna(k) else '(空白)': int(v) for k, v in D[p].source.value_counts(dropna=False).items()} for p in P[1:]}
E['price_nonnull_pct_all'] = {SHORT[p]: round(100 * D[p].price.notna().mean(), 1) for p in P[1:]}
R['e_flows_and_march'] = E

# ---------------- f. 同一間房價格變化 ----------------
pr = {p: D[p].set_index('id') for p in (P03, P06, P09)}
common = sorted(set(pr[P03].index[pr[P03].p.notna()]) & set(pr[P06].index[pr[P06].p.notna()]) & set(pr[P09].index[pr[P09].p.notna()]))
c3, c6, c9 = (pr[p].loc[common, 'p'] for p in (P03, P06, P09))
chg = {'3到6': (c6 / c3 - 1) * 100, '6到9': (c9 / c6 - 1) * 100, '3到9': (c9 / c3 - 1) * 100}
F = {'n_common_priced_in_03_06_09': len(common), 'change_pct': {}, 'quote_dates': {}}
for k, v in chg.items():
    F['change_pct'][k] = {**pct(v), 'unchanged_pct': round(100 * float((np.abs(v) < 1e-9).mean()), 1),
                          'up_pct': round(100 * float((v > 1e-9).mean()), 1), 'down_pct': round(100 * float((v < -1e-9).mean()), 1)}
for p in (P03, P06, P09):
    q = pr[p].loc[common]
    ci = pd.to_datetime(q.price_quote_checkin_date); co = pd.to_datetime(q.price_quote_checkout_date)
    nights = (co - ci).dt.days
    al = pr[p][pr[p].p.notna()]
    F['quote_dates'][SHORT[p]] = {
        'checkin_top5': {str(k.date()): int(v) for k, v in ci.value_counts().head(5).items()}, 'checkin_distinct': int(ci.nunique()),
        'checkin_missing': int(ci.isna().sum()), 'nights': {str(int(k)): int(v) for k, v in nights.value_counts().head(5).items()},
        'checkin_weekday_of_mode': ci.mode().iloc[0].day_name() if ci.notna().any() else None,
        'distinct_all_priced_rows': int(pd.to_datetime(al.price_quote_checkin_date).nunique()),
        'price_equals_quote_per_night_pct': round(100 * float((np.abs(q.p - q.price_quote_price_per_night) < 0.01).mean()), 1)}
# 較乾淨的子集:兩期報價「同星期幾入住、同晚數」才比(季節仍不同,只排除星期與晚數的差)
cin = {p: pd.to_datetime(pr[p].loc[common, 'price_quote_checkin_date']) for p in (P03, P06, P09)}
ngt = {p: (pd.to_datetime(pr[p].loc[common, 'price_quote_checkout_date']) - cin[p]).dt.days for p in (P03, P06, P09)}
F['same_weekday_and_nights_subset'] = {}
for (a, b), lab in (((P03, P06), '3到6'), ((P06, P09), '6到9'), ((P03, P09), '3到9')):
    m = ((cin[a].dt.dayofweek == cin[b].dt.dayofweek) & (ngt[a] == ngt[b])).values
    v = chg[lab][m]
    F['same_weekday_and_nights_subset'][lab] = {**pct(v), 'unchanged_pct': round(100 * float((np.abs(v) < 1e-9).mean()), 1),
                                                'share_of_common_pct': round(100 * float(m.mean()), 1)}
F['quote_weekday_dist_pct'] = {SHORT[p]: {str(k): round(100 * v, 1) for k, v in cin[p].dt.day_name().value_counts(normalize=True).items()} for p in (P03, P06, P09)}
dist = pr[P09].loc[common, 'neighbourhood_cleansed']
df_ = pd.DataFrame({'d': dist.values, 'c': chg['3到9'].values})
gd = df_.groupby('d').c.agg(['size', 'median']).query('size >= 30').sort_values('median')
F['district_3_to_9_median_pct(n>=30)'] = {k: {'n': int(r['size']), 'median_pct': round(float(r['median']), 2)} for k, r in gd.iterrows()}
F['districts_total_in_common'] = int(df_.d.nunique()); F['districts_n_ge_30'] = int(len(gd))
R['f_price_change'] = F

# ---------------- g. 新手第一年怎麼調價 ----------------
d12i = d12.set_index('id')
G = {}
for name, newfun in (('T_當房東起算(主口徑)', lambda x: x.hosts_time_as_host_years * 12 + x.hosts_time_as_host_months <= 12),
                     ('H_host_since(任務單口徑)', lambda x: midx(x.host_since) >= midx(x.last_scraped) - 12)):
    isnew = newfun(d12i.loc[[i for i in common if i in d12i.index]])
    out = {}
    for lab, ids_ in (('新手(2025-12 時開始未滿12個月)', isnew[isnew].index), ('老手', isnew[~isnew].index)):
        a3, a6, a9 = (pr[p].loc[ids_, 'p'] for p in (P03, P06, P09))
        out[lab] = {'n': int(len(ids_)), 'median_price_03_06_09': [round(float(a.median()), 1) for a in (a3, a6, a9)],
                    'median_change_vs_03_pct': {'03到06': round(float(((a6 / a3 - 1) * 100).median()), 2), '03到09': round(float(((a9 / a3 - 1) * 100).median()), 2),
                                                '06到09': round(float(((a9 / a6 - 1) * 100).median()), 2)},
                    'unchanged_03_to_09_pct': round(100 * float((np.abs(a9 / a3 - 1) < 1e-9).mean()), 1),
                    'enough_n_ge_30': bool(len(ids_) >= 30)}
    G[name] = out
G['n_common_also_in_2025-12'] = int(sum(i in d12i.index for i in common))
R['g_first_year_price_path'] = G

# ---------------- 圖 ----------------
def setup_font():
    have = {x.name for x in font_manager.fontManager.ttflist}
    for nm in ('Microsoft JhengHei', 'Microsoft YaHei', 'SimHei'):
        if nm in have:
            plt.rcParams['font.sans-serif'] = [nm]
            break
    else:
        raise SystemExit('找不到中文字型')
    plt.rcParams.update({'axes.unicode_minus': False, 'font.size': 12, 'axes.titlesize': 13, 'axes.labelsize': 12,
                         'xtick.labelsize': 12, 'ytick.labelsize': 12, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
                         'axes.spines.top': False, 'axes.spines.right': False})


def head(fig, title, sub, foot):
    fig.text(0.015, 0.965, title, fontsize=18, fontweight='bold', color=DARK, va='top')
    fig.text(0.015, 0.915, sub, fontsize=12, color='#555555', va='top')
    fig.text(0.015, 0.012, foot, fontsize=12, color='#555555', va='bottom')


setup_font()
FIG.mkdir(parents=True, exist_ok=True)
# 圖 d
fig, axs = plt.subplots(2, 4, figsize=(14, 8.4), dpi=100)
for ax, (key, col, label) in zip(axs.ravel(), METRICS):
    m = Dd['metrics'][key]
    share = key in ('rated_share', 'superhost_share')
    for x, s, c in ((0, 'new', ORANGE), (1, 'old', BLUE)):
        if share:
            v = m[s]['share_pct']; ax.bar(x, v, color=c, width=.55); ax.text(x, v + 1.5, f'{v:.0f}%', ha='center', fontsize=12, color=DARK)
        else:
            ax.vlines(x, m[s]['p25'], m[s]['p75'], color=c, lw=6, alpha=.45)
            ax.plot(x, m[s]['median'], 'o', color=c, ms=11)
            ax.text(x + .12, m[s]['median'], f"{m[s]['median']:g}", va='center', fontsize=12, color=DARK)
    ax.set_xlim(-.6, 1.6); ax.set_xticks([0, 1])
    ax.set_xticklabels([f"新手\n(n={m['new']['n']})", f"老手\n(n={m['old']['n']})"])
    ax.set_title(label, fontsize=12, color=DARK)
    if share:
        ax.set_ylim(0, 115)
    else:
        lo = min(m['new']['p25'], m['old']['p25']); hi = max(m['new']['p75'], m['old']['p75']); pad = (hi - lo) * .25 + 1e-6
        ax.set_ylim(lo - pad if key != 'prank' else 0, hi + pad if key != 'prank' else 100)
    ax.grid(axis='y', color='#e5e5e5')
fig.subplots_adjust(top=.80, bottom=.12, left=.05, right=.985, hspace=.5, wspace=.35)
head(fig, '雪梨新手房東 vs 老手:定價與口碑', f"2026-09 篩選且有價樣本 {len(sp):,} 間(新手 = 開始當房東 12 個月內);點 = 中位數,粗線 = 四分位距(比例題為長條)",
     '掛牌價不是成交價;「開始當房東」由年資欄回推,誤差約一個月;同組 = 區 x 房間數,組內至少 20 間')
fig.savefig(FIG / 'syd_c_newbie_vs_veteran.png'); plt.close(fig)

# 圖 f
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 11), dpi=100, gridspec_kw={'width_ratios': [1, 1.15]})  # 雪梨有 37 區,圖加高才不擠
v = chg['3到9'].clip(-50, 80)
a1.hist(v, bins=np.arange(-50, 81, 5), color=GRAY)
a1.axvline(0, color=DARK, lw=1)
a1.axvline(F['change_pct']['3到9']['p50'], color=ORANGE, lw=3)
a1.text(F['change_pct']['3到9']['p50'] + 12, a1.get_ylim()[1] * .95, f"中位數 {F['change_pct']['3到9']['p50']:+.1f}%", color=ORANGE, fontsize=12, fontweight='bold')
a1.set_xlabel('2026-03 到 2026-09 掛牌價變動(%,超出範圍的併入兩端)'); a1.set_ylabel('房源數')
a1.set_title(f"同一間房 3 月到 9 月的變動(n={len(common):,};完全沒變 {F['change_pct']['3到9']['unchanged_pct']:.0f}%)", fontsize=12)
yy = np.arange(len(gd))
a2.barh(yy, gd['median'], color=BLUE)
a2.set_yticks(yy); a2.set_yticklabels([f"{k}(n={int(n)})" for k, n in zip(gd.index, gd['size'])], fontsize=11)
a2.axvline(0, color=DARK, lw=1)
for y, val in zip(yy, gd['median']):
    a2.text(val + .15 if val >= 0 else .15, y, f'{val:+.1f}', va='center', ha='left', fontsize=12)
a2.set_xlim(-8.5, 9)  # 雪梨各區範圍 -6.7 ~ +6.4
a2.set_xlabel('各區 3 月到 9 月變動中位數(%)'); a2.set_title(f'分區(該區至少 30 間,共 {len(gd)} 區)', fontsize=12)
qd = F['quote_dates']
fig.subplots_adjust(top=.80, bottom=.14, left=.04, right=.985, wspace=.75)
head(fig, '雪梨同一間房的掛牌價,3 月到 9 月變了多少',
     f"2026-03、06、09 三期都有價的 {len(common):,} 間;三期報價入住日最常見:{', '.join(list(qd[SHORT[p]]['checkin_top5'])[0] for p in (P03, P06, P09))}(季節不同,價差可能含季節)",
     '掛牌價不是成交價;三期報價入住日不同,不能全當成房東調價')
fig.savefig(FIG / 'syd_c_price_change_3_to_9.png'); plt.close(fig)

# 圖 g
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.2), dpi=100)
xs = [0, 1, 2]
gk = G['T_當房東起算(主口徑)']
nk, ok = list(gk)[0], list(gk)[1]
for lab, c, nm in ((nk, ORANGE, '新手'), (ok, BLUE, '老手')):
    r = gk[lab]; lv = r['median_price_03_06_09']
    a1.plot(xs, lv, '-o', color=c, lw=3, ms=9, label=f"{nm}(n={r['n']})")
    ch = [0, r['median_change_vs_03_pct']['03到06'], r['median_change_vs_03_pct']['03到09']]
    a2.plot(xs, ch, '-o', color=c, lw=3, ms=9, label=f"{nm}(n={r['n']})")
    off = 1 if nm == '新手' else -1
    # 雪梨:新手價格水準低於老手(墨爾本相反),價格圖標籤方向反過來才不會互相壓到
    off1 = -off if gk[nk]['median_price_03_06_09'][0] < gk[ok]['median_price_03_06_09'][0] else off
    for x, y in zip(xs, lv):
        if x == 2:
            a1.text(x + .08, y, f'{y:g}', ha='left', va='center', color=c, fontsize=12, fontweight='bold')
        elif x == 1:  # V 形谷底:標籤放兩側(新手右、老手左),不壓到線
            a1.text(x + (.08 if nm == '新手' else -.08), y, f'{y:g}', ha='left' if nm == '新手' else 'right', va='center', color=c, fontsize=12, fontweight='bold', bbox=dict(fc='white', ec='none', pad=1.5, alpha=.85))
        else:
            a1.text(x, y + off1 * 2.0, f'{y:g}', ha='center', va='bottom' if off1 > 0 else 'top', color=c, fontsize=12, fontweight='bold')
    for x, y in zip(xs, ch):
        if x == 2:
            a2.text(x + .08, y, f'{y:+.1f}', ha='left', va='center', color=c, fontsize=12, fontweight='bold')
        elif x == 1:
            a2.text(x + (.08 if nm == '新手' else -.08), y, f'{y:+.1f}', ha='left' if nm == '新手' else 'right', va='center', color=c, fontsize=12, fontweight='bold', bbox=dict(fc='white', ec='none', pad=1.5, alpha=.85))
        # x=0 是基準(定義上都是 0),不標,免得兩個 +0.0 疊在一起
for ax, yl, t in ((a1, '掛牌價中位數(澳幣/晚)', '價格水準'), (a2, '相對 3 月的變動中位數(%)', '相對 3 月')):
    ax.set_xticks(xs); ax.set_xticklabels(['2026-03', '2026-06', '2026-09']); ax.set_ylabel(yl); ax.set_title(t, fontsize=12)
    ax.legend(frameon=False, fontsize=12); ax.grid(axis='y', color='#e5e5e5')
a1.set_xlim(-.3, 2.6); a2.set_xlim(-.3, 2.6); a1.set_ylim(305, 360); a2.set_ylim(-4.6, 2.0)  # 雪梨實算範圍(墨爾本版是 247-272 / -0.3-1.9)
fig.subplots_adjust(top=.76, bottom=.14, left=.07, right=.985, wspace=.25)
head(fig, '新手房東第一年怎麼調價(雪梨)', '2025-12 時開始當房東未滿 12 個月 = 新手;只含 3、6、9 月都有價的同一批房源',
     '掛牌價不是成交價;三期報價入住日季節不同,看相對差別(新手 vs 老手)比看絕對漲跌可靠')
fig.savefig(FIG / 'syd_c_newbie_first_year_price_path.png'); plt.close(fig)

OUT_JSON.write_text(json.dumps(R, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, 'item') else str(o)) + '\n', encoding='utf-8')
print('wrote', OUT_JSON.relative_to(ROOT))
