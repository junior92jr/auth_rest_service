from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlmodel import Session

from app.database import get_session

from app.api.auth.models import AuthUser
from app.api.auth.controllers import UserController
from app.api.common.versions import VersionConstroller

from app.api.customers.schemas import CustomerResponse, CustomerUpdate
from app.api.customers.controllers import CustomerController


router = APIRouter()
user_controller = UserController()
customer_controller = CustomerController()
version_controller = VersionConstroller()

annotated_auth_user = Annotated[AuthUser, Depends(
    user_controller.get_current_user)]


@router.get("/me", response_model=CustomerResponse)
def get_authenticated_customer(
        authenticated_user: annotated_auth_user,
        database_session: Session = Depends(get_session),
        client_version: str = Header(...)) -> CustomerResponse:
    """Retrieve Customer profile from the authenticated user."""

    version_controller.is_valid_version(client_version)

    customer = customer_controller.get_customer_profile(
        authenticated_user.username, database_session)

    return CustomerResponse(**customer.columns_to_dict())


@router.put("/me/edit-data", response_model=CustomerResponse)
def update_authenticated_customer(
        update_request: CustomerUpdate,
        authenticated_user: annotated_auth_user,
        database_session: Session = Depends(get_session),
        client_version: str = Header(...)):
    """Retrieve all bank accounts from the database."""

    version_controller.is_valid_version(client_version)

    customer = customer_controller.get_customer_profile(
        authenticated_user.username, database_session)

    customer_to_update = customer_controller.update_customer_data(
        update_request, customer, database_session)

    return CustomerResponse(**customer_to_update.columns_to_dict())
