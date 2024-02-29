from starlette.testclient import TestClient

from app.config import settings
from app.main import create_application


def get_testing_client() -> TestClient:
    """Return Test Client for Fast Api."""

    app = create_application(settings)
    client = TestClient(app)

    return client
