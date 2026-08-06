"""Document ingestion for RAG"""

from chromadb import PersistentClient
from pathlib import Path
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


def get_chroma_client():
    """Get or create Chroma persistent client"""
    try:
        client = PersistentClient(
            path=settings.chroma_persist_directory,
        )
        return client
    except Exception as e:
        logger.error(f"Failed to create Chroma client: {e}")
        raise


def ingest_documents(documents: list, collection_name: str = "RetailMart-Policies"):
    """
    Ingest documents into Chroma for RAG.

    documents: list of dicts with 'text', 'metadata' keys
    """
    try:
        client = get_chroma_client()

        # Get or create collection
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        # Process and add documents
        ids = []
        texts = []
        metadatas = []

        for i, doc in enumerate(documents):
            ids.append(f"doc_{i}")
            texts.append(doc.get("text", ""))
            metadatas.append(doc.get("metadata", {}))

        # Add to collection
        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
        )

        logger.info(f"Ingested {len(documents)} documents into {collection_name}")
        return True

    except Exception as e:
        logger.error(f"Document ingestion failed: {e}")
        return False


def load_sample_documents():
    """
    Load sample RetailMart Global policy documents.
    """
    documents = [
        {
            "text": "Discount Policy: Maximum discount is 30% for regular customers, 40% for loyal customers. Discounts over 25% require manager approval.",
            "metadata": {"type": "policy", "domain": "sales", "doc_id": "discount-001"}
        },
        {
            "text": "Pricing Strategy: Our pricing strategy focuses on value-based pricing with seasonal adjustments. Black Friday and Christmas periods allow up to 35% discounts.",
            "metadata": {"type": "policy", "domain": "pricing", "doc_id": "pricing-001"}
        },
        {
            "text": "Inventory Management: Target stock level is 3 months of average sales. Reorder point is 1.5 months. Safety stock varies by region and seasonality.",
            "metadata": {"type": "sop", "domain": "operations", "doc_id": "inventory-001"}
        },
        {
            "text": "Customer Retention Program: Churn risk assessment is done quarterly. Customers with 30%+ drop in purchase frequency are flagged for retention campaigns.",
            "metadata": {"type": "policy", "domain": "customer_service", "doc_id": "retention-001"}
        },
        {
            "text": "Marketing Budget Allocation: Annual marketing budget is allocated 40% to digital, 30% to traditional, 20% to partnerships, 10% to experimentation.",
            "metadata": {"type": "policy", "domain": "marketing", "doc_id": "marketing-001"}
        },
        {
            "text": "Supplier Relationship: Target supplier lead time is 14 days. Suppliers with consistent delays >5 days are subject to penalty clauses and replacement review.",
            "metadata": {"type": "sop", "domain": "procurement", "doc_id": "supplier-001"}
        },
        {
            "text": "Customer Satisfaction Target: NPS target is 50+. Support resolution time target is 24 hours for critical, 48 hours for high, 72 hours for medium.",
            "metadata": {"type": "target", "domain": "customer_service", "doc_id": "satisfaction-001"}
        },
        {
            "text": "Regional Performance Benchmarks: Target ROIC is 15%. Sales growth target is 8-12% YoY. Profit margin target is 12-18% by region.",
            "metadata": {"type": "target", "domain": "finance", "doc_id": "benchmarks-001"}
        },
    ]

    return documents
