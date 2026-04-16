"""MongoDB connection utilities for LoanSense AI."""

import os
from typing import Optional

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

load_dotenv()

MONGODB_URL = (os.getenv("MONGODB_URL") or "").strip()
DATABASE_NAME = (os.getenv("MONGODB_DB_NAME", "loansense_ai") or "loansense_ai").strip()

_client: Optional[AsyncIOMotorClient] = None


def get_client() -> AsyncIOMotorClient:
    """Return a shared MongoDB client instance."""
    global _client
    if _client is None:
        if not MONGODB_URL:
            raise ValueError("MONGODB_URL is not set in environment variables")
        _client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    """Return the app database instance from the shared client."""
    return get_client()[DATABASE_NAME]
