# -*- coding: utf-8 -*-
"""IS-1111-MEL-MERGE:把墨爾本 A / B / C 三個分支與較早的評論走勢整合成
(1) notes/19_墨爾本深度分析.md  (2) reports/melbourne_deep_dive_2026-11-11.html(單檔、圖片 base64 內嵌)。

只讀 notes/raw/*.json 與 notes/figures/*.png;文字裡的數字全部由 JSON 取值(f-string),
推導值(例如前 4 區占比)在這裡算並 assert 對上分支短報告。可重跑:python build_mel_report.py
"""
import base64
import html
import json
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../Innovation Studio
RAW, FIG = ROOT / "notes" / "raw", ROOT / "notes" / "figures"
OUT_MD = ROOT / "notes" / "19_墨爾本深度分析.md"
OUT_HTML = ROOT / "reports" / "melbourne_deep_dive_2026-11-11.html"


def J(name):
    return json.loads((RAW / f"{name}_2026-11-11.json").read_text(encoding="utf-8"))


A, B, C, Y = J("mel_a_market"), J("mel_b_positioning"), J("mel_c_hosts_time"), J("airbnb_melbourne_2024_2026")


def first(d, prefix):  # 取鍵名以 prefix 開頭的值
    return next(v for k, v in d.items() if k.startswith(prefix))


def rnd(x, k=1):  # 四捨五入,0.5 進位(避免 39.55 被浮點誤差算成 39.5)
    return Decimal(repr(round(float(x), 10))).quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP)


def n(x): return f"{x:,.0f}"
def d0(x): return f"${rnd(x, 0):,}"
def pc(x, k=1): return f"{rnd(x * 100, k)}%"      # 小數 -> 百分比
def f1(x): return f"{rnd(x, 1)}"
def sg(x): return f"{rnd(x, 1):+}%"
def months(lst): return "、".join(str(m) for m in lst) + " 月"


# ---------------- A 市場 ----------------
S, P, D = A["a_supply"], A["b_price"], A["c_districts"]["districts"]
sh_entire = S["room_type"]["Entire home/apt"]["share"]
hc = S["host_concentration"]
eb = P["entire_by_bedrooms"]
top8 = A["d_maps"]["top8_by_listings"]
top4 = sum(x["n_listings"] for x in top8[:4]) / S["n_listings"]
assert pc(top4) == "55.5%"
priced = {k: v["scope_price_median"] for k, v in D.items() if v["scope_price_median"] is not None}
hi_d, lo_d = max(priced, key=priced.get), min(priced, key=priced.get)
assert (hi_d, lo_d) == ("Yarra Ranges", "Knox")


def prow(label, v):
    return [label, n(v["n"]), d0(v["p25"]), d0(v["p50"]), d0(v["p75"])]


price_rows = [prow("全體", P["all_priced"]), prow("整套房", P["by_room_type"]["Entire home/apt"]),
              prow("獨立房間", P["by_room_type"]["Private room"])] + [prow(f"整套 {k} 房", eb[k]) for k in "123"]
dist_rows = [[x["name"], n(x["n_listings"]), n(D[x["name"]]["n_scope_priced"]), d0(D[x["name"]]["scope_price_median"]),
              f"{D[x['name']]['rating_median']:.2f}", pc(D[x["name"]]["entire_share"], 0)] for x in top8[:6]]
cal = A["e_demand"]["calendar_blocked"]["periods"]
cal_keys = sorted(cal)
cal_rows = [[f"{k} {cal[k]['season']}", n(cal[k]["n_listings_in_calendar"])] +
            [pc(cal[k]["all"][w]["blocked_share"]) for w in ("30", "60", "90")] for k in cal_keys]
blk_lo = min(cal[k]["all"]["30"]["blocked_share"] for k in cal_keys)
blk_hi = max(cal[k]["all"]["30"]["blocked_share"] for k in cal_keys)

# ---------------- B 定位與模型 ----------------
G = B["a_grouping"]
T = B["b_positioning"]["table"]
top10 = B["b_positioning"]["top10_districts"]
# 先四捨五入到整數澳幣(跟圖上標的數字一致)再相減;用原始小數相減最大值會是 114.7
dif = [round(T[x]["by_bedrooms"]["2"]["p50"]) - round(T[x]["by_bedrooms"]["1"]["p50"]) for x in top10]
dif_lo, dif_hi = min(dif), max(dif)
assert (dif_lo, dif_hi) == (58, 114)
b1 = {x: T[x]["by_bedrooms"]["1"]["p50"] for x in top10}
b1_hi, b1_lo = max(b1, key=b1.get), min(b1, key=b1.get)
assert (b1_hi, b1_lo) == ("Yarra Ranges", "Darebin")
CA = B["c_amenities"]
AS = CA["association"]
tp = list(CA["top30_prevalence_pct"].items())[:3]
amen_cnt = CA["amenity_count_distribution"]
bbq = next(x for x in AS["top10_positive"] if x["amenity"] == "BBQ grill: gas")
fire = next(x for x in AS["top10_positive"] if x["amenity"].startswith("Indoor fireplace"))
dry = next(x for x in AS["top5_negative"] if x["amenity"].startswith("Paid dryer"))
pos_n = [x["n_with"] for x in AS["top10_positive"]]
amen_rows = [[x["amenity"], n(x["n_with"]), sg(x["within_group_pct"]), sg(x["regression_pct"])] for x in (bbq, fire, dry)]
E = B["d_experiment"]
R = E["results_group_cv"]
exp_rows = []
for k, lab in [("B0", "B0 全市中位數"), ("B1", "B1 區 × 房間數中位數"), ("M1", "M1 線性(Ridge)"),
               ("M2", "M2 梯度提升樹"), ("M2_host", "M2 + 房東名下房源數(對照)")]:
    a = R[k]["all"]
    exp_rows.append([lab, f1(a["MAE_aud"]), f"{a['MdAPE_pct']:.1f}%", f"{a['within20_pct']:.1f}%"])
