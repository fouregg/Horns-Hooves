from typing import Annotated, Any

from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from app.api.dependencies.auth import auth_basic
from app.services.docs import DocsService

router = APIRouter(tags=["Документация"])


@router.get(
    path="/docs",
    include_in_schema=False,
)
async def get_docs(
    _: Annotated[None, Depends(auth_basic)],
    docs_service: Annotated[DocsService, Depends()],
) -> HTMLResponse:
    """Получить HTML-страницу с документацией API."""
    return docs_service.get_docs()


@router.get(
    path="/openapi.json",
    include_in_schema=False,
)
async def get_openapi_json(
    _: Annotated[None, Depends(auth_basic)],
    docs_service: Annotated[DocsService, Depends()],
) -> dict[str, Any]:
    """Получить OpenAPI спецификацию в формате JSON."""
    return docs_service.get_openapi_json()
