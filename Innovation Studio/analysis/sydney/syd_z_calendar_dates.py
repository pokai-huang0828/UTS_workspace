"""雪梨 Airbnb 日曆:哪些日子看起來特別滿?週末和平日差多少?(scope ID: IS-1114-calendar-01)

只用 calendar.csv.gz 的 available(t/f)與 minimum_nights 兩個訊號;資料沒有每天的價格。
- 第 1 天 = 該期 calendar 最早的日期(= 抓取日),第 1-120 天 = [base, base+120)。與 syd_a_market.py 的窗口定義一致。
- 「可以互相比的房子」= 整套(Entire home/apt)、1-2 房、2-4 人、listings 的 minimum_nights 1-7 晚(同 syd_a_market.scope_mask),用該期 listings 篩。
- 突出程度 = 當天數值 - 前後各 W 天內同一個星期幾(排除自己)的中位數;W=14 為主、W=21 為穩定度檢查。
  鄰居日可以落在第 121 天以後(資料有約 365 天),但只對第 1-120 天排名;鄰居少於 2 個的日子不排名。
產出:Innovation Studio/notes/raw/syd_z_calendar_dates_2026-11-14.json / .md
"""
import csv
import gzip
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'scratchpad/insideairbnb_sydney'
RAW = ROOT / 'Innovation Studio/notes/raw'
OUT_JSON = RAW / 'syd_z_calendar_dates_2026-11-14.json'
OUT_MD = RAW / 'syd_z_calendar_dates_2026-11-14.md'
PERIODS = ['2025-12-12', '2026-03-21', '2026-06-16', '2026-09-16']
EXPECT_ROWS = {'2025-12-12': 20436, '2026-03-21': 13563, '2026-06-16': 20573, '2026-09-16': 20833}
CHECK_PERIOD = '2026-09-16'   # 用 csv 模組獨立重算的那一期
H = 120
TOPK = 12
NEAR = 7                      # 每一批房源日曆開始日起 7 天標「近抓取日」(頭幾天幾乎訂不到,且只能跟後面比)
BOTH_K = 24                   # 第 5 步:兩個訊號都排進該期前 24 名(第 1-120 天的前 20%)才算「都突出」
WD = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
GROUPS = {'all': '全部房源', 'scope': '可以互相比的房子'}
SUMS = ['n', 'f', 'mn_n', 'mn3', 'mn_sum']


def read_scope(period):
    df = pd.read_csv(DATA / period / 'data/listings.csv.gz', dtype=str, keep_default_na=False,
                     usecols=['id', 'room_type', 'bedrooms', 'accommodates', 'minimum_nights'])
    acc = pd.to_numeric(df['accommodates'], errors='coerce')
    mn = pd.to_numeric(df['minimum_nights'], errors='coerce')
    m = ((df['room_type'] == 'Entire home/apt') & df['bedrooms'].isin(['1', '2'])
         & acc.between(2, 4) & mn.between(1, 7))
    return len(df), set(df.loc[m, 'id']), set(df['id'])


def daily_sums(period, scope_ids):
    """逐 chunk 彙總成每個日期的計數(全部 / 可互比)。"""
    tot, ids, dup, firsts = None, set(), 0, []
    for ch in pd.read_csv(DATA / period / 'data/calendar.csv.gz', dtype=str, chunksize=2_000_000,
                          usecols=['listing_id', 'date', 'available', 'minimum_nights']):
        mn = pd.to_numeric(ch['minimum_nights'], errors='coerce')
        ins = ch['listing_id'].isin(scope_ids).to_numpy()
        d = pd.DataFrame({'date': ch['date'], 'n': 1, 'f': (ch['available'] == 'f').astype(int),
                          'mn_n': mn.notna().astype(int), 'mn3': (mn >= 3).astype(int), 'mn_sum': mn.fillna(0)})
        for c in SUMS:
            d['s_' + c] = d[c] * ins
        dup += int(ch.duplicated(['listing_id', 'date']).sum())
        ids.update(ch['listing_id'].unique())
        firsts.append(ch.groupby('listing_id')['date'].min())
        g = d.groupby('date').sum()
        tot = g if tot is None else tot.add(g, fill_value=0)
    tot = tot.sort_index()
    base = pd.Timestamp(tot.index[0])
    tot.index = [(pd.Timestamp(x) - base).days + 1 for x in tot.index]  # 第幾天
    first = pd.concat(firsts).groupby(level=0).min().value_counts().sort_index()
    first_dist = {k: int(v) for k, v in first.items()}  # 每間房的日曆從哪一天開始
    return tot, base, ids, dup, first_dist


