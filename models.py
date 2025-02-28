from typing import Annotated
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class PostBase(SQLModel):

    description: str = Field()
    transaction: float = Field()

class Post(PostBase, table = True):

    id: int | None = Field(default = None, primary_key = True)
    created_at: datetime = Field(default_factory = datetime.now)
    ong: int = Field(nullable = False)

class PostCreate(PostBase):

    ong: int = Field(nullable = False)

class PostPatch(PostBase):
    pass