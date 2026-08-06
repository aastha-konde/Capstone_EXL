-- Initialize RetailMart Global Data Warehouse
-- This script is run automatically by Docker if the DB is empty

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Run all individual table creation scripts
\i /docker-entrypoint-initdb.d/01_customers.sql
\i /docker-entrypoint-initdb.d/02_products.sql
\i /docker-entrypoint-initdb.d/03_sales.sql
\i /docker-entrypoint-initdb.d/04_inventory.sql
\i /docker-entrypoint-initdb.d/05_marketing.sql
\i /docker-entrypoint-initdb.d/06_finance.sql
\i /docker-entrypoint-initdb.d/07_employees.sql
\i /docker-entrypoint-initdb.d/08_support_tickets.sql
\i /docker-entrypoint-initdb.d/09_targets.sql
\i /docker-entrypoint-initdb.d/10_calendar.sql

-- Grant permissions (adjust as needed for your app user)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO retailmart;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO retailmart;

-- Create memory/checkpoint tables for LangGraph + app usage
CREATE TABLE IF NOT EXISTS conversation_history (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL DEFAULT gen_random_uuid(),
    user_id INTEGER,
    question TEXT NOT NULL,
    response TEXT,
    intent VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS checkpoint_states (
    thread_id TEXT NOT NULL PRIMARY KEY,
    checkpoint_id TEXT NOT NULL,
    parent_config JSONB,
    config JSONB,
    values JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS generated_reports (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    user_id INTEGER,
    report_type VARCHAR(20),  -- 'PDF', 'PPTX', 'JSON'
    file_path VARCHAR(500),
    question TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_conversation_history_session_id ON conversation_history(session_id);
CREATE INDEX IF NOT EXISTS idx_conversation_history_user_id ON conversation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_history_timestamp ON conversation_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_checkpoint_states_thread_id ON checkpoint_states(thread_id);
CREATE INDEX IF NOT EXISTS idx_generated_reports_session_id ON generated_reports(session_id);
CREATE INDEX IF NOT EXISTS idx_generated_reports_user_id ON generated_reports(user_id);

GRANT ALL PRIVILEGES ON conversation_history TO retailmart;
GRANT ALL PRIVILEGES ON checkpoint_states TO retailmart;
GRANT ALL PRIVILEGES ON generated_reports TO retailmart;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES ON conversation_history TO retailmart;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES ON generated_reports TO retailmart;

-- Note: Synthetic data loading is done separately by the Python loader script
-- This schema file initializes the tables only.
