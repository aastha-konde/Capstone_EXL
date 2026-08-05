"""Chat endpoint - main interface to agent pipeline"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from ..schemas import ChatRequest, ChatResponse, ChatException
from ..agents.graph import run_agent_pipeline_simple
from ..core.logging import get_logger
from ..db import get_db
from ..db.models import ConversationHistory

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Process a natural language business question through the agent pipeline.

    Returns analysis including SQL, KPIs, forecasts, recommendations, and executive summary.
    """
    try:
        # Generate or use provided session ID
        session_id = request.session_id or str(uuid.uuid4())

        logger.info(f"Chat request: {request.question[:100]}... (session: {session_id})")

        # Run the agent pipeline
        agent_state = await run_agent_pipeline_simple(
            question=request.question,
            session_id=session_id,
            user_id=None,  # TODO: Extract from auth
        )

        # Save conversation to database
        try:
            conversation = ConversationHistory(
                session_id=uuid.UUID(session_id) if len(session_id) == 36 else uuid.uuid4(),
                question=request.question,
                intent=agent_state.intent,
                metadata_info={
                    "sql_query": agent_state.sql_query,
                    "error_count": len(agent_state.errors),
                    "response_time_ms": agent_state.total_time_ms,
                },
            )
            db.add(conversation)
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to save conversation history: {e}")
            db.rollback()

        # Build response
        response = ChatResponse(
            session_id=session_id,
            question=request.question,
            intent=agent_state.intent,
            sql_result=agent_state.sql_result,
            analytics={
                "kpis": agent_state.kpis,
                "trends": agent_state.trends,
                "anomalies": agent_state.anomalies,
                "root_causes": agent_state.root_causes,
            } if agent_state.kpis else None,
            forecasts=[
                {
                    "metric": metric,
                    "forecasts": agent_state.forecasts[metric],
                    "mape": agent_state.forecast_accuracy.get(metric, 0),
                }
                for metric in agent_state.forecasts
            ] if agent_state.forecasts else None,
            recommendations=agent_state.recommendations,
            executive_summary=agent_state.executive_summary,
            response_time_ms=agent_state.total_time_ms,
        )

        logger.info(f"Chat response complete ({agent_state.total_time_ms:.2f}ms)")
        return response

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )
