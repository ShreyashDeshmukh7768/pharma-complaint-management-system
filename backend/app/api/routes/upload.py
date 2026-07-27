"""File upload routes.

This router is intentionally limited to receiving a file from the client,
persisting it to the local uploads directory, and returning basic metadata.
No AI processing, database access, or file content extraction belongs here.
"""

from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile, status

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


# ---------------------------------------------------------------------------
# Upload Endpoint
# ---------------------------------------------------------------------------
@router.post(
	"/",
	status_code=status.HTTP_201_CREATED,
	summary="Upload a file",
)
def upload_file(file: UploadFile = File(...)) -> dict[str, str | int]:
	"""Save an uploaded file to the local uploads directory.

	The file is stored using the original filename provided by the client.
	The response includes basic file metadata for confirmation.
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

	return {
		"filename": file.filename,
		"content_type": file.content_type or "application/octet-stream",
		"size_bytes": counting_writer.bytes_written,
		"message": "File uploaded successfully.",
	}

