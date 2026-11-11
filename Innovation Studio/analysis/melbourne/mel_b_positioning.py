"""墨爾本 B 分支:競品定位 + 掛牌價模型實驗(IS-1111-MEL-B)。可重跑:python mel_b_positioning.py
資料:scratchpad/insideairbnb_melbourne/<期別>/data/listings.csv.gz(唯讀);主體 2026-09-16,時間外部檢查用 2026-06-16。
樣本 = 篩選(整套/1-2房/2-4人/最低1-7晚,定義同 airbnb_ab_field_inventory.py)且 price 非空。
只讀數值/類別/日期與 amenities 欄;不讀房東姓名、房源名稱、描述、評論文字。固定隨機種子 SEED。
輸出:notes/raw/mel_b_positioning_2026-11-11.json、notes/figures/mel_b_*.png
"""
import json
import os
import re
from pathlib import Path

os.environ.setdefault('LOKY_MAX_CPU_COUNT', '4')  # 只為了關掉 joblib 找不到實體核心數的警告

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from sklearn.ensemble import HistGradientBoostingRegressor  # noqa: E402
from sklearn.linear_model import Ridge  # noqa: E402
from sklearn.model_selection import GroupKFold, KFold  # noqa: E402
from sklearn.pipeline import make_pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

SEED = 42
ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'scratchpad/insideairbnb_melbourne'
MAIN, PREV = '2026-09-16', '2026-06-16'
OUT_JSON = ROOT / 'Innovation Studio/notes/raw/mel_b_positioning_2026-11-11.json'
FIG = ROOT / 'Innovation Studio/notes/figures'
EXPECT = {'rows': 25715, 'scope': 10940, 'scope_price': 8223, 'new12': 2056}
MIN_GROUP = 30          # 組太小的門檻
K_NEAR = 30             # 退回規則:同房間數、最近的 30 間
TOP_N_AMEN = 40         # 模型用的設施旗標數(依出現比例取前 N,不看價格)
TOP5_NB = 5
EXTREME_CAP = 2000      # 每晚 > 2,000 澳幣視為極端值:不進模型訓練與主要誤差;分位數類統計仍用全部
USECOLS = ['id', 'host_id', 'room_type', 'property_type', 'accommodates', 'bedrooms', 'beds', 'bathrooms_text',
           'neighbourhood_cleansed', 'latitude', 'longitude', 'minimum_nights', 'price', 'amenities',
           'first_review', 'last_scraped', 'calculated_host_listings_count']
FEATURES_ALLOWED = ['neighbourhood_cleansed(區)', 'latitude/longitude', 'property_type(房型細類)', 'bedrooms',
                    'accommodates', 'beds', 'bathrooms_text(解析成浴室數)', 'amenities(設施數 + 前 40 項旗標)',
                    'minimum_nights']
FEATURES_BANNED = {
    'number_of_reviews*, review_scores_*, first_review, last_review, reviews_per_month': '新房東上架前沒有評論',
    'estimated_occupancy_l365d, estimated_revenue_l365d': 'revenue = price × occupancy,直接洩漏答案;occupancy 由評論推算',
    'availability_*': '是上架後的行事曆結果,新房東沒有',
    'price_quote_*': '跟價格直接相關(報價本身)',
    'host_is_superhost, host_listings_count 等房東經營資料': '新房東沒有;房東名下房源數只放在對照版本',
}
BLUE, ORANGE, GRAY, DARK = '#1f5fa8', '#e07b1a', '#9aa0a6', '#222222'
SUB_MODEL = ''  # main() 裡依模型樣本數填入
SUB = f'墨爾本 {MAIN} 期;篩選且有價 8,223 間(整套、1–2 房、2–4 人、最低 1–7 晚);掛牌價不是成交價'


# ---------------- 讀檔與清理 ----------------
def load(period):
    return pd.read_csv(DATA / period / 'data/listings.csv.gz', dtype=str, keep_default_na=False, usecols=USECOLS)


def scope(df):
    acc = pd.to_numeric(df.accommodates.where(df.accommodates.str.isdigit()), errors='coerce')
    mn = pd.to_numeric(df.minimum_nights.where(df.minimum_nights.str.isdigit()), errors='coerce')
    m = (df.room_type == 'Entire home/apt') & df.bedrooms.isin(['1', '2']) & acc.between(2, 4) & mn.between(1, 7)
    return df[m].copy()


def parse_bath(s):
    s = s.strip().lower()
    if not s:
        return np.nan
    if 'half' in s:
        return 0.5
    m = re.search(r'(\d+(\.\d+)?)', s)
    return float(m.group(1)) if m else np.nan


def parse_amen(s):
    try:
        return frozenset(a.strip() for a in json.loads(s) if isinstance(a, str) and a.strip())
    except (ValueError, TypeError):
        return frozenset()


