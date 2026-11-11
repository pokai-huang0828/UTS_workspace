"""「新手房東」定義 v1.1:年資欄(當房東多久)不超過 12 個月(IS-1112-FIX-NEWHOST)。
兩城都用 2026-09-16 那期;原始檔、篩選樣本、有價定義沿用 airbnb_ab_quality_checks.py / airbnb_ab_field_inventory.py:
- 篩選 = 整套 / 1-2 房 / 2-4 人 / 最低 1-7 晚;有價 = 篩選且 price 非空
- 年資(月)= hosts_time_as_host_years * 12 + hosts_time_as_host_months(兩欄任一缺值 = 缺)
- 「不超過 12 個月」的邊界照 analysis/melbourne/mel_c_hosts_time.py:
  房東開始月 = 該列 last_scraped 的月份序號(年*12+月) - 年資(月);
  開始月 >= 基準月序號 - 12 才算新手(基準月 = 該城 last_scraped 最大值的月份,兩城都是 2026-09);24 個月版同理
- 舊代理「首評 12 個月內」= first_review >= 基準日往前 12 個月的同一天(含當天),照 airbnb_new_listing_definition.py
欄義:墨爾本靠 2025-12 那期 host_since 排除法推論(見 notes/19 §5),官方欄位說明還沒查;
雪梨沒有 2025-12 那期可驗證,欄義沿用墨爾本的推論,未另外驗證。
只讀數值與日期欄,不讀姓名、房源名稱、描述、評論文字。只讀本機快取,不下載。
"""
import csv, gzip, json, sys  # noqa: E401
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from airbnb_ab_quality_checks import ROOT, is_scope, listings_path, missing, num  # noqa: E402
from airbnb_new_listing_definition import months_back, single, tenure  # noqa: E402

OUT = ROOT / 'Innovation Studio/notes/raw/airbnb_new_host_definition_2026-11-12.json'
# (全體, 篩選, 篩選且有價, 舊代理首評 12 個月內)
EXPECT = {'sydney': (20833, 7565, 6639, 2028), 'melbourne': (25715, 10940, 8223, 2056)}
# 墨爾本必須重現 mel_c_hosts_time_2026-11-11.json 的 c_new_host_definition(T 口徑)
EXPECT_MEL = {'all_le12': 3045, 'scope_le12': 1216, 'scope_price_le12': 1122, 'scope_price_le24': 2013,
              'scope_price_le12_single': 667, 'both': 857}


def midx(d):  # 'YYYY-MM-DD' -> 年*12+月
    return int(d[:4]) * 12 + int(d[5:7])


def is_new(r, bidx, n):  # 照 mel_c:start_T = ls_idx - t_host >= BIDX - n
    t = tenure(r)
    if t is None or missing(r.get('last_scraped')):
        return False
    return midx(r['last_scraped']) - t >= bidx - n


def main():
    result = {}
    for city, (exp_all, exp_scope, exp_sp, exp_proxy) in EXPECT.items():
        with gzip.open(listings_path(city), 'rt', encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        scope = [r for r in rows if is_scope(r)]
        sp = [r for r in scope if r['price']]
        batch = max(r['last_scraped'] for r in rows if r.get('last_scraped'))
        bidx, cut = midx(batch), months_back(batch, 12)
        proxy = [r for r in sp if not missing(r.get('first_review')) and r['first_review'] >= cut]
        assert (len(rows), len(scope), len(sp), len(proxy)) == (exp_all, exp_scope, exp_sp, exp_proxy), \
            (city, len(rows), len(scope), len(sp), len(proxy))
        groups = {'all': rows, 'scope': scope, 'scope_price': sp}
        cnt = lambda f: {k: sum(f(r) for r in v) for k, v in groups.items()}  # noqa: E731
        ct = {k: {'真新手': 0, '非新手': 0} for k in ('首評12個月內', '首評12個月前', '無評論')}
        for r in sp:
            fr = r.get('first_review')
            k = '無評論' if missing(fr) else ('首評12個月內' if fr >= cut else '首評12個月前')
            ct[k]['真新手' if is_new(r, bidx, 12) else '非新手'] += 1
        both = ct['首評12個月內']['真新手']
        real_yes = sum(v['真新手'] for v in ct.values())
        c = {
            'listings_file': str(listings_path(city).relative_to(ROOT)), 'batch_date': batch,
            'batch_month': batch[:7], 'first_review_cutoff_inclusive': cut,
            'n_rows': cnt(lambda r: True),
            'tenure_nonnull': cnt(lambda r: tenure(r) is not None),
            'new_host_le12': cnt(lambda r: is_new(r, bidx, 12)),
            'new_host_le24': cnt(lambda r: is_new(r, bidx, 24)),
            'new_host_le12_and_single': cnt(lambda r: is_new(r, bidx, 12) and single(r)),
            'crosstab_scope_price(列=舊代理首評分類,欄=真新手12個月)': ct,
            'proxy_yes': len(proxy), 'real_yes': real_yes, 'both': both,
            'proxy_precision_pct(舊代理說新的裡面真新手)': round(100 * both / len(proxy), 1),
            'proxy_recall_pct(真新手裡被舊代理抓到)': round(100 * both / real_yes, 1),
        }
        assert sum(v['真新手'] + v['非新手'] for v in ct.values()) == len(sp)
        assert real_yes == c['new_host_le12']['scope_price']
        if city == 'melbourne':
            got = {'all_le12': c['new_host_le12']['all'], 'scope_le12': c['new_host_le12']['scope'],
                   'scope_price_le12': c['new_host_le12']['scope_price'],
                   'scope_price_le24': c['new_host_le24']['scope_price'],
                   'scope_price_le12_single': c['new_host_le12_and_single']['scope_price'], 'both': both}
            assert got == EXPECT_MEL, ('墨爾本對不上 mel_c', got)
        result[city] = c
        print(city, 'ok', c['new_host_le12'], c['new_host_le24']['scope_price'],
              c['new_host_le12_and_single']['scope_price'], both, flush=True)
    meta = {'scope_id': 'IS-1112-FIX-NEWHOST', 'batch': '2026-09-16',
            'definition': '真新手 = 房東開始月(last_scraped 月份 - 年資月數)>= 基準月 - 12;'
                          '年資(月)= hosts_time_as_host_years*12 + hosts_time_as_host_months;基準月 = last_scraped 最大值的月份',
            'scope_def': '篩選=整套/1-2房/2-4人/最低1-7晚;有價=篩選且 price 非空',
            'field_caveat': '年資欄欄義由墨爾本 2025-12 期 host_since 排除法推論(notes/19 §5),官方欄位說明還沒查',
            'sydney_caveat': '雪梨沒有 2025-12 那期可驗證欄義;雪梨的欄義沿用墨爾本的推論,未另外驗證',
            'melbourne_check': '墨爾本結果已 assert 等於 mel_c_hosts_time_2026-11-11.json 的 c_new_host_definition(T 口徑)'}
    OUT.write_text(json.dumps({'meta': meta, 'cities': result}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('wrote', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
