"""
Pydantic models for chat/Q&A functionality.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    """
    Request model for chat/question endpoint.

    Attributes:
        question: User's question text
        selected_text: Optional pre-selected text from textbook for context

    Example:
        {
            "question": "What is a CNN?",
            "selected_text": null
        }
    """
    question: str = Field(..., min_length=3, max_length=1000, description="User's question")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Selected text from textbook")


class Source(BaseModel):
    """
    Source citation for an answer.

    Attributes:
        chapter_id: Chapter identifier (e.g., "chapter-3-cnns")
        section: Section name (e.g., "Introduction")
        similarity: Similarity score (0-1, from vector search)

    Example:
        {
            "chapter_id": "chapter-3-cnns",
            "section": "Architecture",
            "similarity": 0.92
        }
    """
    chapter_id: str
    section: str
    similarity: float = Field(..., ge=0.0, le=1.0, description="Similarity score 0-1")


class ChatResponse(BaseModel):
    """
    Response model for chat/question endpoint.

    Attributes:
        answer: AI-generated answer text
        sources: List of source citations used
        response_time: Time taken to generate response (seconds)
        tokens_used: Number of Claude API tokens consumed

    Example:
        {
            "answer": "CNNs are neural networks specialized for image processing...",
            "sources": [{
                "chapter_id": "chapter-3-cnns",
                "section": "Introduction",
                "similarity": 0.92
            }],
            "response_time": 1.2,
            "tokens_used": 450
        }
    """
    answer: str
    sources: List[Source] = []
    response_time: float
    tokens_used: int = 0
