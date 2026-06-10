from fastapi_users import schemas 

from uuid import UUID 

class UserRead(schemas.BaseUser[UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    name: str

class UserUpdate(schemas.BaseUserUpdate):
    name: str

