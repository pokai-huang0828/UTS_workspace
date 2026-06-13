# -*- coding: utf-8 -*-
"""Explore APRA annual performance statistics database (insurer-level)."""
import pandas as pd, openpyxl
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40)
PATH = r"D:\KennyWorkLife\UTS_workspace\Foundation Studio\Assessment3\data\APRA_Performance_2024-25.xlsx"

wb = openpyxl.load_workbook(PATH, read_only=True, data_only=True)
print("SHEETS:", wb.sheetnames); wb.close()
print("=" * 80)
for sh in pd.ExcelFile(PATH).sheet_names:
    try:
        df = pd.read_excel(PATH, sheet_name=sh)
        print(f"\n### [{sh}]  shape={df.shape}")
        print("cols:", list(df.columns)[:25])
        print(df.head(6).to_string())
        for col in df.columns:
            if df[col].dtype == object and df[col].nunique() <= 40:
                u = list(df[col].dropna().unique())
                print(f"   · {col} ({df[col].nunique()}): {u[:40]}")
    except Exception as e:
        print(f"\n### [{sh}] ERROR: {e}")
