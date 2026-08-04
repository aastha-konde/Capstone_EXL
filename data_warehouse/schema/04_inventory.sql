-- Inventory table: current stock levels per warehouse/product
CREATE TABLE IF NOT EXISTS inventory (
    warehouse_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    stock_level INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL,
    lead_time INTEGER NOT NULL,  -- days to restock
    supplier_delay INTEGER DEFAULT 0,  -- days late on last delivery
    stock_out BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(warehouse_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_stock_out ON inventory(stock_out);
CREATE INDEX IF NOT EXISTS idx_inventory_stock_level ON inventory(stock_level);
