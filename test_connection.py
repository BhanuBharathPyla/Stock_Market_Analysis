from db_connection import create_connection


connection = create_connection()


if connection:
    connection.close()
    print("MySQL connection closed.")