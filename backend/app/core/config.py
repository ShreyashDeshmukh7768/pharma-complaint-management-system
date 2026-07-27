"""
Centralized application configuration.

This module loads and validates all environment variables using
Pydantic Settings. Every part of the application should import
settings from here instead of reading environment variables directly.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Values are automatically read from the `.env` file during development
    and from real environment variables in production.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # Application Settings
    # ==========================================================

    app_name: str = Field(
        default="AIVOA Pharma Complaint Management System",
        description="Display name of the application.",
    )

    app_version: str = Field(
        default="1.0.0",
        description="Current application version.",
    )

    api_prefix: str = Field(
        default="/api/v1",
        description="Base API route prefix.",
    )

    debug: bool = Field(
        default=True,
        description="Enable debug mode during development.",
    )

    # ==========================================================
    # Database Configuration
    # ==========================================================

    database_url: str = Field(
        default="postgresql://postgres:password@localhost:5432/aivoa_qms",
        description="PostgreSQL database connection string.",
    )

    # ==========================================================
    # AI Configuration
    # ==========================================================

    groq_api_key: str = Field(
        default="",
        description="Groq API Key.",
    )

    groq_model: str = Field(
        default="gemma2-9b-it",
        description="Default Groq model used by the AI pipeline.",
    )

    # ==========================================================
    # File Upload Configuration
    # ==========================================================

    upload_directory: str = Field(
        default="uploads",
        description="Directory used for uploaded complaint documents.",
    )

    max_upload_size_mb: int = Field(
        default=20,
        description="Maximum upload size in MB.",
    )

    # ==========================================================
    # CORS Configuration
    # ==========================================================

    allowed_origins: str = Field(
        default="http://localhost:3000",
        description="Allowed frontend origins.",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The settings are created only once and reused throughout
    the lifetime of the application.
    """
    return Settings()


# Singleton settings object used throughout the project
settings = get_settings()