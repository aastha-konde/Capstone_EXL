"""Conversation memory management"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid
import logging
from ..db.models import ConversationHistory

logger = logging.getLogger(__name__)


def save_conversation(
    db: Session,
    session_id: str,
    question: str,
    intent: str = None,
    metadata: dict = None,
) -> ConversationHistory:
    """
    Save a conversation turn to the database.
    """
    try:
        # Convert session_id to UUID if needed
        if isinstance(session_id, str) and len(session_id) == 36:
            session_uuid = uuid.UUID(session_id)
        else:
            session_uuid = uuid.uuid4()

        conversation = ConversationHistory(
            session_id=session_uuid,
            question=question,
            intent=intent,
            metadata=metadata or {},
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        logger.info(f"Conversation saved: {session_uuid}")
        return conversation

    except Exception as e:
        logger.error(f"Failed to save conversation: {e}")
        db.rollback()
        raise


def get_conversation_history(
    db: Session,
    session_id: str,
    limit: int = 10,
) -> list:
    """
    Retrieve conversation history for a session.
    """
    try:
        # Convert session_id to UUID if needed
        if isinstance(session_id, str) and len(session_id) == 36:
            session_uuid = uuid.UUID(session_id)
        else:
            session_uuid = uuid.uuid4()

        conversations = db.query(ConversationHistory).filter(
            ConversationHistory.session_id == session_uuid
        ).order_by(
            desc(ConversationHistory.created_at)
        ).limit(limit).all()

        return conversations

    except Exception as e:
        logger.error(f"Failed to retrieve conversation history: {e}")
        return []


def get_recent_sessions(db: Session, user_id: int = None, limit: int = 10) -> list:
    """
    Get recent conversation sessions.
    """
    try:
        query = db.query(ConversationHistory)

        if user_id:
            query = query.filter(ConversationHistory.user_id == user_id)

        sessions = query.order_by(
            desc(ConversationHistory.created_at)
        ).limit(limit).all()

        return sessions

    except Exception as e:
        logger.error(f"Failed to get recent sessions: {e}")
        return []