RD = E["random_minus_group_MAE_aud"]
small = [abs(RD[k]) for k in ("B0", "B1", "M1")]
rm2 = E["results_random_cv"]["M2"]["all"]["MAE_aud"]
rm2h = E["results_random_cv"]["M2_host"]["all"]["MAE_aud"]
m2 = R["M2"]
INC = E["extreme_sensitivity_including_excluded_extremes"]["M2"]
EX = B["extreme_rule"]
TC = B["d_temporal_check"]
tr = TC["results"]
SAME = TC["same_rows_in_period_group_cv"]
assert (SAME["M1"]["MAE_aud"], SAME["M2"]["MAE_aud"]) == (74.7, 77.3)
OWNER_SEEN = "45.0"  # 核對報告 L45(JSON 沒有)
ONE_PCT = "1.14"  # 核對報告 L49(JSON 沒有)
DEMO = B["e_demo_case"]
dg, dm1, dm2 = DEMO["comparison_group"], DEMO["model_literal_input_3_amenities"], DEMO["model_if_amenities_filled_to_group_median"]

# ---------------- C 新手與時間 ----------------
RC = C["recheck_initial"]
AV = C["a_validate_tenure_fields"]
vh, vu, hu = AV["vs_host_since_host"], AV["vs_host_since_user"], AV["host_vs_user_2025-12"]
TD = first(C["c_new_host_definition"]["definitions"], "T_")
HD = first(C["c_new_host_definition"]["definitions"], "H_")
cn = TD["counts"]
ct = first(TD, "crosstab")
MET = C["d_new_vs_veteran"]["metrics"]


def mv(key, who, f="median"): return MET[key][who][f]


FL = C["e_flows_and_march"]
mab, mpr = FL["march_absent_but_in_12_and_06"], FL["march_present_and_in_12_and_06"]


def src_prev(m): return m["in_06"]["source"]["previous scrape"] / m["n"] * 100


PCH = C["f_price_change"]
c39, c36, c69 = PCH["change_pct"]["3到9"], PCH["change_pct"]["3到6"], PCH["change_pct"]["6到9"]
same = PCH["same_weekday_and_nights_subset"]["3到9"]
WD = {"Sunday": "週日", "Monday": "週一", "Tuesday": "週二", "Wednesday": "週三", "Thursday": "週四", "Friday": "週五", "Saturday": "週六"}
qd = {m: PCH["quote_dates"][m] for m in ("2026-03", "2026-06", "2026-09")}
qtop = {m: list(v["checkin_top5"])[0][5:] for m, v in qd.items()}
qwd = {m: WD[v["checkin_weekday_of_mode"]] for m, v in qd.items()}
GP = first(C["g_first_year_price_path"], "T_")
gnew, gold = first(GP, "新手"), GP["老手"]

# ---------------- 較早的評論走勢 ----------------
YY = Y["yearly"]
SE = Y["seasonality"]
top3, bot3 = Y["top3_months"], Y["bottom3_months"]

# ======================= 內容(單一來源,同時輸出 md 與 html)=======================
CARDS = [
    ("市場", pc(sh_entire), f"整套房為主;{pc(hc['5_plus']['share'])} 的房源屬於名下 5 間以上的房東。整套 1 房中位 {d0(eb['1']['p50'])}、2 房 {d0(eb['2']['p50'])}(掛牌價);房源數前 4 區占全體 {pc(top4)}。"),
    ("同類比較", f"{G['n_groups']} 組", "區 × 房間數分組;組小於 30 間就退回「全市同房間數、最近的 30 間」。同類比較才是工具的核心。"),
    ("價格模型", f"MAE {f1(R['M2']['all']['MAE_aud'])}", f"比基準好,但只好一點(MAE:B0 {f1(R['B0']['all']['MAE_aud'])}、B1 {f1(R['B1']['all']['MAE_aud'])}、M1 {f1(R['M1']['all']['MAE_aud'])}、M2 {f1(R['M2']['all']['MAE_aud'])},澳幣)。工具價值主要在同類定位,模型是輔助。"),
    ("新手房東", f"{n(cn['scope_with_price']['new12'])} 間", f"找得到(用 `hosts_time_as_host_*`,不是 `host_since`)。定價跟老手差不多(同組百分位 {mv('prank','new'):.1f} 對 {mv('prank','old'):.1f}),差在評論少(近一年 {mv('reviews_ltm','new'):.0f} 對 {mv('reviews_ltm','old'):.0f})。"),
    ("時間", f"旺 {months(SE['high3_months'])}", f"淡旺季看得到(評論、日曆);但三期掛牌價中位數差 {sg(c39['p50'])} 不能當漲跌,每期報價的入住日落在不同季節。"),
]

SEC = []  # (id, 標題, [blocks])


def sec(i, title, *blocks): SEC.append((i, title, list(blocks)))


sec("market", "1 市場長相",
    ("lead", f"整套房占 {pc(sh_entire)};{pc(hc['5_plus']['share'])} 的房源屬於名下 5 間以上的房東。"),
    ("fig", "mel_a_supply.png", "房型、房東規模、整套房房間數"),
    ("read", f"右圖的分母是「房源」不是房東:名下 1 間 {pc(hc['1']['share'])}、2–4 間 {pc(hc['2_4']['share'])}、5 間以上 {pc(hc['5_plus']['share'])}。"),
    ("lead", f"有價 {n(P['n_priced_all'])} 間,中位數 {d0(P['all_priced']['p50'])};整套 1 房 {d0(eb['1']['p50'])}、2 房 {d0(eb['2']['p50'])}、3 房 {d0(eb['3']['p50'])}。"),
    ("fig", "mel_a_price_hist.png", "掛牌價分布(只畫到 p99)"),
    ("table", ["範圍(有價)", "n", "p25", "p50", "p75"], price_rows),
    ("read", f"高於 p99({d0(P['p99_value'])})有 {n(P['n_above_p99'])} 筆,最高 {d0(P['max_price'])};圖已截掉,分位數不受影響。價格是掛牌價,不是成交價。下表列前 6 區,30 區在 JSON。"),
    ("lead", f"房源集中市中心:前 4 區占 {pc(top4)};篩選樣本中位數最高 {hi_d} {d0(priced[hi_d])}、最低 {lo_d} {d0(priced[lo_d])}。"),
    ("fig", "mel_a_map_price_median.png", "各區掛牌價中位數(右為市中心放大)"),
    ("fig", "mel_a_map_listing_count.png", "各區房源數(對數色階)"),
    ("read", f"顏色越深越高。價格高的區不等於房源多的區:房源最多是 {top8[0]['name']} 區({n(top8[0]['n_listings'])} 間)。"),
    ("table", ["區", "房源數", "篩選且有價", "掛牌價中位", "評分中位(該區全部有評分房源)", "整套房占比"], dist_rows),
    )

