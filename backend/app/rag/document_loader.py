"""Load documents from files for RAG"""

from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_documents_from_folder(folder_path: str = None) -> list:
    """
    Load all documents from a folder.

    Args:
        folder_path: Path to folder containing documents.
                    Defaults to /app/rag_documents or project root rag_documents.

    Returns:
        List of documents with 'text' and 'metadata' fields
    """
    if folder_path is None:
        # Try /app/rag_documents first (Docker container path)
        folder_path = Path("/app/rag_documents")

        if not folder_path.exists():
            # Fallback to project root rag_documents
            project_root = Path(__file__).parent.parent.parent.parent
            folder_path = project_root / "rag_documents"
    else:
        folder_path = Path(folder_path)

    documents = []

    if not folder_path.exists():
        logger.warning(f"RAG documents folder not found: {folder_path}")
        return documents

    try:
        # Load all markdown files
        for file_path in folder_path.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title from filename
                title = file_path.stem.replace('_', ' ').title()

                documents.append({
                    "text": content,
                    "metadata": {
                        "type": "policy",
                        "source": file_path.name,
                        "title": title,
                        "doc_id": file_path.stem,
                    }
                })
                logger.info(f"Loaded document: {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to load {file_path.name}: {e}")
                continue

        logger.info(f"Loaded {len(documents)} documents from {folder_path}")
        return documents

    except Exception as e:
        logger.error(f"Error loading documents from folder: {e}")
        return documents


def load_all_documents() -> list:
    """
    Load documents from both custom folder and sample documents.

    Returns:
        Combined list of all documents
    """
    # Load from custom rag_documents folder
    custom_docs = load_documents_from_folder()

    # Also load sample documents as fallback
    from .ingest import load_sample_documents
    sample_docs = load_sample_documents()

    # Combine and deduplicate
    all_docs = custom_docs if custom_docs else sample_docs

    logger.info(f"Total documents available: {len(all_docs)}")
    return all_docs
