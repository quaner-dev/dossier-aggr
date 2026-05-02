import os


def _optional_int_env(name: str) -> int | None:
    value = os.getenv(name)
    return int(value) if value else None


def _optional_float_env(name: str) -> float | None:
    value = os.getenv(name)
    return float(value) if value else None


def _optional_bool_env(name: str) -> bool | None:
    value = os.getenv(name)
    if not value:
        return None
    return value.lower() in {"1", "true", "yes", "on"}


ENV: str = os.getenv("ENV", "dev")

RABBITMQ_USERNAME: str = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_IP: str = os.getenv("RABBITMQ_IP", "localhost")
RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", "5672")

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")
TASKIQ_RESULT_BACKEND_URL: str = os.getenv("TASKIQ_RESULT_BACKEND_URL", "")
TASK_RESULT_TIMEOUT_SECONDS: float = float(os.getenv("TASK_RESULT_TIMEOUT_SECONDS", "10"))
DB_POOL_SIZE: int | None = _optional_int_env("DB_POOL_SIZE")
DB_MAX_OVERFLOW: int | None = _optional_int_env("DB_MAX_OVERFLOW")
DB_POOL_TIMEOUT_SECONDS: float | None = _optional_float_env("DB_POOL_TIMEOUT_SECONDS")
DB_POOL_RECYCLE_SECONDS: int | None = _optional_int_env("DB_POOL_RECYCLE_SECONDS")
DB_POOL_PRE_PING: bool | None = _optional_bool_env("DB_POOL_PRE_PING")
# DATABASE_URL: str = os.getenv(
#     "DATABASE_URL",
#     "postgresql+asyncpg://postgres:OKuzbIJowf@127.0.0.1:5432/postgres",
# )
