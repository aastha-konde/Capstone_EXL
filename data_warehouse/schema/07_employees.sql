-- Employee data for attrition and performance tracking
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    manager VARCHAR(100),
    region VARCHAR(50) NOT NULL,
    experience INTEGER NOT NULL,  -- years
    performance_score NUMERIC(5, 2) DEFAULT 5.0,  -- 1-10
    attrition BOOLEAN DEFAULT FALSE,
    salary NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_region ON employees(region);
CREATE INDEX idx_employees_attrition ON employees(attrition);
CREATE INDEX idx_employees_performance_score ON employees(performance_score);
