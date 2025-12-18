"""User endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.db.models.user_models import User
from src.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/dummy-users",
    response_model=list[User],
    status_code=status.HTTP_201_CREATED,
    summary="Create dummy users",
    description="Creates three dummy users with predefined roles for testing purposes.",
)
def create_dummy_users(
    service: Annotated[UserService, Depends(UserService.as_dependency())],
) -> list[User]:
    """Create three dummy users with different roles."""
    return service.create_dummy_users()
