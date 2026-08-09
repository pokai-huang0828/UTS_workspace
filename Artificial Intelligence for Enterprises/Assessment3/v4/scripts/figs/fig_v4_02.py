# -*- coding: utf-8 -*-
"""P2 用圖 —— 為什麼是現在:工作量沒變多,客戶要的時效變了。

🔴 裁決 O 改版(畫布鎖死 12.2 x 5.7 吋,置入縮放比 = 1.0,fs=9 就是真的 9pt)。
🔴 2026-08-09 依 `notes/15_Kenny第二批答覆_全案重算.md`(位階最高)全面重畫:
   · 節奏改 3.6 個分析日 + 0.5 天整理回信(全程 4.1 天,不是 5 天)
   · 144 人時(不是 120);每筆深入判讀 5.25 分(不是 4.4 分)
   · 帶 2 五個問號**全部填上 Q45 的時間拆解**,並標出 AI 可處理段佔全程 60%-64%
   · 人力堆疊補上「折算 3.7-5.4 人 · 尖峰已不夠」(舊敘事「剛剛好」已作廢)

🔴 2026-08-09 第二輪(方案升級為地端 VLM 事件判讀,依 `notes/16_地端VLM方案升級_裁決與待辦.md`
   與 `notes/_v2_parts/P01-04.md` 的 P2【視覺規格】最新版)本圖三處改動:
   1. **新增因果句與兩條分述**(本輪最關鍵的版面新增,規格明訂不可省):
      括弧標註正下方 fs=12 深藍「這兩段之所以慢,是同一個原因:模型看不到畫面外的東西。」
      再下一列兩條 fs=10 分述,各配一枚與帶 2 高亮格同色的方形標記(見下方「規格偏離」)。
      沒有這三行,五段拆解只是營運圖表;有了它,兩段高亮才是同一個技術缺陷的兩個症狀。
   2. **「現況 4.1 天 -> 4.4 人」與 (Hopp & Spearman, 2011, chaps. 7-9)**:
      兩者同屬壓力測試框,該框依裁決 O 已整塊移出 PNG →
      **落在 SLIDE_TEXT["D_STRESS"]**(本檔 module-level),數值已由 120 人時 / 7.5 / 15.0
      更正為 144 人時 / 4.4 / 9.0 / 18.0,in-text 標記已補上 chaps. 7-9 定位。
   3. **帶 2 抬頭改寫,補上「不算交叉驗證」**:舊版圖上寫「與登記在案的 2-5 天吻合」
      卻沒帶但書,等於在圖上做了一次假交叉驗證(16 號檔 §五 主迴圈自我更正的正是這一點)。
      現改為「與登記在案的 2-5 天吻合,但同一營運來源,不算交叉驗證」,並在左抬頭補證據等級。
   4. 🔴 **帶 2 五段由等寬改為按天數比例**(規格【排版要求】早就這樣寫,舊版沒做到):
      等寬時 AI 可處理段在畫面上只佔 2/5 = 40%,而它正下方的標註寫 60%-64% ——
      **圖自己反駁了自己的論點**,而本輪新增的因果句就掛在這個論點上。
      改為 0.5 / 0.5 / 2.0 / 0.5 / 0.5(區間取中位)後,AI 段實測佔 62.5%,落在標註區間內;
      區間段(0-1 天 / 1-3 天)的邊界改畫虛線,表示這條界線會滑動。
      段名因此收短為「等待排隊 / 撈數據 / 報告回信」——**砍字不砍比例**(裁決 O)。

   ⚠️ **規格偏離一處(刻意,已評估)**:規格要求兩條分述「以細引線指回段 2 與段 3」。
      引線的垂直走廊被括弧線與括弧標註佔滿,硬畫會穿過文字;改以「與帶 2 高亮格同色的
      方形標記 + 分述句開頭直接寫出段名(撈數據慢 / 判讀慢)」完成同一件繫結工作。
      🚫 未採用的替代方案:放大畫布(違反裁決 O)、縮字級到 9 以下(違反 FS_MIN)。

🔴 **SLIDE_TEXT 取代 `notes/14_組版施工清單_移出圖的文字.md` 的「區塊 1」** ——
   該區塊寫於 15 號檔重算之前,內含 4.4 分/筆 · 120 人時 · 27.7-38.7 · 69%-97% ·
   3.5-4.8 人 · 7.5/15.0 人等**全部已作廢的數字**,組版時一律以本檔 SLIDE_TEXT 為準。

本圖只保留「需要圖形關係才講得清楚」的主視覺:
  · 左:那一件判讀的 latency waterfall(X 軸 = 工作日;帶 1 = 1,647 筆批次的實際節奏 /
        帶 2 = 單件客戶爭議的時間拆解五欄 + AI 可處理段括弧 / 帶 3 判定句深藍塊)。
  · 右:人力堆疊(高度按人數比例)+ 紅色引線 + 成長方向斜線 + 三階台階圖示。

以下帶狀純文字元素**已移出本圖**,改由 build_deck_v4.py 以投影片文字框放置
(完整文字與擺放位置見 module-level 的 SLIDE_TEXT):
  平均編制口徑算式帶(含三格與證據等級行)· 算式帶下的引言與徵調研發那一行 · 口徑分隔句 ·
  界定小字(兩個母體警語之一)· 業務基準帶三格 + 帶底母體警語 ·
  壓力測試框(含「現況 4.1 天 -> 4.4 人」與 Hopp & Spearman, 2011, chaps. 7-9 in-text 標記)·
  吞吐量落點框(本輪新增,圖內已無 26% 寬的容身處)· 成長段四行文字 + 階梯佐證兩句 ·
  頁腳「四倍以上」單行。

紅線:
- 畫布固定 newfig(12.2, 5.7);🚫 不得為了塞內容放大畫布。
- 圖不畫投影片標題、不畫頁首進度指示(那兩樣由組版程式負責)。
- 色值只取自 make_figs_v4 的色票常數(ORANGE #E8833A / NAVY #1F4E79 ...)。
- 全圖最小字級 fs=9;負號一律 ASCII hyphen;不用 emoji / 全形減號 / 破折號。
- 主圖不得出現任何「Y 軸 = 人力」的柱狀圖。
- 🚫 作廢數字一個都不得出現:4.4 分 · 120 人時 · 27.7-38.7 · 69%-97% · 3.5-4.8 人 ·
  119.9-167.5 · 15-21 人 · 10-16 人 · 3.0/7.5/15.0 人 · 13 倍 · 全程 5 天。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    plt, FancyArrowPatch, FancyBboxPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT, RED,
    newfig, save, assert_min_fontsize,
)

# ---- 本圖用到的中性灰階(非色相,不屬色票語意色) -------------------
INK = "#333333"          # 內文深灰
INK2 = "#5A5A5A"         # 次級灰
FLAG = "#8C8C8C"         # 旗標灰(規格指定)
STACK_MID = "#E0B84C"    # 人力堆疊中層黃(規格指定)

# ---- 版面常數(0-1 座標 = 12.2 x 5.7 吋畫布)-----------------------
L0, L1 = 0.010, 0.688          # 左主圖欄
S0, S1 = 0.706, 0.945          # 右側欄

# 帶 1 waterfall 的 X 軸:0 - 4.5 個工作日(實際用掉 4.1 天)
PX0 = 0.030
PX_AXIS_END = 0.513
DAY = (PX_AXIS_END - PX0) / 4.5
X_ANALYSIS_END = PX0 + 3.6 * DAY      # 分析段結束(第 3.6 天)
X_DONE = PX0 + 4.1 * DAY              # 客戶收到答覆(第 4.1 天)

# 帶 2 單件爭議拆解:🔴 五段**按天數比例**畫(不是五等欄)。
# 天數取區間中位:排隊 0-1 -> 0.5 · 撈數據 0.5 · 判讀 1-3 -> 2.0 · 覆核 0.5 · 回信 0.5,合計 4.0。
# 段 2 + 段 3 = 2.5 / 4.0 = 62.5%,落在標註的 60%-64% 內 —— 長度即論證,不得為了塞字改比例。
BX0, BX1 = 0.030, 0.556
SEG_DAYS = (0.5, 0.5, 2.0, 0.5, 0.5)
SEG_UNIT = (BX1 - BX0) / sum(SEG_DAYS)

# ==================================================================
# 移出 PNG、必須由投影片原生文字框承載的內容(組版程式直接 import 取用)
#   from figs.fig_v4_02 import SLIDE_TEXT
# 🔴 取代 notes/14 的「區塊 1」(那份的數字整組已作廢)。
# 版位建議(內容區 12.2 x 5.7 吋,圖片置入 scale 1.0、置中):
#   【上帶 約 1.40 吋】A1 / A2 / A3
#   【圖片 約 2.80 吋】
#   【下帶 約 1.45 吋,左 66% / 右 34% 兩欄】左欄 B1 / D / B2 / B3;右欄 F / C1 / C2;最底 E
# 所有數字區間一律 ASCII hyphen;移出文字最小 9pt,算式列最小 10pt。
# ==================================================================
SLIDE_TEXT = {
    "A1_TITLE": dict(
        slot="TOP", fs=12, color=INK, bold=True, align="left",
        text="平均編制口徑:每日工作量 ÷ 每日產能",
        note="規格明訂不可省 —— 它是「本帶與主圖是兩個口徑」的宣告。",
    ),
    "A1_CELL1": dict(
        slot="TOP", width="36%", fc="#F7F7F7",
        rows=[
            dict(fs=11, color=NAVY, bold=True, text="例行批次複核 · 全量"),
            dict(fs=13, color=INK, text="3,000 筆 × 20 秒 ÷ 3,600 = 16.7 人時/天"),
            dict(fs=9, color=INK2,
                 text="證據等級:營運端的實務估計,尚未以計時量測驗證"),
        ],
    ),
    "A1_CELL2": dict(
        slot="TOP", width="40%", fc="#F7F7F7",
        rows=[
            dict(fs=11, color=NAVY, bold=True,
                 text="客戶爭議深入判讀 · 客戶回頭標記的 5-10%"),
            dict(fs=13, color=INK,
                 text="3,000 筆 × 5-10% × 5.25 分 ÷ 60 = 13.1-26.2 人時/天"),
            dict(fs=9, color=INK2,
                 text="證據等級:由一次實際判讀反推(5 人 × 3.6 天 × 8 小時 ÷ 1,647 筆)"),
        ],
    ),
    "A1_CELL3": dict(
        slot="TOP", width="24%", fc="#3F3F3F",
        rows=[
            dict(fs=14, color="white", bold=True,
                 text="合計 29.8-42.9 人時/天 ÷ 40 人時/天"),
            dict(fs=14, color="white", bold=True,
                 text="= 利用率 74%-107%,折算 3.7-5.4 人",
                 emphasis={"107%": ORANGE, "5.4": ORANGE}),
            dict(fs=11, color="white", fc=ORANGE, badge=True,
                 text="上緣已破 100%"),
            dict(fs=9, color="#CFCFCF",
                 text="本格為提案人依現有單價所做的推算;此處的『折算人數』是平均編制,"
                      "不是任何一天的同時在線人力。下緣 74% 仍低於產能 —— "
                      "本頁主張的是尖峰做不到,不是天天做不完。"),
        ],
        note="🔴「107%」與「5.4」兩個值必須以橘色 #E8833A 標示,不可與其他數字同色;"
             "橘色徽章「上緣已破 100%」貼在該行右端。",
    ),
    "A2_PULLQUOTE": dict(
        slot="TOP", fs=13, color=NAVY, bold=True, align="left", rule="4px #1F4E79 左直條",
        text="平均看起來還好,尖峰時這五個人已經不夠。",
        second=dict(fs=11, color=INK,
                    text="→ 這就是尖峰要徵調 7 位研發工程師的原因 —— 不是管理失當,是算術的必然。"),
        note="舊句「在平均意義上,今天這五個人是剛剛好」建立在 69%-97% 的舊算術上,已作廢。",
    ),
    "A3_DIVIDER": dict(
        slot="TOP", fs=10, color=INK2, align="center",
        rule="1pt #BFBFBF 全寬水平線,線上置中白底無框標籤,線上下各留 2% 高度",
        text="以下換一個口徑:不是每天要幾個人,是那一件的時間怎麼被用掉",
    ),
    "B1_SCOPE": dict(
        slot="BOTTOM_LEFT", fs=10, color=INK, align="left", rule="1pt #8A8A8A 上框線",
        rows=[
            "帶 1 的天數是這一件批次判讀(4.1 天)、帶 2 的天數是單件客戶爭議(2.5-5.5 天),兩者不是同一個母體;",
            "單件爭議的時效基準與量測落在下方業務基準帶與「效益與衡量」那一頁。",
        ],
        note="規格明訂不可省、不可縮成腳註,字級不得低於 10。",
    ),
    "D_STRESS": dict(
        slot="BOTTOM_LEFT", fc="#FFF7E0", ec="#E0C271",
        title=dict(fs=11, color=ORANGE_DARK, bold=True,
                   text="壓力測試:完美平行化下的理論下限(非人力需求實證)"),
        rows=[
            dict(fs=10, color=INK,
                 text="同一份 144 人時的分析,若能完美平行化:現況 4.1 個工作日 -> 4.4 人;"),
            dict(fs=10, color=INK,
                 text="壓進 2 個工作日 -> 9.0 人;壓進 1 個工作日 -> 18.0 人。"
                      "算式:144 人時 ÷(工作日數 × 8 小時)"),
            dict(fs=10, color=ORANGE_DARK, bold=True,
                 text="而實際投入是 5 人 —— 這條公式低估約 12%,這是它的自我校準點。"),
            dict(fs=10, color=INK,
                 text="批次複核每天必須做完,無壓縮空間;可被時效壓縮的是爭議判讀那一條。"),
            dict(fs=9, color=INK2,
                 text="四項未驗證假設:工作已全部到齊 · 任務可任意切分 · 無協調與 QA 成本 · "
                      "加人仍線性加速。因此這是下限,不是人力需求;實際節奏見圖上帶 1。"),
        ],
        intext=dict(fs=9, color=INK2, align="right", pad_px=8,
                    text="(Hopp & Spearman, 2011, chaps. 7-9)"),
        note="🔴 本輪補上「現況 4.1 天 -> 4.4 人」那一列(自我校準點)與 chaps. 7-9 定位。"
             "🚫 不得再印成無定位的「(Hopp & Spearman, 2011)」;這是本頁唯一的公開文獻 in-text 標記,刪了本頁就沒有引用。"
             "🚫 框內不得出現 2.5 倍 / 5 倍,也不得以「那一件交付花了 5 天」當基準。"
             "🚫 已作廢:120 人時 · 3.0 / 7.5 / 15.0 人。",
    ),
    "B2_BASELINE": dict(
        slot="BOTTOM_LEFT", fc="#F7F7F7", ec="#8A8A8A",
        left=[
            dict(fs=13, color=INK, bold=True,
                 text="基準:現況單件爭議 2-5 天(從分析到回信的完整鏈路)"),
            dict(fs=13, color=ORANGE, bold=True,
                 text="現況約半數爭議超過兩天。"),
            dict(fs=9, color=INK2,
                 text="營運端的估計值(「大概一半」),尚未以工單時戳量測 —— "
                      "當責:複核營運主管 · 期限:第 6 週交出正式逾時率 · 會改變的決策:G1 是否續行後段。"),
        ],
        mid=[
            dict(fs=13, color=INK, text="客戶期望:2 天內;單純案件當天"),
            dict(fs=10, color=INK2, bold=True, text="客戶期望,非已簽訂之服務水準協議"),
        ],
        right=[
            dict(fs=10, color=INK, text="約半數超過兩天為營運端估計;正式逾時率與時間拆解同批,W1-6 交出。"),
            dict(fs=10, color=INK, text="當責:複核營運主管 · 期限:第 6 週 · 會改變的決策:G1 是否續行後段。"),
        ],
        note="🔴 左格第二行「現況約半數爭議超過兩天。」是本頁唯一把缺口講成"
             "客戶已在承受的事實的地方,放大字級是刻意的,不可省、不可縮字級。",
    ),
    "B3_POPULATION": dict(
        slot="BOTTOM_LEFT", fs=9, color=INK2, align="center",
        text="本帶與圖上帶 1 是兩個母體:帶 1 是一件 1,647 筆的批次判讀,"
             "本帶與圖上帶 2 才是單件客戶爭議。兩者不得互相換算。",
    ),
    "F_THROUGHPUT": dict(
        slot="BOTTOM_RIGHT", fc="#EAF1F8", ec=NAVY,
        rows=[
            dict(fs=10, color=INK,
                 text="若這兩段交給地端設備跑:全客戶 13,000 筆/天,約 2.2-3.5 小時跑完。"),
            dict(fs=10, color=INK,
                 text="設備佔用率約 9%-14% —— 量不是瓶頸,瓶頸是判準與驗證。"),
            dict(fs=9, color=INK2,
                 text="⚠️ 估算,非實測(依公開模型的抽幀吞吐推估;來源表格自標「估算」)。"
                      "當責:提案人 · 期限:第 6 週隨評估底座一併實測 · 會改變的決策:設備台數與 G1 續行。"),
        ],
        note="🔴 本輪新增。規格原定位在圖內帶 2 右端外側,但圖內該處已被"
             "「非 AI 段 36%-40%」兩行佔滿,26% 寬的框放不下 → 依裁決 O「塞不下砍內容」移出。"
             "🔴「估算,非實測」六個字不可省、不可縮字級、不可移到別處。"
             "🚫 框內不得出現任何金額、設備台數,不得由 2.2-3.5 小時反推任何人力節省數,"
             "也不得與任何一條人時算式並排比較。",
    ),
    "C1_GROWTH": dict(
        slot="BOTTOM_RIGHT",
        rows=[
            dict(fs=11, color=NAVY, bold=True,
                 text="目前全球上線約 5 萬台;13,000 ÷ 50,000 ≈ 0.26 筆/台/天。"),
            dict(fs=11, color=ORANGE_DARK, bold=True,
                 text="售出台數是上限,上線台數是已實現的量。"),
            dict(fs=10, color=INK,
                 text="兩者的落差,就是我們接下來要承接、但排不了程的工作量;開通的時點由客戶決定。"),
            dict(fs=10, color=INK2,
                 text="第 6 週對齊售出、開通與在線三個分母;成長不納入目前的回報估算。"
                      "當責:複核營運主管(交付物列入評估底座那一包)· 期限:第 6 週 · "
                      "會改變的決策:分母對齊之後才決定成長要不要進入任何回報估算。"),
        ],
        note="🔴 在線 5 萬台可以寫,售出台數仍不可寫。"
             "🚫 不得由 0.26 筆/台/天回推任何單客戶或單車事件率;"
             "不得出現任何月增裝機台數、不得給已售對已上線的比率。",
    ),
    "C2_STEP": dict(
        slot="BOTTOM_RIGHT", fc="#FFF7E0", ec="#E0C271",
        rows=[
            dict(fs=10, color=INK,
                 text="階梯不是斜坡:一個大型車隊 ≈ 全客戶每日事件量的 23.1%(3,000 ÷ 13,000 筆/天)。"),
            dict(fs=10, color=INK, text="目前正在洽談中的案子裡,就有一個同級規模的車隊。"),
        ],
        note="三階台階圖示已留在圖裡並附「階梯,不是斜坡」標題,框內不必再畫圖示。",
    ),
    "E_FOOTER": dict(
        slot="FOOTER", fs=10, color=INK, bold=True, align="center",
        text="若涵蓋全部既有客戶,複核量將達現況四倍以上。",
    ),
    "_STILL_BY_DECK": "投影片標題、右上角五格進度指示(本頁第 2 格「AI 機會」填深藍 #1F4E79,"
                      "其餘 20% 灰)。圖裡一律不畫,維持原樣。",
}


def _line(ax, x0, x1, y0, y1, color, lw=1.0, ls="-", z=5, alpha=1.0):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls,
            zorder=z, alpha=alpha, solid_capstyle="butt")


def _rect(ax, x, y, w, h, fc, ec="none", lw=1.0, ls="-", z=3):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def _round(ax, x, y, w, h, fc, ec, lw=1.2, z=3, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


# ==================================================================
# 一、主圖:那一件判讀的 latency waterfall(帶 1)
# ==================================================================
def _waterfall(ax):
    # 圖內小標 + 母體標籤(規格「不可省」;是這張圖自己的標題,非投影片標題)
    ax.text(L0 + .004, 0.9945,
            "那一件判讀,時間是這樣被用掉的;而爭議案件的時間,現在也拆開了",
            ha="left", va="top", fontsize=13, color=INK, fontweight="bold", zorder=6)
    ax.text(L0 + .004, 0.9550,
            "這一件 = 1,647 筆事件的批次判讀(某小型車隊 · 單月 · 4 台車 · 23 天)"
            " · 證據等級:已發生的實績",
            ha="left", va="top", fontsize=10, color=INK2, zorder=6)

    # --- X 軸:時間(工作日),刻度每 1 個工作日一格 ----------------
    ay = 0.8975
    _line(ax, PX0, PX_AXIS_END, ay, ay, "#8A8A8A", lw=1.2, z=5)
    for d in range(5):
        x = PX0 + d * DAY
        _line(ax, x, x, ay, ay - .010, "#8A8A8A", lw=1.2, z=5)
        ax.text(x, ay + .003, str(d), ha="center", va="bottom",
                fontsize=10, color=INK2, zorder=6)
    ax.text(PX_AXIS_END + .012, ay + .003, "工作日", ha="left", va="bottom",
            fontsize=10, color=INK2, fontweight="bold", zorder=6)

    # --- 帶 1:1,647 筆批次的實際節奏(3.6 天分析 + 0.5 天整理回信)---
    # 🔴 本輪刪掉帶內第三行「每筆深入判讀 5.25 分」:該算式的正式落點是移出的
    #    算式帶格 2(SLIDE_TEXT["A1_CELL2"]),留在圖上是重複;省下的縱向空間
    #    正好給本輪新增的因果句與兩條分述,畫布因此不必放大(裁決 O)。
    b1b, b1t = 0.8035, 0.8885
    _rect(ax, PX0, b1b, X_ANALYSIS_END - PX0, b1t - b1b, ORANGE, z=3)
    _rect(ax, X_ANALYSIS_END, b1b, X_DONE - X_ANALYSIS_END, b1t - b1b,
          ORANGE_DARK, z=3)
    _line(ax, X_ANALYSIS_END, X_ANALYSIS_END, b1b, b1t, "white", lw=1.6, z=5)

    cxa = (PX0 + X_ANALYSIS_END) / 2
    ax.text(cxa, 0.8735, "分析:3.6 個工作日", ha="center", va="top",
            fontsize=13, color="white", fontweight="bold", zorder=6)
    ax.text(cxa, 0.8355, "5 位專職分析人員並行 · 合計 144 人時",
            ha="center", va="top", fontsize=10, color="white", zorder=6)

    # 段末小旗標(貼在 4.1 天處)+ 右側三行說明
    my = (b1b + b1t) / 2
    ax.add_patch(plt.Polygon([[X_DONE, my + .015], [X_DONE + .013, my],
                              [X_DONE, my - .015]], closed=True, fc=FLAG,
                             ec=FLAG, zorder=5))
    cox = X_DONE + .022
    ax.text(cox, 0.8815, "客戶收到答覆 · 第 4.1 天", ha="left", va="top",
            fontsize=11, color=FLAG, fontweight="bold", zorder=6)
    ax.text(cox, 0.8455, "末段 0.5 天 = 整理與回信", ha="left", va="top",
            fontsize=11, color=ORANGE_DARK, fontweight="bold", zorder=6)
    ax.text(cox, 0.8115, "(不含在 144 人時內,未量測)", ha="left", va="top",
            fontsize=10, color=INK2, zorder=6)


# ==================================================================
# 二、帶 2:單件客戶爭議的時間拆解(Q45;五格問號已填實)
# ==================================================================
def _breakdown(ax):
    # 帶頭:母體宣告 + 證據等級。右側是誠實載體(🔴 不得寫成交叉驗證)。
    ax.text(L0 + .004, 0.7795,
            "另一個母體:單件爭議的時間拆解,合計 2.5-5.5 天(營運端估計,非量測)",
            ha="left", va="top", fontsize=10, color=NAVY,
            fontweight="bold", zorder=6)
    ax.text(L1, 0.7795, "與登記在案的 2-5 天吻合,但同一營運來源,不算交叉驗證",
            ha="right", va="top", fontsize=10, color=INK2, zorder=6)

    b2b, b2t = 0.6675, 0.7495
    # (段名, 天數標籤, 是否 AI 可處理, 是否為區間段)
    # 🔴 段名已依比例寬度收短(等待排隊 / 撈數據 / 報告回信):
    #    塞不下就砍字,🚫 不得為了塞字把任何一段畫寬(裁決 O + 規格「長度即論證」)。
    cells = [
        ("等待排隊", "0-1 天", False, True),
        ("撈數據", "0.5 天", True, False),
        ("判讀", "1-3 天", True, True),
        ("內部覆核", "0.5 天", False, False),
        ("報告回信", "0.5 天", False, False),
    ]
    _round(ax, BX0, b2b, BX1 - BX0, b2t - b2b, "white", "#5A5A5A", lw=1.1, z=3)
    xs = [BX0]
    for d in SEG_DAYS:
        xs.append(xs[-1] + d * SEG_UNIT)
    # AI 可處理段畫成**一整塊連續**的高亮(規格:段 2 + 段 3 的區塊必須連續且明顯佔多數),
    # 中間的段界線隨後以虛線疊上去 —— 不留白色縫隙,免得看起來像兩件不相干的事。
    _rect(ax, xs[1] + .0015, b2b + .0015, (xs[3] - xs[1]) - .003,
          (b2t - b2b) - .003, ORANGE_LIGHT, z=4)
    for i, (lb, days, is_ai, is_range) in enumerate(cells):
        cx0, cw = xs[i], xs[i + 1] - xs[i]
        if i:
            # 區間段的邊界畫虛線:這條界線會滑動(0-1 / 1-3 是區間,不是定值),
            # 對應規格「不得只畫單一寬度冒充確定值」。
            rng = is_range or cells[i - 1][3]
            _line(ax, cx0, cx0, b2b + .006, b2t - .006, "#8A8A8A",
                  lw=1.0, ls=(0, (3, 3)) if rng else "-", z=5)
        ax.text(cx0 + cw / 2, 0.7435, lb, ha="center", va="top",
                fontsize=11, color=INK if is_ai else INK2, zorder=6)
        ax.text(cx0 + cw / 2, 0.7095, days, ha="center", va="top",
                fontsize=13, color=ORANGE_DARK if is_ai else INK,
                fontweight="bold", zorder=6)

    # 右側:拆解已到手,量測版仍待交
    ax.text((BX1 + L1) / 2 + .004, 0.7085,
            "初步拆解已到手;\nW1-6 交出量測版",
            ha="center", va="center", fontsize=11, color=NAVY,
            fontweight="bold", linespacing=1.3, zorder=6)

    # --- AI 可處理段括弧(撈數據 + 判讀 兩段相鄰;寬度即 62.5%)-----
    ax0 = xs[1]
    ax1 = xs[3]
    _line(ax, ax0, ax1, 0.6595, 0.6595, ORANGE_DARK, lw=1.8, z=5)
    _line(ax, ax0, ax0, 0.6595, 0.6655, ORANGE_DARK, lw=1.8, z=5)
    _line(ax, ax1, ax1, 0.6595, 0.6655, ORANGE_DARK, lw=1.8, z=5)
    ax.text((ax0 + ax1) / 2, 0.6535,
            "AI 可處理段:1.5-3.5 天 = 全程的 60%-64%",
            ha="center", va="top", fontsize=12, color=ORANGE_DARK,
            fontweight="bold", zorder=6)

    ax.text(L1, 0.6535, "非 AI 段(排隊 + 覆核 + 回信)只佔 36%-40%,",
            ha="right", va="top", fontsize=10, color=INK2, zorder=6)
    ax.text(L1, 0.6255, "而排隊本身只有 0-1 天,那是排班解得掉的唯一一段。",
            ha="right", va="top", fontsize=10, color=INK2, zorder=6)

    # --- 🔴 本輪新增:因果句(本頁與 P1 的接點,規格明訂不可省)-----
    # 有了這一句,兩段高亮才是「同一個技術缺陷的兩個症狀」,
    # 論證因此從流程改善變成 AI 立案。
    _rect(ax, BX0 - .0055, 0.5903, .0035, 0.0292, NAVY, z=5)
    ax.text(BX0, 0.6195,
            "這兩段之所以慢,是同一個原因:模型看不到畫面外的東西。",
            ha="left", va="top", fontsize=12, color=NAVY,
            fontweight="bold", zorder=6)

    # 兩條分述:各配一枚與帶 2 高亮格同色的方形標記,句首直接寫出段名
    # (規格原寫「細引線指回段 2 / 段 3」,引線走廊被括弧與括弧標註佔滿,
    #  改以同色標記 + 段名完成繫結;見檔頭「規格偏離」。)
    for mx, tx, s in ((BX0, BX0 + .014,
                       "撈數據慢,是因為人要自己去查那個位置與那段路的速限。"),
                      (0.385, 0.399, "判讀慢,是因為模型只拿到一張圖。")):
        _rect(ax, mx, 0.5633, .008, .014, ORANGE_LIGHT,
              ec=ORANGE_DARK, lw=0.9, z=5)
        ax.text(tx, 0.5825, s, ha="left", va="top", fontsize=10,
                color=INK, zorder=6)

    # --- 帶 3:判定句(本圖唯一的深藍色塊)-------------------------
    b3b, b3t = 0.5115, 0.5515
    _rect(ax, L0 + .004, b3b, L1 - L0 - .004, b3t - b3b, NAVY, z=3)
    ax.text((L0 + L1) / 2, (b3b + b3t) / 2,
            "規則不變:主要延遲落在 AI 可處理段 -> 續行後段,否則轉排班。"
            "拆解已指向續行,待量測確認。G1 判。",
            ha="center", va="center", fontsize=12, color="white",
            fontweight="bold", zorder=6)


# ==================================================================
# 三、右側側欄:人力堆疊 + 成長方向
# ==================================================================
def _sidebar(ax):
    sx0, sx1 = S0, S1

    # --- 人力堆疊(高度按人數比例:5 : (未宣稱) : 7)---------------
    unit = 0.0135
    top_t = 0.992
    top_b = top_t - 7 * unit
    mid_t = top_b
    mid_b = mid_t - 0.036
    bot_t = mid_b
    bot_b = bot_t - 5 * unit

    # 頂層:2px 外框 + 陰影(讓紅塊在版面上「明顯不該在那裡」)
    _rect(ax, sx0 + .003, top_b - .0015, sx1 - sx0, top_t - top_b, "#9A9A9A", z=2)
    _rect(ax, sx0, top_b, sx1 - sx0, top_t - top_b, RED, ec=RED, lw=2.0, z=3)
    ax.text((sx0 + sx1) / 2, (top_b + top_t) / 2,
            "+ 7 位研發工程師\n尖峰時離開本職",
            ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", linespacing=1.3, zorder=6)

    _rect(ax, sx0, mid_b + .0015, sx1 - sx0, mid_t - mid_b - .003, STACK_MID, z=3)
    ax.text((sx0 + sx1) / 2, (mid_b + mid_t) / 2, "+ 產品經理與主管 · 處理客訴",
            ha="center", va="center", fontsize=11, color=INK,
            fontweight="bold", zorder=6)

    _rect(ax, sx0, bot_b, sx1 - sx0, bot_t - bot_b, NAVY, z=3)
    # 橘色母題:底層方塊的橘色識別條(沿用 P1 方塊 C 的色值)
    _rect(ax, sx0, bot_b, 0.0045, bot_t - bot_b, ORANGE, z=4)
    ax.text((sx0 + sx1) / 2, 0.8435, "5 位專職分析人員 · 常態編制",
            ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", zorder=6)
    ax.text((sx0 + sx1) / 2, 0.8125, "折算 3.7-5.4 人 · 尖峰已不夠",
            ha="center", va="center", fontsize=10, color=ORANGE_LIGHT, zorder=6)

    # 頂層右側紅色引線 -> 機會成本(本頁字級第二大的文字)
    ly = (top_b + top_t) / 2
    oy = 0.752
    _line(ax, sx1, 0.968, ly, ly, RED, lw=1.6, z=5)
    _line(ax, 0.968, 0.968, ly, oy, RED, lw=1.6, z=5)
    ax.add_patch(FancyArrowPatch((0.968, oy), (0.898, oy),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=RED, lw=1.6, zorder=5))
    ax.text(S0, oy, "機會成本:\n開發產能被拿去補分析產能",
            ha="left", va="center", fontsize=12, color=RED,
            fontweight="bold", linespacing=1.25, zorder=6)

    # --- 成長方向:方向性斜線(不承載任何數值)---------------------
    gy = 0.560
    _line(ax, 0.716, 0.716, gy, 0.666, "#A6A6A6", lw=1.0, z=4)
    _line(ax, 0.716, 0.985, gy, gy, "#A6A6A6", lw=1.0, z=4)
    ax.add_patch(FancyArrowPatch((0.726, 0.568), (0.965, 0.654),
                                 arrowstyle="-|>", mutation_scale=15,
                                 color=ORANGE, lw=2.0, zorder=5))
    ax.text(0.716, 0.678, "事件量", ha="left", va="top", fontsize=10,
            color=INK2, zorder=6)
    ax.text(0.985, 0.556, "時間", ha="right", va="top", fontsize=10,
            color=INK2, zorder=6)

    # --- 三階小台階圖示(第三階虛線 = 尚未發生)+ 圖示標題 ----------
    st_x, st_w, st_b, st_u = 0.706, 0.019, 0.5125, 0.0095
    for i in range(3):
        x = st_x + i * st_w
        h = (i + 1) * st_u
        if i < 2:
            _rect(ax, x, st_b, st_w, h, ORANGE, ec=ORANGE_DARK, lw=0.8, z=5)
        else:
            _rect(ax, x, st_b, st_w, h, "none", ec=ORANGE_DARK, lw=1.1,
                  ls=(0, (3, 2)), z=5)
    ax.text(0.775, 0.523, "階梯,不是斜坡", ha="left", va="center",
            fontsize=11, color=ORANGE_DARK, fontweight="bold", zorder=6)


# ==================================================================
def build():
    # 🔴 裁決 O:畫布固定 12.2 x 5.7 吋,不得放大。
    fig, ax = newfig(12.2, 5.7)

    # 座標尺度鎖死為「1.0 x 單位 = 12.2 吋 / 1.0 y 單位 = 5.7 吋」,
    # 再把 axes 收到實際用到的那塊(X0..X1, Y0..Y1)。
    # save() 用 bbox_inches="tight" + pad_inches=0 → 輸出寬 <= 0.980 x 12.2 吋,
    # 置入 12.2 吋內容區縮放比 = 1.0,fs 值即真實 pt。
    X0, X1 = 0.010, 0.990
    Y0, Y1 = 0.503, 0.996
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    ax.set_position([0.010, 0.300, (X1 - X0), (Y1 - Y0)])

    _waterfall(ax)
    _breakdown(ax)
    _sidebar(ax)

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_02")
