import os


ENV: str = os.getenv("ENV", "dev")

RABBITMQ_USERNAME: str = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_IP: str = os.getenv("RABBITMQ_IP", "localhost")
RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", "5672")

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")
TASKIQ_RESULT_BACKEND_URL: str = os.getenv("TASKIQ_RESULT_BACKEND_URL", "")
TASK_RESULT_TIMEOUT_SECONDS: float = float(os.getenv("TASK_RESULT_TIMEOUT_SECONDS", "10"))

DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT_SECONDS: float = float(os.getenv("DB_POOL_TIMEOUT_SECONDS", "30"))
DB_POOL_RECYCLE_SECONDS: int = int(os.getenv("DB_POOL_RECYCLE_SECONDS", "1800"))
DB_POOL_PRE_PING: bool = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
# DATABASE_URL: str = os.getenv(
#     "DATABASE_URL",
#     "postgresql+asyncpg://postgres:OKuzbIJowf@127.0.0.1:5432/postgres",
# )
