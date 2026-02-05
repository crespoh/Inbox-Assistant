from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name)
    app.include_router(api_router)
    return app


app = create_app()