def prep(sc):
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
    d['beds_n'] = beds.fillna(d.bed_n)            # 床數缺 → 用房間數補 + 缺值旗標
    d['baths'] = d.bathrooms_text.map(parse_bath)
    d['baths_missing'] = d.baths.isna().astype(int)
    d['baths'] = d.baths.fillna(1.0)
    d['amen'] = d.amenities.map(parse_amen)
    d['amen_n'] = d.amen.map(len)
    d['hostcnt'] = pd.to_numeric(d.calculated_host_listings_count, errors='coerce').fillna(1)
    d['nb'] = d.neighbourhood_cleansed
    d['grp'] = d.nb + '|' + d.bedrooms
    d['y'] = np.log(d.price_num)
    return d.reset_index(drop=True)


def months_back(day, n):
    y, m = int(day[:4]), int(day[5:7]) - n
    while m <= 0:
        m, y = m + 12, y - 1
    return f'{y:04d}-{m:02d}-{day[8:10]}'


def q(a, ps=(10, 25, 50, 75, 90)):
    return {f'p{p}': round(float(np.percentile(a, p)), 1) for p in ps}


# ---------------- 比較組 / B1 ----------------
def km(lat0, lon0, lat, lon):
    return np.hypot((lat - lat0) * 111.0, (lon - lon0) * 111.0 * np.cos(np.radians(lat0)))


def b1_predict(tr, te):
    """區×房間數 訓練集中位數;該組訓練集不足 30 間 → 同房間數、經緯度最近 30 間的中位數。"""
    st = tr.groupby('grp').price_num.agg(['median', 'size'])
    pools = {b: (tr.lat.values[tr.bed_n.values == b], tr.lon.values[tr.bed_n.values == b],
                 tr.price_num.values[tr.bed_n.values == b]) for b in (1, 2)}
    out, lvl = np.empty(len(te)), np.empty(len(te), int)
    for i, (g, b, la, lo) in enumerate(zip(te.grp.values, te.bed_n.values, te.lat.values, te.lon.values)):
        if g in st.index and st.at[g, 'size'] >= MIN_GROUP:
            out[i], lvl[i] = st.at[g, 'median'], 1
        else:
            pla, plo, pp = pools[b]
            idx = np.argpartition(km(la, lo, pla, plo), K_NEAR)[:K_NEAR]
            out[i], lvl[i] = np.median(pp[idx]), 2
    return out, lvl


# ---------------- 特徵 ----------------
class Spec:
    def __init__(self, d):
        cnt = pd.Series([a for s in d.amen for a in s]).value_counts()
        self.top_amen = list(cnt.index[:TOP_N_AMEN])
        self.nb_levels = sorted(d.nb.unique())
        ptc = d.property_type.value_counts()
        self.pt_levels = sorted(ptc.index[ptc >= 30]) + ['Other']


def flags(d, spec):
    return np.array([[a in s for a in spec.top_amen] for s in d.amen], float).reshape(len(d), len(spec.top_amen))


def X_lin(d, spec, host=False):
    nb = np.array([[v == lv for lv in spec.nb_levels[1:]] for v in d.nb], float)
    num = d[['bed_n', 'acc', 'beds_n', 'beds_missing', 'baths', 'amen_n']].values.astype(float)
    cols = [nb, num, flags(d, spec)]
    names = [f'區={lv}' for lv in spec.nb_levels[1:]] + ['房間數', '可住人數', '床數', '床數缺值', '浴室數', '設施數'] + \
            [f'設施:{a}' for a in spec.top_amen]
    if host:
        cols.append(np.log1p(d[['hostcnt']].values))
        names.append('房東名下房源數(log)')
    return np.hstack(cols), names


def X_tree(d, spec, host=False):
    nbmap = {v: i for i, v in enumerate(spec.nb_levels)}
    ptmap = {v: i for i, v in enumerate(spec.pt_levels)}
    nb = d.nb.map(nbmap).astype(float).values
    pt = d.property_type.map(lambda v: ptmap.get(v, ptmap['Other'])).astype(float).values
    num = d[['lat', 'lon', 'bed_n', 'acc', 'beds_n', 'baths', 'min_n', 'amen_n']].values.astype(float)
    cols = [nb[:, None], pt[:, None], num, flags(d, spec)]
    names = ['區', '房型細類', '緯度', '經度', '房間數', '可住人數', '床數', '浴室數', '最少入住晚數', '設施數'] + \
            [f'設施:{a}' for a in spec.top_amen]
    if host:
        cols.append(d[['hostcnt']].values.astype(float))
        names.append('房東名下房源數')
    return np.hstack(cols), names


def make_tree(nfeat):
    mask = np.zeros(nfeat, bool)
    mask[:2] = True
    return HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20,
                                         l2_regularization=1.0, categorical_features=mask, random_state=SEED)


