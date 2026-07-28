"""Utilities for extracting structured complaint information using Groq."""

from __future__ import annotations

import json
from typing import Any

from groq import Groq

from app.ai.prompts import COMPLAINT_EXTRACTION_PROMPT
from app.core.config import settings

_groq_client = Groq(api_key=settings.groq_api_key)


def extract_complaint_information(
    complaint_text: str,
) -> dict[str, Any]:
    """Extract structured complaint information from free-form complaint text.

    The complaint text is sent to the configured Groq model together with
    the extraction prompt. The model is expected to return valid JSON,
    which is parsed into a Python dictionary.

    Args:
        complaint_text: Raw complaint text extracted from a document.

    Returns:
        A dictionary containing the extracted complaint fields.

    Raises:
        RuntimeError:
            If the Groq request fails or the model returns invalid JSON.
    """

    try:
        response = _groq_client.chat.completions.create(
            model=settings.groq_model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": COMPLAINT_EXTRACTION_PROMPT,
                },
                {
                    "role": "user",
                    "content": complaint_text,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("Groq returned an empty response.")

        return json.loads(content)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Groq returned invalid JSON."
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            "Failed to extract complaint information from Groq."
        ) from exc