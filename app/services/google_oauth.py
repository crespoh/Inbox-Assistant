from authlib.integrations.starlette_client import OAuth

from app.core.config import get_settings

_oauth: OAuth | None = None


def get_oauth() -> OAuth:
    global _oauth
    if _oauth is not None:
        return _oauth

    settings = get_settings()
    scopes = ["openid", "email", "profile", *settings.gmail_scopes_list]

    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": " ".join(scopes)},
    )
    _oauth = oauth
    return oauth