sec("compare", "2 同類房源怎麼比",
    ("lead", f"區 × 房間數共 {G['n_groups']} 組,中位數 {G['group_size']['median']} 間;{G['n_groups_lt30']} 組不足 30 間,但只涵蓋 {n(G['listings_in_groups_lt30'])} 間({G['pct_listings_in_groups_ge30']}% 的房源在 30 間以上的組)。"),
    ("ol", ["找同區、同房間數的房源;30 間以上就用這組。",
            "不足 30 間 → 改用全市同房間數、直線距離最近的 30 間(不限區)。",
            "記下用了哪一步(1 或 2),報告時一起寫。"]),
    ("read", f"套用規則後,每間房的比較組中位數 {n(G['comparison_size_after_rule']['median'])} 間(p10 = {n(G['comparison_size_after_rule']['p10'])});退回「最近 30 間」時半徑中位數 {G['fallback_radius_km_30th_neighbor']['p50']} 公里。"),
    ("lead", f"前 10 大區內,2 房比 1 房中位數高 {dif_lo}–{dif_hi} 澳幣;1 房以 {b1_hi}({b1[b1_hi]:.0f})最貴、{b1_lo}({b1[b1_lo]:.0f})最便宜。"),
    ("fig", "mel_b_positioning_top10.png", "前 10 大區掛牌價區間(橫條 p25–p75,圓點中位數)"),
    ("read", f"你的價在橫條左邊 = 比同類 75% 便宜。完整 {B['b_positioning']['n_districts']} 區 × 房間數的 p10–p90 在 JSON。"),
    )

sec("amenity", "3 設施和價格",
    ("lead", f"每間房設施中位數 {amen_cnt['p50']:.0f} 項;最常見 {tp[0][0]} {tp[0][1]}%、{tp[1][0]} {tp[1][1]}%、{tp[2][0]} {tp[2][1]}%。"),
    ("fig", "mel_b_amenity_price.png", "設施與掛牌價的關聯(同組比較)"),
    ("table", ["設施", "有這項的房數", "同組比較", "迴歸控制後"], amen_rows),
    ("read", f"固定說法:「有 {bbq['amenity']} 的同類房源,掛牌價中位數高 {bbq['within_group_pct']:.1f}%」。這是關聯,不代表裝了就會漲。兩種算法方向一致的比例 {AS['sign_agree_pct_all_eligible']}%({AS['n_eligible']} 項合格設施);正向前 10 多是少數房源才有的設施({min(pos_n)}–{max(pos_n)} 間,信賴區間寬),負向多是公寓大樓型設施,比較像房源類型的訊號。264 項取最大 10 項,個別估計偏高;圖與表沒畫信賴區間,其中 Stainless steel double oven 的迴歸信賴區間 [{min(x['regression_ci95_pct'][0] for x in AS['top10_positive']):g}, {next(x for x in AS['top10_positive'] if x['regression_ci95_pct'][0] < 0)['regression_ci95_pct'][1]:g}] 含 0。"),
    )

sec("model", "4 價格模型實驗",
    ("lead", f"模型(M1 / M2)只比「區 × 房間數中位數」(B1)少猜錯約 {R['B1']['all']['MAE_aud'] - R['M2']['all']['MAE_aud']:.0f} 澳幣,比全市中位數(B0)少約 {R['B0']['all']['MAE_aud'] - R['M2']['all']['MAE_aud']:.0f} 澳幣;M1 與 M2 幾乎打平。這是老實的結果。"),
    ("ul", [f"目標:猜每晚掛牌價(取對數訓練,誤差換回澳幣);樣本 {n(R['M2']['all']['n'])} 間。",
            "特徵:只用新房東上架前就知道的(區、位置、房型、房間數、人數、床、浴室、設施、最少入住晚數);不用評論、入住推算、行事曆。",
            "切法:同一房東的房源分在同一折(5 折)。",
            "指標:MAE(平均猜偏幾澳幣)、誤差中位數 %、落在兩成內的比例。"]),
    ("table", ["方法", "MAE 澳幣", "誤差中位數", "差 20% 以內"], exp_rows),
    ("fig", "mel_b_mae_compare.png", "各方法 MAE 比較(越低越好)"),
    ("read", f"一般房源猜偏約 {m2['all']['MdAPE_pct']:.0f}%,大約一半猜在兩成內。加房東房源數沒幫助。誤差衡量「猜中別人掛多少」,不是「定多少訂得出去」。"),
    ("ul", [f"不分房東隨機切會高估:M2 MAE {f1(rm2)}(低 {-RD['M2']:.1f})、M2 + 房東數 {f1(rm2h)}(低 {-RD['M2_host']:.1f});B0 / B1 / M1 只差 {min(small):.1f}–{max(small):.1f}。樹模型會記住同房東的習慣,所以主結果用分組切。",
            f"首評在 12 個月內的房源(新上架的代理){n(m2['new12']['n'])} 間(其中只有 {TD['proxy_precision_pct(代理說新的裡面真新手)']}% 是真的新手房東,見第 5 節):M2 MAE {f1(m2['new12']['MAE_aud'])}、誤差中位數 {m2['new12']['MdAPE_pct']:.1f}%、兩成內 {m2['new12']['within20_pct']:.1f}%;其他 {f1(m2['not_new12']['MAE_aud'])} / {m2['not_new12']['MdAPE_pct']:.1f}% / {m2['not_new12']['within20_pct']:.1f}%。這群沒有比較難猜;模型在真新手 {n(cn['scope_with_price']['new12'])} 間上的誤差未計算。",
            f"時間外部檢查:用 2026-06 期 {n(TC['n_train'])} 間訓練,測 9 月新出現的 {n(TC['n_test'])} 間,模型仍比基準好(M2 {f1(tr['M2']['MAE_aud'])}、B1 {f1(tr['B1']['MAE_aud'])})。但這 {n(TC['n_test'])} 間裡有 {OWNER_SEEN}% 的房東在 6 月訓練集出現過,所以不是「完全沒看過的房東」的檢查。線性和樹模型誰比較好,兩種檢查不一致(9 月內分房東驗證時線性 {f1(SAME['M1']['MAE_aud'])}、樹 {f1(SAME['M2']['MAE_aud'])};時間檢查時樹 {f1(tr['M2']['MAE_aud'])}、線性 {f1(tr['M1']['MAE_aud'])}),所以只能說「兩個模型差不多」。",
            f"極端高價:每晚 {n(EX['cap_aud'])} 澳幣以上 {EX['n_excluded']} 間(最高 {n(max(EX['excluded_prices_sorted']))})不進訓練與主要誤差。放回去,M2 MAE 由 {f1(m2['all']['MAE_aud'])} 變 {f1(INC['MAE_aud'])},誤差中位數仍是 {INC['MdAPE_pct']:.1f}%(幾乎不變)。"]),
    ("fig", "mel_b_pred_vs_actual.png", "預測對實際(500 以上被猜低)"),
    ("read", "點集中在 200–350;高價房(500 以上)系統性被猜低,模型把極端往中間拉。"),
    )

