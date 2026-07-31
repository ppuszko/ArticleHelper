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
    is_superuser: bool = Field(nullable=False, default=False)
    is_verified: bool = Field(nullable=False, default=False)


class Document(SQLModel, table=True):
    __tablename__: str = "documents"
    id: UUID = Field(default=uuid7, primary_key=True)
    title: str = Field(nullable=False)
    authors: str = Field(nullable=False)
    citation: str = Field(nullable=False)


class DocSegment(SQLModel, table=True):
    __tablename__: str = "doc_segments"
    id: UUID = Field(default=uuid7, primary_key=True)
    content: str = Field(nullable=False)
    translated_content: str = Field(nullable=False)
    summary: str = Field(nullable=False)
    section: str = Field(default="")
    doc_id: UUID = Field(foreign_key="documents.id")
