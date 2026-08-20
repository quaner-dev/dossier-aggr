from core.database_urls import make_sync_database_url


def test_make_sync_database_url_converts_async_postgresql_driver():
    url = "postgresql+asyncpg://postgres:postgres@postgresql:5432/dossier_aggr"

    assert (
        make_sync_database_url(url)
        == "postgresql+psycopg2://postgres:postgres@postgresql:5432/dossier_aggr"
    )


def test_make_sync_database_url_leaves_sync_url_unchanged():
    assert make_sync_database_url("postgresql+psycopg2://db/app") == (
        "postgresql+psycopg2://db/app"
    )
