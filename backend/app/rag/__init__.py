"""RAG (Retrieval-Augmented Generation) for policy documents"""

from .ingest import ingest_documents, load_sample_documents
from .retrieve import retrieve_relevant_context

__all__ = ["ingest_documents", "load_sample_documents", "retrieve_relevant_context"]
