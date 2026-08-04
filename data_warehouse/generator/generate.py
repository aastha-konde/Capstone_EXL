#!/usr/bin/env python3
"""
RetailMart Global Synthetic Data Generator
Produces ~1M sales records, 50K customers, 5 years of history with realistic patterns:
- Seasonality (Q4 spike)
- Black Friday / Christmas
- COVID-like 2020 disruption
- Supplier delays
- Inventory shortages
- Price wars
- Customer churn
- Regional variance
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Ensure reproducibility for demo purposes
np.random.seed(42)

# Configuration
NUM_CUSTOMERS = 50_000
NUM_PRODUCTS = 5_000
NUM_SALES = 1_000_000  # Target sales records
NUM_WAREHOUSES = 12
NUM_EMPLOYEES = 2_000
NUM_SUPPORT_TICKETS = 150_000
NUM_MARKETING_CAMPAIGNS = 500

# Date range: 5 years
DATE_START = pd.Timestamp('2020-01-01')
DATE_END = pd.Timestamp('2024-12-31')
DATE_RANGE = pd.date_range(DATE_START, DATE_END, freq='D')

# Business constants
REGIONS = ['North', 'South', 'East', 'West', 'Midwest', 'Northeast', 'Southeast', 'Southwest']
WAREHOUSES = [f'WH-{i:02d}' for i in range(1, NUM_WAREHOUSES + 1)]
DEPARTMENTS = ['Sales', 'Marketing', 'Operations', 'Finance', 'HR', 'IT', 'Logistics', 'Customer Service']
CATEGORIES = ['Electronics', 'Home & Garden', 'Sports', 'Clothing', 'Books', 'Furniture', 'Food', 'Health']
SEGMENTS = ['Premium', 'Standard', 'Budget']
LOYALTY_LEVELS = ['Bronze', 'Silver', 'Gold', 'Platinum']
CHANNELS = ['Email', 'Social Media', 'TV', 'Radio', 'Print', 'Online', 'Direct Mail']
PAYMENT_TYPES = ['Credit Card', 'Debit Card', 'Bank Transfer', 'Cash', 'Mobile Payment']
ISSUE_TYPES = ['Delivery', 'Product Quality', 'Billing', 'Returns', 'Other']
PRIORITIES = ['Low', 'Medium', 'High', 'Critical']

def generate_calendar():
    """Generate calendar dimension"""
    print("Generating calendar...")
    dates = []
    for date in DATE_RANGE:
        quarter = f'Q{(date.month - 1) // 3 + 1}'
        is_weekend = date.dayofweek >= 5
        is_holiday = date.month == 12 and date.day == 25  # Christmas
        is_promotion = (date.month in [11, 12]) or (date.month == 1)  # Black Friday, Christmas, New Year sales

        dates.append({
            'date': date,
            'month': date.replace(day=1),
            'quarter': quarter,
            'year': date.year,
            'day_of_week': date.day_name(),
            'is_weekend': is_weekend,
            'is_holiday': is_holiday,
            'holiday_name': 'Christmas' if is_holiday else None,
            'is_promotion_day': is_promotion,
        })
    return pd.DataFrame(dates)

def generate_customers():
    """Generate 50K customers"""
    print("Generating customers...")
    customers = []

    for i in range(NUM_CUSTOMERS):
        joining_date = DATE_START + timedelta(days=np.random.randint(0, (DATE_END - DATE_START).days))
        lifetime_value = np.random.exponential(scale=1000) * np.random.choice([0.5, 1.0, 2.0, 5.0])  # Power law

        customers.append({
            'customer_id': i + 1,
            'gender': np.random.choice(['Male', 'Female', 'Other']),
            'age': np.random.normal(45, 15),
            'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Atlanta', 'Denver', 'Miami']),
            'state': np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:20]),  # Simplified state codes
            'country': 'USA',
            'segment': np.random.choice(SEGMENTS, p=[0.15, 0.60, 0.25]),  # More Standard/Budget
            'joining_date': joining_date,
            'lifetime_value': lifetime_value,
            'income_group': np.random.choice(['Low', 'Middle', 'High'], p=[0.30, 0.50, 0.20]),
            'loyalty_level': np.random.choice(LOYALTY_LEVELS, p=[0.5, 0.25, 0.15, 0.1]),
        })

    df = pd.DataFrame(customers)
    df['age'] = df['age'].clip(18, 80).astype(int)
    return df

def generate_products():
    """Generate 5K products"""
    print("Generating products...")
    products = []

    for i in range(NUM_PRODUCTS):
        category = np.random.choice(CATEGORIES)
        cost = np.random.uniform(10, 500)
        markup = np.random.uniform(1.2, 3.0)

        products.append({
            'product_id': i + 1,
            'category': category,
            'subcategory': f'{category} Sub{i % 10 + 1}',
            'supplier': f'Supplier-{np.random.randint(1, 100)}',
            'brand': f'Brand-{i % 50 + 1}',
            'cost': cost,
            'selling_price': cost * markup,
            'launch_date': DATE_START + timedelta(days=np.random.randint(0, (DATE_END - DATE_START).days)),
            'status': np.random.choice(['Active', 'Discontinued', 'Seasonal'], p=[0.85, 0.10, 0.05]),
        })

    return pd.DataFrame(products)

def generate_sales(customers_df, products_df, calendar_df):
    """Generate ~1M sales transactions with realistic patterns"""
    print("Generating sales transactions (this may take 1-2 minutes)...")

    sales = []
    disruption_window = (pd.Timestamp('2020-03-01'), pd.Timestamp('2020-06-01'))  # COVID-like window

    for i in range(NUM_SALES):
        if i % 100_000 == 0:
            print(f"  {i:,} / {NUM_SALES:,} sales generated...")

        order_date = DATE_START + timedelta(days=np.random.randint(0, (DATE_END - DATE_START).days))

        # Seasonality: Q4 gets 2x boost, promotions get 1.3x boost
        seasonality_factor = 1.0
        if order_date.month in [11, 12]:  # Q4 spike
            seasonality_factor = 2.0
        if order_date.month in [1, 11]:  # New Year, Black Friday prep
            seasonality_factor = 1.3

        # COVID disruption: less sales, more returns
        covid_factor = 0.5 if disruption_window[0] <= order_date <= disruption_window[1] else 1.0

        # Random demand boost/bust
        demand_noise = np.random.lognormal(0, 0.3)

        quantity = max(1, int(np.random.poisson(3) * seasonality_factor * covid_factor * demand_noise))

        customer = customers_df.iloc[np.random.randint(0, len(customers_df))]
        product = products_df.iloc[np.random.randint(0, len(products_df))]

        # Discount correlated with seasonality and customer segment
        if customer['segment'] == 'Premium':
            discount = np.random.uniform(0, 5)
        elif customer['segment'] == 'Standard':
            discount = np.random.uniform(0, 15) if order_date.month in [11, 12] else np.random.uniform(0, 10)
        else:  # Budget
            discount = np.random.uniform(5, 25)

        base_price = product['selling_price'] * quantity
        discounted_sales = base_price * (1 - discount / 100)
        profit = (discounted_sales - product['cost'] * quantity) * covid_factor

        # Returns are more common during disruptions and for high-discount sales
        return_chance = 0.05
        if discount > 20:
            return_chance = 0.15
        if disruption_window[0] <= order_date <= disruption_window[1]:
            return_chance = 0.20

        returned = np.random.random() < return_chance
        if returned:
            profit *= -0.5  # Return loss

        sales.append({
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'discount': discount,
            'sales': discounted_sales,
            'profit': profit,
            'region': np.random.choice(REGIONS),
            'warehouse': np.random.choice(WAREHOUSES),
            'salesperson': f'Sales-Rep-{np.random.randint(1, 500)}',
            'order_date': order_date,
            'delivery_date': order_date + timedelta(days=np.random.randint(1, 15)),
            'returned': returned,
            'payment_type': np.random.choice(PAYMENT_TYPES),
        })

    return pd.DataFrame(sales)

def generate_inventory(products_df):
    """Generate inventory levels per warehouse/product"""
    print("Generating inventory...")

    inventory = []
    for product_id in products_df['product_id'].unique():
        for wh_id, warehouse in enumerate(WAREHOUSES, 1):
            stock_level = np.random.randint(10, 500)
            reorder_level = np.random.randint(50, 200)

            # Some warehouses have stockouts or supplier delays
            stock_out = np.random.random() < 0.05
            supplier_delay = np.random.randint(0, 15) if np.random.random() < 0.1 else 0

            inventory.append({
                'warehouse_id': (product_id - 1) * NUM_WAREHOUSES + wh_id,
                'product_id': product_id,
                'stock_level': stock_level if not stock_out else 0,
                'reorder_level': reorder_level,
                'lead_time': np.random.randint(7, 60),
                'supplier_delay': supplier_delay,
                'stock_out': stock_out,
            })

    return pd.DataFrame(inventory)

def generate_marketing(calendar_df, sales_df):
    """Generate marketing campaigns"""
    print("Generating marketing campaigns...")

    campaigns = []
    for i in range(NUM_MARKETING_CAMPAIGNS):
        start_date = DATE_START + timedelta(days=np.random.randint(0, (DATE_END - DATE_START).days - 60))
        end_date = start_date + timedelta(days=np.random.randint(7, 90))

        budget = np.random.uniform(5_000, 100_000)
        spend = budget * np.random.uniform(0.7, 1.1)

        channel = np.random.choice(CHANNELS)
        region = np.random.choice(REGIONS)

        # Campaign effectiveness tied to region/channel combination
        clicks = int(spend / 10 * np.random.uniform(0.5, 2.0))
        conversion_rate = np.random.uniform(0.01, 0.15)
        conversions = int(clicks * conversion_rate)

        # Rough revenue from campaign (simplified attribution)
        campaign_revenue = conversions * np.random.uniform(50, 500)
        roi = ((campaign_revenue - spend) / spend * 100) if spend > 0 else 0

        campaigns.append({
            'campaign_id': i + 1,
            'campaign_name': f'{channel}-{region}-Campaign-{i}',
            'channel': channel,
            'region': region,
            'budget': budget,
            'spend': spend,
            'clicks': clicks,
            'conversions': conversions,
            'roi': roi,
            'start_date': start_date,
            'end_date': end_date,
        })

    return pd.DataFrame(campaigns)

def generate_finance(calendar_df):
    """Generate monthly finance data by department"""
    print("Generating finance data...")

    finance = []
    for month in pd.date_range(DATE_START.replace(day=1), DATE_END.replace(day=1), freq='MS'):
        for department in DEPARTMENTS:
            # Finance numbers tied to seasonality
            seasonality = 2.0 if month.month in [11, 12] else 1.0

            base_revenue = np.random.uniform(100_000, 500_000) * seasonality
            operating_cost = base_revenue * np.random.uniform(0.3, 0.5)
            salary_cost = base_revenue * np.random.uniform(0.2, 0.35)
            marketing_cost = base_revenue * np.random.uniform(0.05, 0.15)
            profit = base_revenue - operating_cost - salary_cost - marketing_cost
            budget = base_revenue * 1.1  # Budget is usually 10% above actuals

            finance.append({
                'month': month,
                'department': department,
                'operating_cost': operating_cost,
                'salary_cost': salary_cost,
                'marketing_cost': marketing_cost,
                'profit': profit,
                'revenue': base_revenue,
                'budget': budget,
            })

    return pd.DataFrame(finance)

def generate_employees():
    """Generate employee data"""
    print("Generating employees...")

    employees = []
    for i in range(NUM_EMPLOYEES):
        experience = np.random.randint(0, 40)
        performance_score = np.random.normal(6.5, 1.5)

        # Attrition correlated with low performance and experience
        attrition_chance = 0.05
        if performance_score < 4:
            attrition_chance = 0.3
        if experience < 2:
            attrition_chance = 0.15

        salary = np.random.uniform(40_000, 150_000) * (1 + experience * 0.02)

        employees.append({
            'employee_id': i + 1,
            'department': np.random.choice(DEPARTMENTS),
            'manager': f'Manager-{np.random.randint(1, 200)}' if np.random.random() > 0.3 else None,
            'region': np.random.choice(REGIONS),
            'experience': experience,
            'performance_score': np.clip(performance_score, 1, 10),
            'attrition': np.random.random() < attrition_chance,
            'salary': salary,
        })

    return pd.DataFrame(employees)

def generate_support_tickets(customers_df, calendar_df):
    """Generate support tickets"""
    print("Generating support tickets...")

    tickets = []
    for i in range(NUM_SUPPORT_TICKETS):
        customer = customers_df.iloc[np.random.randint(0, len(customers_df))]
        created_date = DATE_START + timedelta(days=np.random.randint(0, (DATE_END - DATE_START).days))

        # Resolution time varies by priority
        priority = np.random.choice(PRIORITIES, p=[0.5, 0.30, 0.15, 0.05])
        if priority == 'Critical':
            resolution_time = np.random.randint(1, 8)
        elif priority == 'High':
            resolution_time = np.random.randint(8, 48)
        elif priority == 'Medium':
            resolution_time = np.random.randint(24, 120)
        else:
            resolution_time = np.random.randint(72, 240)

        closed_date = created_date + timedelta(hours=resolution_time)
        satisfaction = 10 - (resolution_time / 24)  # Inversely correlated with resolution time

        tickets.append({
            'ticket_id': i + 1,
            'customer_id': customer['customer_id'],
            'issue_type': np.random.choice(ISSUE_TYPES),
            'priority': priority,
            'resolution_time': resolution_time,
            'satisfaction': np.clip(satisfaction + np.random.normal(0, 1), 1, 10),
            'created_date': created_date,
            'closed_date': closed_date,
        })

    return pd.DataFrame(tickets)

def generate_targets(calendar_df):
    """Generate monthly sales/profit targets"""
    print("Generating targets...")

    targets = []
    for month in pd.date_range(DATE_START.replace(day=1), DATE_END.replace(day=1), freq='MS'):
        seasonality = 1.5 if month.month in [11, 12] else 1.0

        for department in DEPARTMENTS:
            sales_target = np.random.uniform(500_000, 2_000_000) * seasonality
            profit_target = sales_target * np.random.uniform(0.15, 0.25)
            customer_target = int(np.random.uniform(100, 500) * seasonality)

            targets.append({
                'month': month,
                'department': department,
                'sales_target': sales_target,
                'profit_target': profit_target,
                'customer_target': customer_target,
            })

    return pd.DataFrame(targets)

def save_to_parquet(data_dir, name, df):
    """Save dataframe to Parquet"""
    path = data_dir / f'{name}.parquet'
    df.to_parquet(path, index=False, compression='snappy')
    print(f"✓ Saved {name}: {len(df):,} rows → {path}")
    return path

def main():
    # Create output directory
    generator_dir = Path(__file__).parent
    data_dir = generator_dir.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    print(f"\n{'='*60}")
    print(f"RetailMart Global Synthetic Data Generator")
    print(f"{'='*60}\n")

    # Generate all datasets
    calendar = generate_calendar()
    customers = generate_customers()
    products = generate_products()
    sales = generate_sales(customers, products, calendar)
    inventory = generate_inventory(products)
    marketing = generate_marketing(calendar, sales)
    finance = generate_finance(calendar)
    employees = generate_employees()
    support_tickets = generate_support_tickets(customers, calendar)
    targets = generate_targets(calendar)

    # Save to Parquet
    print(f"\n{'='*60}")
    print("Saving to Parquet files...")
    print(f"{'='*60}\n")

    save_to_parquet(data_dir, 'calendar', calendar)
    save_to_parquet(data_dir, 'customers', customers)
    save_to_parquet(data_dir, 'products', products)
    save_to_parquet(data_dir, 'sales', sales)
    save_to_parquet(data_dir, 'inventory', inventory)
    save_to_parquet(data_dir, 'marketing', marketing)
    save_to_parquet(data_dir, 'finance', finance)
    save_to_parquet(data_dir, 'employees', employees)
    save_to_parquet(data_dir, 'support_tickets', support_tickets)
    save_to_parquet(data_dir, 'targets', targets)

    # Print summary
    print(f"\n{'='*60}")
    print("Data Generation Summary")
    print(f"{'='*60}")
    print(f"Customers: {len(customers):,}")
    print(f"Products: {len(products):,}")
    print(f"Sales: {len(sales):,}")
    print(f"Inventory: {len(inventory):,}")
    print(f"Marketing Campaigns: {len(marketing):,}")
    print(f"Finance Records: {len(finance):,}")
    print(f"Employees: {len(employees):,}")
    print(f"Support Tickets: {len(support_tickets):,}")
    print(f"Targets: {len(targets):,}")
    print(f"Calendar Days: {len(calendar):,}")
    print(f"\nAll Parquet files saved to: {data_dir}")
    print(f"Next: python data_warehouse/loader/load.py")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
