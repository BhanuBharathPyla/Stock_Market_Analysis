import pandas as pd
from db_connection import create_connection


# ---------------------------------------------------------
# 1. Read cleaned CSV
# ---------------------------------------------------------

file_path = "data/processed/cleaned_stock_data.csv"

df = pd.read_csv(file_path)

print("Cleaned CSV loaded successfully!")
print("Total rows in CSV:", len(df))


# ---------------------------------------------------------
# 2. Create MySQL connection
# ---------------------------------------------------------

connection = create_connection()


if connection:

    cursor = connection.cursor()

    # -----------------------------------------------------
    # 3. Insert data into stocks table
    # -----------------------------------------------------

    insert_query = """
        INSERT INTO stocks
        (
            date,
            symbol,
            open_price,
            close_price,
            high_price,
            low_price,
            volume,
            daily_return,
            trend
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            row["date"],
            row["symbol"],
            row["open_price"],
            row["close_price"],
            row["high_price"],
            row["low_price"],
            row["volume"],
            row["daily_return"],
            row["trend"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(insert_query, data)

    connection.commit()

    print("Data inserted successfully!")
    print("Rows inserted:", cursor.rowcount)

    # -----------------------------------------------------
    # 4. Close connection
    # -----------------------------------------------------

    cursor.close()
    connection.close()

    print("MySQL connection closed.")

else:

    print("MySQL connection failed.")