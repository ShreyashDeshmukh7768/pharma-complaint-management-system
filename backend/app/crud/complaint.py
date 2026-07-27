"""Database access helpers for Complaint entities.

This module is intentionally limited to persistence operations only.
Business rules (such as complaint number generation) belong in the
service layer, not the CRUD layer.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate


def create_complaint(
    db: Session,
    complaint_in: ComplaintCreate,
    complaint_number: str,
) -> Complaint:
    """Create and save a new complaint.

    The complaint number is supplied by the service layer because
    numbering is a business rule rather than a database concern.
    """

    complaint = Complaint(
        complaint_number=complaint_number,
        **complaint_in.model_dump(),
    )

    try:
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise


def get_complaint_by_id(
    db: Session,
    complaint_id: uuid.UUID,
) -> Complaint | None:
    """Return a complaint using its UUID."""

    stmt = select(Complaint).where(Complaint.id == complaint_id)
    return db.execute(stmt).scalar_one_or_none()


def get_complaint_by_number(
    db: Session,
    complaint_number: str,
) -> Complaint | None:
    """Return a complaint using its business complaint number."""

    stmt = select(Complaint).where(
        Complaint.complaint_number == complaint_number
    )
    return db.execute(stmt).scalar_one_or_none()


def get_all_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Complaint]:
    """Return complaints ordered from newest to oldest."""

    stmt = (
        select(Complaint)
        .order_by(Complaint.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.execute(stmt).scalars().all())


def update_complaint(
    db: Session,
    complaint: Complaint,
    complaint_in: ComplaintUpdate,
) -> Complaint:
    """Update an existing complaint with supplied fields."""

    update_data = complaint_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(complaint, field, value)

    try:
        # No db.add() is needed because SQLAlchemy is already tracking
        # this object after it was loaded from the database.
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise

def get_latest_complaint(db: Session) -> Complaint | None:
    """Return the most recently created complaint."""

    stmt = (
        select(Complaint)
        .order_by(Complaint.created_at.desc())
        .limit(1)
    )

    return db.execute(stmt).scalar_one_or_none()

def delete_complaint(
    db: Session,
    complaint: Complaint,
) -> None:
    """Delete a complaint from the database."""

    try:
        db.delete(complaint)
        db.commit()
    except Exception:
        db.rollback()
        raise