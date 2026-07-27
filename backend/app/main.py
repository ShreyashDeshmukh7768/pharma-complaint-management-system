"""
FastAPI application entry point.

This module initializes the FastAPI application and registers
system-level endpoints. As the project grows, API routers,
middleware, and startup events will also be added here.
"""

from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered Customer Complaint Management System for "
        "Pharmaceutical Quality Management (QMS)."
    ),
    version=settings.app_version,
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns a welcome message and useful API information.
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

    Used by monitoring tools, deployment platforms,
    and load balancers to verify that the API is running.
    """

    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }