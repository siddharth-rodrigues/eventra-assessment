import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import database_session
from app.scheduler.credit_reset import start_scheduler, stop_scheduler

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:  # pragma: no cover
    logger.info("starting application...")
    start_scheduler()

    yield

    logger.info("shutting down application...")
    stop_scheduler()

    await database_session._ASYNC_ENGINE.dispose()
    logger.info("disposed database engine and closed connections...")

    logger.info("bye! application shutdown completed")
