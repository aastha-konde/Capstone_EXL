"""Anomaly detection using Isolation Forest"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any


def detect_anomalies(
    data: pd.DataFrame,
    columns: List[str] = None,
    contamination: float = 0.05,
) -> Dict[str, Any]:
    """
    Detect anomalies using Isolation Forest.
    """
    try:
        from sklearn.ensemble import IsolationForest

        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns.tolist()

        if not columns:
            return {"anomalies": [], "count": 0}

        # Prepare data
        X = data[columns].fillna(data[columns].mean()).values

        # Fit Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(X)

        # Get anomalies
        anomaly_indices = np.where(predictions == -1)[0]

        anomalies = []
        for idx in anomaly_indices:
            anomalies.append({
                "index": int(idx),
                "values": {col: float(data[col].iloc[idx]) for col in columns},
            })

        return {
            "anomalies": anomalies,
            "count": len(anomalies),
            "percentage": round(len(anomalies) / len(data) * 100, 2),
        }

    except ImportError:
        return {
            "anomalies": [],
            "count": 0,
            "error": "scikit-learn not available"
        }
    except Exception as e:
        return {
            "anomalies": [],
            "count": 0,
            "error": str(e)
        }


def iqr_anomalies(data: pd.DataFrame, columns: List[str] = None) -> Dict[str, Any]:
    """
    Simple IQR-based anomaly detection.
    Useful as a lightweight alternative to Isolation Forest.
    """
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()

    anomalies = []
    for col in columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1

        outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]

        for idx in outliers.index:
            anomalies.append({
                "column": col,
                "index": int(idx),
                "value": float(data[col].iloc[idx]),
                "q1": float(Q1),
                "q3": float(Q3),
            })

    return {
        "anomalies": anomalies,
        "count": len(anomalies),
        "method": "iqr",
    }
