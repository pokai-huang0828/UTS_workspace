# -*- coding: utf-8 -*-
"""Part 1 NIB vs competitors: market share + margins (APRA FY2024-25 performance DB)."""
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
pd.set_option("display.width", 200)

BASE = Path(r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3")
PATH = BASE / "data" / "APRA_Performance_2024-25.xlsx"
FIG = BASE / "figures"

db = pd.read_excel(PATH, sheet_name="Database")
db["Value"] = pd.to_numeric(db["Value"], errors="coerce")
HIB = db["Business type"] == "Health insurance business"

# --- verify NIB structure ---
nib = db[db["Entity name"] == "NIB Health Funds Ltd"]
piv = nib.groupby(["Data item", "Business type"], dropna=False)["Value"].sum().unstack()
print("NIB pivot (Data item x Business type), $:")
print(piv.fillna(0).astype("int64", errors="ignore").to_string())

STATES = {"NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"}

def item(entity_df, name, hib_only=True):
    """Sum a data item, de-duplicating the state-split (sum states, not the NaN total too)."""
    m = entity_df["Data item"] == name
    if hib_only:
        m &= entity_df["Business type"] == "Health insurance business"
    sub = entity_df.loc[m]
    by_state = sub[sub["State and territory"].isin(STATES)]
    return by_state["Value"].sum() if len(by_state) else sub["Value"].sum()

# --- build cross-insurer summary ---
rows = []
for ent, g in db.groupby("Entity name"):
    prem = item(g, "Premium revenue")
    claims = item(g, "Insurance claims")
    opex = item(g, "Other business expenses (inclusive of claims handling expenses)")
    pat = item(g, "Profit (loss) from continuing operations after income tax", hib_only=False)
    if prem and prem > 0:
        rows.append(dict(Entity=ent, Premium=prem, Claims=claims, Opex=opex, PAT=pat,
                         GrossMargin=1 - claims/prem,
                         NetMargin=1 - (claims+opex)/prem,
                         ExpenseRatio=opex/prem))
s = pd.DataFrame(rows).sort_values("Premium", ascending=False).reset_index(drop=True)
s["Share"] = 100 * s["Premium"] / s["Premium"].sum()
short = {"NIB Health Funds Ltd":"nib","Medibank Private Limited":"Medibank","BUPA HI Pty Ltd":"Bupa",
         "The Hospitals Contribution Fund of Australia Ltd":"HCF","HBF Health Limited":"HBF",
         "Australian Unity Health Limited":"Aust Unity","GMHBA Limited":"GMHBA",
         "Defence Health Limited":"Defence Health","Teachers Federation Health Ltd":"Teachers Health"}
s["Short"] = s["Entity"].map(short).fillna(s["Entity"])
print("\nFY2024-25 health-insurance business summary ($m, margins %):")
show = s.head(12).copy()
show["Premium$m"] = (show["Premium"]/1e6).round(0)
show["PAT$m"] = (show["PAT"]/1e6).round(0)
for c in ["NetMargin","ExpenseRatio","Share"]:
    show[c] = (show[c]*100).round(1) if c != "Share" else show[c].round(1)
print(show[["Short","Premium$m","PAT$m","NetMargin","ExpenseRatio","Share"]].to_string(index=False))
print(f"\nTotal industry premium (HIB): ${s['Premium'].sum()/1e9:.1f}bn | insurers with premium: {len(s)}")

# ===== Fig 4: market share =====
top = s.head(7).copy()
other = pd.DataFrame([{"Short":"Other (23)","Share":100-top["Share"].sum()}])
ms = pd.concat([top[["Short","Share"]], other], ignore_index=True)
colors = ["#c0392b" if x=="nib" else "#cdd7e3" for x in ms["Short"]]
fig, ax = plt.subplots(figsize=(9,5))
b = ax.barh(ms["Short"][::-1], ms["Share"][::-1], color=colors[::-1])
for i,(v,n) in enumerate(zip(ms["Share"][::-1], ms["Short"][::-1])):
    ax.text(v+0.3, i, f"{v:.1f}%", va="center", fontsize=9)
ax.set_title("nib is Australia's #4 private health insurer (premium revenue share, FY25)", fontweight="bold")
ax.set_xlabel("% of industry premium revenue"); ax.set_xlim(0,32)
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="x", alpha=.3)
fig.text(.01,-.02,"Source: APRA Annual PHI Performance Statistics, FY2024-25. Health insurance business.", fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig4_market_share.png", bbox_inches="tight"); plt.close(fig)

# ===== Fig 5: net margin vs peers =====
peers = s[s["Short"].isin(["Medibank","Bupa","nib","HCF","HBF","Aust Unity","GMHBA"])].copy()
peers = peers.sort_values("NetMargin", ascending=True)
forprofit = {"nib","Medibank","Bupa"}   # for-profit insurers
colors = ["#c0392b" if x=="nib" else ("#1f4e79" if x in forprofit else "#9aa7b4") for x in peers["Short"]]
fig, ax = plt.subplots(figsize=(9,5))
ax.barh(peers["Short"], peers["NetMargin"]*100, color=colors)
for i,v in enumerate(peers["NetMargin"]*100):
    ax.text(v+0.1, i, f"{v:.1f}%", va="center", fontsize=9)
ax.set_title("nib runs a higher net margin than the mutual funds (FY25)", fontweight="bold")
ax.set_xlabel("Net margin = 1 - (claims + expenses) / premium revenue, %")
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="x", alpha=.3)
ax.text(0.98,0.05,"red = nib · blue = for-profit · grey = mutual/non-profit", transform=ax.transAxes,
        ha="right", fontsize=8, color="grey")
fig.text(.01,-.02,"Source: APRA Annual PHI Performance Statistics, FY2024-25.", fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig5_net_margin.png", bbox_inches="tight"); plt.close(fig)
print("\nSaved fig4, fig5.")
