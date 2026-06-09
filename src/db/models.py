from sqlmodel import SQLModel, Field, Relationship, Enum as PgEnum 
from sqlalchemy import Column, DateTime, func 
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from uuid import UUID 
from uuid6 import uuid7 
from datetime import datetime 
from enum import Enum 
from decimal import Decimal 
from pydantic import EmailStr


class User(SQLModel, table=True):
    __tablename__: str = "users"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    hashed_password: str = Field(nullable=False, exclude=True, repr=False)
    is_active: bool = Field(nullable=True, default=True)
    is_superuser: bool = Field(nullable=False, default=True)
    is_verified: bool = Field(nullable=False, default=True)