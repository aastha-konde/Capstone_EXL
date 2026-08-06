#!/usr/bin/env python3
"""
Initialize PostgreSQL database and schema for RetailMart.
Runs all SQL files in the schema directory.
"""

import os
import psycopg2
from psycopg2 import sql
import logging
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load config from environment
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5433))
POSTGRES_USER = os.getenv('POSTGRES_USER', 'retailmart')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'retailmart_secure_pw')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'retailmart_dw')

SCHEMA_DIR = Path(__file__).parent.parent / 'schema'

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect to default 'postgres' database to create new database
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (POSTGRES_DB,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(POSTGRES_DB)))
            logger.info(f"✓ Created database: {POSTGRES_DB}")
        else:
            logger.info(f"✓ Database already exists: {POSTGRES_DB}")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        logger.error(f"✗ Failed to create database: {e}")
        raise

def init_schema():
    """Run all SQL files in schema directory"""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB
        )
        cursor = conn.cursor()

        # Get all SQL files in order
        sql_files = sorted([f for f in SCHEMA_DIR.glob('*.sql')])

        if not sql_files:
            logger.warning(f"No SQL files found in {SCHEMA_DIR}")
            return

        for sql_file in sql_files:
            logger.info(f"Running: {sql_file.name}")
            with open(sql_file, 'r') as f:
                sql_content = f.read()

            try:
                cursor.execute(sql_content)
                conn.commit()
                logger.info(f"✓ Completed: {sql_file.name}")
            except psycopg2.Error as e:
                conn.rollback()
                logger.error(f"✗ Error in {sql_file.name}: {e}")
                raise

        cursor.close()
        conn.close()
        logger.info("✓ Database schema initialized successfully")

    except psycopg2.Error as e:
        logger.error(f"✗ Failed to initialize schema: {e}")
        raise

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("RetailMart Database Initialization")
    logger.info("=" * 60)
    logger.info(f"Host: {POSTGRES_HOST}:{POSTGRES_PORT}")
    logger.info(f"Database: {POSTGRES_DB}")
    logger.info(f"Schema: {SCHEMA_DIR}")
    logger.info("=" * 60)

    try:
        create_database()
        init_schema()
        logger.info("✓ Database initialization complete!")
    except Exception as e:
        logger.error(f"✗ Initialization failed: {e}")
        exit(1)
