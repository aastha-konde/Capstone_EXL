"""Recommendation Agent - suggest actions based on analysis"""

from langchain_openai import ChatOpenAI
from ..core.config import settings
from ..core.logging import get_logger
from .state import AgentState
import json

logger = get_logger(__name__)

llm = ChatOpenAI(
    model=settings.openrouter_model,
    temperature=settings.llm_temperature,
    openai_api_key=settings.openrouter_api_key,
    openai_api_base=settings.openrouter_base_url,
)


# Business rules for recommendations
BUSINESS_RULES = [
    {
        "condition": "profit_margin < 10",
        "recommendation": "Reduce discount rates or increase prices to improve margins",
        "priority": "High",
        "impact": "5-15% margin improvement",
    },
    {
        "condition": "stock_out > 5%",
        "recommendation": "Increase safety stock levels and improve inventory forecasting",
        "priority": "High",
        "impact": "Reduce stockouts by 30-50%",
    },
    {
        "condition": "customer_churn > 20%",
        "recommendation": "Launch retention campaigns and improve customer service",
        "priority": "Critical",
        "impact": "Recover 15-25% of churning customers",
    },
    {
        "condition": "delivery_time > 10_days",
        "recommendation": "Optimize warehouse location or use faster shipping",
        "priority": "Medium",
        "impact": "Reduce delivery time by 25-40%",
    },
]


async def recommendation_agent(state: AgentState) -> AgentState:
    """
    Generate data-driven recommendations based on KPIs and analysis.
    Combines rule-based engine with LLM reasoning.
    """
    try:
        recommendations = []

        # Rule-based recommendations
        if state.kpis:
            for rule in BUSINESS_RULES:
                # Simplified rule matching
                if "margin" in rule["condition"] and "profit" in state.kpis:
                    recommendations.append({
                        "id": f"rule_{len(recommendations)}",
                        "title": "Improve Profit Margins",
                        "description": rule["recommendation"],
                        "priority": rule["priority"],
                        "confidence": 0.8,
                        "expected_impact": rule["impact"],
                        "estimated_revenue_improvement": 50000,
                        "estimated_cost_savings": 25000,
                        "actions": [
                            "Review current discount strategy",
                            "Analyze price elasticity",
                            "Test price increases in low-elasticity segments",
                        ],
                    })

        # LLM-based recommendations
        if state.question and (state.kpis or state.anomalies or state.trends):
            prompt = f"""Based on this business analysis, suggest 2-3 actionable recommendations.

Question: {state.question}

KPIs: {state.kpis}
Anomalies: {state.anomalies}
Trends: {state.trends}

Respond with JSON array:
[{{
  "title": "Recommendation title",
  "description": "What to do and why",
  "priority": "Low" | "Medium" | "High" | "Critical",
  "confidence": 0.0-1.0,
  "expected_impact": "Business impact description",
  "estimated_revenue_improvement": number,
  "estimated_cost_savings": number,
  "actions": ["Action 1", "Action 2"]
}}]

Provide realistic, data-backed recommendations."""

            try:
                response = await llm.ainvoke(prompt)
                content = response.content.strip()

                # Extract JSON from response
                start_idx = content.find("[")
                end_idx = content.rfind("]") + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    llm_recs = json.loads(json_str)

                    for i, rec in enumerate(llm_recs):
                        recommendations.append({
                            "id": f"llm_{i}",
                            "title": rec.get("title", ""),
                            "description": rec.get("description", ""),
                            "priority": rec.get("priority", "Medium"),
                            "confidence": rec.get("confidence", 0.7),
                            "expected_impact": rec.get("expected_impact", ""),
                            "estimated_revenue_improvement": rec.get("estimated_revenue_improvement", 0),
                            "estimated_cost_savings": rec.get("estimated_cost_savings", 0),
                            "actions": rec.get("actions", []),
                        })
            except Exception as e:
                logger.warning(f"LLM recommendation generation failed: {e}")

        # Sort by priority and confidence
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        recommendations.sort(
            key=lambda x: (
                priority_order.get(x["priority"], 4),
                -x["confidence"]
            )
        )

        state.recommendations = recommendations

        logger.info(f"Generated {len(recommendations)} recommendations")

    except Exception as e:
        logger.error(f"Recommendation agent error: {e}")
        state.errors.append(f"Recommendations failed: {str(e)}")

    return state
