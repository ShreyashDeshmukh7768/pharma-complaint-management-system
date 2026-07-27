"""Complaint API routes.

This layer handles HTTP concerns only (request parsing, response shaping,
status codes) and delegates business logic to the service layer.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from app.services import complaint as complaint_service

router = APIRouter(prefix="/complaints", tags=["Complaints"])


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
@router.post(
	"/",
	response_model=ComplaintResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Create a new complaint",
)
def create_complaint(
	complaint_in: ComplaintCreate,
	db: Session = Depends(get_db),
) -> ComplaintResponse:
	"""Create a complaint record.

	Complaint numbering and related business rules are handled entirely by the
	complaint service layer.
	"""

	complaint = complaint_service.create_complaint(db=db, complaint_in=complaint_in)
	return complaint


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
@router.get(
	"/",
	response_model=list[ComplaintResponse],
	summary="List complaints",
)
def get_all_complaints(
	skip: int = Query(0, ge=0, description="Number of records to skip."),
	limit: int = Query(100, ge=1, le=500, description="Maximum records to return."),
	db: Session = Depends(get_db),
) -> list[ComplaintResponse]:
	"""Return a paginated list of complaints."""

	complaints = complaint_service.get_all_complaints(db=db, skip=skip, limit=limit)
	return complaints


@router.get(
	"/{complaint_id}",
	response_model=ComplaintResponse,
	summary="Get complaint by ID",
)
def get_complaint_by_id(
	complaint_id: uuid.UUID,
	db: Session = Depends(get_db),
) -> ComplaintResponse:
	"""Return a single complaint by UUID.

	Raises 404 when the complaint does not exist.
	"""

	complaint = complaint_service.get_complaint_by_id(db=db, complaint_id=complaint_id)
	if complaint is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Complaint not found.",
		)
	return complaint


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
@router.patch(
	"/{complaint_id}",
	response_model=ComplaintResponse,
	summary="Partially update a complaint",
)
def update_complaint(
	complaint_id: uuid.UUID,
	complaint_in: ComplaintUpdate,
	db: Session = Depends(get_db),
) -> ComplaintResponse:
	"""Update complaint fields provided in the request body.

	Raises 404 when the complaint does not exist.
	"""

	updated = complaint_service.update_complaint(
		db=db,
		complaint_id=complaint_id,
		complaint_in=complaint_in,
	)
	if updated is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Complaint not found.",
		)
	return updated


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
@router.delete(
	"/{complaint_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	summary="Delete a complaint",
)
def delete_complaint(
	complaint_id: uuid.UUID,
	db: Session = Depends(get_db),
) -> None:
	"""Delete a complaint by UUID.

	Raises 404 when the complaint does not exist.
	"""

	deleted = complaint_service.delete_complaint(db=db, complaint_id=complaint_id)
	if not deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Complaint not found.",
		)

