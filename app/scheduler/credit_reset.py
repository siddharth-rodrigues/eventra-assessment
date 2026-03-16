"""Monthly credit reset scheduler.

Resets free-tier users to 3 credits and premium users to 10 credits
on the 1st of each month.
"""

import asyncio
import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, update

from app.core.database_session import new_script_async_session
from app.credits.models import CreditBalance, PlanType

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

FREE_CREDITS = 3
PREMIUM_CREDITS = 10


async def reset_monthly_credits() -> None:
    """Reset credits for all users based on their plan type."""
    logger.info("Starting monthly credit reset...")

    async with new_script_async_session() as session:
        # Reset free users
        await session.execute(
            update(CreditBalance)
            .where(CreditBalance.plan_type == PlanType.FREE.value)
            .values(credits=FREE_CREDITS, last_reset_at=datetime.now(timezone.utc))
        )

        # Reset premium users
        await session.execute(
            update(CreditBalance)
            .where(CreditBalance.plan_type == PlanType.PREMIUM.value)
            .values(credits=PREMIUM_CREDITS, last_reset_at=datetime.now(timezone.utc))
        )

        await session.commit()

    logger.info("Monthly credit reset completed successfully")


def start_scheduler() -> None:
    """Start the credit reset scheduler."""
    scheduler.add_job(
        reset_monthly_credits,
        "cron",
        day=1,
        hour=0,
        minute=0,
        timezone="UTC",
        id="monthly_credit_reset",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Credit reset scheduler started")


def stop_scheduler() -> None:
    """Stop the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Credit reset scheduler stopped")
