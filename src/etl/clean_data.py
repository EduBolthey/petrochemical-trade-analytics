"""
ETL Step 1: Clean and Validate Raw Trade Data
"""

import pandas as pd
import numpy as np
import os

def clean_trade_data(input_path="data/raw/raw_trade_data.csv", output_path="data/processed/cleaned_trade_data.csv"):
    print("=" * 60)
    print("ETL STEP 1: CLEANING TRADE DATA")
    print("=" * 60)
    
    df = pd.read_csv(input_path)
    print(f"Loaded raw records: {len(df)}")
    
    # 1. Type normalization
    df["refYear"] = pd.to_numeric(df["refYear"], errors="coerce").astype(int)
    df["refMonth"] = pd.to_numeric(df["refMonth"], errors="coerce").astype(int)
    df["trade_value_usd"] = pd.to_numeric(df["trade_value_usd"], errors="coerce")
    df["trade_volume_mt"] = pd.to_numeric(df["trade_volume_mt"], errors="coerce")
    
    # 2. Re-compute Trade Unit Value where volume is strictly positive
    valid_vol_mask = (df["trade_volume_mt"] > 0) & df["trade_volume_mt"].notna()
    df.loc[valid_vol_mask, "trade_unit_value_usd_mt"] = (
        df.loc[valid_vol_mask, "trade_value_usd"] / df.loc[valid_vol_mask, "trade_volume_mt"]
    )
    df.loc[~valid_vol_mask, "trade_unit_value_usd_mt"] = np.nan
    
    # 3. Standardize dates
    df["date"] = pd.to_datetime(
        df["refYear"].astype(str) + "-" + df["refMonth"].astype(str).str.zfill(2) + "-01"
    )
    
    # 4. Outlier flags based on IQR (for reporting & analysis)
    q25 = df.loc[valid_vol_mask, "trade_unit_value_usd_mt"].quantile(0.25)
    q75 = df.loc[valid_vol_mask, "trade_unit_value_usd_mt"].quantile(0.75)
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    df["is_price_outlier"] = np.where(
        valid_vol_mask & ((df["trade_unit_value_usd_mt"] < lower_bound) | (df["trade_unit_value_usd_mt"] > upper_bound)),
        1, 0
    )
    
    # 5. Remove infinite values and sort
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.sort_values(["date", "commodity_name", "trade_flow", "reporter_country"]).reset_index(drop=True)
    df["transaction_id"] = np.arange(len(df))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Cleaned records: {len(df)}")
    print(f"Missing volumes: {df['trade_volume_mt'].isna().sum()} ({df['trade_volume_mt'].isna().mean() * 100:.2f}%)")
    print(f"Identified price outliers: {df['is_price_outlier'].sum()}")
    print(f"Saved cleaned data to: {output_path}")
    return df

if __name__ == "__main__":
    clean_trade_data()
