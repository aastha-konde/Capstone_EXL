"""Intent Detection Agent - classify question type and required tables"""

from langchain_google_genai import ChatGoogleGenerativeAI
from ..core.config import settings
from ..core.logging import get_logger
from .state import AgentState
import json

logger = get_logger(__name__)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    api_key=settings.gemini_api_key,
    temperature=settings.llm_temperature,
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

        # Handle both string and list responses from Gemini
        if isinstance(response.content, list):
            # Gemini returns list of content blocks
            content = response.content[0]['text'] if response.content else ""
        else:
            content = response.content

        content = content.strip()

        # Remove markdown JSON backticks if present
        content = content.replace("```json", "").replace("```", "").strip()

        result = json.loads(content)

        state.intent = result.get("intent", "diagnostic")
        state.required_tables = result.get("required_tables", [])

        logger.info(f"Intent detected: {state.intent}, tables: {state.required_tables}")

    except json.JSONDecodeError as e:
        logger.error(f"Intent agent JSON error: {e}")
        # Fallback
        state.intent = "diagnostic"
        state.required_tables = ["sales", "customers", "products"]
    except Exception as e:
        logger.error(f"Intent agent error: {e}")
        state.errors.append(f"Intent detection failed: {str(e)}")
        state.intent = "diagnostic"
        state.required_tables = ["sales", "customers", "products"]

    return state
