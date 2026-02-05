from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.action_item import ActionItem
    from app.models.user import User


class Digest(TimestampMixin, Base):
    __tablename__ = "digests"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "period_start", "period_end", name="uq_user_digest_period"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    highlights: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    top_email_message_ids: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    status: Mapped[str] = mapped_column(String(32), default="draft")
    generated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="digests")
    action_items: Mapped[list["ActionItem"]] = relationship(
        back_populates="digest", cascade="all, delete-orphan"
    )
