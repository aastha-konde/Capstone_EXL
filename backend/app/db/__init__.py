"""Database connections and session management"""

import duckdb
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import threading
from typing import Generator

from ..core.config import settings
from ..core.logging import get_logger

logger = get_logger(__name__)

# SQLAlchemy PostgreSQL engine
engine = create_engine(
    settings.postgres_url,
    poolclass=NullPool if settings.environment == 'development' else None,
    echo=settings.debug,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Thread-local storage for DuckDB connections
_duckdb_local = threading.local()


def get_duckdb_conn():
    """Get or create a thread-local DuckDB connection"""
    if not hasattr(_duckdb_local, 'conn') or _duckdb_local.conn is None:
        path = settings.resolved_duckdb_path
        logger.debug(f"Connecting to DuckDB: {path}")
        _duckdb_local.conn = duckdb.connect(path, read_only=False)
    return _duckdb_local.conn


def get_db() -> Generator[Session, None, None]:
    """Dependency to get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from .models import Base
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Database initialization failed (non-blocking): {str(e)[:100]}")
        # Don't raise - PostgreSQL is optional, DuckDB is primary


def get_db_status():
    """Check database connectivity"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "connected"
    except Exception as e:
        logger.warning(f"PostgreSQL unavailable: {str(e)[:50]}")
        return "disconnected"


def get_duckdb_status():
    """Check DuckDB connectivity"""
    try:
        conn = get_duckdb_conn()
        result = conn.execute("SELECT 1").fetchall()
        return "connected" if result else "error"
    except Exception as e:
        logger.error(f"DuckDB connection failed: {e}")
        return "disconnected"
