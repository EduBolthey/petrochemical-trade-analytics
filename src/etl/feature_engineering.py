"""
ETL Step 3: Feature Engineering for Petrochemical Price Forecasting
"""

import pandas as pd
import numpy as np
import os

def engineer_features(input_path="data/processed/monthly_trade_data.csv", output_path="data/processed/ml_dataset.csv"):
    print("=" * 60)
    print("ETL STEP 3: FEATURE ENGINEERING")
    print("=" * 60)
    
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["commodity_name", "trade_flow", "date"]).reset_index(drop=True)
    
    # Crude oil index proxy by year/month (Brent index normalized, base 100 in 2015)
    crude_oil_year_index = {
        2015: 52.4, 2016: 43.7, 2017: 54.2, 2018: 71.3, 2019: 64.2,
        2020: 41.8, 2021: 70.9, 2022: 99.0, 2023: 82.2, 2024: 80.5
    }
    
    df["crude_oil_proxy"] = df["refYear"].map(crude_oil_year_index) + np.sin(df["refMonth"] * np.pi / 6) * 3.5
    
    group = df.groupby(["commodity_name", "trade_flow"])
    
    # 1. Temporal calendar features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    
    # 2. Price Lag Features
    df["lag_1_price"] = group["trade_unit_value_usd_mt"].shift(1)
    df["lag_2_price"] = group["trade_unit_value_usd_mt"].shift(2)
    df["lag_3_price"] = group["trade_unit_value_usd_mt"].shift(3)
    df["lag_6_price"] = group["trade_unit_value_usd_mt"].shift(6)
    
    # 3. Volume and Value Lags
    df["volume_lag_1"] = group["trade_volume_mt"].shift(1)
    df["volume_lag_3"] = group["trade_volume_mt"].shift(3)
    df["value_lag_1"] = group["trade_value_usd"].shift(1)
    df["value_lag_3"] = group["trade_value_usd"].shift(3)
    
    # 4. Rolling Statistics
    df["rolling_mean_3"] = group["trade_unit_value_usd_mt"].transform(lambda x: x.shift(1).rolling(3, min_periods=1).mean())
    df["rolling_mean_6"] = group["trade_unit_value_usd_mt"].transform(lambda x: x.shift(1).rolling(6, min_periods=1).mean())
    df["rolling_std_3"] = group["trade_unit_value_usd_mt"].transform(lambda x: x.shift(1).rolling(3, min_periods=1).std()).fillna(0)
    df["rolling_std_6"] = group["trade_unit_value_usd_mt"].transform(lambda x: x.shift(1).rolling(6, min_periods=1).std()).fillna(0)
    
    # 5. Price Momentum and Volatility
    df["price_change_1"] = df["lag_1_price"] - df["lag_2_price"]
    df["price_pct_change_1"] = ((df["lag_1_price"] - df["lag_2_price"]) / (df["lag_2_price"] + 1e-5)) * 100
    
    # 6. Target Variable: Next month's unit price
    df["target_price"] = group["trade_unit_value_usd_mt"].shift(-1)
    
    # Drop rows where essential features or target are missing
    feature_cols = [
        "lag_1_price", "lag_2_price", "lag_3_price",
        "volume_lag_1", "value_lag_1",
        "rolling_mean_3", "target_price"
    ]
    df_ml = df.dropna(subset=feature_cols).copy().reset_index(drop=True)
    
    df_ml.to_csv(output_path, index=False)
    print(f"ML Dataset Created: {len(df_ml)} rows, {len(df_ml.columns)} columns")
    print(f"Saved to: {output_path}")
    return df_ml

if __name__ == "__main__":
    engineer_features()
