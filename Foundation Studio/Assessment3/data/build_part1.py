# -*- coding: utf-8 -*-
"""
A3 Part 1 (industry context) + Part 3 DiD foundation.
Source: APRA Quarterly PHI Statistics - Membership Trends, March 2026 quarter.
Outputs charts to ..\figures and prints a 2x2 difference-in-differences result.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3")
PATH = BASE / "data" / "APRA_Membership_Trends_Mar2026.xlsx"
FIG = BASE / "figures"; FIG.mkdir(exist_ok=True)

MONTH = {"Mar": 3, "Jun": 6, "Sep": 9, "Dec": 12}

# ---------- 1. Hospital-treatment insured persons by Year x Quarter x Age ----------
raw = pd.read_excel(PATH, sheet_name="MembershipByAgeData", header=None,
                    usecols=[0, 1, 2, 3, 4, 5])
raw.columns = ["Year", "MonthEnd", "State", "Gender", "Age", "Insured"]
raw["Year"] = pd.to_numeric(raw["Year"], errors="coerce")
raw["MonthEnd"] = raw["MonthEnd"].astype(str).str.strip()
raw["Age"] = pd.to_numeric(raw["Age"], errors="coerce")
raw["Insured"] = pd.to_numeric(raw["Insured"], errors="coerce")
df = raw[(raw["Year"].between(2007, 2026)) & raw["Age"].notna() & raw["Insured"].notna()].copy()
df["Year"] = df["Year"].astype(int)
df["Age"] = df["Age"].astype(int)
df = df[df["MonthEnd"].isin(MONTH)]
df["date"] = pd.to_datetime(dict(year=df["Year"], month=df["MonthEnd"].map(MONTH), day=1))

# national insured persons per (date, age band)
nat = df.groupby(["date", "Age"], as_index=False)["Insured"].sum()
tot = nat.groupby("date", as_index=False)["Insured"].sum().rename(columns={"Insured": "Total"})

# ---------- 2. % of insured persons aged under 40 ----------
u40 = (nat[nat["Age"] < 40].groupby("date", as_index=False)["Insured"].sum()
       .rename(columns={"Insured": "Under40"}))
share = tot.merge(u40, on="date")
share["pct_u40"] = 100 * share["Under40"] / share["Total"]

# ---------- 3. Coverage rate: total HT insured / national population ----------
pop_raw = pd.read_excel(PATH, sheet_name="MembershipData", header=None, usecols=[0, 1, 2, 3])
pop_raw.columns = ["Year", "MonthEnd", "State", "Pop"]
pop_raw["Year"] = pd.to_numeric(pop_raw["Year"], errors="coerce")
pop_raw["MonthEnd"] = pop_raw["MonthEnd"].astype(str).str.strip()
pop_raw["Pop"] = pd.to_numeric(pop_raw["Pop"], errors="coerce")
pop = pop_raw[(pop_raw["Year"].between(2007, 2026)) & pop_raw["Pop"].notna() & pop_raw["MonthEnd"].isin(MONTH)].copy()
pop["date"] = pd.to_datetime(dict(year=pop["Year"].astype(int), month=pop["MonthEnd"].map(MONTH), day=1))
natpop = pop.groupby("date", as_index=False)["Pop"].sum()
cov = tot.merge(natpop, on="date")
cov["coverage_pct"] = 100 * cov["Total"] / cov["Pop"]

print("Coverage sanity (should be ~45%):")
print(cov[["date", "coverage_pct"]].tail(4).to_string(index=False))
print(f"\nUnder-40 share: {share['pct_u40'].iloc[0]:.1f}% ({share['date'].iloc[0].date()}) "
      f"-> {share['pct_u40'].iloc[-1]:.1f}% ({share['date'].iloc[-1].date()})")

# ---------- 4. DiD: 25-29 (treated by 2019-04 age discount) vs 30-34 (control) ----------
band = nat[nat["Age"].isin([25, 30])].pivot(index="date", columns="Age", values="Insured")
band.columns = ["t25_29", "c30_34"]
pre = band.loc["2017-01":"2019-03"]      # pre-policy
post = band.loc["2019-06":"2019-12"]     # post-policy, pre-COVID
d = {
    "t_pre": np.log(pre["t25_29"]).mean(), "t_post": np.log(post["t25_29"]).mean(),
    "c_pre": np.log(pre["c30_34"]).mean(), "c_post": np.log(post["c30_34"]).mean(),
}
did = (d["t_post"] - d["t_pre"]) - (d["c_post"] - d["c_pre"])
print("\n===== Difference-in-Differences (log insured persons) =====")
print(f"  Treated 25-29 :  pre {np.exp(d['t_pre']):,.0f}  ->  post {np.exp(d['t_post']):,.0f}   "
      f"(dlog = {d['t_post']-d['t_pre']:+.4f})")
print(f"  Control 30-34 :  pre {np.exp(d['c_pre']):,.0f}  ->  post {np.exp(d['c_post']):,.0f}   "
      f"(dlog = {d['c_post']-d['c_pre']:+.4f})")
print(f"  DiD estimate  =  {did:+.4f}  (~ {did*100:+.2f}% effect on 25-29 vs 30-34)")

# ================= CHARTS =================
plt.rcParams.update({"figure.dpi": 150, "axes.grid": True, "grid.alpha": .3,
                     "font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
SRC = "Source: APRA Quarterly Private Health Insurance Statistics (Membership Trends), Mar 2026."

# Fig 1: coverage rate
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(cov["date"], cov["coverage_pct"], color="#1f4e79", lw=2)
ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2021-12-01"), color="grey", alpha=.12)
ax.text(pd.Timestamp("2020-04-01"), cov["coverage_pct"].min()+.3, "COVID-19", color="grey")
ax.set_title("Australian hospital-cover coverage rate has trended down", fontweight="bold")
ax.set_ylabel("% of population with hospital cover"); ax.set_xlabel("")
ax.figtext = fig.text(.01, -.02, SRC, fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig1_coverage_trend.png", bbox_inches="tight"); plt.close(fig)

# Fig 2: under-40 share
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(share["date"], share["pct_u40"], color="#c0392b", lw=2)
ax.set_title("The risk pool is ageing: under-40s are a shrinking share of the insured",
             fontweight="bold")
ax.set_ylabel("% of insured persons aged under 40"); ax.set_xlabel("")
fig.text(.01, -.02, SRC, fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig2_under40_share.png", bbox_inches="tight"); plt.close(fig)

# Fig 3: DiD visual (indexed to 2019 Q1 = 100)
idx = band / band.loc["2019-03"] * 100
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(idx.index, idx["t25_29"], color="#1f4e79", lw=2, label="25-29 (got age discount)")
ax.plot(idx.index, idx["c30_34"], color="#888888", lw=2, ls="--", label="30-34 (control)")
ax.axvline(pd.Timestamp("2019-04-01"), color="#c0392b", lw=1.2)
ax.text(pd.Timestamp("2019-05-01"), idx.min().min(), " Apr-2019\n age-based discount",
        color="#c0392b", fontsize=9, va="bottom")
ax.set_xlim(pd.Timestamp("2016-01-01"), pd.Timestamp("2022-06-01"))
ax.set_title("DiD set-up: insured persons by age, indexed to 2019 Q1 = 100", fontweight="bold")
ax.set_ylabel("Insured persons (2019 Q1 = 100)"); ax.legend(frameon=False)
fig.text(.01, -.02, SRC, fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig3_did_setup.png", bbox_inches="tight"); plt.close(fig)

print("\nSaved 3 charts to", FIG)
