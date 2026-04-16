"""AI service functions for Gemini integration."""

import asyncio
import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


async def _get_gemini_model() -> genai.GenerativeModel:
    """Build Gemini model from environment configuration."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are a Senior Credit Underwriter. Analyze borrower and loan document text "
            "for credit risk and affordability. You must respond with STRICT JSON only. "
            "Do not include markdown, explanations, or extra keys."
        ),
    )


async def _validate_analysis_payload(payload: dict) -> dict:
    """Validate required analysis fields and allowed enum values."""
    required_keys = {"risk_score", "decision", "reason", "suggested_amount"}
    missing_keys = required_keys.difference(payload.keys())
    if missing_keys:
        raise ValueError(f"Gemini response missing keys: {sorted(missing_keys)}")

    if payload["risk_score"] not in {"Low", "Med", "High"}:
        raise ValueError("risk_score must be one of: Low, Med, High")

    if payload["decision"] not in {"Approved", "Rejected"}:
        raise ValueError("decision must be one of: Approved, Rejected")

    return payload


async def analyze_loan_document(text: str) -> dict:
    """Analyze extracted loan document text with Gemini and return strict JSON."""
    if not text.strip():
        raise ValueError("Document text is empty")

    model = await _get_gemini_model()
    prompt = (
        "Analyze the following extracted loan application text and return STRICT JSON only with this exact schema:\n"
        "{\n"
        '  "risk_score": "Low|Med|High",\n'
        '  "decision": "Approved|Rejected",\n'
        '  "reason": "short explanation",\n'
        '  "suggested_amount": 0\n'
        "}\n\n"
        "Rules:\n"
        "- Output must be valid JSON object only.\n"
        "- No markdown code fences.\n"
        "- No additional keys.\n\n"
        f"Document Text:\n{text}"
    )

    try:
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 500,
                "response_mime_type": "application/json",
            },
        )
    except Exception as exc:
        raise ValueError(f"Gemini request failed: {exc}") from exc

    response_text = (getattr(response, "text", "") or "").strip()
    if not response_text:
        raise ValueError("Gemini returned an empty response")

    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini returned non-JSON output: {response_text}") from exc

    validated = await _validate_analysis_payload(parsed)
    return {
        "model": "gemini-1.5-flash",
        "analysis": validated,
    }
