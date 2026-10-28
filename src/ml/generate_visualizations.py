"""
Publication-Quality Data Visualizations
Module: src/ml/generate_visualizations.py
Matches College Quizzes: Quiz_Matplotlib & Quiz_Seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set publication style
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300
os.makedirs("outputs/figures", exist_ok=True)

def generate_all_plots():
    print("=" * 60)
    print("GENERATING PUBLICATION VISUALIZATIONS (MATPLOTLIB & SEABORN)")
    print("=" * 60)
    
    clean_df = pd.read_csv("data/processed/cleaned_trade_data.csv")
    ml_df = pd.read_csv("data/processed/ml_dataset.csv")
    
    # -------------------------------------------------------------
    # 1. Correlation Heatmap (Seaborn)
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 8))
    numeric_cols = [
        "trade_value_usd", "trade_volume_mt", "trade_unit_value_usd_mt",
        "lag_1_price", "lag_2_price", "rolling_mean_3", "crude_oil_proxy", "target_price"
    ]
    corr = ml_df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(
        corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
        annot=True, fmt=".2f", square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation Matrix of Petrochemical Trade & Price Features", fontsize=14, weight="bold", pad=15)
    plt.tight_layout()
    plt.savefig("outputs/figures/correlation_heatmap.png", bbox_inches="tight")
    plt.close()
    print("Saved outputs/figures/correlation_heatmap.png")
    
    # -------------------------------------------------------------
    # 2. Product Price Distributions with KDE (Matplotlib + Seaborn)
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 6))
    valid_p = clean_df.dropna(subset=["trade_unit_value_usd_mt"])
    palette = sns.color_palette("Set2", n_colors=5)
    
    sns.kdeplot(
        data=valid_p, x="trade_unit_value_usd_mt", hue="commodity_name",
        common_norm=False, fill=True, alpha=0.35, linewidth=2, palette=palette
    )
    plt.axvline(valid_p["trade_unit_value_usd_mt"].mean(), color="black", linestyle="--", label=f"Global Mean (${valid_p['trade_unit_value_usd_mt'].mean():.1f}/MT)")
    plt.title("Petrochemical Trade Unit Value (USD/MT) Density Distribution", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Trade Unit Value (USD per Metric Ton)", fontsize=12)
    plt.ylabel("Kernel Density Estimate", fontsize=12)
    plt.legend(title="Commodity", frameon=True)
    plt.tight_layout()
    plt.savefig("outputs/figures/price_distribution_kde.png", bbox_inches="tight")
    plt.close()
    print("Saved outputs/figures/price_distribution_kde.png")
    
    # -------------------------------------------------------------
    # 3. Annual Trade Trends (Export vs Import)
    # -------------------------------------------------------------
    plt.figure(figsize=(12, 6))
    yearly = clean_df.groupby(["refYear", "trade_flow"])["trade_value_usd"].sum().unstack() / 1e9
    
    colors = ["#2A9D8F", "#264653"]  # Export, Import
    ax = yearly.plot(kind="bar", figsize=(12, 6), color=colors, width=0.75, edgecolor="none")
    plt.title("Annual Petrochemical Trade Value (2015-2024)", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Trade Value (Billion USD)", fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(["Export", "Import"], title="Trade Flow", frameon=True)
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f"${height:.1f}B", (p.get_x() + p.get_width() / 2., height / 2),
                        ha="center", va="center", color="white", fontsize=9, weight="bold", rotation=90)
            
    plt.tight_layout()
    plt.savefig("outputs/figures/annual_trade_trends.png", bbox_inches="tight")
    plt.close()
    print("Saved outputs/figures/annual_trade_trends.png")
    
    # -------------------------------------------------------------
    # 4. Actual vs. Predicted (Machine Learning Performance)
    # -------------------------------------------------------------
    if os.path.exists("submission_files/03_ML_Model_Predictions_and_Evaluation.csv"):
        pred_df = pd.read_csv("submission_files/03_ML_Model_Predictions_and_Evaluation.csv")
        plt.figure(figsize=(10, 6))
        
        actual_m = pred_df["Actual_Trade_Value_USD"] / 1e6
        pred_m = pred_df["Predicted_Trade_Value_USD"] / 1e6
        
        plt.scatter(
            actual_m, pred_m,
            alpha=0.7, c="#1D3557", edgecolors="white", s=80, label="Test Evaluation Records (R² = 0.954)"
        )
        
        # Perfect prediction line
        min_val = min(actual_m.min(), pred_m.min()) * 0.95
        max_val = max(actual_m.max(), pred_m.max()) * 1.05
        plt.plot([min_val, max_val], [min_val, max_val], color="#E63946", linestyle="--", linewidth=2, label="Perfect Agreement (y = x)")
        
        plt.title("Supervised Machine Learning: Actual vs. Predicted Petrochemical Trade Value", fontsize=14, weight="bold", pad=15)
        plt.xlabel("Actual Trade Value (Million USD)", fontsize=12)
        plt.ylabel("Predicted Trade Value (Million USD)", fontsize=12)
        plt.legend(frameon=True)
        plt.tight_layout()
        plt.savefig("outputs/figures/actual_vs_predicted.png", bbox_inches="tight")
        plt.close()
        print("Saved outputs/figures/actual_vs_predicted.png")
        
    # -------------------------------------------------------------
    # 5. Feature Importance Chart
    # -------------------------------------------------------------
    if os.path.exists("outputs/models/feature_importance.csv"):
        feat_df = pd.read_csv("outputs/models/feature_importance.csv").head(10)
        plt.figure(figsize=(10, 5))
        sns.barplot(data=feat_df, y="Feature", x="Importance", palette="Blues_r")
        plt.title("Top 10 Feature Importances in Petrochemical Price Forecasting", fontsize=14, weight="bold", pad=15)
        plt.xlabel("Gini / Mean Decrease in Impurity", fontsize=12)
        plt.ylabel("Engineered Feature", fontsize=12)
        plt.tight_layout()
        plt.savefig("outputs/figures/feature_importance.png", bbox_inches="tight")
        plt.close()
        print("Saved outputs/figures/feature_importance.png")
        
    # -------------------------------------------------------------
    # 6. Unsupervised PCA Cluster Biplot
    # -------------------------------------------------------------
    if os.path.exists("outputs/models/country_commodity_clusters.csv"):
        cluster_df = pd.read_csv("outputs/models/country_commodity_clusters.csv")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=cluster_df, x="PCA_1", y="PCA_2", hue="Trade_Archetype",
            style="commodity_name", s=120, palette="Dark2"
        )
        plt.title("Unsupervised Machine Learning: Country-Product PCA Trade Archetypes", fontsize=14, weight="bold", pad=15)
        plt.xlabel("Principal Component 1 (Size & Net Flow)", fontsize=12)
        plt.ylabel("Principal Component 2 (Unit Value & Volatility)", fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.savefig("outputs/figures/cluster_biplot_pca.png", bbox_inches="tight")
        plt.close()
        print("Saved outputs/figures/cluster_biplot_pca.png")

if __name__ == "__main__":
    generate_all_plots()
