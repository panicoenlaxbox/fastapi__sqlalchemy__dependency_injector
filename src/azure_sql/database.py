import contextlib
import os
from asyncio import current_task
from typing import AsyncIterator
from urllib.parse import quote_plus

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path=(find_dotenv(usecwd=True)))

# https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg
# https://docs.sqlalchemy.org/en/14/core/engines.html#escaping-special-characters-such-as-signs-in-passwords
SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://"
    f"{os.environ['SQLALCHEMY_URL_USER']}:"
    f"{quote_plus(os.environ['SQLALCHEMY_URL_PASSWORD'])}@"
    f"{os.environ['SQLALCHEMY_URL_HOST']}:"
    f"{os.environ['SQLALCHEMY_URL_PORT']}/"
    f"{os.environ['SQLALCHEMY_URL_DBNAME']}"
)

engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-faq-whentocreate
# https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-asyncio-scoped-session
async_session_factory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
scoped_session = async_scoped_session(async_session_factory, scopefunc=current_task)


@contextlib.asynccontextmanager
async def session_provider() -> AsyncIterator[AsyncSession]:
    # https://stackoverflow.com/questions/63125259/what-is-the-proper-way-to-type-hint-the-return-value-of-an-asynccontextmanager
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    # https://docs.sqlalchemy.org/en/14/orm/contextual.html#using-thread-local-scope-with-web-applications
    try:
        session: AsyncSession
        async with scoped_session() as session:
            yield session
            await session.commit()
    finally:
        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-asyncio-scoped-session
        await scoped_session.remove()
