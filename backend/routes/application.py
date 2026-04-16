"""Routes for loan application workflows."""

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from database.db import get_database
from models.loan import LoanApplication
from services.ai_service import analyze_loan_document
from services.pdf_service import extract_text_from_pdf
from services import risk_service

router = APIRouter(tags=["Application"])


def _serialize_application_document(document: dict[str, Any]) -> dict[str, Any]:
    """Convert MongoDB documents into JSON-safe objects."""
    serialized_document = dict(document)
    if "_id" in serialized_document:
        serialized_document["_id"] = str(serialized_document["_id"])
    if "created_at" in serialized_document and serialized_document["created_at"] is not None:
        serialized_document["created_at"] = serialized_document["created_at"].isoformat()
    return serialized_document


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

    try:
        file_content = await document.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {exc}") from exc
    finally:
        await document.close()

    if not file_content:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty")

    try:
        extracted_text = await extract_text_from_pdf(file_content)
        ai_analysis = await analyze_loan_document(extracted_text)
        risk_result = risk_service.calculate_risk(application.model_dump(), ai_analysis)
        database = get_database()
        application_record = {
            "user_data": application.model_dump(),
            "ai_analysis": ai_analysis,
            "risk_result": risk_result,
            "status": risk_result["decision"],
            "document_name": document.filename,
            "created_at": datetime.now(timezone.utc),
        }
        insert_result = await database["applications"].insert_one(application_record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc

    return {
        "message": "Loan application processed successfully",
        "application": application.model_dump(),
        "document_name": document.filename,
        "ai_analysis": ai_analysis,
        "risk_result": risk_result,
        "saved": True,
        "application_id": str(insert_result.inserted_id),
    }


@router.get("/applications")
async def list_applications() -> dict[str, list[dict[str, Any]]]:
    """Return all saved loan applications."""
    try:
        database = get_database()
        cursor = database["applications"].find().sort("created_at", -1)
        applications: list[dict[str, Any]] = []

        async for application_document in cursor:
            applications.append(_serialize_application_document(application_document))

        return {"applications": applications}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load applications: {exc}") from exc


@router.get("/{application_id}")
async def get_application_by_id(application_id: str) -> dict[str, Any]:
    """Return one saved application by MongoDB ObjectId."""
    database = get_database()
    try:
        application_document = await database["applications"].find_one({"_id": ObjectId(application_id)})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid application ID format: {exc}") from exc

    if not application_document:
        raise HTTPException(status_code=404, detail="Application not found")

    return _serialize_application_document(application_document)
