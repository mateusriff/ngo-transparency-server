from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime

class ProfileBase(SQLModel):
    username: str = Field()
    email: str = Field()
    name: str = Field()
    description: str = Field()
    is_formalized: bool = Field(default=False)
    start_year: int = Field(default=0)
    contact_phone: str = Field()
    instagram_link: Optional[str] = Field(default=None)
    x_link: Optional[str] = Field(default=None)
    facebook_link: Optional[str] = Field(default=None)
    pix_qr_code_link: Optional[str] = Field(default=None)
    site: Optional[str] = Field(default=None)

# Profile model with relationships
class Profile(ProfileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    ong: int = Field(nullable=False)
    
    # Relationships
    gallery_images: Optional[List["GalleryImage"]] = Relationship(back_populates="profile")
    skills: Optional[List["Skill"]] = Relationship(back_populates="profile")
    causes: Optional[List["Cause"]] = Relationship(back_populates="profile")
    sustainable_development_goals: Optional[List["SDG"]] = Relationship(back_populates="profile")

# New table for GalleryImages
class GalleryImage(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    url: str = Field()
    profile_id: int = Field(foreign_key="profile.id")

# Skills table
class Skill(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    profile_id: int = Field(foreign_key="profile.id")

# Causes table
class Cause(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    description: str = Field()
    profile_id: int = Field(foreign_key="profile.id")

# Sustainable Development Goals table
class SDG(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    url_ods: str = Field()
    logo_url: Optional[str] = Field(default=None)
    profile_id: int = Field(foreign_key="profile.id")

# Post models
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

# ProfileCreate model
class ProfileCreate(ProfileBase):
    pass