def group_series(tot, g):
    p = '' if g == 'all' else 's_'
    return pd.DataFrame({'n': tot[p + 'n'], 'f': tot[p + 'f'],
                         'rate': tot[p + 'f'] / tot[p + 'n'],
                         'mn3': tot[p + 'mn3'] / tot[p + 'mn_n'],
                         'mn_mean': tot[p + 'mn_sum'] / tot[p + 'mn_n']})


def excess(s, W, skip=()):
    """skip:房源未到齊的日子(房源組成和其他天不同),不拿來當比較對象。"""
    out = {}
    for d in s.index:
        nb = [s[d + k] for k in range(-W, W + 1, 7)
              if k != 0 and (d + k) in s.index and (d + k) not in skip and pd.notna(s[d + k])]
        out[d] = s[d] - float(np.median(nb)) if len(nb) >= 2 else np.nan
    return pd.Series(out)


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def topk(ex, k=TOPK):
    e = ex.loc[1:H].dropna().sort_values(ascending=False)
    return [int(d) for d in e.index[:k]]


def segments(days, base, val):
    """把排名裡連續的第幾天合成一段;val: 第幾天 -> 多出的百分比(比例差)。"""
    days = sorted(days)
    segs, cur = [], [days[0]] if days else []
    for d in days[1:]:
        if d == cur[-1] + 1:
            cur.append(d)
        else:
            segs.append(cur)
            cur = [d]
    if cur:
        segs.append(cur)
    out = []
    for s in segs:
        a, b = base + pd.Timedelta(days=s[0] - 1), base + pd.Timedelta(days=s[-1] - 1)
        out.append({'start': a.strftime('%Y-%m-%d'), 'end': b.strftime('%Y-%m-%d'),
                    'start_wd': WD[a.dayofweek], 'end_wd': WD[b.dayofweek], 'days': len(s),
                    'day_from': s[0], 'day_to': s[-1],
                    'max_excess': r4(max(val[d] for d in s)), 'mean_excess': r4(np.mean([val[d] for d in s]))})
    return out


def annot(segs, flag):
    for s in segs:
        s['flag'] = '、'.join(sorted({f for d in range(s['day_from'], s['day_to'] + 1) for f in flag[d].split('、') if f}))
    return segs


def date_of(base, d):
    t = base + pd.Timedelta(days=d - 1)
    return t.strftime('%Y-%m-%d'), WD[t.dayofweek]


def csv_recount(period, dates, scope_ids):
    """另一種寫法:csv 模組逐列數(不經 pandas)。"""
    c = {dt: {'n': 0, 'f': 0, 's_n': 0, 's_f': 0} for dt in dates}
    with gzip.open(DATA / period / 'data/calendar.csv.gz', 'rt', encoding='utf-8', newline='') as fh:
        r = csv.reader(fh)
        h = next(r)
        il, idt, iav = h.index('listing_id'), h.index('date'), h.index('available')
        for row in r:
            x = c.get(row[idt])
            if x is None:
                continue
            f = row[iav] == 'f'
            x['n'] += 1
            x['f'] += f
            if row[il] in scope_ids:
                x['s_n'] += 1
                x['s_f'] += f
    return c


