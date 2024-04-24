import sqlite3

def clear_table_entries():
    try:
        # Connect to the database
        connection = sqlite3.connect("Kenny.db")
        cursor = connection.cursor()

        # List all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Iterate over each table and delete all records
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"All entries deleted from table: {table_name}")

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        print("All entries cleared from the database.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Call the function to clear the database entries
clear_table_entries()
