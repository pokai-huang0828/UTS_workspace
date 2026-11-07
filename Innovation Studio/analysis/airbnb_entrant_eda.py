"""Reproduce aggregate Sydney entrant analysis; raw listing records stay local."""
import argparse
import collections
import csv
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import statistics


def money(value):
    return float(value.replace('$', '').replace(',', '')) if value else None


def summarize(rows):
    prices = [money(r['price']) for r in rows if money(r['price']) is not None]
    return {'n': len(rows), 'priced_n': len(prices),
            'median_listed_price': statistics.median(prices) if prices else None}


def analyze(path):
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        columns = reader.fieldnames
    assert hashlib.sha256(path.read_bytes()).hexdigest() == '06bbd629fbe93d9da1f2163e82d584a58738a53d7897d5c081f665aadc4e3c55', 'Use the documented September 2026 Sydney file; revalidate scope and chart labels for another snapshot'
    assert rows and len({r['id'] for r in rows}) == len(rows), 'Listing IDs must be unique'
    assert all(k in columns for k in ['price', 'price_quote_checkin_date', 'price_quote_checkout_date'])
    price_pairs = [(money(r['price']), money(r['price_quote_price_per_night'])) for r in rows
                   if r['price'] and r['price_quote_price_per_night']]
    entire = [r for r in rows if r['room_type'] == 'Entire home/apt']
    # shortcut: scope is a proposed teaching case, revisit after the team selects a target property.
    scope = [r for r in entire if r['bedrooms'] in ('1', '2') and r['accommodates'].isdigit()
             and 2 <= int(r['accommodates']) <= 4 and r['minimum_nights'].isdigit()
             and 1 <= int(r['minimum_nights']) <= 7]
    groups = collections.defaultdict(list)
    for r in scope:
        if r['price'] and r['price_quote_checkin_date'] and r['price_quote_checkout_date']:
            groups[(r['price_quote_checkin_date'], r['price_quote_checkout_date'])].append(r)
    top = sorted(groups.items(), key=lambda x: (-len(x[1]), x[0]))[:5]
    assert top, 'No priced quote groups in the proposed scope'
    common = top[0][1] if top else []
    assert sum(len(v) for v in groups.values()) <= len(scope)
    by_area = collections.defaultdict(list)
    for r in common:
        by_area[r['neighbourhood_cleansed']].append(r)
    result = {
        'source': 'https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/listings.csv.gz',
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'snapshot_directory': '2026-09-16', 'last_scraped': sorted({r['last_scraped'] for r in rows}),
        'rows': len(rows), 'columns': len(columns), 'all': summarize(rows),
        'room_types': dict(collections.Counter(r['room_type'] for r in rows)),
        'minimum_nights_missing': sum(not r['minimum_nights'] for r in rows),
        'minimum_nights_ge_90': sum(int(r['minimum_nights']) >= 90 for r in rows if r['minimum_nights'].isdigit()),
        'price_pair_comparable_n': len(price_pairs),
        'price_pair_equal_n': sum(abs(a-b) < .011 for a,b in price_pairs),
        'scope_definition': 'Entire home/apt; bedrooms 1 or 2; accommodates 2–4; minimum_nights 1–7; missing scope fields excluded',
        'scope': summarize(scope),
        'scope_quote_groups': len(groups),
        'top_scope_quote_groups': [{'checkin': k[0], 'checkout': k[1],
            'nights': (dt.date.fromisoformat(k[1])-dt.date.fromisoformat(k[0])).days,
            **summarize(v)} for k,v in top],
        'largest_quote_group_areas': {k: summarize(v) for k,v in sorted(by_area.items()) if len(v) >= 10},
        'scope_amenities_top': collections.Counter(a for r in scope for a in set(json.loads(r['amenities']))).most_common(12),
        'caveats': ['Listed/quoted prices, not completed bookings or revenue.',
                    'Common dates alone do not equalize bedroom, capacity, fees or guest count.',
                    'Areas with <10 listings omitted only from area aggregate, not from scope.']
    }
    assert sum(result['room_types'].values()) == len(rows)
    assert 0 <= result['price_pair_equal_n'] <= len(price_pairs)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    assert money('$1,234.50') == 1234.5 and money('') is None
    result = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels = ['All Sydney listings', 'Entire home / apt', 'Proposed entrant scope',
              'Scope with listed price', 'Same check-in/out (Sep 17–18)']
    values = [result['rows'], result['room_types']['Entire home/apt'], result['scope']['n'],
              result['scope']['priced_n'], result['top_scope_quote_groups'][0]['n']]
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.subplots_adjust(left=.29, right=.95, top=.86, bottom=.25)
    ax.barh(labels[::-1], values[::-1], color='#247c83')
    for i, value in enumerate(values[::-1]):
        ax.text(value+180, i, f'{value:,}', va='center')
    ax.set_xlim(0, 24000)
    ax.set_xlabel('Listings remaining after each filter')
    ax.set_title('Sydney: defining a comparable competitor set', loc='left', fontweight='bold')
    fig.text(.02, .035, 'Source: Inside Airbnb, 2026-09-16 directory. Scope: 1–2 bedrooms, 2–4 guests, minimum stay 1–7 nights.\n'
             'Same dates do not control bedrooms, capacity, guest count or fees. Listed prices are not transactions.', fontsize=8)
    chart = Path(__file__).resolve().parents[1] / 'notes/08_深度分析/img/airbnb_entrant_scope_2026-11-07.png'
    chart.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(chart, dpi=150, bbox_inches='tight', pad_inches=.25)
    plt.close(fig)
    print(json.dumps(result, ensure_ascii=False, indent=2))