sec("newbie", "5 新手房東",
    ("lead", f"`host_since` 是註冊帳號的日子;當房東多久,最像是看 `hosts_time_as_host_*`。用它抓到真新手(≤ 12 個月)篩選且有價 {n(cn['scope_with_price']['new12'])} 間。"),
    ("table", ["欄位", "實際意思", "證據(2025-12 期)"], [
        ["`host_since`", "註冊帳號的日子", f"跟 `hosts_time_as_user_*` 完全相同 {vu['exact_pct']}%、差 1 個月內 {vu['within_1m_pct']:.0f}%({n(AV['n_2025-12_rows_with_host_since'])} 列)"],
        ["`hosts_time_as_user_*`", "帳號年資", "同上;以抓取日為基準,所以不是「兩欄基準日不同」"],
        ["`hosts_time_as_host_*`", "開始當房東以來(推測)", f"對 `host_since` 完全相同只有 {f1(vh['exact_pct'])}%,{f1(vh['field_shorter_than_1m_pct'])}% 比它短;不大於帳號年資的比例 {hu['host_le_user_pct']}%;2025-12 到 2026-09 每位房東增加 9 或 10 個月"]]),
    ("note", f"`host_since` 對得上帳號年資,這一半證據夠;「年資欄 = 當房東多久」是靠排除法推的,沒有官方定義,證據勉強。核對者補了一個檢驗:首評比回推的開始月早超過 1 個月的只有 {ONE_PCT}%,跟這個解讀不矛盾。"),
    ("table", ["真新手筆數", "全體", "篩選", "篩選且有價"], [
        ["開始當房東 ≤ 12 個月"] + [n(cn[s]["new12"]) for s in ("all", "scope", "scope_with_price")],
        ["24 個月內"] + [n(cn[s]["new24"]) for s in ("all", "scope", "scope_with_price")],
        ["12 個月內且名下只有 1 間"] + [n(cn[s]["new12_and_single"]) for s in ("all", "scope", "scope_with_price")],
        ["24 個月內且名下只有 1 間"] + [n(cn[s]["new24_and_single"]) for s in ("all", "scope", "scope_with_price")]]),
    ("read", f"舊代理(首評 12 個月內)有 {n(TD['proxy_yes'])} 間,其中只有 {n(TD['both'])} 間是真新手:命中率 {TD['proxy_precision_pct(代理說新的裡面真新手)']}%;真新手 {n(TD['real_yes'])} 間裡抓到 {n(TD['both'])} 間:抓到率 {TD['proxy_recall_pct(真新手裡被代理抓到)']}%(漏掉的 {n(ct['無評論']['真新手'])} 間還沒有評論)。"),
    ("fig", "mel_c_newbie_vs_veteran.png", "新手 vs 老手(縱軸不從 0 起;5.0 為評分上限)"),
    ("ul", [f"定價幾乎一樣:掛牌價中位數 {mv('price','new'):.2f} 對 {mv('price','old'):.0f};同組價格百分位 {mv('prank','new'):.1f} 對 {mv('prank','old'):.1f}。",
            f"差別 1,評論少:近一年評論數中位數 {mv('reviews_ltm','new'):.0f} 對 {mv('reviews_ltm','old'):.0f}。",
            f"差別 2,有評分的比例 {MET['rated_share']['new']['share_pct']}% 對 {MET['rated_share']['old']['share_pct']}%(評分中位 {mv('rating','new')} 對 {mv('rating','old')},是評論少,不代表品質較好)。",
            f"差別 3,超讚房東比例 {MET['superhost_share']['new']['share_pct']}% 對 {MET['superhost_share']['old']['share_pct']}%。"]),
    )

