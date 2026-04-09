from collections.abc import AsyncGenerator

from app.db.session import get_db_session


async def db_session_dep() -> AsyncGenerator:
    async for session in get_db_session():
        yield session
