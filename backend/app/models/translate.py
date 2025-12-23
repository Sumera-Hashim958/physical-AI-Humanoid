"""
Pydantic models for translation functionality.
"""

from pydantic import BaseModel, Field
from typing import Literal


class TranslateRequest(BaseModel):
    """
    Request model for translation endpoint.

    Attributes:
        chapter_id: Chapter identifier to translate
        chapter_content: Original chapter content (English)
        target_language: Target language code (currently only 'ur' for Urdu)

    Example:
        {
            "chapter_id": "chapter-3-cnns",
            "chapter_content": "CNNs are neural networks...",
            "target_language": "ur"
        }
    """
    chapter_id: str = Field(..., min_length=1, max_length=200, description="Chapter ID")
    chapter_content: str = Field(..., min_length=10, max_length=50000, description="Chapter content to translate")
    target_language: Literal["ur"] = Field("ur", description="Target language (only Urdu supported)")


class TranslateResponse(BaseModel):
    """
    Response model for translation endpoint.

    Attributes:
        chapter_id: Chapter identifier
        language: Target language code
        translated_content: Translated content
        cached: Whether result was from cache
        tokens_used: Claude API tokens consumed (0 if cached)
        response_time: Time taken to generate response

    Example:
        {
            "chapter_id": "chapter-3-cnns",
            "language": "ur",
            "translated_content": "CNNs ایک قسم کے neural networks ہیں...",
            "cached": false,
            "tokens_used": 1200,
            "response_time": 2.5
        }
    """
    chapter_id: str
    language: str
    translated_content: str
    cached: bool = False
    tokens_used: int = 0
    response_time: float
