# -*- coding: utf-8 -*-
"""P10 用圖 —— 資源、當責與請求。

視覺規格來源:v4/notes/04_十頁內容_v2.md 的「# P10 · 資源、當責與請求 / ## 視覺規格」。

畫的東西(由上而下):
  上區左:人月矩陣(6 工作包 × 5 角色 + 小計 / 角色合計 / PM / 總計)、WP-E 待確認註記、
          第一段(W1-6)拆解行、算式框一(年度增聘成本暴露)、分隔說明、算式框二(人力成本估算)
  上區右:RACI 六列 × 九欄、放行條件框(紅)、三行假設與待確認註記
  中區  :受影響但不在核准鏈上的利害關係人窄帶(三格)
  下區左:相依帶(雙軌 + 待共同確認箭頭 + 組織障礙 + 圖例)
  下區右:六個月後的三格帶 + Q-22;左緣外側放全片最後一次出現的橘色母題
  最底  :Q-19 一行 + 結論條(請求核准)

不畫(由組版程式負責):頁首標題、右上角五格進度指示。

版面座標一律以「吋」思考,再由 X()/Y() 換算成 0-1 座標,避免字塊高度用猜的而互相壓字。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_figs_v4 import (  # noqa: E402
    plt, FancyBboxPatch, FancyArrowPatch, Rectangle,
    NAVY, ORANGE, ORANGE_DARK, ORANGE_LIGHT, RED, GREY, LIGHT, GREEN,
    newfig, save, assert_min_fontsize,
)

plt.rcParams["hatch.linewidth"] = 0.6

DARK = "#333333"     # 沿用 make_figs_v4.panel() 的內文色
PAPER = "#FAFAFA"    # 沿用 make_figs_v4.panel() 的底色
ROW_BG_A = 0.5       # 列名欄底 = LIGHT 加透明度(規格「12% 灰底」),不另立色值

W_IN, H_IN = 19.60, 11.03          # 16:9
FS_TINY, FS_BODY, FS_HEAD, FS_EQ, FS_BIG = 9.0, 10.0, 11.0, 11.5, 20.0

# 版心(吋)
L0, L1 = 0.14, 11.06               # 左欄
R0, R1 = 11.40, 19.46              # 右欄


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


def rect(ax, xi, yi, w, h, fc, ec="white", lw=1.4, hatch=False, z=3, alpha=None):
    ax.add_patch(Rectangle((X(xi), Y(yi + h)), X(w), h / H_IN,
                           fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z))
    if hatch:
        # 斜線紋壓低透明度,免得白線把格內 fs=9 的 FTE×週數切成一段一段。
        ax.add_patch(Rectangle((X(xi), Y(yi + h)), X(w), h / H_IN, fc="none",
                               ec="white", lw=0.0, hatch="////", alpha=0.5, zorder=z + 1))


def roundbox(ax, xi, yi, w, h, fc, ec, lw=1.5, ls="-", z=4):
    ax.add_patch(FancyBboxPatch((X(xi), Y(yi + h)), X(w), h / H_IN,
                                boxstyle="round,pad=0,rounding_size=.006",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def softbox(ax, xi, yi, w, h, col, alpha=0.06, lw=1.6):
    """淺色底 + 同色外框;底色由色票常數加透明度得到,不引入新色值。"""
    ax.add_patch(FancyBboxPatch((X(xi), Y(yi + h)), X(w), h / H_IN,
                                boxstyle="round,pad=0,rounding_size=.005",
                                fc=col, ec="none", alpha=alpha, zorder=2))
    ax.add_patch(FancyBboxPatch((X(xi), Y(yi + h)), X(w), h / H_IN,
                                boxstyle="round,pad=0,rounding_size=.005",
                                fc="none", ec=col, lw=lw, zorder=5))


def raci_mark(ax, xi, yi, letter):
    """A = 實心深藍圓底白字(最重);R = 橘色圓框;C / I = 淺灰字。"""
    if letter == "A":
        ax.text(X(xi), Y(yi), "A", fontsize=FS_BODY, color="white", ha="center",
                va="center", fontweight="bold", zorder=8,
                bbox=dict(boxstyle="circle,pad=0.28", fc=NAVY, ec=NAVY, lw=1.0))
    elif letter == "R":
        ax.text(X(xi), Y(yi), "R", fontsize=FS_BODY, color=ORANGE_DARK, ha="center",
                va="center", fontweight="bold", zorder=8,
                bbox=dict(boxstyle="circle,pad=0.28", fc="white", ec=ORANGE, lw=1.3))
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

RACI_ROWS = ["項目贊助人", "業務負責人(流程與 KPI)", "數據負責人(品質與權限)",
             "技術負責人(模型/系統/安全)", "複核營運主管", "專案負責人(提案人 PM)"]
RACI_COLS = ["WP-A\n評估底座", "WP-B\n標註品質", "WP-C\n脈絡特徵", "WP-D\n爭議回覆",
             "WP-E\n對照重訓", "WP-F\n治理移交", "G1\nW6", "G2\nW12", "G3\nW24"]
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
    fig, ax = newfig(W_IN, H_IN)      # 不下 title:頁首標題由組版程式放
    # newfig 用的是預設 subplot 邊界,座標軸只佔畫布約 77%,會讓下面所有以「吋」
    # 算出來的列高縮水三成而壓字。把座標軸拉滿整張畫布,X()/Y() 的吋數才是真的吋。
    ax.set_position([0.0, 0.0, 1.0, 1.0])

    # ==============================================================
    # 上區左 —— 人月矩陣
    # ==============================================================
    cw_name, cw_role, cw_sub = 1.72, 1.43, 2.05
    xs = [L0 + cw_name + i * cw_role for i in range(5)]
    x_sub = L0 + cw_name + 5 * cw_role

    line(ax, L0, 0.06,
         "人月矩陣〔提案規劃〕　由交付物反推,以 4.33 週/月換算;空格留白不填 0",
         fs=FS_TINY, c=GREY)

    yc = 0.30
    h_head, h_wp, h_sum, h_tot = 0.28, 0.325, 0.28, 0.38

    rect(ax, L0, yc, cw_name, h_head, LIGHT)
    line(ax, L0 + cw_name / 2, yc + h_head / 2, "工作包(人月)", fs=FS_HEAD, c=DARK,
         bold=True, ha="center", va="center")
    for i, r in enumerate(ROLES):
        rect(ax, xs[i], yc, cw_role, h_head, LIGHT)
        line(ax, xs[i] + cw_role / 2, yc + h_head / 2, r, fs=FS_HEAD, c=DARK, bold=True,
             ha="center", va="center")
    rect(ax, x_sub, yc, cw_sub, h_head, LIGHT)
    line(ax, x_sub + cw_sub / 2, yc + h_head / 2, "小計(人月)", fs=FS_HEAD, c=DARK,
         bold=True, ha="center", va="center")
    yc += h_head

    for name, cells, sub, seg1 in WPS:
        rect(ax, L0, yc, cw_name, h_wp, LIGHT, alpha=ROW_BG_A)
        line(ax, L0 + 0.07, yc + h_wp / 2, name, fs=FS_TINY + 0.5, c=DARK, bold=True,
             va="center")
        for i in range(5):
            if i in cells:
                top, val = cells[i]
                fc, tc = tier(float(val))
                rect(ax, xs[i], yc, cw_role, h_wp, fc, hatch=seg1)
                # 兩層都用 va="center":va="bottom" 會以字型 descent 對齊,
                # 中文字塊會比預期高出去而被格線切到。
                top_c = ORANGE_DARK if fc == ORANGE_LIGHT else "white"
                line(ax, xs[i] + cw_role / 2, yc + h_wp / 2 - 0.075, top, fs=FS_TINY,
                     c=top_c, ha="center", va="center")
                line(ax, xs[i] + cw_role / 2, yc + h_wp / 2 + 0.075, val, fs=FS_BODY,
                     c=tc, bold=True, ha="center", va="center")
            else:
                rect(ax, xs[i], yc, cw_role, h_wp, "white")
        fc, tc = tier(float(sub))
        rect(ax, x_sub, yc, cw_sub, h_wp, fc)
        line(ax, x_sub + cw_sub / 2, yc + h_wp / 2, sub, fs=FS_HEAD + 1, c=tc, bold=True,
             ha="center", va="center")
        yc += h_wp

    rect(ax, L0, yc, cw_name, h_sum, LIGHT)
    line(ax, L0 + cw_name / 2, yc + h_sum / 2, "角色合計", fs=FS_BODY, c=DARK, bold=True,
         ha="center", va="center")
    for i, v in enumerate(ROLE_TOTALS):
        fc, tc = tier(float(v))
        rect(ax, xs[i], yc, cw_role, h_sum, fc)
        line(ax, xs[i] + cw_role / 2, yc + h_sum / 2, v, fs=FS_HEAD, c=tc, bold=True,
             ha="center", va="center")
    rect(ax, x_sub, yc, cw_sub, h_sum, ORANGE_DARK)
    line(ax, x_sub + cw_sub / 2, yc + h_sum / 2, SUB_TOTAL, fs=FS_HEAD, c="white",
         bold=True, ha="center", va="center")
    yc += h_sum

    rect(ax, L0, yc, cw_name, h_sum, LIGHT, alpha=ROW_BG_A)
    line(ax, L0 + 0.07, yc + h_sum / 2, "專案負責人(提案人)", fs=FS_TINY + 0.5, c=DARK,
         bold=True, va="center")
    rect(ax, xs[0], yc, cw_role * 5, h_sum, ORANGE_DARK)
    line(ax, xs[0] + cw_role * 2.5, yc + h_sum / 2,
         "0.5×26w = 3.00 人月(跨全期 PM 投入)", fs=FS_BODY, c="white", bold=True,
         ha="center", va="center")
    rect(ax, x_sub, yc, cw_sub, h_sum, ORANGE_DARK)
    line(ax, x_sub + cw_sub / 2, yc + h_sum / 2, "3.00", fs=FS_HEAD, c="white", bold=True,
         ha="center", va="center")
    yc += h_sum

    rect(ax, L0, yc, cw_name + cw_role * 5, h_tot, LIGHT)
    line(ax, L0 + 0.07, yc + h_tot / 2, "總計(六個工作包 + 專案負責人)", fs=FS_HEAD,
         c=DARK, bold=True, va="center")
    rect(ax, x_sub, yc, cw_sub, h_tot, ORANGE_DARK)
    line(ax, x_sub + cw_sub / 2, yc + h_tot / 2 - 0.085, "約 18.2 人月", fs=FS_HEAD + 1,
         c="white", bold=True, ha="center", va="center")
    line(ax, x_sub + cw_sub / 2, yc + h_tot / 2 + 0.090, "〔提案規劃〕", fs=FS_TINY,
         c="white", ha="center", va="center")

    # WP-E 待確認註記
    line(ax, L0, 3.52,
         "WP-E(裁決 K 前移):W8-12 最小離線模型試驗 + W12-24 對照重訓;總投入 4.50 人月不變,"
         "係內部人力前移;逐格 FTE 由技術負責人於 G1 前重排,待確認。", fs=FS_TINY, c=GREY)

    # 第一段拆解行(對應結論條)
    line(ax, L0, 3.78,
         "第一段(W1-6)= 評估底座 2.08 + 標註品質前 4 週 1.39 + 脈絡特徵前 2 週 0.69 "
         "+ 專案負責人 0.69 = 約 4.85 人月。\n"
         "W1-6 的範圍是 WP-A 全部 + WP-B / WP-C 的限額探索,不是只做 WP-A。"
         "(斜線紋 = 第一段涵蓋的工作包,與計畫頁甘特同義)",
         fs=FS_BODY, c=NAVY, bold=True)

    # ==============================================================
    # 上區左下 —— 算式框一 / 分隔說明 / 算式框二
    # ==============================================================
    eq1_top, eq1_h = 4.28, 1.28
    softbox(ax, L0, eq1_top, L1 - L0, eq1_h, ORANGE, alpha=0.06, lw=1.5)
    line(ax, L0 + 0.14, eq1_top + 0.08, "算式框一 · 不做本案時的年度增聘成本暴露",
         fs=FS_BODY, c=ORANGE_DARK, bold=True)
    line(ax, L0 + 0.14, eq1_top + 0.33,
         "　　單人年薪 NT$80-90 萬(以公開薪資量級推算,未使用公司內部薪資資料)",
         fs=FS_EQ, c=DARK)
    line(ax, L0 + 0.14, eq1_top + 0.57, "×　間接費率 1.3(提案人設定的假設)",
         fs=FS_EQ, c=DARK, bold=True)
    line(ax, L0 + 0.14, eq1_top + 0.81, "=　NT$104-117 萬/人/年 × 需增聘 10-16 人",
         fs=FS_EQ, c=DARK)
    line(ax, L0 + 0.14, eq1_top + 1.05,
         "=　每年約 NT$1,040-1,870 萬,約 A$50-89 萬(1 A$ 約 NT$21,概算)",
         fs=FS_EQ, c=DARK, bold=True)

    line(ax, L0, 5.64,
         "框一與框二不得相減、不得畫成同一條式子:框二是本案要花的錢;"
         "框一是不做本案、維持現行做法的年度增聘成本暴露。", fs=FS_TINY, c=GREY)

    eq2_top, eq2_h = 5.90, 1.04
    softbox(ax, L0, eq2_top, L1 - L0, eq2_h, ORANGE, alpha=0.06, lw=1.5)
    line(ax, L0 + 0.14, eq2_top + 0.08,
         "算式框二 · 人力成本估算(全片唯一叫法,不得改稱總成本)",
         fs=FS_BODY, c=ORANGE_DARK, bold=True)
    line(ax, L0 + 0.14, eq2_top + 0.33,
         "　　18.2 人月 × 月薪 NT$6.7-7.5 萬(年薪 80-90 萬 / 12)× 間接費率 1.3",
         fs=FS_EQ, c=DARK, bold=True)
    line(ax, L0 + 0.14, eq2_top + 0.57, "=　約 NT$158-177 萬", fs=FS_EQ, c=DARK)
    line(ax, L0 + 0.14, eq2_top + 0.81, "=　約 1.4-1.7 個 loaded FTE-year",
         fs=FS_EQ, c=ORANGE_DARK, bold=True)

    # ==============================================================
    # 上區右 —— RACI 六列 × 九欄
    # ==============================================================
    lab_w = 2.06          # 要放得下「技術負責人(模型/系統/安全)」不壓到第一欄
    col_w = (R1 - R0 - lab_w) / 9.0
    line(ax, R0, 0.06, "RACI · 六方當責 × 六個工作包 + 三道決策門", fs=FS_HEAD, c=NAVY,
         bold=True)

    ry, h_rh, h_rr = 0.34, 0.36, 0.325
    rect(ax, R0, ry, lab_w, h_rh, LIGHT)
    line(ax, R0 + lab_w / 2, ry + h_rh / 2, "當責角色", fs=FS_BODY, c=DARK, bold=True,
         ha="center", va="center")
    for j, cn in enumerate(RACI_COLS):
        x = R0 + lab_w + j * col_w
        rect(ax, x, ry, col_w, h_rh, NAVY if j >= 6 else LIGHT)
        line(ax, x + col_w / 2, ry + h_rh / 2, cn, fs=FS_TINY,
             c="white" if j >= 6 else DARK, bold=True, ha="center", va="center", lsp=1.35)
    ry += h_rh

    for i, rn in enumerate(RACI_ROWS):
        rect(ax, R0, ry, lab_w, h_rr, LIGHT, alpha=ROW_BG_A)
        line(ax, R0 + 0.06, ry + h_rr / 2, rn, fs=FS_TINY, c=DARK, bold=True, va="center")
        for j in range(9):
            x = R0 + lab_w + j * col_w
            rect(ax, x, ry, col_w, h_rr, "white")
            raci_mark(ax, x + col_w / 2, ry + h_rr / 2, RACI[i][j])
        ry += h_rr

    line(ax, R0, ry + 0.10,
         "A = 當責(每欄只有一個) · R = 執行 · C = 諮詢 · I = 告知;"
         "三道決策門的 A 一律落在項目贊助人。\n"
         "複核營運主管是評估底座那一包的當責人,因為那件事發生在他的團隊裡"
         "(標註品質那一包該列給 C)。", fs=FS_TINY, c=GREY, lsp=1.6)

    # ==============================================================
    # 上區右 —— 放行條件框(紅)
    # ==============================================================
    line(ax, R0, 3.22, "反事實成本暴露 → 只有被實測證明可避免的那一部分才算數",
         fs=FS_TINY, c=GREY)
    g_top, g_h = 3.46, 1.80
    softbox(ax, R0, g_top, R1 - R0, g_h, RED, alpha=0.06, lw=1.7)
    line(ax, R0 + 0.14, g_top + 0.08, "放行條件 · 本案的損益兩平門檻",
         fs=FS_BODY, c=RED, bold=True)
    line(ax, R0 + 0.14, g_top + 0.33,
         "① 若公司選擇以現行流程覆蓋全客戶,年度擴編暴露約 NT$1,040-1,870 萬;",
         fs=FS_EQ, c=DARK)
    line(ax, R0 + 0.14, g_top + 0.57, "　 這不是本案承諾節省。", fs=FS_EQ, c=DARK,
         bold=True)
    line(ax, R0 + 0.14, g_top + 0.81,
         "② 完整專案的人力成本約等於 1.4-1.7 個 loaded FTE-year。", fs=FS_EQ, c=DARK)
    line(ax, R0 + 0.14, g_top + 1.05,
         "③ 只有 G2 實測證明可避免或延後至少此容量,且業務確認會轉成少招人\n"
         "　 或少徵調研發,才放行後續預算。", fs=FS_EQ, c=RED, bold=True)
    line(ax, R1 - 0.14, g_top + g_h - 0.10,
         "當責:業務負責人提出容量轉換的確認 · 時點 G2(W12)· 它決定第二段預算放不放行",
         fs=FS_TINY, c=GREY, ha="right", va="bottom")

    ax.add_patch(FancyArrowPatch((X(L1 + 0.04), Y(eq1_top + 0.55)),
                                 (X(R0 - 0.04), Y(g_top + 0.60)),
                                 arrowstyle="-|>", mutation_scale=14, lw=1.3,
                                 color=GREY, connectionstyle="arc3,rad=-0.10", zorder=7))

    line(ax, R0, 5.38,
         "金額為推算量級,非核定預算;薪資、間接費率、匯率三項均為提案人設定的假設值。",
         fs=FS_BODY, c=GREY)
    line(ax, R0, 5.64,
         "本估算僅涵蓋人力。影片回抽流量、儲存、運算、測試環境、脈絡資料維護與預備金尚未納入,\n"
         "待確認(當責:數據負責人與技術負責人 · G1 前補齊量級 · 它決定第二段額度要不要上修)。",
         fs=FS_BODY, c=DARK, bold=True)
    line(ax, R0, 6.16,
         "上述薪資尺為「一般工程師」的公開量級,而要增聘的是複核分析人員,專案內五種角色\n"
         "也共用同一把尺;實際職類落差待確認(當責:業務負責人 · G1 前確認 · 它決定框一是否整組重算)。",
         fs=FS_TINY, c=GREY)

    # ==============================================================
    # 中區 —— 受影響但不在核准鏈上的利害關係人窄帶
    # ==============================================================
    b_top, b_h = 7.06, 0.96
    softbox(ax, L0, b_top, R1 - L0, b_h, GREEN, alpha=0.09, lw=1.4)
    line(ax, L0 + 0.14, b_top + 0.07, "受影響但不在核准鏈上的利害關係人", fs=FS_HEAD,
         c=GREEN, bold=True)
    stake = [
        ("① 5 位專職分析人員",
         "工作從逐筆看片變成處理難題與治理;轉任與再訓練規劃\n列為移交前置條件,由複核營運主管代表"),
        ("② 車隊客戶的安全主管",
         "判定結果的實際使用者,卻不在核准鏈上;\n由業務負責人代表"),
        ("③ 駕駛",
         "被判定的對象,目前無申訴管道;在申訴機制到位前,本案產出的\n判準與一致性量測不對外供個人考核使用"),
    ]
    seg = (R1 - L0) / 3.0
    for k, (head, body) in enumerate(stake):
        x = L0 + k * seg + 0.16
        line(ax, x, b_top + 0.33, head, fs=FS_BODY, c=GREEN, bold=True)
        line(ax, x, b_top + 0.56, body, fs=FS_TINY, c=DARK, lsp=1.55)
        if k:
            ax.plot([X(L0 + k * seg), X(L0 + k * seg)],
                    [Y(b_top + b_h - 0.08), Y(b_top + 0.10)],
                    color=GREEN, lw=0.8, alpha=0.55, zorder=6)

    # ==============================================================
    # 下區左 —— 相依帶
    # ==============================================================
    roundbox(ax, L0, 8.10, 6.20, 0.26, NAVY, NAVY, lw=1.2)
    line(ax, L0 + 3.10, 8.23,
         "本案 W1-26:評估底座 · 標註品質 · 脈絡特徵 · 爭議回覆自動化 · 對照重訓 · 治理移交",
         fs=FS_TINY, c="white", bold=True, ha="center", va="center")
    roundbox(ax, 4.30, 8.68, 6.20, 0.26, "white", GREY, lw=1.2, ls=(0, (4, 3)))
    line(ax, 7.40, 8.81, "公司既有的雲端判讀規劃(仍在研擬)", fs=FS_TINY, c=GREY,
         bold=True, ha="center", va="center")
    ax.add_patch(FancyArrowPatch((X(6.34), Y(8.36)), (X(6.60), Y(8.68)),
                                 arrowstyle="-|>", mutation_scale=16, lw=2.2,
                                 color=NAVY, zorder=7))
    line(ax, 6.76, 8.40, "我主張的相依關係(待共同確認)", fs=FS_HEAD, c=NAVY, bold=True)
    line(ax, L0, 9.02,
         "請求委員會指派一次共同評估,列為 G1 前置事項;若評估結果是兩案應合併或改序,我接受。",
         fs=FS_BODY, c=GREY)
    line(ax, L1, 9.02, "實線 = 本提案要交付的　　虛線 = 尚未定案", fs=FS_TINY, c=GREY,
         ha="right")
    line(ax, L0, 9.26,
         "組織障礙:政策可改 · 優先序照購買量 · 尖峰徵調研發,"
         "所以我要的不只是預算,是一個贊助人跟三道門", fs=FS_BODY, c=DARK, bold=True)

    # ==============================================================
    # 下區右 —— 六個月後的三格帶 + Q-22 + 橘色母題
    # ==============================================================
    line(ax, R0, 8.10, "六個月之後,委員會手上會多三樣東西", fs=FS_HEAD, c=NAVY, bold=True)
    tw = (R1 - R0 - 0.20) / 3.0
    tri = ["① 一份可稽核的\n　 錯誤率",
           "② 一層把畫面外脈絡\n　 帶進事件的判斷層",
           "③ 一份證明或推翻「脈絡到底\n　 有沒有用」的對照實驗結果"]
    for k, t in enumerate(tri):
        x = R0 + k * (tw + 0.10)
        roundbox(ax, x, 8.40, tw, 0.56, PAPER, NAVY, lw=1.5)
        line(ax, x + tw / 2, 8.68, t, fs=FS_TINY + 0.5, c=DARK, ha="center", va="center",
             lsp=1.55)
    roundbox(ax, R0 - 0.32, 8.53, 0.26, 0.30, ORANGE, ORANGE_DARK, lw=1.2, z=6)

    line(ax, R0, 9.04,
         "就算第二十四週證不出增量,本案仍留下公司第一套可重複的模型評估與標註品質流程,\n"
         "那個東西不隨第三道門撤掉。", fs=FS_BODY, c=DARK)

    # ==============================================================
    # 最底 —— Q-19 一行 + 結論條
    # ==============================================================
    line(ax, L0, 9.56,
         "不做這件事的代價不是多花錢,是三件事同時發生:客戶繼續等兩到五天、"
         "小客戶繼續拿到沒有人看過的判定,而我們的研發工程師在尖峰時繼續被拉去看影片。",
         fs=FS_HEAD, c=NAVY, bold=True)

    bar_top = 9.86
    rect(ax, 0.0, bar_top, W_IN, H_IN - bar_top, NAVY, ec=NAVY, lw=0, z=4)
    line(ax, W_IN / 2, bar_top + 0.10, "G1 決定的是是否續行剩餘工作,不是是否開始。",
         fs=FS_TINY, c="white", ha="center")
    line(ax, W_IN / 2, bar_top + 0.32, "請求核准:六個月整體額度輪廓 · 分段釋出",
         fs=FS_BIG, c="white", bold=True, ha="center")
    line(ax, W_IN / 2, bar_top + 0.74,
         "第一段 W1-6(WP-A + WP-B/WP-C 限額探索)約 4.85 人月 / 量級 NT$42-47 萬 · "
         "G1 由贊助人決定是否續行", fs=FS_BIG, c=ORANGE_LIGHT, bold=True, ha="center")

    assert_min_fontsize(fig)
    return fig


if __name__ == "__main__":
    save(build(), "fig_v4_10")
