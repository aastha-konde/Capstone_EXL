-- Financial data by month and department
CREATE TABLE IF NOT EXISTS finance (
    finance_id SERIAL PRIMARY KEY,
    month DATE NOT NULL,
    department VARCHAR(100) NOT NULL,
    operating_cost NUMERIC(12, 2) DEFAULT 0,
    salary_cost NUMERIC(12, 2) DEFAULT 0,
    marketing_cost NUMERIC(12, 2) DEFAULT 0,
    profit NUMERIC(12, 2) DEFAULT 0,
    revenue NUMERIC(12, 2) DEFAULT 0,
    budget NUMERIC(12, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(month, department)
);

CREATE INDEX IF NOT EXISTS idx_finance_month ON finance(month);
CREATE INDEX IF NOT EXISTS idx_finance_department ON finance(department);
CREATE INDEX IF NOT EXISTS idx_finance_month_department ON finance(month, department);
