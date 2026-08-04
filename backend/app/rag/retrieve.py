"""Document retrieval from Chroma"""

from chromadb import PersistentClient
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


def retrieve_relevant_context(
    query: str,
    collection_name: str = "RetailMart-Policies",
    n_results: int = 3,
) -> list:
    """
    Retrieve relevant policy documents based on query.

    Returns list of relevant document texts.
    """
    try:
        client = PersistentClient(
            path=settings.chroma_persist_directory,
            anonymized_telemetry=settings.chroma_anonymized_telemetry,
        )

        collection = client.get_collection(name=collection_name)

        # Query the collection
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        # Extract documents
        documents = []
        if results and results['documents']:
            documents = results['documents'][0] if results['documents'] else []

        logger.info(f"Retrieved {len(documents)} relevant documents for query")
        return documents

    except Exception as e:
        logger.error(f"Document retrieval failed: {e}")
        return []


def get_context_string(query: str, n_results: int = 3) -> str:
    """
    Get relevant context as a single formatted string for LLM prompting.
    """
    documents = retrieve_relevant_context(query, n_results=n_results)

    if not documents:
        return "No relevant policies found."

    context = "Relevant Company Policies:\n\n"
    for i, doc in enumerate(documents, 1):
        context += f"{i}. {doc}\n\n"

    return context
