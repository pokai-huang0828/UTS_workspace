"""raw → processed:篩選、清洗、拿掉極端值,印出每一步剩幾列。
執行:python "Innovation Studio/model_training/src/01_build_dataset.py"
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

EXPECT = {'main_rows': 20833, 'main_scope': 7565, 'main_scope_price': 6639, 'main_model': 6615,
          'prev_model': 6747, 'timeout_test': 821}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def build(period):
    raw = C.load_raw(period)
    sc = C.scope(raw)
    d = C.prep(sc)
    dm = d[d.price_num <= C.EXTREME_CAP].reset_index(drop=True)
    ext = d[d.price_num > C.EXTREME_CAP].reset_index(drop=True)
    print(f'[{period}] 原始 {len(raw):,} 列 → 篩選(整套/臥室1-2/2-4人/最少1-7晚){len(sc):,} → 有價 {len(d):,} '
          f'→ 去掉每晚>{C.EXTREME_CAP} 的 {len(ext)} 列 → {len(dm):,}')
    return raw, d, dm, ext


def main():
    C.PROC.mkdir(parents=True, exist_ok=True)
    for p in sorted(C.RAW.glob('*.csv.gz')):
        print(f'raw {p.name} sha256={sha(p)}')
    raw9, d9, dm9, ext9 = build(C.MAIN)
    assert len(raw9) == EXPECT['main_rows'], len(raw9)
    assert len(d9) == EXPECT['main_scope_price'], f'篩選且有價應為 6,639,實得 {len(d9)}'
    assert len(dm9) == EXPECT['main_model'], f'去極端後應為 6,615,實得 {len(dm9)}'
    raw6, d6, dm6, _ = build(C.PREV)
    assert len(dm6) == EXPECT['prev_model'], f'6 月去極端後應為 6,747,實得 {len(dm6)}'
    unseen = dm9[~dm9.id.isin(set(raw6.id))].reset_index(drop=True)
    print(f'[時間外] 9 月 {len(dm9):,} 間中 id 沒出現在 6 月整期 listings({len(raw6):,} 列)的:{len(unseen):,}')
    assert len(unseen) == EXPECT['timeout_test'], f'時間外測試應為 821,實得 {len(unseen)}'

    out = {'train_table_2026-09.csv': dm9, 'extremes_dropped_24.csv': ext9,
           'timeout_train_2026-06.csv': dm6, 'timeout_test_2026-09_new.csv': unseen}
    for name, df in out.items():
        df[C.PROC_COLS].to_csv(C.PROC / name, index=False, encoding='utf-8')
        print(f'processed {name}: {len(df):,} 列 × {len(C.PROC_COLS)} 欄, 房東 {df.host_id.nunique():,} 位, '
              f'sha256={sha(C.PROC / name)}')
    print('極端值 24 列的價格範圍:', ext9.price_num.min(), '–', ext9.price_num.max())
    cnt = C.amen_counts(dm9.amen)
    print('(僅供參考,全 6,615 間)出現最多的 40 項設施:', list(cnt.index[:40]))
    print('欄位:', C.PROC_COLS)


if __name__ == '__main__':
    main()
