"""
Descriptive Statistics & Exploratory Statistical Analysis
Module: src/stats/descriptive_stats.py
Matches College Quiz: 2_1_Descriptive_Statistics__Probability_Basics
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import os

def run_descriptive_analysis(data_path="data/processed/cleaned_trade_data.csv"):
    print("=" * 60)
    print("MODULE: DESCRIPTIVE STATISTICS & PROBABILITY BASICS")
    print("=" * 60)
    
    df = pd.read_csv(data_path)
    
    # 1. Overall Numeric Statistics
    cols = ["trade_value_usd", "trade_volume_mt", "trade_unit_value_usd_mt"]
    summary_list = []
    
    for col in cols:
        series = df[col].dropna()
        summary_list.append({
            "Metric_Variable": col,
            "Count": len(series),
            "Mean": series.mean(),
            "Median": series.median(),
            "Std_Dev": series.std(),
            "Variance": series.var(),
            "Min": series.min(),
            "Q25": series.quantile(0.25),
            "Q75": series.quantile(0.75),
            "IQR": series.quantile(0.75) - series.quantile(0.25),
            "Max": series.max(),
            "Skewness": float(stats.skew(series)),
            "Kurtosis": float(stats.kurtosis(series))
        })
        
    overall_stats = pd.DataFrame(summary_list)
    print("\n--- OVERALL DESCRIPTIVE SUMMARY ---")
    print(overall_stats.to_string(index=False))
    
    # 2. Product-wise Unit Price Distribution
    print("\n--- PRODUCT-WISE UNIT PRICE (USD/MT) STATISTICS ---")
    prod_summary = df.groupby("commodity_name")["trade_unit_value_usd_mt"].agg(
        Count="count",
        Mean="mean",
        Median="median",
        Std="std",
        Min="min",
        Max="max",
        Skewness=lambda x: float(stats.skew(x.dropna()))
    ).reset_index()
    print(prod_summary.to_string(index=False))
    
    # 3. Country-wise Trade Summary
    print("\n--- REPORTER COUNTRY TOTAL TRADE VALUE & VOLUME ---")
    country_summary = df.groupby("reporter_country").agg(
        Total_Trade_USD=("trade_value_usd", "sum"),
        Total_Volume_MT=("trade_volume_mt", "sum"),
        Record_Count=("transaction_id", "count")
    ).reset_index()
    print(country_summary.to_string(index=False))
    
    return overall_stats, prod_summary, country_summary

if __name__ == "__main__":
    run_descriptive_analysis()
