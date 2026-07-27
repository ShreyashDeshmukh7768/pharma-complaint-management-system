"""Utility helpers to initialize the database schema.

This module is useful for local development because it can bootstrap tables
quickly without needing a full migration workflow for every small iteration.
"""

from app.database.base import Base
from app.database.session import engine

# Import models so SQLAlchemy registers them on Base.metadata before create_all.
# If models are not imported, SQLAlchemy cannot "see" their table definitions.
import app.models  # noqa: F401


def init_db() -> None:
	"""Create all database tables defined by ORM models.

	During local development, this provides a fast setup path for a fresh
	database. In production, schema changes should be managed by migrations.
	"""

	Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
	init_db()
