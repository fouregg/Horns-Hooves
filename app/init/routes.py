from fastapi import APIRouter, FastAPI

from app.api.routes import docs, organisation


def setup_routes(app: FastAPI) -> FastAPI:
    router = APIRouter(prefix="/api/v1")

    router.include_router(router=docs.router)
    router.include_router(router=organisation.router)

    app.include_router(router=router)

    return app
