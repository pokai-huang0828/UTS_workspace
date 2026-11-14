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
用法(兩步):
  1. python -I "Innovation Studio/meeting_1114/map_data.py" --sal   (只用標準函式庫解析 ABS 街區邊界下載檔)
  2. python "Innovation Studio/meeting_1114/map_data.py"
街區邊界下載檔與來源紀錄:scratchpad/abs_sal_2026-11-14/(SOURCE.txt)
不寫入任何房源編號、名稱、房東名;地名只取房東填的 neighbourhood 欄第一個逗號前的字,且同一格至少 3 間填同一個才給。
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path

try:
    import pandas as pd
except ImportError:  # --sal 模式用 python -I 跑,只用標準函式庫
    pd = None

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / 'scratchpad' / 'insideairbnb_sydney' / '2026-09-16'
OUT = HERE / 'map_data.json'
# 官方街區邊界:ABS ASGS Edition 3(2021)Suburbs and Localities(SAL),CC BY 4.0;下載紀錄見該資料夾 SOURCE.txt
SAL_DIR = ROOT / 'scratchpad' / 'abs_sal_2026-11-14'
SAL_CLEAN = SAL_DIR / 'derived' / 'sal_clean.json'
JSON_BUDGET = 345 * 1024  # map_data.json 整個上限(350 KB 留一點空間)


def prep_sal():
    """第一步(python -I 跑,只用標準函式庫):把下載回來的 SAL GeoJSON 只當資料解析,
    整理成 名字 + 多邊形座標,寫到 derived/sal_clean.json。不執行下載檔裡的任何東西。"""
    feats = []
    for p in sorted(SAL_DIR.glob('sal_2021_page_*.geojson')):
        for f in json.loads(p.read_text(encoding='utf-8'))['features']:
            g, pr = f.get('geometry'), f.get('properties') or {}
            if not g or g.get('type') not in ('Polygon', 'MultiPolygon'):
                continue
            polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            clean = [[[[float(x), float(y)] for x, y, *_ in ring] for ring in poly] for poly in polys]
            feats.append({'code': str(pr.get('sal_code_2021', '')), 'name': str(pr.get('sal_name_2021', '')), 'polys': clean})
    codes = [f['code'] for f in feats]
    assert len(codes) == len(set(codes)), 'SAL 代碼重複(分頁重疊?)'
    SAL_CLEAN.parent.mkdir(exist_ok=True)
    SAL_CLEAN.write_text(json.dumps(feats, ensure_ascii=False), encoding='utf-8')
    print(f'SAL 街區 {len(feats)} 個 → {SAL_CLEAN}')


def load_sal():
    feats = json.loads(SAL_CLEAN.read_text(encoding='utf-8'))
    grid = {}
    for k, f in enumerate(feats):
        xs = [x for poly in f['polys'] for ring in poly for x, _ in ring]
        ys = [y for poly in f['polys'] for ring in poly for _, y in ring]
        f['bb'] = (min(xs), min(ys), max(xs), max(ys))
        for gx in range(math.floor(f['bb'][0] / 0.02), math.floor(f['bb'][2] / 0.02) + 1):
            for gy in range(math.floor(f['bb'][1] / 0.02), math.floor(f['bb'][3] / 0.02) + 1):
                grid.setdefault((gx, gy), []).append(k)
    return feats, grid


def in_poly(x, y, poly):
    """點在多邊形內(射線法,外圈與洞一起算奇偶;洞裡的點算在外面)。"""
    inside = False
    for ring in poly:
        n = len(ring)
        x1, y1 = ring[-1]
        for i in range(n):
            x2, y2 = ring[i]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                inside = not inside
            x1, y1 = x2, y2
    return inside


