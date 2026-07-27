"""
FastAPI application entry point.

This module initializes the FastAPI application and registers
system-level endpoints. As the project grows, API routers,
middleware, startup events, and background tasks will be added here.
"""

from fastapi import FastAPI

from app.api.routes import complaint_router
from app.core.config import settings

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
# API Routers
# ---------------------------------------------------------------------

app.include_router(
    complaint_router,
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

    Used by deployment platforms, monitoring tools, and
    load balancers to verify the API is running.
    """

    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }