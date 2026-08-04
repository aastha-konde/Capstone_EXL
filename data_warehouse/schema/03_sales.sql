-- Sales table: ~1M transactions over 5 years
CREATE TABLE IF NOT EXISTS sales (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    discount NUMERIC(5, 2) DEFAULT 0,
    sales NUMERIC(12, 2) NOT NULL,
    profit NUMERIC(12, 2) NOT NULL,
    region VARCHAR(50) NOT NULL,
    warehouse VARCHAR(50) NOT NULL,
    salesperson VARCHAR(100),
    order_date DATE NOT NULL,
    delivery_date DATE,
    returned BOOLEAN DEFAULT FALSE,
    payment_type VARCHAR(20) NOT NULL,  -- 'Credit Card', 'Debit Card', 'Bank Transfer', 'Cash'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sales_customer_id ON sales(customer_id);
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_order_date ON sales(order_date);
CREATE INDEX idx_sales_region ON sales(region);
CREATE INDEX idx_sales_warehouse ON sales(warehouse);
CREATE INDEX idx_sales_returned ON sales(returned);
CREATE INDEX idx_sales_order_date_region ON sales(order_date, region);
