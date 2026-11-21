"""IS-1121-REPORT-FIG-A:AT2 報告「數據與資源」用的相關係數矩陣熱力圖 + 掛牌價分布圖。
可重跑:python syd_r_report_figures.py
資料(唯讀):scratchpad/insideairbnb_sydney/2026-09-16/data/listings.csv.gz
樣本 = 可比房源 6,639 套;篩選邏輯照抄 syd_b_positioning.py:
  scope() 第 68–72 行(整套、bedrooms 為 '1'/'2'、accommodates 2–4、minimum_nights 1–7)、
  parse_amen() 第 85–89 行(設施 JSON 解析、去重去空白)、prep() 第 99–100 行(price 非空、去 $ 與 ,)。
輸出:notes/raw/syd_r_report_figures_2026-11-21.{json,md}、notes/figures/report_fig_{corr_heatmap,price_dist}_2026-11-21.png
圖上文字為簡體中文(要放進簡體報告)。
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'scratchpad/insideairbnb_sydney'
MAIN = '2026-09-16'
OUT_JSON = ROOT / 'Innovation Studio/notes/raw/syd_r_report_figures_2026-11-21.json'
OUT_MD = ROOT / 'Innovation Studio/notes/raw/syd_r_report_figures_2026-11-21.md'
FIG = ROOT / 'Innovation Studio/notes/figures'
FIG_HEAT = FIG / 'report_fig_corr_heatmap_2026-11-21.png'
FIG_DIST = FIG / 'report_fig_price_dist_2026-11-21.png'
EXPECT_N = 6639

VARS = ['price', 'bedrooms', 'accommodates', 'amenities_n', 'rating', 'accuracy', 'cleanliness',
        'checkin', 'communication', 'location', 'value']
LABEL_ZH = ['挂牌价', '卧室数', '可住人数', '设施数', '总评分', '描述相符', '清洁', '入住', '沟通', '位置', '性价比']
LABEL_TW = ['掛牌價', '臥室數', '可住人數', '設施數', '總評分', '描述相符', '清潔', '入住', '溝通', '位置', '性價比']
REVIEW_COLS = {'rating': 'review_scores_rating', 'accuracy': 'review_scores_accuracy',
               'cleanliness': 'review_scores_cleanliness', 'checkin': 'review_scores_checkin',
               'communication': 'review_scores_communication', 'location': 'review_scores_location',
               'value': 'review_scores_value'}
USECOLS = ['room_type', 'bedrooms', 'accommodates', 'minimum_nights', 'price', 'amenities'] + list(REVIEW_COLS.values())


# ---------------- 樣本(邏輯照抄 syd_b_positioning.py) ----------------
def parse_amen(s):  # syd_b 第 85–89 行
    try:
        return frozenset(a.strip() for a in json.loads(s) if isinstance(a, str) and a.strip())
    except (ValueError, TypeError):
        return frozenset()


def scope(df):  # syd_b 第 68–72 行
    acc = pd.to_numeric(df.accommodates.where(df.accommodates.str.isdigit()), errors='coerce')
    mn = pd.to_numeric(df.minimum_nights.where(df.minimum_nights.str.isdigit()), errors='coerce')
    m = (df.room_type == 'Entire home/apt') & df.bedrooms.isin(['1', '2']) & acc.between(2, 4) & mn.between(1, 7)
    return df[m].copy()


def build():
    raw = pd.read_csv(DATA / MAIN / 'data/listings.csv.gz', dtype=str, keep_default_na=False, usecols=USECOLS)
    assert len(raw) == 20833, f'原始列數 {len(raw)} != 20833'
    d = scope(raw)
    d = d[d.price != ''].copy()                       # syd_b prep() 第 99 行
    assert len(d) == EXPECT_N, f'篩完 {len(d)} 列,不是 {EXPECT_N}:停下來回報,不調規則'
    out = pd.DataFrame(index=d.index)
    out['price'] = d.price.str.replace(r'[,$\s]', '', regex=True).astype(float)   # syd_b prep() 第 100 行
    out['bedrooms'] = d.bedrooms.astype(int)
    out['accommodates'] = d.accommodates.astype(int)
    out['amenities_n'] = d.amenities.map(parse_amen).map(len)
    for k, c in REVIEW_COLS.items():
        out[k] = pd.to_numeric(d[c].where(d[c] != ''), errors='coerce')   # 空字串 = 缺值,不補
    return out[VARS].reset_index(drop=True)


def nested(m):
    return {a: {b: float(m.loc[a, b]) for b in m.columns} for a in m.index}


def stats(df):
    desc = {}
    for v in VARS:
        s = df[v]
        desc[v] = {'n': int(s.notna().sum()), 'missing': int(s.isna().sum()), 'mean': float(s.mean()),
                   'std': float(s.std(ddof=1)), 'min': float(s.min()), 'p25': float(s.quantile(0.25)),
                   'median': float(s.median()), 'p75': float(s.quantile(0.75)), 'max': float(s.max()),
                   'skew': float(s.skew())}
    sp = df.corr(method='spearman')
    dl = df.copy()
    dl['price'] = np.log(dl['price'])
    pe = dl.corr(method='pearson')
    ok = df.notna().astype(int)
    pn = ok.T @ ok
    pbb = {}
    for b in (1, 2):
        p = df.loc[df.bedrooms == b, 'price']
        pbb[str(b)] = {'n': int(len(p)), 'median': float(p.median()), 'p25': float(p.quantile(0.25)),
                       'p75': float(p.quantile(0.75))}
    return {'n': int(len(df)), 'vars': VARS, 'desc': desc, 'spearman': nested(sp), 'pearson_logprice': nested(pe),
            'pair_n': {a: {b: int(pn.loc[a, b]) for b in VARS} for a in VARS}, 'price_by_bedroom': pbb,
            'price_gt_1000': int((df.price > 1000).sum()), 'price_gt_2000': int((df.price > 2000).sum())}


# ---------------- 圖 ----------------
def setup_font():
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in ('Microsoft YaHei', 'SimHei'):
        if name in have:
            plt.rcParams['font.sans-serif'] = [name]
            break
    else:
        raise SystemExit('找不到 Microsoft YaHei / SimHei')
    plt.rcParams.update({'font.family': 'sans-serif', 'axes.unicode_minus': False, 'figure.facecolor': 'white',
                         'savefig.facecolor': 'white'})


def fig_heat(res):
    m = np.array([[res['spearman'][a][b] for b in VARS] for a in VARS])
    fig, ax = plt.subplots(figsize=(8, 7.5))
    im = ax.imshow(m, cmap='RdBu_r', vmin=-1, vmax=1)
    n = len(VARS)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(LABEL_ZH, rotation=45, ha='right', rotation_mode='anchor', fontsize=11)
    ax.set_yticklabels(LABEL_ZH, fontsize=11)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{m[i, j]:.2f}', ha='center', va='center', fontsize=8.5,
                    color='white' if abs(m[i, j]) > 0.6 else '#222222')
    ax.set_xticks(np.arange(-.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=1)
    ax.tick_params(which='both', length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, shrink=0.78, pad=0.025)
    cb.set_label('Spearman ρ', fontsize=10)
    cb.outline.set_visible(False)
    fig.text(0.5, 0.025, 'Spearman 等级相关；样本为 2026 年 9 月筛选后的 6,639 套房源；评分类变量按成对有效样本计算',
             ha='center', va='bottom', fontsize=9, color='#444444')
    fig.subplots_adjust(left=0.12, right=0.97, top=0.99, bottom=0.145)
    fig.savefig(FIG_HEAT, dpi=300)
    plt.close(fig)


def fig_dist(df, res):
    fig, ax = plt.subplots(figsize=(8, 5.2))
    bins = np.arange(0, 1001, 25)
    spec = [(1, '#1f5fa8', 'right'), (2, '#e07b1a', 'left')]
    ymax = 0
    for b, col, _ in spec:
        p = df.loc[df.bedrooms == b, 'price']
        cnt, _e, _p = ax.hist(p, bins=bins, color=col, alpha=0.55, label=f'{b} 卧室（n={len(p):,}）',
                              edgecolor='white', linewidth=0.5)
        ymax = max(ymax, cnt.max())
    ax.set_ylim(0, ymax * 1.18)
    for b, col, ha in spec:
        med = res['price_by_bedroom'][str(b)]['median']
        ax.axvline(med, color=col, linestyle='--', linewidth=1.8)
        ax.text(med + (-6 if ha == 'right' else 6), ymax * 1.12, f'中位数 {med:.0f}', color=col, ha=ha, va='top',
                fontsize=11, fontweight='bold')
    ax.set_xlim(0, 1000)
    ax.set_xticks(range(0, 1001, 100))
    ax.set_xlabel('挂牌价（澳元/晚）', fontsize=12)
    ax.set_ylabel('房源数', fontsize=12)
    ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.86), frameon=False, fontsize=11)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', color='#e5e5e5', linewidth=0.8)
    ax.set_axisbelow(True)
    fig.text(0.5, 0.015, f'另有 {res["price_gt_1000"]:,} 套超过 1,000 澳元/晚未显示', ha='center', va='bottom',
             fontsize=9, color='#444444')
    fig.subplots_adjust(left=0.09, right=0.97, top=0.97, bottom=0.17)
    fig.savefig(FIG_DIST, dpi=300)
    plt.close(fig)


# ---------------- md ----------------
def write_md(res):
    sp, pe, d = res['spearman'], res['pearson_logprice'], res['desc']
    zh = dict(zip(VARS, LABEL_TW))
    pairs = sorted(((sp[a][b], a, b) for i, a in enumerate(VARS) for b in VARS[i + 1:]), key=lambda t: -abs(t[0]))
    top3 = pairs[:3]
    others = [v for v in VARS if v != 'price']
    price_sp = {v: sp['price'][v] for v in others}
    rev7 = [v for v in VARS[4:]]
    pr_rev = [sp['price'][v] for v in rev7]
    rr = [(sp[a][b], a, b) for i, a in enumerate(rev7) for b in rev7[i + 1:]]
    rr_min, rr_max = min(rr), max(rr)
    miss = {v: d[v]['missing'] for v in rev7}
    pbb = res['price_by_bedroom']
    L = []
    L += ['# 雪梨可比房源:相關係數矩陣與掛牌價分布(IS-1121-REPORT-FIG-A)', '',
          '## 1. 怎麼跑、樣本與規則', '',
          '- 重跑:`python "Innovation Studio/analysis/sydney/syd_r_report_figures.py"`(repo 根目錄下執行;不加 `-I`)。',
          '- 資料(唯讀):`scratchpad/insideairbnb_sydney/2026-09-16/data/listings.csv.gz`,20,833 列,`dtype=str, keep_default_na=False` 讀入。',
          '- 樣本規則(照抄 `syd_b_positioning.py` 的 `scope()` 第 68–72 行與 `parse_amen()` 第 85–89 行):'
          '`room_type == Entire home/apt`、`bedrooms` 為 1 或 2、`accommodates` 2–4、`minimum_nights` 1–7、`price` 非空。'
          f'篩完 {res["n"]:,} 列(程式內 assert 檢查為 6,639)。',
          '- 11 個變數:price(去 `$`、`,` 轉數字)、bedrooms、accommodates、amenities_n(設施 JSON 解析後去重去空白的個數)、'
          'rating / accuracy / cleanliness / checkin / communication / location / value(各 `review_scores_*`)。'
          '評分欄空字串視為缺值,不補。',
          '- 相關:Spearman(成對刪除缺值);JSON 內另附 price 取自然對數後的 Pearson(`pearson_logprice`)與每對的有效筆數(`pair_n`)。',
          '- 輸出:`notes/raw/syd_r_report_figures_2026-11-21.json`、`notes/figures/report_fig_corr_heatmap_2026-11-21.png`、'
          '`notes/figures/report_fig_price_dist_2026-11-21.png`。', '',
          '## 2. 描述統計(11 個變數)', '',
          '| 變數 | 中文 | 有效筆數 | 缺值 | 平均 | 標準差 | 最小 | P25 | 中位數 | P75 | 最大 | 偏態 |',
          '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for v in VARS:
        x = d[v]
        L.append(f'| {v} | {zh[v]} | {x["n"]:,} | {x["missing"]:,} | {x["mean"]:.2f} | {x["std"]:.2f} | {x["min"]:g} | '
                 f'{x["p25"]:.2f} | {x["median"]:.2f} | {x["p75"]:.2f} | {x["max"]:g} | {x["skew"]:.2f} |')
    L += ['', '## 3. Spearman 相關矩陣(兩位小數)', '',
          '| | ' + ' | '.join(VARS) + ' |', '|---|' + '---:|' * len(VARS)]
    for a in VARS:
        L.append(f'| **{a}** | ' + ' | '.join(f'{sp[a][b]:.2f}' for b in VARS) + ' |')
    L += ['', '## 4. 看得出什麼(只講數字顯示的事)', '']
    L.append('1. 相關最高的三對(依絕對值):' + ';'.join(f'{a}–{b} = {r:.2f}' for r, a, b in top3) + '。')
    L.append(f'2. 掛牌價與其他 10 個變數的 Spearman:' + '、'.join(f'{v} {price_sp[v]:.2f}' for v in others) + '。')
    L.append(f'3. 掛牌價與 7 個評分類變數的相關介於 {min(pr_rev):.2f} 到 {max(pr_rev):.2f};'
             f'與 accommodates {sp["price"]["accommodates"]:.2f}、bedrooms {sp["price"]["bedrooms"]:.2f}、'
             f'amenities_n {sp["price"]["amenities_n"]:.2f}。')
    L.append(f'4. 6 個分項評分(不含總評分)與總評分的相關介於 '
             f'{min(sp["rating"][v] for v in rev7[1:]):.2f} 到 {max(sp["rating"][v] for v in rev7[1:]):.2f};'
             f'7 個評分變數彼此的相關最低 {rr_min[0]:.2f}({rr_min[1]}–{rr_min[2]})、最高 {rr_max[0]:.2f}({rr_max[1]}–{rr_max[2]})。')
    L.append(f'5. 掛牌價偏態 {d["price"]["skew"]:.2f}(平均 {d["price"]["mean"]:.0f}、中位數 {d["price"]["median"]:.0f});'
             f'1 臥室中位數 {pbb["1"]["median"]:.0f}(n={pbb["1"]["n"]:,},P25–P75 為 {pbb["1"]["p25"]:g}–{pbb["1"]["p75"]:g}),'
             f'2 臥室中位數 {pbb["2"]["median"]:.0f}(n={pbb["2"]["n"]:,},P25–P75 為 {pbb["2"]["p25"]:g}–{pbb["2"]["p75"]:g});'
             f'超過 1,000 澳元的 {res["price_gt_1000"]:,} 套、超過 2,000 澳元的 {res["price_gt_2000"]:,} 套。')
    L.append(f'6. price 取自然對數後的 Pearson:與 bedrooms {pe["price"]["bedrooms"]:.2f}、accommodates {pe["price"]["accommodates"]:.2f}、'
             f'amenities_n {pe["price"]["amenities_n"]:.2f}、rating {pe["price"]["rating"]:.2f}(對照 Spearman 依序 '
             f'{sp["price"]["bedrooms"]:.2f}、{sp["price"]["accommodates"]:.2f}、{sp["price"]["amenities_n"]:.2f}、{sp["price"]["rating"]:.2f})。')
    L += ['', '## 5. 限制', '',
          '- 篩選把範圍壓窄:bedrooms 只有 1 和 2、accommodates 只有 2–4,所以這兩個變數的相關係數只反映這段範圍內的關係,不能外推到更大的房子。',
          f'- 評分擠在接近滿分:總評分中位數 {d["rating"]["median"]:.2f}、P25 {d["rating"]["p25"]:.2f}(滿分 5),分項評分也類似;'
          '變異小、並列值多,Spearman 係數對此類資料較敏感。',
          '- price 是掛牌價,不是成交價;沒有看到實際訂房價格。',
          f'- 評分缺值(沒有評論或沒有評分的房源):rating {miss["rating"]:,}、accuracy {miss["accuracy"]:,}、'
          f'cleanliness {miss["cleanliness"]:,}、checkin {miss["checkin"]:,}、communication {miss["communication"]:,}、'
          f'location {miss["location"]:,}、value {miss["value"]:,}(共 {res["n"]:,} 套);涉及評分的係數用的是成對有效樣本(筆數見 JSON `pair_n`),'
          '有評分的房源不一定等於全體房源的縮影。',
          '- 本表只描述相關,不含因果推論,也沒有做模型或分群。', '']
    OUT_MD.write_text('\n'.join(L), encoding='utf-8')


def main():
    setup_font()
    df = build()
    res = stats(df)
    OUT_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    FIG.mkdir(parents=True, exist_ok=True)
    fig_heat(res)
    fig_dist(df, res)
    write_md(res)
    sp = res['spearman']['price']
    print('n', res['n'], '| bed medians', {k: v['median'] for k, v in res['price_by_bedroom'].items()},
          '| amen median', res['desc']['amenities_n']['median'], '| >2000', res['price_gt_2000'],
          '| >1000', res['price_gt_1000'])
    print('price spearman', {k: round(v, 3) for k, v in sp.items() if k != 'price'})
    pairs = sorted(((res['spearman'][a][b], a, b) for i, a in enumerate(VARS) for b in VARS[i + 1:]),
                   key=lambda t: -abs(t[0]))[:3]
    print('top3', [(round(r, 3), a, b) for r, a, b in pairs])
    print('missing', {v: res['desc'][v]['missing'] for v in VARS[4:]})


if __name__ == '__main__':
    main()
