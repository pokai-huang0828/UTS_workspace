"""方案 A/B 資料品質檢查(IS-1111-BR-DATA):欄位有填,但能不能用。
雪梨、墨爾本 Inside Airbnb 2026-09-16 批次 listings。只讀本機快取,不下載。
篩選樣本定義沿用 airbnb_ab_field_inventory.py:整套、1-2 房、2-4 人、最低 1-7 晚。
輸出不含房東姓名、房源名稱、描述、評論文字(根本沒讀那些欄位)。
"""
import csv
import gzip
import json
import re
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / 'scratchpad/airbnb_2024_two_cities'
PREV_SYD = ROOT / 'scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz'
OUT = ROOT / 'Innovation Studio/notes/raw/airbnb_ab_quality_checks_2026-11-11.json'
# (全體列數, 篩選樣本列數, 篩選樣本有價列數)
EXPECT = {'sydney': (20833, 7565, 6639), 'melbourne': (25715, 10940, 8223)}


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


def pct(a, b):
    return round(100 * a / b, 2) if b else None


def quant(vals, q):
    s = sorted(vals)
    if not s:
        return None
    k = (len(s) - 1) * q / 100
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 4)


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    rk = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rk[order[k]] = avg
        i = j + 1
    return rk


def pearson(x, y):
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sxx * syy) ** 0.5


def spearman(x, y):
    r = pearson(ranks(x), ranks(y))
    return None if r is None else round(r, 4)


def col_nums(rows, c):
    return [v for v in (num(r.get(c)) for r in rows) if v is not None]


def check_price(rows):
    p = [v for v in col_nums(rows, 'price')]
    out = {'n_rows': len(rows), 'n_price': len(p), 'price_missing': len(rows) - len(p),
           'price_missing_pct': pct(len(rows) - len(p), len(rows)), 'n_price_le_0': sum(v <= 0 for v in p)}
    nop = [r for r in rows if num(r.get('price')) is None]
    out['price_missing_and_availability_365_eq_0'] = sum(num(r.get('availability_365')) == 0 for r in nop)
    out['price_missing_and_reviews_ltm_eq_0'] = sum(num(r.get('number_of_reviews_ltm')) == 0 for r in nop)
    out['price_missing_and_has_availability_not_t'] = sum(r.get('has_availability') != 't' for r in nop)
    for q in (1, 5, 25, 50, 75, 95, 99):
        out[f'p{q}'] = quant(p, q)
    if p:
        p99 = quant(p, 99)
        out['min'], out['max'] = min(p), max(p)
        out['n_above_p99'] = sum(v > p99 for v in p)
        out['n_ge_1000'] = sum(v >= 1000 for v in p)
        out['n_ge_5000'] = sum(v >= 5000 for v in p)
        out['max_over_median'] = round(max(p) / quant(p, 50), 1)
    return out


def check_revenue(rows):
    trip = []  # (price, occ, rev)
    n_rev = n_occ = 0
    for r in rows:
        pr, oc, rv = num(r.get('price')), num(r.get('estimated_occupancy_l365d')), num(r.get('estimated_revenue_l365d'))
        n_rev += rv is not None
        n_occ += oc is not None
        if pr is not None and oc is not None and rv is not None:
            trip.append((pr, oc, rv))
    pos = [(p, o, v) for p, o, v in trip if p > 0 and o > 0]
    ratios = [v / (p * o) for p, o, v in pos]
    zero = [(p, o, v) for p, o, v in trip if o == 0]
    within = sum(0.99 <= x <= 1.01 for x in ratios)
    out = {'n_rows': len(rows), 'n_revenue_numeric': n_rev, 'n_occupancy_numeric': n_occ,
           'n_price_occ_rev_all_present': len(trip), 'n_with_occ_gt0_price_gt0': len(pos),
           'n_ratio_within_0.99_1.01': within, 'ratio_within_0.99_1.01_pct': pct(within, len(pos)),
           'ratio_p1': quant(ratios, 1), 'ratio_p5': quant(ratios, 5), 'ratio_p50': quant(ratios, 50),
           'ratio_p95': quant(ratios, 95), 'ratio_p99': quant(ratios, 99),
           'n_occ_eq_0': len(zero), 'n_occ_eq_0_and_revenue_eq_0': sum(v == 0 for _, _, v in zero),
           'n_revenue_gt0_with_occ_eq_0': sum(v > 0 for _, _, v in zero)}
    return out


