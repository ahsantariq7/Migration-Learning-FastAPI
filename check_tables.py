import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
DB_NAME = "test"
DB_USER = "postgres"
DB_PASSWORD = "new_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# List of required tables
required_tables = ["users", "items", "orders", "order_items"]


def check_database():
    """
    Function to check if the database and tables exist.
    """
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = connection.cursor()

        # Check if the connection is successful
        print(f"Connected to the database '{DB_NAME}' successfully.")

        # Check if the required tables exist
        cursor.execute(
            """
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """
        )
        tables = cursor.fetchall()

        # Flatten the result and get the list of table names
        tables_in_db = [table[0] for table in tables]
        print(tables_in_db)

        # Check if the required tables are present
        for table in required_tables:
            if table in tables_in_db:
                print(f"Table '{table}' exists.")
            else:
                print(f"Table '{table}' does NOT exist.")

    except Exception as error:
        print(f"Error while checking database: {error}")

    finally:
        # Close the cursor and the connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")


if __name__ == "__main__":
    check_database()
