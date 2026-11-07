"""Profile documented 2026 snapshots; review history is not a 2024 market panel."""
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / 'scratchpad/airbnb_2024_two_cities'
OUT = ROOT / 'Innovation Studio/notes/raw/airbnb_two_city_profile_2026-11-07.json'
SOURCES = {
    'sydney': 'https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16',
    'melbourne': 'https://data.insideairbnb.com/australia/vic/melbourne/2026-09-16',
}


def download(url, path):
    if not path.exists():
        temporary = path.with_suffix(path.suffix + '.part')
        try:
            with urllib.request.urlopen(url, timeout=90) as response, temporary.open('wb') as target:
                while chunk := response.read(1024 * 1024):
                    target.write(chunk)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    return path


def profile(city, base):
    path = CACHE / f'{city}_listings.csv.gz'
    previous = ROOT / 'scratchpad/airbnb_2026-11-07/sydney_listings.csv.gz'
    if city == 'sydney' and previous.exists():
        path = previous
    else:
        download(base + '/data/listings.csv.gz', path)
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames
    assert rows and len({r['id'] for r in rows}) == len(rows)
    scope = [r for r in rows if r['room_type'] == 'Entire home/apt' and r['bedrooms'] in ('1', '2')
             and r['accommodates'].isdigit() and 2 <= int(r['accommodates']) <= 4
             and r['minimum_nights'].isdigit() and 1 <= int(r['minimum_nights']) <= 7]
    with urllib.request.urlopen(base+'/data/calendar.csv.gz', timeout=45) as response:
        with gzip.GzipFile(fileobj=response) as f:
            calendar_fields = f.readline().decode('utf-8-sig').strip().split(',')
    review_path = download(base+'/visualisations/reviews.csv', CACHE/f'{city}_reviews_summary.csv')
    years = collections.Counter()
    dates = []
    with review_path.open(encoding='utf-8-sig', newline='') as f:
        review_reader = csv.DictReader(f)
        assert {'listing_id', 'date'} <= set(review_reader.fieldnames)
        for r in review_reader:
            date = r['date']
            if date:
                years[date[:4]] += 1
                dates.append(date)
    assert sum(years.values()) == len(dates)
    return {'listings_url': base+'/data/listings.csv.gz',
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'rows': len(rows), 'columns': len(fields),
            'last_scraped': sorted({r['last_scraped'] for r in rows}),
            'price_nonempty': sum(bool(r['price']) for r in rows),
            'scope_rows': len(scope), 'scope_price_nonempty': sum(bool(r['price']) for r in scope),
            'calendar_fields': calendar_fields,
            'reviews_summary_url': base+'/visualisations/reviews.csv',
            'review_rows_with_date': len(dates), 'review_date_min': min(dates), 'review_date_max': max(dates),
            'reviews_by_year': dict(sorted(years.items())),
            'reviews_since_2024': sum(n for y,n in years.items() if y >= '2024'),
            'history_warning': 'Reviews attached to listings in this snapshot; not all historical listings or bookings.'}


if __name__ == '__main__':
    CACHE.mkdir(parents=True, exist_ok=True)
    results = {}
    for city, base in SOURCES.items():
        results[city] = profile(city, base)
        print(city, json.dumps(results[city], ensure_ascii=False), flush=True)
    OUT.write_text(json.dumps({'target_start': '2024-01-01', 'historical_snapshots_2024_acquired': False,
                               'cities': results}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
