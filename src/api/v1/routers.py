"""V1 Routes."""

from fastapi import APIRouter

from src.api.v1.endpoints import user

router = APIRouter(prefix="/api/v1", tags=["V1 Routes"])

router.include_router(router=user.router)
