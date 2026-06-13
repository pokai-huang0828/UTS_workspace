# -*- coding: utf-8 -*-
"""Fix fig3 normalisation + add a parallel-trends (pre-trend) diagnostic."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3")
PATH = BASE / "data" / "APRA_Membership_Trends_Mar2026.xlsx"
FIG = BASE / "figures"
MONTH = {"Mar": 3, "Jun": 6, "Sep": 9, "Dec": 12}

raw = pd.read_excel(PATH, sheet_name="MembershipByAgeData", header=None, usecols=[0,1,2,3,4,5])
raw.columns = ["Year","MonthEnd","State","Gender","Age","Insured"]
for c in ["Year","Age","Insured"]:
    raw[c] = pd.to_numeric(raw[c], errors="coerce")
raw["MonthEnd"] = raw["MonthEnd"].astype(str).str.strip()
df = raw[(raw["Year"].between(2007,2026)) & raw["Age"].notna() & raw["Insured"].notna() & raw["MonthEnd"].isin(MONTH)].copy()
df["date"] = pd.to_datetime(dict(year=df["Year"].astype(int), month=df["MonthEnd"].map(MONTH), day=1))
nat = df.groupby(["date","Age"], as_index=False)["Insured"].sum()
band = nat[nat["Age"].isin([25,30])].pivot(index="date", columns="Age", values="Insured")
band.columns = ["t25_29","c30_34"]
band = band.sort_index()

# ---- parallel-trends diagnostic: avg quarterly log-growth, pre vs around ----
pre = band.loc["2016-03":"2019-03"]
def slope(s):  # OLS slope of log(s) on a time counter -> avg quarterly growth
    y = np.log(s.values); x = np.arange(len(y))
    return np.polyfit(x, y, 1)[0]
print("PRE-PERIOD (2016Q1-2019Q1) average quarterly growth:")
print(f"  Treated 25-29 : {slope(pre['t25_29'])*100:+.2f}% / quarter")
print(f"  Control 30-34 : {slope(pre['c30_34'])*100:+.2f}% / quarter")
print(f"  -> pre-trend gap = {(slope(pre['t25_29'])-slope(pre['c30_34']))*100:+.2f} pp/qtr "
      "(near 0 = parallel; large = parallel-trends VIOLATED)")

# ---- corrected index chart (Series base, aligns on columns) ----
base = band.loc[pd.Timestamp("2019-03-01")]           # Series indexed by column
idx = band.div(base) * 100
win = idx.loc["2015-03":"2022-03"]

plt.rcParams.update({"figure.dpi":150,"axes.grid":True,"grid.alpha":.3,"font.size":11,
                     "axes.spines.top":False,"axes.spines.right":False})
fig, ax = plt.subplots(figsize=(9,5))
ax.plot(win.index, win["t25_29"], color="#1f4e79", lw=2, marker="o", ms=3, label="25-29 (got age discount)")
ax.plot(win.index, win["c30_34"], color="#888888", lw=2, ls="--", marker="s", ms=3, label="30-34 (control)")
ax.axvline(pd.Timestamp("2019-04-01"), color="#c0392b", lw=1.3)
ax.text(pd.Timestamp("2019-05-15"), win.values.max()-1, " Apr-2019 age discount", color="#c0392b", fontsize=9)
ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2021-12-01"), color="grey", alpha=.12)
ax.text(pd.Timestamp("2020-04-01"), win.values.min(), " COVID", color="grey", fontsize=9, va="bottom")
ax.set_ylim(win.values.min()-1, win.values.max()+1)
ax.set_title("Parallel-trends check: 25-29 was already falling faster pre-2019", fontweight="bold")
ax.set_ylabel("Insured persons (2019 Q1 = 100)"); ax.legend(frameon=False, loc="lower left")
fig.text(.01,-.02,"Source: APRA Quarterly PHI Statistics (Membership Trends), Mar 2026.", fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig3_did_setup.png", bbox_inches="tight"); plt.close(fig)
print("\n25-29 vs 30-34 (indexed 2019Q1=100), selected quarters:")
print(win.loc[["2016-03","2017-03","2018-03","2019-03","2019-12","2021-12"]].round(1).to_string())
print("\nfig3 re-saved.")
