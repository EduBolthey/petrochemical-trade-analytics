"""
Supervised Machine Learning Pipeline for Petrochemical Trade Analytics
Module: src/ml/train_models.py
Matches College Quizzes: Quiz_Supervised_ML_Evaluation & Model_Evaluation_and_Practical_Use_Cases
Demonstrates: Linear Regression, Ridge, Random Forest, and Gradient Boosting Regressors
"""

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_evaluate_models():
    print("=" * 60)
    print("MODULE: SUPERVISED MACHINE LEARNING & EVALUATION")
    print("=" * 60)
    
    df = pd.read_csv("data/processed/cleaned_trade_data.csv")
    df = df.dropna(subset=["trade_unit_value_usd_mt", "trade_volume_mt"]).copy()
    
    # Add crude oil proxy and seasonal indicators
    crude_oil_year_index = {
        2015: 52.4, 2016: 43.7, 2017: 54.2, 2018: 71.3, 2019: 64.2,
        2020: 41.8, 2021: 70.9, 2022: 99.0, 2023: 82.2, 2024: 80.5
    }
    df["crude_oil_proxy"] = df["refYear"].map(crude_oil_year_index)
    df["quarter"] = (df["refMonth"] - 1) // 3 + 1
    
    # Target 1: Trade Value (USD)
    features_val = [
        "commodity_name", "reporter_country", "partner_country",
        "trade_flow", "refYear", "quarter", "crude_oil_proxy", "trade_volume_mt"
    ]
    
    categorical_val = ["commodity_name", "reporter_country", "partner_country", "trade_flow"]
    numerical_val = ["refYear", "quarter", "crude_oil_proxy", "trade_volume_mt"]
    
    X = df[features_val]
    y = df["trade_value_usd"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_val),
            ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numerical_val)
        ]
    )
    
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression (Alpha=1.0)": Ridge(alpha=1.0, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=250, max_depth=15, random_state=42, n_jobs=-1),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=250, learning_rate=0.05, max_depth=5, random_state=42)
    }
    
    results = []
    best_model_name = None
    best_r2 = -1e9
    best_pipeline = None
    
    print("\n--- MODEL PERFORMANCE EVALUATION (TARGET: TRADE VALUE USD) ---")
    for name, model in models.items():
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        mape = np.mean(np.abs((y_test - preds) / y_test)) * 100
        
        results.append({
            "Model": name,
            "Target": "Trade_Value_USD",
            "MAE_USD": round(mae, 2),
            "RMSE_USD": round(rmse, 2),
            "R2_Score": round(r2, 4),
            "MAPE_Percent": round(mape, 2)
        })
        
        print(f"[{name}]")
        print(f"  MAE: ${mae/1e6:.2f}M | RMSE: ${rmse/1e6:.2f}M | R2: {r2:.4f} | MAPE: {mape:.2f}%\n")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline
            
    results_df = pd.DataFrame(results)
    
    # Save best model
    os.makedirs("outputs/models", exist_ok=True)
    os.makedirs("submission_files", exist_ok=True)
    joblib.dump(best_pipeline, "outputs/models/best_petrochemical_model.pkl")
    print(f"Best Supervised Model: {best_model_name} (R2={best_r2:.4f}) saved to outputs/models/best_petrochemical_model.pkl")
    
    # Save predictions dataframe
    test_eval_df = X_test.copy()
    test_eval_df["Actual_Trade_Value_USD"] = y_test.values
    test_eval_df["Predicted_Trade_Value_USD"] = best_pipeline.predict(X_test)
    test_eval_df["Absolute_Error_USD"] = np.abs(test_eval_df["Actual_Trade_Value_USD"] - test_eval_df["Predicted_Trade_Value_USD"])
    test_eval_df["Percentage_Error"] = (test_eval_df["Absolute_Error_USD"] / test_eval_df["Actual_Trade_Value_USD"]) * 100
    test_eval_df["Actual_TUV_USD_MT"] = test_eval_df["Actual_Trade_Value_USD"] / test_eval_df["trade_volume_mt"]
    test_eval_df["Predicted_TUV_USD_MT"] = test_eval_df["Predicted_Trade_Value_USD"] / test_eval_df["trade_volume_mt"]
    
    test_eval_df.to_csv("submission_files/03_ML_Model_Predictions_and_Evaluation.csv", index=False)
    results_df.to_csv("outputs/models/model_benchmark_comparison.csv", index=False)
    print("Saved evaluation predictions to submission_files/03_ML_Model_Predictions_and_Evaluation.csv")
    
    # Feature Importances
    try:
        model_step = best_pipeline.named_steps["model"]
        if hasattr(model_step, "feature_importances_"):
            cat_encoder = best_pipeline.named_steps["preprocessor"].transformers_[0][1]
            cat_features = list(cat_encoder.get_feature_names_out(categorical_val))
            all_feat_names = cat_features + numerical_val
            importances = model_step.feature_importances_
            feat_imp_df = pd.DataFrame({"Feature": all_feat_names, "Importance": importances}).sort_values("Importance", ascending=False)
            feat_imp_df.to_csv("outputs/models/feature_importance.csv", index=False)
            print("Feature importances saved to outputs/models/feature_importance.csv")
    except Exception as e:
        print(f"Feature importance note: {e}")
        
    return results_df, test_eval_df

if __name__ == "__main__":
    train_and_evaluate_models()
