"""LangGraph StateGraph wiring all agents together"""

from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from typing import Dict, Any
import time
from datetime import datetime

from ..core.config import settings
from ..core.logging import get_logger
from .state import AgentState
from .intent_agent import intent_agent
from .sql_agent import sql_agent
from .analytics_agent import analytics_agent
from .forecast_agent import forecast_agent
from .recommendation_agent import recommendation_agent
from .executive_summary_agent import executive_summary_agent

logger = get_logger(__name__)


def create_agent_graph():
    """
    Create the LangGraph StateGraph wiring all agents.

    Flow:
    1. Intent Detection -> classify question, identify required tables
    2. SQL Agent -> convert NL to SQL, execute on DuckDB
    3. Analytics Agent -> calculate KPIs, find trends/anomalies
    4. Forecast Agent -> predict future outcomes
    5. Recommendation Agent -> suggest actions
    6. Executive Summary Agent -> synthesize into narrative
    """

    # Create the graph
    graph = StateGraph(AgentState)

    # Add nodes (agent functions)
    graph.add_node("intent", intent_agent)
    graph.add_node("sql", sql_agent)
    graph.add_node("analytics", analytics_agent)
    graph.add_node("forecast", forecast_agent)
    graph.add_node("recommendations", recommendation_agent)
    graph.add_node("summary", executive_summary_agent)

    # Define edges (flow)
    # Linear flow: intent -> sql -> analytics -> forecast -> recommendations -> summary
    graph.add_edge("intent", "sql")
    graph.add_edge("sql", "analytics")
    graph.add_edge("analytics", "forecast")
    graph.add_edge("forecast", "recommendations")
    graph.add_edge("recommendations", "summary")

    # Set entry point
    graph.set_entry_point("intent")
    graph.set_finish_point("summary")

    # Compile the graph
    # Try to use PostgreSQL checkpointer if available, fall back to memory
    try:
        checkpointer = PostgresSaver.from_conn_string(settings.postgres_url)
        compiled_graph = graph.compile(checkpointer=checkpointer)
        logger.info("Graph compiled with PostgreSQL checkpointer")
    except Exception as e:
        logger.warning(f"Could not create PostgreSQL checkpointer: {e}, using in-memory")
        compiled_graph = graph.compile()

    return compiled_graph


async def run_agent_pipeline(
    question: str,
    session_id: str,
    user_id: int = None,
) -> AgentState:
    """
    Execute the full agent pipeline for a question.
    Returns the final AgentState with all outputs.
    """
    start_time = time.time()

    try:
        # Create initial state
        state = AgentState(
            question=question,
            session_id=session_id,
            user_id=user_id,
        )

        # Get compiled graph
        agent_graph = create_agent_graph()

        # Run the pipeline
        logger.info(f"Starting pipeline for: {question}")

        # Execute synchronously (LangGraph handles async internally)
        final_state = await agent_graph.ainvoke(
            {
                "question": state.question,
                "session_id": state.session_id,
                "user_id": state.user_id,
            },
            config={"configurable": {"thread_id": session_id}}
        )

        # Convert back to AgentState if needed
        if isinstance(final_state, dict):
            for key, value in final_state.items():
                setattr(state, key, value)
        else:
            state = final_state

        # Calculate total time
        state.end_time = datetime.utcnow()
        state.total_time_ms = (time.time() - start_time) * 1000

        logger.info(f"Pipeline complete in {state.total_time_ms:.2f}ms")

        return state

    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        state.errors.append(f"Pipeline failed: {str(e)}")
        state.end_time = datetime.utcnow()
        state.total_time_ms = (time.time() - start_time) * 1000
        return state


# Simple in-memory graph for testing (doesn't use StateGraph)
async def run_agent_pipeline_simple(
    question: str,
    session_id: str,
    user_id: int = None,
) -> AgentState:
    """
    Simplified pipeline execution without LangGraph checkpointing.
    Useful for testing and simple deployments.
    """
    start_time = time.time()

    state = AgentState(
        question=question,
        session_id=session_id,
        user_id=user_id,
    )

    try:
        logger.info(f"Starting simple pipeline: {question}")

        # Execute agents sequentially
        state = await intent_agent(state)
        if not state.errors:
            state = await sql_agent(state)
        if not state.errors and state.sql_result:
            state = await analytics_agent(state)
        if not state.errors and state.kpis:
            state = await forecast_agent(state)
        if not state.errors:
            state = await recommendation_agent(state)
        if not state.errors:
            state = await executive_summary_agent(state)

        state.end_time = datetime.utcnow()
        state.total_time_ms = (time.time() - start_time) * 1000

        logger.info(f"Simple pipeline complete in {state.total_time_ms:.2f}ms")

    except Exception as e:
        logger.error(f"Simple pipeline error: {e}", exc_info=True)
        state.errors.append(f"Pipeline failed: {str(e)}")
        state.end_time = datetime.utcnow()
        state.total_time_ms = (time.time() - start_time) * 1000

    return state
