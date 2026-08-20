from sqlalchemy.engine import make_url

_ASYNC_TO_SYNC_DRIVERS = {
    "postgresql+asyncpg": "postgresql+psycopg2",
}


def make_sync_database_url(database_url: str) -> str:
    """Return a synchronous SQLAlchemy URL for migration tooling."""
    parsed_url = make_url(database_url)
    driver_name = _ASYNC_TO_SYNC_DRIVERS.get(parsed_url.drivername)
    if driver_name is None:
        return database_url

    sync_url = parsed_url.set(drivername=driver_name)
    return sync_url.render_as_string(hide_password=False)
