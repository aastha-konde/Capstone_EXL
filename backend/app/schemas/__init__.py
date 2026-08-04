"""Pydantic schemas for request/response validation"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Authentication Schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: Optional[str]
    role: str
    created_at: datetime


# Chat / Agent Schemas
class ChatRequest(BaseModel):
    question: str = Field(..., description="Natural language business question")
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class SQLResult(BaseModel):
    sql: Optional[str]
    rows: Optional[List[Dict[str, Any]]]
    columns: Optional[List[str]]
    row_count: Optional[int]


class KPIValue(BaseModel):
    name: str
    value: float
    unit: Optional[str] = None
    period: Optional[str] = None
    change_percent: Optional[float] = None


class AnalyticsResult(BaseModel):
    kpis: List[KPIValue]
    trends: Optional[List[Dict[str, Any]]]
    anomalies: Optional[List[Dict[str, Any]]]
    root_causes: Optional[List[str]]


class Forecast(BaseModel):
    period: str
    value: float
    confidence_lower: float
    confidence_upper: float
    model_used: str


class ForecastResult(BaseModel):
    metric: str
    forecasts: List[Forecast]
    mape: Optional[float]
    rmse: Optional[float]


class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    priority: str  # 'Low', 'Medium', 'High', 'Critical'
    expected_impact: str
    confidence: float
    estimated_revenue_improvement: Optional[float]
    estimated_cost_savings: Optional[float]
    actions: List[str]


class ExecutiveSummary(BaseModel):
    key_findings: List[str]
    root_causes: List[str]
    future_risks: List[str]
    recommendations: List[Recommendation]
    expected_impact: str
    next_steps: List[str]


class ChatResponse(BaseModel):
    session_id: str
    question: str
    intent: Optional[str] = None
    sql_result: Optional[Dict[str, Any]] = None
    analytics: Optional[Dict[str, Any]] = None
    forecasts: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    executive_summary: Optional[Dict[str, Any]] = None
    response_time_ms: Optional[float] = None


class ChatException(Exception):
    """Chat processing exception"""
    pass


class ReportGenerateRequest(BaseModel):
    session_id: str
    report_type: str = "PDF"  # 'PDF', 'PPTX'
    include_charts: bool = True


class ReportResponse(BaseModel):
    report_id: str
    session_id: str
    report_type: str
    file_url: str
    created_at: datetime
    file_size_bytes: Optional[int]


# Health Check
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    timestamp: datetime
    database: Optional[str]
    duckdb: Optional[str]
