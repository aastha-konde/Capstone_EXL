"""
DecisionLens AI - FastAPI Application
Enterprise Decision Intelligence Platform
"""

import time
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .core.config import settings
from .core.logging import configure_logging, get_logger
from .db import init_db
from .api import chat, health, analytics, recommendations, dataservices
from .rag import ingest_documents, load_all_documents

# Configure logging
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    logger.info("Starting DecisionLens AI application")
    try:
        # Initialize DB in background to avoid blocking startup
        import threading
        db_thread = threading.Thread(target=init_db, daemon=True)
        db_thread.start()

        # Initialize RAG with documents
        if settings.enable_rag:
            try:
                documents = load_all_documents()
                if documents:
                    ingest_documents(documents)
                    logger.info(f"✓ RAG system initialized with {len(documents)} documents")
                else:
                    logger.warning("No documents found for RAG initialization")
            except Exception as e:
                logger.warning(f"RAG initialization failed (non-blocking): {e}")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")

    yield

    logger.info("Shutting down DecisionLens AI application")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Add CORS middleware
cors_origins = [origin.strip() for origin in settings.cors_origins.split(',')]
logger.info(f"CORS Origins configured: {cors_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_timing_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    return response


# Include routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(analytics.router)
app.include_router(recommendations.router)
app.include_router(dataservices.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DecisionLens AI",
        "version": settings.api_version,
        "docs": "/docs" if settings.debug else "Not available",
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
