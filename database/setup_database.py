"""
Database Setup & Star Schema Population
Module: database/setup_database.py
Populates SQLite database 'database/petrochemical_trade.db'
Exports Power BI dimensional modeling tables to 'data/powerbi/'
"""

import sqlite3
import pandas as pd
import numpy as np
import os

def setup_database():
    print("=" * 60)
    print("SETTING UP RELATIONAL DATABASE (SQLITE / STAR SCHEMA)")
    print("=" * 60)
    
    db_path = "database/petrochemical_trade.db"
    os.makedirs("database", exist_ok=True)
    os.makedirs("data/powerbi", exist_ok=True)
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute DDL schema
    with open("database/schema.sql", "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    
    # Load cleaned dataset
    df = pd.read_csv("data/processed/cleaned_trade_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    
    # -------------------------------------------------------------
    # 1. Populate Dim_Commodity
    # -------------------------------------------------------------
    comm_df = df[["cmdCode", "commodity_name", "cmdDesc"]].drop_duplicates().reset_index(drop=True)
    comm_df["chemical_group"] = np.where(
        comm_df["commodity_name"].isin(["Ethylene", "Propylene", "Butadiene"]),
        "Olefins",
        "Aromatics"
    )
    comm_df["commodity_id"] = np.arange(1, len(comm_df) + 1)
    
    comm_df[["commodity_id", "cmdCode", "commodity_name", "cmdDesc", "chemical_group"]].to_sql(
        "Dim_Commodity", conn, if_exists="append", index=False
    )
    comm_df.to_csv("data/powerbi/Dim_Commodity.csv", index=False)
    print(f"Dim_Commodity: {len(comm_df)} records")
    
    # -------------------------------------------------------------
    # 2. Populate Dim_Country
    # -------------------------------------------------------------
    rep = df[["reporter_country", "reporter_iso", "reporter_code"]].rename(
        columns={"reporter_country": "country_name", "reporter_iso": "iso_code", "reporter_code": "country_code"}
    )
    part = df[["partner_country", "partner_iso", "partner_code"]].rename(
        columns={"partner_country": "country_name", "partner_iso": "iso_code", "partner_code": "country_code"}
    )
    country_df = pd.concat([rep, part]).drop_duplicates(subset=["country_name"]).reset_index(drop=True)
    
    # Region assignment
    region_map = {
        "China": "Asia-Pacific", "India": "South Asia", "Japan": "East Asia",
        "Rep. of Korea": "East Asia", "Singapore": "Southeast Asia", "Malaysia": "Southeast Asia",
        "Thailand": "Southeast Asia", "Taiwan": "East Asia",
        "Germany": "Europe", "Netherlands": "Europe", "Belgium": "Europe",
        "United Kingdom": "Europe", "France": "Europe", "Italy": "Europe",
        "Saudi Arabia": "Middle East", "United Arab Emirates": "Middle East",
        "USA": "North America", "Canada": "North America", "Mexico": "North America", "Brazil": "Latin America"
    }
    country_df["region"] = country_df["country_name"].map(region_map).fillna("Other")
    country_df["country_id"] = np.arange(1, len(country_df) + 1)
    
    country_df[["country_id", "country_name", "iso_code", "country_code", "region"]].to_sql(
        "Dim_Country", conn, if_exists="append", index=False
    )
    country_df.to_csv("data/powerbi/Dim_Country.csv", index=False)
    print(f"Dim_Country: {len(country_df)} records")
    
    # -------------------------------------------------------------
    # 3. Populate Dim_Date
    # -------------------------------------------------------------
    dates = pd.date_range(start="2015-01-01", end="2024-12-01", freq="MS")
    date_df = pd.DataFrame({"full_date": dates})
    date_df["year"] = date_df["full_date"].dt.year
    date_df["month"] = date_df["full_date"].dt.month
    date_df["quarter"] = date_df["full_date"].dt.quarter
    date_df["month_name"] = date_df["full_date"].dt.strftime("%B")
    date_df["date_id"] = np.arange(1, len(date_df) + 1)
    date_df["full_date"] = date_df["full_date"].dt.strftime("%Y-%m-%d")
    
    date_df[["date_id", "full_date", "year", "month", "quarter", "month_name"]].to_sql(
        "Dim_Date", conn, if_exists="append", index=False
    )
    date_df.to_csv("data/powerbi/Dim_Date.csv", index=False)
    print(f"Dim_Date: {len(date_df)} records")
    
    # -------------------------------------------------------------
    # 4. Populate Fact_TradeTransactions
    # -------------------------------------------------------------
    # Map foreign keys
    df["full_date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    df = df.merge(date_df[["full_date", "date_id"]], left_on="full_date_str", right_on="full_date", how="left")
    df = df.merge(comm_df[["cmdCode", "commodity_id"]], on="cmdCode", how="left")
    df = df.merge(country_df[["country_name", "country_id"]].rename(columns={"country_id": "reporter_country_id"}),
                  left_on="reporter_country", right_on="country_name", how="left")
    df = df.merge(country_df[["country_name", "country_id"]].rename(columns={"country_id": "partner_country_id"}),
                  left_on="partner_country", right_on="country_name", how="left")
    
    fact_cols = [
        "transaction_id", "date_id", "commodity_id",
        "reporter_country_id", "partner_country_id", "trade_flow",
        "trade_volume_mt", "trade_value_usd", "trade_unit_value_usd_mt",
        "is_price_outlier", "is_reported"
    ]
    fact_df = df[fact_cols].copy()
    fact_df.to_sql("Fact_TradeTransactions", conn, if_exists="append", index=False)
    fact_df.to_csv("data/powerbi/Fact_TradeData.csv", index=False)
    print(f"Fact_TradeTransactions: {len(fact_df)} records")
    
    # Create analytical view
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS View_TradeAnalytics AS
    SELECT 
        f.transaction_id,
        d.full_date,
        d.year,
        d.month_name,
        c.commodity_name,
        c.chemical_group,
        rep.country_name AS reporter_country,
        rep.region AS reporter_region,
        part.country_name AS partner_country,
        part.region AS partner_region,
        f.trade_flow,
        f.trade_volume_mt,
        f.trade_value_usd,
        f.trade_unit_value_usd_mt
    FROM Fact_TradeTransactions f
    JOIN Dim_Date d ON f.date_id = d.date_id
    JOIN Dim_Commodity c ON f.commodity_id = c.commodity_id
    JOIN Dim_Country rep ON f.reporter_country_id = rep.country_id
    JOIN Dim_Country part ON f.partner_country_id = part.country_id;
    """)
    
    conn.commit()
    conn.close()
    print("Database setup complete: database/petrochemical_trade.db")
    print("Power BI star-schema tables saved to: data/powerbi/")

if __name__ == "__main__":
    setup_database()
