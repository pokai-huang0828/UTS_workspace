# -*- coding: utf-8 -*-
"""Inspect the tidy data sheets + contents index."""
import pandas as pd
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 60)

PATH = r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3\data\APRA_Membership_Trends_Mar2026.xlsx"

# 1) Contents index
print("################ CONTENTS ################")
c = pd.read_excel(PATH, sheet_name="Contents", header=None)
print(c.dropna(how="all").to_string(max_rows=70))

# 2) Tidy data sheets
for sh in ["MembershipByAgeData", "MembershipData"]:
    print(f"\n################ {sh} ################")
    df = pd.read_excel(PATH, sheet_name=sh)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print(df.head(4).to_string())
    # unique values of low-cardinality object columns
    for col in df.columns:
        if df[col].dtype == object or df[col].nunique() <= 25:
            u = df[col].dropna().unique()
            if len(u) <= 30:
                print(f"  · {col} ({df[col].nunique()}): {list(u)[:30]}")
