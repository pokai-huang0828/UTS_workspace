"""T6 收入情景(估算,不是實際收入)。

年收入 = 每晚價格 × 入住晚數 × (1 − 服務費率) − 使用者填的年成本
- 入住晚數:同類的 estimated_occupancy_l365d(Inside Airbnb 由評論數推算),**先排除估計 0 晚的房源**(視為沒在營業),
  再取第 25/50/75 百分位 = 低/中/高,每一個再以 180 晚封頂(大雪梨非房東同住的整套房,每 365 天最多 180 晚)。
- 服務費率兩種情景:約 3%(房東只付小額服務費的拆分制)與約 15.5%(房東付全額的單一費率制)。
- 價格:使用者打算開的價;沒給就用模型參考價。
"""
import numpy as np

from . import data_access as D

CAP_NIGHTS = 180
FEE_RATES = {'約 3%': 0.03, '約 15.5%': 0.155}
NOTE = ('估算,不是實際收入;入住晚數是由評論推算的(Inside Airbnb 的 estimated_occupancy_l365d),價格是掛牌價。'
        '這裡假設入住晚數和你開的價無關(同類的晚數是它們各自標價下的數字)。')


def scenarios(price, occ_values, annual_cost=0.0, cap=CAP_NIGHTS, fee_rates=FEE_RATES):
    """occ_values:同類每間房的估算入住晚數(陣列)。回傳低/中/高 × 兩種費率。"""
    occ = np.asarray(occ_values, float)
    occ = occ[~np.isnan(occ)]
    n_total = int(len(occ))
    occ = occ[occ > 0]                       # 估計 0 晚 = 視為沒在營業,不納入分位數
    n_zero = n_total - int(len(occ))
    if not len(occ):
        raise ValueError('同類房源的估算入住晚數全是 0 或缺值,算不出收入情景。')
    raw = dict(zip(['低', '中', '高'], np.percentile(occ, [25, 50, 75])))
    rows = []
    for lvl, n_raw in raw.items():
        n = min(float(n_raw), cap)
        for fname, rate in fee_rates.items():
            gross = price * n
            rows.append({'level': lvl, 'nights_raw': round(float(n_raw), 1), 'nights': round(n, 1),
                         'capped': bool(n_raw > cap), 'fee_name': fname, 'fee_rate': rate,
                         'gross': round(gross, 0), 'fee': round(gross * rate, 0), 'cost': round(float(annual_cost), 0),
                         'income': round(gross * (1 - rate) - annual_cost, 0)})
    return {'price': round(float(price), 1), 'n_with_occ': int(len(occ)), 'n_total': n_total, 'n_zero': n_zero, 'cap': cap, 'rows': rows, 'note': NOTE}


def income_for_group(pool, group_ids, price, annual_cost=0.0):
    occ = pool.loc[pool.id.isin(set(group_ids)), 'occ365'].values
    return scenarios(price, occ, annual_cost)