sec("time", "6 時間與淡旺季",
    ("lead", f"評論逐年墊高:2025 年比 2024 年 +{Y['growth']['y2025_vs_y2024_pct']}%;2026 年 1–8 月比 2025 年同期 +{Y['growth']['jan_aug_2026_vs_2025_pct']}%。"),
    ("fig", "melbourne_reviews_monthly_2026-11-11.png", "每月評論數(只含還在架上的房源)"),
    ("read", f"最多:{top3[0]['month']}({n(top3[0]['reviews_all'])})、{top3[1]['month']}、{top3[2]['month']};最少:{bot3[0]['month']}({n(bot3[0]['reviews_all'])})。早年已下架的房源不在內,成長率偏高。"),
    ("lead", f"兩年平均:偏旺的是 {months(SE['high3_months'])},偏淡的是 {months(SE['low3_months'])};2024 與 2025 各月指數的相關係數 {SE['corr_2024_2025']:.2f},形狀很像。"),
    ("fig", "melbourne_seasonality_2026-11-11.png", "評論淡旺季指數(100 = 平均)"),
    ("read", "這是「評論的」淡旺季,不等於入住的淡旺季:評論住完才寫,高峰比入住晚。"),
    ("fig", "melbourne_new_listings_2026-11-11.png", "每月新上架(首評月份代理)"),
    ("read", f"首評落在當年的房源:2024 年 {n(YY['2024']['first_review_listings_all'])}、2025 年 {n(YY['2025']['first_review_listings_all'])}、2026 年(到 9/18){n(YY['2026']['first_review_listings_all'])} 間。首評月不等於上架月,上架可能更早。"),
    ("lead", f"四期抓取日後 30 天的不可訂占比,從 {pc(blk_lo)}(3 月)到 {pc(blk_hi)}(12 月)。"),
    ("fig", "mel_a_calendar_blocked.png", "四期日曆:未來 30 / 60 / 90 天不可訂占比"),
    ("table", ["期別", "房源數", "30 天", "60 天", "90 天"], cal_rows),
    ("read", f"不可訂 = 被訂走或房東自己關,分不出來。3 月那期只有 {n(cal['2026-03-21']['n_listings_in_calendar'])} 間,四期不能當同一批比。"),
    ("lead", f"同一間房 3 到 9 月的掛牌價變化中位數 {sg(c39['p50'])}({n(PCH['n_common_priced_in_03_06_09'])} 間),但單間差很大;各期報價的入住日落在不同季節,不能當成房東調價。"),
    ("fig", "mel_c_price_change_3_to_9.png", "同一間房 3 到 9 月的掛牌價變動"),
    ("read", f"單間 p10 到 p90:{sg(c39['p10'])} 到 {sg(c39['p90'])}。三期報價的入住日最常見分別是 3 月 {qtop['2026-03']}({qwd['2026-03']})、6 月 {qtop['2026-06']}({qwd['2026-06']})、9 月 {qtop['2026-09']}({qwd['2026-09']}),落在秋、冬、春。只比「同星期、同晚數」的 {n(same['n'])} 間(約 {same['share_of_common_pct']:.0f}%)中位數 {sg(same['p50'])},結論一樣,但季節仍沒排除。"),
    ("p", f"新手與老手同方向:3 到 9 月中位數新手 {sg(gnew['median_change_vs_03_pct']['03到09'])}(n={n(gnew['n'])})、老手 {sg(gold['median_change_vs_03_pct']['03到09'])}(n={n(gold['n'])}),差不到 1 個百分點,別讀成「新手較保守」。"),
    ("lead", f"3 月那期只有 {n(RC['2026-03']['rows'])} 間:最可能是沒收「休眠房源」(證據強度中高;官方為什麼這樣收,看不出)。"),
    ("table", [f"2026-06 那期裡的房源", f"3 月缺席({n(mab['n'])} 間)", f"3 月在({n(mpr['n'])} 間)"], [
        ["有價比例", f"{mab['in_06']['price_nonnull_pct']}%", f"{mpr['in_06']['price_nonnull_pct']}%"],
        ["全年可訂天數 = 0", f"{mab['in_06']['availability_365_eq_0_pct']}%", f"{mpr['in_06']['availability_365_eq_0_pct']}%"],
        ["來源為「前次爬取」", f"{src_prev(mab):.1f}%", f"{src_prev(mpr):.1f}%"],
        ["近一年評論數 = 0", f"{mab['in_06']['reviews_ltm_eq_0_pct']}%", f"{mpr['in_06']['reviews_ltm_eq_0_pct']}%"]]),
    ("read", f"缺席的幾乎都是早就全年不可訂、沒評論的房源;3 月消失的 {n(FL['gone_in_03_n'])} 間,6 月回來 {FL['gone_in_03_returned_in_06_pct']}%。"),
    )

sec("demo", "7 示範:系統最後會長這樣",
    ("demo", None),
    )

sec("impact", "8 對專案的影響",
    ("ul", [f"新手定義建議改用年資欄 `hosts_time_as_host_*`,並列新舊筆數:年資欄 {n(cn['scope_with_price']['new12'])} 間、舊代理(首評 12 個月內){n(TD['proxy_yes'])} 間(其中真新手 {n(TD['both'])})。欄義官方說明寫報告前先補查。",
            "實驗主線可寫成「同類定位為主、模型為輔」:同類分組 → 設施關聯(註明不是因果)→ 模型只比基準好一點。",
            f"跨期比較:價格只有 3、6、9 月三期可用(2025-12 期 price 非空率 {RC['2025-12']['price_nonnull_pct']:.0f}%);三期報價入住日季節不同,不能當成房東調價;3 月那期只有 {n(RC['2026-03']['rows'])} 間。",
            f"舊筆記更正(只列出,不改 `notes/16`、`17`、`18`):「`host_since` 整欄空」只描述 2026-09 那期;2026-03、06 也是空的,但 2025-12 那期 {RC['2025-12']['host_since_nonnull_pct']:.0f}% 有值,而且它是帳號註冊日,不是開始當房東。",
            f"舊筆記更正:`17` 的「新上架房源」(首評 12 個月內)代理,命中率只有 {TD['proxy_precision_pct(代理說新的裡面真新手)']}%(抓到率 {TD['proxy_recall_pct(真新手裡被代理抓到)']}%)。",
            "後續要補:模型在真新手(年資欄 12 個月內)上的誤差,目前未計算。"]),
    )

