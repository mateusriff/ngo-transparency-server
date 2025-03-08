from datetime import datetime
from sqlmodel import Field, SQLModel

class PostBase(SQLModel):
    description: str = Field()
    transaction: float = Field()

class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    ong: int = Field(nullable=False)

class PostCreate(PostBase):
    ong: int = Field(nullable=False)

class PostPatch(PostBase):
    pass

class ProfileBase(SQLModel):
    name: str = Field()
    email: str = Field()

class Profile(ProfileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    ong: int = Field(nullable=False)

class ProfileCreate(ProfileBase):
    ong: int = Field(nullable=False)

class ProfilePatch(ProfileBase):
    pass