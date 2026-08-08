# -*- coding: utf-8 -*-
"""P10 用圖 —— 資源、當責與請求(裁決 O 版:畫布鎖 12.2 x 5.7)。

視覺規格來源:v4/notes/04_十頁內容_v2.md 的「# P10 · 資源、當責與請求 / ## 視覺規格」。
畫布裁決來源:v4/notes/12_出圖稽核與畫布裁決.md §二 裁決 O。

🔴 裁決 O 的三條硬規則(改圖時不得再破):
  1. 畫布固定 newfig(12.2, 5.7) —— 置入投影片縮放比 = 1.0,fs=9 就是真的 9pt。
     內容塞不下時砍內容,**不得放大畫布**(上一版被畫到 19.6 吋,fs9 落地只剩 5.7pt)。
  2. 最小字級 fs=9,不得下修;build() 結束前呼叫 assert_min_fontsize(fig) 驗。
  3. 帶狀純文字元素移出圖,改由 build_deck_v4.py 以投影片文字框放(向量、永遠清晰)。

留在圖裡的(靠位置/連線/顏色/比例傳達意義,拆掉就講不清楚):
  左:人月矩陣(6 工作包 × 5 角色 + 小計 / 角色合計 / PM / 總計,色階 + 斜線紋)
      + 斜線紋與「內部前移」兩條圖例
  右:RACI 六列 × 九欄(A 實心深藍圓、R 橘框圓、C/I 淺灰)+ 字母圖例
      + 相依帶(雙軌 + 待共同確認箭頭 + 實虛線圖例)+ 橘色母題(不加文字)

y >= RESERVED_TOP(4.35 吋)的底帶刻意留白,留給組版程式疊原生文字框
(兩個算式框移出圖的落點)。_check_layout() 會 assert 這條帶上沒有任何文字。

移出圖、改由組版程式放的(全部是純文字,靠左對齊的 × / = 不傳達圖形關係;
完整逐字清單見交付回報的 moved_to_slide,一個字都不能少):
  算式框一、算式框二、放行條件框、兩框下方三行註記與框間分隔說明、箭頭上的反事實說明、
  利害關係人窄帶、六個月後三格帶 + Q-22、Q-19、組織障礙一行、相依帶下方的請求行、
  WP-E 待確認註記全文、第一段人月拆解算式全文、RACI 六方當責的完整職稱與複核營運主管註記、
  結論條三行。

不畫(由組版程式負責):頁首標題、右上角五格進度指示。

版面座標一律以「吋」思考,再由 X()/Y() 換算成 0-1 座標,避免字塊高度用猜的而互相壓字。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matplotlib.text import Text  # noqa: E402

from make_figs_v4 import (  # noqa: E402
    plt, FancyBboxPatch, FancyArrowPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT, GREY, LIGHT,
    newfig, save, assert_min_fontsize,
)

plt.rcParams["hatch.linewidth"] = 0.6

DARK = "#333333"     # 沿用 make_figs_v4.panel() 的內文色
ROW_BG_A = 0.5       # 列名欄底 = LIGHT 加透明度(規格「12% 灰底」),不另立色值

# 🔴 裁決 O:畫布尺寸鎖死,不得為了塞內容而放大。
W_IN, H_IN = 12.2, 5.7
FS_TINY, FS_BODY, FS_HEAD = 9.0, 10.0, 10.5

# 版心(吋)—— 左右兩欄各 5.85 寬,中間 0.30 吋槽溝
L0 = 0.10
R0, R1 = 6.25, 12.10

# 底帶留白起點(吋):此線以下不畫任何東西,留給組版程式的原生文字框。
RESERVED_TOP = 4.35

# 容器框登記簿:每個 rect / roundbox / softbox 都登記,供 _check_layout() 驗文字未溢出。
CONTAINERS = []


def X(i):
    return i / W_IN


def Y(i):
    """i = 距畫布上緣的吋數。"""
    return 1.0 - i / H_IN


def line(ax, xi, yi, s, fs=FS_BODY, c=DARK, bold=False, ha="left", va="top", lsp=1.5):
    # NT$ / A$ 的 $ 會被 matplotlib 當成 mathtext 起訖符,整段改用 rm 字型而缺中文字,
    # 所以一律跳脫成 \$。
    return ax.text(X(xi), Y(yi), s.replace("$", r"\$"), fontsize=fs, color=c,
                   ha=ha, va=va, zorder=8, linespacing=lsp,
                   fontweight="bold" if bold else "normal")


def rect(ax, xi, yi, w, h, fc, ec="white", lw=1.0, hatch=False, z=3, alpha=None):
    CONTAINERS.append((xi, yi, w, h))
    ax.add_patch(Rectangle((X(xi), Y(yi + h)), X(w), h / H_IN,
                           fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z))
    if hatch:
        # 斜線紋壓低透明度,免得白線把格內 fs=9 的 FTE×週數切成一段一段。
        ax.add_patch(Rectangle((X(xi), Y(yi + h)), X(w), h / H_IN, fc="none",
                               ec="white", lw=0.0, hatch="////", alpha=0.5, zorder=z + 1))


def roundbox(ax, xi, yi, w, h, fc, ec, lw=1.5, ls="-", z=4, register=True):
    if register:
        CONTAINERS.append((xi, yi, w, h))
    ax.add_patch(FancyBboxPatch((X(xi), Y(yi + h)), X(w), h / H_IN,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def raci_mark(ax, xi, yi, letter):
    """A = 實心深藍圓底白字(最重);R = 橘色圓框;C / I = 淺灰字。"""
    if letter == "A":
        ax.text(X(xi), Y(yi), "A", fontsize=9.5, color="white", ha="center",
                va="center", fontweight="bold", zorder=8,
                bbox=dict(boxstyle="circle,pad=0.22", fc=NAVY, ec=NAVY, lw=1.0))
    elif letter == "R":
        ax.text(X(xi), Y(yi), "R", fontsize=9.5, color=ORANGE_DARK, ha="center",
                va="center", fontweight="bold", zorder=8,
                bbox=dict(boxstyle="circle,pad=0.22", fc="white", ec=ORANGE, lw=1.2))
    else:
        ax.text(X(xi), Y(yi), letter, fontsize=FS_TINY, color=GREY, ha="center",
                va="center", zorder=8)


# ------------------------------------------------------------------
# 資料(全部取自 P10 視覺規格,未自行編造)
# ------------------------------------------------------------------
ROLES = ["資料科學", "資料工程", "軟體工程", "業務分析", "複核營運"]

# (工作包, {角色索引: (上層 FTE×週數, 下層 人月)}, 小計, 是否屬第一段)
WPS = [
    ("WP-A 評估底座 W1-6",  {0: ("0.5×6w", "0.69"), 4: ("1.0×6w", "1.39")}, "2.08", True),
    ("WP-B 標註品質 W3-10", {1: ("0.5×8w", "0.92"), 4: ("1.0×8w", "1.85")}, "2.77", True),
    ("WP-C 脈絡特徵 W5-12", {1: ("0.5×8w", "0.92"), 2: ("1.0×8w", "1.85")}, "2.77", True),
    ("WP-D 爭議回覆 W8-16", {2: ("0.5×9w", "1.04"), 3: ("0.5×9w", "1.04")}, "2.08", False),
    ("WP-E 對照重訓 W8-24", {0: ("內部前移", "3.00"), 1: ("內部前移", "1.50")}, "4.50", False),
    ("WP-F 治理移交 W20-26", {1: ("0.3×7w", "0.48"), 3: ("0.3×7w", "0.48")}, "0.97", False),
]
ROLE_TOTALS = ["3.70", "3.83", "2.89", "1.52", "3.23"]
SUB_TOTAL = "15.17"

# 圖內用簡稱(欄寬 1.20 吋放不下完整職稱);完整職稱移到投影片文字,一個字都不刪。
RACI_ROWS = ["項目贊助人", "業務負責人", "數據負責人", "技術負責人",
             "複核營運主管", "專案負責人"]
RACI_COLS = ["WP-A\n評估\n底座", "WP-B\n標註\n品質", "WP-C\n脈絡\n特徵", "WP-D\n爭議\n回覆",
             "WP-E\n對照\n重訓", "WP-F\n治理\n移交", "G1\n決策門\nW6", "G2\n決策門\nW12",
             "G3\n決策門\nW24"]
RACI = [
    ["I", "I", "I", "I", "I", "C", "A", "A", "A"],
    ["C", "C", "C", "R", "I", "R", "C", "C", "C"],
    ["C", "A", "C", "I", "C", "R", "C", "C", "C"],
    ["R", "C", "A", "A", "A", "C", "C", "C", "C"],
    ["A", "C", "I", "C", "I", "C", "I", "C", "I"],
    ["R", "R", "R", "R", "R", "A", "R", "R", "R"],
]


def _selfcheck():
    """規格硬規則,違反即為錯圖:每欄只准一個 A;人月一律程式驗算不得手算。"""
    for j, cn in enumerate(RACI_COLS):
        n = sum(1 for i in range(len(RACI_ROWS)) if RACI[i][j] == "A")
        assert n == 1, "RACI 第 %s 欄有 %d 個 A(規格:每欄只准一個)" % (cn.replace("\n", " "), n)
    for j in (6, 7, 8):
        assert RACI[0][j] == "A", "三道決策門的 A 必須落在項目贊助人"
    assert RACI[4][0] == "A" and RACI[4][1] == "C", "複核營運主管:評估底座 A、標註品質 C"

    subs = sum(float(w[2]) for w in WPS)
    assert abs(subs - float(SUB_TOTAL)) < 0.02, "小計欄加總 %.2f != %s" % (subs, SUB_TOTAL)
    assert abs(subs + 3.00 - 18.17) < 0.02, "總計不是 18.17"
    assert abs((2.08 + 1.39 + 0.69 + 0.69) - 4.85) < 0.005, "第一段拆解不等於 4.85"


def _check_layout(fig):
    """裁決 O 的驗收 3:所有 Text 兩兩不重疊、且不溢出所屬容器框與畫布。"""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    fw = fig.get_size_inches()[0] * fig.dpi
    fh = fig.get_size_inches()[1] * fig.dpi
    eps = fig.dpi / 72.0          # 1 pt 容差,吸收字型 descent 的四捨五入

    texts = [t for t in fig.findobj(Text) if t.get_text().strip()]
    bbs = [t.get_window_extent(rend) for t in texts]

    bad = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = bbs[i], bbs[j]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > eps and oy > eps:
                bad.append("重疊 %.1fx%.1fpx:%r vs %r"
                           % (ox, oy, texts[i].get_text()[:18], texts[j].get_text()[:18]))
    assert not bad, "文字兩兩重疊共 %d 處:%s" % (len(bad), bad[:6])

    # 畫布邊界
    out = [t.get_text()[:20] for t, b in zip(texts, bbs)
           if b.x0 < -eps or b.y0 < -eps or b.x1 > fw + eps or b.y1 > fh + eps]
    assert not out, "文字超出畫布共 %d 處:%s" % (len(out), out[:6])

    # 容器框:取「中心落在其中、面積最小」的框當歸屬,再驗全包住
    boxes = []
    for xi, yi, w, h in CONTAINERS:
        boxes.append((xi / W_IN * fw, (xi + w) / W_IN * fw,
                      fh - (yi + h) / H_IN * fh, fh - yi / H_IN * fh, w * h))
    spill = []
    for t, b in zip(texts, bbs):
        cx, cy = (b.x0 + b.x1) / 2.0, (b.y0 + b.y1) / 2.0
        owner = None
        for bx0, bx1, by0, by1, area in boxes:
            if bx0 <= cx <= bx1 and by0 <= cy <= by1 and (owner is None or area < owner[4]):
                owner = (bx0, bx1, by0, by1, area)
        if owner is None:
            continue
        if (b.x0 < owner[0] - eps or b.x1 > owner[1] + eps
                or b.y0 < owner[2] - eps or b.y1 > owner[3] + eps):
            spill.append("%r 溢出 %.1f/%.1f/%.1f/%.1f px"
                         % (t.get_text()[:18], owner[0] - b.x0, b.x1 - owner[1],
                            owner[2] - b.y0, b.y1 - owner[3]))
    assert not spill, "文字溢出容器框共 %d 處:%s" % (len(spill), spill[:6])

    # 底帶留白:任何文字都不得侵入,否則組版程式疊上來的原生文字框會壓到圖
    band_y = fh - RESERVED_TOP / H_IN * fh
    intrude = [t.get_text()[:20] for t, b in zip(texts, bbs) if b.y0 < band_y - eps]
    assert not intrude, ("侵入底帶留白(y >= %.2f 吋)共 %d 處:%s"
                         % (RESERVED_TOP, len(intrude), intrude[:6]))
    print("  版面檢查通過:%d 個文字物件,零重疊、零溢出、底帶留白乾淨。" % len(texts))


def tier(v):
    """單色順序色階(淺橘 -> 深橘),色值只取自色票常數;深色格改白字。"""
    if v < 1.0:
        return ORANGE_LIGHT, DARK
    if v < 2.0:
        return ORANGE, DARK
    return ORANGE_DARK, "white"


# ==================================================================
def build():
    _selfcheck()
    del CONTAINERS[:]
    fig, ax = newfig(W_IN, H_IN)      # 不下 title:頁首標題由組版程式放
    # newfig 用的是預設 subplot 邊界,座標軸只佔畫布約 77%,會讓下面所有以「吋」
    # 算出來的列高縮水三成而壓字。把座標軸拉滿整張畫布,X()/Y() 的吋數才是真的吋。
    ax.set_position([0.0, 0.0, 1.0, 1.0])

    # ==============================================================
    # 左欄上 —— 人月矩陣
    # ==============================================================
    cw_name, cw_role, cw_sub = 1.42, 0.70, 0.93     # 1.42 + 3.50 + 0.93 = 5.85
    xs = [L0 + cw_name + i * cw_role for i in range(5)]
    x_sub = L0 + cw_name + 5 * cw_role

    line(ax, L0, 0.05,
         "人月矩陣〔提案規劃〕　由交付物反推,以 4.33 週/月換算;空格留白不填 0",
         fs=FS_TINY, c=GREY)

    yc = 0.30
    h_head, h_wp, h_sum, h_tot = 0.30, 0.38, 0.30, 0.38

    rect(ax, L0, yc, cw_name, h_head, LIGHT)
    line(ax, L0 + cw_name / 2, yc + h_head / 2, "工作包(人月)", fs=FS_TINY + 0.5, c=DARK,
         bold=True, ha="center", va="center")
    for i, r in enumerate(ROLES):
        rect(ax, xs[i], yc, cw_role, h_head, LIGHT)
        line(ax, xs[i] + cw_role / 2, yc + h_head / 2, r, fs=FS_TINY, c=DARK, bold=True,
             ha="center", va="center")
    rect(ax, x_sub, yc, cw_sub, h_head, LIGHT)
    line(ax, x_sub + cw_sub / 2, yc + h_head / 2, "小計(人月)", fs=FS_TINY, c=DARK,
         bold=True, ha="center", va="center")
    yc += h_head

    for name, cells, sub, seg1 in WPS:
        rect(ax, L0, yc, cw_name, h_wp, LIGHT, alpha=ROW_BG_A)
        line(ax, L0 + 0.06, yc + h_wp / 2, name, fs=FS_TINY, c=DARK, bold=True,
             va="center")
        for i in range(5):
            if i in cells:
                top, val = cells[i]
                fc, tc = tier(float(val))
                rect(ax, xs[i], yc, cw_role, h_wp, fc, hatch=seg1)
                # 兩層都用 va="center":va="bottom" 會以字型 descent 對齊,
                # 中文字塊會比預期高出去而被格線切到。
                # 上層對比:淺橘底走深橘字、深橘底走白字、中間的 ORANGE 底走 DARK
                # (白字壓在 #E8833A 上只有 2.5:1,fs=9 會糊掉)。
                top_c = {ORANGE_LIGHT: ORANGE_DARK, ORANGE_DARK: "white"}.get(fc, DARK)
                line(ax, xs[i] + cw_role / 2, yc + h_wp / 2 - 0.095, top, fs=FS_TINY,
                     c=top_c, ha="center", va="center")
                line(ax, xs[i] + cw_role / 2, yc + h_wp / 2 + 0.095, val, fs=FS_BODY,
                     c=tc, bold=True, ha="center", va="center")
            else:
                rect(ax, xs[i], yc, cw_role, h_wp, "white")
        fc, tc = tier(float(sub))
        rect(ax, x_sub, yc, cw_sub, h_wp, fc)
        line(ax, x_sub + cw_sub / 2, yc + h_wp / 2, sub, fs=FS_HEAD, c=tc, bold=True,
             ha="center", va="center")
        yc += h_wp

    rect(ax, L0, yc, cw_name, h_sum, LIGHT)
    line(ax, L0 + cw_name / 2, yc + h_sum / 2, "角色合計", fs=FS_TINY, c=DARK, bold=True,
         ha="center", va="center")
    for i, v in enumerate(ROLE_TOTALS):
        fc, tc = tier(float(v))
        rect(ax, xs[i], yc, cw_role, h_sum, fc)
        line(ax, xs[i] + cw_role / 2, yc + h_sum / 2, v, fs=FS_BODY, c=tc, bold=True,
             ha="center", va="center")
    rect(ax, x_sub, yc, cw_sub, h_sum, ORANGE_DARK)
    line(ax, x_sub + cw_sub / 2, yc + h_sum / 2, SUB_TOTAL, fs=FS_BODY, c="white",
         bold=True, ha="center", va="center")
    yc += h_sum

    rect(ax, L0, yc, cw_name, h_sum, LIGHT, alpha=ROW_BG_A)
    line(ax, L0 + 0.06, yc + h_sum / 2, "專案負責人(提案人)", fs=FS_TINY, c=DARK,
         bold=True, va="center")
    rect(ax, xs[0], yc, cw_role * 5, h_sum, ORANGE_DARK)
    line(ax, xs[0] + cw_role * 2.5, yc + h_sum / 2,
         "0.5×26w = 3.00 人月(跨全期 PM 投入)", fs=FS_TINY, c="white", bold=True,
         ha="center", va="center")
    rect(ax, x_sub, yc, cw_sub, h_sum, ORANGE_DARK)
    line(ax, x_sub + cw_sub / 2, yc + h_sum / 2, "3.00", fs=FS_BODY, c="white", bold=True,
         ha="center", va="center")
    yc += h_sum

    rect(ax, L0, yc, cw_name + cw_role * 5, h_tot, LIGHT)
    line(ax, L0 + 0.06, yc + h_tot / 2, "總計(六個工作包 + 專案負責人)", fs=FS_TINY + 0.5,
         c=DARK, bold=True, va="center")
    rect(ax, x_sub, yc, cw_sub, h_tot, ORANGE_DARK)
    line(ax, x_sub + cw_sub / 2, yc + h_tot / 2 - 0.085, "約 18.2 人月", fs=FS_BODY,
         c="white", bold=True, ha="center", va="center")
    line(ax, x_sub + cw_sub / 2, yc + h_tot / 2 + 0.090, "〔提案規劃〕", fs=FS_TINY,
         c="white", ha="center", va="center")
    yc += h_tot                                          # yc = 3.86

    # 兩條圖例(解釋圖面上的斜線紋與「內部前移」兩個記號,屬圖不屬文,留在圖裡)
    line(ax, L0, yc + 0.08,
         "斜線紋 = 第一段(W1-6)涵蓋的工作包(與計畫頁甘特同義):WP-A 全部 + WP-B / WP-C 限額探索\n"
         "「內部前移」= 裁決 K 後由 WP-E 內部重排人力,總投入 4.50 人月不變",
         fs=FS_TINY, c=GREY, lsp=1.55)

    # ==============================================================
    # 右欄上 —— RACI 六列 × 九欄
    # ==============================================================
    line(ax, R0, 0.05, "RACI · 六方當責 × 六個工作包 + 三道決策門", fs=FS_HEAD, c=NAVY,
         bold=True)

    lab_w = 1.20
    col_w = (R1 - R0 - lab_w) / 9.0          # = 0.5167
    ry, h_rh, h_rr = 0.34, 0.50, 0.325
    rect(ax, R0, ry, lab_w, h_rh, LIGHT)
    line(ax, R0 + lab_w / 2, ry + h_rh / 2, "當責角色", fs=FS_TINY, c=DARK, bold=True,
         ha="center", va="center")
    for j, cn in enumerate(RACI_COLS):
        x = R0 + lab_w + j * col_w
        rect(ax, x, ry, col_w, h_rh, NAVY if j >= 6 else LIGHT)
        line(ax, x + col_w / 2, ry + h_rh / 2, cn, fs=FS_TINY,
             c="white" if j >= 6 else DARK, bold=True, ha="center", va="center", lsp=1.3)
    ry += h_rh

    for i, rn in enumerate(RACI_ROWS):
        rect(ax, R0, ry, lab_w, h_rr, LIGHT, alpha=ROW_BG_A)
        line(ax, R0 + 0.06, ry + h_rr / 2, rn, fs=FS_TINY, c=DARK, bold=True, va="center")
        for j in range(9):
            x = R0 + lab_w + j * col_w
            rect(ax, x, ry, col_w, h_rr, "white")
            raci_mark(ax, x + col_w / 2, ry + h_rr / 2, RACI[i][j])
        ry += h_rr                                        # ry = 2.79

    line(ax, R0, ry + 0.09,
         "A = 當責(每欄只有一個) · R = 執行 · C = 諮詢 · I = 告知;"
         "三道決策門的 A 一律落在項目贊助人", fs=FS_TINY, c=GREY)

    # ==============================================================
    # 右欄下 —— 相依帶(雙軌 + 待共同確認箭頭)
    # ==============================================================
    up_y, lo_y, rail_h = 3.22, 3.78, 0.28
    roundbox(ax, R0, up_y, 3.10, rail_h, NAVY, NAVY, lw=1.2)
    line(ax, R0 + 1.55, up_y + rail_h / 2, "本案 W1-26:六個工作包(見左表)",
         fs=FS_TINY, c="white", bold=True, ha="center", va="center")
    roundbox(ax, 8.70, lo_y, 3.30, rail_h, "white", GREY, lw=1.2, ls=(0, (4, 3)))
    line(ax, 8.70 + 1.65, lo_y + rail_h / 2, "公司既有的雲端判讀規劃(仍在研擬)",
         fs=FS_TINY, c=GREY, bold=True, ha="center", va="center")
    ax.add_patch(FancyArrowPatch((X(9.05), Y(up_y + rail_h)), (X(9.45), Y(lo_y)),
                                 arrowstyle="-|>", mutation_scale=13, lw=2.0,
                                 color=NAVY, zorder=7))
    # 標籤貼著箭頭起點左側,免得被讀成上軌的圖說
    line(ax, 7.05, up_y + rail_h + 0.04, "我主張的相依關係(待共同確認)",
         fs=FS_TINY, c=NAVY, bold=True)
    line(ax, R0, lo_y + rail_h + 0.08,
         "實線 = 本提案要交付的　　虛線 = 尚未定案", fs=FS_TINY, c=GREY)

    # 全片最後一次出現的橘色母題(人工複核防線,不加文字),收在圖面內容的最末端
    roundbox(ax, R1 - 0.22, lo_y + rail_h + 0.05, 0.22, 0.20, ORANGE, ORANGE_DARK,
             lw=1.2, z=6, register=False)

    # ==============================================================
    # 底帶 y >= 4.35 吋 —— 刻意留白,不畫任何東西
    # 兩個算式框是純文字(靠左對齊的 × / = 不傳達圖形關係),依裁決 O 第 4 條移出圖,
    # 由 build_deck_v4.py 用 PowerPoint 原生文字框疊在這條空白帶上:
    #   置圖後這條帶對應投影片 y 約 5.35-6.75 吋、x 0.55-12.54 吋,
    #   兩框並排、字級 11-12pt(原生向量),比烘進 PNG 的 9pt 更清楚。
    #   完整文字見交付回報的 moved_to_slide 第 1、2 項,一個字都不能少。
    # ==============================================================

    assert_min_fontsize(fig)
    _check_layout(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_10")
