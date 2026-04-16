"""PDF-related service functions."""

from io import BytesIO

import pdfplumber


async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF document using pdfplumber."""
    if not file_content:
        raise ValueError("Uploaded PDF is empty")

    extracted_pages: list[str] = []
    with pdfplumber.open(BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            extracted_pages.append(page.extract_text() or "")

    extracted_text = "\n".join(extracted_pages).strip()
    if not extracted_text:
        raise ValueError("No readable text found in PDF")
    return extracted_text
