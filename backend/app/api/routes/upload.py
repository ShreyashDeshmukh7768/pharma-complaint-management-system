"""
File upload routes.

Workflow
--------
1. Upload PDF
2. Extract text
3. AI field extraction
4. AI risk assessment
5. Save complaint to PostgreSQL
6. Return saved complaint + AI response
"""

from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.ai.extractor import (
    analyze_complaint,
    extract_complaint_information,
)

from app.database.session import get_db
from app.schemas.complaint import ComplaintCreate
from app.services import complaint as complaint_service
from app.utils import extract_text_from_pdf

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOADS_DIR = Path(__file__).resolve().parents[4] / "uploads"


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

class _CountingWriter:
    """Counts uploaded bytes while saving."""

    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.bytes_written = 0

    def write(self, data: bytes):
        written = self.file_obj.write(data)
        self.bytes_written += written
        return written


def _extract_pdf_text(saved_file_path: Path) -> str:
    """Extract text from uploaded PDF."""

    if saved_file_path.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    return extract_text_from_pdf(saved_file_path)


# ---------------------------------------------------------------------
# Upload Endpoint
# ---------------------------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Upload Complaint PDF",
)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload PDF

    Automatically
u
    • Extracts fields

    • Performs AI analysis

    • Saves complaint into PostgreSQL
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename missing.",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    destination = UPLOADS_DIR / file.filename

    file.file.seek(0)

    with destination.open("wb") as f:
        writer = _CountingWriter(f)
        shutil.copyfileobj(file.file, writer)

    extracted_text = _extract_pdf_text(destination)

    try:

        # -----------------------------
        # AI Extraction
        # -----------------------------

        extracted_fields = extract_complaint_information(
            extracted_text
        )

        # -----------------------------
        # AI Analysis
        # -----------------------------

        analysis = analyze_complaint(
            extracted_fields
        )

        # -----------------------------
        # Build Complaint Schema
        # -----------------------------

        complaint = ComplaintCreate(

            customer_name=extracted_fields["customer_name"],

            customer_email=extracted_fields["customer_email"],

            company_name=extracted_fields["company_name"],

            product_name=extracted_fields["product_name"],

            batch_number=extracted_fields["batch_number"],

            manufacturing_date=extracted_fields["manufacturing_date"],

            expiry_date=extracted_fields["expiry_date"],

            complaint_description=extracted_fields[
                "complaint_description"
            ],

            complaint_category=extracted_fields[
                "complaint_category"
            ],

            received_date=extracted_fields[
                "received_date"
            ],
        )

        # -----------------------------
        # Save into PostgreSQL
        # -----------------------------

        saved = complaint_service.create_complaint(
            db=db,
            complaint_in=complaint,
        )

        # -----------------------------
        # Update AI Fields
        # -----------------------------

        saved = complaint_service.update_ai_fields(
            db=db,
            complaint_id=saved.id,
            summary=analysis["summary"],
            risk_level=analysis["risk_level"],
            confidence_score=analysis["confidence_score"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI Processing Failed : {exc}",
        )

    return {

        "message": "Complaint uploaded successfully.",

        "filename": file.filename,

        "content_type": file.content_type,

        "size_bytes": writer.bytes_written,

        "extracted_text": extracted_text,

        "extracted_fields": extracted_fields,

        "analysis": analysis,

        "database": {
            "saved": True,
            "complaint_id": str(saved.id),
            "complaint_number": saved.complaint_number,
        },
    }