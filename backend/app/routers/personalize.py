"""
Personalization router for adapting content to user's level.
Provides content personalization using Claude AI with caching.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.personalize import PersonalizeRequest, PersonalizeResponse
from app.models.user import User
from app.routers.auth import get_current_user
from app.services.claude_service import ClaudeService
from app.services.db_service import DBService
import time


# Create router
router = APIRouter()


@router.post("/chapter", response_model=PersonalizeResponse)
async def personalize_chapter(
    request: PersonalizeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Personalize chapter content based on user's programming level.

    **Flow:**
    1. Check cache for (chapter_id, user_level) pair
    2. If cached, return cached content (fast!)
    3. If not cached, call Claude API to personalize
    4. Save to cache for future requests
    5. Return personalized content

    **Authentication:** Requires valid JWT token

    **Rate Limit:** 5 personalizations/day per user (TODO: implement)

    Args:
        request: Chapter ID and content to personalize
        current_user: Authenticated user (from JWT token)

    Returns:
        PersonalizeResponse: Personalized content with metadata

    Raises:
        HTTPException: 500 if services unavailable

    Example Request:
        POST /api/personalize/chapter
        Headers:
            Authorization: Bearer <jwt_token>
        Body:
            {
                "chapter_id": "chapter-3-cnns",
                "chapter_content": "CNNs are neural networks specialized for image processing..."
            }

    Example Response (200 OK):
        {
            "chapter_id": "chapter-3-cnns",
            "user_level": "beginner",
            "personalized_content": "Let's learn about CNNs in simple terms! CNNs (Convolutional Neural Networks) are a special type of neural network...",
            "cached": false,
            "tokens_used": 850,
            "response_time": 2.1
        }

    Example Response (Cached):
        {
            "chapter_id": "chapter-3-cnns",
            "user_level": "beginner",
            "personalized_content": "Let's learn about CNNs in simple terms...",
            "cached": true,
            "tokens_used": 0,
            "response_time": 0.05
        }
    """
    start_time = time.time()

    try:
        user_level = current_user.programming_level

        # Step 1: Check cache
        cached_content = await DBService.get_personalized_content(
            chapter_id=request.chapter_id,
            user_level=user_level
        )

        if cached_content:
            # Cache hit! Return immediately
            return PersonalizeResponse(
                chapter_id=request.chapter_id,
                user_level=user_level,
                personalized_content=cached_content,
                cached=True,
                tokens_used=0,
                response_time=time.time() - start_time
            )

        # Step 2: Cache miss - call Claude API
        result = await ClaudeService.personalize_chapter(
            chapter_content=request.chapter_content,
            user_level=user_level,
            max_tokens=2000
        )

        # Step 3: Save to cache
        await DBService.save_personalized_content(
            chapter_id=request.chapter_id,
            user_level=user_level,
            personalized_content=result["personalized_content"]
        )

        # Step 4: Return response
        return PersonalizeResponse(
            chapter_id=request.chapter_id,
            user_level=user_level,
            personalized_content=result["personalized_content"],
            cached=False,
            tokens_used=result["tokens_used"],
            response_time=time.time() - start_time
        )

    except ValueError as e:
        # Claude API not configured
        return PersonalizeResponse(
            chapter_id=request.chapter_id,
            user_level=current_user.programming_level,
            personalized_content=f"⚠️ {str(e)}",
            cached=False,
            tokens_used=0,
            response_time=time.time() - start_time
        )
    except Exception as e:
        print(f"[ERROR] Personalize endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to personalize content: {str(e)}"
        )


@router.get("/cache/{chapter_id}", response_model=PersonalizeResponse | None)
async def get_cached_personalization(
    chapter_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get cached personalized content for a chapter (if exists).

    Args:
        chapter_id: Chapter identifier
        current_user: Authenticated user

    Returns:
        PersonalizeResponse if cached, None if not cached

    Example Request:
        GET /api/personalize/cache/chapter-3-cnns
        Headers:
            Authorization: Bearer <jwt_token>
    """
    start_time = time.time()
    user_level = current_user.programming_level

    cached_content = await DBService.get_personalized_content(
        chapter_id=chapter_id,
        user_level=user_level
    )

    if cached_content:
        return PersonalizeResponse(
            chapter_id=chapter_id,
            user_level=user_level,
            personalized_content=cached_content,
            cached=True,
            tokens_used=0,
            response_time=time.time() - start_time
        )

    return None
