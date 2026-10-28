"""
Unsupervised Machine Learning & Evaluation Metrics
Module: src/ml/unsupervised_clustering.py
Matches College Quiz: Quiz_Unsupervised_ML_EvaluationMetrics
"""

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def run_unsupervised_pipeline(data_path="data/processed/cleaned_trade_data.csv"):
    print("=" * 60)
    print("MODULE: UNSUPERVISED MACHINE LEARNING & EVALUATION")
    print("=" * 60)
    
    df = pd.read_csv(data_path)
    
    # 1. Aggregate into Country-Commodity Trade Profile
    profile = df.groupby(["reporter_country", "commodity_name"]).agg(
        Total_Export_USD=("trade_value_usd", lambda x: x[df.loc[x.index, "trade_flow"] == "Export"].sum()),
        Total_Import_USD=("trade_value_usd", lambda x: x[df.loc[x.index, "trade_flow"] == "Import"].sum()),
        Total_Volume_MT=("trade_volume_mt", "sum"),
        Mean_Unit_Price_USD_MT=("trade_unit_value_usd_mt", "mean"),
        Price_Std_USD_MT=("trade_unit_value_usd_mt", "std")
    ).reset_index().fillna(0)
    
    profile["Net_Trade_Balance_USD"] = profile["Total_Export_USD"] - profile["Total_Import_USD"]
    profile["Export_to_Import_Ratio"] = (profile["Total_Export_USD"] + 1) / (profile["Total_Import_USD"] + 1)
    
    feature_cols = [
        "Total_Export_USD", "Total_Import_USD", "Total_Volume_MT",
        "Mean_Unit_Price_USD_MT", "Net_Trade_Balance_USD", "Export_to_Import_Ratio"
    ]
    
    X = profile[feature_cols].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. K-Means Clustering & Metric Evaluation across k=2,3,4,5
    clustering_metrics = []
    best_k = 3
    best_sil = -1
    
    for k in [2, 3, 4, 5]:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        
        sil = silhouette_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        
        clustering_metrics.append({
            "Clusters_k": k,
            "Silhouette_Score": round(sil, 4),
            "Davies_Bouldin_Index": round(db, 4),
            "Calinski_Harabasz_Index": round(ch, 2)
        })
        
        if sil > best_sil:
            best_sil = sil
            best_k = k
            
    metrics_df = pd.DataFrame(clustering_metrics)
    print("\n--- K-MEANS CLUSTERING EVALUATION METRICS ---")
    print(metrics_df.to_string(index=False))
    
    # Fit optimal K-Means
    optimal_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    profile["Cluster_ID"] = optimal_kmeans.fit_predict(X_scaled)
    
    cluster_names = {
        0: "Balanced Regional Traders",
        1: "Major Feedstock Exporters",
        2: "High-Volume Petrochemical Importers"
    }
    profile["Trade_Archetype"] = profile["Cluster_ID"].map(cluster_names).fillna("Specialized Trader")
    
    # 3. Principal Component Analysis (PCA)
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_scaled)
    profile["PCA_1"] = pca_coords[:, 0]
    profile["PCA_2"] = pca_coords[:, 1]
    
    var_exp = pca.explained_variance_ratio_
    print(f"\n--- PCA DIMENSIONALITY REDUCTION ---")
    print(f"PC1 Variance Explained: {var_exp[0]*100:.2f}%")
    print(f"PC2 Variance Explained: {var_exp[1]*100:.2f}%")
    print(f"Total 2D Variance Captured: {sum(var_exp)*100:.2f}%")
    
    # 4. Anomaly Detection using Isolation Forest
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    profile["Is_Anomaly"] = iso_forest.fit_predict(X_scaled)
    profile["Is_Anomaly"] = np.where(profile["Is_Anomaly"] == -1, 1, 0)
    print(f"\n--- ISOLATION FOREST ANOMALIES DETECTED ---")
    print(f"Anomalous Trade Profiles: {profile['Is_Anomaly'].sum()} out of {len(profile)}")
    
    os.makedirs("outputs/models", exist_ok=True)
    metrics_df.to_csv("outputs/models/unsupervised_clustering_metrics.csv", index=False)
    profile.to_csv("outputs/models/country_commodity_clusters.csv", index=False)
    print("Saved clustering outputs to outputs/models/")
    
    return metrics_df, profile

if __name__ == "__main__":
    run_unsupervised_pipeline()
