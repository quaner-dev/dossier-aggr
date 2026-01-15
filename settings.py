import os

ENV: str = os.getenv("ENV", "dev")

RABBITMQ_USERNAME: str = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_IP: str = os.getenv("RABBITMQ_IP", "localhost")
RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", "5672")

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")
# DATABASE_URL: str = os.getenv(
#     "DATABASE_URL",
#     "postgresql+asyncpg://postgres:OKuzbIJowf@127.0.0.1:5432/postgres",
# )