def locate(x, y, feats, grid):
    for k in grid.get((math.floor(x / 0.02), math.floor(y / 0.02)), []):
        b = feats[k]['bb']
        if b[0] <= x <= b[2] and b[1] <= y <= b[3] and any(in_poly(x, y, poly) for poly in feats[k]['polys']):
            return feats[k]['name']
    return ''

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
    sal_feats, sal_grid = load_sal()
    L['sal'] = [locate(x, y, sal_feats, sal_grid) for x, y in zip(L['lon'], L['lat'])]
    snames, sidx = [], {}

    def si(nm):
        if nm not in sidx:
            sidx[nm] = len(snames); snames.append(nm)
        return sidx[nm]

    geo =json.loads((DATA / 'visualisations' / 'neighbourhoods.geojson').read_text(encoding='utf-8'))
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
            stop = Counter(x for x in c['sal'] if x).most_common(1)
            cells[-1] += [si(stop[0][0]), int(stop[0][1])] if stop else [None, 0]
        subs = []
        for snm, sg in g[g['sal'] != ''].groupby('sal'):
            tc = sg.groupby(['ci', 'cj']).size().idxmax()  # 這個街區在這一區房源最多的那一格(放名字用)
            subs.append([si(snm), len(sg), int(sg['ent'].sum()), int(sg['priv'].sum()), int(sg['has_price'].sum()),
                         med(sg['pv'], MIN_CELL_PRICED), int(tc[0]), int(tc[1])])
        subs.sort(key=lambda r: (-r[1], snames[r[0]]))
        districts.append({
            'suburbs': subs, 'no_suburb_n': int((g['sal'] == '').sum()),
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
            'cell_fields': ['i', 'j', 'n', 'entire', 'private', 'priced', 'median_priced', 'place_index', 'place_top_n', 'place_filled_n',
                            'suburb_index', 'suburb_top_n'],
            'suburb': ('街區 = 澳洲統計局(ABS)ASGS 第三版(2021)Suburbs and Localities(SAL),授權 CC BY 4.0;'
                       '名字照官方原文。ABS 說明 SAL 是用統計小區拼出來的近似邊界,不是法定邊界。'
                       '每間房源用經緯度做點在多邊形內的判斷對到街區;對不到的記在各區 no_suburb_n。'
                       'suburb_index / suburb_top_n = 這一格裡房源最多的街區與它在這一格的間數(這一格總共幾間 = n)。'
                       'districts[].suburbs 每列 = [suburb_index, 全部, 整套, 獨立房間, 有價, 開價中間價(有價不到 5 間為 null), '
                       '放名字的格子 i, j];一個街區跨兩區時各區各算(以 neighbourhood_cleansed 為準)。'
                       'suburb_rings 與 suburb_names 同順序,是簡化後的街區邊界(只畫線用)。'),
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
                   'scope_priced': len(sp), 'median_all': med(L['pv'], 1), 'cells': ncell, 'cells_with_place': nplace,
                   # 全雪梨「可以互相比的房子」(篩選且有價)裡 1 個臥室、2 個臥室的間數與開價中間價(筆記 20 第 103 行)
                   'b1_n': int((sp['bedrooms'] == '1').sum()), 'b1_median': med(sp.loc[sp['bedrooms'] == '1', 'price_v'], 1),
                   'b2_n': int((sp['bedrooms'] == '2').sum()), 'b2_median': med(sp.loc[sp['bedrooms'] == '2', 'price_v'], 1)},
        'places': places,
        'suburb_names': snames,
        'districts': districts,
    }
    # 街區邊界(只存有房源的街區;每個多邊形各自簡化,只畫線)
    by_sal = {f['name']: f for f in sal_feats}
    base = len(json.dumps(out, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    for stol in (0.0001, 0.00015, 0.0002, 0.0003, 0.0004, 0.0005, 0.0007, 0.001, 0.0015):
        srings = []
        for nm in snames:
            rr = []
            for poly in by_sal[nm]['polys']:
                for ring in poly:
                    pts = [tuple(p) for p in ring]
                    if pts[0] == pts[-1]:
                        pts = pts[:-1]
                    if len(pts) < 3:
                        continue
                    far = max(range(len(pts)), key=lambda k: (pts[k][0] - pts[0][0]) ** 2 + (pts[k][1] - pts[0][1]) ** 2)
                    s4 = dp(pts[:far + 1], stol)[:-1] + dp(pts[far:] + pts[:1], stol)[:-1]
                    q4 = []
                    for x, y in s4:
                        q = (round(x * 1e4), round(y * 1e4))
                        if not q4 or q4[-1] != q:
                            q4.append(q)
                    if len(q4) >= 3:  # 存成 1/10000 度的整數:第一點是絕對值,後面每點是跟前一點的差
                        flat = [q4[0][0], q4[0][1]]
                        for (ax, ay), (bx, by) in zip(q4, q4[1:]):
                            flat += [bx - ax, by - ay]
                        rr.append(flat)
            srings.append(rr)
        rbytes = len(json.dumps(srings, separators=(',', ':')))
        if rbytes <= 150 * 1024 and base + rbytes + 20 <= JSON_BUDGET:
            break
    out['suburb_rings'] = srings
    out['about']['suburb_geometry'] = f'suburb_rings:每個環 = [x0, y0, dx1, dy1, ...],單位 1/10000 度(經度、緯度 × 10000 取整數),第一點是絕對值、之後是跟前一點的差;Douglas-Peucker 容許誤差 {stol} 度(約 {stol * 111000:.0f} 公尺),{rbytes / 1024:.1f} KB;只用來畫街區界線,房源對街區用的是下載回來的邊界(下載時已請 ABS 服務簡化到 0.00005 度,約 5 公尺)。'
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
    T = out['totals']
    chk('json 裡的全雪梨開價中間價(到元)', round(T['median_all']), EXPECT['all_priced_median'])
    chk('全雪梨可以互相比的房子 1 個臥室:間數、中間價(到元)', (T['b1_n'], round(T['b1_median'])), (4029, 299))
    chk('全雪梨可以互相比的房子 2 個臥室:間數、中間價(到元)', (T['b2_n'], round(T['b2_median'])), (2610, 414))
    chk('各區全部間數加總 = 全體', sum(d['n'] for d in districts), len(L))
    chk('各區有價加總 = 全體有價', sum(d['priced'] for d in districts), int(L['has_price'].sum()))
    chk('各區篩選且有價加總', sum(d['scope_priced'] for d in districts), len(sp))
    bad = [d['name'] for d in districts
           if [sum(c[k] for c in d['cells']) for k in (2, 3, 4, 5)] != [d['n'], d['entire'], d['private'], d['priced']]]
    chk('每一區:方格的全部/整套/獨立/有價加總 = 區的數字(對不上的區)', bad, [])
    bad2 = [d['name'] for d in districts if sum(r[1] for r in d['suburbs']) + d['no_suburb_n'] != d['n']]
    chk('每一區:街區清單加總 + 對不到街區 = 區的全部間數(對不上的區)', bad2, [])
    nomatch = sum(d['no_suburb_n'] for d in districts)
    chk('全體:街區加總 + 對不到街區', sum(r[1] for d in districts for r in d['suburbs']) + nomatch, EXPECT['rows'])
    bad3 = [d['name'] for d in districts
            if sum(c[11] for c in d['cells']) != int(L.loc[L['neighbourhood_cleansed'] == d['name']].groupby(['ci', 'cj'])['sal'].agg(
                lambda s: s[s != ''].value_counts().max() if (s != '').any() else 0).sum())]
    chk('每一格的「最多街區間數」重算一致(對不上的區)', bad3, [])
    print(f'街區:房源對到 {len(snames)} 個街區(下載 {len(sal_feats)} 個);對不到任何街區 {nomatch} 間({nomatch / len(L):.2%})')
    for nm in ('Sydney', 'Waverley'):
        print(f'  {nm} 前五大街區:' + '、'.join(f'{snames[r[0]]} {r[1]:,}' for r in D[nm]['suburbs'][:5]) + f';對不到 {D[nm]["no_suburb_n"]} 間')
    print(f'方格:{ncell:,} 個(區 × 格);有地名的 {nplace:,} 個,占 {nplace / ncell:.1%}'
          f'(房東填地名的列:{int((L["place"] != "").sum()):,} / {len(L):,})')
    print(f'方格大小:約 {lat_m:.0f} 公尺(南北)× {lon_m:.0f} 公尺(東西)')
    print(f'邊界:容許誤差 {tol} 度;共用點 {shared:,} / {nverts:,};簡化後 {npts:,} 點;座標 {gbytes / 1024:.1f} KB;各區面積最大變化 {area_diff:.2%}')
    print(f'map_data.json:{OUT.stat().st_size / 1024:.1f} KB(上限 350 KB)')
    top = districts[0]
    print(f'最多的區:{top["name"]} {top["n"]:,} 間,占 {top["n"] / len(L):.1%};第二 {districts[1]["name"]} {districts[1]["n"]:,}')
    if not ok or OUT.stat().st_size > 350 * 1024:
        sys.exit('對賬或大小不符,停下來回報')
    print('全部相符')


if __name__ == '__main__':
    if '--sal' in sys.argv:
        prep_sal()  # 第一步:python -I map_data.py --sal(只解析下載回來的街區邊界)
    else:
        main()      # 第二步:python map_data.py
