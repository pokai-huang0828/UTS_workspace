"""T1 找同類。

規則(照報告):同區 × 同臥室數為一組;該組不足 30 間 → 改用全市同臥室數、距離最近的 30 間。
組內依「可住人數差距」(小的在前)和「設施 Jaccard 相似度」(大的在前)排序,回傳前 10–20 間與匹配理由。
匹配只用下面 MATCH_COLS 這幾欄,刻意不把價格欄傳進來(避免拿價格找價格的循環論證)。
"""
import numpy as np

from . import data_access as D

MIN_GROUP = 30
K_NEAR = 30
MATCH_COLS = ['id', 'nb', 'bed_n', 'acc', 'lat', 'lon', 'amen']   # 不含任何價格欄


def peer_group(pool, nb, bed_n, lat=None, lon=None):
    """回傳 (同類那一組的 id 陣列, 用了哪一層規則, 用到的經緯度)。pool 只會用到 MATCH_COLS。"""
    m = pool[MATCH_COLS]
    if lat is None or lon is None:
        lat, lon = D.nb_center(nb)
    g = m[(m.nb == nb) & (m.bed_n == bed_n)]
    if len(g) >= MIN_GROUP:
        return g.id.values, '同區同臥室數', (lat, lon), len(g)
    p = m[m.bed_n == bed_n]
    dist = D.km(lat, lon, p.lat.values, p.lon.values)
    # 距離一樣時用 id 排,讓結果固定
    order = np.lexsort((p.id.values, dist))[:K_NEAR]
    return p.id.values[order], f'同區同臥室數只有 {len(g)} 間(不足 {MIN_GROUP}),改用全市同臥室數最近 {K_NEAR} 間', (lat, lon), len(g)


def find_peers(pool, nb, bed_n, acc, amen, lat=None, lon=None, top_n=20):
    """T1 主函式。top_n 會被限制在 10–20 之間。"""
    top_n = int(min(20, max(10, top_n)))
    amen = frozenset(amen)
    ids, level, (lat, lon), n_same = peer_group(pool, nb, bed_n, lat, lon)
    m = pool[MATCH_COLS]
    g = m[m.id.isin(set(ids))].copy()
    g['acc_diff'] = (g.acc - acc).abs()
    g['jac'] = g.amen.map(lambda s: D.jaccard(s, amen))
    g['common'] = g.amen.map(lambda s: len(s & amen))
    g['dist_km'] = D.km(lat, lon, g.lat.values, g.lon.values)
    g = g.sort_values(['acc_diff', 'jac', 'id'], ascending=[True, False, True])
    top = g.head(top_n)
    rows = []
    for r in top.itertuples():
        reasons = ['同區' if r.nb == nb else f'不同區(距離約 {r.dist_km:.1f} 公里)',
                   f'同為 {r.bed_n} 臥室', f'可住人數差 {r.acc_diff} 人', f'共同設施 {r.common} 項']
        rows.append({'id': r.id, 'nb': r.nb, 'bedrooms': int(r.bed_n), 'acc': int(r.acc), 'amen_n': len(r.amen),
                     'jaccard': round(float(r.jac), 3), 'acc_diff': int(r.acc_diff), 'common': int(r.common),
                     'reason': ';'.join(reasons)})
    return {'group_ids': list(ids), 'group_n': len(ids), 'level': level, 'same_nb_bed_n': n_same, 'fallback': n_same < MIN_GROUP,
            'latlon_used': (round(lat, 5), round(lon, 5)), 'top': rows}
