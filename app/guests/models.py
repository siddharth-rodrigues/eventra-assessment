from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base

if TYPE_CHECKING:
    from app.events.models import Event


class Guest(Base):
    __tablename__ = "guests"

    guest_id: Mapped[str] = mapped_column(
        sa.String(36), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(sa.String(256), nullable=True)
    phone: Mapped[str | None] = mapped_column(sa.String(20), nullable=True)
    is_attending: Mapped[bool | None] = mapped_column(sa.Boolean, nullable=True)
    rsvp_responded_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    event_id: Mapped[str] = mapped_column(
        sa.ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )

    event: Mapped[Event] = relationship(
        back_populates="guests", lazy="selectin"
    )
