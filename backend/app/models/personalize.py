"""
Pydantic models for content personalization.
"""

from pydantic import BaseModel, Field


class PersonalizeRequest(BaseModel):
    """
    Request model for personalization endpoint.

    Attributes:
        chapter_id: Chapter identifier to personalize
        chapter_content: Original chapter content (optional if using cached)

    Example:
        {
            "chapter_id": "chapter-3-cnns",
            "chapter_content": "CNNs are neural networks..."
        }
    """
    chapter_id: str = Field(..., min_length=1, max_length=200, description="Chapter ID")
    chapter_content: str = Field(..., min_length=10, max_length=50000, description="Chapter content to personalize")


class PersonalizeResponse(BaseModel):
    """
    Response model for personalization endpoint.

    Attributes:
        chapter_id: Chapter identifier
        user_level: User's programming level
        personalized_content: Content adapted for user's level
        cached: Whether result was from cache
        tokens_used: Claude API tokens consumed (0 if cached)
        response_time: Time taken to generate response

    Example:
        {
            "chapter_id": "chapter-3-cnns",
            "user_level": "beginner",
            "personalized_content": "Let's learn about CNNs in simple terms...",
            "cached": false,
            "tokens_used": 850,
            "response_time": 2.1
        }
    """
    chapter_id: str
    user_level: str
    personalized_content: str
    cached: bool = False
    tokens_used: int = 0
    response_time: float
