import os

from sqlalchemy.engine import make_url

ENV: str = os.getenv("ENV", "dev")


def _load_database_url() -> str:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/dossier_aggr",
    )
    if make_url(database_url).get_backend_name() != "postgresql":
        raise ValueError("DATABASE_URL must use PostgreSQL")
    return database_url


DATABASE_URL: str = _load_database_url()

DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT_SECONDS: float = float(os.getenv("DB_POOL_TIMEOUT_SECONDS", "30"))
DB_POOL_RECYCLE_SECONDS: int = int(os.getenv("DB_POOL_RECYCLE_SECONDS", "1800"))
DB_POOL_PRE_PING: bool = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
