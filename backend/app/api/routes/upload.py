"""File upload routes.

This router is intentionally limited to receiving a file from the client,
persisting it to the local uploads directory, and returning upload metadata.
PDF text extraction is delegated to the reusable utility module.
"""

from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.utils import extract_text_from_pdf

router = APIRouter(prefix="/upload", tags=["Upload"])


# The project's uploads directory lives at the backend root.
UPLOADS_DIR = Path(__file__).resolve().parents[4] / "uploads"


class _CountingWriter:
	"""Wrap a binary file object and count bytes as data is written.

	`shutil.copyfileobj()` writes through this wrapper, so we can save the file
	and measure the byte size in a single pass without reading the upload twice.
	"""

	def __init__(self, file_obj):
		self._file_obj = file_obj
		self.bytes_written = 0

	def write(self, data: bytes) -> int:
		written = self._file_obj.write(data)
		self.bytes_written += written
		return written


def _extract_pdf_text_if_needed(saved_file_path: Path) -> str | None:
	"""Extract text from a saved PDF file when the extension indicates PDF.

	Non-PDF files bypass extraction and return `None`. PDF extraction errors are
	translated into HTTP exceptions so the route stays HTTP-friendly.
	"""

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
	summary="Upload a file",
)
def upload_file(file: UploadFile = File(...)) -> dict[str, str | int | None]:
	"""Save an uploaded file to the local uploads directory.

	The file is stored using the original filename provided by the client.
	The response includes basic file metadata and, for PDFs, the extracted text.
	"""

	if not file.filename:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Uploaded file must have a filename.",
		)

	UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

	destination_path = UPLOADS_DIR / file.filename

	# Ensure the file is written from the beginning in case the upload object
	# has been touched before reaching this handler.
	file.file.seek(0)

	with destination_path.open("wb") as destination_file:
		counting_writer = _CountingWriter(destination_file)
		shutil.copyfileobj(file.file, counting_writer)

	extracted_text = _extract_pdf_text_if_needed(destination_path)

	return {
		"filename": file.filename,
		"content_type": file.content_type or "application/octet-stream",
		"size_bytes": counting_writer.bytes_written,
		"extracted_text": extracted_text,
		"message": "File uploaded successfully.",
	}

