"""把 T1、T2、T3、T6、T7 的結果組成一個 dict,並輸出成一頁純靜態 HTML(不引用任何外部網址)。

public=True:同類清單只列區、臥室、可住人數、設施數、相似度(不列房源 id、名稱、房東、網址、價格)。
public=False:另外列房源 id 和匹配理由,只留本機。
T4、T5:有 review_analysis 的彙總檔時,顯示「已讀過評論的 10 間房之一」的示範(不是使用者輸入的那間房);檔案不存在就標「尚未接上」。
"""
from html import escape

from . import amenities, data_access as D, income, peers, pricing, reviews, season

FALLBACK_WARN = '同區同臥室數不足 30 間,以下是用全市最近的 30 間算的,樣本小,僅供參考。'
MONTHS_ZH = ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月', '7 月', '8 月', '9 月', '10 月', '11 月', '12 月']


def check_input(pool, nb, bedrooms, acc):
    """輸入範圍檢查;不合就丟 ValueError(中文訊息)。回傳資料裡的標準區名(區名不分大小寫)。"""
    if bedrooms not in (1, 2):
        raise ValueError(f'臥室數只支援 1 或 2(你輸入 {bedrooms})。這個原型的資料只涵蓋整套、1–2 臥、可住 2–4 人的房子。')
    if acc not in (2, 3, 4):
        raise ValueError(f'可住人數只支援 2–4 人(你輸入 {acc})。這個原型的資料只涵蓋整套、1–2 臥、可住 2–4 人的房子。')
    nbs = sorted(pool.nb.unique())
    hit = [x for x in nbs if x.lower() == str(nb).strip().lower()]
    if not hit:
        raise ValueError(f'找不到區「{nb}」。目前支援的區(資料裡的英文名稱)共 {len(nbs)} 個:' + '、'.join(nbs))
    return hit[0]


def build(nb, bedrooms, acc, beds, baths, amen, price=None, annual_cost=0.0, lat=None, lon=None,
          threshold=amenities.DEFAULT_THRESHOLD, year=2026, top_n=20, review_demo='房源C'):
    pool = D.load_pool()
    nb = check_input(pool, nb, bedrooms, acc)
    amen, amen_unmatched = amenities.resolve(pool, amen)
    codes = reviews.available_codes()
    if review_demo is not None and codes and review_demo not in codes:
        raise ValueError(f'評論示範沒有「{review_demo}」。可選:' + '、'.join(codes))
    t1 = peers.find_peers(pool, nb, bedrooms, acc, amen, lat, lon, top_n)
    gid = t1['group_ids']
    mp = pricing.model_price(nb, bedrooms, acc, beds, baths, amen, lat, lon)
    t2 = pricing.price_position(pool, gid, price, mp['price'])
    t2['model'] = mp
    t3 = amenities.amenity_gaps(pool, gid, amen, threshold)
    use_price = price if price is not None else mp['price']
    t6 = income.income_for_group(pool, gid, use_price, annual_cost)
    t6['price_source'] = '你打算開的價' if price is not None else '模型參考價'
    t7 = season.season_reference(gid, pool, year)
    if not t7['holidays']['items']:
        t7['holidays_prev'] = season.holidays(year - 1)
    return {'input': {'nb': nb, 'bedrooms': bedrooms, 'acc': acc, 'beds': beds, 'baths': baths,
                      'amen': sorted(amen), 'amen_unmatched': amen_unmatched, 'price': price, 'annual_cost': annual_cost, 'year': year,
                      'threshold_pct': round(100 * threshold, 1)},
            'T1': t1, 'T2': t2, 'T3': t3, 'T6': t6, 'T7': t7,
            'fallback': t1['fallback'], 'review_demo': review_demo,
            'T4': {'status': '示範' if codes and review_demo else '尚未接上'},
            'T5': {'status': '示範' if codes and review_demo else '尚未接上'}}


