from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    environment: str = Field(default="dev")
    project_name: str = Field(default="AI Inbox Assistant")
    database_url: str = Field(default="sqlite:///./inbox.db")

    # OAuth / Gmail
    google_client_id: str = Field(default="")
    google_client_secret: str = Field(default="")
    google_redirect_uri: str = Field(default="http://localhost:8000/auth/callback")
    gmail_scopes: str = Field(
        default="https://www.googleapis.com/auth/gmail.readonly"
    )

    # App / email settings
    app_base_url: str = Field(default="http://localhost:8000")
    digest_sender_email: str = Field(default="no-reply@example.com")

    # Stripe
    stripe_api_key: str = Field(default="")

    @property
    def gmail_scopes_list(self) -> List[str]:
        return [scope.strip() for scope in self.gmail_scopes.split(",") if scope.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
