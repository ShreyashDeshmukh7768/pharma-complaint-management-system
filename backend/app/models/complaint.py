"""Complaint ORM model for pharmaceutical complaint management."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum as SAEnum, Float, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.enums import ComplaintCategory, ComplaintStatus, RiskLevel


class Complaint(Base):
    """Represents a pharmaceutical customer complaint.

    Each Complaint object corresponds to one row in the `complaints`
    database table.
    """

    __tablename__ = "complaints"

    # ---------------------------------------------------------------------
    # Identification
    # ---------------------------------------------------------------------

    # Globally unique identifier for every complaint.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Human-readable complaint number used by quality teams.
    complaint_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    # ---------------------------------------------------------------------
    # Customer Information
    # ---------------------------------------------------------------------

    customer_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    customer_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ---------------------------------------------------------------------
    # Product Information
    # ---------------------------------------------------------------------

    # Frequently searched, so an index improves query performance.
    product_name: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    batch_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    manufacturing_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # ---------------------------------------------------------------------
    # Complaint Information
    # ---------------------------------------------------------------------

    complaint_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    complaint_category: Mapped[ComplaintCategory] = mapped_column(
        SAEnum(
            ComplaintCategory,
            name="complaint_category_enum",
        ),
        nullable=False,
    )

    # Date on which the complaint was received by the company.
    # This is different from created_at, which records when the
    # complaint was stored in the system.
    received_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # ---------------------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------------------

    status: Mapped[ComplaintStatus] = mapped_column(
        SAEnum(
            ComplaintStatus,
            name="complaint_status_enum",
        ),
        nullable=False,
        default=ComplaintStatus.OPEN,
        server_default=ComplaintStatus.OPEN.value,
    )

    # ---------------------------------------------------------------------
    # AI Generated Fields
    # ---------------------------------------------------------------------

    # Populated later by the AI pipeline.
    ai_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ai_risk_level: Mapped[RiskLevel | None] = mapped_column(
        SAEnum(
            RiskLevel,
            name="risk_level_enum",
        ),
        nullable=True,
    )

    ai_confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # ---------------------------------------------------------------------
    # Audit Fields
    # ---------------------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )