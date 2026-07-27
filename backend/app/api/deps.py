"""
Reusable FastAPI dependencies.

This module centralizes commonly used dependencies so route files stay clean
and consistent.
"""

from sqlalchemy.orm import Session

from app.database import get_db


def get_database_session() -> Session:
    """
    Return a database session dependency.

    Routes should use:

        db: Session = Depends(get_database_session)

    instead of importing get_db directly.
    """
    return next(get_db())