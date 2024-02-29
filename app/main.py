from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api
from app.config import Settings, settings
from app.utils.logger import logger_config
from app.database import create_db_and_tables


logger = logger_config(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Triggers event before Fast API is started."""

    create_db_and_tables()

    logger.info("startup: triggered")

    yield

    logger.info("shutdown: triggered")


def create_application(app_settings: Settings) -> FastAPI:
    """Return a FastApi application."""

    application = FastAPI(
        title=app_settings.PROJECT_NAME,
        version=app_settings.VERSION,
        docs_url="/",
        description=app_settings.DESCRIPTION,
        lifespan=lifespan,
    )

    application.include_router(api)

    return application


app = create_application(settings)
