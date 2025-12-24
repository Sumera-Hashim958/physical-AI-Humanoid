"""
Ingest textbook MDX files into Qdrant vector database.

This script:
1. Reads MDX files from frontend/docs/
2. Chunks content by sections (headings)
3. Generates embeddings using sentence-transformers
4. Uploads to Qdrant for RAG chatbot

Usage:
    python scripts/ingest_textbook.py
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict
import uuid

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.utils.config import get_settings


def read_mdx_file(file_path: str) -> str:
    """Read MDX file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def chunk_by_sections(content: str, chapter_id: str) -> List[Dict]:
    """
    Chunk content by markdown headings.

    Each chunk contains:
    - Section heading + content
    - Metadata (chapter_id, section_title)

    Args:
        content: MDX file content
        chapter_id: e.g., "chapter-01-intro-physical-ai"

    Returns:
        List of chunks with metadata
    """
    chunks = []

    # Remove frontmatter (---...---)
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Split by headings (## or ###)
    sections = re.split(r'\n(#{2,3}\s+.+?)\n', content)

    current_section = "Introduction"

    for i, section in enumerate(sections):
        # Check if this is a heading
        if section.startswith('##'):
            heading_text = re.sub(r'^#{2,3}\s+', '', section).strip()
            current_section = heading_text
        elif section.strip():
            # This is content
            chunk_text = f"Section: {current_section}\n\n{section.strip()}"

            # Only add chunks with substantial content (>100 chars)
            if len(chunk_text) > 100:
                chunks.append({
                    "content": chunk_text,
                    "chapter_id": chapter_id,
                    "section": current_section
                })

    return chunks


def main():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("TEXTBOOK INGESTION PIPELINE")
    print("=" * 60)

    # Step 1: Load embedding model
    print("\n[1/5] Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim vectors
    print(f"[OK] Model loaded: all-MiniLM-L6-v2 (384 dimensions)")

    # Step 2: Connect to Qdrant
    print("\n[2/5] Connecting to Qdrant...")
    settings = get_settings()
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        timeout=60
    )
    print(f"[OK] Connected to Qdrant: {settings.qdrant_url}")

    # Step 3: Create/recreate collection
    print("\n[3/5] Setting up collection...")
    collection_name = settings.qdrant_collection_name

    # Delete if exists (fresh start)
    try:
        client.delete_collection(collection_name)
        print(f"[DELETE] Deleted existing collection: {collection_name}")
    except:
        pass

    # Create new collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,  # all-MiniLM-L6-v2 dimension
            distance=Distance.COSINE
        )
    )
    print(f"[OK] Created collection: {collection_name}")

    # Step 4: Read and chunk MDX files
    print("\n[4/5] Reading and chunking textbook files...")

    # Get path to frontend/docs/
    backend_dir = Path(__file__).parent.parent
    docs_dir = backend_dir.parent / "frontend" / "docs"

    if not docs_dir.exists():
        print(f"[ERROR] Docs directory not found: {docs_dir}")
        return

    all_chunks = []

    # Process each chapter
    mdx_files = sorted(docs_dir.glob("chapter-*.mdx"))

    for mdx_file in mdx_files:
        chapter_id = mdx_file.stem  # e.g., "chapter-01-intro-physical-ai"
        print(f"  [PROCESSING] {chapter_id}")

        content = read_mdx_file(mdx_file)
        chunks = chunk_by_sections(content, chapter_id)
        all_chunks.extend(chunks)

        print(f"     [OK] Generated {len(chunks)} chunks")

    print(f"\n[OK] Total chunks: {len(all_chunks)}")

    # Step 5: Generate embeddings and upload
    print("\n[5/5] Generating embeddings and uploading to Qdrant...")

    points = []
    batch_size = 32

    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]

        # Generate embeddings for batch
        texts = [chunk["content"] for chunk in batch]
        embeddings = model.encode(texts, show_progress_bar=False)

        # Create points
        for j, (chunk, embedding) in enumerate(zip(batch, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "content": chunk["content"],
                    "chapter_id": chunk["chapter_id"],
                    "section": chunk["section"]
                }
            )
            points.append(point)

        print(f"  [UPLOAD] Uploading batch {i//batch_size + 1}/{(len(all_chunks)-1)//batch_size + 1}...")

    # Upload all points
    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print(f"\n[OK] Uploaded {len(points)} vectors to Qdrant!")

    # Verify
    collection_info = client.get_collection(collection_name)
    print(f"\n[INFO] Collection Info:")
    print(f"   - Name: {collection_name}")
    print(f"   - Vectors: {collection_info.points_count}")
    print(f"   - Status: {collection_info.status}")

    print("\n" + "=" * 60)
    print("[SUCCESS] INGESTION COMPLETE!")
    print("=" * 60)
    print("\nYour ChatBot can now answer questions about the textbook!")


if __name__ == "__main__":
    main()
