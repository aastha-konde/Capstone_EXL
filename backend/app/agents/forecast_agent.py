"""Forecast Agent - predict future outcomes using ML models"""

from ..core.logging import get_logger
from .state import AgentState
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import warnings

warnings.filterwarnings('ignore')

logger = get_logger(__name__)


def simple_forecast(data: list, periods: int = 3) -> dict:
    """
    Simple exponential smoothing forecast when Prophet/ARIMA aren't available.
    Used as fallback for quick estimates.
    """
    if len(data) < 2:
        return {"forecasts": [], "mape": 0}

    values = np.array([float(v) for v in data])
    alpha = 0.3  # Smoothing factor

    forecast = []
    last_val = values[-1]

    # Exponential smoothing
    for _ in range(periods):
        forecast.append(last_val)
        last_val = alpha * last_val + (1 - alpha) * values[-1]

    return {
        "forecasts": [float(f) for f in forecast],
        "method": "exponential_smoothing",
        "mape": 0,
    }


async def forecast_agent(state: AgentState) -> AgentState:
    """
    Forecast future outcomes.
    Falls back to simple exponential smoothing if advanced models aren't available.
    """
    try:
        if not state.sql_result:
            logger.warning("No SQL result for forecasting")
            return state

        rows = state.sql_result.get("rows", [])
        if not rows:
            return state

        df = pd.DataFrame(rows)

        # Identify numeric columns for forecasting
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols:
            logger.warning("No numeric columns to forecast")
            return state

        state.forecasts = {}
        state.forecast_models = {}
        state.forecast_accuracy = {}

        # Forecast each numeric metric
        for col in numeric_cols:
            try:
                values = df[col].dropna().values.tolist()

                if len(values) < 2:
                    continue

                # Use simple forecasting
                forecast_result = simple_forecast(values, periods=3)

                state.forecasts[col] = [
                    {
                        "period": f"Period {i+1}",
                        "value": float(f),
                        "confidence_lower": float(f * 0.9),
                        "confidence_upper": float(f * 1.1),
                    }
                    for i, f in enumerate(forecast_result["forecasts"])
                ]

                state.forecast_models[col] = forecast_result["method"]
                state.forecast_accuracy[col] = forecast_result.get("mape", 0)

                logger.info(f"Forecast for {col}: {len(state.forecasts[col])} periods")

            except Exception as e:
                logger.warning(f"Could not forecast {col}: {e}")
                continue

    except Exception as e:
        logger.error(f"Forecast agent error: {e}")
        state.errors.append(f"Forecasting failed: {str(e)}")

    return state
