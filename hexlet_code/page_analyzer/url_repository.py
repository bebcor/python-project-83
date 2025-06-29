import psycopg2

from .database import DATABASE_URL


def find_url_by_name(url_name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM urls WHERE name = %s",
                (url_name,)
            )
            return cursor.fetchone()


def create_url(url_name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO urls (name) "
                "VALUES (%s) RETURNING id, name, created_at",
                (url_name,)
            )
            return cursor.fetchone()


def get_url_by_id(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM urls WHERE id = %s",
                (url_id,)
            )
            return cursor.fetchone()


def get_all_urls_with_checks():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.id, 
                    u.name,
                    MAX(uc.created_at) AS last_check_date,
                    (SELECT status_code 
                     FROM url_checks 
                     WHERE url_id = u.id 
                     ORDER BY created_at DESC 
                     LIMIT 1) AS last_check_status
                FROM urls u
                LEFT JOIN url_checks uc ON u.id = uc.url_id
                GROUP BY u.id
                ORDER BY u.id DESC
            """)
            return cursor.fetchall()


def get_url_checks(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, status_code, h1, title, description, created_at "
                "FROM url_checks WHERE url_id = %s ORDER BY id DESC",
                (url_id,)
            )
            checks = []
            for row in cursor.fetchall():
                checks.append({
                    'id': row[0],
                    'status_code': row[1],
                    'h1': row[2],
                    'title': row[3],
                    'description': row[4],
                    'created_at': row[5].strftime('%Y-%m-%d') if row[5] else ''
                })
            return checks


def create_url_check(
        url_id, status_code=None, h1=None, title=None, description=None
):
    h1 = h1[:255] if h1 and len(h1) > 255 else h1
    title = title[:255] if title and len(title) > 255 else title
    description = (
    description[:500] 
    if description and len(description) > 500 
    else description
    )
    
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO url_checks "
                "(url_id, status_code, h1, title, description) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at",
                (url_id, status_code, h1, title, description)
            )
            return cursor.fetchone()
