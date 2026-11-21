"""T3 設施差距:同類每項設施的普及率;列出普及率 ≥ 門檻、而這間房沒有的設施。

門檻 80% 是報告寫的暫定值,做成參數 threshold。
"""
import pandas as pd

from . import data_access as D

DEFAULT_THRESHOLD = 0.80


def amenity_gaps(pool, group_ids, amen, threshold=DEFAULT_THRESHOLD):
    g = pool[pool.id.isin(set(group_ids))]
    n = len(g)
    cnt = pd.Series([a for s in g.amen for a in s]).value_counts()
    prev = (cnt / n).sort_values(ascending=False)
    amen = frozenset(amen)
    gaps = [{'amenity': a, 'pct': round(100 * float(p), 1)} for a, p in prev.items()
            if p >= threshold and a not in amen]
    gaps.sort(key=lambda x: (-x['pct'], x['amenity']))
    have = [{'amenity': a, 'pct': round(100 * float(prev.get(a, 0.0)), 1)} for a in sorted(amen)]
    return {'n': n, 'threshold_pct': round(100 * threshold, 1), 'gaps': gaps, 'have': have,
            'n_common_amen': int((prev >= threshold).sum())}


def resolve(pool, names):
    """設施名稱比對:不分大小寫、去頭尾空白,對到資料裡的標準寫法。
    回傳 (對到的標準名稱 frozenset, 對不到的原始輸入 list)。只差大小寫的多種寫法,取資料裡最常見的那種。"""
    cnt = pd.Series([a for s in pool.amen for a in s]).value_counts()
    canon = {}
    for a, c in sorted(cnt.items(), key=lambda x: (-x[1], x[0])):
        canon.setdefault(a.strip().lower(), a)
    ok, bad = set(), []
    for n in names:
        n = (n or '').strip()
        if not n:
            continue
        if n.lower() in canon:
            ok.add(canon[n.lower()])
        elif n not in bad:
            bad.append(n)
    return frozenset(ok), bad
