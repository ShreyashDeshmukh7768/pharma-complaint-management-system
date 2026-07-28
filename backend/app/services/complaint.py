"""
Business service layer for complaint workflows.

This module contains business logic only. Database access is delegated
to the CRUD layer.
"""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.crud import complaint as complaint_crud
from app.models.complaint import Complaint
from app.models.enums import ComplaintCategory, RiskLevel
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate


# ---------------------------------------------------------------------
# Complaint Number Generation
# ---------------------------------------------------------------------

def _format_complaint_number(year: int, sequence: int) -> str:
    """Return complaint number in format CMP-YYYY-000001."""

    return f"CMP-{year}-{sequence:06d}"


def _extract_sequence(complaint_number: str) -> int:
    """Extract numeric sequence from complaint number."""

    try:
        return int(complaint_number.split("-")[-1])
    except (ValueError, IndexError):
        return 0


def _generate_complaint_number(db: Session) -> str:
    """Generate the next complaint number."""

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

        except Exception:
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


# ---------------------------------------------------------------------
# Manual Complaint Creation
# ---------------------------------------------------------------------

def create_complaint(
    db: Session,
    complaint_in: ComplaintCreate,
) -> Complaint:
    """
    Create complaint from manually entered form.
    """

    complaint_number = _generate_complaint_number(db)

    return complaint_crud.create_complaint(
        db=db,
        complaint_in=complaint_in,
        complaint_number=complaint_number,
    )


# ---------------------------------------------------------------------
# AI Complaint Creation
# ---------------------------------------------------------------------

def create_complaint_from_ai(
    db: Session,
    extracted_fields: dict,
    analysis: dict,
) -> Complaint:
    """
    Create complaint directly from AI extracted fields.
    """

    complaint_data = ComplaintCreate(
        customer_name=extracted_fields.get("customer_name") or "Unknown",

        customer_email=(
            extracted_fields.get("customer_email")
            or "unknown@example.com"
        ),

        company_name=(
            extracted_fields.get("company_name")
            or extracted_fields.get("customer_name")
            or "Unknown"
        ),

        product_name=(
            extracted_fields.get("product_name")
            or "Unknown Product"
        ),

        batch_number=(
            extracted_fields.get("batch_number")
            or "Unknown"
        ),

        manufacturing_date=extracted_fields.get(
            "manufacturing_date"
        ),

        expiry_date=extracted_fields.get(
            "expiry_date"
        ),

        complaint_description=(
            extracted_fields.get("complaint_description")
            or "No description provided."
        ),

        complaint_category=ComplaintCategory(
            extracted_fields.get("complaint_category")
        ),

        received_date=extracted_fields.get(
            "received_date"
        ),
    )

    complaint = create_complaint(
        db=db,
        complaint_in=complaint_data,
    )

    # -------------------------
    # Store AI Fields
    # -------------------------

    complaint.ai_summary = analysis.get("summary")

    risk = analysis.get("risk_level")
    if risk:
        complaint.ai_risk_level = RiskLevel(risk)

    complaint.ai_confidence_score = analysis.get(
        "confidence_score"
    )

    db.commit()
    db.refresh(complaint)

    return complaint


# ---------------------------------------------------------------------
# AI Field Update
# ---------------------------------------------------------------------

def update_ai_fields(
    db: Session,
    complaint_id: uuid.UUID,
    summary: str | None = None,
    risk_level: str | None = None,
    confidence_score: float | None = None,
) -> Complaint | None:
    """Update the AI-generated fields on an existing complaint."""

    complaint = complaint_crud.get_complaint_by_id(
        db=db,
        complaint_id=complaint_id,
    )

    if complaint is None:
        return None

    if summary is not None:
        complaint.ai_summary = summary

    if risk_level is not None:
        complaint.ai_risk_level = RiskLevel(risk_level)

    if confidence_score is not None:
        complaint.ai_confidence_score = confidence_score

    try:
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise


# ---------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------

def get_complaint_by_id(
    db: Session,
    complaint_id: uuid.UUID,
) -> Complaint | None:

    return complaint_crud.get_complaint_by_id(
        db=db,
        complaint_id=complaint_id,
    )


def get_all_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Complaint]:

    return complaint_crud.get_all_complaints(
        db=db,
        skip=skip,
        limit=limit,
    )


# ---------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------

def update_complaint(
    db: Session,
    complaint_id: uuid.UUID,
    complaint_in: ComplaintUpdate,
) -> Complaint | None:

    complaint = complaint_crud.get_complaint_by_id(
        db=db,
        complaint_id=complaint_id,
    )

    if complaint is None:
        return None

    return complaint_crud.update_complaint(
        db=db,
        complaint=complaint,
        complaint_in=complaint_in,
    )


# ---------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------

def delete_complaint(
    db: Session,
    complaint_id: uuid.UUID,
) -> bool:

    complaint = complaint_crud.get_complaint_by_id(
        db=db,
        complaint_id=complaint_id,
    )

    if complaint is None:
        return False

    complaint_crud.delete_complaint(
        db=db,
        complaint=complaint,
    )

    return True


__all__ = [
    "create_complaint",
    "create_complaint_from_ai",
    "update_ai_fields",
    "get_complaint_by_id",
    "get_all_complaints",
    "update_complaint",
    "delete_complaint",
]