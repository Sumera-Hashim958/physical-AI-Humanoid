"""
Translation router for Urdu translation with caching.
Provides chapter translation using Claude AI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.translate import TranslateRequest, TranslateResponse
from app.models.user import User
from app.routers.auth import get_current_user
from app.services.claude_service import ClaudeService
from app.services.db_service import DBService
import time


# Create router
router = APIRouter()


@router.post("/chapter", response_model=TranslateResponse)
async def translate_chapter(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Translate chapter content to Urdu (educational style).

    **Flow:**
    1. Check cache for (chapter_id, language) pair
    2. If cached, return cached translation (fast!)
    3. If not cached, call Claude API to translate
    4. Save to cache for all users to share
    5. Return translated content

    **Authentication:** Requires valid JWT token

    **Rate Limit:** 5 translations/day per user (TODO: implement)

    **Caching:** Translations are shared across all users (language-specific, not user-specific)

    Args:
        request: Chapter ID, content, and target language
        current_user: Authenticated user (from JWT token)

    Returns:
        TranslateResponse: Translated content with metadata

    Raises:
        HTTPException: 500 if services unavailable

    Example Request:
        POST /api/translate/chapter
        Headers:
            Authorization: Bearer <jwt_token>
        Body:
            {
                "chapter_id": "chapter-3-cnns",
                "chapter_content": "CNNs are neural networks specialized for image processing...",
                "target_language": "ur"
            }

    Example Response (200 OK):
        {
            "chapter_id": "chapter-3-cnns",
            "language": "ur",
            "translated_content": "CNNs ایک خاص قسم کے neural networks ہیں جو تصویروں کی پروسیسنگ کے لیے بنائے گئے ہیں...",
            "cached": false,
            "tokens_used": 1200,
            "response_time": 2.5
        }

    Example Response (Cached):
        {
            "chapter_id": "chapter-3-cnns",
            "language": "ur",
            "translated_content": "CNNs ایک خاص قسم کے neural networks ہیں...",
            "cached": true,
            "tokens_used": 0,
            "response_time": 0.03
        }
    """
    start_time = time.time()

    try:
        # Step 1: Check cache
        cached_translation = await DBService.get_translation(
            chapter_id=request.chapter_id,
            language=request.target_language
        )

        if cached_translation:
            # Cache hit! Return immediately
            return TranslateResponse(
                chapter_id=request.chapter_id,
                language=request.target_language,
                translated_content=cached_translation,
                cached=True,
                tokens_used=0,
                response_time=time.time() - start_time
            )

        # Step 2: Cache miss - call Claude API
        result = await ClaudeService.translate_to_urdu(
            chapter_content=request.chapter_content,
            max_tokens=3000
        )

        # Step 3: Save to cache (shared across all users)
        await DBService.save_translation(
            chapter_id=request.chapter_id,
            language=request.target_language,
            translated_content=result["translated_content"]
        )

        # Step 4: Return response
        return TranslateResponse(
            chapter_id=request.chapter_id,
            language=request.target_language,
            translated_content=result["translated_content"],
            cached=False,
            tokens_used=result["tokens_used"],
            response_time=time.time() - start_time
        )

    except ValueError as e:
        # Claude API not configured
        return TranslateResponse(
            chapter_id=request.chapter_id,
            language=request.target_language,
            translated_content=f"⚠️ {str(e)}",
            cached=False,
            tokens_used=0,
            response_time=time.time() - start_time
        )
    except Exception as e:
        print(f"[ERROR] Translate endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to translate content: {str(e)}"
        )


@router.get("/cache/{chapter_id}/{language}", response_model=TranslateResponse | None)
async def get_cached_translation(
    chapter_id: str,
    language: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get cached translation for a chapter (if exists).

    Args:
        chapter_id: Chapter identifier
        language: Target language code
        current_user: Authenticated user

    Returns:
        TranslateResponse if cached, None if not cached

    Example Request:
        GET /api/translate/cache/chapter-3-cnns/ur
        Headers:
            Authorization: Bearer <jwt_token>
    """
    start_time = time.time()

    cached_translation = await DBService.get_translation(
        chapter_id=chapter_id,
        language=language
    )

    if cached_translation:
        return TranslateResponse(
            chapter_id=chapter_id,
            language=language,
            translated_content=cached_translation,
            cached=True,
            tokens_used=0,
            response_time=time.time() - start_time
        )

    return None
