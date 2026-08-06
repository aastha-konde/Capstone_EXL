"""Data service endpoints for business analytics.

All queries are written against the actual schema in
data_warehouse/schema/*.sql. Historical data spans 2020-01-01 to
2024-12-31 (see data_warehouse/generator/generate.py), so queries
anchor trailing-window calculations to MAX(date) in each table rather
than CURRENT_DATE, which would fall outside the data range.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from ..db import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["data-services"])


@router.get("/sales")
async def get_sales(db: Session = Depends(get_db)):
    """
    Get sales analytics: totals, YoY growth, by region, top products, monthly trend.
    """
    try:
        totals_query = """
        SELECT
            COUNT(*) AS total_orders,
            SUM(sales) AS total_revenue,
            AVG(sales) AS avg_order_value
        FROM sales
        """
        result = db.execute(text(totals_query)).fetchone()
        total_orders = result[0] or 0
        total_revenue = float(result[1]) if result[1] else 0.0
        avg_order_value = float(result[2]) if result[2] else 0.0

        by_region = [
            {"region": r[0], "revenue": float(r[1]) if r[1] else 0.0}
            for r in db.execute(text("""
                SELECT region, SUM(sales) AS revenue
                FROM sales
                GROUP BY region
                ORDER BY revenue DESC
            """)).fetchall()
        ]

        by_product = [
            {
                "product": f"{p[2]} ({p[1]})",
                "quantity": int(p[3]) if p[3] else 0,
                "revenue": float(p[4]) if p[4] else 0.0,
            }
            for p in db.execute(text("""
                SELECT s.product_id, p.category, p.brand,
                       SUM(s.quantity) AS quantity, SUM(s.sales) AS revenue
                FROM sales s
                JOIN products p ON p.product_id = s.product_id
                GROUP BY s.product_id, p.category, p.brand
                ORDER BY revenue DESC
                LIMIT 10
            """)).fetchall()
        ]

        trends = [
            {
                "month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                "revenue": float(t[1]) if t[1] else 0.0,
                "orders": t[2] or 0,
            }
            for t in db.execute(text("""
                WITH bounds AS (SELECT MAX(order_date) AS anchor FROM sales)
                SELECT DATE_TRUNC('month', order_date) AS month,
                       SUM(sales) AS revenue,
                       COUNT(*) AS orders
                FROM sales, bounds
                WHERE order_date >= DATE_TRUNC('month', bounds.anchor) - INTERVAL '11 months'
                GROUP BY DATE_TRUNC('month', order_date)
                ORDER BY month
            """)).fetchall()
        ]

        yoy_result = db.execute(text("""
            WITH bounds AS (SELECT MAX(order_date) AS anchor FROM sales)
            SELECT
                SUM(CASE WHEN order_date >= DATE_TRUNC('year', bounds.anchor)
                         THEN sales ELSE 0 END) AS current_year_revenue,
                SUM(CASE WHEN order_date >= DATE_TRUNC('year', bounds.anchor) - INTERVAL '1 year'
                          AND order_date < DATE_TRUNC('year', bounds.anchor)
                         THEN sales ELSE 0 END) AS prev_year_revenue
            FROM sales, bounds
        """)).fetchone()
        current_year_revenue = float(yoy_result[0]) if yoy_result[0] else 0.0
        prev_year_revenue = float(yoy_result[1]) if yoy_result[1] else 0.0
        yoy_growth = (
            (current_year_revenue - prev_year_revenue) / prev_year_revenue * 100
            if prev_year_revenue > 0 else 0.0
        )

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
async def get_finance(db: Session = Depends(get_db)):
    """
    Get financial analytics: totals, by department, monthly trend.
    """
    try:
        totals_query = """
        SELECT
            SUM(revenue) AS total_revenue,
            SUM(operating_cost + salary_cost + marketing_cost) AS total_cost,
            SUM(profit) AS total_profit
        FROM finance
        """
        result = db.execute(text(totals_query)).fetchone()
        total_revenue = float(result[0]) if result[0] else 0.0
        total_cost = float(result[1]) if result[1] else 0.0
        total_profit = float(result[2]) if result[2] else 0.0
        profit_margin = (total_profit / total_revenue) if total_revenue > 0 else 0.0

        by_department = [
            {
                "department": d[0],
                "revenue": float(d[1]) if d[1] else 0.0,
                "cost": float(d[2]) if d[2] else 0.0,
                "profit": float(d[3]) if d[3] else 0.0,
            }
            for d in db.execute(text("""
                SELECT department,
                       SUM(revenue) AS revenue,
                       SUM(operating_cost + salary_cost + marketing_cost) AS cost,
                       SUM(profit) AS profit
                FROM finance
                GROUP BY department
                ORDER BY profit DESC
            """)).fetchall()
        ]

        trends = [
            {
                "month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                "revenue": float(t[1]) if t[1] else 0.0,
                "cost": float(t[2]) if t[2] else 0.0,
                "profit": float(t[3]) if t[3] else 0.0,
            }
            for t in db.execute(text("""
                WITH bounds AS (SELECT MAX(month) AS anchor FROM finance)
                SELECT DATE_TRUNC('month', f.month) AS month,
                       SUM(f.revenue) AS revenue,
                       SUM(f.operating_cost + f.salary_cost + f.marketing_cost) AS cost,
                       SUM(f.profit) AS profit
                FROM finance f, bounds
                WHERE f.month >= DATE_TRUNC('month', bounds.anchor) - INTERVAL '11 months'
                GROUP BY DATE_TRUNC('month', f.month)
                ORDER BY month
            """)).fetchall()
        ]

        return {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "total_profit": total_profit,
            "profit_margin": profit_margin,
            "by_department": by_department,
            "trends": trends,
        }
    except Exception as e:
        logger.error(f"Failed to fetch finance data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch finance data: {str(e)}"
        )


@router.get("/marketing")
async def get_marketing(db: Session = Depends(get_db)):
    """
    Get marketing analytics: totals, by channel, top campaigns, monthly trend.
    """
    try:
        totals_query = """
        SELECT
            SUM(spend) AS total_spend,
            SUM(clicks) AS total_clicks,
            SUM(conversions) AS total_conversions,
            AVG(roi) AS avg_roi
        FROM marketing
        """
        result = db.execute(text(totals_query)).fetchone()
        total_spend = float(result[0]) if result[0] else 0.0
        total_clicks = int(result[1]) if result[1] else 0
        total_conversions = int(result[2]) if result[2] else 0
        avg_roi = float(result[3]) if result[3] else 0.0

        by_channel = [
            {
                "channel": c[0],
                "spend": float(c[1]) if c[1] else 0.0,
                "roi": float(c[2]) if c[2] else 0.0,
                "conversions": int(c[3]) if c[3] else 0,
            }
            for c in db.execute(text("""
                SELECT channel, SUM(spend) AS spend, AVG(roi) AS roi, SUM(conversions) AS conversions
                FROM marketing
                GROUP BY channel
                ORDER BY spend DESC
            """)).fetchall()
        ]

        campaigns = [
            {
                "campaign": c[0],
                "spend": float(c[1]) if c[1] else 0.0,
                "roi": float(c[2]) if c[2] else 0.0,
                "conversions": int(c[3]) if c[3] else 0,
            }
            for c in db.execute(text("""
                SELECT campaign_name, SUM(spend) AS spend, AVG(roi) AS roi, SUM(conversions) AS conversions
                FROM marketing
                GROUP BY campaign_name
                ORDER BY spend DESC
                LIMIT 10
            """)).fetchall()
        ]

        trends = [
            {
                "month": t[0].strftime('%b %Y') if t[0] else 'N/A',
                "spend": float(t[1]) if t[1] else 0.0,
                "conversions": int(t[2]) if t[2] else 0,
                "roi": float(t[3]) if t[3] else 0.0,
            }
            for t in db.execute(text("""
                WITH bounds AS (SELECT MAX(start_date) AS anchor FROM marketing)
                SELECT DATE_TRUNC('month', m.start_date) AS month,
                       SUM(m.spend) AS spend,
                       SUM(m.conversions) AS conversions,
                       AVG(m.roi) AS roi
                FROM marketing m, bounds
                WHERE m.start_date >= DATE_TRUNC('month', bounds.anchor) - INTERVAL '11 months'
                GROUP BY DATE_TRUNC('month', m.start_date)
                ORDER BY month
            """)).fetchall()
        ]

        return {
            "total_spend": total_spend,
            "total_clicks": total_clicks,
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
async def get_inventory(db: Session = Depends(get_db)):
    """
    Get inventory analytics: totals, low-stock alerts, warehouse breakdown,
    top products by value, and stock health by category.
    """
    try:
        totals_query = """
        SELECT
            SUM(i.stock_level) AS total_quantity,
            SUM(i.stock_level * p.selling_price) AS total_value
        FROM inventory i
        JOIN products p ON p.product_id = i.product_id
        """
        result = db.execute(text(totals_query)).fetchone()
        total_quantity = float(result[0]) if result[0] else 0.0
        total_value = float(result[1]) if result[1] else 0.0

        low_stock_count = db.execute(text("""
            SELECT COUNT(*) FROM inventory
            WHERE stock_level < reorder_level OR stock_out = TRUE
        """)).scalar() or 0

        turnover_rate = db.execute(text("""
            WITH sales_totals AS (
                SELECT
                    SUM(quantity) AS total_qty_sold,
                    GREATEST(EXTRACT(YEAR FROM MAX(order_date))::int
                             - EXTRACT(YEAR FROM MIN(order_date))::int + 1, 1) AS years_span
                FROM sales
            ),
            inv_totals AS (
                SELECT SUM(stock_level) AS total_stock FROM inventory
            )
            SELECT
                CASE WHEN inv_totals.total_stock > 0
                     THEN (sales_totals.total_qty_sold::float / sales_totals.years_span) / inv_totals.total_stock
                     ELSE 0 END
            FROM sales_totals, inv_totals
        """)).scalar()
        turnover_rate = float(turnover_rate) if turnover_rate else 0.0

        by_product = [
            {
                "product": f"{p[2]} ({p[1]})",
                "quantity": int(p[3]) if p[3] else 0,
                "reorder_point": int(p[4]) if p[4] else 0,
                "value": float(p[5]) if p[5] else 0.0,
                "status": p[6],
            }
            for p in db.execute(text("""
                SELECT i.product_id, p.category, p.brand,
                       i.stock_level, i.reorder_level,
                       i.stock_level * p.selling_price AS value,
                       CASE WHEN i.stock_level < i.reorder_level OR i.stock_out THEN 'low' ELSE 'normal' END AS status
                FROM inventory i
                JOIN products p ON p.product_id = i.product_id
                ORDER BY value DESC
                LIMIT 10
            """)).fetchall()
        ]

        warehouse = [
            {
                "warehouse": w[0],
                "total_items": int(w[1]),
                "value": float(w[2]) if w[2] else 0.0,
                "utilization": float(w[3]) if w[3] else 0.0,
            }
            for w in db.execute(text("""
                SELECT
                    'WH-' || LPAD((((i.warehouse_id - 1) % 12) + 1)::text, 2, '0') AS warehouse,
                    COUNT(*) AS total_items,
                    SUM(i.stock_level * p.selling_price) AS value,
                    ROUND(100.0 * SUM(CASE WHEN NOT i.stock_out THEN 1 ELSE 0 END) / COUNT(*), 1) AS utilization
                FROM inventory i
                JOIN products p ON p.product_id = i.product_id
                GROUP BY 1
                ORDER BY 1
            """)).fetchall()
        ]

        by_category = [
            {
                "category": c[0],
                "items": int(c[1]),
                "low_stock": int(c[2]),
                "value": float(c[3]) if c[3] else 0.0,
            }
            for c in db.execute(text("""
                SELECT p.category,
                       COUNT(*) AS items,
                       SUM(CASE WHEN i.stock_level < i.reorder_level OR i.stock_out THEN 1 ELSE 0 END) AS low_stock,
                       SUM(i.stock_level * p.selling_price) AS value
                FROM inventory i
                JOIN products p ON p.product_id = i.product_id
                GROUP BY p.category
                ORDER BY value DESC
            """)).fetchall()
        ]

        return {
            "total_value": total_value,
            "total_quantity": total_quantity,
            "low_stock_count": low_stock_count,
            "turnover_rate": turnover_rate,
            "by_product": by_product,
            "warehouse": warehouse,
            "by_category": by_category,
        }
    except Exception as e:
        logger.error(f"Failed to fetch inventory data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch inventory data: {str(e)}"
        )
