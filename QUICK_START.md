# DecisionLens AI - Quick Start Guide

## 🚀 Start the Application (30 seconds)

```bash
cd /home/labuser/Desktop/Capstone_EXL
docker compose up -d --build
```

## 🌐 Access the Application

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://localhost:3000 | Dashboard & Chat |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Health** | http://localhost:8000/health | System status |
| **Status** | http://localhost:8000/status | Feature flags |

## ✅ Verify Everything is Running

```bash
docker compose ps
```

Should show:
- ✅ retailmart-frontend (running)
- ✅ retailmart-backend (running)  
- ✅ retailmart-postgres (healthy)

## 📊 Check System Status

```bash
curl http://localhost:8000/status | jq .
```

Should show:
```json
{
  "database": "connected",
  "duckdb": "connected",
  "features": {
    "rag": true,
    "forecasting": true,
    "anomaly_detection": true
  }
}
```

## 💬 Test Chat Interface

Open http://localhost:3000 and try asking:
- "What are the top 5 products by sales?"
- "What's our discount policy?"
- "Show me customer trends"

## 📚 RAG System Status

✅ **7 documents indexed and ready**
- Discount policies
- Pricing strategies
- Inventory management
- Customer service standards
- Financial targets
- Product launch guidelines

## 🛑 Stop the Application

```bash
docker compose down
```

## 🔄 Restart with Fresh Data

```bash
docker compose down
rm -rf backend/chroma_data/*
docker compose up -d --build
```

## 📝 View Logs

```bash
# All services
docker compose logs -f

# Just backend
docker compose logs -f backend

# Just frontend
docker compose logs -f frontend
```

## 🐛 Troubleshooting

**Can't access frontend?**
```bash
docker compose logs frontend | tail -20
```

**Can't access API?**
```bash
docker compose logs backend | tail -20
```

**Database connection failed?**
```bash
docker exec retailmart-postgres psql -U retailmart -d retailmart_dw -c "SELECT 1"
```

## 🔧 Common Tasks

### Add a Custom RAG Document
1. Create `rag_documents/my_policy.md`
2. Restart backend: `docker compose restart backend`
3. Documents auto-load on startup

### Load Full Database
```bash
python data_warehouse/loader/load.py
```

### View Backend Config
```bash
cat .env
```

### Run API Test
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

## 📞 Support

- Backend Issues → `docker compose logs backend`
- Frontend Issues → `docker compose logs frontend`
- Database Issues → `docker compose logs postgres`

---

**Everything is ready!** 🎉 Start with `/IMPLEMENTATION_COMPLETE.md` for full details.