sec("blind", "9 看不到的事",
    ("table", ["不要這樣說", "改這樣說"], [
        ["成交價:「墨爾本中位數 " + d0(P["all_priced"]["p50"]) + " 是房東賺的」", "「這是掛牌價中位數;成交價、清潔費、折扣看不到」"],
        ["真實入住:「推算入住 = 住了幾晚」「評論數 = 訂單數」", "「這是用評論推算的代理;0 晚也可能只是沒人留評論」"],
        [f"裝設施就漲:「裝 BBQ 能漲 {bbq['within_group_pct']:.0f}%」", f"「有 gas BBQ 的同類房源,掛牌價中位數高 {bbq['within_group_pct']:.1f}%({bbq['n_with']} 間;關聯不是因果)」"],
        ["新手一定定低價:「新手定價比較低」", f"「新手同組價格百分位中位 {mv('prank','new'):.1f},老手 {mv('prank','old'):.1f},幾乎沒差」"],
        [f"三期價格漲跌:「房東 3 月到 9 月漲價 {c39['p50']:.1f}%」", f"「同一間房 3 月與 9 月報價中位差 {sg(c39['p50'])},但入住日季節不同,不等於調價」"],
        ["模型誤差:「模型能預測房價」「準確率很高」", f"「模型猜別人的掛牌價,平均猜偏 {m2['all']['MAE_aud']:.0f} 澳幣,誤差中位數 {m2['all']['MdAPE_pct']:.0f}%,約一半猜在兩成內」"],
        ["不可訂:「30 天不可訂 = 被訂走」", "「不可訂 = 被訂走或房東自己關,分不出來」"],
        ["新手:「首評 12 個月內 = 新手」", f"「首評代理只有 {TD['proxy_precision_pct(代理說新的裡面真新手)']}% 是真新手;要精確請用年資欄」"],
        ["3 月:「3 月那批房源下架了」", f"「3 月缺席的 {n(mab['n'])} 間多半是休眠房源,6 月以前次爬取身分回來」"]]),
    )

SOURCES = [
    ["房型占比、房東規模、價格分位、p99", "A", "a_supply.room_type / host_concentration;b_price.all_priced / by_room_type / entire_by_bedrooms / p99_value / n_above_p99"],
    ["分區表、前 4 區占比", "A", "c_districts.districts.* / d_maps.top8_by_listings"],
    ["四期不可訂占比", "A", "e_demand.calendar_blocked.periods.<期別>.all.<30/60/90>.blocked_share"],
    ["60 組、631、8.3 公里", "B", "a_grouping"],
    ["前 10 區價格區間", "B", "b_positioning.table / top10_districts"],
    ["設施比例與價格關聯", "B", "c_amenities.top30_prevalence_pct / association"],
    ["MAE、誤差中位數、兩成內、分群", "B", "d_experiment.results_group_cv / results_random_cv / random_minus_group_MAE_aud"],
    ["極端值、時間外部檢查", "B", "extreme_rule / d_experiment.extreme_sensitivity_* / d_temporal_check.results"],
    ["示範案例", "B", "e_demo_case"],
    ["欄位差在哪、欄位非空率", "C", "a_validate_tenure_fields / recheck_initial"],
    ["真新手筆數、命中率與抓到率", "C", "c_new_host_definition.definitions.T_*"],
    ["新手 vs 老手;3 月少一批", "C", "d_new_vs_veteran.metrics;e_flows_and_march"],
    ["同一間房價格變化、入住日、新手路徑", "C", "f_price_change / g_first_year_price_path"],
    ["時間檢查 M1 / M2(9 月內分房東 74.7 / 77.3;時間檢查 72.6 / 70.9)", "B", "d_temporal_check.same_rows_in_period_group_cv / results"],
    ["45.0%(820 間的房東在 6 月訓練集出現過)、1.14%(首評早於回推開始月超過 1 個月)、37 項(A 15 / C 13 / B 9)", "R", "`raw/mel_review_2026-11-11.md`:45.0% → L45;1.14% → L49;37 項 → L7、L19、L30、L37"],
    ["每年評論、成長率、淡旺季、新上架", "Y", "yearly / growth / seasonality / monthly / top3_months / bottom3_months"],
]

periods = " / ".join(C["meta"]["periods"])
sec("data", "10 資料與核對狀態",
    ("ul", ["出處:Inside Airbnb 官方下載頁 https://insideairbnb.com/get-the-data/ ;墨爾本四期:" + periods + "(深度分析以 2026-09-16 期為主)。",
            "本機資料夾:`scratchpad/insideairbnb_melbourne/`(未進版控)。",
            f"樣本:全體 {n(A['meta']['recon']['listings_rows'])} 間;篩選(整套、1–2 房、2–4 人、最低 1–7 晚){n(A['meta']['recon']['scope_rows'])} 間;篩選且有價 {n(A['meta']['recon']['scope_with_price_rows'])} 間。",
            "核對狀態:2026-11-11 由未參與撰寫的 Claude 分身獨立重算 37 項數字(A 15、C 13、B 9),全部吻合;重跑 B 的程式,模型誤差重現;B 的特徵沒有洩漏答案、分組切分正確。核對者指出的 3 處措辭已修。",
            "**沒有核對的**:A 的四期日曆占比、評分四分位、各區房源數;B 的設施關聯、特徵重要度、各分群誤差(只重跑重現,沒獨立重算);C 的新手對老手比較與分區變動;圖只抽看。沒有其他家族模型核對。修改後的措辭只有修改者回讀。",
            "限制:價格都是掛牌價;沒有成交價與真實入住;下架房源不在內(存活者偏誤);經緯度有隨機偏移;年資欄欄義是推斷。",
            "來源檔(`notes/raw/`):A = `mel_a_market`、B = `mel_b_positioning`、C = `mel_c_hosts_time`、Y = `airbnb_melbourne_2024_2026`,皆為 `_2026-11-11.json`;分支短報告為同名 `.md`;R = `mel_review_2026-11-11.md`(獨立核對報告)。"]),
    ("h3", "數字來源對照(數字 → 來源檔 + 鍵名)"),
    ("table", ["數字", "檔", "JSON 鍵名"], SOURCES),
    )

