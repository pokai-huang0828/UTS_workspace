"""T7 淡旺季參考(只是參考,不預測價格)。

① 評論月份指數:可比房源 2024、2025 兩年的評論日期 → 每年各月占全年比例 × 12 × 100 → 兩年平均。
   100 = 平均月份;評論是住完才寫,高峰會比入住晚一點;評論數不是訂單數。
② 指定年份的 NSW 公眾假期(檔案只有 2021–2025)。
③ 日曆:同類房源未來 12 個月每月「不可訂」的比例;不可訂分不出是已被訂走還是房東自己關閉。
"""
import numpy as np
import pandas as pd

from . import data_access as D

PREV_NOV, PREV_MAY = 135.5, 75.3   # 之前的結果(notes/raw/syd_y_2024_2026_2026-11-11.md,評論檔全部房源)
CAL_MONTHS = [f'{y}-{m:02d}' for y, m in [(2026, 10), (2026, 11), (2026, 12)] + [(2027, k) for k in range(1, 10)]]


def review_index(ids):
    c = D.review_month_counts()
    c = c[c.listing_id.isin(set(ids))]
    per_year = {}
    for y in (2024, 2025):
        s = c[c.year == y].groupby('month').n.sum().reindex(range(1, 13), fill_value=0)
        per_year[y] = (s / s.sum() * 12 * 100) if s.sum() else s * np.nan
    avg = (per_year[2024] + per_year[2025]) / 2
    return {'n_listings': int(c.listing_id.nunique()), 'n_reviews': int(c.n.sum()),
            'index': {int(m): round(float(v), 1) for m, v in avg.items()},
            'index_2024': {int(m): round(float(v), 1) for m, v in per_year[2024].items()},
            'index_2025': {int(m): round(float(v), 1) for m, v in per_year[2025].items()},
            'mean': round(float(avg.mean()), 2),
            'nov_vs_prev': round(float(avg[11] - PREV_NOV), 1), 'may_vs_prev': round(float(avg[5] - PREV_MAY), 1)}


def holidays(year):
    h = D.nsw_holidays()
    h = h[h.date.dt.year == year]
    if h.empty:
        have = sorted(D.nsw_holidays().date.dt.year.unique())
        return {'year': year, 'items': [], 'note': f'{year} 年待補(手上的假期檔只有 {have[0]}–{have[-1]} 年)'}
    return {'year': year, 'items': [{'date': d.strftime('%Y-%m-%d'),
                                     'name': n + ('(只適用銀行業)' if 'bank holiday' in n.lower() else '')}
                                    for d, n in zip(h.date, h.name)],
            'note': f'NSW 公眾假期,共 {len(h)} 天'}


def calendar_unavail(ids, months=CAL_MONTHS):
    c = D.calendar_month_unavail()
    c = c[c.listing_id.isin(set(ids)) & c.ym.isin(months)]
    s = c.groupby('ym')[['days', 'unavail']].sum().reindex(months)
    n = c.groupby('ym').listing_id.nunique().reindex(months)
    return {'months': [{'ym': m, 'pct': None if pd.isna(s.at[m, 'days']) or not s.at[m, 'days']
                        else round(100 * float(s.at[m, 'unavail'] / s.at[m, 'days']), 1),
                        'n_listings': 0 if pd.isna(n.at[m]) else int(n.at[m])} for m in months],
            'note': '「不可訂」分不出是已被訂走還是房東自己關閉;資料是 2026-09-16 抓的,所以從下一個整月 2026-10 起算,'
                    '2027-09 只有到 9/16 的 16 天。'}


def season_reference(group_ids, pool, year=2026):
    return {'index_peers': review_index(group_ids), 'index_all': review_index(pool.id.values),
            'holidays': holidays(year), 'calendar': calendar_unavail(group_ids)}
