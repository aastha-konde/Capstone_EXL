"""Agent state management for LangGraph"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class AgentState:
    """
    Shared state across all agents in the pipeline.
    Passed through the graph and updated by each agent node.
    """
    # Input
    question: str
    session_id: str
    user_id: Optional[int] = None

    # Intent Detection output
    intent: Optional[str] = None  # 'diagnostic', 'predictive', 'prescriptive'
    required_tables: List[str] = field(default_factory=list)

    # SQL Agent output
    sql_query: Optional[str] = None
    sql_result: Optional[Dict[str, Any]] = None  # {'rows': [...], 'columns': [...]}
    sql_error: Optional[str] = None

    # Analytics Agent output
    kpis: Dict[str, Any] = field(default_factory=dict)  # {metric: {value, unit, change_percent}}
    trends: List[Dict[str, Any]] = field(default_factory=list)
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    root_causes: List[str] = field(default_factory=list)

    # Forecast Agent output
    forecasts: Dict[str, Any] = field(default_factory=dict)  # {metric: [Forecast]}
    forecast_models: Dict[str, str] = field(default_factory=dict)  # {metric: model_name}
    forecast_accuracy: Dict[str, float] = field(default_factory=dict)  # {metric: mape}

    # Recommendation Agent output
    recommendations: List[Dict[str, Any]] = field(default_factory=list)

    # Executive Summary output
    executive_summary: Optional[Dict[str, Any]] = None

    # Report generation
    report_path: Optional[str] = None

    # Metadata
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    total_time_ms: Optional[float] = None
    errors: List[str] = field(default_factory=list)


def create_state(
    question: str,
    session_id: str,
    user_id: Optional[int] = None
) -> AgentState:
    """Create a new agent state"""
    return AgentState(
        question=question,
        session_id=session_id,
        user_id=user_id,
    )
