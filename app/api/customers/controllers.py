from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.utils.logger import logger_config

from app.api.auth.models import AuthUser
from app.api.common.exceptions import CustomerUpdateError

from app.api.customers.schemas import CustomerUpdate
from app.api.customers.models import Customer


logger = logger_config(__name__)


class CustomerController:
    """Constroller class that handles Customer logic with the database."""

    def get_customer_profile(
            self, email: str, database_session: Session) -> Customer:
        """Method that gets the profile from the authenticated user."""

        results = database_session.exec(
            select(Customer).where(Customer.email == email))

        customer = results.first()

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer not found with email: {email}")

        return customer

    def activate_customer_account(
            self, user: AuthUser, customer: Customer,
            database_session: Session) -> Customer:
        """Method that activates a customer account."""

        customer.user = user.id

        try:
            database_session.add(customer)
            database_session.commit()
            database_session.refresh(customer)

            return customer

        except CustomerUpdateError as error:
            logger.error(error.message.format(customer.email))

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service error, transactions will Rollback.")

    def update_customer_data(
            self, update_request: CustomerUpdate,
            customer: Customer, database_session: Session) -> Customer:
        """Method that updates customer data."""

        customer.language = update_request.language

        try:
            database_session.add(customer)
            database_session.commit()
            database_session.refresh(customer)

            return customer

        except CustomerUpdateError as error:
            logger.error(error.message.format(customer.email))

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service error, transactions will Rollback.")
