"""Routes for loan application workflows."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.loan import LoanApplication
from services.ai_service import analyze_loan_document
from services.pdf_service import extract_text_from_pdf

router = APIRouter(tags=["Application"])


@router.post("/apply")
async def create_application(
    full_name: str = Form(...),
    email: str = Form(...),
    monthly_income: float = Form(...),
    loan_amount: float = Form(...),
    loan_purpose: str = Form(...),
    document: UploadFile = File(...),
) -> dict:
    """Accept loan application form-data and analyze uploaded PDF document."""
    if document.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        application = LoanApplication(
            full_name=full_name,
            email=email,
            monthly_income=monthly_income,
            loan_amount=loan_amount,
            loan_purpose=loan_purpose,
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid form data: {exc}") from exc

    file_content = await document.read()
    if not file_content:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty")

    try:
        extracted_text = await extract_text_from_pdf(file_content)
        ai_analysis = await analyze_loan_document(extracted_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc

    return {
        "message": "Loan application processed successfully",
        "application": application.model_dump(),
        "document_name": document.filename,
        "analysis": ai_analysis,
    }
