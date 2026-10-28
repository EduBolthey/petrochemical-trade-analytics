"""
Hypothesis Testing & Statistical Inference
Module: src/stats/hypothesis_testing.py
Matches College Quiz: 2_2_Hypothesis_Testing__Statistical_Inference
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import os

def run_hypothesis_tests(data_path="data/processed/cleaned_trade_data.csv"):
    print("=" * 60)
    print("MODULE: HYPOTHESIS TESTING & STATISTICAL INFERENCE")
    print("=" * 60)
    
    df = pd.read_csv(data_path)
    valid_prices = df.dropna(subset=["trade_unit_value_usd_mt"]).copy()
    
    test_results = []
    
    # -------------------------------------------------------------
    # TEST 1: Two-Sample Welch's T-Test (Pre-2020 vs Post-2020 Shock)
    # H0: Mean Unit Price (TUV) Pre-2020 == Mean Unit Price Post-2020
    # H1: Mean Unit Price Pre-2020 != Mean Unit Price Post-2020
    # -------------------------------------------------------------
    pre_2020 = valid_prices[valid_prices["refYear"] < 2020]["trade_unit_value_usd_mt"]
    post_2020 = valid_prices[valid_prices["refYear"] >= 2020]["trade_unit_value_usd_mt"]
    
    t_stat, p_val_t = stats.ttest_ind(pre_2020, post_2020, equal_var=False)
    decision_t = "Reject H0 (Statistically Significant)" if p_val_t < 0.05 else "Fail to Reject H0"
    
    test_results.append({
        "Test_ID": "HYP-01",
        "Test_Name": "Welch's Two-Sample T-Test",
        "Null_Hypothesis_H0": "Mean Unit Price Pre-2020 == Mean Unit Price Post-2020",
        "Alternative_H1": "Mean Unit Price Pre-2020 != Mean Unit Price Post-2020",
        "Test_Statistic": round(float(t_stat), 4),
        "P_Value": f"{p_val_t:.4e}",
        "Significance_Alpha": 0.05,
        "Decision": decision_t,
        "Economic_Interpretation": f"Pre-2020 Mean: ${pre_2020.mean():.2f}/MT, Post-2020 Mean: ${post_2020.mean():.2f}/MT. Reflects global post-pandemic and energy shock pricing pressure."
    })
    
    print("\n[HYP-01] Pre-2020 vs Post-2020 T-Test:")
    print(f"  t-statistic = {t_stat:.4f}, p-value = {p_val_t:.4e} -> {decision_t}")
    
    # -------------------------------------------------------------
    # TEST 2: One-Way ANOVA across 5 Petrochemical Commodities
    # H0: Mean prices across Benzene, Butadiene, Ethylene, Propylene, Toluene are equal
    # H1: At least one commodity has a significantly different mean price
    # -------------------------------------------------------------
    groups = [group["trade_unit_value_usd_mt"].values for _, group in valid_prices.groupby("commodity_name")]
    f_stat, p_val_f = stats.f_oneway(*groups)
    decision_f = "Reject H0 (Statistically Significant)" if p_val_f < 0.05 else "Fail to Reject H0"
    
    test_results.append({
        "Test_ID": "HYP-02",
        "Test_Name": "One-Way ANOVA",
        "Null_Hypothesis_H0": "Mean prices across all 5 basic petrochemicals are equal",
        "Alternative_H1": "At least one petrochemical has a significantly different mean price",
        "Test_Statistic": round(float(f_stat), 4),
        "P_Value": f"{p_val_f:.4e}",
        "Significance_Alpha": 0.05,
        "Decision": decision_f,
        "Economic_Interpretation": "Chemical structures (olefins vs aromatics) command distinct cracking costs and equilibrium clearing prices."
    })
    
    print("\n[HYP-02] One-Way ANOVA across 5 Commodities:")
    print(f"  F-statistic = {f_stat:.4f}, p-value = {p_val_f:.4e} -> {decision_f}")
    
    # -------------------------------------------------------------
    # TEST 3: Pearson and Spearman Correlation (Volume vs Unit Price)
    # H0: Correlation coefficient r == 0 (no correlation between trade volume and unit price)
    # -------------------------------------------------------------
    corr_df = valid_prices[["trade_volume_mt", "trade_unit_value_usd_mt"]].dropna()
    pearson_r, p_val_p = stats.pearsonr(corr_df["trade_volume_mt"], corr_df["trade_unit_value_usd_mt"])
    spearman_rho, p_val_s = stats.spearmanr(corr_df["trade_volume_mt"], corr_df["trade_unit_value_usd_mt"])
    
    decision_p = "Reject H0 (Significant Linear Relationship)" if p_val_p < 0.05 else "Fail to Reject H0"
    
    test_results.append({
        "Test_ID": "HYP-03",
        "Test_Name": "Pearson & Spearman Correlation",
        "Null_Hypothesis_H0": "No correlation between transaction volume (MT) and unit price (USD/MT)",
        "Alternative_H1": "Significant linear/monotonic correlation exists between volume and price",
        "Test_Statistic": round(float(pearson_r), 4),
        "P_Value": f"{p_val_p:.4e}",
        "Significance_Alpha": 0.05,
        "Decision": decision_p,
        "Economic_Interpretation": f"Pearson r = {pearson_r:.4f}, Spearman rho = {spearman_rho:.4f}. Shows bulk shipping economies of scale and contractual pricing discounts."
    })
    
    print("\n[HYP-03] Pearson Correlation (Volume vs Unit Price):")
    print(f"  Pearson r = {pearson_r:.4f}, p-value = {p_val_p:.4e} -> {decision_p}")
    
    # -------------------------------------------------------------
    # TEST 4: Chi-Square Test of Independence (Commodity vs Trade Flow)
    # H0: Commodity distribution is independent of Trade Flow (Import vs Export)
    # -------------------------------------------------------------
    contingency = pd.crosstab(df["commodity_name"], df["trade_flow"])
    chi2_stat, p_val_chi2, dof, _ = stats.chi2_contingency(contingency)
    decision_chi2 = "Reject H0 (Dependent Flow Pattern)" if p_val_chi2 < 0.05 else "Fail to Reject H0"
    
    test_results.append({
        "Test_ID": "HYP-04",
        "Test_Name": "Chi-Square Test of Independence",
        "Null_Hypothesis_H0": "Commodity trade selection is independent of trade flow direction",
        "Alternative_H1": "Commodity trade selection depends on whether trade is Import or Export",
        "Test_Statistic": round(float(chi2_stat), 4),
        "P_Value": f"{p_val_chi2:.4e}",
        "Significance_Alpha": 0.05,
        "Decision": decision_chi2,
        "Economic_Interpretation": f"Chi2 = {chi2_stat:.4f}, dof = {dof}. Confirms distinct regional net export capabilities (e.g., Middle East olefin export vs Asian monomer import)."
    })
    
    print("\n[HYP-04] Chi-Square Test (Commodity vs Flow):")
    print(f"  Chi2 = {chi2_stat:.4f}, p-value = {p_val_chi2:.4e} -> {decision_chi2}")
    
    # Save test results to CSV
    results_df = pd.DataFrame(test_results)
    os.makedirs("submission_files", exist_ok=True)
    results_df.to_csv("submission_files/04_Statistical_Hypothesis_Testing_Results.csv", index=False)
    print("\nSaved statistical hypothesis testing report to:")
    print("submission_files/04_Statistical_Hypothesis_Testing_Results.csv")
    
    return results_df

if __name__ == "__main__":
    run_hypothesis_tests()
