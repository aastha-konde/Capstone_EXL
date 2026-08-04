"""Model evaluation metrics"""

import numpy as np
import pandas as pd
from typing import Tuple, List


def calculate_mape(actual: List[float], predicted: List[float]) -> float:
    """
    Mean Absolute Percentage Error.
    """
    actual = np.array(actual)
    predicted = np.array(predicted)

    # Avoid division by zero
    mask = actual != 0
    if not mask.any():
        return 0.0

    return float(np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100)


def calculate_rmse(actual: List[float], predicted: List[float]) -> float:
    """
    Root Mean Squared Error.
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    return float(np.sqrt(np.mean((actual - predicted) ** 2)))


def calculate_mae(actual: List[float], predicted: List[float]) -> float:
    """
    Mean Absolute Error.
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    return float(np.mean(np.abs(actual - predicted)))


def calculate_r2(actual: List[float], predicted: List[float]) -> float:
    """
    R-squared (coefficient of determination).
    """
    actual = np.array(actual)
    predicted = np.array(predicted)

    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)

    if ss_tot == 0:
        return 0.0

    return float(1 - (ss_res / ss_tot))


def model_accuracy(
    actual: List[float],
    predicted: List[float],
    threshold: float = 0.1
) -> Dict[str, float]:
    """
    Overall model accuracy metrics.
    """
    actual = np.array(actual)
    predicted = np.array(predicted)

    mape = calculate_mape(actual, predicted)
    rmse = calculate_rmse(actual, predicted)
    mae = calculate_mae(actual, predicted)
    r2 = calculate_r2(actual, predicted)

    # Accuracy based on % error threshold
    pct_error = np.abs((actual - predicted) / actual)
    accuracy = (pct_error < threshold).sum() / len(actual) * 100

    return {
        "mape": mape,
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "accuracy": accuracy,
    }
