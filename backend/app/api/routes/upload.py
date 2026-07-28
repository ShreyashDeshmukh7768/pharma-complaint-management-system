"""File upload routes.

This router receives uploaded files, stores them locally, extracts text from
PDFs, invokes the AI extraction pipeline, and performs AI risk assessment.
"""

from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.ai.extractor import (
    analyze_complaint,
    extract_complaint_information,
)
from app.utils import extract_text_from_pdf

router = APIRouter(prefix="/upload", tags=["Upload"])

# ---------------------------------------------------------------------------
# Upload directory
# ---------------------------------------------------------------------------

UPLOADS_DIR = Path(__file__).resolve().parents[4] / "uploads"


class _CountingWriter:
    """Wrap a binary file object and count bytes written."""

    def __init__(self, file_obj):
        self._file_obj = file_obj
        self.bytes_written = 0

    def write(self, data: bytes) -> int:
        written = self._file_obj.write(data)
        self.bytes_written += written
        return written


def _extract_pdf_text_if_needed(saved_file_path: Path) -> str | None:
    """Extract text from a PDF file if applicable."""

    if saved_file_path.suffix.lower() != ".pdf":
        return None

    try:
        return extract_text_from_pdf(saved_file_path)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while extracting text from the PDF.",
        ) from exc


# ---------------------------------------------------------------------------
# Upload Endpoint
# ---------------------------------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a complaint document",
)
def upload_file(file: UploadFile = File(...)) -> dict:
    """
    Upload a complaint document.

    Workflow:
    1. Save uploaded file.
    2. Extract text if it is a PDF.
    3. Extract structured complaint fields using AI.
    4. Perform AI risk assessment.
    5. Return the complete AI response.
    """

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename.",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    destination_path = UPLOADS_DIR / file.filename

    file.file.seek(0)

    with destination_path.open("wb") as destination_file:
        counting_writer = _CountingWriter(destination_file)
        shutil.copyfileobj(file.file, counting_writer)

    extracted_text = _extract_pdf_text_if_needed(destination_path)

    extracted_fields = None
    analysis = None

    if extracted_text:
        try:
            extracted_fields = extract_complaint_information(extracted_text)
            analysis = analyze_complaint(extracted_fields)

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI processing failed: {str(exc)}",
            ) from exc

    return {
        "filename": file.filename,
        "content_type": file.content_type or "application/octet-stream",
        "size_bytes": counting_writer.bytes_written,
        "extracted_text": extracted_text,
        "extracted_fields": extracted_fields,
        "analysis": analysis,
        "message": "File uploaded successfully.",
    }