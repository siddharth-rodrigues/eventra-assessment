import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.auth.views import router as auth_router
from app.core import lifespan
from app.core.config import get_settings
from app.events.views import router as events_router
from app.guests.views import router as guests_router
from app.credits.views import router as credits_router
from app.probe.views import router as probe_router

logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title="Eventra API",
    version="1.0.0",
    description="Event management platform API",
    openapi_url="/openapi.json",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan.lifespan,
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(events_router, prefix="/api/v1/events", tags=["events"])
app.include_router(guests_router, prefix="/api/v1/guests", tags=["guests"])
app.include_router(credits_router, prefix="/api/v1/credits", tags=["credits"])
app.include_router(probe_router, prefix="/api/v1", tags=["health"])

# Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/")
        for origin in get_settings().security.backend_cors_origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
