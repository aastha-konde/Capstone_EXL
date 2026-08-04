# DecisionLens AI - System Architecture

## Overview

DecisionLens AI is a multi-agent enterprise decision intelligence platform built with LangGraph, FastAPI, and modern ML models.

```
User Question (NL)
    ↓
┌─ FastAPI /chat endpoint ─┐
│                          │
│  Intent Detection Agent   │
│  ├─ Classify question    │
│  ├─ Route to tables      │
│  └─ Choose agent path    │
│          ↓               │
│  SQL Agent              │
│  ├─ Generate SQL        │
│  ├─ Validate (read-only)│
│  └─ Execute on DuckDB   │
│          ↓               │
│  Analytics Agent        │
│  ├─ Calculate KPIs      │
│  ├─ Detect trends       │
│  └─ Find anomalies      │
│          ↓               │
│  Forecast Agent         │
│  ├─ Prophet/ARIMA/XGB   │
│  ├─ Ensemble voting     │
│  └─ Confidence intervals│
│          ↓               │
│  Recommendation Agent   │
│  ├─ Rule engine         │
│  ├─ LLM reasoning       │
│  └─ RAG (policies)      │
│          ↓               │
│  Executive Summary Agent│
│  ├─ McKinsey narrative  │
│  ├─ Key findings        │
│  └─ Next steps          │
│          ↓               │
│  Report Generation      │
│  ├─ PDF (ReportLab)     │
│  ├─ PPTX (python-pptx)  │
│  └─ JSON (raw)          │
└─────────────────────────┘
    ↓
Executive-Ready Intelligence
```

## Component Architecture

### 1. Data Warehouse (PostgreSQL + DuckDB)

**Tables:**
- `customers` (50K): Demographic, segment, loyalty, LTV
- `products` (5K): Category, pricing, supplier, status
- `sales` (1M): Transactions, profit, region, warehouse
- `inventory`: Stock levels, reorder points, supplier delays
- `marketing`: Campaign performance, ROI, spend tracking
- `finance`: Department financials, costs, profit, budget variance
- `employees`: Performance, attrition, experience, salary
- `support_tickets`: Issue tracking, resolution time, CSAT
- `targets`: Sales, profit, customer targets by dept/month
- `calendar`: Time dimension, seasonality, holidays, promotions

**Role:**
- PostgreSQL: System-of-record, conversation history, app state, checkpoints
- DuckDB: Fast analytics queries (SELECT-only, schema-aware)

### 2. LangGraph Agent Pipeline

**Workflow:** Linear execution with conditional routing (can skip agents based on intent)

**Agents:**

1. **Intent Detection**
   - Input: Natural language question
   - Output: intent type (diagnostic/predictive/prescriptive), required tables
   - Tech: LLM (OpenRouter Qwen)

2. **SQL Agent**
   - Input: Question, required tables, schema
   - Output: SQL query, executed result (rows, columns, count)
   - Guards: Read-only enforcement (SELECT only, no INSERT/UPDATE/DELETE)
   - Tech: LLM + DuckDB

3. **Analytics Agent**
   - Input: SQL result DataFrame
   - Output: KPIs, trends, anomalies, root causes
   - Calculations: Revenue, profit, margins, growth, turnover, attrition
   - Tech: pandas, numpy, statistics

4. **Forecast Agent**
   - Input: Time series data from analytics
   - Output: Forecasts with confidence intervals, MAPE/RMSE, best model
   - Models: Prophet (default) → ARIMA → XGBoost (fallback: exponential smoothing)
   - Tech: Prophet, statsmodels, XGBoost, sklearn

5. **Recommendation Agent**
   - Input: KPIs, forecasts, state
   - Output: Prioritized recommendations with impact estimates
   - Sources: Rule engine (profit margin, stock-out rules) + LLM reasoning + RAG
   - Tech: LLM + ChromaDB + rule engine

6. **Executive Summary Agent**
   - Input: All prior agent outputs
   - Output: McKinsey/BCG-style narrative, key findings, risks, next steps
   - Tone: Consulting-grade, actionable, data-backed
   - Tech: LLM

### 3. Backend (FastAPI)

**Endpoints:**

```
POST /api/chat           → Run full agent pipeline
GET  /health            → System health check
GET  /status            → Detailed status (DB, features, version)
```

**Middleware:**
- CORS (configurable origins)
- Request timing (X-Process-Time header)
- Error handling (HTTP exceptions + general error handler)
- Structured logging (structlog)

**Configuration:**
- Environment-based (.env)
- pydantic-settings with validation
- Feature flags (RAG, forecasting, anomaly, Power BI)

**Security:**
- JWT authentication (auth endpoint planned for Phase 3 completion)
- RBAC roles: admin, executive, analyst, viewer
- Password hashing (passlib + bcrypt)

### 4. Database Layer

**SQLAlchemy ORM Models:**
- `User`: Application users
- `ConversationHistory`: Chat messages, intent, metadata
- `GeneratedReport`: PDF/PPTX reports, paths, metadata
- `CheckpointState`: LangGraph state checkpointing for resumption
- `UserPreference`: Saved settings

**Connections:**
- PostgreSQL: SQLAlchemy + psycopg2
- DuckDB: Thread-local connections, read-only mode

### 5. ML Models

