"""OpenAPI Router."""

from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/api/ref", include_in_schema=False)
def custom_openapi_ui() -> HTMLResponse:
    """Serve the custom OpenAPI UI."""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")
