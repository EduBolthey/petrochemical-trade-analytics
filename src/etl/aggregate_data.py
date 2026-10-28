"""
ETL Step 2: Time Series and Dimensional Aggregations
"""

import pandas as pd
import numpy as np
import os

def aggregate_data(input_path="data/processed/cleaned_trade_data.csv"):
    print("=" * 60)
    print("ETL STEP 2: DATA AGGREGATION")
    print("=" * 60)
    
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    
    # 1. Monthly Product-Flow Aggregation (Primary dataset for ML time-series forecasting)
    group_cols = ["date", "refYear", "refMonth", "cmdCode", "commodity_name", "trade_flow"]
    monthly_df = df.groupby(group_cols, as_index=False).agg(
        trade_volume_mt=("trade_volume_mt", "sum"),
        trade_value_usd=("trade_value_usd", "sum"),
        transaction_count=("transaction_id", "count")
    )
    
    # Calculate monthly weighted trade unit value
    monthly_df["trade_unit_value_usd_mt"] = np.where(
        monthly_df["trade_volume_mt"] > 0,
        monthly_df["trade_value_usd"] / monthly_df["trade_volume_mt"],
        np.nan
    )
    
    # Sort
    monthly_df = monthly_df.sort_values(["commodity_name", "trade_flow", "date"]).reset_index(drop=True)
    monthly_df.to_csv("data/processed/monthly_trade_data.csv", index=False)
    print(f"Saved monthly aggregated dataset: {len(monthly_df)} rows")
    
    # 2. Annual Country-Product Balance Aggregation
    annual_df = df.groupby(["refYear", "reporter_country", "commodity_name", "trade_flow"], as_index=False).agg(
        trade_volume_mt=("trade_volume_mt", "sum"),
        trade_value_usd=("trade_value_usd", "sum")
    )
    annual_df.to_csv("data/processed/annual_trade_data.csv", index=False)
    print(f"Saved annual aggregated dataset: {len(annual_df)} rows")
    
    return monthly_df, annual_df

if __name__ == "__main__":
    aggregate_data()
