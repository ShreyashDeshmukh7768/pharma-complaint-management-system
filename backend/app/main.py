"""
FastAPI application entry point.

This module initializes the FastAPI application, configures middleware,
registers API routers, and exposes system-level endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import complaint_router, upload_router
from app.core.config import settings

from app.database.base import Base
from app.database.session import engine

# Import models so SQLAlchemy registers them
from app.models.complaint import Complaint

# Create all database tables
Base.metadata.create_all(bind=engine)
# ---------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered Customer Complaint Management System "
        "for Pharmaceutical Quality Management (QMS)."
    ),
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# API Routers
# ---------------------------------------------------------------------

app.include_router(
    complaint_router,
    prefix=settings.api_prefix,
)

app.include_router(
    upload_router,
    prefix=settings.api_prefix,
)

# ---------------------------------------------------------------------
# System Endpoints
# ---------------------------------------------------------------------

@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns basic information about the running API.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "documentation": "/docs",
        "health_check": "/health",
    }


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Used by deployment platforms, monitoring tools,
    and load balancers to verify the API is running.
    """
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }