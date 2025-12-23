"""
Chat router for RAG Q&A functionality.
Provides question answering using Qdrant vector search + Claude AI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.chat import ChatRequest, ChatResponse, Source
from app.models.user import User
from app.routers.auth import get_current_user
from app.services.qdrant_service import QdrantService
from app.services.claude_service import ClaudeService
from app.services.db_service import DBService
import json


# Create router
router = APIRouter()


@router.post("/question", response_model=ChatResponse)
async def ask_question(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Ask a question and get an AI-generated answer using RAG.

    **Flow:**
    1. Search Qdrant for relevant textbook chunks
    2. Send chunks + question to Claude API
    3. Get grounded answer with citations
    4. Save to chat_history table
    5. Return response to user

    **Authentication:** Requires valid JWT token

    **Rate Limit:** 20 questions/hour per user (TODO: implement)

    Args:
        request: Question and optional selected text
        current_user: Authenticated user (from JWT token)

    Returns:
        ChatResponse: Answer with sources and metadata

    Raises:
        HTTPException: 500 if services unavailable

    Example Request:
        POST /api/chat/question
        Headers:
            Authorization: Bearer <jwt_token>
        Body:
            {
                "question": "What is a CNN?",
                "selected_text": null
            }

    Example Response (200 OK):
        {
            "answer": "CNNs (Convolutional Neural Networks) are...",
            "sources": [
                {
                    "chapter_id": "chapter-3-cnns",
                    "section": "Introduction",
                    "similarity": 0.92
                }
            ],
            "response_time": 1.2,
            "tokens_used": 450
        }

    Example Response (Claude API not configured):
        {
            "answer": "⚠️ Claude API not configured: ANTHROPIC_API_KEY not set...",
            "sources": [],
            "response_time": 0.01,
            "tokens_used": 0
        }
    """
    try:
        # Step 1: Search Qdrant for relevant chunks
        # TODO: For MVP, this returns empty until we have embeddings
        # In production: embed question + search Qdrant
        context_chunks = await QdrantService.search_similar_chunks(
            question=request.question,
            top_k=5,
            score_threshold=0.7
        )

        # Step 2: Get answer from Claude
        result = await ClaudeService.answer_question(
            question=request.question,
            context_chunks=context_chunks,
            max_tokens=1000
        )

        # Step 3: Save to chat history
        sources_json = json.dumps(result["sources"]) if result["sources"] else json.dumps([])

        await DBService.save_chat_history(
            user_id=current_user.id,
            question=request.question,
            answer=result["answer"],
            sources=sources_json
        )

        # Step 4: Return response
        return ChatResponse(
            answer=result["answer"],
            sources=[Source(**src) for src in result["sources"]],
            response_time=result["response_time"],
            tokens_used=result["tokens_used"]
        )

    except ValueError as e:
        # Claude API not configured - return helpful error
        return ChatResponse(
            answer=f"⚠️ {str(e)}",
            sources=[],
            response_time=0.0,
            tokens_used=0
        )
    except Exception as e:
        print(f"[ERROR] Chat endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process question: {str(e)}"
        )


@router.get("/history", response_model=list)
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    limit: int = 20
):
    """
    Get user's chat history (recent questions and answers).

    Args:
        current_user: Authenticated user (from JWT token)
        limit: Number of recent chats to return (default: 20, max: 100)

    Returns:
        List of chat history entries

    Example Request:
        GET /api/chat/history?limit=10
        Headers:
            Authorization: Bearer <jwt_token>

    Example Response (200 OK):
        [
            {
                "id": 1,
                "question": "What is a CNN?",
                "answer": "CNNs are neural networks...",
                "sources": [{...}],
                "created_at": "2025-12-23T10:30:00"
            },
            ...
        ]
    """
    # Limit to max 100
    limit = min(limit, 100)

    try:
        history = await DBService.get_chat_history(
            user_id=current_user.id,
            limit=limit
        )
        return history
    except Exception as e:
        print(f"[ERROR] Failed to get chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat history"
        )
