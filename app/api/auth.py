from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User
from app.services.google_oauth import get_oauth

router = APIRouter()


def _token_expires_at(token: dict) -> datetime | None:
    if token.get("expires_at") is not None:
        return datetime.fromtimestamp(token["expires_at"], tz=timezone.utc)
    if token.get("expires_in") is not None:
        return datetime.now(tz=timezone.utc) + timedelta(seconds=token["expires_in"])
    return None


@router.get("/login")
async def login(request: Request) -> RedirectResponse:
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=500, detail="Google OAuth is not configured.")

    oauth = get_oauth()
    redirect_uri = settings.google_redirect_uri
    # TODO: Store OAuth state server-side for enhanced security.
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent",
    )


@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    oauth = get_oauth()
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = await oauth.google.parse_id_token(request, token)

    email = userinfo.get("email") if userinfo else None
    google_sub = userinfo.get("sub") if userinfo else None
    display_name = userinfo.get("name") if userinfo else None
    if not email or not google_sub:
        raise HTTPException(status_code=400, detail="Google user info unavailable.")

    user = (
        db.query(User)
        .filter((User.google_sub == google_sub) | (User.email == email))
        .one_or_none()
    )
    if not user:
        user = User(email=email, google_sub=google_sub, display_name=display_name)
        db.add(user)
    else:
        user.email = email
        user.google_sub = google_sub
        if display_name:
            user.display_name = display_name

    user.google_access_token = token.get("access_token")
    if token.get("refresh_token"):
        user.google_refresh_token = token["refresh_token"]
    user.access_token_expires_at = _token_expires_at(token)

    db.commit()
    db.refresh(user)

    request.session["user_id"] = user.id
    return RedirectResponse(url="/")


@router.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/")