DEMO_LINES = [
    f"輸入:{DEMO['input']}。",
    f"同類房源(步驟 {dg['rule_step']}):{n(dg['n'])} 間;掛牌價 p25 / p50 / p75 = {dg['p25']:.0f} / {dg['p50']:.0f} / {dg['p75']:.0f}。只看 2 人房:{n(dg['subset_accommodates_2']['n'])} 間,{dg['subset_accommodates_2']['p25']:.0f} / {dg['subset_accommodates_2']['p50']:.0f} / {dg['subset_accommodates_2']['p75']:.0f}。",
    f"模型參考(M2,照字面只有 {dm1['amenity_count']} 項設施):約 {dm1['point_aud']:.0f},參考區間 {dm1['ref_range_aud'][0]:.0f}–{dm1['ref_range_aud'][1]:.0f}。設施補到同類中位數 {dm2['amenity_count']} 項:約 {dm2['point_aud']:.0f},區間 {dm2['ref_range_aud'][0]:.0f}–{dm2['ref_range_aud'][1]:.0f}(只是關聯,不代表補了設施就會漲)。",
    "缺的同類常見設施:" + "、".join(f"{x['amenity']} {x['group_prevalence_pct']}%" for x in DEMO["missing_top3_common_in_group"]) + "。",
    "同類一半以上有、且同組比較為正向:" + "、".join(f"{x['amenity']}({x['group_prevalence_pct']}%,{sg(x['within_group_pct'])})" for x in DEMO["missing_top3_common_ge50pct_and_positive_within_group"]) + "。",
]
DEMO_NOTE = "這是示範輸出,不是定價建議;價格是別人的掛牌價,不是成交價。參考區間 = 模型點估 × 交叉驗證中間 50% 的誤差。"
SEC[[s[0] for s in SEC].index("demo")][2].append(("read", DEMO_NOTE))

TITLE = "墨爾本 Airbnb 深度分析"
SUB = "給準備入行的新房東:競品定位工具的資料底稿。Inside Airbnb 墨爾本 2026-09-16 期為主,另有 3 期;價格都是掛牌價,不是成交價。"
FIGS_USED = []