def summary_text(r):
    i, t1, t2, t3, t6, t7 = r['input'], r['T1'], r['T2'], r['T3'], r['T6'], r['T7']
    lines = []
    if i['amen_unmatched']:
        lines.append('【注意】這幾項設施對不到資料裡的任何設施名稱,沒有算進去:' + '、'.join(i['amen_unmatched'])
                     + '(請用資料裡的英文名稱,不分大小寫)')
    if r['fallback']:
        lines.append('【小樣本】' + FALLBACK_WARN)
    lines += [f"輸入:{i['nb']} 區、整套、{i['bedrooms']} 臥室、可住 {i['acc']} 人、{i['beds']:g} 床、{i['baths']:g} 浴;設施 {', '.join(i['amen'])}",
             f"T1 同類:{t1['level']},共 {t1['group_n']:,} 間;列出最像的 {len(t1['top'])} 間",
             f"T2 同類掛牌價 25/50/75 分位 = {t2['p25']} / {t2['p50']} / {t2['p75']} 澳元/晚;模型參考價 {t2['model']['price']}(落在同類第 {t2['ref_pct']:.0f} 百分位)"]
    if 'my_pct' in t2:
        lines.append(f"    你打算開 {t2['my_price']:g} → 同類第 {t2['my_pct']:.0f} 百分位")
    lines.append(f"T3 同類普及率 ≥ {t3['threshold_pct']:g}% 而你沒有的設施 {len(t3['gaps'])} 項:"
                 + '、'.join(f"{g['amenity']}({g['pct']}%)" for g in t3['gaps'][:6]) + (' …' if len(t3['gaps']) > 6 else ''))
    lines.append(f"T6 年收入(估算,未扣稅;每晚 {t6['price']:g},{t6['price_source']};年成本 {i['annual_cost']:g};"
                 f"同類 {t6['n_total']:,} 間裡有 {t6['n_zero']:,} 間估計 0 晚,已排除):")
    for x in t6['rows']:
        lines.append(f"    {x['level']}:{x['nights']:g} 晚{'(原 ' + format(x['nights_raw'], 'g') + ',封頂 180)' if x['capped'] else ''}"
                     f" × 服務費 {x['fee_name']} → 約 {x['income']:,.0f} 澳元/年(稅、清潔、水電等沒填的成本還沒扣)")
    ip, ia = t7['index_peers'], t7['index_all']
    lines.append(f"T7 評論月份指數(同類中有評論的 {ip['n_listings']} 間):11 月 {ip['index'][11]}、5 月 {ip['index'][5]};"
                 f"全部可比房源 6,639 間:11 月 {ia['index'][11]}(與之前 135.5 差 {ia['nov_vs_prev']:+})、5 月 {ia['index'][5]}(與之前 75.3 差 {ia['may_vs_prev']:+})")
    lines.append(f"    假期:{t7['holidays']['note']};日曆不可訂比例 " +
                 '、'.join(f"{m['ym']} {m['pct']}%" for m in t7['calendar']['months'][:3]) + ' …')
    if r['T4']['status'] == '示範':
        lines.append(f"T4、T5:示範(不是你輸入的那間房),已讀過評論的 10 間房之一「{r['review_demo']}」;詳見頁面")
    else:
        lines.append('T4 評論方面分析、T5 改進優先級:尚未接上')
    return '\n'.join(lines)


# ---------------- HTML ----------------
CSS = """
body{font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif;max-width:980px;margin:16px auto;padding:0 14px;color:#222;font-size:14px;line-height:1.5}
h1{font-size:20px;margin:6px 0} h2{font-size:16px;margin:18px 0 6px;border-left:4px solid #2b6cb0;padding-left:8px}
.warn{background:#fff4e5;border:1px solid #f0b86e;padding:8px 12px;border-radius:6px;font-weight:bold}
.pending{background:#f2f2f2;border:1px dashed #999;padding:8px 12px;border-radius:6px;color:#555}
table{border-collapse:collapse;margin:4px 0;font-size:13px} td,th{border:1px solid #ccc;padding:3px 7px;text-align:left}
th{background:#eef3f9} .num{text-align:right} .say{color:#555;font-size:13px}
.demo{background:#e8f1ff;border:2px solid #2b6cb0;padding:8px 12px;border-radius:6px;font-weight:bold;font-size:15px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px} .tag{color:#a33;font-weight:bold}
"""


