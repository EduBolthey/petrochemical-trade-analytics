"""
ETL Step 4: Time-Series Train/Test Split
Preserves chronological integrity (train on past, evaluate on future)
"""

import pandas as pd
import os

def split_data(input_path="data/processed/ml_dataset.csv"):
    print("=" * 60)
    print("ETL STEP 4: TIME-SERIES TRAIN/TEST SPLIT")
    print("=" * 60)
    
    df = pd.read_csv(input_path)
    
    # Train: 2015 - 2022, Test: 2023 - 2024
    train = df[df["year"] <= 2022].copy().reset_index(drop=True)
    test = df[df["year"] >= 2023].copy().reset_index(drop=True)
    
    train.to_csv("data/processed/train_data.csv", index=False)
    test.to_csv("data/processed/test_data.csv", index=False)
    
    print(f"Training set: {len(train)} rows (Years {train['year'].min()} to {train['year'].max()})")
    print(f"Testing set: {len(test)} rows (Years {test['year'].min()} to {test['year'].max()})")
    print("Files saved to data/processed/train_data.csv and test_data.csv")
    return train, test

if __name__ == "__main__":
    split_data()
