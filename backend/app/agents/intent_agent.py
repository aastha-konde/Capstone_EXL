"""Intent Detection Agent - classify question type and required tables"""

from langchain_openai import ChatOpenAI
from ..core.config import settings
from ..core.logging import get_logger
from .state import AgentState
import json

logger = get_logger(__name__)

# Initialize LLM
llm = ChatOpenAI(
    model=settings.openrouter_model,
    temperature=settings.llm_temperature,
    openai_api_key=settings.openrouter_api_key,
    openai_api_base=settings.openrouter_base_url,
)


async def intent_agent(state: AgentState) -> AgentState:
    """
    Classify the user's question and determine which tables are needed.
    This helps route the question to the appropriate downstream agents.
    """
    try:
        prompt = f"""Analyze this business question and classify it.

Question: {state.question}

Respond with JSON:
{{
  "intent": "diagnostic" | "predictive" | "prescriptive",
  "required_tables": ["table1", "table2", ...],
  "explanation": "brief explanation of the question type"
}}

Available tables: customers, products, sales, inventory, marketing, finance, employees, support_tickets, targets, calendar

Intent types:
- diagnostic: "Why did X happen?" - requires analysis of what happened
- predictive: "What will happen?" - requires forecasting
- prescriptive: "What should we do?" - requires recommendations

Respond only with valid JSON."""

        response = await llm.ainvoke(prompt)
        result = json.loads(response.content)

        state.intent = result.get("intent", "diagnostic")
        state.required_tables = result.get("required_tables", [])

        logger.info(f"Intent detected: {state.intent}, tables: {state.required_tables}")

    except Exception as e:
        logger.error(f"Intent agent error: {e}")
        state.errors.append(f"Intent detection failed: {str(e)}")
        state.intent = "diagnostic"  # Default fallback
        state.required_tables = ["sales", "customers", "products"]  # Common fallback

    return state
