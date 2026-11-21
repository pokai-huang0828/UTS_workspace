"""T2 價格位置與參考價。價格一律是「掛牌價」(Inside Airbnb 抓到的標價,不是成交價)。

- 同類的第 25/50/75 百分位價:用 T1 的同類那一組(6,639 間母體)。
- 使用者打算開的價 → 它在同類裡的百分位(同類中掛牌價 ≤ 這個價的比例)。
- 模型參考價:載入 model_training/runs/run_2026-11-21_01/model_final.joblib(XGBoost,6,615 間訓練)。
"""
import numpy as np
import pandas as pd

from . import data_access as D


def model_price(nb, bed_n, acc, beds, baths, amen, lat=None, lon=None, property_type=None, min_nights=None):
    """跟 model_training/src/predict_one.py 同一套做法。沒給的欄位用 model_card.json 的預設值。"""
    bundle, card = D.load_model()
    dfl = card['defaults_for_predict_one']
    spec = D.C.Spec.from_dict(bundle['spec'])
    if nb not in spec.nb_levels:
        raise ValueError(f'區「{nb}」不在訓練資料裡')
    clat, clon = dfl['nb_centroid_median_latlon'][nb]
    amen = frozenset(amen)
    row = pd.DataFrame([{'nb': nb, 'property_type': property_type or dfl['property_type_most_common'],
                         'lat': clat if lat is None else lat, 'lon': clon if lon is None else lon,
                         'bed_n': bed_n, 'acc': acc, 'beds_n': beds, 'baths': baths,
                         'min_n': dfl['min_nights_median'] if min_nights is None else min_nights,
                         'amen_n': len(amen), 'amen': amen}])
    X, _ = D.C.make_X(row, spec)
    price = float(np.exp(bundle['model'].predict(X)[0]))
    unknown = sorted(amen - set(spec.top_amen))
    return {'price': round(price, 1), 'model_name': bundle['model_name'], 'trained_on': card['trained_on'],
            'amen_not_in_model': unknown}


def price_position(pool, group_ids, my_price=None, ref_price=None):
    pr = pool.loc[pool.id.isin(set(group_ids)), 'price_num'].values
    p25, p50, p75 = np.percentile(pr, [25, 50, 75])
    out = {'n': int(len(pr)), 'p25': round(float(p25), 1), 'p50': round(float(p50), 1), 'p75': round(float(p75), 1)}
    if my_price is not None:
        out['my_price'] = float(my_price)
        out['my_pct'] = round(float(100 * np.mean(pr <= my_price)), 1)
    if ref_price is not None:
        out['ref_pct'] = round(float(100 * np.mean(pr <= ref_price)), 1)
    return out
