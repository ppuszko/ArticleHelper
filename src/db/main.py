from fastapi import Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends 
from fastapi_users.db import SQLAlchemyUserDatabase

from collections.abc import AsyncIterator

from .models import User
from ..config.db import DBConfig



def init_engine(url: str = DBConfig.DB_URL) -> AsyncEngine:
    return create_async_engine(url=url)


def init_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def get_sessionmaker(request: Request) -> async_sessionmaker[AsyncSession]:
    sessionmaker = getattr(request.app.state, "sessionmaker", None)
    if sessionmaker is None:
        raise RuntimeError("Sessionmaker not initialized")
    
    return sessionmaker

async def get_session(sessionmaker: async_sessionmaker[AsyncSession] = Depends(get_sessionmaker)) -> AsyncIterator[AsyncSession]:
    async with sessionmaker() as session:
        yield session 

async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)