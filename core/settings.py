"""应用全局配置，统一从环境变量读取。"""

import os
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

from sqlalchemy import URL

ENV: str = os.getenv("ENV", "dev")
TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Shanghai")
CHINA_TZ = ZoneInfo(TIMEZONE)

DB_HOST: str = os.environ["DB_HOST"]
DB_PORT: int = int(os.environ["DB_PORT"])
DB_USER: str = os.environ["DB_USER"]
DB_PASSWORD: str = os.environ["DB_PASSWORD"]
DB_NAME: str = os.environ["DB_NAME"]

DB_ASYNC_URL: str = URL.create(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
).render_as_string(hide_password=False)

DB_SYNC_URL: str = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
).render_as_string(hide_password=False)

DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT_SECONDS: float = float(os.getenv("DB_POOL_TIMEOUT_SECONDS", "30"))
DB_POOL_RECYCLE_SECONDS: int = int(os.getenv("DB_POOL_RECYCLE_SECONDS", "1800"))
DB_POOL_PRE_PING: bool = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"

# Kafka and object-storage settings are application-wide configuration, not
# adapter-owned state.  Keeping the environment lookup here gives every
# integration (lifespan, services, CLI tools) one consistent source of truth.
KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
)
KAFKA_CLIENT_ID: str = os.getenv("KAFKA_CLIENT_ID", "dossier-aggr-api")
KAFKA_SEND_TIMEOUT_SECONDS: float = float(
    os.getenv("KAFKA_SEND_TIMEOUT_SECONDS", "5")
)

OBJECT_STORAGE_PROVIDER: str = os.getenv(
    "OBJECT_STORAGE_PROVIDER", "s3-compatible"
)
OBJECT_STORAGE_BUCKET_PREFIX: str = os.getenv(
    "OBJECT_STORAGE_BUCKET_PREFIX", "viid"
)
OBJECT_STORAGE_ENDPOINT_URL: str = os.getenv("OBJECT_STORAGE_ENDPOINT_URL", "")
OBJECT_STORAGE_REGION: str = os.getenv("OBJECT_STORAGE_REGION", "us-east-1")
OBJECT_STORAGE_ACCESS_KEY_ID: str = os.getenv("OBJECT_STORAGE_ACCESS_KEY_ID", "")
OBJECT_STORAGE_SECRET_ACCESS_KEY: str = os.getenv(
    "OBJECT_STORAGE_SECRET_ACCESS_KEY", ""
)
OBJECT_STORAGE_PUBLIC_BASE_URL: str = os.getenv(
    "OBJECT_STORAGE_PUBLIC_BASE_URL", ""
)


@dataclass(frozen=True, slots=True)
class AppSettings:
    """Runtime settings snapshot built from the current environment.

    A snapshot is preferable for lifespan wiring: all clients created during
    one startup use the same values, while tests and command-line invocations
    can still change environment variables before constructing it.
    """

    kafka_bootstrap_servers: str = field(
        default_factory=lambda: os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )
    )
    kafka_client_id: str = field(
        default_factory=lambda: os.getenv("KAFKA_CLIENT_ID", "dossier-aggr-api")
    )
    kafka_send_timeout_seconds: float = field(
        default_factory=lambda: float(os.getenv("KAFKA_SEND_TIMEOUT_SECONDS", "5"))
    )
    object_storage_provider: str = field(
        default_factory=lambda: os.getenv(
            "OBJECT_STORAGE_PROVIDER", "s3-compatible"
        )
    )
    object_storage_bucket_prefix: str = field(
        default_factory=lambda: os.getenv("OBJECT_STORAGE_BUCKET_PREFIX", "viid")
    )
    object_storage_endpoint_url: str = field(
        default_factory=lambda: os.getenv("OBJECT_STORAGE_ENDPOINT_URL", "")
    )
    object_storage_region: str = field(
        default_factory=lambda: os.getenv("OBJECT_STORAGE_REGION", "us-east-1")
    )
    object_storage_access_key_id: str = field(
        default_factory=lambda: os.getenv("OBJECT_STORAGE_ACCESS_KEY_ID", "")
    )
    object_storage_secret_access_key: str = field(
        default_factory=lambda: os.getenv("OBJECT_STORAGE_SECRET_ACCESS_KEY", "")
    )
    object_storage_public_base_url: str = field(
        default_factory=lambda: os.getenv("OBJECT_STORAGE_PUBLIC_BASE_URL", "")
    )

    def __post_init__(self) -> None:
        if self.kafka_send_timeout_seconds <= 0:
            raise ValueError("KAFKA_SEND_TIMEOUT_SECONDS must be greater than zero")
        if not self.kafka_bootstrap_servers.strip():
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS must not be empty")
        if self.object_storage_provider != "s3-compatible":
            raise ValueError("OBJECT_STORAGE_PROVIDER must be s3-compatible")
        if not self.object_storage_bucket_prefix.strip():
            raise ValueError("OBJECT_STORAGE_BUCKET_PREFIX must not be empty")
        if bool(self.object_storage_access_key_id) != bool(
            self.object_storage_secret_access_key
        ):
            raise ValueError("object storage access key and secret must be set together")
        if not self.object_storage_public_base_url.strip():
            raise ValueError("OBJECT_STORAGE_PUBLIC_BASE_URL must not be empty")


def validate_runtime_settings() -> None:
    """Validate Kafka and object-storage settings at application startup."""

    if KAFKA_SEND_TIMEOUT_SECONDS <= 0:
        raise ValueError("KAFKA_SEND_TIMEOUT_SECONDS must be greater than zero")
    if not KAFKA_BOOTSTRAP_SERVERS.strip():
        raise ValueError("KAFKA_BOOTSTRAP_SERVERS must not be empty")
    if OBJECT_STORAGE_PROVIDER != "s3-compatible":
        raise ValueError("OBJECT_STORAGE_PROVIDER must be s3-compatible")
    if not OBJECT_STORAGE_BUCKET_PREFIX.strip():
        raise ValueError("OBJECT_STORAGE_BUCKET_PREFIX must not be empty")
    if bool(OBJECT_STORAGE_ACCESS_KEY_ID) != bool(OBJECT_STORAGE_SECRET_ACCESS_KEY):
        raise ValueError("object storage access key and secret must be set together")
    if not OBJECT_STORAGE_PUBLIC_BASE_URL.strip():
        raise ValueError("OBJECT_STORAGE_PUBLIC_BASE_URL must not be empty")
