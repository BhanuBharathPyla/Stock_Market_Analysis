import pandas as pd


# File paths
files = {
    "AAPL": "data/raw/aapl_stock_prices.csv",
    "GOOG": "data/raw/goog_stock_prices.csv",
    "MSFT": "data/raw/msft_stock_prices.csv"
}


# Read and inspect each stock file
for stock, file in files.items():

    print("=" * 60)
    print(f"{stock} STOCK DATA")
    print("=" * 60)

    df = pd.read_csv(file)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nNumber of rows and columns:")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\n" + "=" * 60)