def main():
    t0 = time.time()
    res = {'scope_id': 'IS-1114-calendar-01', 'generated': '2026-11-14',
           'definitions': {
               'day_1': '該期 calendar 最早日期(= 抓取日);第 1-120 天 = 抓取日起 120 個日期',
               'blocked_rate': '那一天 available = f 的房源數 ÷ 那一天有紀錄的房源數',
               'scope': '整套(Entire home/apt)、bedrooms 1-2、accommodates 2-4、listings minimum_nights 1-7;用該期 listings 篩',
               'weekend': '週五、週六晚(日期是週五或週六);平日 = 週日到週四晚;只用第 1-120 天,先算每天比例再平均',
               'excess': '當天 - 前後各 W 天同星期幾(排除自己)的中位數;W=14 主、W=21 檢查;鄰居可在第 121 天後;'
                         '「房源未到齊」的日子不當鄰居;鄰居 < 2 個不排名',
               'flags': '近抓取日 = 每一批(>= 1% 房源)日曆開始日起 7 天;房源未到齊 = 那天有紀錄房源 < 第 1-120 天最多那天',
               'mn3': '那一天 calendar minimum_nights >= 3 的房源 ÷ 那一天 minimum_nights 有值的房源',
               'both': f'第 5 步:同一天在「不能訂多出」與「最少住 3 晚以上多出」都排進該期前 {BOTH_K} 名(全部房源、W=14)且兩者 > 0',
           }, 'periods': {}}
    for p in PERIODS:
        n_rows, scope_ids, list_ids = read_scope(p)
        tot, base, cal_ids, dup, first_dist = daily_sums(p, scope_ids)
        full_n = tot.loc[1:H, 'n'].max()
        # 每一批(>= 1% 房源)日曆開始日起 NEAR 天 = 近抓取日;有紀錄房源少於最多那天 = 房源未到齊
        starts = [(pd.Timestamp(k) - base).days + 1 for k, v in first_dist.items() if v >= 0.01 * n_rows]
        near = {d for st in starts for d in range(st, st + NEAR)}
        thin = {d for d in range(1, H + 1) if tot.loc[d, 'n'] < full_n}
        flag = {d: '、'.join(x for x, c in (('近抓取日', d in near), ('房源未到齊', d in thin)) if c)
                for d in range(1, H + 1)}
        P = {'base_date': base.strftime('%Y-%m-%d'), 'calendar_first_date_by_listing': first_dist,
             'flagged_days': {date_of(base, d)[0]: f for d, f in flag.items() if f},
             'listings_rows': n_rows, 'listings_rows_expected': EXPECT_ROWS[p],
             'scope_listings': len(scope_ids), 'calendar_listings': len(cal_ids),
             'calendar_ids_not_in_listings': len(cal_ids - list_ids), 'listings_ids_not_in_calendar': len(list_ids - cal_ids),
             'duplicate_listing_date_rows': dup, 'calendar_days': int(tot.index.max()),
             'day1_n': {'all': int(tot.loc[1, 'n']), 'scope': int(tot.loc[1, 's_n'])},
             'day120_n': {'all': int(tot.loc[H, 'n']), 'scope': int(tot.loc[H, 's_n'])}}
        S = {g: group_series(tot, g) for g in GROUPS}
        EX = {g: {'b14': excess(S[g]['rate'], 14, thin), 'b21': excess(S[g]['rate'], 21, thin),
                  'm14': excess(S[g]['mn3'], 14, thin), 'm21': excess(S[g]['mn3'], 21, thin),
                  'mm14': excess(S[g]['mn_mean'], 14, thin)} for g in GROUPS}
        days = list(range(1, H + 1))
        P['daily'] = []
        for d in days:
            dt, wd = date_of(base, d)
            row = {'day': d, 'date': dt, 'wd': wd}
            for g in GROUPS:
                s = S[g].loc[d]
                row[g] = {'n': int(s['n']), 'blocked_rate': r4(s['rate']), 'mn3_share': r4(s['mn3']),
                          'mn_mean': r4(s['mn_mean']), 'blocked_excess_w14': r4(EX[g]['b14'][d]),
                          'blocked_excess_w21': r4(EX[g]['b21'][d]), 'mn3_excess_w14': r4(EX[g]['m14'][d]),
                          'mn_mean_excess_w14': r4(EX[g]['mm14'][d])}
            P['daily'].append(row)
        # 1. 分段摘要
        P['summary'] = {}
        for g in GROUPS:
            r = S[g]['rate'].loc[1:H]
            P['summary'][g] = {f'{a}-{b}': r4(r.loc[a:b].mean()) for a, b in [(1, 30), (31, 60), (61, 90), (91, 120)]}
            P['summary'][g].update({'mean_1_120': r4(r.mean()), 'min': r4(r.min()), 'min_date': date_of(base, int(r.idxmin()))[0],
                                    'max': r4(r.max()), 'max_date': date_of(base, int(r.idxmax()))[0]})
        # 2. 週末對平日
        wdx = pd.Series({d: (base + pd.Timedelta(days=d - 1)).dayofweek for d in days})
        P['weekend'] = {}
        for g in GROUPS:
            r = S[g]['rate'].loc[1:H]
            we, wk = r[wdx.isin([4, 5])].mean(), r[wdx.isin([6, 0, 1, 2, 3])].mean()
            ok = pd.Series({d: not flag[d] for d in days})
            we2, wk2 = r[wdx.isin([4, 5]) & ok].mean(), r[wdx.isin([6, 0, 1, 2, 3]) & ok].mean()
            P['weekend'][g] = {'fri_sat': r4(we), 'sun_thu': r4(wk), 'diff_pp': round((we - wk) * 100, 2),
                               'diff_pp_excl_flagged_days': round((we2 - wk2) * 100, 2), 'n_flagged_days': int((~ok).sum()),
                               'n_fri_sat_days': int(wdx.isin([4, 5]).sum()), 'n_sun_thu_days': int(wdx.isin([6, 0, 1, 2, 3]).sum())}
        # 3/4. 前 12 名與連續段
        P['top_blocked'], P['top_mn3'], P['stability'] = {}, {}, {}
        for g in GROUPS:
            o = 'scope' if g == 'all' else 'all'
            tb = topk(EX[g]['b14'])
            P['top_blocked'][g] = {'days': [{'day': d, 'date': date_of(base, d)[0], 'wd': date_of(base, d)[1],
                                             'blocked_rate': r4(S[g]['rate'][d]), 'excess': r4(EX[g]['b14'][d]),
                                             'excess_other_group': r4(EX[o]['b14'][d]), 'mn3_excess': r4(EX[g]['m14'][d]),
                                             'flag': flag[d]}
                                            for d in tb],
                                   'segments': annot(segments(tb, base, EX[g]['b14']), flag)}
            tm = topk(EX[g]['m14'])
            P['top_mn3'][g] = {'days': [{'day': d, 'date': date_of(base, d)[0], 'wd': date_of(base, d)[1],
                                         'mn3_share': r4(S[g]['mn3'][d]), 'excess': r4(EX[g]['m14'][d]),
                                         'mn_mean': r4(S[g]['mn_mean'][d]), 'mn_mean_excess': r4(EX[g]['mm14'][d]),
                                         'excess_other_group': r4(EX[o]['m14'][d]), 'blocked_excess': r4(EX[g]['b14'][d]),
                                         'flag': flag[d]}
                                        for d in tm],
                               'segments': annot(segments(tm, base, EX[g]['m14']), flag)}
            # 6. 穩定度
            tb21, tm21 = topk(EX[g]['b21']), topk(EX[g]['m21'])
            P['stability'][g] = {'blocked_same_in_top12': len(set(tb) & set(tb21)), 'mn3_same_in_top12': len(set(tm) & set(tm21)),
                                 'blocked_w21_only': [date_of(base, d)[0] for d in tb21 if d not in tb],
                                 'mn3_w21_only': [date_of(base, d)[0] for d in tm21 if d not in tm]}
        # 5. 兩個訊號都突出(全部房源)
        rb = EX['all']['b14'].loc[1:H].rank(ascending=False, method='min')
        rm = EX['all']['m14'].loc[1:H].rank(ascending=False, method='min')
        both = [d for d in days if rb.get(d, 999) <= BOTH_K and rm.get(d, 999) <= BOTH_K
                and EX['all']['b14'][d] > 0 and EX['all']['m14'][d] > 0]
        segs = annot(segments(both, base, EX['all']['b14']), flag) if both else []
        for s in segs:
            rng = range(s['day_from'], s['day_to'] + 1)
            s['period'] = p
            s['mn3_max_excess'] = r4(max(EX['all']['m14'][d] for d in rng))
            s['scope_blocked_max_excess'] = r4(max(EX['scope']['b14'][d] for d in rng))
            s['scope_mn3_max_excess'] = r4(max(EX['scope']['m14'][d] for d in rng))
        P['both'] = segs
        P['_ex'] = EX  # 暫存(不寫進 json)
        P['_base'] = base
        P['_scope_ids'] = scope_ids
        res['periods'][p] = P
        print(f'{p} done {time.time() - t0:.0f}s', flush=True)

    res['both_all_periods'] = sorted([s for p in PERIODS for s in res['periods'][p]['both']], key=lambda s: s['start'])

    # 驗算:csv 模組重算兩個日期(第 1 天 + 該期全部房源不能訂多出最多的那天)
    C = res['periods'][CHECK_PERIOD]
    d2 = C['top_blocked']['all']['days'][0]['date']
    chk_dates = [C['base_date'], d2]
    rc = csv_recount(CHECK_PERIOD, chk_dates, C['_scope_ids'])
    by_date = {r['date']: r for r in C['daily']}
    res['check_csv_recount'] = {'period': CHECK_PERIOD, 'rows': []}
    for dt in chk_dates:
        x, r = rc[dt], by_date[dt]
        a_rate, s_rate = x['f'] / x['n'], x['s_f'] / x['s_n']
        res['check_csv_recount']['rows'].append({
            'date': dt, 'csv_all': f"{x['f']}/{x['n']}", 'csv_all_rate': r4(a_rate), 'pandas_all_rate': r['all']['blocked_rate'],
            'csv_scope': f"{x['s_f']}/{x['s_n']}", 'csv_scope_rate': r4(s_rate), 'pandas_scope_rate': r['scope']['blocked_rate'],
            'match': r4(a_rate) == r['all']['blocked_rate'] and r4(s_rate) == r['scope']['blocked_rate']
                     and x['n'] == r['all']['n'] and x['s_n'] == r['scope']['n']})
    print(f'csv recount done {time.time() - t0:.0f}s', flush=True)

    for p in PERIODS:
        for k in ('_ex', '_base', '_scope_ids'):
            res['periods'][p].pop(k)
    res['seconds'] = round(time.time() - t0, 1)
    OUT_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    OUT_MD.write_text(render_md(res), encoding='utf-8')
    print('wrote', OUT_JSON.name, OUT_MD.name, f'{time.time() - t0:.0f}s')