def fit_predict(method, tr, te, spec):
    if method == 'B0':
        return np.full(len(te), np.median(tr.price_num))
    if method == 'B1':
        return b1_predict(tr, te)[0]
    host = method.endswith('_host')
    if method.startswith('M1'):
        Xtr, _ = X_lin(tr, spec, host)
        Xte, _ = X_lin(te, spec, host)
        m = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(Xtr, tr.y)
    else:
        Xtr, _ = X_tree(tr, spec, host)
        Xte, _ = X_tree(te, spec, host)
        m = make_tree(Xtr.shape[1]).fit(Xtr, tr.y)
    return np.exp(m.predict(Xte))


def metrics(y, p):
    ae = np.abs(p - y)
    ape = ae / y
    return {'n': int(len(y)), 'MAE_aud': round(float(ae.mean()), 1), 'MdAPE_pct': round(float(100 * np.median(ape)), 1),
            'within20_pct': round(float(100 * np.mean(ape <= 0.2)), 1)}


METHODS = ['B0', 'B1', 'M1', 'M2', 'M1_host', 'M2_host']
METHOD_LABEL = {'B0': 'B0 全市中位數', 'B1': 'B1 區×房間數中位數', 'M1': 'M1 線性(Ridge)', 'M2': 'M2 梯度提升樹',
                'M1_host': 'M1 + 房東房源數(對照)', 'M2_host': 'M2 + 房東房源數(對照)'}


def run_cv(d, spec, how):
    folds = (GroupKFold(5).split(d, groups=d.host_id) if how == 'group'
             else KFold(5, shuffle=True, random_state=SEED).split(d))
    oof = {m: np.zeros(len(d)) for m in METHODS}
    for tr_i, te_i in folds:
        tr, te = d.iloc[tr_i], d.iloc[te_i]
        for m in METHODS:
            oof[m][te_i] = fit_predict(m, tr, te, spec)
    return oof


# ---------------- 圖 ----------------
def setup_font():
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in ('Microsoft JhengHei', 'Microsoft YaHei', 'SimHei'):
        if name in have:
            plt.rcParams['font.sans-serif'] = [name]
            break
    else:
        raise SystemExit('找不到中文字型')
    plt.rcParams.update({'font.family': 'sans-serif', 'axes.unicode_minus': False, 'font.size': 12})


def style(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(GRAY)
    ax.spines['bottom'].set_color(GRAY)
    ax.tick_params(colors=DARK, labelsize=12)


def titles(fig, main, sub=SUB, y0=0.97, gap=0.045):
    fig.text(0.02, y0, main, fontsize=17, fontweight='bold', color=DARK, va='top')
    fig.text(0.02, y0 - gap, sub, fontsize=12, color='#555555', va='top')


def fig_positioning(pos, top10):
    fig, ax = plt.subplots(figsize=(8.75, 7.2), dpi=160)
    h = 0.36
    xmax = 0
    for i, nb in enumerate(top10):
        for b, dy, c in (('1', -h / 2, BLUE), ('2', h / 2, ORANGE)):
            cell = pos[nb]['by_bedrooms'].get(b)
            if not cell:
                continue
            y = i + dy
            ax.barh(y, cell['p75'] - cell['p25'], left=cell['p25'], height=h * 0.85, color=c, alpha=0.55)
            ax.plot(cell['p50'], y, 'o', color=c, markersize=7, markeredgecolor=DARK, markeredgewidth=0.8)
            ax.text(cell['p75'] + 6, y, f"{cell['p50']:.0f}(n={cell['n']:,})", va='center', fontsize=12, color=DARK)
            xmax = max(xmax, cell['p75'])
    from matplotlib.patches import Patch
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10)
    ax.invert_yaxis()
    ax.set_xlim(0, xmax + 150)
    ax.set_xlabel('每晚掛牌價(澳幣);橫條 = p25 到 p75,圓點 = 中位數,括號 = 房源數', fontsize=12)
    ax.legend(handles=[Patch(color=BLUE, alpha=0.55, label='1 房'), Patch(color=ORANGE, alpha=0.55, label='2 房')],
              loc='lower right', frameon=False, fontsize=12)
    style(ax)
    fig.subplots_adjust(left=0.2, right=0.97, top=0.86, bottom=0.1)
    titles(fig, '前 10 大區的掛牌價區間(1 房 vs 2 房)')
    fig.savefig(FIG / 'mel_b_positioning_top10.png', facecolor='white')
    plt.close(fig)


