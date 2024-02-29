from fastapi import APIRouter

from app.api.customers import routers as customers
from app.api.auth import routers as authentication


api = APIRouter()


api.include_router(
    customers.router, prefix="/customers", tags=["Customers"],
)

api.include_router(
    authentication.router, prefix="/auth", tags=["Authentication"],
)
