"""方案 A/B 欄位盤點:雪梨、墨爾本 Inside Airbnb 2026-09-16 批次 listings。
只讀本機快取,不下載。calendar 表頭取自 airbnb_two_city_profile_2026-11-07.json(該程式當時只讀表頭記下的)。
"""
import csv
import gzip
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / 'scratchpad/airbnb_2024_two_cities'
PREV_SYD = ROOT / 'scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz'
PROFILE = ROOT / 'Innovation Studio/notes/raw/airbnb_two_city_profile_2026-11-07.json'
OUT = ROOT / 'Innovation Studio/notes/raw/airbnb_ab_field_inventory_2026-11-11.json'
EXPECT = {'sydney': (20833, 6639), 'melbourne': (25715, 8223)}  # (全體列數, 篩選樣本有價列數)

COMMON = ['id', 'price', 'room_type', 'property_type', 'accommodates', 'bedrooms', 'beds', 'bathrooms',
          'bathrooms_text', 'neighbourhood_cleansed', 'latitude', 'longitude', 'minimum_nights',
          'maximum_nights', 'last_scraped']
PLAN_A = ['amenities', 'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
          'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
          'review_scores_value', 'number_of_reviews', 'number_of_reviews_ltm', 'reviews_per_month',
          'first_review', 'last_review', 'host_since', 'host_is_superhost', 'host_response_rate',
          'host_acceptance_rate', 'host_listings_count', 'calculated_host_listings_count',
          'instant_bookable', 'license', 'description', 'name']
PLAN_B = ['availability_30', 'availability_60', 'availability_90', 'availability_365',
          'estimated_occupancy_l365d', 'estimated_revenue_l365d', 'number_of_reviews_ltm',
          'number_of_reviews_l30d', 'reviews_per_month', 'has_availability', 'calendar_last_scraped']
STATS_FIELDS = ['estimated_occupancy_l365d', 'estimated_revenue_l365d', 'availability_365',
                'number_of_reviews_ltm', 'price']
KEYWORDS = {'清潔費': ['cleaning'], '服務費': ['fee'], '押金': ['deposit'],
            '週月折扣': ['weekly', 'monthly'], '房屋買價或租金': ['purchase', 'mortgage', 'rent', 'buy', 'value_of']}


def missing(v):
    return v is None or v.strip() == '' or v.strip().upper() == 'N/A'


def num(v):
    v = re.sub(r'[,$\s]', '', v or '')
    try:
        return float(v)
    except ValueError:
        return None


def is_scope(r):
    return (r['room_type'] == 'Entire home/apt' and r['bedrooms'] in ('1', '2')
            and r['accommodates'].isdigit() and 2 <= int(r['accommodates']) <= 4
            and r['minimum_nights'].isdigit() and 1 <= int(r['minimum_nights']) <= 7)


def fill(rows, col):
    n = len(rows)
    ne = sum(not missing(r[col]) for r in rows)
    return {'nonempty': ne, 'missing': n - ne, 'missing_pct': round(100 * (n - ne) / n, 2) if n else None}


def stats(rows, col):
    vals = [x for x in (num(r[col]) for r in rows) if x is not None]
    if not vals:
        return {'n_numeric': 0}
    return {'n_numeric': len(vals), 'min': min(vals), 'median': statistics.median(vals), 'max': max(vals)}


def listings_path(city):
    if city == 'sydney' and PREV_SYD.exists():
        return PREV_SYD
    return CACHE / f'{city}_listings.csv.gz'


def main():
    prev = json.loads(PROFILE.read_text(encoding='utf-8'))['cities']
    wanted = [('common', COMMON), ('plan_a', PLAN_A), ('plan_b', PLAN_B)]
    result = {}
    for city, (exp_rows, exp_price) in EXPECT.items():
        path = listings_path(city)
        assert path.exists(), f'找不到原始 listings: {path}'
        with gzip.open(path, 'rt', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fields = list(reader.fieldnames)
        assert len(rows) == exp_rows, (city, 'rows', len(rows), exp_rows)
        scope = [r for r in rows if is_scope(r)]
        scope_price = [r for r in scope if r['price']]
        assert len(scope_price) == exp_price, (city, 'scope price rows', len(scope_price), exp_price)
        assert len(scope) == prev[city]['scope_rows'], (city, 'scope rows', len(scope))

        with (CACHE / f'{city}_reviews_summary.csv').open(encoding='utf-8-sig', newline='') as f:
            reviews_header = next(csv.reader(f))

        groups = {}
        absent = []
        for g, cols in wanted:
            groups[g] = {}
            for c in cols:
                if c not in fields:
                    groups[g][c] = {'exists': False}
                    absent.append(c)
                else:
                    groups[g][c] = {'exists': True, 'all': fill(rows, c), 'scope': fill(scope, c),
                                    'scope_with_price': fill(scope_price, c)}
        kw = {k: [c for c in fields if any(w in c.lower() for w in ws)] for k, ws in KEYWORDS.items()}
        st = {c: ({'exists': True, **stats(scope, c)} if c in fields else {'exists': False}) for c in STATS_FIELDS}
        result[city] = {
            'listings_file': str(path.relative_to(ROOT)),
            'rows_all': len(rows), 'rows_scope': len(scope), 'rows_scope_with_price': len(scope_price),
            'missing_def': "空字串或 'N/A' 視為缺值;scope=整套/1-2房/2-4人/最低1-7晚;scope_with_price=scope 且 price 非空",
            'recon_vs_profile_2026-11-07': {'rows': prev[city]['rows'], 'scope_rows': prev[city]['scope_rows'],
                                            'scope_price_nonempty': prev[city]['scope_price_nonempty'],
                                            'all_match': True},
            'fields': groups,
            'absent_fields': sorted(set(absent)),
            'keyword_scan': {k: (v if v else '沒有') for k, v in kw.items()},
            'scope_stats_price_parsed': st,
            'listings_columns': fields,
            'calendar_columns': prev[city]['calendar_fields'],
            'calendar_columns_source': 'airbnb_two_city_profile_2026-11-07.json(未重新連網;本機無 calendar 檔)',
            'reviews_columns': reviews_header,
            'reviews_columns_source': f'{city}_reviews_summary.csv 表頭(visualisations/reviews.csv,非完整 reviews.csv.gz)',
        }
        print(city, 'rows', len(rows), 'scope', len(scope), 'scope_price', len(scope_price), 'cols', len(fields), flush=True)
        # 缺值最嚴重(存在欄位,依全體缺值%)
        flat = [(g, c, v) for g, d in groups.items() for c, v in d.items() if v['exists']]
        flat.sort(key=lambda t: -t[2]['all']['missing_pct'])
        for g, c, v in flat[:8]:
            print(f"  {c}: all {v['all']['missing_pct']}% / scope {v['scope']['missing_pct']}%")
        print('  absent:', sorted(set(absent)))
        print('  keyword:', {k: v for k, v in result[city]['keyword_scan'].items()})
    OUT.write_text(json.dumps({'batch': '2026-09-16', 'scope_id': 'IS-1111-INV', 'cities': result},
                              ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('wrote', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
