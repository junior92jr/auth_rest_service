from sqlmodel import Session, SQLModel, create_engine

from app.config import settings


engine = create_engine(settings.DATABASE_URI)


def create_db_and_tables() -> None:
    """Creates Database tables from the models."""

    SQLModel.metadata.create_all(engine)


def get_session():
    """Gives a session to the database."""

    with Session(engine) as session:
        yield session
