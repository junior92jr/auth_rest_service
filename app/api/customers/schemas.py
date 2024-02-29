import enum
import uuid

from pydantic import BaseModel


class LanguageChoices(str, enum.Enum):
    """Enum class that handles language choices."""

    en = "en"
    de = "de"


class CustomerResponse(BaseModel):
    """Data class model that handles recover password request."""

    customer_id: uuid.UUID
    email: str
    country: str
    language: str


class CustomerUpdate(BaseModel):
    """Data class model that handles recover password request."""

    language: LanguageChoices
