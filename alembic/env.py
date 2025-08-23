import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Import your models' Base
from src.db.models import Base
from src.core.config import DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URL from your application's config
if DATABASE_URL:
    config.set_main_option('sqlalchemy.url', DATABASE_URL)
else:
    raise ValueError("DATABASE_URL is not set, please check your .env file or environment variables.")


# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def do_run_migrations(connection):
    """Helper function to run migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Create an async engine
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True
    )

    # Connect and run migrations
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Dispose the engine
    await connectable.dispose()


# Alembic can be run in two modes: 'offline' and 'online'.
# We are only implementing the 'online' mode for simplicity and because it's the most common case.
if context.is_offline_mode():
    raise NotImplementedError("Offline mode is not supported in this configuration.")
else:
    asyncio.run(run_migrations_online())
