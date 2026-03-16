import logging

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database_session import new_async_session
from app.credits.models import CreditBalance, PlanType
from app.credits.schemas import CreditBalanceResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/me",
    response_model=CreditBalanceResponse,
    description="Get current user's credit balance",
)
async def get_my_credits(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> CreditBalanceResponse:
    result = await session.execute(
        select(CreditBalance).where(
            CreditBalance.user_id == current_user.user_id
        )
    )
    balance = result.scalar_one_or_none()

    if balance is None:
        # Create default balance for new users
        balance = CreditBalance(
            user_id=current_user.user_id,
            credits=3,
            plan_type=PlanType.FREE.value,
        )
        session.add(balance)
        await session.commit()
        await session.refresh(balance)

    return CreditBalanceResponse(
        credits=balance.credits,
        plan_type=balance.plan_type,
        last_reset_at=balance.last_reset_at,
    )
