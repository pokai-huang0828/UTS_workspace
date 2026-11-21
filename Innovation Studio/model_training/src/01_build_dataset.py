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


def build_group(group):
    """新增兩群房源:只用 2026-09-16 期;每一步剩幾列都印出來。"""
    G = C.GROUPS[group]
    raw = C.load_raw(C.MAIN)
    print(f'[{group}] 原始 {len(raw):,} 列(sha256 {sha(C.RAW / f"listings_{C.MAIN}.csv.gz")[:16]}…)')
    if group == 'private_room':
        r1 = raw[raw.room_type == 'Private room']
        print(f'  步驟 1 room_type == Private room:{len(r1):,};其中 price 非空 {int((r1.price != "").sum()):,}(參考值 3,726)')
        acc = C._num(r1.accommodates)
        print(f'  步驟 2 accommodates 純數字且 1–4:{int(acc.between(1, 4).sum()):,}(非純數字 {int(acc.isna().sum())})')
        r2 = r1[acc.between(1, 4)]
        mn = C._num(r2.minimum_nights)
        print(f'  步驟 3 minimum_nights 純數字且 1–7:{int(mn.between(1, 7).sum()):,}(非純數字 {int(mn.isna().sum())})')
        sc = C.scope_private(raw)
        assert len(sc) == int(mn.between(1, 7).sum())
        print('  (參考)這一群的臥室數原始值:', dict(sc.bedrooms.replace('', '(空)').value_counts()))
        print(f'  (參考)bathrooms_text 含 shared 的比例:{100 * sc.bathrooms_text.str.lower().str.contains("shared").mean():.1f}%')
    else:
        r1 = raw[raw.room_type == 'Entire home/apt']
        print(f'  步驟 1 room_type == Entire home/apt:{len(r1):,}')
        sc = C.scope_entire_all(raw)
    d = C.prep(sc, group)
    print(f'  步驟 {"4" if group == "private_room" else "2"} price 非空:{len(d):,}'
          + ('(預期 13,899)' if group == 'entire_home_all' else ''))
    if group == 'entire_home_all':
        assert len(d) == 13899, len(d)
    print('  缺值補值:', C.LAST_FILLS, '| 缺值旗標加總 臥室', int(d.bed_missing.sum()), '可住人數', int(d.acc_missing.sum()),
          '最少晚數', int(d.min_missing.sum()))
    dm = d[d.price_num <= G['cap']].reset_index(drop=True)
    ext = d[d.price_num > G['cap']].reset_index(drop=True)
    print(f'  步驟 {"5" if group == "private_room" else "3"} 去掉每晚 > {G["cap"]:,} 的 {len(ext)} 列 → {len(dm):,}'
          f'(被去掉的價格範圍 {ext.price_num.min() if len(ext) else "無"} – {ext.price_num.max() if len(ext) else "無"})')
    # 是否在第一次訓練那 6,615 間之內(只用 id 對,不輸出 id 清單)
    base = C.prep(C.scope(raw))
    ids6615 = set(base[base.price_num <= C.EXTREME_CAP].id)
    assert len(ids6615) == EXPECT['main_model']
    for df in (dm, ext):
        df['in_run01'] = df.id.isin(ids6615).astype(int)
    print(f'  其中屬於第一次訓練的 6,615 間:{int(dm.in_run01.sum()):,};在 6,615 之外:{int((dm.in_run01 == 0).sum()):,}')
    if group == 'entire_home_all':
        assert int(dm.in_run01.sum()) == 6615
    print(f'  模型用表:{len(dm):,} 列、房東 {dm.host_id.nunique():,} 位;價格 中位數 {dm.price_num.median():.1f} 平均 {dm.price_num.mean():.1f} '
          f'最低 {dm.price_num.min():.1f} 最高 {dm.price_num.max():.1f}')
    print('  臥室數分布(補值後):', dict(dm.bed_n.value_counts().sort_index()))
    print(f'  可住人數 {dm.acc.min():.0f}–{dm.acc.max():.0f};最少入住晚數 {dm.min_n.min():.0f}–{dm.min_n.max():.0f}(中位數 {dm.min_n.median():.0f})')
    C.PROC.mkdir(parents=True, exist_ok=True)
    for name, df in ((G['table'], dm), (G['ext'], ext)):
        df[C.PROC_COLS_EXT].to_csv(C.PROC / name, index=False, encoding='utf-8')
        print(f'processed {name}: {len(df):,} 列 × {len(C.PROC_COLS_EXT)} 欄, 房東 {df.host_id.nunique():,} 位, sha256={sha(C.PROC / name)}')


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
    # 不加參數 = 第一次訓練那一群(整套 1–2 臥),行為不變;--group private_room / entire_home_all = 新增兩群
    g = sys.argv[sys.argv.index('--group') + 1] if '--group' in sys.argv else 'entire_1_2'
    main() if g == 'entire_1_2' else build_group(g)
