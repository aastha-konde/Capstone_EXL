"""Data service endpoints for business analytics"""

from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
import logging
from ..db import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["data-services"])


@router.get("/sales")
async def get_sales(db: Session = next(get_db())):
    """
    Get sales analytics data including revenue, orders, and trends.
    """
    try:
        # Query total revenue and orders
        sales_query = """
        SELECT
            COUNT(*) as total_orders,
            SUM(CAST(sales_amount AS FLOAT)) as total_revenue,
            AVG(CAST(sales_amount AS FLOAT)) as avg_order_value
        FROM sales
        WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE)
        """

        result = db.execute(text(sales_query)).fetchone()

        # Query by region
        region_query = """
        SELECT region, SUM(CAST(sales_amount AS FLOAT)) as revenue
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
        """
        by_region = [{"region": r[0], "revenue": float(r[1]) if r[1] else 0}
                     for r in db.execute(text(region_query)).fetchall()]

        # Query by product
        product_query = """
        SELECT product_id, COUNT(*) as quantity, SUM(CAST(sales_amount AS FLOAT)) as revenue
        FROM sales
        GROUP BY product_id
        ORDER BY revenue DESC
        LIMIT 10
        """
        by_product = [{"product": f"Product {p[0]}", "quantity": p[1], "revenue": float(p[2]) if p[2] else 0}
                      for p in db.execute(text(product_query)).fetchall()]

        # Query trends (last 12 months)
        trends_query = """
        SELECT
            DATE_TRUNC('month', order_date) as month,
            SUM(CAST(sales_amount AS FLOAT)) as revenue,
            COUNT(*) as orders
        FROM sales
        WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY DATE_TRUNC('month', order_date)
        ORDER BY month
        """
        trends = [{"month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                   "revenue": float(t[1]) if t[1] else 0,
                   "orders": t[2] if t[2] else 0}
                  for t in db.execute(text(trends_query)).fetchall()]

        total_revenue = float(result[1]) if result[1] else 0
        total_orders = result[0] if result[0] else 0
        avg_order_value = float(result[2]) if result[2] else 0

        # Calculate YoY growth
        prev_year_query = """
        SELECT SUM(CAST(sales_amount AS FLOAT))
        FROM sales
        WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE - INTERVAL '1 year')
        AND order_date < DATE_TRUNC('year', CURRENT_DATE)
        """
        prev_year_revenue = float(db.execute(text(prev_year_query)).scalar() or 0)
        yoy_growth = ((total_revenue - prev_year_revenue) / prev_year_revenue * 100) if prev_year_revenue > 0 else 0

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "avg_order_value": avg_order_value,
            "yoy_growth": yoy_growth,
            "by_region": by_region,
            "by_product": by_product,
            "trends": trends,
        }
    except Exception as e:
        logger.error(f"Failed to fetch sales data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch sales data: {str(e)}"
        )


