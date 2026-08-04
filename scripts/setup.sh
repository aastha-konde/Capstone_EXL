#!/bin/bash
set -e

echo "=========================================="
echo "DecisionLens AI - Environment Setup"
echo "=========================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Please install Miniconda/Anaconda first."
    exit 1
fi

# Activate the ai_agent_env if it exists, otherwise create it
ENV_NAME="ai_agent_env"
if conda env list | grep -q "^$ENV_NAME "; then
    echo "✓ Activating existing conda environment: $ENV_NAME"
    source "$(conda run -n base python -c 'import site; print(site.getsitepackages()[0])')/../activate" "$ENV_NAME"
else
    echo "Creating conda environment: $ENV_NAME"
    conda create -n "$ENV_NAME" python=3.11 -y
    source "$(conda run -n base python -c 'import site; print(site.getsitepackages()[0])')/../activate" "$ENV_NAME"
fi

# Source the environment (bash-specific)
eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"

echo "✓ Using Python: $(python --version)"

# Install/upgrade core dependencies
echo ""
echo "Installing required Python packages..."

pip install --upgrade pip setuptools wheel

# Core packages (should already be there)
pip install -q \
    fastapi uvicorn \
    sqlalchemy sqlmodel \
    pydantic pydantic-settings \
    pandas numpy \
    langchain langchain-core langgraph langchain-openai \
    chromadb

# Missing packages as per plan
pip install -q \
    duckdb \
    scikit-learn xgboost \
    statsmodels \
    prophet \
    plotly kaleido \
    reportlab python-pptx \
    faker \
    asyncpg psycopg2-binary \
    passlib \
    PyJWT \
    bcrypt \
    python-dotenv \
    tenacity \
    alembic

# Optional but useful
pip install -q \
    pytest pytest-asyncio pytest-cov \
    black flake8 \
    httpx \
    qdrant-client

echo ""
echo "✓ All Python packages installed successfully"

# Create directory structure if it doesn't exist
echo ""
echo "Creating directory structure..."
mkdir -p data_warehouse/{schema,generator,loader}
mkdir -p backend/app/{api,agents,analytics,ml,rag,memory,db,schemas,core,evaluation}
mkdir -p backend/tests/{unit,integration}
mkdir -p frontend/src/{pages,components,hooks,services,styles}
mkdir -p rag_documents
mkdir -p docs
mkdir -p scripts

echo "✓ Directories created"

# Create environment files
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠ Update .env with your actual OPENROUTER_API_KEY"
else
    echo "✓ .env already exists"
fi

if [ ! -f .env.local ]; then
    cp .env.example .env.local
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update .env with your OPENROUTER_API_KEY"
echo "2. Run: source scripts/setup.sh (to activate the conda env in your shell)"
echo "3. Run: conda activate ai_agent_env (to use the environment)"
echo "4. Run: python data_warehouse/generator/generate.py (to create synthetic data)"
echo "5. Run: docker compose up --build (to start all services)"
echo ""
