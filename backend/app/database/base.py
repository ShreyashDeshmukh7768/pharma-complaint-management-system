"""Shared SQLAlchemy declarative base class for all ORM models.

This module defines the single `Base` type every model should inherit from.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
		"""Root class for all SQLAlchemy ORM models in the project.

		Why models inherit from this base:
		- It gives each model SQLAlchemy's declarative mapping behavior, so class
			attributes like `Column(...)` are interpreted as table definitions.
		- It registers every model with a shared `Base.metadata` collection.

		How SQLAlchemy uses metadata:
		- `Base.metadata` stores table objects for all inherited models.
		- Operations such as `Base.metadata.create_all(engine)` or migrations read
			this metadata to create, inspect, and manage database tables.
		"""

		pass

