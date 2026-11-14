# -*- coding: utf-8 -*-
"""地圖資料:雪梨 38 區 + 區內小方格(約 550 公尺見方),輸出 map_data.json 給 index.html 的地圖用。

資料:scratchpad/insideairbnb_sydney/2026-09-16/(listings.csv.gz、visualisations/neighbourhoods.geojson)
算法照既有分析(數字要一致):
- 讀檔:Innovation Studio/analysis/sydney/syd_a_market.py 第 59-65 行(dtype=str、keep_default_na=False)
- 價格轉數字:同檔第 68-69 行 num()(去掉 , $ 空白)
- 篩選:同檔第 72-76 行 scope_mask()(整套、bedrooms 1-2、accommodates 2-4、minimum_nights 1-7)
- 有價:同檔第 359 行(price 去空白後非空)
- 區的中間價:同檔第 416 行(pandas median);1 房/2 房分組照 syd_b_positioning.py 第 98-117 行(篩選且有價,按 bedrooms 分)
- 不到 30 間不給 1 房/2 房中間價:同 syd_b 的分組門檻(筆記 20 第 79-81 行)
用法:python "Innovation Studio/meeting_1114/map_data.py"
不寫入任何房源編號、名稱、房東名;地名只取房東填的 neighbourhood 欄第一個逗號前的字,且同一格至少 3 間填同一個才給。
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / 'scratchpad' / 'insideairbnb_sydney' / '2026-09-16'
OUT = HERE / 'map_data.json'

CELL_LAT, CELL_LON = 0.005, 0.006
MIN_CELL_PRICED = 5      # 一格有價不到 5 間 → 中間價空值
MIN_BED_N = 30           # 區的 1 房/2 房不到 30 間 → 空值
MIN_PLACE = 3            # 同一格至少 3 間填同一個地名才給
GEO_BUDGET = 80 * 1024   # 邊界座標合計上限
EXPECT = {'rows': 20833, 'priced': 17721, 'scope': 7565, 'scope_priced': 6639, 'districts': 38,
          'all_priced_median': 338,
          'Sydney_1': (1291, 323), 'Sydney_2': (564, 455), 'Waverley_1': (387, 331), 'Manly_1': (237, 366)}
COLS = ['latitude', 'longitude', 'neighbourhood_cleansed', 'neighbourhood', 'room_type', 'bedrooms',
        'accommodates', 'minimum_nights', 'price']


def num(s):  # syd_a_market.py 第 68-69 行
    return pd.to_numeric(s.str.replace(r'[,$\s]', '', regex=True), errors='coerce')


def scope_mask(df):  # syd_a_market.py 第 72-76 行
    acc = pd.to_numeric(df['accommodates'], errors='coerce')
    mn = pd.to_numeric(df['minimum_nights'], errors='coerce')
    return ((df['room_type'] == 'Entire home/apt') & df['bedrooms'].isin(['1', '2'])
            & acc.between(2, 4) & mn.between(1, 7))


def med(s, min_n):
    s = s.dropna()
    if len(s) < min_n or len(s) == 0:
        return None
    v = round(float(s.median()), 2)
    return int(v) if v == int(v) else v


# ---------------- 邊界簡化(共用邊只簡化一次,相鄰兩區走同一組點,不會裂開) ----------------
COSLAT = math.cos(math.radians(33.87))


def dp(pts, tol):
    """Douglas-Peucker;pts 是 (lon, lat),距離用 lon×cos(緯度) 換成接近等距。保留頭尾。"""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a][0] * COSLAT, pts[a][1]
        bx, by = pts[b][0] * COSLAT, pts[b][1]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        best, bi = -1.0, -1
        for k in range(a + 1, b):
            px, py = pts[k][0] * COSLAT, pts[k][1]
            d = abs(dx * (ay - py) - dy * (ax - px)) / L if L > 0 else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, k
        if bi > 0 and best > tol:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [p for p, k in zip(pts, keep) if k]


def ring_area(r):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
        a += (x1 * COSLAT) * y2 - (x2 * COSLAT) * y1
    return a / 2


def simplify_all(feats, tol):
    rings = []  # (district, [pt...]) 不含重複的收尾點
    for name, geom in feats:
        polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
        for poly in polys:
            for ring in poly:
                pts = [(round(x, 7), round(y, 7)) for x, y in ring]
                if pts[0] == pts[-1]:
                    pts = pts[:-1]
                rings.append((name, pts))
    member = {}
    for ri, (_, pts) in enumerate(rings):
        for p in pts:
            member.setdefault(p, set()).add(ri)
    fixed = set()
    for ri, (_, pts) in enumerate(rings):
        n = len(pts)
        for k in range(n):
            m = member[pts[k]]
            if len(m) >= 3 or member[pts[k - 1]] != m or member[pts[(k + 1) % n]] != m:
                fixed.add(pts[k])
    out = {}
    shared = sum(1 for m in member.values() if len(m) >= 2)
    for name, pts in rings:
        n = len(pts)
        idx = [k for k in range(n) if pts[k] in fixed]
        if len(idx) < 2:
            base = idx[0] if idx else 0
            far = max(range(n), key=lambda k: (pts[k][0] - pts[base][0]) ** 2 + (pts[k][1] - pts[base][1]) ** 2)
            idx = sorted({base, far})
        res = []
        for t in range(len(idx)):
            a, b = idx[t], idx[(t + 1) % len(idx)]
            chain = pts[a:b + 1] if b > a else pts[a:] + pts[:b + 1]
            rev = chain[0] > chain[-1]
            c = dp(chain[::-1] if rev else chain, tol)
            if rev:
                c = c[::-1]
            res.extend(c[:-1])
        r4 = []
        for x, y in res:
            q = (round(x, 4), round(y, 4))
            if not r4 or r4[-1] != q:
                r4.append(q)
        if len(r4) > 1 and r4[0] == r4[-1]:
            r4.pop()
        if len(r4) >= 3:
            out.setdefault(name, []).append((r4, abs(ring_area(pts)), abs(ring_area(r4))))
    return out, shared, len(member)


def main():
    L = pd.read_csv(DATA / 'data' / 'listings.csv.gz', dtype=str, keep_default_na=False, usecols=lambda c: c in COLS)
    L['price_v'] = num(L['price'])
    L['scope'] = scope_mask(L)
    L['has_price'] = L['price'].str.strip() != ''          # syd_a_market.py 第 359 行
    L['lat'] = pd.to_numeric(L['latitude'], errors='coerce')
    L['lon'] = pd.to_numeric(L['longitude'], errors='coerce')
    assert L[['lat', 'lon']].notna().all().all(), '有房源沒有經緯度'
    assert L.loc[L['has_price'], 'price_v'].notna().all(), '有價列有無法解析的 price'
    L['ent'] = L['room_type'] == 'Entire home/apt'
    L['priv'] = L['room_type'] == 'Private room'
    L['pv'] = L['price_v'].where(L['has_price'])
    L['ci'] = (L['lat'] / CELL_LAT).apply(math.floor)
    L['cj'] = (L['lon'] / CELL_LON).apply(math.floor)
    L['place'] = L['neighbourhood'].str.split(',').str[0].str.strip().str.replace(r'\s+', ' ', regex=True)
    sp = L[L['scope'] & L['has_price']]

    geo = json.loads((DATA / 'visualisations' / 'neighbourhoods.geojson').read_text(encoding='utf-8'))
    feats = [(f['properties']['neighbourhood'], f['geometry']) for f in geo['features']]
    assert set(n for n, _ in feats) == set(L['neighbourhood_cleansed']), '區名與 geojson 對不上'

    # 邊界:從細到粗試,取第一個放得進 80 KB 的容許誤差
    for tol in (0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0008, 0.001, 0.0013, 0.0016, 0.002, 0.003):
        geom, shared, nverts = simplify_all(feats, tol)
        rings_json = {k: [[c for p in r for c in p] for r, _, _ in v] for k, v in geom.items()}
        gbytes = len(json.dumps(rings_json, separators=(',', ':')))
        if gbytes <= GEO_BUDGET:
            break
    area_diff = max(abs(sum(a2 for _, _, a2 in v) - sum(a1 for _, a1, _ in v)) / sum(a1 for _, a1, _ in v)
                    for v in geom.values())
    npts = sum(len(r) for v in geom.values() for r, _, _ in v)

    places, pidx = [], {}
    districts = []
    for name, g in L.groupby('neighbourhood_cleansed'):
        gp = g[g['has_price']]
        gs = sp[sp['neighbourhood_cleansed'] == name]
        b = {}
        for k in ('1', '2'):
            s = gs.loc[gs['bedrooms'] == k, 'price_v']
            b[k] = (len(s), med(s, MIN_BED_N))
        rings = geom[name]
        big = max(rings, key=lambda t: t[2])[0]
        A = cx = cy = 0.0
        for (x1, y1), (x2, y2) in zip(big, big[1:] + big[:1]):
            f = x1 * y2 - x2 * y1
            A += f; cx += (x1 + x2) * f; cy += (y1 + y2) * f
        label = [round(cx / (3 * A), 4), round(cy / (3 * A), 4)] if A else list(big[0])
        cells = []
        for (ci, cj), c in g.groupby(['ci', 'cj']):
            fill = c.loc[c['place'] != '', 'place']
            top = Counter(fill).most_common(1)
            pl, pn = (top[0] if top else (None, 0))
            if pn < MIN_PLACE:
                pl = None
            if pl is not None and pl not in pidx:
                pidx[pl] = len(places); places.append(pl)
            cells.append([int(ci), int(cj), len(c), int(c['ent'].sum()), int(c['priv'].sum()), int(c['has_price'].sum()),
                          med(c['pv'], MIN_CELL_PRICED), pidx[pl] if pl is not None else None,
                          int(pn) if pl is not None else 0, int(len(fill))])
        districts.append({
            'name': name, 'n': len(g), 'entire': int(g['ent'].sum()), 'private': int(g['priv'].sum()),
            'priced': len(gp), 'median_all': med(gp['price_v'], MIN_CELL_PRICED), 'scope_priced': len(gs),
            'b1_n': b['1'][0], 'b1_median': b['1'][1], 'b2_n': b['2'][0], 'b2_median': b['2'][1],
            'label': label, 'rings': rings_json[name], 'cells': cells})
    districts.sort(key=lambda d: -d['n'])

    # 每度緯度、經度的公尺數(WGS84 近似式),在南緯 33.87 度
    lat_m =CELL_LAT * (111132.954 - 559.822 * math.cos(2 * math.radians(33.87)))
    lon_m = CELL_LON * (111412.84 * math.cos(math.radians(33.87)))
    ncell = sum(len(d['cells']) for d in districts)
    nplace = sum(1 for d in districts for c in d['cells'] if c[7] is not None)
    out = {
        'about': {
            'period': '2026-09-16',
            'source': 'Inside Airbnb 雪梨 2026-09-16 期 listings.csv.gz 與 neighbourhoods.geojson',
            'cell': f'小方格 = 緯度 {CELL_LAT} 度 × 經度 {CELL_LON} 度;在雪梨(南緯 33.87 度)約 {lat_m:.0f} 公尺(南北)× {lon_m:.0f} 公尺(東西)。'
                    f'格子編號 i = floor(緯度 / {CELL_LAT})、j = floor(經度 / {CELL_LON});格子西南角 = (i×{CELL_LAT}, j×{CELL_LON})。'
                    '格子是我們自己切的,不是官方街區邊界;一格跨兩區時照房源的 neighbourhood_cleansed 分開記。',
            'cell_fields': ['i', 'j', 'n', 'entire', 'private', 'priced', 'median_priced', 'place_index', 'place_top_n', 'place_filled_n'],
            'cell_rules': f'median_priced:有價不到 {MIN_CELL_PRICED} 間為 null;place:房東填的 neighbourhood 欄第一個逗號前的字,同一格至少 {MIN_PLACE} 間填同一個才給,否則 null;place_filled_n = 這一格有幾間填了地名。',
            'district_rules': f'median_all = 區內全體有價的開價中間價;b1/b2 = 篩選且有價(整套、1-2 房、2-4 人、最低 1-7 晚)的 1 房/2 房,不到 {MIN_BED_N} 間中間價為 null。',
            'price_note': '開價是房東開的價(每晚、澳幣),不是實際訂到的價。',
            'geometry': f'rings = [經度, 緯度, 經度, 緯度, ...] 扁平陣列,小數 4 位;相鄰區共用的邊只簡化一次(Douglas-Peucker,容許誤差 {tol} 度,約 {tol * 111000:.0f} 公尺);原始 {nverts:,} 個點 → {npts:,} 個點;各區面積最大變化 {area_diff:.2%}。',
            'meters': {'cell_ns_m': round(lat_m), 'cell_ew_m': round(lon_m)},
            'place_filled_rows': int((L['place'] != '').sum()),
            'place_note': (f'neighbourhood 欄(房東自己填的地名)這一期有填的 {int((L["place"] != "").sum()):,} / {len(L):,} 列;'
                           '整欄空的時候,所有方格的 place_index 都是 null(2026-09-16 期實測整欄空)。'),
        },
        'totals': {'n': len(L), 'priced': int(L['has_price'].sum()), 'scope': int(L['scope'].sum()),
                   'scope_priced': len(sp), 'median_all': med(L['pv'], 1), 'cells': ncell, 'cells_with_place': nplace},
        'places': places,
        'districts': districts,
    }
    txt = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    OUT.write_text(txt, encoding='utf-8', newline='\n')

    # ---------------- 對賬 ----------------
    ok = True

    def chk(label, got, exp):
        nonlocal ok
        same = got == exp
        ok &= same
        print(f"  {'相符' if same else '不符'}  {label}:算出 {got},應為 {exp}")

    D = {d['name']: d for d in districts}
    print('對賬:')
    chk('區數', len(districts), EXPECT['districts'])
    chk('全體', len(L), EXPECT['rows'])
    chk('全體有價', int(L['has_price'].sum()), EXPECT['priced'])
    chk('篩選', int(L['scope'].sum()), EXPECT['scope'])
    chk('篩選且有價', len(sp), EXPECT['scope_priced'])
    chk('全體有價開價中間價(四捨五入到元)', round(L['pv'].median()), EXPECT['all_priced_median'])
    for key in ('Sydney_1', 'Sydney_2', 'Waverley_1', 'Manly_1'):
        nm, bd = key.split('_')
        d = D[nm]
        got = (d[f'b{bd}_n'], round(d[f'b{bd}_median']) if d[f'b{bd}_median'] is not None else None)
        chk(f'{nm} {bd} 房(篩選且有價)間數、中間價(到元;原值 {d[f"b{bd}_median"]})', got, EXPECT[key])
    chk('各區全部間數加總 = 全體', sum(d['n'] for d in districts), len(L))
    chk('各區有價加總 = 全體有價', sum(d['priced'] for d in districts), int(L['has_price'].sum()))
    chk('各區篩選且有價加總', sum(d['scope_priced'] for d in districts), len(sp))
    bad = [d['name'] for d in districts
           if [sum(c[k] for c in d['cells']) for k in (2, 3, 4, 5)] != [d['n'], d['entire'], d['private'], d['priced']]]
    chk('每一區:方格的全部/整套/獨立/有價加總 = 區的數字(對不上的區)', bad, [])
    print(f'方格:{ncell:,} 個(區 × 格);有地名的 {nplace:,} 個,占 {nplace / ncell:.1%}'
          f'(房東填地名的列:{int((L["place"] != "").sum()):,} / {len(L):,})')
    print(f'方格大小:約 {lat_m:.0f} 公尺(南北)× {lon_m:.0f} 公尺(東西)')
    print(f'邊界:容許誤差 {tol} 度;共用點 {shared:,} / {nverts:,};簡化後 {npts:,} 點;座標 {gbytes / 1024:.1f} KB;各區面積最大變化 {area_diff:.2%}')
    print(f'map_data.json:{OUT.stat().st_size / 1024:.1f} KB(上限 300 KB)')
    top = districts[0]
    print(f'最多的區:{top["name"]} {top["n"]:,} 間,占 {top["n"] / len(L):.1%};第二 {districts[1]["name"]} {districts[1]["n"]:,}')
    if not ok or OUT.stat().st_size > 300 * 1024:
        sys.exit('對賬或大小不符,停下來回報')
    print('全部相符')


if __name__ == '__main__':
    main()
