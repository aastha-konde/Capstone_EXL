"""Health and system status endpoints"""

from fastapi import APIRouter, HTTPException, status
from ..core.logging import get_logger
from ..db import get_db_status, get_duckdb_status
from ..schemas import HealthResponse
from datetime import datetime
from .. import __version__
from ..core.config import settings

logger = get_logger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check"""
    db_status = get_db_status()
    duckdb_status = get_duckdb_status()

    # Healthy if at least one DB is connected
    if db_status == "disconnected" and duckdb_status == "disconnected":
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=__version__,
        environment=settings.environment,
        timestamp=datetime.utcnow(),
        database=db_status,
        duckdb=duckdb_status,
    )


@router.get("/status")
async def status_check():
    """Detailed status information"""
    return {
        "app": "DecisionLens AI",
        "version": __version__,
        "environment": settings.environment,
        "database": get_db_status(),
        "duckdb": get_duckdb_status(),
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "rag": settings.enable_rag,
            "forecasting": settings.enable_forecasting,
            "anomaly_detection": settings.enable_anomaly_detection,
            "power_bi_embed": settings.enable_power_bi_embed,
        },
    }
