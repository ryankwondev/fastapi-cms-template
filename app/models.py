from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime

class Role(str, Enum):
    administrator = "administrator"
    non_administrator = "non_administrator"

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(...)
    hashed_password: str = Field(...)
    role: Role = Field(...)
    is_active: bool = Field(default=True)
    # Other profile-related fields can be added here

class Content(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(...)
    body: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: UUID = Field(foreign_key="user.id")
