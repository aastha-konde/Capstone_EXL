-- Customers table: 50K unique customers with demographic and value data
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    age INTEGER NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'USA',
    segment VARCHAR(50) NOT NULL,  -- 'Premium', 'Standard', 'Budget'
    joining_date DATE NOT NULL,
    lifetime_value NUMERIC(12, 2) DEFAULT 0,
    income_group VARCHAR(20) NOT NULL,  -- 'Low', 'Middle', 'High'
    loyalty_level VARCHAR(20) NOT NULL DEFAULT 'Bronze',  -- 'Bronze', 'Silver', 'Gold', 'Platinum'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_segment ON customers(segment);
CREATE INDEX idx_customers_loyalty_level ON customers(loyalty_level);
CREATE INDEX idx_customers_state ON customers(state);
CREATE INDEX idx_customers_income_group ON customers(income_group);
CREATE INDEX idx_customers_joining_date ON customers(joining_date);
