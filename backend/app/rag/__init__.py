"""RAG (Retrieval-Augmented Generation) for policy documents"""

from .ingest import ingest_documents, load_sample_documents
from .retrieve import retrieve_relevant_context, get_context_string
from .document_loader import load_documents_from_folder, load_all_documents

__all__ = [
    "ingest_documents",
    "load_sample_documents",
    "retrieve_relevant_context",
    "get_context_string",
    "load_documents_from_folder",
    "load_all_documents",
]
