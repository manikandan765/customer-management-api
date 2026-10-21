import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

from src.database import Base
from src.models import Customer

load_dotenv()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Safely escape '%' for configparser, while keeping it valid for SQLAlchemy
db_url = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", db_url.replace('%', '%%'))

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    pass
else:
    run_migrations_online()
