# -*- coding: utf-8 -*-
"""Fig 6: NHF (nib) share price vs ASX200, indexed. Source: Yahoo Finance chart API (monthly)."""
import json, pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3")
DATA, FIG = BASE/"data", BASE/"figures"

def load(name):
    j = json.loads((DATA/f"yahoo_{name}.json").read_text(encoding="utf-8"))
    r = j["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s")
    close = r["indicators"]["quote"][0]["close"]   # price (close) for a like-for-like comparison
    return pd.Series(close, index=ts, name=name).dropna()

nhf, axjo = load("NHF"), load("AXJO")
df = pd.concat([nhf, axjo], axis=1).dropna()
df.index = df.index.to_period("M").to_timestamp()
idx = df / df.iloc[0] * 100

print(f"Window: {idx.index[0].date()} -> {idx.index[-1].date()}")
print(f"NHF total return (index): {idx['NHF'].iloc[-1]:.0f}  | ASX200: {idx['AXJO'].iloc[-1]:.0f}")
print(idx.iloc[::12].round(0).to_string())

plt.rcParams.update({"figure.dpi":150,"axes.grid":True,"grid.alpha":.3,"font.size":11,
                     "axes.spines.top":False,"axes.spines.right":False})
fig, ax = plt.subplots(figsize=(9,5))
ax.plot(idx.index, idx["NHF"], color="#c0392b", lw=2, label="nib (NHF)")
ax.plot(idx.index, idx["AXJO"], color="#888888", lw=2, ls="--", label="ASX 200")
ax.axhline(100, color="k", lw=.6, alpha=.4)
ax.set_title(f"nib's share price has far outpaced the ASX 200 since {idx.index[0].year}", fontweight="bold")
ax.set_ylabel(f"Share price, indexed ({idx.index[0].strftime('%b %Y')} = 100)")
ax.legend(frameon=False, loc="upper left")
fig.text(.01,-.02,"Source: Yahoo Finance (monthly close price). Price return, dividends excluded.", fontsize=8, color="grey")
fig.tight_layout(); fig.savefig(FIG/"fig6_share_price.png", bbox_inches="tight"); plt.close(fig)
print("Saved fig6.")
