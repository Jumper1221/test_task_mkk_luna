import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.config import Config
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

from alembic import command
from app.db.session import get_async_session
from app.main import app as fastapi_app

pytest_plugins = ("pytest_asyncio",)


def _set_test_db_env(database_url: str) -> None:
    url = make_url(database_url)
    if url.host:
        os.environ["POSTGRES_HOST"] = url.host
    if url.port:
        os.environ["POSTGRES_PORT"] = str(url.port)
    if url.username:
        os.environ["POSTGRES_USER"] = url.username
    if url.password:
        os.environ["POSTGRES_PASSWORD"] = url.password
    if url.database:
        os.environ["POSTGRES_DB"] = url.database


def _to_sync_url(database_url: str) -> str:
    url = make_url(database_url)
    return url.set(drivername="postgresql+psycopg2").render_as_string(
        hide_password=False
    )


def _to_async_url(database_url: str) -> str:
    url = make_url(database_url)
    return url.set(drivername="postgresql+asyncpg").render_as_string(
        hide_password=False
    )


@pytest.fixture(scope="session")
def postgres_container() -> Generator[str, None, None]:
    os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

    with PostgresContainer(
        "postgis/postgis:16-3.4",
        username="test",
        password="test",
        dbname="test",
    ) as postgres:
        database_url = postgres.get_connection_url()
        _set_test_db_env(database_url)
        yield database_url


def run_migrations(database_url: str) -> None:
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def migrated_database(postgres_container: str) -> str:
    run_migrations(_to_sync_url(postgres_container))
    return postgres_container


@pytest.fixture(scope="session")
def async_engine(migrated_database: str) -> Generator[AsyncEngine, None, None]:
    engine = create_async_engine(
        _to_async_url(migrated_database),
        poolclass=NullPool,
        echo=False,
    )
    yield engine
    asyncio.run(engine.dispose())


@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.connect() as connection:
        transaction = await connection.begin()

        session_factory = async_sessionmaker(
            bind=connection,
            expire_on_commit=False,
            class_=AsyncSession,
        )

        async with session_factory() as session:
            yield session

        await transaction.rollback()


@pytest.fixture(scope="function")
def app(db_session: AsyncSession) -> FastAPI:
    async def override_get_async_session():
        yield db_session

    fastapi_app.dependency_overrides[get_async_session] = override_get_async_session
    return fastapi_app


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    fastapi_app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client
