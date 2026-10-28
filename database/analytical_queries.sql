-- ====================================================================
-- ADVANCED SQL ANALYTICAL QUERIES FOR PETROCHEMICAL TRADE INTELLIGENCE
-- Demonstrates: CTEs, Window Functions, Aggregate Joins, Moving Averages
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: EXECUTIVE TRADE BALANCE BY COUNTRY (SURPLUS VS DEFICIT)
-- Computes Total Exports, Total Imports, Net Trade Balance, and Export/Import Coverage Ratio
-- --------------------------------------------------------------------
SELECT 
    rep.country_name,
    rep.region,
    ROUND(SUM(CASE WHEN f.trade_flow = 'Export' THEN f.trade_value_usd ELSE 0 END) / 1e9, 2) AS Total_Export_USD_Billions,
    ROUND(SUM(CASE WHEN f.trade_flow = 'Import' THEN f.trade_value_usd ELSE 0 END) / 1e9, 2) AS Total_Import_USD_Billions,
    ROUND((SUM(CASE WHEN f.trade_flow = 'Export' THEN f.trade_value_usd ELSE 0 END) - 
           SUM(CASE WHEN f.trade_flow = 'Import' THEN f.trade_value_usd ELSE 0 END)) / 1e9, 2) AS Net_Trade_Balance_Billions,
    ROUND(SUM(CASE WHEN f.trade_flow = 'Export' THEN f.trade_value_usd ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN f.trade_flow = 'Import' THEN f.trade_value_usd ELSE 0 END), 0), 2) AS Coverage_Ratio
FROM Fact_TradeTransactions f
JOIN Dim_Country rep ON f.reporter_country_id = rep.country_id
GROUP BY rep.country_name, rep.region
ORDER BY Net_Trade_Balance_Billions DESC;


-- --------------------------------------------------------------------
-- QUERY 2: WINDOW FUNCTION - YEAR-OVER-YEAR (YoY) GROWTH RATE BY COMMODITY
-- Uses LAG() window function partitioned by commodity_name over annual calendar
-- --------------------------------------------------------------------
WITH YearlyCommodityTrade AS (
    SELECT 
        d.year,
        c.commodity_name,
        SUM(f.trade_value_usd) AS annual_trade_value
    FROM Fact_TradeTransactions f
    JOIN Dim_Date d ON f.date_id = d.date_id
    JOIN Dim_Commodity c ON f.commodity_id = c.commodity_id
    GROUP BY d.year, c.commodity_name
)
SELECT 
    year,
    commodity_name,
    ROUND(annual_trade_value / 1e9, 2) AS Trade_Value_Billions,
    ROUND(LAG(annual_trade_value, 1) OVER (PARTITION BY commodity_name ORDER BY year) / 1e9, 2) AS Prev_Year_Value_Billions,
    ROUND(((annual_trade_value - LAG(annual_trade_value, 1) OVER (PARTITION BY commodity_name ORDER BY year)) / 
           NULLIF(LAG(annual_trade_value, 1) OVER (PARTITION BY commodity_name ORDER BY year), 0)) * 100, 2) AS YoY_Growth_Pct
FROM YearlyCommodityTrade
ORDER BY commodity_name, year;


-- --------------------------------------------------------------------
-- QUERY 3: WINDOW FUNCTION - RANKING TOP 3 EXPORT COMMODITIES PER YEAR
-- Uses DENSE_RANK() OVER (PARTITION BY year ORDER BY export_value DESC)
-- --------------------------------------------------------------------
WITH AnnualProductExports AS (
    SELECT 
        d.year,
        c.commodity_name,
        ROUND(SUM(f.trade_value_usd) / 1e9, 2) AS Export_Value_Billions,
        DENSE_RANK() OVER (PARTITION BY d.year ORDER BY SUM(f.trade_value_usd) DESC) AS Export_Rank
    FROM Fact_TradeTransactions f
    JOIN Dim_Date d ON f.date_id = d.date_id
    JOIN Dim_Commodity c ON f.commodity_id = c.commodity_id
    WHERE f.trade_flow = 'Export'
    GROUP BY d.year, c.commodity_name
)
SELECT year, Export_Rank, commodity_name, Export_Value_Billions
FROM AnnualProductExports
WHERE Export_Rank <= 3
ORDER BY year, Export_Rank;


-- --------------------------------------------------------------------
-- QUERY 4: ROLLING 3-YEAR CUMULATIVE EXPORT VOLUME USING UNBOUNDED PRECEDING
-- Demonstrates running analytical window totals
-- --------------------------------------------------------------------
SELECT 
    d.year,
    c.commodity_name,
    ROUND(SUM(f.trade_volume_mt) / 1e6, 2) AS Annual_Volume_Mt,
    ROUND(SUM(SUM(f.trade_volume_mt)) OVER (
        PARTITION BY c.commodity_name 
        ORDER BY d.year 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) / 1e6, 2) AS Rolling_3Yr_Cumulative_Mt
FROM Fact_TradeTransactions f
JOIN Dim_Date d ON f.date_id = d.date_id
JOIN Dim_Commodity c ON f.commodity_id = c.commodity_id
WHERE f.trade_flow = 'Export' AND f.trade_volume_mt IS NOT NULL
GROUP BY d.year, c.commodity_name
ORDER BY c.commodity_name, d.year;


-- --------------------------------------------------------------------
-- QUERY 5: BILATERAL CORRIDOR ANALYSIS (TOP 10 CROSS-BORDER FLOWS)
-- Identifies top global supply chain trading corridors
-- --------------------------------------------------------------------
SELECT 
    rep.country_name AS Exporter,
    part.country_name AS Destination,
    c.commodity_name,
    COUNT(f.transaction_id) AS Shipments,
    ROUND(SUM(f.trade_volume_mt) / 1e6, 2) AS Total_Volume_Mt,
    ROUND(SUM(f.trade_value_usd) / 1e9, 2) AS Total_Value_USD_Billions,
    ROUND(SUM(f.trade_value_usd) / NULLIF(SUM(f.trade_volume_mt), 0), 2) AS Weighted_Avg_Price_USD_MT
FROM Fact_TradeTransactions f
JOIN Dim_Country rep ON f.reporter_country_id = rep.country_id
JOIN Dim_Country part ON f.partner_country_id = part.country_id
JOIN Dim_Commodity c ON f.commodity_id = c.commodity_id
WHERE f.trade_flow = 'Export'
GROUP BY rep.country_name, part.country_name, c.commodity_name
ORDER BY Total_Value_USD_Billions DESC
LIMIT 10;
