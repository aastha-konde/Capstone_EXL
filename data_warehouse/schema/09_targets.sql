-- Monthly departmental targets for performance tracking
CREATE TABLE IF NOT EXISTS targets (
    target_id SERIAL PRIMARY KEY,
    month DATE NOT NULL,
    department VARCHAR(100) NOT NULL,
    sales_target NUMERIC(12, 2) NOT NULL,
    profit_target NUMERIC(12, 2) NOT NULL,
    customer_target INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(month, department)
);

CREATE INDEX idx_targets_month ON targets(month);
CREATE INDEX idx_targets_department ON targets(department);
CREATE INDEX idx_targets_month_department ON targets(month, department);
