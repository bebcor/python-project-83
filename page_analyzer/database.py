import logging
import os
import time

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection(max_retries=5, retry_delay=2):
    attempt = 0
    while attempt < max_retries:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            logger.info("Successfully connected to database")
            return conn
        except OperationalError as e:
            attempt += 1
            error_msg = (
                f"Database connection error "
                f"(attempt {attempt}/{max_retries}): {str(e)}"
            )
            logger.warning(error_msg)
            if attempt < max_retries:
                time.sleep(retry_delay)
    
    logger.error(f"Failed to connect to database after {max_retries} attempts")
    raise RuntimeError("Database connection failed")


def init_db():
    logger.info("Initializing database...")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'urls'
                );
            """)
            exists = cur.fetchone()[0]
            
            if not exists:
                logger.info("Creating database tables...")
                with open('database.sql', 'r') as f:
                    sql_script = f.read()
                cur.execute(sql_script)
                conn.commit()
                logger.info("Database tables created successfully")
            else:
                logger.info("Tables already exist")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
