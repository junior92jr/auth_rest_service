import enum
from typing import Optional

from sqlmodel import Field, SQLModel, AutoString

from pydantic import EmailStr, UUID4


class LanguageChoices(str, enum.Enum):
    en = "en"
    de = "de"


class Customer(SQLModel, table=True):
    customer_id: UUID4 = Field(primary_key=True)
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    country: str
    language: LanguageChoices = Field(default=None, nullable=True)
    user: Optional[int] = Field(
        foreign_key="authuser.id", default=None, nullable=True)

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
