"""User Service."""

from fastapi import HTTPException, status
from loguru import logger
from sqlmodel import Session, select

from src.db.models.user_models import User
from src.services.base_service import BaseService


class UserService(BaseService):
    """User Service."""

    db_session: Session

    def __init__(self, db_session: Session) -> None:
        """Initialize the UserService."""
        super().__init__(db_session)

    def create_dummy_users(self) -> list[User]:
        """Create three dummy users for testing or development purposes."""
        try:
            dummy_users = [
                User(
                    username="dummy_admin",
                    email="admin@dummy.com",
                    display_name="Dummy Admin",
                    is_dummy=True,
                    settings={"role": "admin"},
                ),
                User(
                    username="dummy_developer",
                    email="developer@dummy.com",
                    display_name="Dummy Developer",
                    is_dummy=True,
                    settings={"role": "developer"},
                ),
                User(
                    username="dummy_viewer",
                    email="viewer@dummy.com",
                    display_name="Dummy Viewer",
                    is_dummy=True,
                    settings={"role": "viewer"},
                ),
            ]

            created_users: list[User] = []
            for user in dummy_users:
                statement = select(User).where(User.username == user.username)
                existing_user = self.db_session.exec(statement).first()
                if not existing_user:
                    self.db_session.add(user)
                    created_users.append(user)
                    logger.info(f"Created dummy user: {user.username}")
                else:
                    logger.info(f"Dummy user already exists: {user.username}")
                    created_users.append(existing_user)

            self.db_session.commit()

            for user in created_users:
                self.db_session.refresh(user)
        except Exception as e:
            logger.exception(f"Failed to create dummy users: {e!s}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
        else:
            return created_users
