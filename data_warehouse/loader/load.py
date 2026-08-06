#!/usr/bin/env python3
"""
Load synthetic data from Parquet into PostgreSQL and DuckDB.
Supports loading into both local PostgreSQL and Docker-based PostgreSQL.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import psycopg2
import duckdb
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load variables from the project's .env file (if present) without
# overriding any that are already set in the shell environment.
ENV_PATH = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load config from environment.
# NOTE: Docker Compose maps the Postgres container's 5432 to host port
# 5433 (see docker-compose.yml: "5433:5432"), so the default here must
# be 5433 to match a Dockerized Postgres accessed from the host.
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5433))
POSTGRES_USER = os.getenv('POSTGRES_USER', 'retailmart')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'retailmart_secure_pw')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'retailmart_dw')

DUCKDB_PATH = os.getenv('DUCKDB_PATH', './data_warehouse/retailmart.duckdb')

# Data files
DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_FILES = {
    'calendar': 'calendar',
    'customers': 'customers',
    'products': 'products',
    'sales': 'sales',
    'inventory': 'inventory',
    'marketing': 'marketing',
    'finance': 'finance',
    'employees': 'employees',
    'support_tickets': 'support_tickets',
    'targets': 'targets',
}

def get_postgres_connection():
    """Create PostgreSQL connection"""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB
        )
        logger.info(f"✓ Connected to PostgreSQL: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
        return conn
    except psycopg2.Error as e:
        logger.error(f"✗ Failed to connect to PostgreSQL: {e}")
        raise

def load_postgres(table_name, df, conn):
    """Load dataframe into PostgreSQL table"""
    cursor = conn.cursor()

    try:
        # Convert dataframe to list of tuples for insertion
        columns = ', '.join([f'"{col}"' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))

        insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

        # Convert DataFrame rows to tuples
        data = [tuple(row) for row in df.itertuples(index=False, name=None)]

        # Use executemany for batch insert
        cursor.executemany(insert_query, data)
        conn.commit()

        logger.info(f"✓ Loaded {len(df):,} rows into {table_name}")
        return True

    except Exception as e:
        conn.rollback()
        logger.error(f"✗ Error loading {table_name}: {e}")
        return False
    finally:
        cursor.close()

def load_duckdb(table_name, df):
    """Load dataframe into DuckDB"""
    try:
        conn = duckdb.connect(DUCKDB_PATH)
        conn.register(f'_temp_{table_name}', df)
        conn.execute(f'CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM _temp_{table_name}')
        conn.close()

        logger.info(f"✓ Loaded {len(df):,} rows into DuckDB {table_name}")
        return True

    except Exception as e:
        logger.error(f"✗ Error loading {table_name} to DuckDB: {e}")
        return False

def verify_loads(pg_conn):
    """Verify data was loaded correctly"""
    cursor = pg_conn.cursor()

    print("\n" + "="*60)
    print("Data Load Verification")
    print("="*60 + "\n")

    for table_name in DATA_FILES.keys():
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"{table_name:20} : {count:>10,} rows")

    cursor.close()

def main():
    print(f"\n{'='*60}")
    print("RetailMart Global Data Loader")
    print(f"{'='*60}\n")

    print(f"Source: {DATA_DIR}")
    print(f"PostgreSQL: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print(f"DuckDB: {DUCKDB_PATH}\n")

    # Check if Parquet files exist
    missing_files = []
    for table_name, file_name in DATA_FILES.items():
        parquet_file = DATA_DIR / f'{file_name}.parquet'
        if not parquet_file.exists():
            missing_files.append(file_name)

    if missing_files:
        logger.error(f"Missing Parquet files: {', '.join(missing_files)}")
        logger.error(f"Run: python data_warehouse/generator/generate.py")
        sys.exit(1)

    # Connect to PostgreSQL
    try:
        pg_conn = get_postgres_connection()
    except Exception as e:
        logger.error(f"Cannot proceed without PostgreSQL connection: {e}")
        sys.exit(1)

    # Load each table
    print(f"{'='*60}")
    print("Loading data...")
    print(f"{'='*60}\n")

    for table_name, file_name in DATA_FILES.items():
        parquet_file = DATA_DIR / f'{file_name}.parquet'

        print(f"Loading {table_name}...")
        try:
            df = pd.read_parquet(parquet_file)

            # Type conversions for date columns
            date_columns = ['date', 'month', 'created_date', 'closed_date', 'joining_date',
                          'launch_date', 'order_date', 'delivery_date', 'start_date', 'end_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.date

            # Load to PostgreSQL
            if load_postgres(table_name, df, pg_conn):
                # Also load to DuckDB (in parallel would be nice, but sequential is safe)
                load_duckdb(table_name, df)
            else:
                logger.warning(f"Skipping DuckDB load for {table_name}")

        except Exception as e:
            logger.error(f"Failed to load {table_name}: {e}")
            continue

    # Verify
    verify_loads(pg_conn)

    # Create DuckDB views for ease of querying
    try:
        print(f"\n{'='*60}")
        print("Creating DuckDB views...")
        print(f"{'='*60}\n")

        duck_conn = duckdb.connect(DUCKDB_PATH)

        # Create a simple view for KPI calculation
        duck_conn.execute('''
            CREATE OR REPLACE VIEW sales_summary AS
            SELECT
                YEAR(s.order_date) as year,
                MONTH(s.order_date) as month,
                s.region,
                SUM(s.sales) as total_sales,
                SUM(s.profit) as total_profit,
                COUNT(*) as transaction_count,
                AVG(s.sales) as avg_transaction_value
            FROM sales s
            GROUP BY YEAR(s.order_date), MONTH(s.order_date), s.region
        ''')
        logger.info("✓ Created sales_summary view in DuckDB")

        duck_conn.close()

    except Exception as e:
        logger.warning(f"Could not create views: {e}")

    pg_conn.close()

    print(f"\n{'='*60}")
    print("✓ Data loading complete!")
    print(f"{'='*60}\n")
    print("You can now:")
    print("1. Use PostgreSQL for transactional data and memory")
    print("2. Use DuckDB for fast analytical queries")
    print("3. Run: uvicorn backend.app.main:app --reload")

if __name__ == '__main__':
    main()
