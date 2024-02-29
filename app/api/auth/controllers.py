from typing import Annotated

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import jwt_settings
from app.database import get_session
from app.utils.logger import logger_config
from app.api.common.exceptions import UserCreationError

from app.api.auth.schemas import (
    RecoverPasswordRequest,
    AuthTokenDataResponse
)
from app.api.auth.models import AuthUser


logger = logger_config(__name__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class JWTAuthController:
    """Constroller class that handles Auth logic with the database."""

    def get_password_hashed(self, password: str) -> str:
        """Method that returns a hashed plain password."""

        return pwd_context.hash(password)

    def verify_password(
            self, plain_password: str,
            hashed_password: str) -> CryptContext.hash:
        """Method that verifies JWT hashing pasword."""

        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> CryptContext.hash:
        """Method that hashes the password string from parameter."""

        return pwd_context.hash(password)

    def create_access_token(
            self, data: dict, expires_delta: timedelta | None = None):
        """Method that creates encoded JWT access token."""

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)

        return encoded_jwt


class UserController(JWTAuthController):
    """Controller Class that handles AuthUser funtionality with the database."""

    def get_user(self, username: str, database_session: Session) -> AuthUser:
        """Method that retrieves an AuthUser row from the database."""

        statement = select(AuthUser).where(AuthUser.username == username)
        user = database_session.exec(statement).first()

        if user:
            return user

    def get_current_user(
            self, token: Annotated[str, Depends(oauth2_scheme)],
            database_session: Session = Depends(get_session)) -> AuthUser:
        """Method that retrieve the current authenticated AuthUser."""

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
            username: str = payload.get("sub")

            if username is None:
                raise credentials_exception
            token_data = AuthTokenDataResponse(username=username)
        except JWTError:
            raise credentials_exception

        user = self.get_user(
            username=token_data.username, database_session=database_session)

        if user is None:
            raise credentials_exception

        return user

    def authenticate_user(
            self, username: str, password: str,
            database_session: Session) -> AuthUser:
        """Methot that authenticates a user using the credentials."""

        user = self.get_user(username, database_session)

        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False

        return user

    def create_user_in_database(
            self, set_password_request: RecoverPasswordRequest,
            session: Session) -> AuthUser:
        """Creare a new AuthUser instance into the database."""

        hashed_password = self.get_password_hashed(set_password_request.password)
        set_password_request.password = hashed_password

        new_user = AuthUser(
            username=set_password_request.email,
            password=set_password_request.password
        )

        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user

        except UserCreationError as error:
            logger.error(error.message.format(new_user.username))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service error, transactions will Rollback.")

    def update_user_password(
            self, user: AuthUser, new_password: str,
            database_session: Session) -> AuthUser:
        """Method that updates the password of an AuthUser instance."""

        hashed_password = self.get_password_hashed(new_password)
        user.password = hashed_password

        try:
            database_session.add(user)
            database_session.commit()
            database_session.refresh(user)

            return user

        except UserCreationError as error:
            logger.error(error.message.format(user.username))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service error, transactions will Rollback."
            )

    def compare_hash_passwords(
            self, user: AuthUser, request_password: str) -> None:
        """Method that compares hashed password in database."""

        if not self.verify_password(request_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Old Password does not match."
            )
