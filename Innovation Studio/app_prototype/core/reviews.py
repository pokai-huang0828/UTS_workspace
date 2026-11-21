"""T4、T5 的「示範」資料:讀 review_analysis 已經算好的彙總(10 間房 × 每間 30 條評論,由 Claude Sonnet 讀過)。

只讀三個彙總檔,不讀評論原文,也不讀 labels_*.json:
- summary.json:各方面合計、T5 暫定規則與每間房的優先改進項
- listing_summary_public.csv:每間房 × 每個方面的統計,只有代號(房源A–J)
- listing_summary_local.csv:同上,多了區、評分(只用在本機版;本檔刻意不讀 listing_id 欄)
檔案不存在 → 回傳 None,頁面維持「尚未接上」。
"""
import json
from pathlib import Path

import pandas as pd

from . import data_access as D

RUN = D.IS / 'review_analysis' / 'runs' / 'run_2026-11-21_listing10'
ASPECTS = ['清潔', '噪音', '位置與交通', '入住', '房東溝通', '性價比', '設施與舒適']
RULE_TEXT = ('某個方面至少被提到 3 次、而且「有抱怨的比例」(負評加有好有壞,佔有提到的幾成)達 20% 以上,才列入;'
             '依比例由高到低取前 3 項。')
MIN_MENTIONS, MIN_PCT, TOP_K = 3, 20.0, 3


def _files():
    return RUN / 'summary.json', RUN / 'listing_summary_public.csv', RUN / 'listing_summary_local.csv'


def available_codes():
    s, p, _ = _files()
    if not (s.exists() and p.exists()):
        return []
    return sorted(pd.read_csv(p, encoding='utf-8-sig').房源.unique())


def _plain(r):
    n_all, k = int(r['評論數']), int(r['有提到'])
    if k == 0:
        return f'{n_all} 條評論裡沒有人提到。'
    s = (f'{n_all} 條評論裡有 {k} 條提到;好評 {int(r["好評"])} 條、負評 {int(r["負評"])} 條、有好有壞 {int(r["有好有壞"])} 條,'
         f'有抱怨的佔 {r["有抱怨的比例%"]:.0f}%。')
    if k < MIN_MENTIONS:
        s += f'(提到不到 {MIN_MENTIONS} 次,證據不足。)'
    return s


def load_demo(code, public=True):
    """回傳 dict(code、n_reviews、aspects 列、priorities、rule、empty_text、local 額外資訊)或 None。"""
    s_f, p_f, l_f = _files()
    if not (s_f.exists() and p_f.exists()):
        return None
    summ = json.load(open(s_f, encoding='utf-8'))
    pub = pd.read_csv(p_f, encoding='utf-8-sig')
    pub = pub[pub.房源 == code]
    if pub.empty:
        return None
    rows = []
    for a in ASPECTS:
        x = pub[pub.方面 == a]
        if x.empty:
            continue
        r = x.iloc[0]
        rows.append({'aspect': a, 'n_reviews': int(r['評論數']), 'mentions': int(r['有提到']), 'pos': int(r['好評']),
                     'neg': int(r['負評']), 'mixed': int(r['有好有壞']), 'complaint_pct': float(r['有抱怨的比例%']),
                     'plain': _plain(r)})
    prio = []
    for x in summ['T5 暫定規則']['每間房的優先改進項'].get(code, []):
        row = next((q for q in rows if q['aspect'] == x['方面']), None)
        prio.append({'aspect': x['方面'], 'complaint_pct': float(x['有抱怨的比例%']), 'mentions': int(x['有提到']),
                     'plain': (f'被提到 {x["有提到"]} 次,其中有抱怨的佔 {x["有抱怨的比例%"]:.0f}%'
                               + (f'(負評 {row["neg"]} 條、有好有壞 {row["mixed"]} 條)' if row else '') + '。')})
    out = {'code': code, 'n_reviews': rows[0]['n_reviews'] if rows else 0, 'aspects': rows, 'priorities': prio,
           'rule': RULE_TEXT, 'empty_text': '沒有明顯要優先改的:沒有任何方面同時達到「至少被提到 3 次」和「有抱怨的比例 20% 以上」。',
           'n_listings': summ['n_listings'], 'per_listing': summ['n_reviews'] // summ['n_listings'],
           'reader': summ['讀的模型'], 'local': None}
    if not public and l_f.exists():     # 本機版才多顯示區與評分;不讀 listing_id 欄
        loc = pd.read_csv(l_f, encoding='utf-8-sig', usecols=['房源', '區', '臥室', '總評分'])
        loc = loc[loc.房源 == code]
        if not loc.empty:
            r = loc.iloc[0]
            out['local'] = {'nb': str(r['區']), 'bedrooms': int(r['臥室']), 'rating': float(r['總評分'])}
    return out
