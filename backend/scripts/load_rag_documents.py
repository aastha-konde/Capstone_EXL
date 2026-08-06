#!/usr/bin/env python3
"""
Script to load RAG documents into Chroma database.
Run this after starting the backend to populate the vector database.

Usage:
    python backend/scripts/load_rag_documents.py
"""

import sys
from pathlib import Path

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from app.core.config import settings
from app.rag import load_all_documents, ingest_documents
from app.core.logging import get_logger

logger = get_logger(__name__)


def main():
    """Load and ingest RAG documents"""
    print("\n" + "="*60)
    print("RetailMart RAG Document Loader")
    print("="*60 + "\n")

    try:
        # Load documents
        print("📂 Loading documents...")
        documents = load_all_documents()

        if not documents:
            print("❌ No documents found!")
            return False

        print(f"✓ Loaded {len(documents)} documents")

        # Show document summary
        for doc in documents:
            metadata = doc.get('metadata', {})
            print(f"  - {metadata.get('title', 'Unknown')}")

        # Ingest into Chroma
        print("\n📚 Ingesting documents into Chroma database...")
        success = ingest_documents(documents)

        if success:
            print("✓ Successfully ingested all documents")
            print("\n" + "="*60)
            print("RAG system is ready!")
            print("="*60 + "\n")
            return True
        else:
            print("❌ Failed to ingest documents")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Failed to load RAG documents: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
