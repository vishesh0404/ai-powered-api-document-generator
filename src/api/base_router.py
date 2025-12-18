"""Base router for Ingo API."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping() -> dict:
    """Ping the API."""
    return {"message": "pong"}
