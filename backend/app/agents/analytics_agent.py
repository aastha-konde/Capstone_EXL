"""Analytics Agent - calculate KPIs and identify trends"""

from ..core.logging import get_logger
from .state import AgentState
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

logger = get_logger(__name__)


def calculate_kpis(sql_result: dict, question: str) -> dict:
    """Calculate KPIs from SQL result"""
    if not sql_result or not sql_result.get("rows"):
        return {}

    rows = sql_result["rows"]
    df = pd.DataFrame(rows)

    kpis = {}

    # Calculate basic statistics on numeric columns
    for col in df.select_dtypes(include=[np.number]).columns:
        kpis[col] = {
            "value": float(df[col].sum()) if col in ["sales", "profit", "revenue"] else float(df[col].mean()),
            "unit": "$" if "sales" in col or "profit" in col or "revenue" in col else "",
            "count": int(df[col].count()),
        }

    # Count operations
    for col in df.columns:
        if col == "customer_id":
            kpis["unique_customers"] = {
                "value": int(df[col].nunique()),
                "unit": "count"
            }
        elif col == "product_id":
            kpis["unique_products"] = {
                "value": int(df[col].nunique()),
                "unit": "count"
            }

    return kpis


def identify_anomalies(sql_result: dict) -> list:
    """Identify anomalies in the data"""
    if not sql_result or not sql_result.get("rows"):
        return []

    rows = sql_result["rows"]
    df = pd.DataFrame(rows)
    anomalies = []

    # Find outliers in numeric columns using IQR method
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

        if len(outliers) > 0:
            anomalies.append({
                "field": col,
                "count": len(outliers),
                "percentage": round(len(outliers) / len(df) * 100, 2),
            })

    return anomalies


def identify_trends(sql_result: dict) -> list:
    """Identify trends in the data"""
    if not sql_result or not sql_result.get("rows"):
        return []

    rows = sql_result["rows"]
    df = pd.DataFrame(rows)
    trends = []

    # Look for date columns to identify time-based trends
    date_cols = [col for col in df.columns if "date" in col.lower()]

    if date_cols and len(df) > 1:
        date_col = date_cols[0]
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        for metric in numeric_cols:
            if len(df) > 1:
                first_val = df[metric].iloc[0]
                last_val = df[metric].iloc[-1]

                if first_val != 0:
                    change = ((last_val - first_val) / first_val) * 100
                    direction = "increasing" if change > 0 else "decreasing"

                    trends.append({
                        "metric": metric,
                        "change_percent": round(change, 2),
                        "direction": direction,
                    })

    return trends


async def analytics_agent(state: AgentState) -> AgentState:
    """
    Calculate KPIs, identify trends, and find anomalies.
    Operates on the SQL result data.
    """
    try:
        if not state.sql_result:
            logger.warning("No SQL result to analyze")
            return state

        # Calculate KPIs
        kpis = calculate_kpis(state.sql_result, state.question)
        state.kpis = kpis

        # Find anomalies
        anomalies = identify_anomalies(state.sql_result)
        state.anomalies = anomalies

        # Identify trends
        trends = identify_trends(state.sql_result)
        state.trends = trends

        # Simple root cause heuristics
        root_causes = []
        if anomalies:
            root_causes.append(f"Detected {len(anomalies)} anomalies in the data")

        if any(t["change_percent"] < -20 for t in trends):
            root_causes.append("Significant downward trend detected in key metrics")

        if any(t["change_percent"] > 50 for t in trends):
            root_causes.append("Unusual spike detected in key metrics")

        state.root_causes = root_causes

        logger.info(f"Analytics: {len(state.kpis)} KPIs, {len(anomalies)} anomalies, {len(trends)} trends")

    except Exception as e:
        logger.error(f"Analytics agent error: {e}")
        state.errors.append(f"Analytics failed: {str(e)}")

    return state
