USE stock_analysis;

-- ============================================
-- STOCK ANALYSIS - SQL ANALYTICS
-- ============================================

-- 1. Total number of records
SELECT COUNT(*) AS total_rows
FROM stocks;


-- 2. Average closing price by stock
SELECT
    symbol,
    ROUND(AVG(close_price), 2) AS average_close_price
FROM stocks
GROUP BY symbol
ORDER BY average_close_price DESC;


-- 3. Highest and lowest closing price
SELECT
    symbol,
    ROUND(MAX(close_price), 2) AS highest_close_price,
    ROUND(MIN(close_price), 2) AS lowest_close_price
FROM stocks
GROUP BY symbol
ORDER BY highest_close_price DESC;


-- 4. Average daily return
SELECT
    symbol,
    ROUND(AVG(daily_return) * 100, 4)
        AS average_daily_return_percent
FROM stocks
GROUP BY symbol
ORDER BY average_daily_return_percent DESC;


-- 5. Total trading volume
SELECT
    symbol,
    SUM(volume) AS total_volume
FROM stocks
GROUP BY symbol
ORDER BY total_volume DESC;


-- 6. UP / DOWN / NO_CHANGE trend analysis
SELECT
    symbol,
    trend,
    COUNT(*) AS number_of_days
FROM stocks
GROUP BY symbol, trend
ORDER BY symbol, number_of_days DESC;


-- 7. Trend percentage using window function
SELECT
    symbol,
    trend,
    COUNT(*) AS number_of_days,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (PARTITION BY symbol),
        2
    ) AS percentage
FROM stocks
GROUP BY symbol, trend
ORDER BY symbol, percentage DESC;


-- 8. Stock ranking using RANK()
SELECT
    symbol,
    ROUND(AVG(daily_return) * 100, 4)
        AS average_daily_return_percent,
    RANK() OVER (
        ORDER BY AVG(daily_return) DESC
    ) AS stock_rank
FROM stocks
GROUP BY symbol
ORDER BY stock_rank;


-- 9. Volatility
SELECT
    symbol,
    ROUND(STDDEV(daily_return) * 100, 2)
        AS volatility_percent
FROM stocks
GROUP BY symbol
ORDER BY volatility_percent DESC;


-- 10. Complete stock performance summary
SELECT
    symbol,
    COUNT(*) AS total_days,
    ROUND(AVG(close_price), 2) AS avg_close_price,
    ROUND(MAX(close_price), 2) AS highest_close_price,
    ROUND(MIN(close_price), 2) AS lowest_close_price,
    ROUND(AVG(daily_return) * 100, 2)
        AS avg_daily_return_percent,
    ROUND(STDDEV(daily_return) * 100, 2)
        AS volatility_percent,

    SUM(
        CASE
            WHEN trend = 'UP' THEN 1
            ELSE 0
        END
    ) AS up_days,

    SUM(
        CASE
            WHEN trend = 'DOWN' THEN 1
            ELSE 0
        END
    ) AS down_days,

    SUM(
        CASE
            WHEN trend = 'NO_CHANGE' THEN 1
            ELSE 0
        END
    ) AS no_change_days,

    SUM(volume) AS total_volume

FROM stocks
GROUP BY symbol
ORDER BY avg_daily_return_percent DESC;