@router.get("/finance")
async def get_finance(db: Session = next(get_db())):
    """
    Get financial analytics including revenue, costs, and profit.
    """
    try:
        # Query total financials
        finance_query = """
        SELECT
            SUM(CAST(revenue AS FLOAT)) as total_revenue,
            SUM(CAST(cost AS FLOAT)) as total_cost,
            SUM(CAST(profit AS FLOAT)) as total_profit
        FROM finance
        WHERE period_date >= DATE_TRUNC('year', CURRENT_DATE)
        """

        result = db.execute(text(finance_query)).fetchone()

        total_revenue = float(result[0]) if result[0] else 0
        total_cost = float(result[1]) if result[1] else 0
        total_profit = float(result[2]) if result[2] else 0
        profit_margin = (total_profit / total_revenue) if total_revenue > 0 else 0

        # Query by region
        region_query = """
        SELECT region, SUM(CAST(revenue AS FLOAT)), SUM(CAST(cost AS FLOAT)), SUM(CAST(profit AS FLOAT))
        FROM finance
        GROUP BY region
        ORDER BY profit DESC
        """
        by_region = [{"region": r[0], "revenue": float(r[1]) if r[1] else 0,
                      "cost": float(r[2]) if r[2] else 0, "profit": float(r[3]) if r[3] else 0}
                     for r in db.execute(text(region_query)).fetchall()]

        # Query by category
        category_query = """
        SELECT category, SUM(CAST(revenue AS FLOAT)), SUM(CAST(profit AS FLOAT))
        FROM finance
        GROUP BY category
        ORDER BY revenue DESC
        """
        by_category = [{"category": c[0], "revenue": float(c[1]) if c[1] else 0, "profit": float(c[2]) if c[2] else 0}
                       for c in db.execute(text(category_query)).fetchall()]

        # Query trends
        trends_query = """
        SELECT
            DATE_TRUNC('month', period_date) as month,
            SUM(CAST(revenue AS FLOAT)) as revenue,
            SUM(CAST(cost AS FLOAT)) as cost,
            SUM(CAST(profit AS FLOAT)) as profit
        FROM finance
        WHERE period_date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY DATE_TRUNC('month', period_date)
        ORDER BY month
        """
        trends = [{"month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                   "revenue": float(t[1]) if t[1] else 0,
                   "cost": float(t[2]) if t[2] else 0,
                   "profit": float(t[3]) if t[3] else 0}
                  for t in db.execute(text(trends_query)).fetchall()]

        return {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "total_profit": total_profit,
            "profit_margin": profit_margin,
            "by_region": by_region,
            "by_category": by_category,
            "trends": trends,
        }
    except Exception as e:
        logger.error(f"Failed to fetch finance data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch finance data: {str(e)}"
        )


@router.get("/marketing")
async def get_marketing(db: Session = next(get_db())):
    """
    Get marketing analytics including campaigns, spend, and ROI.
    """
    try:
        # Query total marketing metrics
        marketing_query = """
        SELECT
            SUM(CAST(spend AS FLOAT)) as total_spend,
            SUM(CAST(impressions AS FLOAT)) as total_impressions,
            SUM(CAST(conversions AS FLOAT)) as total_conversions
        FROM marketing
        WHERE campaign_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '3 months')
        """

        result = db.execute(text(marketing_query)).fetchone()

        total_spend = float(result[0]) if result[0] else 0
        total_impressions = float(result[1]) if result[1] else 0
        total_conversions = float(result[2]) if result[2] else 0

        # Query by channel
        channel_query = """
        SELECT channel, SUM(CAST(spend AS FLOAT)), AVG(CAST(roi AS FLOAT)), SUM(CAST(conversions AS FLOAT))
        FROM marketing
        GROUP BY channel
        ORDER BY spend DESC
        """
        by_channel = [{"channel": c[0], "spend": float(c[1]) if c[1] else 0,
                       "roi": float(c[2]) if c[2] else 0, "conversions": int(c[3]) if c[3] else 0}
                      for c in db.execute(text(channel_query)).fetchall()]

        # Query campaigns
        campaigns_query = """
        SELECT campaign_id, SUM(CAST(spend AS FLOAT)), AVG(CAST(roi AS FLOAT)), SUM(CAST(conversions AS FLOAT))
        FROM marketing
        GROUP BY campaign_id
        ORDER BY spend DESC
        LIMIT 10
        """
        campaigns = [{"campaign": f"Campaign {c[0]}", "spend": float(c[1]) if c[1] else 0,
                      "roi": float(c[2]) if c[2] else 0, "conversions": int(c[3]) if c[3] else 0}
                     for c in db.execute(text(campaigns_query)).fetchall()]

        # Calculate average ROI
        avg_roi_query = "SELECT AVG(CAST(roi AS FLOAT)) FROM marketing"
        avg_roi = float(db.execute(text(avg_roi_query)).scalar() or 0)

        # Query trends
        trends_query = """
        SELECT
            DATE_TRUNC('month', campaign_date) as month,
            SUM(CAST(spend AS FLOAT)) as spend,
            SUM(CAST(conversions AS FLOAT)) as conversions,
            AVG(CAST(roi AS FLOAT)) as roi
        FROM marketing
        WHERE campaign_date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY DATE_TRUNC('month', campaign_date)
        ORDER BY month
        """
        trends = [{"month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                   "spend": float(t[1]) if t[1] else 0,
                   "conversions": float(t[2]) if t[2] else 0,
                   "roi": float(t[3]) if t[3] else 0}
                  for t in db.execute(text(trends_query)).fetchall()]

        return {
            "total_spend": total_spend,
            "total_impressions": total_impressions,
            "total_conversions": total_conversions,
            "avg_roi": avg_roi,
            "by_channel": by_channel,
            "campaigns": campaigns,
            "trends": trends,
        }
    except Exception as e:
        logger.error(f"Failed to fetch marketing data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch marketing data: {str(e)}"
        )