def check_occupancy(rows):
    oc = col_nums(rows, 'estimated_occupancy_l365d')
    out = {'n_rows': len(rows), 'n_numeric': len(oc), 'missing_pct': pct(len(rows) - len(oc), len(rows))}
    if oc:
        mx = max(oc)
        out.update({'max': mx, 'n_eq_0': sum(v == 0 for v in oc), 'eq_0_pct': pct(sum(v == 0 for v in oc), len(oc)),
                    'n_at_max': sum(v == mx for v in oc), 'at_max_pct': pct(sum(v == mx for v in oc), len(oc)),
                    'p50': quant(oc, 50), 'p95': quant(oc, 95)})
    pairs = [(num(r.get('estimated_occupancy_l365d')), num(r.get('number_of_reviews_ltm'))) for r in rows]
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    out['n_pairs_with_reviews_ltm'] = len(pairs)
    out['spearman_vs_reviews_ltm'] = spearman([a for a, _ in pairs], [b for _, b in pairs])
    pos = [a / b for a, b in pairs if b > 0 and a is not None]
    out['occ_per_review_ltm_p5'] = quant(pos, 5)
    out['occ_per_review_ltm_p50'] = quant(pos, 50)
    out['occ_per_review_ltm_p95'] = quant(pos, 95)
    out['n_reviews_ltm_eq_0_and_occ_gt0'] = sum(b == 0 and a > 0 for a, b in pairs)
    out['n_reviews_ltm_gt0_and_occ_eq_0'] = sum(b > 0 and a == 0 for a, b in pairs)
    return out


def check_activity(rows):
    n = len(rows)
    ltm = col_nums(rows, 'number_of_reviews_ltm')
    lr = [r['last_review'] for r in rows if not missing(r.get('last_review'))]
    old = sum(x < '2024-01-01' for x in lr)
    noreview = sum(missing(r.get('first_review')) and missing(r.get('last_review')) for r in rows)
    nrev0 = [x for x in col_nums(rows, 'number_of_reviews')]
    return {'n_rows': n, 'reviews_ltm_numeric': len(ltm), 'reviews_ltm_eq_0': sum(v == 0 for v in ltm),
            'reviews_ltm_eq_0_pct': pct(sum(v == 0 for v in ltm), len(ltm)),
            'last_review_present': len(lr), 'last_review_missing': n - len(lr),
            'last_review_before_2024_01_01': old, 'last_review_before_2024_pct_of_present': pct(old, len(lr)),
            'last_review_before_2024_pct_of_rows': pct(old, n),
            'no_review_first_and_last_missing': noreview, 'no_review_pct': pct(noreview, n),
            'number_of_reviews_eq_0': sum(v == 0 for v in nrev0),
            'number_of_reviews_eq_0_pct': pct(sum(v == 0 for v in nrev0), len(nrev0)),
            'last_review_min': min(lr) if lr else None, 'last_review_max': max(lr) if lr else None}


def check_first_review(rows, cutoff):
    n = len(rows)
    yrs = Counter()
    for r in rows:
        fr = r.get('first_review')
        yrs['none' if missing(fr) else fr[:4]] += 1
    g = lambda y: yrs.get(str(y), 0)
    before_2023 = sum(c for y, c in yrs.items() if y != 'none' and int(y) <= 2022)
    recent12 = sum(1 for r in rows if not missing(r.get('first_review')) and r['first_review'] >= cutoff)
    return {'n_rows': n, 'bins': {'2022_and_before': before_2023, '2023': g(2023), '2024': g(2024),
                                  '2025': g(2025), '2026': g(2026), 'no_review': yrs.get('none', 0)},
            'all_years': dict(sorted((k, v) for k, v in yrs.items())),
            'first_review_within_12m_before_batch': recent12, 'cutoff_date': cutoff,
            'within_12m_pct_of_rows': pct(recent12, n)}


def check_neigh(rows):
    def summarize(rs):
        c = Counter(r['neighbourhood_cleansed'] for r in rs if not missing(r.get('neighbourhood_cleansed')))
        v = sorted(c.values())
        return {'n_neighbourhoods': len(c), 'n_rows': len(rs), 'min': v[0] if v else None,
                'median': statistics.median(v) if v else None, 'max': v[-1] if v else None,
                'n_ge_30': sum(x >= 30 for x in v), 'n_lt_30': sum(x < 30 for x in v),
                'rows_in_ge_30': sum(x for x in v if x >= 30), 'rows_in_lt_30': sum(x for x in v if x < 30)}
    priced = [r for r in rows if num(r.get('price')) is not None]
    active = [r for r in priced if (num(r.get('number_of_reviews_ltm')) or 0) > 0]
    return {'sample_all_rows': summarize(rows), 'sample_priced': summarize(priced),
            'sample_priced_and_reviews_ltm_gt0': summarize(active)}


def check_amenities(rows):
    ok, counts, c = 0, [], Counter()
    nonmiss = [r for r in rows if not missing(r.get('amenities'))]
    for r in nonmiss:
        try:
            a = json.loads(r['amenities'])
        except (ValueError, TypeError):
            continue
        if isinstance(a, list):
            ok += 1
            counts.append(len(a))
            c.update(set(str(x).strip() for x in a))
    return {'n_rows': len(rows), 'n_nonmissing': len(nonmiss), 'parse_ok': ok,
            'parse_ok_pct_of_nonmissing': pct(ok, len(nonmiss)), 'parse_ok_pct_of_rows': pct(ok, len(rows)),
            'n_amenities_median': statistics.median(counts) if counts else None,
            'n_amenities_p5': quant(counts, 5), 'n_amenities_p95': quant(counts, 95),
            'n_empty_list': sum(x == 0 for x in counts),
            'distinct_amenity_names': len(c),
            'top10': [{'name': k, 'share_pct': pct(v, ok)} for k, v in c.most_common(10)]}


