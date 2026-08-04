"""SQLAlchemy models for application state (not the data warehouse)"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    """Application users"""
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default='viewer')  # admin, executive, analyst, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ConversationHistory(Base):
    """Conversation history for multi-turn support"""
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True)
    session_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('app_users.id'), nullable=True, index=True)
    question = Column(Text, nullable=False)
    response = Column(Text)
    intent = Column(String(100))
    metadata_json = Column("metadata", JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class GeneratedReport(Base):
    """Generated reports for download"""
    __tablename__ = "generated_reports"

    id = Column(Integer, primary_key=True)
    report_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('app_users.id'), nullable=True, index=True)
    report_type = Column(String(20))  # 'PDF', 'PPTX', 'JSON'
    file_path = Column(String(500))
    question = Column(Text)
    summary = Column(Text)
    metadata_json = Column("metadata",JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)


class CheckpointState(Base):
    """LangGraph checkpoint states for agent resumption"""
    __tablename__ = "checkpoint_states"

    id = Column(Integer, primary_key=True)
    thread_id = Column(String(255), nullable=False, index=True)
    checkpoint_id = Column(String(255), nullable=False)
    parent_config = Column(JSON)
    config = Column(JSON)
    values = Column(JSON)
    metadata_json = Column("metadata", JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserPreference(Base):
    """User preferences and settings"""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('app_users.id'), nullable=False, index=True)
    key = Column(String(100), nullable=False)
    value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
