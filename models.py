from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime

class ProfileBase(SQLModel):
    username: str = Field()
    email: str = Field()
    name: str = Field()
    description: str = Field()
    is_formalized: bool = Field(default=False)
    start_year: int = Field(default=datetime.now().year)
    contact_phone: str = Field()
    instagram_link: Optional[str] = Field(default=None)
    x_link: Optional[str] = Field(default=None)
    facebook_link: Optional[str] = Field(default=None)
    pix_qr_code_link: Optional[str] = Field(default=None)
    site: Optional[str] = Field(default=None)

class Skill(SQLModel):
    id: int  = Field()
    name: str = Field()
    
class Cause(SQLModel):
    id: int = Field()
    name: str = Field()
    description: str = Field()
    
class SDG(SQLModel):
    id: int = Field()
    name: str = Field()
    url_ods: str = Field()
    logo_url: Optional[str] = Field(default=None)
    
class Profile(ProfileBase, table=True):
    id: int = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    ong: int = Field(nullable=False)
    
    gallery_images: Optional[List[str]] = Field(default=[])
    skills: Optional[List[Skill]] = Field(default=[])
    causes: Optional[List[Cause]] = Field(default=[])
    sustainable_development_goals: Optional[List[SDG]] = Field(default=[])
    
class PostBase(SQLModel):
    title: str = Field()
    content: str = Field()
    ong: int = Field(nullable=False)

class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

class PostCreate(PostBase):
    pass

class PostPatch(SQLModel):
    title: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)

class ProfileCreate(ProfileBase):
    pass