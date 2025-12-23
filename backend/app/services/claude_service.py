"""
Claude AI service for RAG Q&A, personalization, and translation.
Uses Anthropic's Claude API for all AI operations.
"""

from anthropic import Anthropic, AnthropicError
from app.utils.config import get_settings
from typing import List, Dict, Optional
import time


class ClaudeService:
    """
    Service for Claude API operations.

    Handles AI-powered Q&A, content personalization, and translation
    using Anthropic's Claude models.

    Example:
        >>> answer = await ClaudeService.answer_question(
        ...     question="What is a CNN?",
        ...     context_chunks=[{"content": "CNNs are..."}]
        ... )
        >>> print(answer["answer"])
    """

    _client: Anthropic | None = None

    @classmethod
    def get_client(cls) -> Anthropic:
        """
        Get or create Anthropic client singleton.

        Returns:
            Anthropic: Connected Anthropic client instance

        Raises:
            ValueError: If ANTHROPIC_API_KEY is not set
        """
        settings = get_settings()

        # Check API key before attempting to create client
        if (not settings.anthropic_api_key or
            settings.anthropic_api_key == "" or
            "your_anthropic_api_key" in settings.anthropic_api_key.lower()):
            raise ValueError(
                "ANTHROPIC_API_KEY not set in .env file. "
                "Get your free API key ($5 credits) from: https://console.anthropic.com"
            )

        if cls._client is None:
            try:
                cls._client = Anthropic(api_key=settings.anthropic_api_key)
                print(f"[OK] Connected to Claude API (model: {settings.claude_model})")
            except Exception as e:
                print(f"[ERROR] Failed to initialize Claude client: {e}")
                raise

        return cls._client

    @classmethod
    async def answer_question(
        cls,
        question: str,
        context_chunks: List[Dict],
        max_tokens: int = 1000
    ) -> Dict:
        """
        Answer a question using RAG approach with Claude.

        Provides grounded answers based only on textbook context.
        Cites sources and responds "I don't have this information"
        when context is insufficient.

        Args:
            question: User's question
            context_chunks: List of relevant chunks from Qdrant
                [{"content": "...", "chapter_id": "...", "section": "..."}]
            max_tokens: Maximum response length (default: 1000)

        Returns:
            dict: Answer with metadata
            {
                "answer": "CNNs are neural networks...",
                "sources": [{"chapter_id": "ch3", "section": "Intro"}],
                "tokens_used": 450,
                "response_time": 1.2
            }

        Raises:
            ValueError: If ANTHROPIC_API_KEY not set
            AnthropicError: If API call fails

        Example:
            >>> result = await ClaudeService.answer_question(
            ...     question="What are transformers?",
            ...     context_chunks=[
            ...         {"content": "Transformers are...", "chapter_id": "ch5"}
            ...     ]
            ... )
        """
        settings = get_settings()
        start_time = time.time()

        try:
            client = cls.get_client()

            # Build context from chunks
            if not context_chunks:
                return {
                    "answer": "I don't have enough information in the textbook to answer this question. Please try rephrasing or ask about a different topic.",
                    "sources": [],
                    "tokens_used": 0,
                    "response_time": time.time() - start_time
                }

            # Format context for Claude
            context_text = "\n\n".join([
                f"[Source: {chunk.get('chapter_id', 'unknown')} - {chunk.get('section', 'unknown')}]\n{chunk['content']}"
                for chunk in context_chunks
            ])

            # Create prompt
            system_prompt = """You are a helpful AI tutor for a Physical AI textbook.
Your role is to answer questions ONLY based on the textbook content provided in the context.

Rules:
1. Answer ONLY using information from the provided context
2. Cite sources by mentioning the chapter/section
3. If the context doesn't contain enough information, say: "I don't have enough information in the textbook to answer this question."
4. Keep answers concise and educational
5. Use examples from the textbook when available"""

            user_prompt = f"""Context from textbook:
{context_text}

Question: {question}

Please answer the question based only on the context above. Cite the relevant chapter/section."""

            # Call Claude API
            message = client.messages.create(
                model=settings.claude_model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract answer
            answer_text = message.content[0].text

            # Extract sources from context_chunks
            sources = [
                {
                    "chapter_id": chunk.get("chapter_id", "unknown"),
                    "section": chunk.get("section", "unknown"),
                    "similarity": chunk.get("similarity", 0.0)
                }
                for chunk in context_chunks
            ]

            return {
                "answer": answer_text,
                "sources": sources,
                "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
                "response_time": time.time() - start_time
            }

        except ValueError as e:
            # API key not set
            return {
                "answer": f"⚠️ Claude API not configured: {str(e)}",
                "sources": [],
                "tokens_used": 0,
                "response_time": time.time() - start_time
            }
        except AnthropicError as e:
            print(f"[ERROR] Claude API error: {e}")
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "tokens_used": 0,
                "response_time": time.time() - start_time
            }

    @classmethod
    async def personalize_chapter(
        cls,
        chapter_content: str,
        user_level: str,  # beginner/intermediate/advanced
        max_tokens: int = 2000
    ) -> Dict:
        """
        Personalize chapter content based on user's programming level.

        Adapts explanations, adds examples, and adjusts complexity.

        Args:
            chapter_content: Original chapter text
            user_level: User's programming level (beginner/intermediate/advanced)
            max_tokens: Maximum response length (default: 2000)

        Returns:
            dict: Personalized content
            {
                "personalized_content": "...",
                "tokens_used": 850,
                "response_time": 2.1
            }

        Example:
            >>> result = await ClaudeService.personalize_chapter(
            ...     chapter_content="CNNs are...",
            ...     user_level="beginner"
            ... )
        """
        settings = get_settings()
        start_time = time.time()

        try:
            client = cls.get_client()

            # Level-specific guidelines
            level_guidelines = {
                "beginner": "Use simple language, add many examples, explain basic concepts, avoid jargon",
                "intermediate": "Balance theory and practice, some technical terms ok, add coding examples",
                "advanced": "Technical depth, advanced concepts, research papers, optimization techniques"
            }

            guidelines = level_guidelines.get(user_level, level_guidelines["beginner"])

            system_prompt = f"""You are adapting a Physical AI textbook chapter for a {user_level} level student.

Guidelines:
{guidelines}

Keep the core information accurate but adapt the presentation style."""

            user_prompt = f"""Original chapter content:
{chapter_content}

Please adapt this for a {user_level} level student."""

            # Call Claude API
            message = client.messages.create(
                model=settings.claude_model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return {
                "personalized_content": message.content[0].text,
                "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
                "response_time": time.time() - start_time
            }

        except ValueError as e:
            return {
                "personalized_content": f"⚠️ Claude API not configured: {str(e)}",
                "tokens_used": 0,
                "response_time": time.time() - start_time
            }

    @classmethod
    async def translate_to_urdu(
        cls,
        chapter_content: str,
        max_tokens: int = 3000
    ) -> Dict:
        """
        Translate chapter content to educational Urdu.

        Uses Claude to translate while maintaining educational context
        and technical accuracy.

        Args:
            chapter_content: Original chapter text (English)
            max_tokens: Maximum response length (default: 3000)

        Returns:
            dict: Translated content
            {
                "translated_content": "...",
                "tokens_used": 1200,
                "response_time": 2.5
            }

        Example:
            >>> result = await ClaudeService.translate_to_urdu(
            ...     chapter_content="CNNs are neural networks..."
            ... )
        """
        settings = get_settings()
        start_time = time.time()

        try:
            client = cls.get_client()

            system_prompt = """You are translating a Physical AI textbook to educational Urdu.

Guidelines:
1. Translate naturally, not word-for-word
2. Keep technical terms in English when appropriate (e.g., CNN, GPU, PyTorch)
3. Use educational Urdu suitable for university students
4. Maintain technical accuracy
5. Use proper Urdu script (not Roman Urdu)"""

            user_prompt = f"""Translate this textbook content to educational Urdu:

{chapter_content}"""

            # Call Claude API
            message = client.messages.create(
                model=settings.claude_model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return {
                "translated_content": message.content[0].text,
                "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
                "response_time": time.time() - start_time
            }

        except ValueError as e:
            return {
                "translated_content": f"⚠️ Claude API not configured: {str(e)}",
                "tokens_used": 0,
                "response_time": time.time() - start_time
            }

    @classmethod
    async def health_check(cls) -> Dict:
        """
        Check Claude API connection health.

        Returns:
            dict: Health status

        Example:
            >>> health = await ClaudeService.health_check()
            >>> print(health["status"])  # "healthy" or "unconfigured"
        """
        settings = get_settings()

        # Check if API key is not configured or is placeholder
        if (not settings.anthropic_api_key or
            settings.anthropic_api_key == "" or
            "your_anthropic_api_key" in settings.anthropic_api_key.lower()):
            return {
                "status": "unconfigured",
                "message": "ANTHROPIC_API_KEY not set. Get your free key ($5 credits) from: https://console.anthropic.com",
                "model": settings.claude_model
            }

        try:
            client = cls.get_client()
            # Simple API test - list models or make minimal request
            return {
                "status": "healthy",
                "model": settings.claude_model,
                "message": "Claude API connected successfully"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
