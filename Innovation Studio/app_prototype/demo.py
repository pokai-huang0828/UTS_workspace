"""命令列:輸入一間房的條件 → 印摘要 + 寫出兩份 HTML(outputs/<name>_public.html 與 outputs/<name>_local.html)。

例(報告附錄 B):
  python "Innovation Studio/app_prototype/demo.py" --nb Sydney --bedrooms 1 --acc 2 --beds 1 --baths 1 \
      --amen "Kitchen,Washer,Wifi" --price 300
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from core import report  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def main():
    ap = argparse.ArgumentParser(description='民宿營運助手原型:T1/T2/T3/T6/T7')
    ap.add_argument('--nb', required=True, help='區(neighbourhood_cleansed),例如 Sydney')
    ap.add_argument('--bedrooms', type=int, required=True, help='臥室數,目前只支援 1 或 2')
    ap.add_argument('--acc', type=int, required=True, help='可住人數,目前只支援 2–4')
    ap.add_argument('--beds', type=float, required=True)
    ap.add_argument('--baths', type=float, required=True)
    ap.add_argument('--amen', default='', help='已有設施,逗號分隔,用資料裡的英文名稱')
    ap.add_argument('--price', type=float, default=None, help='打算開的每晚價格(澳元);不填就用模型參考價')
    ap.add_argument('--cost', type=float, default=0.0, help='一年的成本(澳元),收入情景會扣掉')
    ap.add_argument('--lat', type=float, default=None)
    ap.add_argument('--lon', type=float, default=None)
    ap.add_argument('--threshold', type=float, default=0.80, help='設施差距的普及率門檻(暫定 0.80)')
    ap.add_argument('--year', type=int, default=2026, help='要列公眾假期的年份')
    ap.add_argument('--review-demo', default='房源C', help='T4、T5 要示範哪一間已讀過評論的房(房源A–J,預設 房源C)')
    ap.add_argument('--name', default='example_appendixB', help='輸出檔名前綴')
    a = ap.parse_args()

    try:
        r = report.build(a.nb, a.bedrooms, a.acc, a.beds, a.baths, a.amen.split(','), a.price, a.cost,
                         a.lat, a.lon, a.threshold, a.year, review_demo=a.review_demo)
    except ValueError as err:
        print(f'輸入有問題:{err}', file=sys.stderr)
        sys.exit(2)
    print(report.summary_text(r))
    out = HERE / 'outputs'
    out.mkdir(exist_ok=True)
    for public, tag in [(True, 'public'), (False, 'local')]:
        f = out / f'{a.name}_{tag}.html'
        f.write_text(report.to_html(r, public=public), encoding='utf-8')
        print(f'已寫出:{f}')


if __name__ == '__main__':
    main()
