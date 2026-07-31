from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select 

from uuid import UUID 

from src.db.models import Document
from src.tools.schemas import DocInfo

class DocService:
    def __init__(self, session: AsyncSession):
        self._session = session 

    async def add_doc(self, doc_info: DocInfo):
        doc = Document(**(doc_info.model_dump()))

        self._session.add(doc)

    async def get_doc_by_id(self, id: UUID) -> Document:
        res = await self._session.exec(select(Document).where(Document.id == id))
        doc = res.first()

        if doc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document with given id not found")
        return doc 
    
    
