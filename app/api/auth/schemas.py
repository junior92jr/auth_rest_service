from pydantic import BaseModel, EmailStr, Field


class RecoverPasswordRequest(BaseModel):
    """Data class model that handles recover password request."""

    recovery_code: int
    email: EmailStr
    password: str = Field(min_length=10, max_length=30)


class ResetPasswordRequest(BaseModel):
    """Data class model that handles resets password request."""

    old_password: str = Field(min_length=10, max_length=30)
    new_password: str = Field(min_length=10, max_length=30)


class AuthTokenResponse(BaseModel):
    """Data class model that handles Auth Token response."""

    access_token: str
    token_type: str


class AuthTokenDataResponse(BaseModel):
    """Data class model that handles Auth Token response."""

    username: str | None = None


class UserResponse(BaseModel):
    """Data class model that handles Auth Token response."""

    username: str
    is_active: bool


class PasswordCreatedResponse(BaseModel):
    """Data class model that handles Auth Token response."""

    message: str
