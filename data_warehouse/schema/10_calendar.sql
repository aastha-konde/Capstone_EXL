-- Time dimension for analytics and seasonality
CREATE TABLE IF NOT EXISTS calendar (
    date DATE PRIMARY KEY,
    month DATE NOT NULL,
    quarter VARCHAR(2) NOT NULL,
    year INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    holiday_name VARCHAR(100),
    is_promotion_day BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_calendar_month ON calendar(month);
CREATE INDEX IF NOT EXISTS idx_calendar_year ON calendar(year);
CREATE INDEX IF NOT EXISTS idx_calendar_is_weekend ON calendar(is_weekend);
CREATE INDEX IF NOT EXISTS idx_calendar_is_holiday ON calendar(is_holiday);
CREATE INDEX IF NOT EXISTS idx_calendar_is_promotion_day ON calendar(is_promotion_day);
