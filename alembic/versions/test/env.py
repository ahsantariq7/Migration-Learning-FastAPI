from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models import Base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env_vars/.env.development")

# Alembic Config object, which provides access to the .ini file
config = context.config

# Retrieve the database URL and script path from environment variables
db_user = os.getenv("DB_USER")
print(db_user)
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
script_path = os.getenv("SCRIPT_PATH")

# Construct the database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Update the alembic configuration with the database URL and script path
config.set_main_option("sqlalchemy.url", db_url)

# Dynamically set the script location if defined in .env
if script_path:
    config.set_main_option("script_location", script_path)

# Interpret the config file for logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your models' metadata for autogenerate support
# This points to the MetaData of your SQLAlchemy models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Choose whether to run migrations offline or online based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