def check_host(rows):
    n = len(rows)
    sh = Counter('missing' if missing(r.get('host_is_superhost')) else r['host_is_superhost'] for r in rows)
    out = {'n_rows': n, 'superhost_values': dict(sh), 'superhost_missing_pct': pct(sh.get('missing', 0), n),
           'superhost_t_pct_of_nonmissing': pct(sh.get('t', 0), n - sh.get('missing', 0))}
    for c in ('host_listings_count', 'calculated_host_listings_count', 'host_since'):
        v = col_nums(rows, c) if c != 'host_since' else [r for r in rows if not missing(r.get(c))]
        out[f'{c}_missing_pct'] = pct(n - len(v), n)
    cal = col_nums(rows, 'calculated_host_listings_count')
    out['calculated_host_listings_ge2'] = sum(v >= 2 for v in cal)
    out['calculated_host_listings_ge2_pct'] = pct(sum(v >= 2 for v in cal), len(cal))
    out['calculated_host_listings_ge5_pct'] = pct(sum(v >= 5 for v in cal), len(cal))
    hl = col_nums(rows, 'host_listings_count')
    out['host_listings_count_ge2_pct'] = pct(sum(v >= 2 for v in hl), len(hl))
    return out


def check_avail(rows):
    a = col_nums(rows, 'availability_365')
    ha = Counter('missing' if missing(r.get('has_availability')) else r['has_availability'] for r in rows)
    return {'n_rows': len(rows), 'availability_365_numeric': len(a),
            'eq_0': sum(v == 0 for v in a), 'eq_0_pct': pct(sum(v == 0 for v in a), len(a)),
            'eq_365': sum(v == 365 for v in a), 'eq_365_pct': pct(sum(v == 365 for v in a), len(a)),
            'has_availability_values': dict(ha)}


def check_bath(rows):
    n = len(rows)
    nm = [r['bathrooms_text'] for r in rows if not missing(r.get('bathrooms_text'))]
    dig = sum(bool(re.search(r'\d', t)) for t in nm)
    half = sum((not re.search(r'\d', t)) and 'half' in t.lower() for t in nm)
    b = col_nums(rows, 'bathrooms')
    return {'n_rows': n, 'bathrooms_text_missing': n - len(nm), 'bathrooms_text_missing_pct': pct(n - len(nm), n),
            'parse_digit_ok': dig, 'parse_digit_ok_pct_of_rows': pct(dig, n),
            'parse_digit_ok_pct_of_nonmissing': pct(dig, len(nm)),
            'half_bath_no_digit': half, 'parse_ok_incl_half_pct_of_rows': pct(dig + half, n),
            'bathrooms_numeric_missing_pct': pct(n - len(b), n)}


def run_checks(rows, cutoff):
    return {'a_price': check_price(rows), 'b_revenue_vs_price_x_occ': check_revenue(rows),
            'c_occupancy': check_occupancy(rows), 'd_activity': check_activity(rows),
            'e_first_review_years': check_first_review(rows, cutoff), 'f_neighbourhoods': check_neigh(rows),
            'g_amenities': check_amenities(rows), 'h_host': check_host(rows),
            'i_availability': check_avail(rows), 'j_bathrooms_text': check_bath(rows)}


def listings_path(city):
    if city == 'sydney' and PREV_SYD.exists():
        return PREV_SYD
    return CACHE / f'{city}_listings.csv.gz'


def main():
    result = {}
    for city, (exp_all, exp_scope, exp_scope_price) in EXPECT.items():
        path = listings_path(city)
        assert path.exists(), f'找不到原始 listings: {path}'
        with gzip.open(path, 'rt', encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == exp_all, (city, 'rows', len(rows), exp_all)
        scope = [r for r in rows if is_scope(r)]
        assert len(scope) == exp_scope, (city, 'scope rows', len(scope), exp_scope)
        scope_price = [r for r in scope if r['price']]
        assert len(scope_price) == exp_scope_price, (city, 'scope price rows', len(scope_price), exp_scope_price)
        scraped = sorted({r['last_scraped'] for r in rows if r.get('last_scraped')})
        cutoff = f"{int(scraped[-1][:4]) - 1}{scraped[-1][4:]}"  # 批次日期往前推 12 個月
        result[city] = {
            'listings_file': str(path.relative_to(ROOT)),
            'rows_all': len(rows), 'rows_scope': len(scope), 'rows_scope_with_price': len(scope_price),
            'last_scraped_min_max': [scraped[0], scraped[-1]],
            'sample_defs': {'all': '全體 listings', 'scope': '整套/1-2房/2-4人/最低1-7晚',
                            'scope_price': 'scope 且 price 非空(競品分析/報酬測算實際可用)'},
            'all': run_checks(rows, cutoff), 'scope': run_checks(scope, cutoff),
            'scope_price': run_checks(scope_price, cutoff),
        }
        print(city, 'ok', len(rows), len(scope), len(scope_price), flush=True)
    OUT.write_text(json.dumps({'batch': '2026-09-16', 'scope_id': 'IS-1111-BR-DATA', 'cities': result},
                              ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('wrote', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
