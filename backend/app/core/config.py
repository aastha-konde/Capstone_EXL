"""Application configuration from environment variables"""

from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    """Application settings loaded from environment"""

    # Environment
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # API
    api_title: str = "DecisionLens AI"
    api_version: str = "1.0.0"
    api_description: str = "Enterprise Decision Intelligence Platform"

    # LLM Configuration (Google Gemini API)
    llm_provider: str = "gemini"
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-3.5-flash"
    llm_temperature: float = 0.7
    llm_timeout: int = 60

    # Database Configuration
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "retailmart"
    postgres_password: str = "retailmart_secure_pw"
    postgres_db: str = "retailmart_dw"
    postgres_pool_size: int = 10
    postgres_max_overflow: int = 20

    # DuckDB Configuration
    duckdb_path: str = ""

    @property
    def resolved_duckdb_path(self) -> str:
        """Resolve DuckDB path - support both relative and absolute paths"""
        if not self.duckdb_path or self.duckdb_path == "":
            # Default to project root/data_warehouse/retailmart.duckdb
            project_root = Path(__file__).parent.parent.parent.parent
            return str(project_root / "data_warehouse" / "retailmart.duckdb")

        path = Path(self.duckdb_path)
        if path.is_absolute():
            return str(path)

        # If relative, resolve from project root
        project_root = Path(__file__).parent.parent.parent.parent
        return str(project_root / self.duckdb_path)

    # JWT Configuration
    jwt_secret_key: str = "your_secret_key_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    jwt_refresh_expiration_days: int = 30

    # Security
    cors_origins: str = "http://localhost:3000,http://localhost:3001,http://localhost:5173,https://r3r5029m-3000.inc1.devtunnels.ms"
    allowed_hosts: str = "localhost,127.0.0.1"

    # Chroma RAG
    chroma_persist_directory: str = "./chroma_data"
    chroma_anonymized_telemetry: bool = False

    # Memory Configuration
    conversation_history_retention_days: int = 90
    report_retention_days: int = 365

    # Feature Flags
    enable_power_bi_embed: bool = False
    enable_rag: bool = True
    enable_forecasting: bool = True
    enable_anomaly_detection: bool = True

    # Frontend Configuration
    vite_api_url: str = "http://localhost:8000"
    vite_api_timeout: int = 30000

    # Email Configuration
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    report_delivery_email: Optional[str] = None

    class Config:
        env_file = str(Path(__file__).parent.parent.parent.parent / ".env")
        case_sensitive = False
        extra = "ignore"

    @property
    def postgres_url(self) -> str:
        """PostgreSQL connection URL"""
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def async_postgres_url(self) -> str:
        """Async PostgreSQL connection URL (asyncpg)"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


# Create a singleton instance
settings = Settings()
