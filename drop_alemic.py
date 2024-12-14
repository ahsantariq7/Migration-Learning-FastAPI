import psycopg2

# PostgreSQL connection details
DB_NAME = "test"
DB_USER = "postgres"
DB_PASSWORD = "new_password"
DB_HOST = "localhost"
DB_PORT = "5432"


def drop_all_alembic_versions():
    """
    Function to drop the alembic_version table from the database.
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

        # Drop the alembic_version table
        cursor.execute("DROP TABLE IF EXISTS alembic_version;")
        print("Dropped the 'alembic_version' table from the database.")

        # Commit changes
        connection.commit()

    except Exception as error:
        print(f"Error while dropping alembic_version table: {error}")

    finally:
        # Close the cursor and the connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")


if __name__ == "__main__":
    drop_all_alembic_versions()
