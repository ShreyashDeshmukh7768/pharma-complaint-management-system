"""Pydantic schemas for complaint APIs.

These schemas define validated request/response contracts for complaint
endpoints and are aligned with the SQLAlchemy Complaint model.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import ComplaintCategory, ComplaintStatus, RiskLevel


class ComplaintBase(BaseModel):
    """Common complaint fields shared across multiple schemas."""

    model_config = ConfigDict(from_attributes=True)

    # ------------------------------------------------------------------
    # Customer Information
    # ------------------------------------------------------------------
    customer_name: str = Field(
        min_length=1,
        max_length=255,
        description="Name of the customer raising the complaint.",
    )

    customer_email: EmailStr = Field(
        description="Validated customer email address.",
    )

    company_name: str = Field(
        min_length=1,
        max_length=255,
        description="Customer organization or company name.",
    )

    # ------------------------------------------------------------------
    # Product Information
    # ------------------------------------------------------------------
    product_name: str = Field(
        min_length=1,
        max_length=255,
        description="Name of the pharmaceutical product.",
    )

    batch_number: str = Field(
        min_length=1,
        max_length=100,
        description="Manufacturing batch or lot number.",
    )

    manufacturing_date: date = Field(
        description="Product manufacturing date.",
    )

    expiry_date: date = Field(
        description="Product expiry date.",
    )

    # ------------------------------------------------------------------
    # Complaint Information
    # ------------------------------------------------------------------
    complaint_description: str = Field(
        min_length=1,
        description="Detailed description of the complaint.",
    )

    complaint_category: ComplaintCategory = Field(
        description="Complaint classification.",
    )

    received_date: date = Field(
        description="Date the complaint was received.",
    )


class ComplaintCreate(ComplaintBase):
    """Request body used when creating a new complaint.

    The backend automatically generates:
    - Complaint Number
    - Initial Status (OPEN)

    The client only provides complaint details.
    """

    pass


class ComplaintUpdate(BaseModel):
    """Schema for updating an existing complaint.

    Every field is optional to support partial updates.
    """

    model_config = ConfigDict(from_attributes=True)

    customer_name: str | None = Field(default=None, min_length=1, max_length=255)
    customer_email: EmailStr | None = None
    company_name: str | None = Field(default=None, min_length=1, max_length=255)

    product_name: str | None = Field(default=None, min_length=1, max_length=255)
    batch_number: str | None = Field(default=None, min_length=1, max_length=100)
    manufacturing_date: date | None = None
    expiry_date: date | None = None

    complaint_description: str | None = Field(default=None, min_length=1)
    complaint_category: ComplaintCategory | None = None
    received_date: date | None = None

    # Workflow
    status: ComplaintStatus | None = None

    # AI Fields
    ai_summary: str | None = None
    ai_risk_level: RiskLevel | None = None
    ai_confidence_score: float | None = None


class ComplaintResponse(ComplaintBase):
    """Response returned by complaint APIs."""

    model_config = ConfigDict(from_attributes=True)

    # ------------------------------------------------------------------
    # System Generated Fields
    # ------------------------------------------------------------------
    id: uuid.UUID
    complaint_number: str
    status: ComplaintStatus

    # ------------------------------------------------------------------
    # AI Generated Fields
    # ------------------------------------------------------------------
    ai_summary: str | None = None
    ai_risk_level: RiskLevel | None = None
    ai_confidence_score: float | None = None

    # ------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------
    created_at: datetime
    updated_at: datetime