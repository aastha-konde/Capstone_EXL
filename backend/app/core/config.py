"""Application configuration from environment variables"""

from pydantic_settings import BaseSettings
from typing import Optional


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

    # LLM Configuration (OpenRouter)
    openrouter_api_key: str
    openrouter_model: str = "qwen/qwen-2.5-72b-instruct"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
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
    duckdb_path: str = "./data_warehouse/retailmart.duckdb"

    # JWT Configuration
    jwt_secret_key: str = "your_secret_key_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    jwt_refresh_expiration_days: int = 30

    # Security
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
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

    class Config:
        env_file = ".env"
        case_sensitive = False

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
