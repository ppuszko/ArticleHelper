from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from collections.abc import AsyncIterator

from db.main import get_sessionmaker

class UnitOfWork:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.__sessionmaker = sessionmaker
        self.__session: AsyncSession | None = None 

    async def __aenter__(self) -> "UnitOfWork":
        self.__session = self.__sessionmaker()
        return self 
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.__session:
            try:
                if exc_val:
                    await self.__session.rollback()
                else:
                    await self.__session.commit()
            finally:
                await self.__session.close()
                self.__session = None
    
    def __get_session(self) -> AsyncSession:
        if self.__session is None:
            raise RuntimeError("Session not initialized on UnitOfWork object.")
        return self.__session
    

async def get_uow(sessionmaker: async_sessionmaker[AsyncSession] = Depends(get_sessionmaker)) -> AsyncIterator[UnitOfWork]:
    uow = UnitOfWork(sessionmaker)
    async with uow:
        yield uow  

