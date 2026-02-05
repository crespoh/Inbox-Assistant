from fastapi import APIRouter

from app.api import auth

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])


@router.get("/", tags=["public"])
async def root() -> dict:
    return {"status": "ok", "message": "AI Inbox Assistant API"}


@router.get("/health", tags=["public"])
async def health() -> dict:
    return {"status": "healthy"}