def fig_amenity(rows):
    fig, ax = plt.subplots(figsize=(8.75, 8.0), dpi=160)
    h = 0.38
    for i, r in enumerate(rows):
        ax.barh(i - h / 2, r['within_group_pct'], height=h * 0.9, color=BLUE, label='同組比較(區×房間數)' if i == 0 else None)
        ax.barh(i + h / 2, r['regression_pct'], height=h * 0.9, color=ORANGE, label='迴歸控制後' if i == 0 else None)
    ax.axvline(0, color=GRAY, lw=1)
    ax.axhline(9.5, color=GRAY, lw=0.8, ls='--')
    labels = [f"{r['amenity'] if len(r['amenity']) <= 34 else r['amenity'][:32] + '...'}(有 {r['n_with']:,})"
              for r in rows]
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(labels, fontsize=12)
    ax.invert_yaxis()
    ax.set_xlabel('有這項設施的同類房源,掛牌價中位數高(負值 = 低)多少 %', fontsize=12)
    ax.legend(loc='lower right', frameon=False, fontsize=12)
    style(ax)
    fig.subplots_adjust(left=0.45, right=0.97, top=0.86, bottom=0.09)
    titles(fig, '設施與掛牌價的關聯:正向前 10、負向前 5', SUB.replace('(整套、1–2 房、2–4 人、最低 1–7 晚)', '') +
           '\n是關聯不是因果:「有這項設施的同類房源掛牌價較高」,不是「裝了會漲」', gap=0.04)
    fig.savefig(FIG / 'mel_b_amenity_price.png', facecolor='white')
    plt.close(fig)


def fig_mae(res_g, res_r):
    fig, ax = plt.subplots(figsize=(8.75, 5.6), dpi=160)
    h = 0.38
    for i, m in enumerate(METHODS):
        g, r = res_g[m]['all']['MAE_aud'], res_r[m]['all']['MAE_aud']
        ax.barh(i - h / 2, g, height=h * 0.9, color=BLUE, label='依房東分組切(主結果)' if i == 0 else None)
        ax.barh(i + h / 2, r, height=h * 0.9, color=GRAY, label='不分組隨機切(對照,偏樂觀)' if i == 0 else None)
        ax.text(g + 1, i - h / 2, f'{g:.1f}', va='center', fontsize=12, color=DARK)
        ax.text(r + 1, i + h / 2, f'{r:.1f}', va='center', fontsize=12, color='#555555')
    ax.set_yticks(range(len(METHODS)))
    ax.set_yticklabels([METHOD_LABEL[m] for m in METHODS])
    ax.invert_yaxis()
    ax.set_xlabel('平均絕對誤差 MAE(澳幣/晚,越低越好;5 折交叉驗證)', fontsize=12)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=12)
    style(ax)
    fig.subplots_adjust(left=0.3, right=0.95, top=0.77, bottom=0.12)
    titles(fig, '各方法猜掛牌價的誤差(MAE)', SUB_MODEL +
           '\n誤差 = 猜中「別人掛多少」的能力,不是「定多少訂得出去」', gap=0.05)
    fig.savefig(FIG / 'mel_b_mae_compare.png', facecolor='white')
    plt.close(fig)


def fig_scatter(y, p, cap, label):
    fig, ax = plt.subplots(figsize=(8.75, 8.2), dpi=160)
    keep = (y <= cap) & (p <= cap)
    ax.scatter(y[keep], p[keep], s=6, alpha=0.25, color=BLUE, linewidths=0)
    xs = np.array([0, cap])
    ax.plot(xs, xs, color=DARK, lw=1)
    ax.plot(xs, xs * 1.2, color=GRAY, lw=1, ls='--')
    ax.plot(xs, xs * 0.8, color=GRAY, lw=1, ls='--')
    ax.text(cap * 0.03, cap * 0.97, '實線:預測 = 實際;兩條虛線之間:差 20% 以內', ha='left', va='top', fontsize=12,
            color='#555555')
    ax.set_xlim(0, cap)
    ax.set_ylim(0, cap)
    ax.set_xlabel('實際掛牌價(澳幣/晚)', fontsize=12)
    ax.set_ylabel('模型預測(樣本外)', fontsize=12)
    style(ax)
    fig.subplots_adjust(left=0.11, right=0.96, top=0.85, bottom=0.08)
    titles(fig, f'{label}:預測 vs 實際(依房東分組 5 折,樣本外)',
           SUB_MODEL +
           f'\n兩軸截到實際價 p99 = {cap:.0f} 澳幣,未畫 {int((~keep).sum())} 點', gap=0.04)
    fig.savefig(FIG / 'mel_b_pred_vs_actual.png', facecolor='white')
    plt.close(fig)


