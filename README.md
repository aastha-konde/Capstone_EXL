# DecisionLens AI

**An enterprise-grade AI platform that transforms data into strategic business decisions.**

## 🎯 Vision

Transform the question from *"What happened?"* to:
- **Why did it happen?**
- **Which departments/regions contributed?**
- **What will happen next?**
- **What actions should management take?**
- **What will those actions cost and save?**

DecisionLens AI is a multi-agent system that understands business questions in natural language, analyzes enterprise data, identifies root causes, forecasts outcomes, and recommends data-driven actions with confidence estimates.

## 📊 System Architecture

```
User Question (NL)
    ↓
Intent Detection Agent (Classify & route)
    ↓
SQL Agent (Retrieve data)
    ↓
Analytics Agent (Calculate KPIs, trends, anomalies)
    ↓
Forecast Agent (Predict future outcomes)
    ↓
Recommendation Agent (Suggest actions)
    ↓
Executive Summary Agent (Narrative + insights)
    ↓
Report Generator (PDF/PowerPoint)
    ↓
Executive-Ready Intelligence
```

## 🏢 RetailMart Global Dataset

A fictional enterprise data warehouse with:
- **~1 million** sales transactions
- **~50,000** unique customers
- **5 years** of historical data
- **10 integrated tables**: Customers, Products, Sales, Inventory, Marketing, Finance, Employees, Support Tickets, Targets, Calendar
- **Realistic behavior**: seasonality, Black Friday/Christmas spikes, disruptions (COVID-like), supplier delays, churn, price wars, regional variance

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Qwen (via OpenRouter) or Llama 3 |
| **Agent Framework** | LangGraph + LangChain |
| **Backend** | FastAPI + SQLAlchemy + Pydantic |
| **Databases** | PostgreSQL (system-of-record), DuckDB (analytics) |
| **ML/Analytics** | scikit-learn, XGBoost, Prophet, statsmodels |
| **RAG** | ChromaDB (policy documents, SOPs) |
| **Reports** | ReportLab (PDF), python-pptx (PowerPoint) |
| **Dashboard** | React + Vite + Plotly |
| **Memory** | PostgreSQL + LangGraph checkpointer |
| **Deployment** | Docker Compose (local), Kubernetes-ready (prod) |
| **Auth** | JWT + RBAC (admin, executive, analyst, viewer) |

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+ (or use `ai_agent_env` conda environment)
- Docker + Docker Compose
- PostgreSQL 16 (optional, for local dev without Docker)
- OpenRouter API Key (for Qwen/Llama 3 access)

### 2. Setup Environment

```bash
# Clone and enter directory
cd /path/to/Capstone_EXL

# Run setup script (installs Python deps, creates dirs)
source scripts/setup.sh
conda activate ai_agent_env

# Copy .env.example to .env and update with your OpenRouter key
cp .env.example .env
# Edit .env and set OPENROUTER_API_KEY
```

### 3. Generate Synthetic Data

```bash
python data_warehouse/generator/generate.py
python data_warehouse/loader/load.py
```

This creates:
- PostgreSQL tables with 1M+ rows
- DuckDB file (`retailmart.duckdb`) for fast analytics queries

### 4. Run Services

#### Option A: Local Development
```bash
# Terminal 1: Backend (FastAPI)
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Frontend (React Vite)
cd frontend && npm install && npm run dev

# Terminal 3: (Optional) Initialize RAG
python backend/scripts/init_rag.py
```

#### Option B: Docker Compose (Full Stack)
```bash
docker compose up --build
```
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

### 5. Test the Pipeline

Open `http://localhost:8000/docs` (Swagger UI) and try the `/chat` endpoint with a sample question:

```json
{
  "question": "Why did revenue decline in Q3 2024 in the South region?"
}
```

Expected response includes: SQL, KPIs, trends, forecasts, recommendations, and an executive summary.

## 📖 Example Questions

DecisionLens AI can answer:

- "Why did revenue decline last quarter?"
- "Which region is underperforming and why?"
- "Which products should we discontinue?"
- "Why are customer complaints increasing?"
- "What is the forecast for next quarter revenue?"
- "Which marketing campaigns had poor ROI?"
- "What actions should we take to improve profitability?"
- "Which warehouse is causing delivery delays?"

## 🧠 Agents Explained

### Intent Detection Agent
Classifies the question type (diagnostic, predictive, prescriptive) and identifies required data sources to optimize downstream agent routing.

### SQL Agent
Converts natural language to SQL, validates (read-only guard), executes against DuckDB, and returns structured results.

