"""Business service layer for complaint workflows.

This module contains business logic only. Database access is delegated
to the CRUD layer.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.crud import complaint as complaint_crud
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate


def _format_complaint_number(year: int, sequence: int) -> str:
    """Return a complaint number in the format CMP-YYYY-000001."""

    return f"CMP-{year}-{sequence:06d}"


def _extract_sequence(complaint_number: str) -> int:
    """Extract the numeric sequence from a complaint number.

    Example:
        CMP-2026-000145 -> 145

    Returns 0 if the format is invalid.
    """

    try:
        return int(complaint_number.split("-")[-1])
    except (ValueError, IndexError):
        return 0


def _generate_complaint_number(db: Session) -> str:
    """Generate the next unique complaint number."""

    current_year = datetime.now().year

    latest = complaint_crud.get_latest_complaint(db)

    if latest is None:
        sequence = 1

    else:
        try:
            year = int(latest.complaint_number.split("-")[1])

            if year == current_year:
                sequence = _extract_sequence(latest.complaint_number) + 1
            else:
                sequence = 1

        except (ValueError, IndexError):
            sequence = 1

    while True:
        complaint_number = _format_complaint_number(
            current_year,
            sequence,
        )

        existing = complaint_crud.get_complaint_by_number(
            db,
            complaint_number,
        )

        if existing is None:
            return complaint_number

        sequence += 1


def create_complaint(
    db: Session,
    complaint_in: ComplaintCreate,
) -> Complaint:
    """Create a complaint after applying business rules."""

    complaint_number = _generate_complaint_number(db)

    complaint = complaint_crud.create_complaint(
        db=db,
        complaint_in=complaint_in,
        complaint_number=complaint_number,
    )

    # Future extension points
    #
    # trigger_ai_analysis(complaint)
    # send_notification(complaint)
    # write_audit_log("complaint_created", complaint)

    return complaint


__all__ = [
    "create_complaint",
]