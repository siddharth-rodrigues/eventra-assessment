from __future__ import annotations

import enum
import uuid
from datetime import date, datetime, time
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base

if TYPE_CHECKING:
    from app.guests.models import Guest


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"


class Event(Base):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(
        sa.String(36), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    event_date: Mapped[date] = mapped_column(sa.Date, nullable=False)
    event_time: Mapped[time | None] = mapped_column(sa.Time, nullable=True)
    location: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    occasion: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    status: Mapped[str] = mapped_column(
        sa.String(20), nullable=False, default=EventStatus.DRAFT.value
    )
    guest_limit: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    is_rsvp_enabled: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=False
    )

    host_id: Mapped[str] = mapped_column(
        sa.ForeignKey("auth_user.user_id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

    guests: Mapped[list[Guest]] = relationship(
        back_populates="event", lazy="selectin"
    )