### Analytics Agent
Calculates:
- **KPIs**: Revenue, Profit, Margin, AOV, CLV, Inventory Turnover, Campaign ROI, Attrition
- **Analysis**: Variance, contribution, Pareto (80/20), ABC segmentation, RFM analysis, trends, anomalies

### Forecast Agent
Runs Prophet, ARIMA (statsmodels), and XGBoost in parallel, backtests, selects best by MAPE/RMSE, returns confidence intervals and feature importance.

### Recommendation Agent
Merges:
- Deterministic business rules (e.g., "if discount > 30% AND margin < 5%, recommend reducing discounts")
- LLM reasoning over state (analytics + forecasts)
- RAG-retrieved company policies
- Expected impact estimates (revenue, cost savings)

### Executive Summary Agent
Writes a McKinsey/Deloitte-style narrative:
- Key findings
- Root causes
- Future risks
- Recommended actions
- Expected impact
- Next steps

### Report Generator
Produces PDF (ReportLab) and PowerPoint (python-pptx) with:
- Executive summary
- Charts (Plotly rendered as PNG)
- KPI tables
- Forecasts + confidence intervals
- Recommendations ranked by impact
- Company logo, date, prepared-by footer

## 📊 Dashboard Features

The React dashboard includes:

- **Executive Overview**: key metrics, alerts, trends
- **Sales Analytics**: by product, region, channel, salesperson
- **Finance**: revenue/profit, department breakdown, budget variance
- **Marketing**: campaign ROI, spend efficiency, conversion trends
- **Inventory**: stock levels, reorder alerts, turnover, supplier delays
- **Operations**: warehouse performance, delivery times
- **Customer Analytics**: segments, lifetime value, churn risk, NPS
- **Forecasts**: revenue, demand, churn prediction
- **Recommendations**: actionable insights ranked by impact
- **Anomaly Alerts**: outliers and unusual trends
- **Natural Language Chat**: ask questions directly

## 🔐 Authentication & Authorization

**JWT + RBAC** with roles:
- **Admin**: Full access, user management
- **Executive**: View all reports, recommendations, dashboards
- **Analyst**: View data, SQL access, generate reports
- **Viewer**: Read-only access to dashboards

## 📁 Project Structure

```
Capstone_EXL/
├── README.md                          (This file)
├── .env.example                       (Environment template)
├── docker-compose.yml                 (Full stack orchestration)
├── data_warehouse/
│   ├── schema/                        (DDL for 10 tables)
│   ├── generator/                     (Synthetic data ~1M rows)
│   └── loader/                        (Postgres + DuckDB loading)
├── backend/
│   ├── app/
│   │   ├── main.py                    (FastAPI app)
│   │   ├── core/                      (config, auth, logging, retry)
│   │   ├── api/                       (routers: auth, chat, kpis, reports)
│   │   ├── agents/                    (LangGraph pipeline + 6 agents)
│   │   ├── analytics/                 (KPI + trend analysis)
│   │   ├── ml/                        (forecast, anomaly, segmentation, churn)
│   │   ├── rag/                       (Chroma retrieval)
│   │   ├── memory/                    (Postgres conversation history)
│   │   ├── reports/                   (PDF + PPTX builders)
│   │   ├── db/                        (SQLAlchemy models, DuckDB, sessions)
│   │   ├── schemas/                   (Pydantic request/response)
│   │   └── evaluation/                (metrics, accuracy, latency)
│   ├── tests/                         (unit + integration tests)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/                     (Dashboard, Chat, Reports)
│   │   ├── components/                (Charts, Alerts, PowerBI stub)
│   │   ├── services/                  (API client, auth)
│   │   └── styles/                    (Tailwind, dark mode)
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── rag_documents/                     (Fictional policies, SOPs, annual report)
├── docs/
│   ├── architecture.md                (System architecture)
│   ├── er_diagram.md                  (Mermaid: Database schema)
│   ├── sequence_diagrams.md           (Mermaid: Agent flows)
│   ├── api.md                         (API reference)
│   ├── deployment.md                  (Docker, K8s, cloud deployment)
│   ├── sample_prompts.md              (Example questions)
│   └── evaluation.md                  (Metrics, testing approach)
└── scripts/
    ├── setup.sh                       (Install deps, create dirs)
    ├── seed_db.sh                     (Load data, init Chroma)
    └── run_dev.sh                     (Local dev server startup)
```

## 🧪 Testing & Evaluation

Run tests:
```bash
pytest backend/tests -v
```

