"""Reusable PDF text extraction helpers.

This module is intentionally independent from FastAPI and SQLAlchemy so it can
be reused by services, scripts, or background jobs.
"""

from pathlib import Path

import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: Path) -> str:
	"""Extract and return all readable text from a PDF file.

	The PDF is opened with PyMuPDF, every page is read in order, and the page
	text is joined with a newline separator. Leading/trailing whitespace and
	blank page output are removed before returning the final text.

	Args:
		file_path: Path to the PDF file on disk.

	Returns:
		The combined extracted text from all pages.

	Raises:
		FileNotFoundError: If the file does not exist.
		ValueError: If the PDF has no extractable text.
	"""
	

	if not file_path.exists():
		raise FileNotFoundError(f"PDF file not found: {file_path}")
	
    

	page_texts: list[str] = []

	with fitz.open(file_path) as pdf_document:
		for page in pdf_document:
			text = page.get_text("text").strip()
			if text:
				page_texts.append(text)

	if not page_texts:
		raise ValueError(f"No extractable text found in PDF: {file_path}")

	return "\n".join(page_texts).strip()

