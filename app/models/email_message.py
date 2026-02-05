from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.action_item import ActionItem
    from app.models.user import User


class EmailMessage(TimestampMixin, Base):
    __tablename__ = "email_messages"
    __table_args__ = (
        UniqueConstraint("user_id", "gmail_message_id", name="uq_user_gmail_message"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    gmail_message_id: Mapped[str] = mapped_column(String(128), index=True)
    gmail_thread_id: Mapped[str | None] = mapped_column(String(128), index=True)

    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    from_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    to_emails: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    cc_emails: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    body_plain: Mapped[str | None] = mapped_column(Text, nullable=True)
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    label_ids: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    ai_category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_importance_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship(back_populates="email_messages")
    action_items: Mapped[list["ActionItem"]] = relationship(
        back_populates="email_message", cascade="all, delete-orphan"
    )
