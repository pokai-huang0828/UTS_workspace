"""煙霧測試:python "Innovation Studio/app_prototype/tests/smoke_test.py"(全過 → 結束碼 0)。

檢查附錄 B 的數字、T1 的規則(10–20 間、不用價格、可重現、小組退回規則)、T6 的封頂/費率/成本、
T7 的指數平均與之前結果的差距、公開版 HTML 不含房源 id 與網址。
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from core import data_access as D, income, peers, report, reviews, season  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append(bool(ok))
    print(f"[{'過' if ok else '不過'}] {name}" + (f' — {detail}' if detail else ''))


pool = D.load_pool()
check('母體 6,639 間', len(pool) == 6639, f'{len(pool)}')

# ---------- 附錄 B ----------
AMEN = ['Kitchen', 'Washer', 'Wifi']
r = report.build('Sydney', 1, 2, 1, 1, AMEN, price=300)
t1, t2, t3 = r['T1'], r['T2'], r['T3']
check('附錄 B:同類 1,291 間', t1['group_n'] == 1291 and t2['n'] == 1291, f"T1 {t1['group_n']}、T2 {t2['n']}")
want = (265.9, 323.4, 388.8)
got = (t2['p25'], t2['p50'], t2['p75'])
check('附錄 B:25/50/75 分位 265.9 / 323.4 / 388.8', all(abs(a - b) < 0.05 for a, b in zip(got, want)),
      f'算出 {got[0]} / {got[1]} / {got[2]}')
gaps = {g['amenity']: g['pct'] for g in t3['gaps']}
for a, p in [('Smoke alarm', 97.1), ('Hot water', 93.1), ('Dishes and silverware', 91.2)]:
    check(f'附錄 B:設施差距含 {a}({p}%)', a in gaps and abs(gaps[a] - p) < 0.05, f'算出 {gaps.get(a)}')

# ---------- T1 ----------
check('T1:回傳 10–20 間', 10 <= len(t1['top']) <= 20, f"{len(t1['top'])} 間")
check('T1:匹配欄位不含價格', not any('price' in c for c in peers.MATCH_COLS), str(peers.MATCH_COLS))
shuffled = pool.copy()
shuffled['price_num'] = np.random.default_rng(0).permutation(shuffled.price_num.values)
a1 = peers.find_peers(pool, 'Sydney', 1, 2, AMEN)
a2 = peers.find_peers(shuffled.drop(columns=['price_num', 'y']), 'Sydney', 1, 2, AMEN)
check('T1:價格欄打亂/拿掉後結果不變', [x['id'] for x in a1['top']] == [x['id'] for x in a2['top']])
a3 = peers.find_peers(pool, 'Sydney', 1, 2, AMEN)
check('T1:同一輸入跑兩次結果相同', a1 == a3)

# 小組退回規則:找同區同臥室數不足 30 間的組(依區名排序取第一個)
cnt = pool.groupby(['nb', 'bed_n']).size()
small = cnt[cnt < 30].sort_index()
nb_s, bed_s = small.index[0]
fb = peers.find_peers(pool, nb_s, int(bed_s), 2, AMEN)
check(f'T1:退回規則({nb_s} {bed_s} 臥只有 {small.iloc[0]} 間 → 最近 30 間)',
      fb['group_n'] == 30 and '改用' in fb['level'] and 10 <= len(fb['top']) <= 20,
      f"{fb['level']};同類 {fb['group_n']} 間,其中同區 {sum(pool.set_index('id').loc[fb['group_ids'], 'nb'] == nb_s)} 間")

# ---------- T6 ----------
s = income.scenarios(300, [200, 250, 300, 400], annual_cost=0)
check('T6:入住晚數超過 180 → 封頂 180', all(x['nights'] == 180 and x['capped'] for x in s['rows']),
      f"原始 {[x['nights_raw'] for x in s['rows'][::2]]} → {[x['nights'] for x in s['rows'][::2]]}")
low3 = next(x for x in s['rows'] if x['fee_name'] == '約 3%')['income']
low15 = next(x for x in s['rows'] if x['fee_name'] == '約 15.5%')['income']
check('T6:兩種費率的收入不同', low3 != low15, f'{low3:,.0f} vs {low15:,.0f}')
s0 = income.scenarios(300, [50, 80, 120], annual_cost=0)
s1 = income.scenarios(300, [50, 80, 120], annual_cost=5000)
check('T6:年成本有被扣掉', all(abs((a['income'] - b['income']) - 5000) < 1 for a, b in zip(s0['rows'], s1['rows'])))
t6 = r['T6']
check('T6:附錄 B 例子有算出 6 個情景', len(t6['rows']) == 6,
      ';'.join(f"{x['level']}{x['nights']:g}晚/{x['fee_name']}={x['income']:,.0f}" for x in t6['rows']))

# ---------- T7 ----------
ip, ia = r['T7']['index_peers'], r['T7']['index_all']
check('T7:同類月份指數 12 個月平均約 100', abs(ip['mean'] - 100) < 0.5, f"{ip['mean']}")
check('T7:全市月份指數 12 個月平均約 100', abs(ia['mean'] - 100) < 0.5, f"{ia['mean']}")
check('T7:11 月、5 月與之前結果(135.5 / 75.3)的差距已算出', ia['nov_vs_prev'] is not None,
      f"全市 11 月 {ia['index'][11]}(差 {ia['nov_vs_prev']:+})、5 月 {ia['index'][5]}(差 {ia['may_vs_prev']:+});"
      f"同類 11 月 {ip['index'][11]}、5 月 {ip['index'][5]}")
check('T7:2026 年假期標待補', '待補' in season.holidays(2026)['note'])
check('T7:2025 年 NSW 假期有資料', len(season.holidays(2025)['items']) > 0, f"{len(season.holidays(2025)['items'])} 天")
cal = r['T7']['calendar']['months']
check('T7:日曆 12 個月都有比例', len(cal) == 12 and all(m['pct'] is not None for m in cal))

# ---------- HTML ----------
pub = report.to_html(r, public=True)
loc = report.to_html(r, public=False)
leak = [x['id'] for x in t1['top'] if re.search(rf'(?<!\d){x["id"]}(?!\d)', pub)]
check('公開版不含同類房源 id', not leak, f'洩漏 {len(leak)} 個')
check('公開版沒有任何網址', not re.search(r'https?://|www\.|airbnb\.com', pub, re.I))
check('本機版有房源 id', all(x['id'] in loc for x in t1['top']))
check('頁首警語在', '這是原型的計算結果,價格是掛牌價,收入是估算' in pub)
DEMO = '這是示範,不是你輸入的那間房。'
check('T4、T5 有示範區塊與醒目說明(公開版)', pub.count(DEMO) >= 2 and '代號 房源C' in pub and '尚未接上' not in pub)
check('T4:示範房 7 個方面都列出', all(a in pub for a in ['清潔', '噪音', '位置與交通', '入住', '房東溝通', '性價比', '設施與舒適']))
check('T5:規則白話與限制都寫了', '至少被提到 3 次' in pub and '20%' in pub and '還沒有人拿人工答案對過' in pub and '暫定' in pub)
r_nodemo = report.build('Sydney', 1, 2, 1, 1, AMEN, price=300, review_demo=None)
check('T4、T5:沒有示範資料時維持「尚未接上」', report.to_html(r_nodemo, True).count('尚未接上') >= 2)
loc_id = pd.read_csv(reviews.RUN / 'listing_summary_local.csv', encoding='utf-8-sig', dtype={'listing_id': str})
loc_id = loc_id[loc_id.房源 == '房源C'].listing_id.iloc[0]
check('公開版不含示範房的房源 id、不含本機專屬字樣', loc_id not in pub and '(本機版才有)' not in pub and '(本機版才有)' in loc)
r_h = report.build('Sydney', 1, 2, 1, 1, AMEN, price=300, review_demo='房源A')
check('T5:優先改進項與 summary.json 一致(房源A:噪音、設施與舒適)',
      [x['aspect'] for x in reviews.load_demo('房源A')['priorities']] == ['噪音', '設施與舒適'])
check('T5:沒有任何項目達標 → 寫「沒有明顯要優先改的」', '沒有明顯要優先改的' in report.to_html(
    report.build('Sydney', 1, 2, 1, 1, AMEN, price=300, review_demo='房源G'), True))

# ---------- 補強(VERIFY.md 的建議) ----------
check('T2:模型參考價 265.7(±0.1)', abs(t2['model']['price'] - 265.7) <= 0.1, f"{t2['model']['price']}")
check('T2:開 300 → 同類第 41 百分位', round(t2['my_pct']) == 41, f"{t2['my_pct']}")
check('T6:新的入住晚數 42 / 96 / 180(排除 0 晚)', [x['nights'] for x in t6['rows'][::2]] == [42, 96, 180],
      f"{[x['nights'] for x in t6['rows'][::2]]};同類 {t6['n_total']} 間、0 晚 {t6['n_zero']} 間")
check('T6:同類 112 間估計 0 晚被排除', t6['n_zero'] == 112 and t6['n_with_occ'] == 1179)
want_inc = [12222, 10647, 27936, 24336, 52380, 45630]
check('T6:六個金額', [x['income'] for x in t6['rows']] == want_inc, f"{[x['income'] for x in t6['rows']]}")
check('T6:頁面寫明已排除 0 晚與「未扣稅」', '有 112 間估計 0 晚,已排除' in pub and '年收入(估算,未扣稅)' in pub and '都還沒扣' in pub)
check('T7:全部可比房源 11 月 136.9 / 5 月 75.0', (ia['index'][11], ia['index'][5]) == (136.9, 75.0), f"{ia['index'][11]} / {ia['index'][5]}")
check('T7:同類 11 月 142.4 / 5 月 80.2', (ip['index'][11], ip['index'][5]) == (142.4, 80.2), f"{ip['index'][11]} / {ip['index'][5]}")
check('T7:日曆第一個月(2026-10)62.3%', cal[0]['ym'] == '2026-10' and cal[0]['pct'] == 62.3, f"{cal[0]}")
check('T7:Bank Holiday 標「只適用銀行業」', any('Bank Holiday' in x['name'] and '只適用銀行業' in x['name'] for x in season.holidays(2025)['items']))
check('T7:表頭「全部可比房源(6,639 間)」、原因標「未驗證」、日曆不再寫「幾乎訂不到」',
      '全部可比房源(6,639 間)' in pub and '可能是因為範圍不同(未驗證)' in pub and '幾乎訂不到' not in pub)

# 設施大小寫與對不到
rl = report.build('Sydney', 1, 2, 1, 1, ['wifi', 'KITCHEN', ' washer '], price=300)
check('設施大小寫不同(wifi / WIFI)結果相同', rl['T3'] == t3 and rl['T1']['top'] == t1['top'] and rl['input']['amen'] == r['input']['amen'])
rb = report.build('Sydney', 1, 2, 1, 1, ['Kitchen', 'Wi-Fi', 'Washer'], price=300)
pb = report.to_html(rb, True)
check('設施對不到會被列出(頁面與命令列摘要)', rb['input']['amen_unmatched'] == ['Wi-Fi'] and '沒有算進去' in pb and 'Wi-Fi' in pb
      and 'Wi-Fi' in report.summary_text(rb))

# 輸入檢查
def err_of(**kw):
    a = dict(nb='Sydney', bedrooms=1, acc=2, beds=1, baths=1, amen=AMEN)
    a.update(kw)
    try:
        report.build(a['nb'], a['bedrooms'], a['acc'], a['beds'], a['baths'], a['amen'])
    except ValueError as e:
        return str(e)
    return None
e3, e9, ez = err_of(bedrooms=3), err_of(acc=9), err_of(nb='Nowhere')
check('輸入 3 臥室 → 中文錯誤訊息', e3 and '只支援 1 或 2' in e3, str(e3))
check('輸入可住 9 人 → 中文錯誤訊息', e9 and '2–4' in e9, str(e9))
check('輸入不存在的區 → 中文錯誤訊息並列出可用的區', ez and '找不到區' in ez and 'Sydney' in ez, str(ez)[:60])

# 小樣本警語
rf = report.build(nb_s, int(bed_s), 2, 1, 1, AMEN, price=300)
pf = report.to_html(rf, True)
check('退回規則的例子頁面有小樣本警語(T2、T3、T6、T7 各一句)',
      rf['fallback'] and pf.count('同區同臥室數不足 30 間,以下是用全市最近的 30 間算的,樣本小,僅供參考') == 4, f"{pf.count('樣本小')} 句")
check('一般例子(同類 1,291 間)沒有小樣本警語', '樣本小' not in pub)


n_ok = sum(RESULTS)
print(f'\n共 {len(RESULTS)} 項,過 {n_ok} 項')
sys.exit(0 if n_ok == len(RESULTS) else 1)