# ---------------- 主程式 ----------------
def main():
    rng = np.random.default_rng(SEED)
    raw = load(MAIN)
    assert len(raw) == EXPECT['rows'], len(raw)
    sc = scope(raw)
    assert len(sc) == EXPECT['scope'], len(sc)
    d = prep(sc)
    assert len(d) == EXPECT['scope_price'], len(d)
    batch = raw.last_scraped[raw.last_scraped != ''].max()
    cut = months_back(batch, 12)
    d['is_new'] = (d.first_review != '') & (d.first_review >= cut)
    assert d.is_new.sum() == EXPECT['new12'], d.is_new.sum()
    print('對賬 ok', len(raw), len(sc), len(d), int(d.is_new.sum()), flush=True)
    out = {'scope_id': 'IS-1111-MEL-B', 'batch': MAIN, 'seed': SEED,
           'reconciliation': {'rows_all': len(raw), 'rows_scope': len(sc), 'rows_scope_price': len(d),
                              'new12': int(d.is_new.sum()), 'baseline_day': batch, 'new12_cutoff_inclusive': cut,
                              'all_match_expected': True}}

    # ---- 極端值 ----
    p = d.price_num.values
    p1, p99 = np.percentile(p, 1), np.percentile(p, 99)
    out['price_distribution'] = {**q(p, (1, 10, 25, 50, 75, 90, 99)), 'min': float(p.min()), 'max': float(p.max()),
                                 'n_above_p99': int((p > p99).sum()), 'n_below_p1': int((p < p1).sum()),
                                 'n_ge_1000': int((p >= 1000).sum()), 'n_lt_50': int((p < 50).sum())}
    dm = d[d.price_num <= EXTREME_CAP].reset_index(drop=True)
    ext = d[d.price_num > EXTREME_CAP].reset_index(drop=True)
    out['extreme_rule'] = {'cap_aud': EXTREME_CAP, 'n_excluded': int(len(ext)), 'n_model_sample': int(len(dm)),
                           'excluded_prices_sorted': sorted(float(v) for v in ext.price_num),
                           'n_excluded_new12': int(ext.is_new.sum()),
                           'applies_to': '模型訓練、主要誤差、設施迴歸(c-ii);分組、定位表、同組設施比較(c-i)用全部 8,223(中位數/分位數不受影響)'}

    # ---- a. 分組 ----
    sizes = d.grp.value_counts()
    small = sizes[sizes < MIN_GROUP]
    own = d.grp.map(sizes).values
    fb = own < MIN_GROUP
    radii = []
    for i in np.where(fb)[0]:
        same = (d.bed_n.values == d.bed_n.values[i])
        same[i] = False
        dist = km(d.lat.values[i], d.lon.values[i], d.lat.values[same], d.lon.values[same])
        radii.append(np.partition(dist, K_NEAR - 1)[K_NEAR - 1])
    comp_size = np.where(fb, K_NEAR, own)
    out['a_grouping'] = {
        'primary_group': '區(neighbourhood_cleansed)× 房間數(1/2)',
        'n_groups': int(len(sizes)), 'n_possible': int(d.nb.nunique() * 2),
        'group_size': {'median': float(sizes.median()), 'min': int(sizes.min()), 'max': int(sizes.max())},
        'n_groups_lt30': int(len(small)), 'listings_in_groups_lt30': int(small.sum()),
        'listings_in_groups_ge30': int(len(d) - small.sum()),
        'pct_listings_in_groups_ge30': round(100 * (len(d) - small.sum()) / len(d), 1),
        'rule': ['步驟 1:找同區、同房間數的房源;若有 30 間以上,就用這一組。',
                 '步驟 2:不足 30 間 → 改找全市同房間數、經緯度直線距離最近的 30 間(不限區)。',
                 '步驟 3:比較組固定記下用了哪一步(1 = 同區同房間數,2 = 最近 30 間)。'],
        'comparison_size_after_rule': {'median': float(np.median(comp_size)), 'p10': float(np.percentile(comp_size, 10))},
        'fallback_radius_km_30th_neighbor': (q(np.array(radii), (25, 50, 75)) if radii else None),
        'note': '組大小含房源自己;實際給新房東用時,新房源不在組內。',
    }

    # ---- b. 定位表 ----
    nb_n = d.nb.value_counts()
    pos = {}
    for nb in nb_n.index[nb_n >= MIN_GROUP]:
        cells = {}
        for b in ('1', '2'):
            s = d.price_num[(d.nb == nb) & (d.bedrooms == b)].values
            if len(s):
                cells[b] = {'n': int(len(s)), **q(s), 'small_lt30': bool(len(s) < MIN_GROUP)}
        pos[nb] = {'n': int(nb_n[nb]), 'by_bedrooms': cells}
    top10 = list(nb_n.index[:10])
    out['b_positioning'] = {'rule': '區內篩選且有價房源 30 間以上才列;格內 n<30 標 small_lt30', 'n_districts': len(pos),
                            'districts_excluded_lt30': {k: int(v) for k, v in nb_n[nb_n < MIN_GROUP].items()},
                            'top10_districts': top10, 'table': pos,
                            'city_by_bedrooms': {b: {'n': int((d.bedrooms == b).sum()),
                                                     **q(d.price_num[d.bedrooms == b].values)} for b in ('1', '2')}}

    # ---- c. 設施 ----
    cnt = pd.Series([a for s in d.amen for a in s]).value_counts()
    an = d.amen_n.values
    out['c_amenities'] = {
        'n_distinct_amenities': int(len(cnt)),
        'top30_prevalence_pct': {a: round(100 * c / len(d), 1) for a, c in cnt.head(30).items()},
        'amenity_count_distribution': {**q(an), 'min': int(an.min()), 'max': int(an.max()), 'mean': round(float(an.mean()), 1),
                                       'n_zero': int((an == 0).sum()),
                                       'hist_bins_of_10': {f'{k * 10}-{k * 10 + 9}': int(((an // 10) == k).sum())
                                                           for k in range(int(an.max()) // 10 + 1)}},
    }
    big = fb == False  # noqa: E712  只用 30 間以上的組做同組比較
    dg = d[big].copy()
    dg['rel'] = dg.y - dg.groupby('grp').y.transform('median')
    nbd = pd.get_dummies(dm.nb, drop_first=True).values.astype(float)
    base = np.hstack([np.ones((len(dm), 1)), nbd, dm[['bed_n', 'acc', 'beds_n', 'baths']].values.astype(float)])
    assoc = []
    for a in cnt.index:
        w_g = dg.amen.map(lambda s: a in s).values
        if w_g.sum() < 30 or (~w_g).sum() < 30:
            continue
        within = float(np.exp(np.median(dg.rel.values[w_g]) - np.median(dg.rel.values[~w_g])) - 1)
        f = dm.amen.map(lambda s: a in s).values.astype(float)
        X = np.hstack([base, f[:, None]])
        beta, *_ = np.linalg.lstsq(X, dm.y.values, rcond=None)
        resid = dm.y.values - X @ beta
        s2 = resid @ resid / (len(dm) - X.shape[1])
        se = float(np.sqrt(s2 * np.linalg.pinv(X.T @ X)[-1, -1]))
        assoc.append({'amenity': a, 'n_with': int(w_g.sum()), 'n_without': int((~w_g).sum()),
                      'n_with_full': int(f.sum()), 'within_group_pct': round(100 * within, 1),
                      'regression_pct': round(100 * float(np.exp(beta[-1]) - 1), 1),
                      'regression_ci95_pct': [round(100 * float(np.exp(beta[-1] - 1.96 * se) - 1), 1),
                                              round(100 * float(np.exp(beta[-1] + 1.96 * se) - 1), 1)]})
    assoc.sort(key=lambda r: -r['within_group_pct'])
    pos10, neg5 = assoc[:10], assoc[-5:][::-1]
    out['c_amenities']['association'] = {
        'method_i': '同組(區×房間數,只用 30 間以上的組,涵蓋 %d 間)內:每間價格先除以自己組的中位數,再比有/沒有該設施兩邊的中位數' % len(dg),
        'method_ii': 'log(價格) ~ 區 + 房間數 + 可住人數 + 床數 + 浴室數 + 該設施(每項設施各跑一次 OLS);報 exp(係數)-1',
        'eligible_rule': '同組比較樣本中有、沒有兩邊各 30 間以上', 'n_eligible': len(assoc),
        'top10_positive': pos10, 'top5_negative': neg5,
        'sign_agree_pct_all_eligible': round(100 * np.mean([np.sign(r['within_group_pct']) == np.sign(r['regression_pct'])
                                                            for r in assoc]), 1),
        'wording': '有這項設施的同類房源掛牌價中位數高 X%(關聯,不是因果)'}

    out['c_amenities']['association']['method_ii'] += f'(排除極端值後 {len(dm):,} 間)'
    # ---- d. 實驗(以下 d = 排除極端值後的模型樣本)----
    d_all, d = d, dm
    spec = Spec(d)
    top5 = list(nb_n.index[:TOP5_NB])
    masks = {'all': np.ones(len(d), bool), 'bed1': d.bed_n.values == 1, 'bed2': d.bed_n.values == 2,
             'top5_district': d.nb.isin(top5).values, 'other_district': ~d.nb.isin(top5).values,
             'new12': d.is_new.values, 'not_new12': ~d.is_new.values}
    y = d.price_num.values
    res = {}
    oofs = {}
    for how in ('group', 'random'):
        oof = run_cv(d, spec, how)
        oofs[how] = oof
        res[how] = {m: {k: metrics(y[mk], oof[m][mk]) for k, mk in masks.items()} for m in METHODS}
        print(how, {m: res[how][m]['all']['MAE_aud'] for m in METHODS}, flush=True)
    keep99 = y <= p99
    best = min(('M1', 'M2'), key=lambda m: res['group'][m]['all']['MAE_aud'])
    lr = d.y.values - np.log(oofs['group'][best])
    lr2 = d.y.values - np.log(oofs['group']['M2'])
    # 極端值放回評估:用全部模型樣本訓練的模型去猜那幾間(它們本來就沒進訓練,屬樣本外)
    y_all = np.concatenate([y, ext.price_num.values])
    with_ext = {m: metrics(y_all, np.concatenate([oofs['group'][m], fit_predict(m, d, ext, spec)]))
                for m in ('B0', 'B1', 'M1', 'M2')}
    out['d_experiment'] = {
        'target': 'log(price) 訓練,exp 回澳幣報誤差(B0/B1 直接用澳幣中位數)',
        'features_allowed': FEATURES_ALLOWED, 'features_banned_and_why': FEATURES_BANNED,
        'M1': f'Ridge(alpha=1,先標準化);特徵 = 區 one-hot + 房間數 + 可住人數 + 床數(+缺值旗標)+ 浴室數 + 設施數 + 前 {TOP_N_AMEN} 項設施旗標',
        'M2': f'sklearn {__import__("sklearn").__version__} HistGradientBoostingRegressor(400 輪, lr 0.05, 31 葉, 每葉至少 20);'
              f'特徵 = 區、房型細類(類別)+ 經緯度 + 房間數 + 可住人數 + 床數 + 浴室數 + 最少入住晚數 + 設施數 + 前 {TOP_N_AMEN} 項設施旗標',
        'host_variant': 'M1/M2 再加 calculated_host_listings_count(線性版取 log1p),只當對照,新房東上架前雖知道自己有幾間但樣本裡多房東主導',
        'top_amenities_used': spec.top_amen, 'property_type_levels': spec.pt_levels,
        'split_main': 'GroupKFold(5),group = host_id(同房東全在同一折)',
        'split_contrast': f'KFold(5, shuffle, seed={SEED}),不分房東',
        'top5_districts': top5,
        'results_group_cv': res['group'], 'results_random_cv': res['random'],
        'random_minus_group_MAE_aud': {m: round(res['random'][m]['all']['MAE_aud'] - res['group'][m]['all']['MAE_aud'], 1)
                                       for m in METHODS},
        'best_model': best,
        'best_model_log_residual_quantiles': {k: round(float(v), 4) for k, v in
                                              zip(('q10', 'q25', 'q50', 'q75', 'q90'), np.percentile(lr, [10, 25, 50, 75, 90]))},
        'M2_log_residual_quantiles': {k: round(float(v), 4) for k, v in
                                      zip(('q10', 'q25', 'q50', 'q75', 'q90'), np.percentile(lr2, [10, 25, 50, 75, 90]))},
        'extreme_sensitivity_excluding_actual_above_p99': {m: metrics(y[keep99], oofs['group'][m][keep99])
                                                           for m in ('B0', 'B1', 'M1', 'M2')},
        'extreme_sensitivity_including_excluded_extremes': with_ext,
    }

    # 排列重要度(M2,依房東分組第 1 折)
    tr_i, te_i = next(GroupKFold(5).split(d, groups=d.host_id))
    tr, te = d.iloc[tr_i], d.iloc[te_i]
    Xtr, names = X_tree(tr, spec)
    Xte, _ = X_tree(te, spec)
    mdl = make_tree(Xtr.shape[1]).fit(Xtr, tr.y)
    yte = te.price_num.values
    base_mae = np.abs(np.exp(mdl.predict(Xte)) - yte).mean()
    imp = []
    for j, nm in enumerate(names):
        inc = []
        for _ in range(5):
            Xp = Xte.copy()
            Xp[:, j] = rng.permutation(Xp[:, j])
            inc.append(np.abs(np.exp(mdl.predict(Xp)) - yte).mean() - base_mae)
        imp.append((nm, float(np.mean(inc))))
    imp.sort(key=lambda t: -t[1])
    out['d_experiment']['permutation_importance_M2_fold1'] = {
        'how': '依房東分組第 1 折:訓練後把測試集某一欄隨機打亂 5 次,看 MAE(澳幣)平均變大多少', 'base_MAE_aud': round(float(base_mae), 1),
        'n_test': int(len(te)), 'top10': [{'feature': n, 'MAE_increase_aud': round(v, 2)} for n, v in imp[:10]]}

    # 時間外部檢查
    raw6 = load(PREV)
    d6_all = prep(scope(raw6))
    d6 = d6_all[d6_all.price_num <= EXTREME_CAP].reset_index(drop=True)
    unseen = ~d.id.isin(set(raw6.id))
    n_unseen_all = int((~d_all.id.isin(set(raw6.id))).sum())
    te = d[unseen]
    spec6 = Spec(d6)
    tres = {m: metrics(te.price_num.values, fit_predict(m, d6, te, spec6)) for m in ('B0', 'B1', 'M1', 'M2')}
    same_rows_cv = {m: metrics(y[unseen.values], oofs['group'][m][unseen.values]) for m in ('B0', 'B1', 'M1', 'M2')}
    out['d_temporal_check'] = {'done': True, 'train': f'{PREV} 篩選且有價 {len(d6):,} 間', 'test':
                               f'{MAIN} 篩選且有價、id 不在 {PREV} 整期 listings 裡的 {int(unseen.sum()):,} 間',
                               'n_train': int(len(d6)), 'n_test': int(unseen.sum()),
                               'n_train_excluded_extreme': int(len(d6_all) - len(d6)),
                               'n_test_before_extreme_rule': n_unseen_all,
                               'n_test_new12': int(d.is_new.values[unseen.values].sum()), 'results': tres,
                               'same_rows_in_period_group_cv': same_rows_cv}
    print('temporal', tres, flush=True)

    # ---- e. 示範案例 ----
    g = d_all[d_all.grp == 'Melbourne|1']
    want = ['Kitchen', 'Washer', 'Wifi']
    gcnt = pd.Series([a for s in g.amen for a in s]).value_counts() / len(g)
    missing3 = [(a, round(100 * float(v), 1)) for a, v in gcnt.items() if a not in want][:3]
    wg = {r['amenity']: r['within_group_pct'] for r in assoc}
    common_pos = sorted([(a, round(100 * float(v), 1), wg[a]) for a, v in gcnt.items()
                         if a not in want and v >= 0.5 and wg.get(a, 0) > 0], key=lambda t: -t[2])[:3]
    full = make_tree(X_tree(d, spec)[0].shape[1]).fit(X_tree(d, spec)[0], d.y)
    med_k = int(g.amen_n.median())
    filled = frozenset(want) | frozenset(list(gcnt.index[:med_k]))

    def demo(amen):
        row = pd.DataFrame([{'nb': 'Melbourne', 'property_type': 'Entire rental unit', 'lat': g.lat.median(),
                             'lon': g.lon.median(), 'bed_n': 1, 'acc': 2, 'beds_n': 1, 'baths': 1.0,
                             'min_n': int(g.min_n.median()), 'amen': amen, 'amen_n': len(amen)}])
        pt = float(np.exp(full.predict(X_tree(row, spec)[0])[0]))
        rq = out['d_experiment']['M2_log_residual_quantiles']
        return {'point_aud': round(pt, 0), 'ref_range_aud': [round(pt * np.exp(rq['q25']), 0), round(pt * np.exp(rq['q75']), 0)],
                'amenity_count': len(amen)}
    g2 = g[g.acc == 2]
    out['e_demo_case'] = {
        'input': 'Melbourne 區、整套(Entire rental unit)、1 房、2 人、1 床、1 浴、有 Kitchen + Washer + Wifi',
        'comparison_group': {'rule_step': 1, 'n': int(len(g)), **q(g.price_num.values, (25, 50, 75)),
                             'subset_accommodates_2': {'n': int(len(g2)), **q(g2.price_num.values, (25, 50, 75))}},
        'group_median_amenity_count': med_k,
        'model_literal_input_3_amenities': demo(frozenset(want)),
        'model_if_amenities_filled_to_group_median': demo(filled),
        'model_note': f'M2 用模型樣本 {len(d):,} 間重訓;參考區間 = 點估 × exp(交叉驗證對數誤差 q25..q75),即樣本外約一半房源落在此區間;'
                      f'經緯度、最少入住晚數取該組中位數',
        'missing_top3_common_in_group': [{'amenity': a, 'group_prevalence_pct': v} for a, v in missing3],
        'missing_top3_common_ge50pct_and_positive_within_group': [
            {'amenity': a, 'group_prevalence_pct': v, 'within_group_pct': w} for a, v, w in common_pos],
        'disclaimer': '這是示範輸出,不是定價建議;價格是別人的掛牌價,不是成交價。'}

    # ---- 圖 ----
    global SUB_MODEL
    SUB_MODEL = (f'墨爾本 {MAIN} 期;模型樣本 {len(d):,} 間(篩選且有價,排除每晚 2,000 澳幣以上 {len(ext)} 間);'
                 '掛牌價不是成交價')
    FIG.mkdir(parents=True, exist_ok=True)
    setup_font()
    fig_positioning(pos, top10)
    fig_amenity(pos10 + neg5)
    fig_mae(res['group'], res['random'])
    fig_scatter(y, oofs['group'][best], float(np.percentile(y, 99)), METHOD_LABEL[best])
    out['figures'] = ['mel_b_positioning_top10.png', 'mel_b_amenity_price.png', 'mel_b_mae_compare.png',
                      'mel_b_pred_vs_actual.png']
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float) + '\n', encoding='utf-8')
    print('wrote', OUT_JSON.relative_to(ROOT))


if __name__ == '__main__':
    main()