# ======================= 輸出 md =======================
def render_md():
    L = [f"# 19 {TITLE}", f"> IS-1111-MEL-MERGE,2026-11-11。{SUB}", "", "## 0 一頁結論"]
    L += [f"- **{t}({b})**:{x}" for t, b, x in CARDS]
    for _, title, blocks in SEC:
        L += ["", f"## {title}"]
        prev = None
        for b in blocks:
            k = b[0]
            blank = prev is not None and (prev in ("table", "ul", "ol", "demo", "h3") or k in ("table", "ul", "ol", "h3", "demo")
                                          or (k == "lead" and prev in ("read", "p", "note")))
            if blank:
                L.append("")
            elif prev is not None:
                L[-1] += "  "  # 行尾兩空白 = 斷行,同組內不另空一行
            if k == "lead": L.append(f"**{b[1]}**")
            elif k == "read": L.append(f"怎麼讀:{b[1]}")
            elif k in ("p", "note"): L.append(("> " if k == "note" else "") + b[1])
            elif k == "h3": L.append(f"### {b[1]}")
            elif k == "fig":
                L.append(f"![{b[2]}](figures/{b[1]})")
                L.append(f"*圖:{b[2]}*")
            elif k == "ul": L += [f"- {x}" for x in b[1]]
            elif k == "ol": L += [f"{i}. {x}" for i, x in enumerate(b[1], 1)]
            elif k == "table":
                L.append("| " + " | ".join(b[1]) + " |")
                L.append("|" + "---|" * len(b[1]))
                L += ["| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in b[2]]
            elif k == "demo":
                L += [f"> {x}" for x in DEMO_LINES]
            prev = k
    text = "\n".join(L) + "\n"
    OUT_MD.write_text(text, encoding="utf-8")
    return text.count("\n")


# ======================= 輸出 html =======================
CSS = """
*{box-sizing:border-box}
body{margin:0;background:#fff;color:#1f2933;font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",system-ui,sans-serif;font-size:17px;line-height:1.85}
main{max-width:900px;margin:0 auto;padding:24px 18px 64px}
h1{font-size:1.9rem;line-height:1.3;margin:.2em 0 .3em}
h2{font-size:1.5rem;margin:2.4em 0 .6em;padding-top:.6em;border-top:2px solid #d5dbe1}
h3{font-size:1.2rem;margin:1.8em 0 .5em}
.sub{color:#52606d;margin:0 0 1em}
nav{font-size:.95rem;margin:1em 0 0}nav a{margin-right:.9em;white-space:nowrap}
a{color:#1d5fa6}
code{background:#eef1f4;padding:.05em .35em;border-radius:3px;font-size:.92em;word-break:break-all}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:1.2em 0}
.card{flex:1 1 260px;border:1px solid #cfd6dd;border-top:5px solid #1d5fa6;border-radius:6px;padding:12px 16px;background:#f9fbfd}
.card .tag{font-size:.9rem;color:#52606d}
.card .big{font-size:1.7rem;font-weight:700;line-height:1.3;color:#14467a}
.card p{margin:.3em 0 0;font-size:1rem;line-height:1.7}
.lead{font-weight:700;font-size:1.1rem;margin:1.6em 0 .6em;padding-left:.7em;border-left:5px solid #1d5fa6}
.read{margin:.5em 0 1.2em;color:#3e4c59;background:#f4f6f8;border-radius:4px;padding:.5em .8em}
.read b{color:#14467a;margin-right:.4em}
.note{margin:.5em 0;color:#7a3e00;background:#fff6e8;border-left:4px solid #e0a040;padding:.4em .8em}
figure{margin:1em 0}
figure img{display:block;width:100%;height:auto;border:1px solid #e1e5ea}
figcaption{font-size:.92rem;color:#52606d;margin-top:.3em}
.tw{overflow-x:auto;margin:.8em 0 1.2em;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;min-width:100%;font-size:.95rem;line-height:1.55}
th,td{border:1px solid #d5dbe1;padding:.45em .7em;text-align:left;vertical-align:top}
th{background:#eef2f6;white-space:nowrap}
td:not(:first-child){}
ul,ol{padding-left:1.4em}li{margin:.35em 0}
.demo{border:2px solid #1d5fa6;border-radius:8px;padding:14px 18px;background:#f5f9ff;margin:1em 0}
.demo .stamp{display:inline-block;background:#c0392b;color:#fff;font-size:.85rem;padding:.1em .6em;border-radius:3px;margin-bottom:.4em}
.demo .in{margin:.2em 0 .8em;font-weight:700}
.bars{margin:.6em 0 1em}
.brow{display:flex;align-items:center;gap:10px;margin:.5em 0}
.blab{flex:0 0 9.5em;font-size:.92rem}
.track{position:relative;flex:1 1 auto;height:22px;background:#e6ebf0;border-radius:3px}
.bar{position:absolute;top:0;height:22px;background:#7aa6d6;border-radius:3px}
.bar.m{background:#e3a35c}
.tick{position:absolute;top:-3px;width:3px;height:28px;background:#14467a}
.bval{flex:0 0 7.5em;font-size:.92rem;text-align:right}
.axis{display:flex;justify-content:space-between;margin-left:calc(9.5em + 10px);margin-right:calc(7.5em + 10px);font-size:.8rem;color:#52606d}
.demo ul{margin:.4em 0}
details{margin:1em 0}summary{cursor:pointer}
@media (max-width:600px){body{font-size:16px}h1{font-size:1.55rem}.blab{flex-basis:6.5em}.bval{flex-basis:5.5em}.axis{margin-left:calc(6.5em + 10px);margin-right:calc(5.5em + 10px)}}
"""


def inl(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(https://[^\s;,)<]+)", r'<a href="\1">\1</a>', s)


def img64(name):
    FIGS_USED.append(name)
    return "data:image/png;base64," + base64.b64encode((FIG / name).read_bytes()).decode("ascii")


def demo_html():
    lo_, hi_ = 150, 320
    pos = lambda x: (x - lo_) / (hi_ - lo_) * 100
    def bar(lab, a, b, mid, cls=""):
        return (f'<div class="brow"><div class="blab">{lab}</div><div class="track">'
                f'<div class="bar {cls}" style="left:{pos(a):.1f}%;width:{pos(b) - pos(a):.1f}%"></div>'
                f'<div class="tick" style="left:{pos(mid):.1f}%"></div></div>'
                f'<div class="bval">{a:.0f}–{b:.0f}(點 {mid:.0f})</div></div>')
    bars = ('<div class="bars">'
            + bar("同類 p25–p75", dg["p25"], dg["p75"], dg["p50"])
            + bar("模型(3 項設施)", dm1["ref_range_aud"][0], dm1["ref_range_aud"][1], dm1["point_aud"], "m")
            + bar("模型(補到 40 項)", dm2["ref_range_aud"][0], dm2["ref_range_aud"][1], dm2["point_aud"], "m")
            + f'<div class="axis"><span>{lo_}</span><span>每晚掛牌價(澳幣)</span><span>{hi_}</span></div></div>')
    return ('<div class="demo"><span class="stamp">示範輸出,不是定價建議</span>'
            f'<div class="in">{inl(DEMO_LINES[0])}</div>{bars}<ul>'
            + "".join(f"<li>{inl(x)}</li>" for x in DEMO_LINES[1:]) + "</ul></div>")


def render_html():
    o = [f'<!DOCTYPE html>\n<html lang="zh-Hant"><head><meta charset="utf-8">'
         f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><style>{CSS}</style></head><body><main>',
         f"<h1>{TITLE}</h1><p class=\"sub\">{inl(SUB)}</p>",
         "<nav>" + "".join(f'<a href="#{i}">{t}</a>' for i, t, _ in SEC) + "</nav>",
         '<h2 id="top" style="border-top:0;margin-top:1.4em">0 一頁結論</h2><div class="cards">']
    for t, b, x in CARDS:
        o.append(f'<div class="card"><div class="tag">{t}</div><div class="big">{inl(b)}</div><p>{inl(x)}</p></div>')
    o.append("</div>")
    for i, title, blocks in SEC:
        o.append(f'<h2 id="{i}">{title}</h2>')
        for b in blocks:
            k = b[0]
            if k == "lead": o.append(f'<p class="lead">{inl(b[1])}</p>')
            elif k == "read": o.append(f'<p class="read"><b>怎麼讀</b>{inl(b[1])}</p>')
            elif k == "p": o.append(f"<p>{inl(b[1])}</p>")
            elif k == "note": o.append(f'<p class="note">{inl(b[1])}</p>')
            elif k == "h3": o.append(f"<h3>{inl(b[1])}</h3>")
            elif k == "fig": o.append(f'<figure><img src="{img64(b[1])}" alt="{html.escape(b[2])}"><figcaption>圖:{html.escape(b[2])}</figcaption></figure>')
            elif k in ("ul", "ol"): o.append(f"<{k}>" + "".join(f"<li>{inl(x)}</li>" for x in b[1]) + f"</{k}>")
            elif k == "table":
                o.append('<div class="tw"><table><thead><tr>' + "".join(f"<th>{inl(h)}</th>" for h in b[1]) + "</tr></thead><tbody>"
                         + "".join("<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>" for r in b[2]) + "</tbody></table></div>")
            elif k == "demo": o.append(demo_html())
    o.append("</main></body></html>\n")
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text("\n".join(o), encoding="utf-8")


if __name__ == "__main__":
    lines = render_md()
    render_html()
    print(f"md 行數 {lines};html {OUT_HTML.stat().st_size / 1024:.0f} KB;內嵌圖 {len(FIGS_USED)} 張")