Evaluation metrics tracked:
- **SQL Accuracy**: % of questions generating correct schema queries
- **Hallucination Rate**: % of agent responses with unsupported claims
- **Forecast MAPE/RMSE**: Against held-out test periods
- **Recommendation Usefulness**: User feedback on actionability
- **Response Latency**: Agent end-to-end timing

## 🔄 Multi-Turn Conversations

The system remembers prior context via a Postgres-backed LangGraph checkpointer. Follow-up questions like:
- "Break that down by region"
- "What if we increased the discount by 5%?"
- "Show me the impact on profitability"

...automatically reuse context from the prior turn without re-running the entire pipeline.

## 📝 RAG (Retrieval-Augmented Generation)

The Recommendation Agent grounds advice in company policies:
- Discount policy limits
- Hiring & retention SOPs
- Marketing strategy guidelines
- Financial policies
- Product lifecycle rules
- Annual business plan

RAG documents are stored in ChromaDB with sentence embeddings (local, no API cost).

## 🚢 Deployment

### Docker Compose (Development)
```bash
docker compose up --build
```

### Production Checklist
- [ ] Update `JWT_SECRET_KEY` in `.env` (generate a strong key)
- [ ] Set `ENVIRONMENT=production` and `DEBUG=false`
- [ ] Configure actual PostgreSQL credentials
- [ ] Enable HTTPS + TLS
- [ ] Set `POSTGRES_PASSWORD` to a strong password
- [ ] Update `CORS_ORIGINS` to your frontend domain
- [ ] Configure logging to a centralized service
- [ ] Set up monitoring/alerting (Prometheus, Datadog, etc.)
- [ ] Use a managed service for PostgreSQL (AWS RDS, Google Cloud SQL, etc.)

### Cloud Deployment
See [docs/deployment.md](docs/deployment.md) for:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Kubernetes (minikube → production)

## 📚 Documentation

- [Architecture Overview](docs/architecture.md) — system design, agent workflows, data flow
- [Database Schema (ER Diagram)](docs/er_diagram.md) — Mermaid entity-relationship diagram
- [Sequence Diagrams](docs/sequence_diagrams.md) — agent interaction flows
- [API Reference](docs/api.md) — endpoints, request/response shapes, examples
- [Deployment Guide](docs/deployment.md) — Docker, Kubernetes, cloud platforms
- [Sample Prompts](docs/sample_prompts.md) — example questions + expected responses
- [Evaluation Metrics](docs/evaluation.md) — how to measure performance

## 🔧 Configuration

All configuration is env-var driven (see `.env.example`):

```bash
# LLM Provider
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=qwen/qwen-2.5-72b-instruct  # or qwen/qwen-2.5-coder, llama-3-70b, etc.

# Database
POSTGRES_HOST=localhost
POSTGRES_USER=retailmart
POSTGRES_PASSWORD=...

# Security
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256

# Dashboard
ENABLE_POWER_BI_EMBED=false  # Set to true + provide credentials to enable

# Feature Flags
ENABLE_FORECASTING=true
ENABLE_ANOMALY_DETECTION=true
ENABLE_RAG=true
```

## 🎯 Development Roadmap

**Phase 1 (✓ Complete)**: Repo scaffold, Docker Compose, DB schema  
**Phase 2 (✓ Complete)**: Synthetic data generator + loader  
**Phase 3 (In Progress)**: FastAPI backend + JWT auth  
**Phase 4**: LangGraph agents (Intent → SQL → Analytics → Forecast → Recommendation → Summary)  
**Phase 5**: ML models (Prophet, XGBoost, sklearn)  
**Phase 6**: RAG + memory layer  
**Phase 7**: Report generators (PDF, PPTX)  
**Phase 8**: React dashboard + Plotly  
**Phase 9**: Tests, evaluation, docs, diagrams  

## 🤝 Contributing

This is an educational capstone project. To extend:

1. Add new agents to `backend/app/agents/`
2. Add new analytics functions to `backend/app/analytics/`
3. Add new ML models to `backend/app/ml/`
4. Add new dashboard pages to `frontend/src/pages/`
5. Update docs in `docs/`

## 📜 License

Educational / Capstone Project

## 🙋 Support

For questions or issues:
1. Check [docs/](docs/) for detailed explanations
2. Review [sample_prompts.md](docs/sample_prompts.md) for usage examples
3. Check backend logs: `docker logs retailmart-backend`
4. Check frontend logs: browser console (F12)

---

**Built with ❤️ as an enterprise AI capstone project.**
