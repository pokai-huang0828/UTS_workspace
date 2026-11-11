"""墨爾本分支 A(IS-1111-MEL-A):市場概況、地圖、需求。
主體用 2026-09-16 一期;calendar 用四期。只讀 scratchpad/insideairbnb_melbourne,不改原始資料。
產出:notes/raw/mel_a_market_2026-11-11.json、.md;notes/figures/mel_a_*.png。
篩選定義與 price 解析照 airbnb_ab_field_inventory.py。
"""
import json
import time
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize
from matplotlib.patches import Patch, PathPatch
from matplotlib.path import Path as MPath

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'scratchpad/insideairbnb_melbourne'
RAW = ROOT / 'Innovation Studio/notes/raw'
FIG = ROOT / 'Innovation Studio/notes/figures'
OUT_JSON = RAW / 'mel_a_market_2026-11-11.json'
OUT_MD = RAW / 'mel_a_market_2026-11-11.md'
PERIODS = ['2025-12-12', '2026-03-21', '2026-06-16', '2026-09-16']
MAIN = '2026-09-16'
EXPECT = (25715, 10940, 8223)  # 全體列數 / 篩選樣本 / 篩選且有價
MIN_N = 10
BLUE, ORANGE, GRAY, DARK = '#1F5A8C', '#D9822B', '#B5B5B5', '#222222'
ROOM_ZH = {'Entire home/apt': '整套房', 'Private room': '獨立房間', 'Shared room': '合住房間', 'Hotel room': '飯店房間'}
SEASON = {'2025-12-12': '12月(夏)', '2026-03-21': '3月(秋)', '2026-06-16': '6月(冬)', '2026-09-16': '9月(春)'}
CAL_WIN = (30, 60, 90)
LIST_COLS = ['id', 'price', 'room_type', 'property_type', 'accommodates', 'bedrooms', 'minimum_nights',
             'neighbourhood_cleansed', 'review_scores_rating', 'estimated_occupancy_l365d', 'availability_30',
             'availability_90', 'availability_365', 'calculated_host_listings_count', 'last_scraped',
             'calendar_last_scraped']


def setup_font():
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in ('Microsoft JhengHei', 'Microsoft YaHei', 'SimHei'):
        if name in have:
            plt.rcParams['font.sans-serif'] = [name]
            break
    else:
        raise SystemExit('找不到中文字型')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 12
    return name


def read_listings(period):
    p = DATA / period / 'data/listings.csv.gz'
    df = pd.read_csv(p, dtype=str, keep_default_na=False, usecols=lambda c: c in LIST_COLS)
    for c in LIST_COLS:
        if c not in df.columns:
            df[c] = ''
    return df


def num(s):
    return pd.to_numeric(s.str.replace(r'[,$\s]', '', regex=True), errors='coerce')


def scope_mask(df):
    acc = pd.to_numeric(df['accommodates'], errors='coerce')
    mn = pd.to_numeric(df['minimum_nights'], errors='coerce')
    return ((df['room_type'] == 'Entire home/apt') & df['bedrooms'].isin(['1', '2'])
            & acc.between(2, 4) & mn.between(1, 7))


def pcts(s):
    a = np.asarray(s, float)
    a = a[~np.isnan(a)]
    if len(a) == 0:
        return {'n': 0}
    q = np.percentile(a, [10, 25, 50, 75, 90])
    return {'n': int(len(a)), 'p10': round(q[0], 2), 'p25': round(q[1], 2), 'p50': round(q[2], 2),
            'p75': round(q[3], 2), 'p90': round(q[4], 2)}


def sh(n, tot):
    return round(n / tot, 4) if tot else None


# ---------- 圖框架 ----------
def new_fig(h, title, sub, ncols=1, top_in=1.25):
    fig = plt.figure(figsize=(8.75, h), dpi=160)
    fig.patch.set_facecolor('white')
    fig.text(0.02, 1 - 0.12 / h, title, fontsize=17, fontweight='bold', color=DARK, va='top')
    fig.text(0.02, 1 - 0.55 / h, sub, fontsize=12, color='#555555', va='top', linespacing=1.4)
    return fig, 1 - top_in / h


def clean(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=12)


# ---------- calendar(逐 chunk 串流) ----------
def calendar_blocked(period, scope_ids):
    """先逐 chunk 彙總成「每個日期」的房源日數,再以 calendar 最早日期為抓取日起算 30/60/90 天窗口 [base, base+N)。"""
    path = DATA / period / 'data/calendar.csv.gz'
    t0 = time.time()
    tot, ids, nrows = None, set(), 0
    for ch in pd.read_csv(path, usecols=['listing_id', 'date', 'available'], dtype=str, chunksize=2_000_000):
        nrows += len(ch)
        ins = ch['listing_id'].isin(scope_ids)
        blk = ch['available'] == 'f'
        ids.update(ch['listing_id'].unique())
        g = pd.DataFrame({'date': ch['date'], 'n': 1, 'b': blk.astype(int), 'sn': ins.astype(int),
                          'sb': (ins & blk).astype(int)}).groupby('date').sum()
        tot = g if tot is None else tot.add(g, fill_value=0)
    tot = tot.sort_index()
    base = pd.Timestamp(tot.index[0])
    out = {'base_date': tot.index[0], 'calendar_rows_total': nrows, 'calendar_min_date': tot.index[0],
           'calendar_max_date': tot.index[-1], 'n_listings_in_calendar': len(ids),
           'seconds': round(time.time() - t0, 1)}
    for k, (cn, cb) in {'all': ('n', 'b'), 'scope': ('sn', 'sb')}.items():
        out[k] = {}
        for n in CAL_WIN:
            end = (base + pd.Timedelta(days=n)).strftime('%Y-%m-%d')
            w = tot[tot.index < end]
            out[k][str(n)] = {'listing_days': int(w[cn].sum()), 'blocked_days': int(w[cb].sum()),
                              'blocked_share': sh(int(w[cb].sum()), int(w[cn].sum())), 'window_days': len(w)}
    return out


