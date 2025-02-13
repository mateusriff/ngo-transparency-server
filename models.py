from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str = Field()
    description: str = Field()
    transaction: float = Field()
    ong: int = Field(nullable=False)

