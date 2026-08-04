# Sample Questions for DecisionLens AI

These are example natural language questions you can ask the system. Each demonstrates different capabilities.

## Diagnostic Questions (Why?)

### Revenue & Sales

1. **"Why did revenue decline last quarter?"**
   - Expected: SQL on sales + finance, variance analysis, trend detection
   - Output: KPIs (revenue down X%), root causes (seasonality, discounts), trends

2. **"Which region is underperforming?"**
   - Expected: Regional sales comparison, region-level metrics
   - Output: South/North/East/West sales, profit margins by region

3. **"Why are customers in the Northeast churning?"**
   - Expected: Sales trend analysis for Northeast, support ticket analysis
   - Output: Churn rate, root causes (long delivery times, support issues), timeline

### Operations & Inventory

4. **"Which warehouse is causing delayed deliveries?"**
   - Expected: Inventory × sales analysis, delivery time correlation
   - Output: Average delivery time by warehouse, stock-out rate, supplier delays

5. **"Why are inventory costs increasing?"**
   - Expected: Inventory × finance analysis
   - Output: Stock levels trending, reorder costs, supplier delays impact

### Marketing & Customers

6. **"Which marketing campaigns generated poor ROI?"**
   - Expected: Marketing table analysis, ROI ranking, channel comparison
   - Output: Campaign list ranked by ROI, best/worst performers, spend efficiency

7. **"Why are customer complaints increasing?"**
   - Expected: Support tickets trend, customer segments, issue type breakdown
   - Output: Complaint volume trend, issue types (delivery, quality, billing), CSAT drop

## Predictive Questions (What will happen?)

8. **"What will next quarter revenue be?"**
   - Expected: Forecast agent runs time series models, returns confidence interval
   - Output: Q4 forecast ($X-Y million), model (Prophet/ARIMA/XGBoost), confidence (95%)

9. **"Which customers are likely to churn in the next 6 months?"**
   - Expected: Churn prediction model, customer segmentation
   - Output: At-risk customer count, top risk factors, prediction confidence

10. **"Forecast demand for Q4 by product category?"**
    - Expected: Time series by category, seasonal adjustment
    - Output: Forecast by Electronics/Home/Clothing/etc., seasonality factors

## Prescriptive Questions (What should we do?)

11. **"What actions should we take to improve profitability?"**
    - Expected: KPI analysis → margin issues → rules engine → LLM recommendations
    - Output: Top 3 recommendations (reduce discounts, optimize supplier, increase prices)
              with confidence, estimated impact, and implementation steps

12. **"Which products should we discontinue?"**
    - Expected: Product profitability analysis, demand prediction
    - Output: Low-margin products, declining trends, discontinuation ROI

13. **"How can we reduce our inventory costs?"**
    - Expected: Inventory × finance analysis, supplier performance
    - Output: Recommendations: improve forecasting, reduce safety stock, switch suppliers
              with cost savings estimates

14. **"What should we do to reduce customer complaints?"**
    - Expected: Support ticket analysis, root cause identification
    - Output: Recommendations: improve warehouse ops, faster resolution, SLA changes
              with impact (expected CSAT improvement)

## Segment-Specific Questions

15. **"Compare profitability across customer segments"**
    - Expected: Customer segment analysis, RFM segmentation
    - Output: Premium vs Standard vs Budget segment profit, retention, LTV

16. **"Which departments are exceeding their targets?"**
    - Expected: Finance vs targets comparison
    - Output: Department performance table, over/under-budget analysis, trends

17. **"Analyze sales performance by salesperson in Q3"**
    - Expected: Sales agent ranking, quota attainment
    - Output: Top/bottom performers, revenue per person, quota achievement %

## Time-Bound Questions

18. **"How did we perform during the Black Friday campaign?"**
    - Expected: Sales spike detection, campaign impact analysis
    - Output: Campaign metrics (revenue, profit, ROI), vs normal sales

19. **"What was the impact of the price increase in February?"**
    - Expected: Price change detection, time series before/after
    - Output: Revenue change, volume impact, margin improvement

## Comparative Questions

20. **"How does our East region compare to competitors' estimated performance?"**
    - Expected: (Note: Requires competitor data; can use internal benchmarks)
    - Output: Regional position, gap to targets, improvement recommendations

---

## Expected Response Structure

Every question triggers the full pipeline:

```json
{
  "session_id": "uuid",
  "question": "Why did revenue decline last quarter?",
  "intent": "diagnostic",
  "sql_result": {
    "rows": [...],
    "columns": ["month", "revenue", "profit"],
    "row_count": 12
  },
  "analytics": {
    "kpis": {
      "total_revenue": {"value": 2500000, "unit": "$"},
      "avg_profit_margin": {"value": 0.12, "unit": "%"}
    },
    "trends": [{"metric": "revenue", "change_percent": -19.4, "direction": "decreasing"}],
    "anomalies": [],
    "root_causes": ["Discount increased to 18%", "Supplier delays"]
  },
  "forecasts": {
    "revenue": [
      {
        "period": "Period 1",
        "value": 2800000,
        "confidence_lower": 2600000,
        "confidence_upper": 3000000
      }
    ]
  },
  "recommendations": [
    {
      "title": "Reduce discounts to improve margins",
      "priority": "High",
      "confidence": 0.92,
      "expected_impact": "8-12% margin improvement",
      "estimated_revenue_improvement": 200000
    }
  ],
  "executive_summary": {
    "key_findings": ["Revenue down 19.4% vs prior quarter"],
    "root_causes": ["Aggressive discounting", "Supplier delays"],
    "future_risks": ["Continued downward trend if not addressed"],
    "recommended_actions": [
      {"action": "Restore normal discount levels", "priority": "High", "impact": "+8% margin"}
    ],
    "narrative": "DecisionLens analysis shows..."
  },
  "response_time_ms": 2345.67
}
```

## Tips for Getting Better Results

1. **Be specific:** "South region Q3" vs "regions"
2. **Ask one thing:** Don't combine multiple questions
3. **Use timeframes:** "Last quarter," "past 6 months," "Q4 forecast"
4. **Include metrics:** "profitability," "growth," "churn" (vs vague "performance")
5. **Follow up:** "Why?" builds on prior analysis using conversation history

---

## Testing the API Directly

### Using curl:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Why did revenue decline last quarter?"}'
```

### Using Python:

```python
import requests

response = requests.post(
    'http://localhost:8000/api/chat',
    json={'question': 'Which region is underperforming?'}
)

print(response.json())
```

### Expected Response Time

- Simple diagnostic: 3-5 seconds (SQL + analytics)
- With forecasting: 8-12 seconds (adds Prophet/ARIMA)
- With recommendations: 12-18 seconds (adds LLM reasoning)

---

**Last Updated:** 2026-08-04  
**Version:** 1.0