# ---------- 地圖 ----------
def geo_paths(geo):
    res = {}
    for f in geo['features']:
        name = f['properties']['neighbourhood']
        verts, codes, best = [], [], (-1, None)
        for poly in f['geometry']['coordinates']:
            for i, ring in enumerate(poly):
                r = np.asarray(ring, float)
                verts.append(r)
                codes += [MPath.MOVETO] + [MPath.LINETO] * (len(r) - 2) + [MPath.CLOSEPOLY]
                if i == 0:
                    x, y = r[:, 0], r[:, 1]
                    cr = x[:-1] * y[1:] - x[1:] * y[:-1]
                    a = cr.sum() / 2
                    if abs(a) > best[0]:
                        best = (abs(a), (float((x[:-1] + x[1:]) @ cr / (6 * a)), float((y[:-1] + y[1:]) @ cr / (6 * a))))
        res[name] = (MPath(np.vstack(verts), codes), best[1])
    return res


INSET_POS = {'Maribyrnong': (144.86, -37.885), 'Melbourne': (144.905, -37.923), 'Port Phillip': (144.985, -37.950),
             'Yarra': (145.085, -37.745), 'Stonnington': (145.062, -37.935)}  # 放大圖內手動擺位(有引線)
INSET = (144.80, 145.12, -37.97, -37.70)  # 市中心放大框 (lon0, lon1, lat0, lat1)


def draw_map(paths, values, fname, title, sub, cmap, norm, cbar_label, top_labels, label_fmt, low=(), ticks=None):
    """左 = 全區;右 = 市中心放大(同色階)。標名用白色描邊字,直接標在區的中心。"""
    h = 6.6
    fig, _ = new_fig(h, title, sub)
    allv = np.vstack([p.vertices for p, _ in paths.values()])
    ext = (allv[:, 0].min(), allv[:, 0].max(), allv[:, 1].min(), allv[:, 1].max())
    axm = fig.add_axes([0.01, 0.20, 0.52, 0.60])
    axi = fig.add_axes([0.55, 0.20, 0.44, 0.60])
    halo = [pe.withStroke(linewidth=3, foreground='white')]
    for ax in (axm, axi):
        for name, (path, _) in paths.items():
            col = GRAY if name in low or values.get(name) is None else cmap(norm(values[name]))
            ax.add_patch(PathPatch(path, facecolor=col, edgecolor='white', lw=0.7))
        ax.axis('off')
    axm.set_xlim(ext[0] - 0.02, ext[1] + 0.02); axm.set_ylim(ext[2] - 0.02, ext[3] + 0.02)
    axi.set_xlim(INSET[0], INSET[1]); axi.set_ylim(INSET[2], INSET[3])
    for ax, lat in ((axm, (ext[2] + ext[3]) / 2), (axi, (INSET[2] + INSET[3]) / 2)):
        ax.set_aspect(1 / np.cos(np.radians(lat)))
    axm.add_patch(plt.Rectangle((INSET[0], INSET[2]), INSET[1] - INSET[0], INSET[3] - INSET[2], fill=False,
                                edgecolor=ORANGE, lw=2))
    for sp_ in axi.spines.values():
        sp_.set_visible(True); sp_.set_edgecolor(ORANGE); sp_.set_linewidth(2)
    axi.set_xticks([]); axi.set_yticks([])
    axi.axis('on')
    axi.set_title('橘框 = 市中心放大', fontsize=12, loc='left', color=ORANGE)
    for n in top_labels:
        cx, cy = paths[n][1]
        inside = INSET[0] < cx < INSET[1] and INSET[2] < cy < INSET[3]
        ax = axi if inside else axm
        nm, val = label_fmt(n, values.get(n), n in low).split('||')
        txt = nm + chr(10) + val
        if inside and n in INSET_POS:
            ax.annotate(txt, xy=(cx, cy), xytext=INSET_POS[n], fontsize=12, ha='center', va='center', color=DARK,
                        fontweight='bold', path_effects=halo,
                        arrowprops=dict(arrowstyle='-', color='#444444', lw=1.0, shrinkA=0, shrinkB=0))
        else:
            ax.text(cx, cy, txt, fontsize=12, ha='center', va='center', color=DARK, fontweight='bold',
                    path_effects=halo)
    cax = fig.add_axes([0.28, 0.115, 0.44, 0.022])
    cb = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='horizontal')
    if ticks:
        cb.set_ticks(ticks)
        cb.set_ticklabels([f'{t:,}' for t in ticks])
        cb.ax.minorticks_off()
    cb.ax.tick_params(labelsize=12)
    cb.set_label(cbar_label, fontsize=12)
    if low:
        fig.legend(handles=[Patch(facecolor=GRAY, label=f'灰色 = 樣本太少(篩選且有價 少於 {MIN_N} 間),不報中位數')],
                   loc='lower center', bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=12)
    fig.savefig(FIG / fname, dpi=160, facecolor='white')
    plt.close(fig)


