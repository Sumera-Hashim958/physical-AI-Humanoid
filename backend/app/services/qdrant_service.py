"""
Qdrant vector search service.
Handles vector similarity search for RAG chatbot using Qdrant Cloud.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, SearchRequest
from app.utils.config import get_settings
from typing import List, Dict
import uuid
from sentence_transformers import SentenceTransformer


class QdrantService:
    """
    Service for Qdrant vector database operations.

    Handles connection to Qdrant Cloud and semantic search
    for textbook content chunks.

    Example:
        >>> results = await QdrantService.search_similar_chunks(
        ...     question="What is a CNN?",
        ...     top_k=5
        ... )
        >>> for chunk in results:
        ...     print(chunk["content"], chunk["similarity"])
    """

    _client: QdrantClient | None = None
    _embedding_model: SentenceTransformer | None = None

    @classmethod
    def get_client(cls) -> QdrantClient:
        """
        Get or create Qdrant client singleton.

        Returns:
            QdrantClient: Connected Qdrant client instance

        Raises:
            ConnectionError: If unable to connect to Qdrant Cloud
        """
        if cls._client is None:
            settings = get_settings()

            try:
                cls._client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key,
                    timeout=30  # 30 second timeout
                )
                print(f"[OK] Connected to Qdrant: {settings.qdrant_url}")
            except Exception as e:
                print(f"[ERROR] Failed to connect to Qdrant: {e}")
                raise ConnectionError(f"Qdrant connection failed: {e}")

        return cls._client

    @classmethod
    def get_embedding_model(cls) -> SentenceTransformer:
        """
        Get or create embedding model singleton.

        Returns:
            SentenceTransformer: Loaded embedding model

        Note:
            Model is cached after first load to avoid reloading
        """
        if cls._embedding_model is None:
            print("[INFO] Loading embedding model: all-MiniLM-L6-v2...")
            cls._embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("[OK] Embedding model loaded (384 dimensions)")

        return cls._embedding_model

    @classmethod
    async def search_similar_chunks(
        cls,
        question: str,
        top_k: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Search for textbook chunks similar to the question.

        Uses semantic similarity search to find relevant content.
        For MVP, we'll use a simple approach - in production, you'd
        embed the question using Claude/OpenAI embeddings.

        Args:
            question: User's question text
            top_k: Number of results to return (default: 5)
            score_threshold: Minimum similarity score (0-1, default: 0.7)

        Returns:
            List of matching chunks with metadata:
            [
                {
                    "id": "chunk_123",
                    "content": "CNNs are neural networks...",
                    "chapter_id": "chapter-3-cnns",
                    "section": "Introduction",
                    "similarity": 0.92
                },
                ...
            ]

        Raises:
            Exception: If search fails

        Example:
            >>> chunks = await QdrantService.search_similar_chunks(
            ...     "What are transformers?",
            ...     top_k=3
            ... )
        """
        client = cls.get_client()
        settings = get_settings()
        model = cls.get_embedding_model()

        try:
            # Step 1: Embed the question
            question_embedding = model.encode(question).tolist()

            # Step 2: Search Qdrant
            search_results = client.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=question_embedding,
                limit=top_k,
                score_threshold=score_threshold
            )

            # Step 3: Format results
            chunks = []
            for result in search_results:
                chunks.append({
                    "id": str(result.id),
                    "content": result.payload.get("content", ""),
                    "chapter_id": result.payload.get("chapter_id", ""),
                    "section": result.payload.get("section", ""),
                    "similarity": result.score
                })

            print(f"[OK] Found {len(chunks)} relevant chunks (score >= {score_threshold})")
            return chunks

        except Exception as e:
            print(f"[ERROR] Qdrant search failed: {e}")
            raise

    @classmethod
    async def create_collection_if_not_exists(
        cls,
        vector_size: int = 1536  # Default for OpenAI/Claude embeddings
    ) -> bool:
        """
        Create Qdrant collection if it doesn't exist.

        Args:
            vector_size: Dimension of embedding vectors (default: 1536)

        Returns:
            bool: True if collection created or exists, False on error

        Example:
            >>> success = await QdrantService.create_collection_if_not_exists()
        """
        client = cls.get_client()
        settings = get_settings()
        collection_name = settings.qdrant_collection_name

        try:
            # Check if collection exists
            collections = client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if collection_name in collection_names:
                print(f"[OK] Collection '{collection_name}' already exists")
                return True

            # Create collection
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE  # Cosine similarity for semantic search
                )
            )
            print(f"[OK] Created collection '{collection_name}'")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to create collection: {e}")
            return False

    @classmethod
    async def health_check(cls) -> Dict:
        """
        Check Qdrant connection health.

        Returns:
            dict: Health status with connection info

        Example:
            >>> health = await QdrantService.health_check()
            >>> print(health["status"])  # "healthy" or "unhealthy"
        """
        try:
            client = cls.get_client()
            settings = get_settings()

            # Get collections to verify connection
            collections = client.get_collections()
            collection_names = [c.name for c in collections.collections]

            return {
                "status": "healthy",
                "qdrant_url": settings.qdrant_url,
                "collections": collection_names,
                "target_collection": settings.qdrant_collection_name,
                "collection_exists": settings.qdrant_collection_name in collection_names
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
