"""Utilities for extracting and analyzing pharmaceutical complaints using Groq."""

from __future__ import annotations

import json
from typing import Any

from groq import Groq

from app.ai.prompts import (
    COMPLAINT_EXTRACTION_PROMPT,
    RISK_ASSESSMENT_PROMPT,
)
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


def analyze_complaint(
    complaint_data: dict[str, Any],
) -> dict[str, Any]:
    """Analyze an extracted pharmaceutical complaint.

    The structured complaint information is sent to the configured Groq
    model together with the risk assessment prompt. The model returns
    structured JSON containing a summary, risk level, confidence score,
    and recommended actions.

    Args:
        complaint_data: Structured complaint information extracted by the AI.

    Returns:
        A dictionary containing the AI risk assessment.

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
                    "content": RISK_ASSESSMENT_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        complaint_data,
                        indent=2,
                    ),
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
            "Failed to analyze complaint."
        ) from exc