@router.get("/inventory")
async def get_inventory(db: Session = next(get_db())):
    """
    Get inventory analytics including stock levels and warehouse status.
    """
    try:
        # Query total inventory
        inventory_query = """
        SELECT
            SUM(CAST(quantity_on_hand AS FLOAT)) as total_quantity,
            SUM(CAST(stock_value AS FLOAT)) as total_value
        FROM inventory
        """

        result = db.execute(text(inventory_query)).fetchone()

        total_quantity = float(result[0]) if result[0] else 0
        total_value = float(result[1]) if result[1] else 0

        # Count low stock items
        low_stock_query = """
        SELECT COUNT(*) FROM inventory
        WHERE quantity_on_hand < reorder_point
        """
        low_stock_count = db.execute(text(low_stock_query)).scalar() or 0

        # Calculate average turnover rate
        turnover_query = "SELECT AVG(CAST(turnover_rate AS FLOAT)) FROM inventory"
        turnover_rate = float(db.execute(text(turnover_query)).scalar() or 0)

        # Query by product
        product_query = """
        SELECT product_id, quantity_on_hand, reorder_point, stock_value,
               CASE WHEN quantity_on_hand < reorder_point THEN 'low' ELSE 'normal' END as status
        FROM inventory
        ORDER BY stock_value DESC
        LIMIT 10
        """
        by_product = [{"product": f"Product {p[0]}", "quantity": float(p[1]) if p[1] else 0,
                       "reorder_point": float(p[2]) if p[2] else 0, "value": float(p[3]) if p[3] else 0,
                       "status": p[4]}
                      for p in db.execute(text(product_query)).fetchall()]

        # Query by warehouse
        warehouse_query = """
        SELECT warehouse_id, COUNT(*) as total_items, SUM(CAST(stock_value AS FLOAT)) as value,
               CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM inventory) AS FLOAT) as utilization
        FROM inventory
        GROUP BY warehouse_id
        """
        warehouse = [{"warehouse": f"Warehouse {w[0]}", "total_items": w[1],
                      "value": float(w[2]) if w[2] else 0, "utilization": float(w[3]) if w[3] else 0}
                     for w in db.execute(text(warehouse_query)).fetchall()]

        # Query trends (last 12 months)
        trends_query = """
        SELECT
            DATE_TRUNC('month', CURRENT_DATE) as month,
            SUM(CAST(quantity_on_hand AS FLOAT)) as quantity,
            SUM(CAST(stock_value AS FLOAT)) as value,
            AVG(CAST(turnover_rate AS FLOAT)) as turnover
        FROM inventory
        GROUP BY DATE_TRUNC('month', CURRENT_DATE)
        ORDER BY month
        """
        trends = [{"month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                   "quantity": float(t[1]) if t[1] else 0,
                   "value": float(t[2]) if t[2] else 0,
                   "turnover": float(t[3]) if t[3] else 0}
                  for t in db.execute(text(trends_query)).fetchall()]

        return {
            "total_value": total_value,
            "total_quantity": total_quantity,
            "low_stock_count": low_stock_count,
            "turnover_rate": turnover_rate,
            "by_product": by_product,
            "warehouse": warehouse,
            "trends": trends,
        }
    except Exception as e:
        logger.error(f"Failed to fetch inventory data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch inventory data: {str(e)}"
        )