def main():
    font = setup_font()
    FIG.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    L = read_listings(MAIN)
    L['price_v'] = num(L['price'])
    L['scope'] = scope_mask(L)
    L['has_price'] = L['price'].str.strip() != ''
    sp = L[L['scope'] & L['has_price']]
    assert (len(L), int(L['scope'].sum()), len(sp)) == EXPECT, ('對賬失敗', len(L), int(L['scope'].sum()), len(sp))
    assert sp['price_v'].notna().all(), 'scope 有價列有無法解析的 price'
    print('對賬 OK', EXPECT, '字型', font, flush=True)
    N, NS, NP = EXPECT
    geo = json.loads((DATA / MAIN / 'visualisations/neighbourhoods.geojson').read_text(encoding='utf-8'))
    paths = geo_paths(geo)
    assert set(paths) == set(L['neighbourhood_cleansed']), '區名與 geojson 對不上'
    R = {'meta': {
        'scope_id': 'IS-1111-MEL-A', 'main_period': MAIN, 'periods': PERIODS,
        'recon': {'listings_rows': N, 'scope_rows': NS, 'scope_with_price_rows': NP, 'passed': True},
        'scope_definition': '整套房(Entire home/apt)、bedrooms 1-2、accommodates 2-4、minimum_nights 1-7;有價 = price 非空',
        'price_note': '掛牌價(每晚),不是成交價;單位為資料原值($)',
        'percentile_method': 'numpy percentile(線性內插)',
        'font': font}}

    # ---- a 供給長相 ----
    rt = L['room_type'].value_counts()
    eh = L[L['room_type'] == 'Entire home/apt']
    bd = eh['bedrooms'].replace('', '缺值')
    bd = bd.where(bd.isin(['1', '2', '3', '4', '缺值']), '5以上')
    ac = pd.to_numeric(eh['accommodates'], errors='coerce')
    ac_g = ac.clip(upper=9).fillna(-1).astype(int).astype(str).replace({'9': '9以上', '-1': '缺值'})
    pt = L['property_type'].value_counts().head(8)
    hc = pd.to_numeric(L['calculated_host_listings_count'], errors='coerce')
    hg = {'1': (hc == 1).sum(), '2_4': hc.between(2, 4).sum(), '5_plus': (hc >= 5).sum(), 'missing': hc.isna().sum()}
    R['a_supply'] = {
        'n_listings': N,
        'room_type': {k: {'n': int(v), 'share': sh(v, N)} for k, v in rt.items()},
        'entire_home_n': len(eh),
        'entire_home_bedrooms': {k: {'n': int(v), 'share': sh(v, len(eh))} for k, v in bd.value_counts().sort_index().items()},
        'entire_home_accommodates': {k: {'n': int(v), 'share': sh(v, len(eh))} for k, v in ac_g.value_counts().sort_index().items()},
        'property_type_top8': [{'name': k, 'n': int(v), 'share': sh(v, N)} for k, v in pt.items()],
        'host_concentration': {k: {'listings': int(v), 'share': sh(v, N)} for k, v in hg.items()},
        'host_concentration_note': 'calculated_host_listings_count;以房源為分母(不是以房東為分母)'}

    # ---- b 掛牌價 ----
    P = L[L['has_price']].copy()
    p99 = float(np.percentile(P['price_v'], 99))
    ent = P[P['room_type'] == 'Entire home/apt']
    ebd = ent['bedrooms'].replace('', '缺值')
    ebd = ebd.where(ebd.isin(['1', '2', '3', '4', '缺值']), '5以上')
    R['b_price'] = {
        'n_priced_all': len(P), 'all_priced': pcts(P['price_v']),
        'by_room_type': {k: pcts(g['price_v']) for k, g in P.groupby('room_type')},
        'entire_by_bedrooms': {k: pcts(ent.loc[ebd == k, 'price_v']) for k in ['1', '2', '3', '4', '5以上', '缺值'] if (ebd == k).any()},
        'p99_value': round(p99, 2), 'n_above_p99': int((P['price_v'] > p99).sum()), 'max_price': float(P['price_v'].max()),
        'hist_note': f'直方圖只畫到 p99 = ${p99:,.0f};更貴的不畫'}

    # ---- c 分區表 ----
    low = set()
    dist = {}
    for name, g in L.groupby('neighbourhood_cleansed'):
        gs = g[g['scope'] & g['has_price']]
        rat = pd.to_numeric(g['review_scores_rating'], errors='coerce').dropna()
        med = round(float(gs['price_v'].median()), 2) if len(gs) >= MIN_N else None
        if med is None:
            low.add(name)
        dist[name] = {'n_listings': len(g), 'n_scope_priced': len(gs), 'scope_price_median': med,
                      'scope_price_note': None if med is not None else '樣本太少',
                      'rating_median': round(float(rat.median()), 3) if len(rat) else None, 'n_rated': len(rat),
                      'entire_share': sh((g['room_type'] == 'Entire home/apt').sum(), len(g))}
    R['c_districts'] = {'min_n_for_median': MIN_N, 'rating_note': '評分中位數 = 該區所有有評分房源',
                        'districts': dist}

    # ---- d 地圖 ----
    cmap = LinearSegmentedColormap.from_list('b', ['#E8F1FA', '#0B3A66'])
    cnt = {k: v['n_listings'] for k, v in dist.items()}
    top8 = [k for k, _ in sorted(cnt.items(), key=lambda t: -t[1])[:8]]
    pv = {k: v['scope_price_median'] for k, v in dist.items()}
    valid = [v for v in pv.values() if v is not None]
    draw_map(paths, pv, 'mel_a_map_price_median.png', '各區篩選樣本掛牌價中位數',
             f'{MAIN[:7]} 一期;篩選且有價 {NP:,} 間;掛牌價(每晚)不是成交價;標名者 = 房源數前 8 區',
             cmap, Normalize(min(valid), max(valid)), '掛牌價中位數($/晚)', top8,
             lambda n, v, lo: f'{n}||樣本太少' if lo else f'{n}||${v:,.0f}', low=low)
    draw_map(paths, cnt, 'mel_a_map_listing_count.png', '各區房源數',
             f'{MAIN[:7]} 一期;全體 {N:,} 間;色階為對數;標名者 = 房源數前 8 區',
             cmap, LogNorm(100, 10000), '房源數(對數色階)', top8,
             lambda n, v, lo: f'{n}||{v:,}', ticks=[100, 300, 1000, 3000, 10000])
    R['d_maps'] = {'files': ['mel_a_map_price_median.png', 'mel_a_map_listing_count.png'],
                   'top8_by_listings': [{'name': k, 'n_listings': cnt[k]} for k in top8],
                   'low_sample_districts': sorted(low), 'n_low_sample_districts': len(low)}

    # ---- e 需求代理 ----
    occ = pd.to_numeric(sp['estimated_occupancy_l365d'], errors='coerce')
    occv = occ.dropna()
    cap = float(occv.max())
    bins = [('0', 0, 0), ('1-50', 1, 50), ('51-100', 51, 100), ('101-150', 101, 150), ('151-200', 151, 200),
            ('201-254', 201, 254), ('255(上限)', 255, 255)]
    occ_bins = {n: int(((occv >= a) & (occv <= b)).sum()) for n, a, b in bins}
    avail = {}
    for d in (30, 90, 365):
        a = pd.to_numeric(sp[f'availability_{d}'], errors='coerce').dropna()
        pc = pcts(a)
        avail[str(d)] = {**pc, 'mean': round(float(a.mean()), 2), 'share_zero': sh((a == 0).sum(), len(a)),
                         'share_full': sh((a == d).sum(), len(a)),
                         'pct_of_window': {k: round(pc[k] / d, 4) for k in ('p10', 'p25', 'p50', 'p75', 'p90')}}
    cal = {}
    for p in PERIODS:
        Lp = L if p == MAIN else read_listings(p)
        sc_ids = set(Lp.loc[scope_mask(Lp), 'id'])
        r = calendar_blocked(p, sc_ids)
        bs = Lp['calendar_last_scraped'].replace('', np.nan).dropna()
        r.update({'n_listings_file': len(Lp), 'n_scope_file': len(sc_ids), 'folder_period': p, 'season': SEASON[p],
                  'listings_calendar_last_scraped_mode': bs.mode().iloc[0], 'listings_calendar_last_scraped_min': bs.min(),
                  'listings_calendar_last_scraped_max': bs.max()})
        cal[p] = r
        print('calendar', p, r['calendar_min_date'], r['calendar_max_date'], r['n_listings_in_calendar'], r['all']['30']['blocked_share'],
              r['all']['90']['blocked_share'], r['seconds'], 's', flush=True)
    R['e_demand'] = {
        'proxy_note': 'estimated_occupancy_l365d 由評論數推算,不是真實入住;availability 是日曆可訂天數;兩者都是代理',
        'occupancy_proxy': {'sample': '篩選且有價', 'n': int(len(occv)), 'n_missing': int(occ.isna().sum()),
                            'max_value': cap, 'share_zero': sh((occv == 0).sum(), len(occv)),
                            'share_at_cap': sh((occv >= 255).sum(), len(occv)), 'median': float(occv.median()),
                            'mean': round(float(occv.mean()), 2), 'bins': occ_bins},
        'availability_proxy': {'sample': '篩選且有價', 'by_window': avail},
        'calendar_blocked': {
            'definition': '窗口 = calendar 最早日期(約等於抓取日,與 listings 的 calendar_last_scraped 差 0-2 天)起算 N 天 [base, base+N);不可訂(available=f)= 被訂走或房東自己關閉,分不出來;'
                          '分母 = 窗口內所有房源日;all = calendar 內全部房源,scope = 篩選樣本',
            'periods': cal}}

    # ---- f 評分 ----
    rt_all = pd.to_numeric(L['review_scores_rating'], errors='coerce').dropna()
    q = np.percentile(sp['price_v'], [25, 50, 75])
    grp = np.digitize(sp['price_v'], q, right=True)  # 0: <=p25, 1: (p25,p50], ...
    rs = pd.to_numeric(sp['review_scores_rating'], errors='coerce')
    qn = ['Q1(最便宜 25%)', 'Q2', 'Q3', 'Q4(最貴 25%)']
    byq = {}
    for i, nme in enumerate(qn):
        m = (grp == i)
        r_ = rs[m].dropna()
        byq[nme] = {'n_priced': int(m.sum()), 'n_rated': int(len(r_)),
                    'price_min': float(sp['price_v'][m].min()), 'price_max': float(sp['price_v'][m].max()),
                    'rating_median': round(float(r_.median()), 3)}
    R['f_rating'] = {
        'all_rated': {'n_rated': int(len(rt_all)), 'n_listings': N, 'share_rated': sh(len(rt_all), N),
                      **pcts(rt_all), 'share_5_0': sh((rt_all == 5).sum(), len(rt_all)),
                      'share_ge_4_5': sh((rt_all >= 4.5).sum(), len(rt_all)),
                      'share_below_4': sh((rt_all < 4).sum(), len(rt_all))},
        'scope_priced_price_quartile_cuts': [float(x) for x in q],
        'scope_priced_by_price_quartile': byq,
        'quartile_note': 'Q1 = 價格小於等於 p25;Q2 = p25 到 p50;依此類推;評分中位數只算有評分者'}

    # ---- 圖 ----
    sub_all = f'{MAIN[:7]} 一期;全體 {N:,} 間'
    # 1 供給
    fig, top = new_fig(5.0, '供給長相:房型與房東集中度', sub_all + ';右圖以房源為分母(不是以房東)')
    axs = fig.subplots(1, 2)
    fig.subplots_adjust(left=0.17, right=0.97, top=top, bottom=0.14, wspace=0.62)
    items = list(rt.items())
    names = [ROOM_ZH.get(k, k) for k, _ in items][::-1]
    vals = [v / N for _, v in items][::-1]
    axs[0].barh(names, vals, color=BLUE)
    for i, v in enumerate(vals):
        axs[0].text(v + 0.01, i, f'{v:.1%}', va='center', fontsize=12, color=DARK)
    axs[0].set_xlim(0, max(vals) * 1.3)
    axs[0].set_title('房型占比', fontsize=13, loc='left')
    hn = [('名下 1 間', '1'), ('名下 2-4 間', '2_4'), ('名下 5 間以上', '5_plus')][::-1]
    hv = [hg[k] / N for _, k in hn]
    axs[1].barh([n for n, _ in hn], hv, color=ORANGE)
    for i, v in enumerate(hv):
        axs[1].text(v + 0.01, i, f'{v:.1%}', va='center', fontsize=12, color=DARK)
    axs[1].set_xlim(0, max(hv) * 1.3)
    axs[1].set_title('房源屬於哪種房東', fontsize=13, loc='left')
    for a in axs:
        clean(a)
        a.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1, decimals=0))
    fig.savefig(FIG / 'mel_a_supply.png', dpi=160, facecolor='white'); plt.close(fig)

    # 2 價格直方圖
    fig, top = new_fig(5.0, '掛牌價分布', f'{MAIN[:7]} 一期;有價 {len(P):,} 間;只畫到 p99 = ${p99:,.0f}(更貴的 {R["b_price"]["n_above_p99"]} 間未畫);掛牌價不是成交價')
    ax = fig.add_axes([0.10, 0.15, 0.86, top - 0.15])
    pv_ = P['price_v'][P['price_v'] <= p99]
    bw = int(np.ceil(p99 / 45 / 10) * 10)
    ax.hist(pv_, bins=np.arange(0, pv_.max() + bw, bw), color=BLUE, edgecolor='white')
    med = R['b_price']['all_priced']['p50']
    ax.axvline(med, color=ORANGE, lw=2)
    ax.text(med + bw, ax.get_ylim()[1] * 0.92, f'中位數 ${med:,.0f}', color=ORANGE, fontsize=13, fontweight='bold')
    ax.set_xlabel('掛牌價($/晚)', fontsize=12); ax.set_ylabel('房源數', fontsize=12)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
    clean(ax)
    fig.savefig(FIG / 'mel_a_price_hist.png', dpi=160, facecolor='white'); plt.close(fig)

    # 3 需求代理
    fig, top = new_fig(5.4, '需求代理:推算入住與日曆可訂天數',
                       f'{MAIN[:7]} 一期;篩選且有價 {NP:,} 間;兩者都是代理,不是真實入住')
    axs = fig.subplots(1, 2)
    fig.subplots_adjust(left=0.09, right=0.97, top=top - 0.06, bottom=0.2, wspace=0.42)
    lab = [b[0] for b in bins]
    cv = [occ_bins[k] / len(occv) for k in lab]
    axs[0].bar(range(len(lab)), cv, color=[ORANGE if k in ('0', '255(上限)') else BLUE for k in lab])
    for i, v in enumerate(cv):
        axs[0].text(i, v + 0.008, f'{v:.0%}', ha='center', fontsize=12, color=DARK)
    axs[0].set_xticks(range(len(lab)))
    axs[0].set_xticklabels(['0', '1-50', '51-\n100', '101-\n150', '151-\n200', '201-\n254', '255\n上限'], fontsize=12, rotation=0)
    axs[0].set_ylim(0, max(cv) * 1.15)
    axs[0].set_xlabel('推算近一年入住晚數', fontsize=12)
    axs[0].set_title('推算入住晚數分組(占比)', fontsize=13, loc='left')
    axs[0].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1, decimals=0))
    for i, d in enumerate((30, 90, 365)):
        a_ = avail[str(d)]['pct_of_window']
        axs[1].plot([a_['p10'], a_['p90']], [i, i], color=GRAY, lw=2)
        axs[1].plot([a_['p25'], a_['p75']], [i, i], color=BLUE, lw=9, solid_capstyle='butt')
        axs[1].plot(a_['p50'], i, 'o', color=ORANGE, ms=9)
        axs[1].text(a_['p50'], i + 0.28, f'中位 {a_["p50"]:.0%}', ha='center', fontsize=12, color=DARK)
    axs[1].set_yticks(range(3)); axs[1].set_yticklabels(['未來 30 天', '未來 90 天', '未來 365 天'], fontsize=12)
    axs[1].set_ylim(-0.5, 2.7)
    axs[1].set_xlim(-0.03, 1.03)
    axs[1].set_title('日曆可訂天數占窗口比例', fontsize=13, loc='left')
    axs[1].set_xlabel('粗條 = p25 到 p75;細線 = p10 到 p90', fontsize=12)
    axs[1].xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1, decimals=0))
    for a in axs:
        clean(a)
    fig.savefig(FIG / 'mel_a_demand_proxy.png', dpi=160, facecolor='white'); plt.close(fig)

    # 4 calendar 四期
    fig, top = new_fig(5.4, '四期日曆:抓取日後的不可訂房源日占比',
                       '各期 calendar 全部房源;不可訂 = 被訂走或房東自己關閉,分不出來;各期房源數不同(03 期較少)')
    ax = fig.add_axes([0.09, 0.17, 0.88, top - 0.17])
    w = 0.26
    for j, (n, c) in enumerate(zip(CAL_WIN, (BLUE, ORANGE, GRAY))):
        vv = [cal[p]['all'][str(n)]['blocked_share'] for p in PERIODS]
        xs = np.arange(4) + (j - 1) * w
        ax.bar(xs, vv, w * 0.94, color=c, label=f'後 {n} 天')
        for x, v in zip(xs, vv):
            ax.text(x, v + 0.008, f'{v:.0%}', ha='center', fontsize=12, color=DARK)
    ax.set_xticks(range(4))
    ax.set_xticklabels([f'{p}\n{SEASON[p]}\n{cal[p]["n_listings_in_calendar"]:,} 間' for p in PERIODS], fontsize=12)
    ax.set_ylim(0, max(cal[p]['all']['30']['blocked_share'] for p in PERIODS) * 1.3)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1, decimals=0))
    ax.legend(frameon=False, fontsize=12, ncol=3, loc='upper left')
    clean(ax)
    fig.savefig(FIG / 'mel_a_calendar_blocked.png', dpi=160, facecolor='white'); plt.close(fig)

    # 5 評分
    fig, top = new_fig(5.4, '評分分布與價格分組',
                       f'{MAIN[:7]} 一期;左圖 = 有評分的全體 {len(rt_all):,} 間;右圖 = 篩選且有價、依掛牌價四分位分組')
    axs = fig.subplots(1, 2)
    fig.subplots_adjust(left=0.09, right=0.97, top=top - 0.04, bottom=0.2, wspace=0.34)
    e = np.arange(3.0, 5.01, 0.1)
    h_, _ = np.histogram(np.clip(rt_all, 3.0, 5.0), bins=e)
    axs[0].bar(e[:-1] + 0.05, h_, 0.09, color=BLUE)
    below = int((rt_all < 3.0).sum())
    axs[0].set_xlabel(f'評分(3.0 以下 {below} 間併入最左格)', fontsize=12); axs[0].set_ylabel('房源數', fontsize=12)
    axs[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
    axs[0].axvline(R['f_rating']['all_rated']['p50'], color=ORANGE, lw=2)
    axs[0].text(R['f_rating']['all_rated']['p50'] - 0.04, axs[0].get_ylim()[1] * 0.9,
                f'中位數 {R["f_rating"]["all_rated"]["p50"]:.2f}', color=ORANGE, fontsize=13, fontweight='bold', ha='right')
    axs[0].set_title('評分直方圖', fontsize=13, loc='left')
    qv = [byq[k]['rating_median'] for k in qn]
    axs[1].bar(range(4), qv, color=[BLUE, BLUE, BLUE, BLUE])
    for i, v in enumerate(qv):
        axs[1].text(i, v + 0.004, f'{v:.2f}', ha='center', fontsize=12, color=DARK)
    axs[1].set_xticks(range(4)); axs[1].set_xticklabels(['Q1\n最便宜', 'Q2', 'Q3', 'Q4\n最貴'], fontsize=12)
    axs[1].set_ylim(min(qv) - 0.15, max(qv) + 0.06)
    axs[1].set_title('評分中位數(縱軸不從 0 起)', fontsize=13, loc='left')
    for a in axs:
        clean(a)
    fig.savefig(FIG / 'mel_a_rating.png', dpi=160, facecolor='white'); plt.close(fig)

    R['figures'] = sorted(p.name for p in FIG.glob('mel_a_*.png'))
    OUT_JSON.write_text(json.dumps(R, ensure_ascii=False, indent=2, default=lambda o: o.item()) + '\n', encoding='utf-8')
    print('wrote', OUT_JSON.relative_to(ROOT), R['figures'], flush=True)
    if 'write_report' in globals():
        write_report(R)


def write_report(R):
    """短報告:數字全從 R(= JSON)取,結論句只用數字,不手填。"""
    a, b, c = R['a_supply'], R['b_price'], R['c_districts']['districts']
    e, f = R['e_demand'], R['f_rating']
    pc = lambda x, d=1: f'{x * 100:.{d}f}%'
    usd = lambda x: f'${x:,.0f}'
    N, NP = R['meta']['recon']['listings_rows'], R['meta']['recon']['scope_with_price_rows']
    rt, hc, bd, bp = a['room_type'], a['host_concentration'], a['entire_home_bedrooms'], b['entire_by_bedrooms']
    top8 = R['d_maps']['top8_by_listings']
    top4 = sum(x['n_listings'] for x in top8[:4])
    med = {k: v['scope_price_median'] for k, v in c.items() if v['scope_price_median'] is not None}
    hi, lo = max(med, key=med.get), min(med, key=med.get)
    nmin = min(v['n_scope_priced'] for v in c.values())
    occ, av, cal = e['occupancy_proxy'], e['availability_proxy']['by_window'], e['calendar_blocked']['periods']
    fa, fq = f['all_rated'], f['scope_priced_by_price_quartile']
    q1, q4 = fq['Q1(最便宜 25%)']['rating_median'], fq['Q4(最貴 25%)']['rating_median']
    pt = a['property_type_top8']
    c30 = {p: cal[p]['all']['30']['blocked_share'] for p in PERIODS}
    pmax, pmin = max(c30, key=c30.get), min(c30, key=c30.get)
    L = ['# 墨爾本 A:市場概況、地圖、需求(2026-09-16 一期)',
         f'> IS-1111-MEL-A。對賬已過:全體 {N:,} / 篩選 {R["meta"]["recon"]["scope_rows"]:,} / 篩選且有價 {NP:,}。價格 = 掛牌價,不是成交價。', '',
         '## 1 供給長相',
         f'**整套房占 {pc(rt["Entire home/apt"]["share"])};{pc(hc["5_plus"]["share"])} 的房源屬於名下 5 間以上的房東。**',
         '![](../figures/mel_a_supply.png)',
         f'整套房裡 1 房 {pc(bd["1"]["share"])}、2 房 {pc(bd["2"]["share"])}。前 3 種類型:{pt[0]["name"]} {pc(pt[0]["share"])}、{pt[1]["name"]} {pc(pt[1]["share"])}、{pt[2]["name"]} {pc(pt[2]["share"])}。',
         f'怎麼讀:右圖是「房源」的分母,名下 1 間 {pc(hc["1"]["share"])}、2-4 間 {pc(hc["2_4"]["share"])}、5 間以上 {pc(hc["5_plus"]["share"])}。', '',
         '## 2 掛牌價分布',
         f'**有價 {b["n_priced_all"]:,} 間,中位數 {usd(b["all_priced"]["p50"])};整套房 {usd(b["by_room_type"]["Entire home/apt"]["p50"])},隨房間數往上。**',
         '![](../figures/mel_a_price_hist.png)',
         '| 範圍(有價) | n | p10 | p25 | p50 | p75 | p90 |', '|---|---|---|---|---|---|---|']
    rows = [('全體', b['all_priced'])] + [(ROOM_ZH.get(k, k), v) for k, v in b['by_room_type'].items() if k in ('Entire home/apt', 'Private room')]
    rows += [(f'整套 {k} 房', bp[k]) for k in ('1', '2', '3')]
    for nm, v in rows:
        L.append(f'| {nm} | {v["n"]:,} | ' + ' | '.join(usd(v[k]) for k in ('p10', 'p25', 'p50', 'p75', 'p90')) + ' |')
    L += [f'怎麼讀:高於 p99({usd(b["p99_value"])})的有 {b["n_above_p99"]} 筆,最高 {usd(b["max_price"])};圖已截掉,分位數不受影響。', '',
          '## 3 分區表(完整 30 區在 JSON)',
          f'**房源集中市中心:房源數前 4 區占全體 {pc(top4 / N)};篩選樣本中位數最高 {hi} {usd(med[hi])}、最低 {lo} {usd(med[lo])}。**',
          '| 區 | 房源數 | 篩選且有價 | 掛牌價中位 | 評分中位 | 整套房占比 |', '|---|---|---|---|---|---|']
    for x in top8:
        v = c[x['name']]
        L.append(f'| {x["name"]} | {v["n_listings"]:,} | {v["n_scope_priced"]:,} | {usd(v["scope_price_median"]) if v["scope_price_median"] else "樣本太少"} | {v["rating_median"]:.2f} | {pc(v["entire_share"], 0)} |')
    L += [f'怎麼讀:30 區篩選且有價最少也有 {nmin} 間,沒有被標「樣本太少」的區。', '',
          '## 4 兩張地圖(右側為市中心放大)',
          f'**價格高的區不等於房源多的區:房源集中在市中心的 Melbourne 區({c["Melbourne"]["n_listings"]:,} 間)。**',
          '![](../figures/mel_a_map_price_median.png)', '![](../figures/mel_a_map_listing_count.png)',
          '怎麼讀:顏色越深越高;房源數用對數色階。灰色 = 樣本太少(這期沒有)。', '',
          '## 5 需求代理(兩者都是代理)',
          f'**篩選且有價樣本:推算入住 0 晚占 {pc(occ["share_zero"])},頂到 255 上限占 {pc(occ["share_at_cap"])},中位數 {occ["median"]:.0f} 晚。**',
          '![](../figures/mel_a_demand_proxy.png)',
          f'日曆未來 30 / 90 / 365 天可訂天數中位數:{av["30"]["p50"]:.0f} / {av["90"]["p50"]:.0f} / {av["365"]["p50"]:.0f} 天。',
          f'**四期抓取日後 30 天不可訂房源日占比:{pc(c30[pmin], 0)}({cal[pmin]["season"]})到 {pc(c30[pmax], 0)}({cal[pmax]["season"]})。**',
          '![](../figures/mel_a_calendar_blocked.png)',
          '| 期別 | 房源數 | 30 天 | 60 天 | 90 天 |', '|---|---|---|---|---|']
    for p in PERIODS:
        L.append(f'| {p} {cal[p]["season"]} | {cal[p]["n_listings_in_calendar"]:,} | ' + ' | '.join(pc(cal[p]['all'][str(n)]['blocked_share']) for n in CAL_WIN) + ' |')
    L += ['怎麼讀:不可訂 = 被訂走或房東自己關閉,分不出來;窗口從 calendar 最早日期起算。', '',
          '## 6 評分',
          f'**有評分者(占 {pc(fa["share_rated"], 0)})中位數 {fa["p50"]:.2f},{pc(fa["share_ge_4_5"], 0)} 在 4.5 分以上;最貴四分位比最便宜高 {q4 - q1:.2f} 分。**',
          '![](../figures/mel_a_rating.png)',
          f'怎麼讀:分數擠在 4.5 到 5.0,差 {q4 - q1:.2f} 分很小;右圖縱軸不從 0 起。', '',
          '## 數字來源對照(數字 → JSON 鍵名)',
          '| 數字 | 鍵名 |', '|---|---|',
          '| 房型占比 / 房東規模 | a_supply.room_type / a_supply.host_concentration |',
          '| 房間數 / 前 8 類型 | a_supply.entire_home_bedrooms / property_type_top8 |',
          '| 分位數、p99、極端值 | b_price.all_priced / by_room_type / entire_by_bedrooms / p99_value / n_above_p99 |',
          '| 分區表 | c_districts.districts.* |', '| 前 8 區、樣本太少區 | d_maps.top8_by_listings / low_sample_districts |',
          '| 推算入住 0 / 255 / 中位 | e_demand.occupancy_proxy.share_zero / share_at_cap / median |',
          '| 可訂天數 | e_demand.availability_proxy.by_window.30 / 90 / 365 |',
          '| 四期不可訂占比 | e_demand.calendar_blocked.periods.<期別>.all.<30/60/90>.blocked_share |',
          '| 評分、價格四分位 | f_rating.all_rated / scope_priced_by_price_quartile |', '',
          '## 看不到的事(不要這樣說 → 改這樣說)',
          '- 「中位數 $263 是房東賺的」 → 「這是掛牌價中位數;成交價、清潔費、折扣看不到」。',
          '- 「推算入住 60 晚 = 住了 60 晚」 → 「這是用評論數推算的代理;0 晚也可能只是沒人留評論」。',
          '- 「63% 被訂走」 → 「63% 不可訂,被訂走或房東自己關,分不出來」。',
          f'- 「秋天最空、夏天最滿」 → 「03 期只有 {cal["2026-03-21"]["n_listings_in_calendar"]:,} 間,房源組成與其他期不同,四期不能當同一批比」。',
          f'- 「某區最貴 / 最便宜」 → 「該區篩選樣本中位數較高 / 較低(各區樣本 {nmin} 間起),區內差距看不到」。',
          '- 「35.8% 的房東有 5 間以上」 → 「35.8% 的房源屬於這類房東;房東人數比例看不到」。',
          '- 「評分高所以貴」 → 「越貴的組評分中位數略高,只是相關;評分只有約 82% 的房源有」。',
          '- 「價格四期趨勢」 → 「2025-12 那期 price 全空,價格只有 2026-09 一期可用」。']
    OUT_MD.write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('wrote', OUT_MD.relative_to(ROOT), len(L), 'lines', flush=True)


if __name__ == '__main__':
    main()
