"""Pydantic models related to loan applications."""

from pydantic import BaseModel, EmailStr, Field


class LoanApplication(BaseModel):
    """Input model for a loan application request."""

    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    monthly_income: float = Field(..., gt=0)
    loan_amount: float = Field(..., gt=0)
    loan_purpose: str = Field(..., min_length=3, max_length=200)
    status: str = Field(default="Pending")
