from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from azure_sql.database import session_provider


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # https://docs.python.org/3/library/typing.html#typing.AsyncGenerator
    async with session_provider() as session:
        yield session
