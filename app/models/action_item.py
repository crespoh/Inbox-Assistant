from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.digest import Digest
    from app.models.email_message import EmailMessage


class ActionItem(TimestampMixin, Base):
    __tablename__ = "action_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    digest_id: Mapped[int | None] = mapped_column(
        ForeignKey("digests.id"), index=True, nullable=True
    )
    email_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("email_messages.id"), index=True, nullable=True
    )

    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="open")
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    digest: Mapped["Digest"] = relationship(back_populates="action_items")
    email_message: Mapped["EmailMessage"] = relationship(back_populates="action_items")
