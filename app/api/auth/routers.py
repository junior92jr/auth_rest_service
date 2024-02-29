from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import get_session
from app.api.auth.schemas import (
    ResetPasswordRequest,
    RecoverPasswordRequest,
    AuthTokenResponse,
    PasswordCreatedResponse,
    PasswordRessetedResponse
)
from app.api.auth.models import AuthUser

from app.api.auth.controllers import UserController
from app.api.customers.controllers import CustomerController
from app.api.common.versions import VersionConstroller
from app.config import jwt_settings


router = APIRouter()
user_controller = UserController()
customer_controller = CustomerController()
version_controller = VersionConstroller()

annotated_auth_user = Annotated[AuthUser, Depends(
    user_controller.get_current_user)]


@router.post(
    "/recover-password",
    response_model=PasswordCreatedResponse)
def recover_password(
        payload: RecoverPasswordRequest,
        database_session: Session = Depends(get_session),
        client_version: str = Header(...)) -> PasswordCreatedResponse:
    """Set password for an importend customer and create AutUser."""

    version_controller.is_valid_version(client_version)

    if not payload.recovery_code == jwt_settings.FIXED_RECOVERY_CODE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Recovery Code sent by email is incorrect."
        )

    imported_customer = customer_controller.get_customer_profile(
        payload.email, database_session)

    user = user_controller.get_user(payload.email, database_session)

    if user:
        user = user_controller.update_user_password(
            user, payload.password, database_session)
    else:
        user = user_controller.create_user_in_database(
            payload, database_session)

    customer = customer_controller.activate_customer_account(
        user, imported_customer, database_session)

    return PasswordCreatedResponse(
        message=f"New Credentials Created for {customer.email}.")


@router.post("/reset-password", response_model=PasswordRessetedResponse)
def reset_password(
        request: ResetPasswordRequest,
        authenticate_user: annotated_auth_user,
        database_session: Session = Depends(get_session),
        client_version: str = Header(...)) -> PasswordRessetedResponse:
    """Reset password for an importend customer and update AutUser."""

    version_controller.is_valid_version(client_version)

    user_controller.compare_hash_passwords(
        authenticate_user, request.old_password)

    user = user_controller.update_user_password(
        authenticate_user, request.new_password, database_session)

    return PasswordRessetedResponse(
        message=f"New Credentials Created for {user.username}.")


@router.post("/login")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        database_session: Session = Depends(get_session),
        client_version: str = Header(...)) -> AuthTokenResponse:
    """Authenticate with credentials and gets a valid auth token."""

    version_controller.is_valid_version(client_version)

    user = user_controller.authenticate_user(
        form_data.username, form_data.password, database_session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(
        minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = user_controller.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return AuthTokenResponse(access_token=access_token, token_type="bearer")
