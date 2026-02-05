from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import router as api_router
from app.core.config import get_settings
from app.db.session import init_db


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        session_cookie=settings.session_cookie_name,
        same_site="lax",
        https_only=settings.environment == "prod",
    )
    app.include_router(api_router)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app


app = create_app()
