"""Database utilities using SQLModel."""

from collections.abc import Generator

from fastapi.requests import Request
from pydantic import StrictStr
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from src.common import BaseModel
from src.utils import DB_DIR, SCHEMA_NAME


class BaseSQLModel(SQLModel):
    """Base SQLModel class for models."""


class DatabaseConfig(BaseModel):
    """Database configuration settings."""

    uri: StrictStr = f"{DB_DIR}/api_data.db"
    """Database file path for DuckDB."""


def _create_database_schema(engine: Engine) -> None:
    """Create the application schema if it doesn't exist.

    Uses raw SQL through the engine to avoid direct SQLAlchemy imports.
    """
    with engine.begin() as conn:
        _ = conn.exec_driver_sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")


def _create_all_tables(engine: Engine) -> None:
    """Create all SQLModel tables in the configured engine."""
    SQLModel.metadata.create_all(engine)


def init_engine(config: DatabaseConfig) -> Engine:
    """Initialize and return a SQLModel engine based on the given config."""
    database_url = f"duckdb:///{config.uri}"
    engine = create_engine(database_url)
    _create_database_schema(engine)
    _create_all_tables(engine)
    return engine


def get_db_session(request: Request) -> Generator:
    """Yield a SQLModel session for standard HTTP requests using app state engine."""
    engine = request.app.state.engine
    with Session(engine) as session:
        yield session