**Forecast:**
- Prophet (Facebook's time series)
- ARIMA (Auto-regressive integrated moving average)
- XGBoost (with lag features)
- Ensemble: Returns best by MAPE

**Anomaly Detection:**
- Isolation Forest (sklearn)
- Fallback: IQR-based detection

**Segmentation:**
- K-Means clustering (RFM features)
- Quartile-based segmentation for customer loyalty

**Evaluation:**
- MAPE: Mean absolute percentage error
- RMSE: Root mean squared error
- R²: Coefficient of determination
- Accuracy: % predictions within threshold

### 6. RAG (Retrieval-Augmented Generation)

**Storage:** ChromaDB persistent client
- Embedded in backend (no separate service)
- Sentence embeddings (local, no API cost)

**Documents:**
- Discount policy
- Pricing strategy
- Inventory management SOP
- Customer retention program
- Marketing budget allocation
- Supplier relationship policy
- Customer satisfaction targets
- Regional performance benchmarks

**Retrieval:** Semantic search on user query → top 3 documents → LLM context

### 7. Conversation Memory

**Storage:** PostgreSQL `conversation_history` table
- Session ID (UUID)
- User ID
- Question, intent, response metadata
- Multi-turn support: Session ID groups related messages

**Checkpointing:**
- LangGraph PostgreSQL checkpointer (if available)
- Fallback: In-memory checkpointing
- Enables agent resumption, state recovery

### 8. Report Generation

**PDF (ReportLab):**
- Title, metadata (question, timestamp)
- Executive summary narrative
- KPI table
- Recommendations with priority
- Forecasts and confidence intervals
- Footer: "Prepared by DecisionLens AI"

**PowerPoint (python-pptx):**
- Title slide
- Executive summary slide
- KPI stat boxes
- Recommendations slide
- Forecast slide

### 9. Frontend (React + Vite)

**Pages:**
- Chat Panel: Natural language Q&A
- Dashboard: System status, quick links, coming soon features

**Features:**
- Dark mode toggle
- Responsive design (Tailwind CSS)
- Real-time chat (axios + state)
- API integration (http://localhost:8000)

**Not yet implemented (Phase 8 stubs):**
- Power BI Embed component
- Advanced charts (Plotly)
- User auth UI
- Report download link
- Session history sidebar

## Data Flow Example

### Question: "Why did revenue decline in Q3 2024 in the South region?"

```
1. Intent Detection
   → Intent: "diagnostic"
   → Required tables: [sales, customers, products, marketing, finance]
   
2. SQL Agent
   → Generated SQL:
     SELECT 
       SUM(s.sales) as revenue,
       s.region,
       DATE_TRUNC('month', s.order_date) as month
     FROM sales s
     WHERE s.region = 'South'
       AND EXTRACT(YEAR FROM s.order_date) = 2024
       AND EXTRACT(QUARTER FROM s.order_date) = 3
     GROUP BY s.region, DATE_TRUNC('month', s.order_date)
   
   → Result: 12 rows (revenue by month/region)

3. Analytics Agent
   → KPIs:
     - Q3 Revenue: $2.5M (vs Q2: $3.1M, -19.4% decline)
     - Q3 Profit Margin: 11.2% (vs Q2: 13.8%)
     - Average Order Value: $125 (vs Q2: $145)
   → Trends:
     - Downward trend across 3 months
   → Anomalies: None
   → Root causes:
     - Discount increased to 18% (from 12%)
     - Supplier delays: 3 days longer than normal
     - Marketing spend down 25%

4. Forecast Agent
   → Q4 2024 Revenue Forecast: $2.8M
     (confidence: $2.6M - $3.0M)
   → Model: ARIMA (MAPE: 8.2%)

5. Recommendation Agent
   → Rec 1: Reduce discounts to 12% → +8% margin
   → Rec 2: Improve supplier logistics → recover $150K revenue
   → Rec 3: Increase Q4 marketing by 30% → offset Q3 decline

6. Executive Summary Agent
   → Narrative:
     "South region experienced a 19% revenue decline in Q3 2024,
      driven by aggressive discounting and supply chain friction.
      Root causes: elevated discounts (+18%), supplier delays (3d),
      marketing spend reduction (-25%). Immediate actions recommended:
      restore normal discount levels, resolve supplier delays,
      increase Q4 marketing investment. Expected recovery: +12-15%."

7. Report Generation (optional)
   → PDF with all above + charts, logo, footer
```

## Deployment

### Local Development
```bash
docker-compose up --build
# Postgres: 5433, Backend: 8000, Frontend: 3000
```

### Production
- K8s (HPA, persistent volumes)
- Managed PostgreSQL (AWS RDS)
- Dedicated DuckDB + caching layer
- API gateway (Kong, Istio)
- Monitoring (Prometheus, Grafana)

## Performance Considerations

- **SQL execution**: DuckDB read-only for speed (vs Postgres OLTP)
- **Agent parallelization**: Currently linear; can fan-out analytics agents
- **LLM caching**: Session state cached in PostgreSQL checkpointer
- **Forecast caching**: Model predictions cached per metric/period
- **RAG**: Chroma in-process (no network latency)

## Security

- **Read-only SQL**: Whitelist SELECT only, block INSERT/UPDATE/DELETE
- **JWT auth**: Token-based API access (in progress)
- **RBAC**: 4 roles with permission guards per endpoint
- **Data privacy**: Conversation history encrypted (future)
- **API rate limiting**: Per-user quotas (future)

---

**Architecture Version:** 1.0  
**Last Updated:** 2026-08-04  
**Status:** Phase 4+ complete, production-ready for MVP
