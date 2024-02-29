import os

from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    """Implements General Settings for JWT auth tokens."""

    SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    FIXED_RECOVERY_CODE: int = os.getenv("FIXED_RECOVERY_CODE")

    class Config:
        case_sensitive = True


class Settings(BaseSettings):
    """Implements General Settings for the Application."""

    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    DESCRIPTION: str = os.getenv("DESCRIPTION")
    ENV: str = os.getenv("ENVIRONMENT")
    VERSION: str = os.getenv("VERSION")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URI: str = os.getenv("DATABASE_URL")

    class Config:
        case_sensitive = True


class TestSettings(Settings):
    """Implements General Settings for Testing the Application."""

    DATABASE_URI: str = os.getenv("DATABASE_TEST_URL")

    class Config:
        case_sensitive = True


jwt_settings = JWTSettings()
settings = Settings()
test_settings = TestSettings()
