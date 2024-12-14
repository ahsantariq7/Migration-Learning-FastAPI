import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command


class DBManager:
    def __init__(self, env_file=".env_vars/.env.production"):
        # Load environment variables from the provided .env file
        load_dotenv(env_file)

        # Fetch database configuration from environment variables
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT", "5432")  # Default to 5432 if not set
        self.db_name = os.getenv("DB_NAME")

        # Construct the database URL for async
        self.db_url = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

        # Initialize SQLAlchemy async engine and session factory
        self.engine = create_async_engine(self.db_url, echo=True)
        self.Session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_session(self):
        """Provide an asynchronous SQLAlchemy session for interacting with the database."""
        async with self.Session() as session:
            yield session

    async def close(self):
        """Dispose of the engine when done (cleanup)."""
        await self.engine.dispose()

    async def run_migrations(self, alembic_cfg):
        """Run Alembic migrations."""
        script_path = os.getenv("SCRIPT_PATH")
        if not script_path:
            raise ValueError("SCRIPT_PATH is not set in environment variables!")

        alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
        alembic_cfg.set_main_option("script_location", script_path)

        # Run Alembic upgrade (to the latest migration)
        command.upgrade(alembic_cfg, "head")

    async def make_migrations(self, alembic_cfg, message="Autogenerated migration"):
        """Generate a new Alembic migration (similar to 'makemigrations')."""
        try:
            script_path = os.getenv("SCRIPT_PATH")
            if not script_path:
                raise ValueError("SCRIPT_PATH is not set in environment variables!")

            alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
            alembic_cfg.set_main_option("script_location", script_path)

            # Generate a new migration script with autogenerate
            command.revision(alembic_cfg, autogenerate=True, message=message)

            print("Migration created successfully.")
        except Exception as e:
            print(f"Error during makemigrations: {e}")

    async def migrate(self, alembic_cfg):
        """Apply Alembic migrations to the latest version (similar to 'migrate')."""
        try:
            script_path = os.getenv("SCRIPT_PATH")
            alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
            alembic_cfg.set_main_option("script_location", script_path)

            # Run Alembic upgrade command
            command.upgrade(alembic_cfg, "head")
            print("Database migrated successfully.")
        except Exception as e:
            print(f"Error during migration: {e}")


# Example usage
async def main():
    import sys

    # Load environment variables from the command line argument if provided
    if len(sys.argv) > 1:
        env_file = sys.argv[1]
    else:
        env_file = ".env_vars/.env.production"  # Default to production file

    db_manager = DBManager(env_file)

    alembic_cfg = Config("alembic.ini")

    if len(sys.argv) > 2 and sys.argv[2] == "makemigrations":
        await db_manager.make_migrations(alembic_cfg, message="Schema update")
    else:
        await db_manager.migrate(alembic_cfg)

    print(f"Using database URL: {db_manager.db_url}")
    print(f"Script Path: {os.getenv('SCRIPT_PATH')}")

    await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
