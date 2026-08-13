import mysql.connector


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="stock_analysis"
        )

        if connection.is_connected():
            print("MySQL connection successful!")

        return connection

    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None