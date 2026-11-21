"""抽 50 條評論當試跑樣本。規則寫死、種子固定,可重跑。
來源:scratchpad/insideairbnb_sydney/2026-09-16/data/reviews.csv.gz(唯讀,不複製:230 MB)
範圍:只要「可比房源」6,639 間的評論(id 取自 model_training/data/processed)。
"""
import json, re, hashlib
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parents[1]
REV = ROOT / 'scratchpad/insideairbnb_sydney/2026-09-16/data/reviews.csv.gz'
MT = ROOT / 'Innovation Studio/model_training/data'
SEED, N_RANDOM, N_LOW = 42, 35, 15
DATE_FROM, LEN_MIN, LEN_MAX = '2025-01-01', 150, 1200

tt = pd.read_csv(MT / 'processed/train_table_2026-09.csv', dtype=str, keep_default_na=False)
ex = pd.read_csv(MT / 'processed/extremes_dropped_24.csv', dtype=str, keep_default_na=False)
idcol = 'id' if 'id' in tt.columns else tt.columns[0]
scope_ids = set(tt[idcol]) | set(ex[idcol])
assert len(scope_ids) == 6639, len(scope_ids)

ls = pd.read_csv(MT / 'raw/listings_2026-09-16.csv.gz', dtype=str, keep_default_na=False, usecols=['id', 'review_scores_rating'])
ls = ls[ls.id.isin(scope_ids)].copy()
ls['rating'] = pd.to_numeric(ls.review_scores_rating, errors='coerce')
p10 = ls.rating.quantile(0.10)
low_ids = set(ls[ls.rating <= p10].id)

rv = pd.read_csv(REV, dtype=str, keep_default_na=False, usecols=['listing_id', 'id', 'date', 'comments'])  # 不讀評論者姓名
stats = {'全部評論': len(rv)}
rv = rv[rv.listing_id.isin(scope_ids)].copy(); stats['可比房源的評論'] = len(rv)
rv = rv[rv.date >= DATE_FROM].copy(); stats[f'{DATE_FROM} 以後'] = len(rv)
rv['text'] = rv.comments.str.replace(r'<br\s*/?>', ' ', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
rv['n_char'] = rv.text.str.len()
letters = rv.text.str.count(r'[^\W\d_]')
ascii_letters = rv.text.str.count(r'[A-Za-z]')
rv['is_en'] = (letters > 0) & (ascii_letters / letters.clip(lower=1) >= 0.9) & (rv.text.str.split().str.len() >= 15)
stats['其中:空白'] = int((rv.n_char == 0).sum())
stats['其中:看起來是英文且至少 15 個字'] = int(rv.is_en.sum())
stats['長度分位(字元)'] = {k: int(v) for k, v in rv.n_char.quantile([.1, .25, .5, .75, .9]).items()}
stats[f'短於 {LEN_MIN} 字元的比例%'] = round(float((rv.n_char < LEN_MIN).mean() * 100), 1)
stats[f'長於 {LEN_MAX} 字元的比例%'] = round(float((rv.n_char > LEN_MAX).mean() * 100), 1)
el = rv[rv.is_en & rv.n_char.between(LEN_MIN, LEN_MAX)].copy()
stats['符合抽樣條件(英文、150–1,200 字元)'] = len(el)
stats['符合條件占 2025 以後評論的比例%'] = round(len(el) / max(stats[f'{DATE_FROM} 以後'], 1) * 100, 1)
stats['評分最低一成的門檻'] = float(p10)
low = el[el.listing_id.isin(low_ids)]
stats['其中來自評分最低一成房源'] = len(low)
s_low = low.sample(n=N_LOW, random_state=SEED)
s_rand = el[~el.id.isin(s_low.id)].sample(n=N_RANDOM, random_state=SEED)
s_low = s_low.assign(stratum='low_rated'); s_rand = s_rand.assign(stratum='random')
out = pd.concat([s_rand, s_low]).sample(frac=1, random_state=SEED).reset_index(drop=True)
out.insert(0, 'rid', [f'R{i+1:02d}' for i in range(len(out))])
out = out[['rid', 'id', 'listing_id', 'date', 'stratum', 'n_char', 'text']].rename(columns={'id': 'review_id'})
out.to_csv(BASE / 'data/sample_50.csv', index=False, encoding='utf-8')
stats['抽出'] = {'隨機': N_RANDOM, '評分最低一成的房源': N_LOW, '合計': len(out), '不同房源數': int(out.listing_id.nunique())}
stats['樣本長度中位數(字元)'] = int(out.n_char.median())
stats['sample_50.csv sha256'] = hashlib.sha256((BASE / 'data/sample_50.csv').read_bytes()).hexdigest()
(BASE / 'data/sample_stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(stats, ensure_ascii=False, indent=1))
