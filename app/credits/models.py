import enum
import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class PlanType(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"


class CreditBalance(Base):
    __tablename__ = "credit_balances"

    id: Mapped[str] = mapped_column(
        sa.String(36), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        sa.ForeignKey("auth_user.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    credits: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=3)
    plan_type: Mapped[str] = mapped_column(
        sa.String(20), nullable=False, default=PlanType.FREE.value
    )
    last_reset_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
