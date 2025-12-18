"""Base service class for the API."""

from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from src.db.database import get_db_session


class BaseService:
    """Base service class for the API."""

    db_session: Session

    def __init__(self, db_session: Session) -> None:
        """Initialize the base service with a database session."""
        self.db_session = db_session

    def raise_not_found_error(self, message: str) -> None:
        """Raise HTTP 404 not found error with given detail."""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    def raise_conflict_error(self, message: str) -> None:
        """Raise HTTP 409 conflict error with given detail."""
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )

    @classmethod
    def as_dependency(cls) -> ...:
        """Factory for FastAPI DI for HTTP routes."""

        def _get_service(
            db_session: Annotated[Session, Depends(get_db_session)],
        ) -> BaseService:
            return cls(db_session)

        return _get_service
