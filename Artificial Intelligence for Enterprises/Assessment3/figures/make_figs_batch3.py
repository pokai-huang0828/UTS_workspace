# -*- coding: utf-8 -*-
"""A3 圖表 · 第三批:P7 倫理護欄表(補上講稿自評唯一沒有現成圖檔的內容頁)"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY, RED, GREY = "#1F3864", "#C00000", "#808080"
LIGHT, GREEN = "#D9D9D9", "#548235"

def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", name)

def fig_ethics():
    """左側:口說講透的兩點(各佔大塊);右側:其餘四項護欄表 + 禁用特徵清單。"""
    fig, ax = plt.subplots(figsize=(13, 6.8))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    ax.text(.5, .985, "社會文化與倫理影響", ha="center", va="top",
            fontsize=16, color=NAVY, fontweight="bold")

    # ---- 左:講透的兩點 ----
    TALK = [
        (.545, "① 脆弱客戶:兩個方向的代價不對稱", RED,
         "還款行為異常同時是流失前兆與財務困難前兆,\n"
         "模型在數學上無法區分兩者。\n\n"
         "漏掉一個要走的客戶,只是損失利差;\n"
         "把財困客戶當商機,是監管事件。\n\n"
         "護欄:高分名單進入外撥前必須先過財務困難篩選,\n"
         "命中者強制轉入 hardship 並自留存名單移除 ——\n"
         "此規則寫在系統層,不是人工判斷層。"),
        (.075, "② 忠誠稅:AI 把它自動化了", RED,
         "「表現出要走的人拿到折扣」必然鏡像\n「不吵不鬧的忠誠客戶繼續付較高利率」。\n"
         "AI 沒有創造這個機制,但把它規模化、精準化。\n\n"
         "CBA 是 2025 年澳洲最受信任的金融品牌\n(Roy Morgan, 2025)——\n"
         "這個信任資產與「只有吵的人有糖吃」直接衝突。\n\n"
         "護欄:設前後簿利率差上限;對「從未被選中\n但符合資格」的客戶定期主動利率檢視。"),
    ]
    for y, title, col, body in TALK:
        ax.add_patch(FancyBboxPatch((.02, y), .50, .40,
                                    boxstyle="round,pad=0,rounding_size=.015",
                                    fc="#FFF7F7", ec=col, lw=1.8, zorder=3))
        ax.text(.27, y + .355, title, ha="center", va="center", fontsize=12,
                color=col, fontweight="bold", zorder=4)
        ax.text(.27, y + .155, body, ha="center", va="center", fontsize=9,
                color="#333333", zorder=4, linespacing=1.75)

    # ---- 右上:其餘四項護欄表 ----
    ROWS = [("可解釋性", "對客戶 / 客戶經理 / 監管\n三種粒度的說明", "合規"),
            ("禁用特徵清單", "見下方", "合規 + 資料"),
            ("代理歧視稽核", "地理區 / 貸款規模分位 / 年齡帶\n三切面量測優惠獲取率差異", "合規"),
            ("客戶經理的\n演算法管理", "配額規則變更需與員工代表協商;\n模型建議不作個人績效考核", "業務負責人")]
    x0, y0, w = .545, .60, .435
    ax.text(x0 + w / 2, .955, "其餘四項護欄與簽核責任", ha="center", va="top",
            fontsize=11.5, color=NAVY, fontweight="bold")
    hdr = [("議題", .11), ("護欄", .22), ("簽核", .105)]
    cx = x0
    for t, cw in hdr:
        ax.add_patch(FancyBboxPatch((cx, .875), cw, .045,
                                    boxstyle="round,pad=0,rounding_size=.008",
                                    fc=NAVY, ec=NAVY, zorder=3))
        ax.text(cx + cw / 2, .8975, t, ha="center", va="center", fontsize=9,
                color="white", fontweight="bold", zorder=4)
        cx += cw
    yy = .875
    for issue, guard, sign in ROWS:
        yy -= .068
        cx = x0
        for txt, cw in zip((issue, guard, sign), [h[1] for h in hdr]):
            ax.add_patch(FancyBboxPatch((cx, yy), cw, .065,
                                        boxstyle="round,pad=0,rounding_size=.006",
                                        fc="#FAFAFA", ec=LIGHT, lw=1, zorder=3))
            ax.text(cx + cw / 2, yy + .0325, txt, ha="center", va="center",
                    fontsize=7.6, color="#333333", zorder=4, linespacing=1.5)
            cx += cw

    # ---- 右下:禁用特徵清單 ----
    ax.add_patch(FancyBboxPatch((x0, .075), w, .49,
                                boxstyle="round,pad=0,rounding_size=.015",
                                fc="#F4F9F1", ec=GREEN, lw=1.8, zorder=3))
    ax.text(x0 + w / 2, .525, "禁用特徵清單(主動排除)", ha="center", va="center",
            fontsize=11.5, color=GREEN, fontweight="bold", zorder=4)
    ax.text(x0 + w / 2, .425,
            "①  CDR 資料分享請求紀錄\n"
            "②  贖回 / 結清詢問紀錄\n"
            "③  受保護屬性的地理代理(郵遞區號、分行別)",
            ha="center", va="center", fontsize=9.5, color="#333333",
            zorder=4, linespacing=2.1)
    ax.text(x0 + w / 2, .245,
            "以客戶行使 CDR 資料可攜權的行為作為預測特徵,\n"
            "等同於對行使法定權利者施加差別待遇。\n"
            "即使技術上可行、合規上未被明文禁止,\n"
            "本提案主動排除。",
            ha="center", va="center", fontsize=9.5, color=GREEN,
            fontweight="bold", zorder=4, linespacing=1.9)
    ax.text(x0 + w / 2, .108,
            "因此模型預測能力上限受限 —— 這是主動的倫理取捨,不是資料不可得。",
            ha="center", va="center", fontsize=8.6, color=GREY, zorder=4)
    save(fig, "fig07_ethics")

if __name__ == "__main__":
    print("產出第三批圖表:")
    fig_ethics()
