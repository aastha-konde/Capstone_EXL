-- Products table: ~5K products across categories
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) NOT NULL,
    supplier VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    cost NUMERIC(10, 2) NOT NULL,
    selling_price NUMERIC(10, 2) NOT NULL,
    launch_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',  -- 'Active', 'Discontinued', 'Seasonal'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_subcategory ON products(subcategory);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_supplier ON products(supplier);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_launch_date ON products(launch_date);
