"""Reusable enum definitions for complaint domain models.

These enums standardize values used by SQLAlchemy models, validation schemas,
and API payloads across the backend.
"""

from enum import Enum


class ComplaintStatus(str, Enum):
	"""Lifecycle status for a customer complaint record.

	This keeps complaint workflow states consistent in the database and API,
	which helps reporting, filtering, and audit traceability.
	"""

	OPEN = "OPEN"
	UNDER_REVIEW = "UNDER_REVIEW"
	INVESTIGATION = "INVESTIGATION"
	CAPA_INITIATED = "CAPA_INITIATED"
	CLOSED = "CLOSED"


class RiskLevel(str, Enum):
	"""Risk severity assigned to a complaint.

	Risk level supports prioritization, escalation rules, and compliance-driven
	response timelines in pharmaceutical quality workflows.
	"""

	LOW = "LOW"
	MEDIUM = "MEDIUM"
	HIGH = "HIGH"
	CRITICAL = "CRITICAL"


class ComplaintCategory(str, Enum):
	"""Domain categories describing the type of complaint.

	Categories make it easier to trend root causes, drive CAPA analytics, and
	produce regulatory or internal quality reports.
	"""

	PRODUCT_QUALITY = "PRODUCT_QUALITY"
	PACKAGING = "PACKAGING"
	LABELING = "LABELING"
	CONTAMINATION = "CONTAMINATION"
	STABILITY = "STABILITY"
	ADVERSE_EVENT = "ADVERSE_EVENT"
	OTHER = "OTHER"


__all__ = ["ComplaintStatus", "RiskLevel", "ComplaintCategory"]

