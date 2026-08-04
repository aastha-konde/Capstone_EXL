"""Customer segmentation and RFM analysis"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any


def rfm_analysis(
    sales_data: pd.DataFrame,
    customer_column: str = "customer_id",
    date_column: str = "order_date",
    amount_column: str = "sales",
) -> Dict[str, Any]:
    """
    RFM (Recency, Frequency, Monetary) analysis for customer segmentation.
    """
    try:
        # Calculate RFM metrics
        current_date = pd.to_datetime(sales_data[date_column]).max()

        rfm = sales_data.groupby(customer_column).agg({
            date_column: lambda x: (current_date - pd.to_datetime(x).max()).days,
            customer_column: 'count',
            amount_column: 'sum',
        }).rename(columns={
            date_column: 'recency',
            customer_column: 'frequency',
            amount_column: 'monetary',
        })

        # Quartile-based segmentation
        rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
        rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1, 2, 3, 4], duplicates='drop')

        # Combine scores
        rfm['rfm_score'] = (
            rfm['r_score'].astype(int) * 100 +
            rfm['f_score'].astype(int) * 10 +
            rfm['m_score'].astype(int)
        )

        # Segment labels
        def segment_name(score):
            if score >= 444:
                return "Champions"
            elif score >= 334:
                return "Loyal Customers"
            elif score >= 224:
                return "Potential Loyalists"
            elif score >= 114:
                return "At Risk"
            else:
                return "Lost"

        rfm['segment'] = rfm['rfm_score'].apply(segment_name)

        return {
            "rfm": rfm.to_dict('index'),
            "segments": rfm['segment'].value_counts().to_dict(),
            "average_ltv": float(rfm['monetary'].mean()),
        }

    except Exception as e:
        return {
            "error": str(e),
            "rfm": {},
            "segments": {},
        }


def segment_customers(
    data: pd.DataFrame,
    n_clusters: int = 4,
    features: List[str] = None,
) -> Dict[str, Any]:
    """
    Customer segmentation using K-Means clustering.
    """
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler

        if features is None:
            features = data.select_dtypes(include=[np.number]).columns.tolist()

        if not features:
            return {"error": "No numeric features", "segments": []}

        # Prepare data
        X = data[features].fillna(data[features].mean()).values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        # Analyze clusters
        segments = {}
        for cluster_id in range(n_clusters):
            mask = clusters == cluster_id
            segment_data = data[mask]

            segments[f"Segment_{cluster_id}"] = {
                "size": int(mask.sum()),
                "percentage": round(mask.sum() / len(data) * 100, 2),
                "characteristics": {
                    feat: float(segment_data[feat].mean())
                    for feat in features
                },
            }

        return {
            "segments": segments,
            "n_clusters": n_clusters,
            "inertia": float(kmeans.inertia_),
        }

    except ImportError:
        return {
            "error": "scikit-learn not available",
            "segments": [],
        }
    except Exception as e:
        return {
            "error": str(e),
            "segments": [],
        }
