"""LoanSense AI backend entry point.

This module starts a FastAPI application with a simple health endpoint
that frontend and deployment checks can call.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.application import router as application_router

app = FastAPI(
    title="LoanSense AI API",
    version="0.1.0",
    description="AI-Powered Loan Eligibility and Risk Assessment backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(application_router)


@app.get("/", tags=["System"])
def root() -> dict[str, str]:
    """Root endpoint for quick health checks."""
    return {"status": "ok", "service": "loansense-backend"}
