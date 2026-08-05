"""SQL Agent - convert NL to SQL and execute on DuckDB"""

from langchain_google_genai import ChatGoogleGenerativeAI
import duckdb
from ..core.config import settings
from ..core.logging import get_logger
from .state import AgentState
import json
import re

logger = get_logger(__name__)

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    api_key=settings.gemini_api_key,
    temperature=0.2,
)

# Database schema
SCHEMA_DESCRIPTION = """
Tables:
- customers: customer_id, gender, age, city, state, segment, joining_date, lifetime_value, income_group, loyalty_level
- products: product_id, category, subcategory, supplier, brand, cost, selling_price, launch_date, status
- sales: order_id, customer_id, product_id, quantity, discount, sales, profit, region, warehouse, salesperson, order_date, delivery_date, returned, payment_type
- inventory: warehouse_id, product_id, stock_level, reorder_level, lead_time, supplier_delay, stock_out
- marketing: campaign_id, campaign_name, channel, region, budget, spend, clicks, conversions, roi, start_date, end_date
- finance: month, department, operating_cost, salary_cost, marketing_cost, profit, revenue, budget
- employees: employee_id, department, manager, region, experience, performance_score, attrition, salary
- support_tickets: ticket_id, customer_id, issue_type, priority, resolution_time, satisfaction, created_date, closed_date
- targets: month, department, sales_target, profit_target, customer_target
- calendar: date, month, quarter, year, day_of_week, is_weekend, is_holiday, is_promotion_day
"""


def validate_sql(sql: str) -> bool:
    """Ensure the query is read-only (SELECT only)"""
    sql_upper = sql.upper().strip()

    # Only allow SELECT queries
    if not sql_upper.startswith("SELECT"):
        return False

    # Deny dangerous operations
    dangerous = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
    for cmd in dangerous:
        if cmd in sql_upper:
            return False

    return True


async def sql_agent(state: AgentState) -> AgentState:
    """
    Convert natural language question to SQL and execute on DuckDB.
    Only supports SELECT queries (read-only).
    """
    try:
        prompt = f"""Convert this business question to SQL for a DuckDB database.

{SCHEMA_DESCRIPTION}

Question: {state.question}

Generate a single SQL SELECT query that answers the question. Respond with ONLY the SQL query, no explanation."""

        response = await llm.ainvoke(prompt)

        # Handle both string and list responses from Gemini
        if isinstance(response.content, list):
            sql_query = response.content[0]['text'] if response.content else ""
        else:
            sql_query = response.content

        sql_query = sql_query.strip()

        # Clean up response (LLM might add markdown backticks)
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        logger.info(f"Generated SQL: {sql_query}")

        # Validate query (read-only guard)
        if not validate_sql(sql_query):
            state.sql_error = "Query must be SELECT only (read-only access)"
            state.errors.append(state.sql_error)
            logger.warning(f"Query blocked: {sql_query}")
            return state

        state.sql_query = sql_query

        # Execute on DuckDB
        db_path = settings.resolved_duckdb_path
        logger.debug(f"Connecting to DuckDB at: {db_path}")
        conn = duckdb.connect(db_path, read_only=True)
        try:
            result = conn.execute(sql_query).fetchall()
            columns = [desc[0] for desc in conn.description] if conn.description else []

            # Convert to list of dicts
            rows = [dict(zip(columns, row)) for row in result]

            state.sql_result = {
                "rows": rows,
                "columns": columns,
                "row_count": len(rows),
            }

            logger.info(f"SQL executed: {len(rows)} rows, {len(columns)} columns")

        finally:
            conn.close()

    except Exception as e:
        state.sql_error = str(e)
        state.errors.append(f"SQL execution failed: {str(e)}")
        logger.error(f"SQL agent error: {e}")

    return state
