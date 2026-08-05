"""Executive Summary Agent - generate McKinsey/BCG-style narrative"""

from langchain_google_genai import ChatGoogleGenerativeAI
from ..core.config import settings
from ..core.logging import get_logger
from .state import AgentState
import json

logger = get_logger(__name__)

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    api_key=settings.gemini_api_key,
    temperature=0.6,
)


async def executive_summary_agent(state: AgentState) -> AgentState:
    """
    Generate an executive-level summary in McKinsey/BCG consulting style.
    Synthesizes all prior agent outputs into a compelling narrative.
    """
    try:
        # Prepare context from all prior agents
        context = f"""
Original Question: {state.question}

SQL Query Executed: {state.sql_query}

KPIs Calculated: {state.kpis}

Trends Identified: {state.trends}

Anomalies Found: {state.anomalies}

Root Causes: {state.root_causes}

Forecasts: {state.forecasts}

Recommendations: {state.recommendations}
"""

        prompt = f"""You are a senior management consultant. Write an executive summary addressing this business question.

{context}

Provide a JSON response with:
{{
  "key_findings": ["Finding 1", "Finding 2", ...],
  "root_causes": ["Root cause 1", "Root cause 2", ...],
  "future_risks": ["Risk 1", "Risk 2", ...],
  "recommended_actions": [
    {{"action": "Action 1", "priority": "High", "impact": "Expected impact"}},
    ...
  ],
  "expected_impact": "Overall expected impact summary",
  "next_steps": ["Step 1", "Step 2", ...],
  "narrative": "2-3 paragraph executive summary in consulting style"
}}

Focus on:
1. What the data shows (key findings)
2. Why it matters (root causes)
3. Future outlook (risks and opportunities)
4. What to do (actionable recommendations)
5. How to implement (next steps)

Be concise, data-driven, and action-oriented. Use the tone of a McKinsey/BCG partner briefing an executive."""

        response = await llm.ainvoke(prompt)

        # Handle both string and list responses from Gemini
        if isinstance(response.content, list):
            content = response.content[0]['text'] if response.content else ""
        else:
            content = response.content

        content = content.strip()

        # Extract JSON
        start_idx = content.find("{")
        end_idx = content.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            summary = json.loads(json_str)

            state.executive_summary = {
                "key_findings": summary.get("key_findings", []),
                "root_causes": summary.get("root_causes", []) or state.root_causes,
                "future_risks": summary.get("future_risks", []),
                "recommended_actions": summary.get("recommended_actions", []),
                "expected_impact": summary.get("expected_impact", ""),
                "next_steps": summary.get("next_steps", []),
                "narrative": summary.get("narrative", ""),
            }

        logger.info("Executive summary generated")

    except Exception as e:
        logger.error(f"Executive summary agent error: {e}")
        state.errors.append(f"Executive summary failed: {str(e)}")

        # Fallback summary
        state.executive_summary = {
            "key_findings": list(state.kpis.keys()) if state.kpis else [],
            "root_causes": state.root_causes,
            "future_risks": [],
            "recommended_actions": [
                {"action": rec["title"], "priority": rec["priority"], "impact": rec.get("expected_impact", "")}
                for rec in state.recommendations[:3]
            ],
            "expected_impact": "See detailed recommendations",
            "next_steps": ["Review recommendations", "Create action plan"],
            "narrative": f"Analysis of: {state.question}",
        }

    return state
