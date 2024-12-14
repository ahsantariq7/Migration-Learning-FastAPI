import os
import subprocess


def makemigrations(description):
    """
    Run the Alembic command to autogenerate a migration.
    """
    try:
        # Define the alembic.ini path
        alembic_ini_path = os.path.join(os.getcwd(), "alembic.ini")

        # Check if the alembic.ini file exists
        if not os.path.exists(alembic_ini_path):
            raise FileNotFoundError("alembic.ini not found in the expected directory")

        # Run Alembic revision command
        subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", description], check=True
        )

        print(f"Migration '{description}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during makemigrations: {e}")
    except FileNotFoundError as e:
        print(e)


def migrate():
    """
    Run the Alembic command to apply migrations.
    """
    try:
        # Run Alembic upgrade command
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during migration: {e}")


if __name__ == "__main__":
    makemigrations("Initial migration")
    migrate()
