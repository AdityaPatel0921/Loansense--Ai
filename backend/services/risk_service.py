"""Financial risk engine for LoanSense AI."""


def calculate_risk(application_data: dict, ai_analysis: dict) -> dict:
    """
    Calculates DTI, EMI, and final risk decision based on Gemini analysis.
    Logic for Cognizant Hackathon 2025.
    """
    # 1. Inputs extract karo
    monthly_income = application_data.get("monthly_income", 0)
    loan_amount = application_data.get("loan_amount", 0)
    # Gemini analysis response wrapped as per document [cite: 168]
    gemini_risk = ai_analysis.get("analysis", {}).get("risk_score", "High")

    # 2. Debt-to-Income (DTI) Calculation [cite: 131]
    annual_income = monthly_income * 12
    dti_ratio = loan_amount / annual_income if annual_income > 0 else 1.0

    # 3. Suggested EMI Calculation (8.5% interest, 5 years) [cite: 134]
    r = 8.5 / (12 * 100) # Monthly interest rate
    n = 5 * 12           # Tenure in months
    emi = (loan_amount * r * (1 + r)**n) / ((1 + r)**n - 1) if loan_amount > 0 else 0

    # 4. Final Risk Logic & Decision [cite: 137]
    final_risk_level = "High"
    decision = "Rejected"

    if dti_ratio < 0.3 and gemini_risk == "Low":
        final_risk_level = "Low"
        decision = "Approved"
    elif 0.3 <= dti_ratio <= 0.5 or gemini_risk == "Med":
        final_risk_level = "Medium"
        decision = "Manual Review"
    else:
        final_risk_level = "High"
        decision = "Rejected"

    return {
        "final_risk_level": final_risk_level,
        "risk_score_percent": round(dti_ratio * 100, 2),
        "suggested_emi": round(emi, 2),
        "decision": decision,
        "dti_ratio": round(dti_ratio, 4)
    }