def _tbl(head, rows, num_cols=()):
    h = ''.join(f'<th>{escape(str(x))}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td class="{"num" if j in num_cols else ""}">{escape(str(c))}</td>'
                                 for j, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<table><tr>{h}</tr>{b}</table>'


def _demo_banner(code):
    return (f'<div class="demo">這是示範,不是你輸入的那間房。新上架的房子還沒有評論。'
            f'這裡拿已經讀過評論的 10 間房之一(代號 {escape(code)})來示範:讀完它最近 30 條評論之後,這一區會長什麼樣子。</div>')


def _t4_t5(r, public):
    """回傳 T4、T5 兩段 HTML。"""
    d = reviews.load_demo(r['review_demo'], public) if r.get('review_demo') else None
    if d is None:
        return ['<h2>T4 評論方面分析</h2><div class="pending"><span class="tag">尚未接上。</span>'
                '找不到評論示範資料(review_analysis 的彙總檔),所以這裡沒有內容。</div>',
                '<h2>T5 改進優先級與避坑清單</h2><div class="pending"><span class="tag">尚未接上。</span>'
                '找不到評論示範資料,所以這裡沒有內容。</div>']
    e = escape
    ban = _demo_banner(d['code'])
    loc = ''
    if d['local']:
        loc = (f'<p class="say">(本機版才有)這間示範房:{e(d["local"]["nb"])} 區、{d["local"]["bedrooms"]} 臥室、'
               f'Airbnb 總評分 {d["local"]["rating"]:g}。</p>')
    t4 = ['<h2>T4 評論方面分析(示範)</h2>', ban, loc,
          f'<p class="say">下表是示範房 {e(d["code"])} 的 {d["n_reviews"]} 條評論,分成 7 個方面。'
          '一條評論可以同時提到好幾個方面;「有抱怨的比例」= (負評 + 有好有壞)÷ 有提到的條數。</p>',
          _tbl(['方面', '有提到幾條', '好評', '負評', '有好有壞', '有抱怨的比例', '白話'],
               [[a['aspect'], a['mentions'], a['pos'], a['neg'], a['mixed'],
                 f"{a['complaint_pct']:.1f}%" if a['mentions'] else '—', a['plain']] for a in d['aspects']], (1, 2, 3, 4, 5))]
    t5 = ['<h2>T5 改進優先級(示範)</h2>', ban,
          f'<p class="say">排序規則(暫定):{e(d["rule"])}</p>']
    if d['priorities']:
        t5.append(_tbl(['順位', '方面', '有抱怨的比例', '有提到幾條', '白話'],
                       [[k + 1, x['aspect'], f"{x['complaint_pct']:.1f}%", x['mentions'], x['plain']]
                        for k, x in enumerate(d['priorities'])], (0, 2, 3)))
    else:
        t5.append(f'<p><b>{e(d["empty_text"])}</b></p>')
    t5.append(f'<p class="say">限制:① 只有 {d["n_listings"]} 間房、每間 {d["per_listing"]} 條評論,不是全部房源;② 是一個 AI(' + e(d['reader']) +
              ')讀的,還沒有人拿人工答案對過;③ 上面的排序規則是暫定的,還沒定案;④ 這是示範房的評論,不代表你輸入的那間房。</p>')
    return t4 + t5


def to_html(r, public=True):
    i, t1, t2, t3, t6, t7 = r['input'], r['T1'], r['T2'], r['T3'], r['T6'], r['T7']
    e = escape
    fb = f'<p class="warn">{FALLBACK_WARN}</p>' if r['fallback'] else ''
    out = [f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><title>民宿營運助手 原型結果</title><style>{CSS}</style></head><body>',
           '<div class="warn">這是原型的計算結果,價格是掛牌價,收入是估算。</div>',
           f'<h1>雪梨 Airbnb 民宿營運助手:一間房的參考頁{"(公開版)" if public else "(本機版,含房源 id,不外傳)"}</h1>',
           '<p class="say">資料:Inside Airbnb 雪梨 2026-09-16 期快照;比較的範圍是「整套、1–2 臥、可住 2–4 人、最少 1–7 晚、有掛牌價」的 6,639 間。'
           '掛牌價是房東在網站上標的價,不是實際成交價。</p>',
           '<h2>輸入的房子</h2>',
           f'<p>{e(i["nb"])} 區、整套、{i["bedrooms"]} 臥室、可住 {i["acc"]} 人、{i["beds"]:g} 張床、{i["baths"]:g} 間浴室;'
           f'已有設施:{e("、".join(i["amen"]))};打算開的價:{"未填" if i["price"] is None else format(i["price"], "g") + " 澳元/晚"};'
           f'年成本:{i["annual_cost"]:g} 澳元。</p>']
    if i['amen_unmatched']:
        out.append('<p class="warn">這幾項設施對不到資料裡的任何設施名稱,<u>沒有算進去</u>:' + e('、'.join(i['amen_unmatched'])) +
                   '。請用資料裡的英文名稱(不分大小寫)。</p>')

    # T1
    out.append('<h2>T1 找同類</h2>')
    out.append(f'<p><b>{t1["group_n"]:,} 間</b> <span class="say">← 同類有這麼多間。規則:{e(t1["level"])}。'
               f'下面列出其中最像的 {len(t1["top"])} 間:先比可住人數差多少,再比設施重疊多少(相似度 0–1,越大越像)。找同類時完全不看價格。</span></p>')
    if public:
        rows = [[k + 1, p['nb'], p['bedrooms'], p['acc'], p['amen_n'], f"{p['jaccard']:.2f}"] for k, p in enumerate(t1['top'])]
        out.append(_tbl(['#', '區', '臥室', '可住人數', '設施數', '設施相似度'], rows, (0, 2, 3, 4, 5)))
    else:
        rows = [[k + 1, p['id'], p['nb'], p['bedrooms'], p['acc'], p['amen_n'], f"{p['jaccard']:.2f}", p['reason']]
                for k, p in enumerate(t1['top'])]
        out.append(_tbl(['#', '房源 id', '區', '臥室', '可住人數', '設施數', '設施相似度', '匹配理由'], rows, (0, 3, 4, 5, 6)))
    out.append('<p class="say">相似度只看設施清單重疊的比例;設施數少的房源(例如只填 3 項)跟大部分房源的相似度都會偏低,這是正常的。</p>')

    # T2
    out.append('<h2>T2 價格位置與參考價(掛牌價,澳元/晚)</h2>' + fb)
    rows = [['同類第 25 百分位', t2['p25'], '同類裡有四分之一的房源標價比這個低'],
            ['同類中位數', t2['p50'], '同類標價的正中間'],
            ['同類第 75 百分位', t2['p75'], '同類裡有四分之一的房源標價比這個高'],
            ['模型參考價', t2['model']['price'], f"用 {t2['model']['model_name']} 模型、只看上架前就知道的條件猜的標價;落在同類第 {t2['ref_pct']:.0f} 百分位"]]
    if 'my_pct' in t2:
        rows.append(['你打算開的價', f"{t2['my_price']:g}", f"在同類裡排第 {t2['my_pct']:.0f} 百分位(同類有 {t2['my_pct']:.0f}% 標價不高於它)"])
    out.append(_tbl(['項目', '數字', '白話'], rows, (1,)))
    if t2['model']['amen_not_in_model']:
        out.append(f'<p class="say">注意:這些設施不在模型的 40 項名單裡,只算進設施數:{e("、".join(t2["model"]["amen_not_in_model"]))}。</p>')
    out.append('<p class="say">模型在沒看過的測試房源上,一半的誤差在 18.4% 以內(誤差中位數);參考價是「同條件的房源大概標多少」,不是定價建議。</p>')

    # T3
    out.append('<h2>T3 設施差距</h2>' + fb)
    out.append(f'<p>同類中至少 {t3["threshold_pct"]:g}% 的房源有、而你的清單裡沒有的設施:<b>{len(t3["gaps"])} 項</b>'
               f'<span class="say">(門檻 {t3["threshold_pct"]:g}% 是暫定值;列出來只是「需要評估的改進機會」,可能只是你沒勾,不代表一定要買)</span></p>')
    out.append(_tbl(['設施(資料裡的英文名)', '同類普及率', '白話'],
                    [[g['amenity'], f"{g['pct']}%", f"同類每 100 間約 {g['pct']:.0f} 間有"] for g in t3['gaps']], (1,)))
    out.append('<p class="say">你已有的設施在同類的普及率:' +
               e('、'.join(f"{h['amenity']} {h['pct']}%" for h in t3['have'])) + '。</p>')

    # T4 / T5
    out.extend(_t4_t5(r, public))

    # T6
    out.append('<h2>T6 年收入情景(估算,未扣稅)</h2>' + fb)
    out.append(f'<p class="say">{e(t6["note"])} 公式:每晚價格 × 入住晚數 ×(1 − 平台服務費率)− 你填的年成本。'
               f'每晚價格用{e(t6["price_source"])} {t6["price"]:g} 澳元。</p>')
    out.append(f'<p class="say">入住晚數:同類 {t6["n_total"]:,} 間裡有 {t6["n_zero"]:,} 間估計 0 晚,已排除(視為沒在營業);'
               f'剩下 {t6["n_with_occ"]:,} 間取第 25/50/75 百分位當低/中/高,每一個最多算 {t6["cap"]} 晚'
               f'(依報告引用的規定:大雪梨非房東同住的整套房,每年最多出租 180 晚)。所以低/中/高是「有在營業的同類」的低中高。</p>')
    rows = [[x['level'], f"{x['nights']:g}" + (f"(原 {x['nights_raw']:g},封頂)" if x['capped'] else ''), x['fee_name'],
             f"{x['gross']:,.0f}", f"{x['fee']:,.0f}", f"{x['cost']:,.0f}", f"{x['income']:,.0f}",
             f"一年約住 {x['nights']:g} 晚、扣掉平台服務費和你填的成本後約剩 {x['income']:,.0f} 澳元;稅、清潔、水電等你沒填的成本都還沒扣"] for x in t6['rows']]
    out.append(_tbl(['情景', '入住晚數', '服務費率', '總房費', '服務費', '年成本', '年收入(估算,未扣稅)', '白話'], rows, (3, 4, 5, 6)))

    # T7
    ip, ia, cal, hol = t7['index_peers'], t7['index_all'], t7['calendar'], t7['holidays']
    out.append('<h2>T7 淡旺季參考(只是參考,不預測價格)</h2>' + fb)
    out.append('<p class="say">① 評論月份指數:用 2024、2025 兩年的評論日期,算每個月評論占全年的比例,100 = 一般月份,'
               '120 = 比一般月份多兩成。評論是住完才寫,高峰會比入住晚一點;評論數不是訂單數。</p>')
    rows = [[MONTHS_ZH[m - 1], ip['index'][m], ia['index'][m]] for m in range(1, 13)]
    out.append('<div class="grid"><div>' +
               _tbl(['月份', f'同類(有評論的 {ip["n_listings"]} 間)', '全部可比房源(6,639 間)'], rows, (1, 2)) + '</div><div>')
    out.append(f'<p class="say">同類用了 {ip["n_reviews"]:,} 則評論;全部可比房源用了 {ia["n_reviews"]:,} 則(其中 2024–2025 年有評論的房源 {ia["n_listings"]:,} 間)。'
               f'之前的結果(評論檔全部房源)是 11 月 135.5、5 月 75.3;這裡全部可比房源是 11 月 {ia["index"][11]}'
               f'(差 {ia["nov_vs_prev"]:+})、5 月 {ia["index"][5]}(差 {ia["may_vs_prev"]:+})。差別可能是因為範圍不同(未驗證):之前算全部房源,這裡只算可比的整套 1–2 臥。</p>')
    out.append(f'<p>② 公眾假期({hol["year"]}):{e(hol["note"])}</p>')
    hp = t7.get('holidays_prev')
    if hp and hp['items']:
        out.append(f'<p class="say">先列 {hp["year"]} 年 NSW 公眾假期當參考(日期每年會變):' +
                   e('、'.join(f"{x['date'][5:]} {x['name']}" for x in hp['items'])) + '</p>')
    elif hol['items']:
        out.append('<p class="say">' + e('、'.join(f"{x['date'][5:]} {x['name']}" for x in hol['items'])) + '</p>')
    out.append('</div></div>')
    out.append(f'<p>③ 日曆:同類房源未來 12 個月每月「不可訂」的比例。<span class="say">{e(cal["note"])}</span></p>')
    out.append(_tbl(['月份'] + [m['ym'] for m in cal['months']],
                    [['不可訂比例'] + [('—' if m['pct'] is None else f"{m['pct']}%") for m in cal['months']]]))
    out.append('<p class="say">比例越高,代表那個月同類房源越多天已經不能訂(可能被訂走,也可能房東自己關)。越遠的月份,可能有房東還沒開放日曆或先關著,數字要打折看。</p>')
    out.append('<hr><p class="say">產生方式:Innovation Studio/app_prototype/demo.py。資料是 2026-09 的快照,只涵蓋整套 1–2 臥。</p></body></html>')
    return '\n'.join(out)
