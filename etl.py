import pandas as pd
import logging
import os


# ---------------------------------------------------------
# 1. Create logs folder
# ---------------------------------------------------------

os.makedirs("logs", exist_ok=True)


# ---------------------------------------------------------
# 2. Configure logging
# ---------------------------------------------------------

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL process started")


# ---------------------------------------------------------
# 3. Input files
# ---------------------------------------------------------

files = {
    "AAPL": "data/raw/aapl_stock_prices.csv",
    "GOOG": "data/raw/goog_stock_prices.csv",
    "MSFT": "data/raw/msft_stock_prices.csv"
}


# ---------------------------------------------------------
# 4. Read CSV files
# ---------------------------------------------------------

dataframes = []

for stock, file in files.items():

    try:
        df = pd.read_csv(file)

        logging.info(
            f"{stock} file loaded successfully. Rows: {len(df)}"
        )

        dataframes.append(df)

    except FileNotFoundError:
        logging.error(f"File not found: {file}")
        print(f"ERROR: File not found: {file}")

    except Exception as e:
        logging.error(f"Error reading {file}: {e}")
        print(f"ERROR reading {file}: {e}")


# ---------------------------------------------------------
# 5. Combine all stock data
# ---------------------------------------------------------

df = pd.concat(
    dataframes,
    ignore_index=True
)

print("\nTotal rows before cleaning:", len(df))

logging.info(
    f"Total rows before cleaning: {len(df)}"
)


# ---------------------------------------------------------
# 6. Convert date to datetime
# ---------------------------------------------------------

df["date"] = pd.to_datetime(df["date"])

logging.info("Date column converted to datetime")


# ---------------------------------------------------------
# 7. Remove duplicate rows
# ---------------------------------------------------------

duplicates_before = df.duplicated().sum()

df = df.drop_duplicates()

duplicates_after = df.duplicated().sum()

print("Duplicates removed:", duplicates_before)

logging.info(
    f"Duplicates removed: {duplicates_before}"
)

logging.info(
    f"Duplicates remaining: {duplicates_after}"
)


# ---------------------------------------------------------
# 8. Handle missing close_price
# ---------------------------------------------------------
# Business Rule:
# Replace missing close_price with median close_price
# for the respective stock.
# ---------------------------------------------------------

missing_close_before = df["close_price"].isnull().sum()

df["close_price"] = (
    df.groupby("symbol")["close_price"]
    .transform(
        lambda x: x.fillna(x.median())
    )
)

missing_close_after = df["close_price"].isnull().sum()

print(
    "Missing close_price before:",
    missing_close_before
)

print(
    "Missing close_price after:",
    missing_close_after
)

logging.info(
    f"Missing close_price before: {missing_close_before}"
)

logging.info(
    f"Missing close_price after: {missing_close_after}"
)


# ---------------------------------------------------------
# 9. Handle missing volume
# ---------------------------------------------------------
# Business Rule:
# Replace missing volume with 0.
# ---------------------------------------------------------

missing_volume_before = df["volume"].isnull().sum()

df["volume"] = df["volume"].fillna(0)

missing_volume_after = df["volume"].isnull().sum()

print(
    "Missing volume before:",
    missing_volume_before
)

print(
    "Missing volume after:",
    missing_volume_after
)

logging.info(
    f"Missing volume before: {missing_volume_before}"
)

logging.info(
    f"Missing volume after: {missing_volume_after}"
)


# ---------------------------------------------------------
# 10. Validate and correct high_price
# ---------------------------------------------------------
# Rule:
# high_price must be >= open_price
# high_price must be >= close_price
# ---------------------------------------------------------

required_high = df[
    ["open_price", "close_price"]
].max(axis=1)

invalid_high_before = (
    (df["high_price"] < df["open_price"]) |
    (df["high_price"] < df["close_price"])
).sum()

df["high_price"] = pd.concat(
    [
        df["high_price"],
        required_high
    ],
    axis=1
).max(axis=1)

invalid_high_after = (
    (df["high_price"] < df["open_price"]) |
    (df["high_price"] < df["close_price"])
).sum()

print(
    "Invalid high_price before:",
    invalid_high_before
)

print(
    "Invalid high_price after:",
    invalid_high_after
)

logging.info(
    f"Invalid high_price before: {invalid_high_before}"
)

logging.info(
    f"Invalid high_price after: {invalid_high_after}"
)


# ---------------------------------------------------------
# 11. Validate and correct low_price
# ---------------------------------------------------------
# Rule:
# low_price must be <= open_price
# low_price must be <= close_price
# ---------------------------------------------------------

required_low = df[
    ["open_price", "close_price"]
].min(axis=1)

invalid_low_before = (
    (df["low_price"] > df["open_price"]) |
    (df["low_price"] > df["close_price"])
).sum()

df["low_price"] = pd.concat(
    [
        df["low_price"],
        required_low
    ],
    axis=1
).min(axis=1)

invalid_low_after = (
    (df["low_price"] > df["open_price"]) |
    (df["low_price"] > df["close_price"])
).sum()

print(
    "Invalid low_price before:",
    invalid_low_before
)

print(
    "Invalid low_price after:",
    invalid_low_after
)

logging.info(
    f"Invalid low_price before: {invalid_low_before}"
)

logging.info(
    f"Invalid low_price after: {invalid_low_after}"
)


# ---------------------------------------------------------
# 12. Calculate daily return
# ---------------------------------------------------------

df["daily_return"] = (
    (df["close_price"] - df["open_price"])
    / df["open_price"]
)

logging.info("Daily return calculated")


# ---------------------------------------------------------
# 13. Classify trend
# ---------------------------------------------------------

df["trend"] = df["daily_return"].apply(
    lambda x:
        "UP"
        if x > 0
        else "DOWN"
        if x < 0
        else "NO_CHANGE"
)

logging.info("Trend classification completed")


# ---------------------------------------------------------
# 14. Final validation
# ---------------------------------------------------------

print("\n========== FINAL VALIDATION ==========")

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nDuplicate rows:",
    df.duplicated().sum()
)

print(
    "Invalid high_price:",
    (
        (df["high_price"] < df["open_price"]) |
        (df["high_price"] < df["close_price"])
    ).sum()
)

print(
    "Invalid low_price:",
    (
        (df["low_price"] > df["open_price"]) |
        (df["low_price"] > df["close_price"])
    ).sum()
)

print("\nTrend distribution:")
print(df["trend"].value_counts())


# ---------------------------------------------------------
# 15. Save cleaned data
# ---------------------------------------------------------

os.makedirs(
    "data/processed",
    exist_ok=True
)

output_file = "data/processed/cleaned_stock_data.csv"

df.to_csv(
    output_file,
    index=False
)

logging.info(
    f"Cleaned data saved to {output_file}"
)

logging.info("ETL process completed successfully")


print(
    f"\nCleaned data saved to: {output_file}"
)

print(
    "\nTotal clean rows:",
    len(df)
)

print("\nETL process completed successfully!")