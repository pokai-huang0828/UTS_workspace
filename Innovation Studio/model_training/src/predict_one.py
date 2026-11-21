"""輸入一間房「上架前就知道」的條件 → 模型參考價 + 同類(同區同臥室數;不足 30 間改用同臥室數最近 30 間)的 25/50/75 分位價。
例(報告附錄 B):
  python "Innovation Studio/model_training/src/predict_one.py" --nb Sydney --bedrooms 1 --acc 2 --beds 1 --baths 1 \
      --amen "Kitchen,Washer,Wifi"
沒給經緯度 → 用該區房源經緯度的中位數;沒給房型細類 → 最常見的那一種;沒給最少入住晚數 → 全體中位數(都記在 model_card.json)。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', default='run_2026-11-21_01')
    ap.add_argument('--nb', required=True, help='區(neighbourhood_cleansed),例如 Sydney')
    ap.add_argument('--bedrooms', type=int, required=True, choices=[1, 2])
    ap.add_argument('--acc', type=int, required=True, help='可住人數 2–4')
    ap.add_argument('--beds', type=float, required=True)
    ap.add_argument('--baths', type=float, required=True)
    ap.add_argument('--amen', default='', help='設施,逗號分隔,要用資料裡的英文名稱(如 Kitchen,Washer,Wifi)')
    ap.add_argument('--property-type', default=None)
    ap.add_argument('--min-nights', type=int, default=None)
    ap.add_argument('--lat', type=float, default=None)
    ap.add_argument('--lon', type=float, default=None)
    a = ap.parse_args()

    run = C.RUNS / a.run
    bundle = joblib.load(run / 'model_final.joblib')
    card = json.load(open(run / 'model_card.json', encoding='utf-8'))
    dfl = card['defaults_for_predict_one']
    spec = C.Spec.from_dict(bundle['spec'])
    if a.nb not in spec.nb_levels:
        sys.exit(f'區「{a.nb}」不在訓練資料裡;可用:{spec.nb_levels}')
    lat, lon = dfl['nb_centroid_median_latlon'][a.nb]
    lat = a.lat if a.lat is not None else lat
    lon = a.lon if a.lon is not None else lon
    amen = frozenset(x.strip() for x in a.amen.split(',') if x.strip())
    unknown = sorted(amen - set(spec.top_amen))
    row = pd.DataFrame([{'nb': a.nb, 'property_type': a.property_type or dfl['property_type_most_common'],
                         'lat': lat, 'lon': lon, 'bed_n': a.bedrooms, 'acc': a.acc, 'beds_n': a.beds, 'baths': a.baths,
                         'min_n': a.min_nights if a.min_nights is not None else dfl['min_nights_median'],
                         'amen_n': len(amen), 'amen': amen}])
    X, _ = C.make_X(row, spec)
    price = float(np.exp(bundle['model'].predict(X)[0]))

    print(f'模型:{bundle["model_name"]}({card["trained_on"]})')
    print(f'輸入:{row.drop(columns="amen").iloc[0].to_dict()};設施 {sorted(amen)}')
    if unknown:
        print(f'  注意:這些設施不在模型的 40 項名單裡,只算進設施數:{unknown}')
    print(f'模型參考價:{price:,.1f} 澳元/晚')
    for label, name in [('6,615 間(去掉每晚 > 2,000)', ['train_table_2026-09.csv']),
                        ('6,639 間(含極端值,同報告附錄 B 的口徑)', ['train_table_2026-09.csv', 'extremes_dropped_24.csv'])]:
        pool = pd.concat([pd.read_csv(C.PROC / n, dtype={'id': str, 'host_id': str, 'bedrooms': str},
                                      keep_default_na=False) for n in name])
        pr, how = C.peers(pool, a.nb, a.bedrooms, lat, lon)
        p25, p50, p75 = np.percentile(pr, [25, 50, 75])
        print(f'同類({how},{label}):{len(pr):,} 間;25/50/75 分位 = {p25:,.1f} / {p50:,.1f} / {p75:,.1f};'
              f'參考價落在同類第 {100 * np.mean(pr <= price):.0f} 百分位')


if __name__ == '__main__':
    main()
