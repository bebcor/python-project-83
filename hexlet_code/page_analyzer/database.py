import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Инициализация БД при старте приложения"""
    print("Initializing database...")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'urls'
                );
            """)
            exists = cur.fetchone()[0]
            
            if not exists:
                print("Creating database tables...")
                with open('database.sql', 'r') as f:
                    sql_script = f.read()
                cur.execute(sql_script)
                conn.commit()
                print("Database tables created successfully")
            else:
                print("Tables already exist")
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
