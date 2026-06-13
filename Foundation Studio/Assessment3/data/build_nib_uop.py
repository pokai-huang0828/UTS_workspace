# -*- coding: utf-8 -*-
"""Fig 7: nib group underlying operating profit (UOP), FY21-FY25.
Source: nib Holdings annual reports (FY21 5-year summary; FY23/FY25 announcements)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

FIG = Path(r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3\figures")
fy   = ["FY21", "FY22", "FY23", "FY24", "FY25"]
uop  = [204.9, 237.0, 263.2, 257.5, 239.2]
npat = [160.5, None, 191.1, 181.6, 198.6]   # FY22 NPAT not to hand; shown where available

plt.rcParams.update({"figure.dpi":150,"font.size":11,"axes.spines.top":False,"axes.spines.right":False})
fig, ax = plt.subplots(figsize=(9,5))
bars = ax.bar(fy, uop, color=["#c0392b"]*3 + ["#e08a7d"]*2, width=.6)
for b, v in zip(bars, uop):
    ax.text(b.get_x()+b.get_width()/2, v+3, f"{v:.0f}", ha="center", fontsize=10, fontweight="bold")
# NPAT markers where available
xs = [i for i,v in enumerate(npat) if v]
ax.plot(xs, [npat[i] for i in xs], "o-", color="#1f4e79", lw=1.5, ms=5, label="Statutory NPAT")
ax.annotate("peak", xy=(2, 263.2), xytext=(2, 285), ha="center", color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("claims inflation\nweighs on profit", xy=(4, 239.2), xytext=(3.4, 200),
            color="grey", fontsize=9, arrowprops=dict(arrowstyle="->", color="grey"))
ax.set_ylim(0, 300); ax.set_ylabel("A$ million")
ax.set_title("nib underlying operating profit peaked in FY23, then eased", fontweight="bold")
ax.legend(frameon=False, loc="lower right")
ax.text(.5,.93,"red bars = underlying operating profit (UOP)", transform=ax.transAxes, ha="center", fontsize=8, color="grey")
ax.grid(axis="y", alpha=.3)
fig.text(.01,-.02,"Source: nib Holdings annual reports (FY21 five-year summary; FY23/FY25 results). FY24-25 under AASB 17.",
         fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig7_nib_uop.png", bbox_inches="tight"); plt.close(fig)
print("Saved fig7. UOP:", dict(zip(fy, uop)))