# ---------- 筆記 ----------
def pct(x):
    return '—' if x is None else f'{x * 100:.1f}%'


def pp(x):
    return '—' if x is None else f'{x * 100:+.1f}'


def md_table(head, rows):
    o = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    o += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(o)


def seg_txt(s):
    if s['days'] == 1:
        return f"{s['start']}({s['start_wd']})"
    return f"{s['start']}({s['start_wd']})到 {s['end']}({s['end_wd']}),{s['days']} 天"


def render_md(res):
    Ps = res['periods']
    o = []
    # 開頭三行結論
    we = [Ps[p]['weekend']['all']['diff_pp'] for p in PERIODS]
    segs = sorted([dict(s, period=p) for p in PERIODS for s in Ps[p]['top_blocked']['all']['segments'] if not s['flag']],
                  key=lambda s: -s['max_excess'])[:3]
    o.append('# 雪梨 Airbnb 日曆:哪些日子特別滿?週末和平日差多少?(2026-11-14)\n')
    o.append(f"**結論 1:** 週五、週六晚的不能訂比例,比週日到週四晚高 {min(we):.1f} 到 {max(we):.1f} 個百分點"
             f"(全部房源,四期各自抓取日後第 1–120 天;各期分別是 " + '、'.join(f'{p} 期 {w:+.1f}' for p, w in zip(PERIODS, we)) + ')。  ')
    o.append('**結論 2:** 扣掉「前後各 14 天同星期幾」的中位數後,最突出的幾段是 '
             + ';'.join(f"{seg_txt(s)} 多 {s['max_excess'] * 100:.1f} 個百分點({s['period']} 期)" for s in segs)
             + '(全部房源;標「近抓取日」「房源未到齊」的日子不算,見第 0 節)。  ')
    o.append('**結論 3:** 這個方法能看到「哪幾天不能訂的房源特別多」和「房東在哪幾天把最少住幾晚調高」;'
             '看不到價格、分不出被訂走還是房東自己關、也看不到原因(是什麼假期或活動要另外用官方日期對)。\n')
    o.append('資料:Inside Airbnb 雪梨四期 calendar.csv.gz(available、minimum_nights;沒有每天的價格)。'
             '腳本:`Innovation Studio/analysis/sydney/syd_z_calendar_dates.py`。第 1 天 = 該期抓取日(calendar 最早日期)。'
             '「可以互相比的房子」= 整套、1–2 房、2–4 人、最低入住 1–7 晚(用該期 listings 篩,同 syd_a_market.py)。'
             '百分點 = 兩個比例相減後 ×100。\n')

    # 資料檢查
    o.append('## 0. 資料檢查\n')
    rows = []
    for p in PERIODS:
        P = Ps[p]
        ok = '一致' if P['day1_n']['all'] == P['listings_rows'] == P['listings_rows_expected'] else '不一致'
        rows.append([p, P['base_date'], f"{P['listings_rows']:,}", f"{P['day1_n']['all']:,}", ok, f"{P['scope_listings']:,}",
                     f"{P['day1_n']['scope']:,}", f"{P['day120_n']['all']:,}", P['duplicate_listing_date_rows']])
    o.append(md_table(['期別', '第 1 天日期', 'listings 列數', '第 1 天有紀錄房源', '對得上?', '可互比(listings)',
                       '可互比第 1 天', '第 120 天有紀錄房源', '重複列'], rows))
    ck = res['check_csv_recount']
    o.append('\n為什麼第 1 天的房源數會少:每間房的日曆不是同一天抓的。各期「日曆從哪一天開始」的房源數:')
    for p in PERIODS:
        P = Ps[p]
        o.append(f"- {p} 期:" + '、'.join(f'{k} 開始 {v:,} 間' for k, v in P['calendar_first_date_by_listing'].items())
                 + f";所以第 1 天只有 {P['day1_n']['all']:,} 間有紀錄,到第 120 天是 {P['day120_n']['all']:,} 間(= listings 列數)。")
    o.append(f'- 處理方式:每一批房源(占 1% 以上)的日曆開始日起 {NEAR} 天標「近抓取日」(抓取當天和頭幾天本來就幾乎訂不到,'
             '而且第 1 週前面沒有日子可以比、只能跟後面比,多出的數字會偏大);有紀錄房源少於該期最多那天的日子標「房源未到齊」。'
             '這些日子照樣排名,表格「注意」欄會標出來,開頭結論不拿它們當「最突出」。'
             '算「前後同星期幾的中位數」時,不拿「房源未到齊」的日子當比較對象(那幾天的房源組成和其他天不同)。')
    o.append('- 2026-06-16 期特別要小心:有 4,853 間房的日曆從 06-28、06-29 才開始,所以 06-28 到 07-05 對這批房源來說也是「近抓取日」,'
             '07-01 到 07-05 的數字可能有一部分是這個原因。')
    o.append(f"\n另一種寫法驗算({ck['period']} 期,用 Python csv 模組逐列數,不經 pandas):")
    for r in ck['rows']:
        o.append(f"- {r['date']}:全部 {r['csv_all']} = {pct(r['csv_all_rate'])}(pandas {pct(r['pandas_all_rate'])});"
                 f"可互比 {r['csv_scope']} = {pct(r['csv_scope_rate'])}(pandas {pct(r['pandas_scope_rate'])});"
                 f"{'一致' if r['match'] else '不一致'}")
    o.append('')

    # 1
    o.append('## 1. 每一期第 1–120 天的不能訂比例(分段平均)\n')
    o.append('每天的數字在 json 的 `periods.<期別>.daily`。這裡只放分段平均和最高、最低那天。\n')
    rows = []
    for p in PERIODS:
        for g, gn in GROUPS.items():
            s = Ps[p]['summary'][g]
            rows.append([p, gn, pct(s['1-30']), pct(s['31-60']), pct(s['61-90']), pct(s['91-120']), pct(s['mean_1_120']),
                         f"{pct(s['max'])}({s['max_date']})", f"{pct(s['min'])}({s['min_date']})"])
    o.append(md_table(['期別', '哪一群', '第 1–30 天', '第 31–60 天', '第 61–90 天', '第 91–120 天', '第 1–120 天',
                       '最高那天', '最低那天'], rows))
    o.append('\n怎麼讀:比例會跟著「離抓取日多遠」變,所以下面第 3 步不直接比大小,而是跟前後同星期幾比。\n')

    # 2
    o.append('## 2. 週末對平日(第 1–120 天)\n')
    rows = []
    for p in PERIODS:
        for g, gn in GROUPS.items():
            w = Ps[p]['weekend'][g]
            rows.append([p, gn, pct(w['fri_sat']), pct(w['sun_thu']), f"{w['diff_pp']:+.1f}",
                         f"{w['n_fri_sat_days']} / {w['n_sun_thu_days']}",
                         f"{w['diff_pp_excl_flagged_days']:+.1f}(去掉 {w['n_flagged_days']} 天)"])
    o.append(md_table(['期別', '哪一群', '週五、週六晚', '週日到週四晚', '差(百分點)', '天數(週末/平日)',
                       '去掉標註日子後的差'], rows))
    o.append('\n怎麼讀:先算每一天的比例,再把週五、週六的日子平均、週日到週四的日子平均,相減。\n')

    # 3
    o.append('## 3. 不能訂比例特別突出的日子(每期前 12 名,全部房源)\n')
    o.append('多出 = 那一天的比例 − 前後各 14 天同一個星期幾(不含自己)的中位數,單位百分點。'
             '「可互比多出」是同一天在「可以互相比的房子」那一群的多出;「最少住 3 晚多出」是第 4 步的訊號在同一天的值。'
             '可互比那一群自己的前 12 名在 json `top_blocked.scope`。\n')
    for p in PERIODS:
        T = Ps[p]['top_blocked']['all']
        o.append(f'### {p} 期(第 1–120 天)\n')
        o.append(md_table(['名次', '日期', '星期', '第幾天', '不能訂比例', '多出(百分點)', '可互比多出', '最少住 3 晚多出', '注意'],
                          [[i + 1, r['date'], r['wd'], r['day'], pct(r['blocked_rate']), pp(r['excess']),
                            pp(r['excess_other_group']), pp(r['mn3_excess']), r['flag']] for i, r in enumerate(T['days'])]))
        multi = [s for s in T['segments'] if s['days'] > 1]
        o.append('\n連起來的段:' + ('; '.join(f"{seg_txt(s)},最多多 {s['max_excess'] * 100:.1f}" + (f"(注意:{s['flag']})" if s['flag'] else '') for s in multi)
                                    if multi else '沒有(前 12 名都是單日)') + '\n')

    # 4
    o.append('## 4. 最少住幾晚:房東把門檻調高的日子(每期前 12 名,全部房源)\n')
    o.append('訊號 = 那一天要求最少住 3 晚以上的房源比例;多出的算法同第 3 步。也列出「最少住幾晚的平均」與它的多出(單位:晚)。'
             '平均會被少數要求住 30 晚、90 晚以上的房源拉高,所以排名用 3 晚以上的比例。\n')
    for p in PERIODS:
        T = Ps[p]['top_mn3']['all']
        o.append(f'### {p} 期(第 1–120 天)\n')
        o.append(md_table(['名次', '日期', '星期', '第幾天', '最少住 3 晚以上', '多出(百分點)', '最少住幾晚平均', '平均多出(晚)',
                           '可互比多出', '不能訂多出', '注意'],
                          [[i + 1, r['date'], r['wd'], r['day'], pct(r['mn3_share']), pp(r['excess']),
                            f"{r['mn_mean']:.1f}", f"{r['mn_mean_excess']:+.2f}", pp(r['excess_other_group']),
                            pp(r['blocked_excess']), r['flag']] for i, r in enumerate(T['days'])]))
        multi = [s for s in T['segments'] if s['days'] > 1]
        o.append('\n連起來的段:' + ('; '.join(f"{seg_txt(s)},最多多 {s['max_excess'] * 100:.1f}" + (f"(注意:{s['flag']})" if s['flag'] else '') for s in multi)
                                    if multi else '沒有(前 12 名都是單日)') + '\n')

    # 5
    o.append('## 5. 兩個訊號都突出的日子(四期合起來)\n')
    o.append(f'規則:同一天在該期第 1–120 天裡,「不能訂多出」和「最少住 3 晚以上多出」都排進前 {BOTH_K} 名(約前 20%),'
             '而且兩個都大於 0;全部房源、前後各 14 天。連續的日子合成一段,數字取段內最大。只寫日期和星期幾,是什麼假期或活動由別人用官方日期對。\n')
    B = res['both_all_periods']
    if B:
        o.append(md_table(['日期或日期段', '哪一期看到的', '第幾天', '不能訂多出(百分點)', '最少住 3 晚以上多出(百分點)',
                           '可互比:不能訂多出', '可互比:3 晚以上多出', '注意'],
                          [[seg_txt(s), s['period'], f"{s['day_from']}–{s['day_to']}" if s['days'] > 1 else s['day_from'],
                            pp(s['max_excess']), pp(s['mn3_max_excess']), pp(s['scope_blocked_max_excess']),
                            pp(s['scope_mn3_max_excess']), s['flag']] for s in B]))
    else:
        o.append('沒有日子同時符合。')
    o.append('')

    # 6
    o.append('## 6. 穩不穩:把「前後各 14 天」改成「前後各 21 天」\n')
    rows = []
    for p in PERIODS:
        for g, gn in GROUPS.items():
            s = Ps[p]['stability'][g]
            rows.append([p, gn, f"{s['blocked_same_in_top12']}/12", f"{s['mn3_same_in_top12']}/12",
                         ', '.join(s['blocked_w21_only']) or '—'])
    o.append(md_table(['期別', '哪一群', '不能訂前 12 名一樣的', '最少住 3 晚前 12 名一樣的', '21 天才進前 12 的日子(不能訂)'], rows))
    o.append('\n怎麼讀:一樣的越多,代表名單不太受「跟前後幾天比」的選法影響。\n')

    # 怎麼講才對
    o.append('## 怎麼講才對\n')
    o.append('- 不要這樣說:「這幾天被訂走比較多」「需求比較高」。→ 改這樣說:「這幾天不能訂的房源比較多」;'
             '不能訂 = 被訂走或房東自己關掉,資料分不出來(同 20_雪梨深度分析.md 的講法)。')
    o.append('- 不要這樣說:「四個月後那幾天已經很滿了」。→ 改這樣說:「離抓取日越遠越不準;遠的日子不能訂,'
             '有一部分是房東還沒開放日曆。所以我們只跟前後幾天、同一個星期幾比,看多出多少」。')
    o.append('- 不要這樣說:「這幾天價格比較高」「房東漲價」。→ 改這樣說:「這裡量的是滿不滿(不能訂的比例)和房東的設定'
             '(最少住幾晚),資料沒有每天的價格」。')
    o.append('- 不要這樣說:「12 月那期比 3 月那期滿」。→ 改這樣說:「四期的房源數不同(2026-03-21 那期只有 13,563 間,'
             '其他三期約 2.04 萬到 2.08 萬間),抓取日也在不同季節,不能把四期的比例直接互相比;要比就比同一期裡面的週末對平日、'
             '某一天對前後幾天」。')
    o.append('- 不要這樣說:「這是某某節日造成的」。→ 改這樣說:「這幾個日期在兩個訊號上都突出(列日期與星期幾);'
             '是不是假期或活動,要對官方日期表才知道,而且就算對上,也只是時間上重疊,不代表是它造成的」。')
    o.append('- 不要這樣說:「最少住幾晚平均變高很多」。→ 改這樣說:「要求最少住 3 晚以上的房源比例多了 X 個百分點'
             '(哪一期、全部房源、第幾天)」;平均會被少數長住房源拉高。')
    o.append('- 不要這樣說:「抓取當天最滿,多出三十幾個百分點」。→ 改這樣說:「抓取當天和頭幾天本來就幾乎訂不到,而且只能跟後面的日子比,所以標「近抓取日」的多出不算數;要看的是其他日子跟前後同星期幾比還多出來的部分」。')
    o.append('- 每個數字都講清楚:哪一期、哪一群房子(全部房源 / 可以互相比的房子)、抓取日後第幾天到第幾天。\n')
    o.append(f"<sub>來源:syd_z_calendar_dates_2026-11-14.json;腳本執行約 {res['seconds']:.0f} 秒</sub>")
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    main()
