"""AI service functions for Claude integration."""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def _get_claude_client() -> Anthropic:
    """Build Anthropic client from environment configuration."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in environment variables")
    return Anthropic(api_key=api_key)


async def analyze_loan_document(text: str) -> dict:
    """Analyze extracted loan document text with Claude."""
    if not text.strip():
        raise ValueError("Document text is empty")

    client = _get_claude_client()
    prompt = (
        "You are a loan risk analysis assistant. "
        "Review the following extracted loan application text and return concise JSON with keys "
        "risk_level, summary, and recommendation.\n\n"
        f"Document Text:\n{text}"
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=700,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    response_text = ""
    if message.content:
        first_block = message.content[0]
        response_text = getattr(first_block, "text", "")

    return {
        "model": "claude-3-5-sonnet-latest",
        "analysis": response_text,
    }


async def analyze_with_claude(prompt: str) -> dict:
    """Analyze application data with Claude.

    TODO: Implement Anthropic API integration.
    """
    _ = prompt
    pass
