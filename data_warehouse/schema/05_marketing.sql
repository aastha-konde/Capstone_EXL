-- Marketing campaigns and ROI tracking
CREATE TABLE IF NOT EXISTS marketing (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(200) NOT NULL,
    channel VARCHAR(50) NOT NULL,  -- 'Email', 'Social Media', 'TV', 'Radio', 'Print', 'Online'
    region VARCHAR(50) NOT NULL,
    budget NUMERIC(12, 2) NOT NULL,
    spend NUMERIC(12, 2) NOT NULL,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    roi NUMERIC(10, 2) DEFAULT 0,  -- (revenue - spend) / spend * 100
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_marketing_campaign_name ON marketing(campaign_name);
CREATE INDEX IF NOT EXISTS idx_marketing_channel ON marketing(channel);
CREATE INDEX IF NOT EXISTS idx_marketing_region ON marketing(region);
CREATE INDEX IF NOT EXISTS idx_marketing_start_date ON marketing(start_date);
CREATE INDEX IF NOT EXISTS idx_marketing_roi ON marketing(roi);
