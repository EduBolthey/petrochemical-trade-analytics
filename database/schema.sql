-- ====================================================================
-- DATABASE SCHEMA: PETROCHEMICAL TRADE ANALYTICS (STAR SCHEMA)
-- Compatible with SQLite, PostgreSQL, and MySQL
-- ====================================================================

-- 1. DIMENSION TABLE: COMMODITY (HS6 CLASSIFICATION)
CREATE TABLE IF NOT EXISTS Dim_Commodity (
    commodity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cmdCode INTEGER UNIQUE NOT NULL,
    commodity_name TEXT NOT NULL,
    cmdDesc TEXT NOT NULL,
    chemical_group TEXT NOT NULL -- Olefin vs Aromatic
);

-- 2. DIMENSION TABLE: COUNTRY (GEOGRAPHICAL & ECONOMIC METRICS)
CREATE TABLE IF NOT EXISTS Dim_Country (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT UNIQUE NOT NULL,
    iso_code TEXT NOT NULL,
    country_code INTEGER NOT NULL,
    region TEXT NOT NULL
);

-- 3. DIMENSION TABLE: DATE (TIME CALENDAR)
CREATE TABLE IF NOT EXISTS Dim_Date (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month_name TEXT NOT NULL
);

-- 4. FACT TABLE: TRADE TRANSACTIONS
CREATE TABLE IF NOT EXISTS Fact_TradeTransactions (
    transaction_id INTEGER PRIMARY KEY,
    date_id INTEGER NOT NULL,
    commodity_id INTEGER NOT NULL,
    reporter_country_id INTEGER NOT NULL,
    partner_country_id INTEGER NOT NULL,
    trade_flow TEXT NOT NULL, -- 'Import' or 'Export'
    trade_volume_mt REAL,
    trade_value_usd REAL NOT NULL,
    trade_unit_value_usd_mt REAL,
    is_price_outlier INTEGER DEFAULT 0,
    is_reported INTEGER DEFAULT 1,
    FOREIGN KEY (date_id) REFERENCES Dim_Date(date_id),
    FOREIGN KEY (commodity_id) REFERENCES Dim_Commodity(commodity_id),
    FOREIGN KEY (reporter_country_id) REFERENCES Dim_Country(country_id),
    FOREIGN KEY (partner_country_id) REFERENCES Dim_Country(country_id)
);

-- INDEXES FOR FAST QUERYING & ANALYTICS
CREATE INDEX IF NOT EXISTS idx_fact_date ON Fact_TradeTransactions(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_commodity ON Fact_TradeTransactions(commodity_id);
CREATE INDEX IF NOT EXISTS idx_fact_reporter ON Fact_TradeTransactions(reporter_country_id);
CREATE INDEX IF NOT EXISTS idx_fact_flow ON Fact_TradeTransactions(trade_flow);
