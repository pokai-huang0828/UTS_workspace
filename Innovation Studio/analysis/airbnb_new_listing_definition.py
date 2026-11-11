"""「新上架房源」代理定義與敏感度(IS-1111-BR-AIM)。
原始檔、樣本、基準日全部沿用 airbnb_ab_quality_checks.py:
- 樣本 = 篩選(整套/1-2房/2-4人/最低1-7晚)且 price 非空(有價樣本)
- 基準日 = 該城 listings 的 last_scraped 最大值
- 窗口起點 = 基準日往前推 N 個月的同一天;first_review >= 起點(含起點當天)才算新上架
- 房東年資(月)= hosts_time_as_host_years * 12 + hosts_time_as_host_months(欄義照欄名推斷)
只讀數值與日期欄,不讀房東姓名、房源名稱、描述、評論文字。只讀本機快取,不下載。
"""
import csv, gzip, json, sys  # noqa: E401
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from airbnb_ab_quality_checks import EXPECT, ROOT, is_scope, listings_path, missing, num  # noqa: E402

OUT = ROOT / 'Innovation Studio/notes/raw/airbnb_new_listing_definition_2026-11-11.json'
EXPECT_NEW12 = {'sydney': 2028, 'melbourne': 2056}  # 品質檢查 JSON 的 first_review_within_12m_before_batch
WINDOWS = (6, 12, 18)


def months_back(d, n):
    y, m, day = int(d[:4]), int(d[5:7]), d[8:10]
    assert int(day) <= 28, d  # 避免月底日期不存在
    m -= n
    while m <= 0:
        m += 12
        y -= 1
    return f'{y:04d}-{m:02d}-{day}'


def single(r):  # 房東在這個城市這批資料裡只有這一間
    return num(r.get('calculated_host_listings_count')) == 1


def tenure(r):  # 房東年資(月);缺值回 None
    y, m = num(r.get('hosts_time_as_host_years')), num(r.get('hosts_time_as_host_months'))
    return None if y is None or m is None else y * 12 + m


def mix(rs):
    c = [num(r.get('calculated_host_listings_count')) for r in rs]
    return {'eq_1': sum(v == 1 for v in c), '2_to_4': sum(v is not None and 2 <= v <= 4 for v in c),
            'ge_5': sum(v is not None and v >= 5 for v in c), 'missing': sum(v is None for v in c)}


def le(r, n):  # 房東年資 <= n 個月(缺值不算)
    return tenure(r) is not None and tenure(r) <= n


def main():
    result = {}
    for city, (exp_all, _exp_scope, exp_sp) in EXPECT.items():
        with gzip.open(listings_path(city), 'rt', encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == exp_all, (city, len(rows))
        sp = [r for r in rows if is_scope(r) and r['price']]
        assert len(sp) == exp_sp, (city, len(sp))
        batch = max(r['last_scraped'] for r in rows if r.get('last_scraped'))
        has_fr = [r for r in sp if not missing(r.get('first_review'))]
        no_rev = [r for r in sp if missing(r.get('first_review'))]
        win = {}
        for n in WINDOWS:
            cut = months_back(batch, n)
            new = [r for r in has_fr if r['first_review'] >= cut]
            win[f'{n}m'] = {'cutoff_inclusive': cut, 'n_new': len(new),
                            'n_new_single_host': sum(single(r) for r in new),
                            'n_new_host_tenure_le_window': sum(le(r, n) for r in new),
                            'n_new_single_and_tenure_le_window': sum(single(r) and le(r, n) for r in new),
                            'n_first_review_on_cutoff_day': sum(r['first_review'] == cut for r in new)}
        assert win['12m']['n_new'] == EXPECT_NEW12[city], (city, win['12m']['n_new'])
        new12 = [r for r in has_fr if r['first_review'] >= win['12m']['cutoff_inclusive']]
        result[city] = {
            'listings_file': str(listings_path(city).relative_to(ROOT)), 'batch_date': batch,
            'n_scope_price': len(sp), 'n_with_first_review': len(has_fr), 'n_no_review': len(no_rev),
            'n_scope_price_tenure_nonmissing': sum(tenure(r) is not None for r in sp), 'windows': win,
            'new12': {'n_first_review_after_batch': sum(r['first_review'] > batch for r in new12),
                      'n_availability_365_eq_0': sum(num(r.get('availability_365')) == 0 for r in new12),
                      'n_reviews_ltm_eq_0': sum(num(r.get('number_of_reviews_ltm')) == 0 for r in new12),
                      'host_listings_mix': mix(new12), 'n_distinct_host_id': len({r['host_id'] for r in new12})},
            'no_review': {'n_availability_365_eq_0': sum(num(r.get('availability_365')) == 0 for r in no_rev),
                          'host_listings_mix': mix(no_rev), 'n_host_tenure_le_12': sum(le(r, 12) for r in no_rev),
                          'n_single_and_tenure_le_12': sum(single(r) and le(r, 12) for r in no_rev)},
        }
        print(city, 'ok', len(rows), len(sp), win['12m']['n_new'], flush=True)
    OUT.write_text(json.dumps({'batch': '2026-09-16', 'scope_id': 'IS-1111-BR-AIM', 'cities': result},
                              ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('wrote', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
