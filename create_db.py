import psycopg2
from psycopg2 import sql


def create_new_database(
    db_name, db_user, db_password, db_host="localhost", db_port="5432"
):
    """
    Create a new PostgreSQL database.
    """
    try:
        # Connect to PostgreSQL as the superuser to create the new database
        connection = psycopg2.connect(
            dbname="postgres",  # Connect to the default 'postgres' database
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Prepare the CREATE DATABASE SQL query
        create_db_query = sql.SQL("CREATE DATABASE {db_name}").format(
            db_name=sql.Identifier(db_name)
        )

        # Execute the SQL command to create the new database
        cursor.execute(create_db_query)
        print(f"Database '{db_name}' created successfully.")

    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{db_name}' already exists.")

    except Exception as error:
        print(f"Error while creating the database: {error}")

    finally:
        # Close the connection and cursor
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection closed.")


if __name__ == "__main__":
    # Define the new database details
    NEW_DB_NAME = "staging"
    DB_USER = "postgres"
    DB_PASSWORD = "new_password"
    DB_HOST = "localhost"  # or your DB host
    DB_PORT = "5432"  # Default PostgreSQL port

    # Call the function to create the new database
    create_new_database(NEW_DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
