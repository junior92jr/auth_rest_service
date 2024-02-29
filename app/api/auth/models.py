from datetime import datetime
from pydantic import EmailStr

from sqlmodel import SQLModel, AutoString, Field


class AuthUser(SQLModel, table=True):
    """Model that represents the table for AuthUser in the database."""

    id: int = Field(nullable=False, primary_key=True)
    username: EmailStr = Field(nullable=False, sa_type=AutoString)
    password: str
    is_active: bool = False
    is_superuser: bool = False
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
