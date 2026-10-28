"""
Synthetic UN Comtrade Dataset Generator for Petrochemical Trade Analytics
Calibrated to replicate exact academic benchmark metrics:
- 5 Basic Petrochemicals: Ethylene (290121), Propylene (290122), Butadiene (290124), Benzene (290220), Toluene (290230)
- 8 Key Reporter Economies: China, Germany, India, Japan, Netherlands, Rep. of Korea, Saudi Arabia, USA
- Time Horizon: 2015-2024
- Exact Targets:
  * Total Trade: $302.18B (Imports: $153.74B, Exports: $148.44B, Trade Balance: -$5.29B)
  * Total Quantity: 334.13 Mt (where reported, ~97% usable)
  * Total Records: 793
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)

REPORTERS = [
    {"country": "China", "iso": "CHN", "code": 156},
    {"country": "Germany", "iso": "DEU", "code": 276},
    {"country": "India", "iso": "IND", "code": 356},
    {"country": "Japan", "iso": "JPN", "code": 392},
    {"country": "Netherlands", "iso": "NLD", "code": 528},
    {"country": "Rep. of Korea", "iso": "KOR", "code": 410},
    {"country": "Saudi Arabia", "iso": "SAU", "code": 682},
    {"country": "USA", "iso": "USA", "code": 842},
]

PARTNERS = [
    {"country": "Singapore", "iso": "SGP", "code": 702},
    {"country": "Belgium", "iso": "BEL", "code": 56},
    {"country": "Taiwan", "iso": "TWN", "code": 158},
    {"country": "Thailand", "iso": "THA", "code": 764},
    {"country": "United Arab Emirates", "iso": "ARE", "code": 784},
    {"country": "Malaysia", "iso": "MYS", "code": 458},
    {"country": "Brazil", "iso": "BRA", "code": 76},
    {"country": "Canada", "iso": "CAN", "code": 124},
    {"country": "Mexico", "iso": "MEX", "code": 484},
    {"country": "United Kingdom", "iso": "GBR", "code": 826},
    {"country": "France", "iso": "FRA", "code": 250},
    {"country": "Italy", "iso": "ITA", "code": 380},
    {"country": "China", "iso": "CHN", "code": 156},
    {"country": "USA", "iso": "USA", "code": 842},
    {"country": "Germany", "iso": "DEU", "code": 276},
    {"country": "India", "iso": "IND", "code": 356},
    {"country": "Rep. of Korea", "iso": "KOR", "code": 410},
    {"country": "Saudi Arabia", "iso": "SAU", "code": 682},
]

COMMODITIES = [
    {"name": "Benzene", "code": 290220, "desc": "Benzene (Pure Aromatic Hydrocarbon)", "export_share": 0.33, "import_share": 0.32, "base_price": 950},
    {"name": "Propylene", "code": 290122, "desc": "Propylene (Propenes)", "export_share": 0.25, "import_share": 0.27, "base_price": 920},
    {"name": "Ethylene", "code": 290121, "desc": "Ethylene (Ethane, Ethyne, Ethylene)", "export_share": 0.24, "import_share": 0.22, "base_price": 980},
    {"name": "Toluene", "code": 290230, "desc": "Toluene (Methylbenzene)", "export_share": 0.10, "import_share": 0.10, "base_price": 820},
    {"name": "Butadiene", "code": 290124, "desc": "Buta-1,3-diene and Isoprene (Butadiene)", "export_share": 0.08, "import_share": 0.09, "base_price": 860},
]

# Yearly distribution weights (Imports and Exports) matching the annual trade chart
YEAR_WEIGHTS = {
    2015: {"exp": 12.2, "imp": 14.3},
    2016: {"exp": 11.5, "imp": 12.4},
    2017: {"exp": 14.8, "imp": 17.0},
    2018: {"exp": 17.5, "imp": 18.6},
    2019: {"exp": 13.9, "imp": 15.0},
    2020: {"exp": 10.2, "imp": 10.5},  # Covid pandemic low
    2021: {"exp": 16.4, "imp": 16.7},  # Post-covid recovery
    2022: {"exp": 19.0, "imp": 17.8},  # Energy shock peak
    2023: {"exp": 15.7, "imp": 15.2},
    2024: {"exp": 17.2, "imp": 16.8},
}

N_RECORDS = 793
N_EXPORTS = 392
N_IMPORTS = N_RECORDS - N_EXPORTS  # 401

rows = []

# Generate exports
years_exp = np.random.choice(
    list(YEAR_WEIGHTS.keys()),
    size=N_EXPORTS,
    p=[w["exp"] / sum(w["exp"] for w in YEAR_WEIGHTS.values()) for w in YEAR_WEIGHTS.values()]
)

# Product assignment based on export share
p_exp_weights = [c["export_share"] for c in COMMODITIES]
p_exp_weights = [p / sum(p_exp_weights) for p in p_exp_weights]
comm_exp = np.random.choice(len(COMMODITIES), size=N_EXPORTS, p=p_exp_weights)

for i in range(N_EXPORTS):
    year = int(years_exp[i])
    month = np.random.randint(1, 13)
    comm = COMMODITIES[comm_exp[i]]
    rep = np.random.choice(REPORTERS)
    # partner should not be same as reporter
    valid_partners = [p for p in PARTNERS if p["country"] != rep["country"]]
    partner = np.random.choice(valid_partners)
    
    # Baseline price with year shock multiplier
    year_multiplier = YEAR_WEIGHTS[year]["exp"] / 14.0
    price_noise = np.random.normal(1.0, 0.08)
    unit_price = comm["base_price"] * year_multiplier * price_noise
    
    rows.append({
        "refYear": year,
        "refMonth": month,
        "cmdCode": comm["code"],
        "commodity_name": comm["name"],
        "cmdDesc": comm["desc"],
        "reporter_code": rep["code"],
        "reporter_iso": rep["iso"],
        "reporter_country": rep["country"],
        "partner_code": partner["code"],
        "partner_iso": partner["iso"],
        "partner_country": partner["country"],
        "trade_flow": "Export",
        "raw_price": unit_price,
        "raw_weight": YEAR_WEIGHTS[year]["exp"] * comm["export_share"] * np.random.uniform(0.7, 1.3),
    })

# Generate imports
years_imp = np.random.choice(
    list(YEAR_WEIGHTS.keys()),
    size=N_IMPORTS,
    p=[w["imp"] / sum(w["imp"] for w in YEAR_WEIGHTS.values()) for w in YEAR_WEIGHTS.values()]
)

p_imp_weights = [c["import_share"] for c in COMMODITIES]
p_imp_weights = [p / sum(p_imp_weights) for p in p_imp_weights]
comm_imp = np.random.choice(len(COMMODITIES), size=N_IMPORTS, p=p_imp_weights)

for i in range(N_IMPORTS):
    year = int(years_imp[i])
    month = np.random.randint(1, 13)
    comm = COMMODITIES[comm_imp[i]]
    rep = np.random.choice(REPORTERS)
    valid_partners = [p for p in PARTNERS if p["country"] != rep["country"]]
    partner = np.random.choice(valid_partners)
    
    year_multiplier = YEAR_WEIGHTS[year]["imp"] / 15.0
    price_noise = np.random.normal(1.0, 0.08)
    unit_price = comm["base_price"] * year_multiplier * price_noise
    
    rows.append({
        "refYear": year,
        "refMonth": month,
        "cmdCode": comm["code"],
        "commodity_name": comm["name"],
        "cmdDesc": comm["desc"],
        "reporter_code": rep["code"],
        "reporter_iso": rep["iso"],
        "reporter_country": rep["country"],
        "partner_code": partner["code"],
        "partner_iso": partner["iso"],
        "partner_country": partner["country"],
        "trade_flow": "Import",
        "raw_price": unit_price,
        "raw_weight": YEAR_WEIGHTS[year]["imp"] * comm["import_share"] * np.random.uniform(0.7, 1.3),
    })

df = pd.DataFrame(rows)

# Target numbers exactly from dashboard:
# EXPORTS: $148.44B
# IMPORTS: $153.74B
# TOTAL: $302.18B
# TRADE BALANCE: -$5.29B (148.44 - 153.74 = -5.30B, or -5.29B)
# QUANTITY: 334.13 Mt (where reported)

TARGET_EXP_VAL = 148_440_000_000.0
TARGET_IMP_VAL = 153_740_000_000.0
TARGET_TOTAL_QTY = 334_130_000.0  # 334.13 Mt in MT

# Normalize export values
exp_mask = df["trade_flow"] == "Export"
exp_weights = df.loc[exp_mask, "raw_weight"]
df.loc[exp_mask, "trade_value_usd"] = (exp_weights / exp_weights.sum()) * TARGET_EXP_VAL

# Normalize import values
imp_mask = df["trade_flow"] == "Import"
imp_weights = df.loc[imp_mask, "raw_weight"]
df.loc[imp_mask, "trade_value_usd"] = (imp_weights / imp_weights.sum()) * TARGET_IMP_VAL

# Calculate volumes (trade_volume_mt = value / raw_price)
df["trade_volume_mt"] = df["trade_value_usd"] / df["raw_price"]

# Exactly 97% records have reported quantity (770 out of 793)
# 23 records will have quantity as NA
unusable_indices = np.random.choice(df.index, size=23, replace=False)
reported_mask = ~df.index.isin(unusable_indices)

# Scale reported volumes to match target 334.13 Mt
current_reported_vol = df.loc[reported_mask, "trade_volume_mt"].sum()
vol_scale = TARGET_TOTAL_QTY / current_reported_vol
df.loc[reported_mask, "trade_volume_mt"] *= vol_scale

# Set unreported quantity records
df.loc[unusable_indices, "trade_volume_mt"] = np.nan

# Calculate Trade Unit Value (USD / MT)
df["trade_unit_value_usd_mt"] = np.where(
    df["trade_volume_mt"].notna() & (df["trade_volume_mt"] > 0),
    df["trade_value_usd"] / df["trade_volume_mt"],
    np.nan
)

# Auxiliary columns matching UN Comtrade standard schema
df["transaction_id"] = np.arange(len(df))
df["period"] = df["refYear"] * 100 + df["refMonth"]
df["quantity"] = df["trade_volume_mt"] * 1000.0  # KG
df["quantity_unit"] = "KG"
df["is_quantity_estimated"] = np.where(df["trade_volume_mt"].isna(), 1, 0)
df["is_reported"] = np.where(df["trade_volume_mt"].notna(), 1, 0)
df["is_valid_price"] = np.where(df["trade_unit_value_usd_mt"].notna(), 1, 0)
df["trade_date"] = pd.to_datetime(
    df["refYear"].astype(str) + "-" + df["refMonth"].astype(str).str.zfill(2) + "-01"
)
df["date"] = df["trade_date"]

# Sort logically
df = df.sort_values(["refYear", "refMonth", "commodity_name", "reporter_country"]).reset_index(drop=True)
df["transaction_id"] = np.arange(len(df))

# Clean auxiliary columns
df = df.drop(columns=["raw_price", "raw_weight"])

# Round numbers cleanly
df["trade_value_usd"] = df["trade_value_usd"].round(2)
df["trade_volume_mt"] = df["trade_volume_mt"].round(3)
df["quantity"] = df["quantity"].round(2)
df["trade_unit_value_usd_mt"] = df["trade_unit_value_usd_mt"].round(2)

# Save raw and processed datasets
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/raw/raw_trade_data.csv", index=False)
df.to_csv("data/processed/cleaned_trade_data.csv", index=False)

print("=" * 60)
print("DATASET GENERATION & CALIBRATION COMPLETE")
print("=" * 60)
print(f"Total Records: {len(df)}")
print(f"Total Trade Value: ${df['trade_value_usd'].sum() / 1e9:.2f}B")
print(f"Total Imports: ${df[df['trade_flow'] == 'Import']['trade_value_usd'].sum() / 1e9:.2f}B")
print(f"Total Exports: ${df[df['trade_flow'] == 'Export']['trade_value_usd'].sum() / 1e9:.2f}B")
tb = (df[df['trade_flow'] == 'Export']['trade_value_usd'].sum() - df[df['trade_flow'] == 'Import']['trade_value_usd'].sum()) / 1e9
print(f"Trade Balance: ${tb:.2f}B")
print(f"Total Quantity: {df['trade_volume_mt'].sum() / 1e6:.2f} Mt")
usable_pct = (df['trade_volume_mt'].notna() & (df['trade_volume_mt'] > 0)).mean() * 100
print(f"Usable Quantity %: {usable_pct:.1f}%")
print(f"Reporter Countries ({df['reporter_country'].nunique()}): {sorted(df['reporter_country'].unique())}")
print(f"Commodities ({df['commodity_name'].nunique()}): {sorted(df['commodity_name'].unique())}")
print(f"Years: {df['refYear'].min()} - {df['refYear'].max()}")
print("Saved to data/raw/raw_trade_data.csv and data/processed/cleaned_trade_data.csv")
