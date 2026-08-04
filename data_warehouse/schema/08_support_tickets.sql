-- Customer support tickets
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    issue_type VARCHAR(100) NOT NULL,  -- 'Delivery', 'Product Quality', 'Billing', 'Returns', 'Other'
    priority VARCHAR(20) NOT NULL,  -- 'Low', 'Medium', 'High', 'Critical'
    resolution_time INTEGER DEFAULT 0,  -- hours
    satisfaction NUMERIC(5, 2) DEFAULT 0,  -- 1-10
    created_date DATE NOT NULL,
    closed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_support_tickets_customer_id ON support_tickets(customer_id);
CREATE INDEX idx_support_tickets_issue_type ON support_tickets(issue_type);
CREATE INDEX idx_support_tickets_priority ON support_tickets(priority);
CREATE INDEX idx_support_tickets_created_date ON support_tickets(created_date);
CREATE INDEX idx_support_tickets_satisfaction ON support_tickets(satisfaction);
