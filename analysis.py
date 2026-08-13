import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# 1. CONNECT TO MYSQL
# ============================================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stock_analysis"
)

print("MySQL connection successful!")


# ============================================================
# 2. CREATE OUTPUT FOLDER
# ============================================================

output_folder = "visualizations"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("Visualization folder ready!")


# ============================================================
# 3. FETCH STOCK SUMMARY FROM MYSQL
# ============================================================

query = """
SELECT
    symbol,
    COUNT(*) AS total_days,
    ROUND(AVG(close_price), 2) AS avg_close_price,
    ROUND(MAX(close_price), 2) AS highest_close_price,
    ROUND(MIN(close_price), 2) AS lowest_close_price,
    ROUND(AVG(daily_return) * 100, 2) AS avg_daily_return_percent,
    ROUND(STDDEV(daily_return) * 100, 2) AS volatility_percent,

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
"""


df = pd.read_sql(query, connection)

print("\n========== STOCK SUMMARY ==========")
print(df)


# ============================================================
# 4. SAVE SUMMARY AS CSV
# ============================================================

df.to_csv(
    "visualizations/stock_summary.csv",
    index=False
)

print("\nStock summary saved successfully!")


# ============================================================
# 5. AVERAGE CLOSING PRICE CHART
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["symbol"],
    df["avg_close_price"]
)

plt.title("Average Closing Price by Stock")
plt.xlabel("Stock")
plt.ylabel("Average Closing Price")

plt.tight_layout()

plt.savefig(
    "visualizations/average_closing_price.png"
)



# ============================================================
# 6. AVERAGE DAILY RETURN CHART
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["symbol"],
    df["avg_daily_return_percent"]
)

plt.title("Average Daily Return by Stock")
plt.xlabel("Stock")
plt.ylabel("Average Daily Return (%)")

plt.tight_layout()

plt.savefig(
    "visualizations/average_daily_return.png"
)

plt.show()


# ============================================================
# 7. VOLATILITY CHART
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["symbol"],
    df["volatility_percent"]
)

plt.title("Stock Volatility Comparison")
plt.xlabel("Stock")
plt.ylabel("Volatility (%)")

plt.tight_layout()

plt.savefig(
    "visualizations/volatility.png"
)

plt.show()


# ============================================================
# 8. UP VS DOWN DAYS
# ============================================================

plt.figure(figsize=(8, 5))

x = range(len(df))

plt.bar(
    x,
    df["up_days"],
    width=0.4,
    label="UP Days"
)

plt.bar(
    [i + 0.4 for i in x],
    df["down_days"],
    width=0.4,
    label="DOWN Days"
)

plt.xticks(
    [i + 0.2 for i in x],
    df["symbol"]
)

plt.title("UP vs DOWN Trading Days")
plt.xlabel("Stock")
plt.ylabel("Number of Days")

plt.legend()

plt.tight_layout()

plt.savefig(
    "visualizations/up_vs_down_days.png"
)

plt.show()


# ============================================================
# 9. TOTAL TRADING VOLUME
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["symbol"],
    df["total_volume"]
)

plt.title("Total Trading Volume by Stock")
plt.xlabel("Stock")
plt.ylabel("Total Volume")

plt.tight_layout()

plt.savefig(
    "visualizations/total_trading_volume.png"
)

plt.show()


# ============================================================
# 10. CLOSE MYSQL CONNECTION
# ============================================================

connection.close()

print("\nMySQL connection closed.")
print("All visualizations created successfully!")

# ============================================================
# 11. BEST PERFORMING STOCK
# ============================================================

best_stock = df.loc[df["avg_daily_return_percent"].idxmax()]

print("\n========== BEST PERFORMING STOCK ==========")
print("Stock:", best_stock["symbol"])
print("Average Daily Return:", best_stock["avg_daily_return_percent"], "%")
print("Average Closing Price:", best_stock["avg_close_price"])

# ============================================================
# 12. HIGHEST CLOSING PRICE BY STOCK
# ============================================================

highest_close = df.groupby("symbol")["highest_close_price"].max()

plt.figure(figsize=(8, 5))
highest_close.plot(kind="bar")

plt.title("Highest Closing Price by Stock")
plt.xlabel("Stock")
plt.ylabel("Highest Closing Price")
plt.tight_layout()

plt.savefig("visualizations/highest_closing_price.png")
plt.show()