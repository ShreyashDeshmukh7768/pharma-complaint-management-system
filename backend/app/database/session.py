"""SQLAlchemy session and engine configuration.

This module centralizes database connectivity so FastAPI routes and services can
reuse a single engine configuration and obtain short-lived sessions per request.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# Engine manages the database connection pool and low-level DBAPI connections.
# `pool_pre_ping=True` helps recover from stale/disconnected PostgreSQL connections
# that can appear in long-running production services.
engine = create_engine(
	settings.database_url,
	pool_pre_ping=True,
	echo=settings.debug,
)


# SessionLocal is a factory that creates new SQLAlchemy Session objects.
# `autocommit=False` and `autoflush=False` give explicit control over
# transactions and flush timing, while `expire_on_commit=False` avoids
# unnecessary lazy reloads after commit in typical API workflows.
SessionLocal = sessionmaker(
	bind=engine,
	autocommit=False,
	autoflush=False,
	expire_on_commit=False,
	class_=Session,
)


def get_db() -> Generator[Session, None, None]:
	"""Yield a database session for one request and close it afterward.

	Use this function as a FastAPI dependency (e.g., `Depends(get_db)`) so every
	request gets an isolated session and the connection is always released.
	"""

	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

