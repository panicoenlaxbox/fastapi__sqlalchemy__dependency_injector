import os
import subprocess
from pathlib import Path

import psycopg2
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from azure_sql.database import scoped_session
from azure_sql.dependencies import get_session


@pytest.fixture(scope="session", autouse=True)
def migrate_db():
    conn = psycopg2.connect(
        database="postgres",
        user=os.environ["SQLALCHEMY_URL_USER"],
        password=os.environ["SQLALCHEMY_URL_PASSWORD"],
        host=os.environ["SQLALCHEMY_URL_HOST"],
        port=int(os.environ["SQLALCHEMY_URL_PORT"]),
    )
    # https://stackoverflow.com/a/68112827
    conn.autocommit = True
    with conn.cursor() as cur:
        query = f"DROP DATABASE IF EXISTS \"{os.environ['SQLALCHEMY_URL_DBNAME']}\" WITH (FORCE);"
        cur.execute(query)
        query = f"CREATE DATABASE \"{os.environ['SQLALCHEMY_URL_DBNAME']}\";"
        cur.execute(query)

    os.chdir(Path(__file__).parent.parent.parent)
    subprocess.run(["alembic", "upgrade", "head"], check=True)


@pytest.fixture
async def session():
    session: AsyncSession
    async with scoped_session() as session:
        await session.begin()
        yield session
        await session.rollback()
    await scoped_session.remove()


@pytest.fixture
async def session_provider(session):
    yield lambda: session


@pytest.fixture
async def http_client(_app):
    # https://fastapi.tiangolo.com/advanced/async-tests/#httpx
    # https://www.python-httpx.org/advanced/#calling-into-python-web-apps
    async with AsyncClient(app=_app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
async def _app(session):
    from azure_sql.application import app

    # https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-appdependency_overrides-attribute
    app.dependency_overrides[get_session] = lambda: session
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
async def container(_app):
    return _app.container
