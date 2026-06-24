import pymysql
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    # Ensure these keys match your .env file exactly
    password = os.getenv("MYSQL_PWD", "")
    db_name = os.getenv("DB_NAME", "")
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    
    # Use pymysql directly instead of mysql.connector
    return pymysql.connect(
        host=host,
        user=user,
        password=password, 
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor # This replaces dictionary=True
    )

def fetch_all_users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM hackathon_entries ORDER BY entry_id DESC;")
            results = cursor.fetchall()
            for row in results:
                for key, value in row.items():
                    if isinstance(value, (datetime.date, datetime.datetime)):
                        row[key] = value.isoformat()
        return results
    finally:
        conn.close()

def get_user_id_by_email(email: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM hackathon_entries WHERE user_email = %s LIMIT 1", (email,))
            result = cursor.fetchone()
            if result:
                return result['user_id']
            return None
    finally:
        conn.close()

def insert_user(user_data: dict):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # We omit entry_id and user_id from INSERT if they are auto-increment,
            # or we insert them if provided. Let's assume we insert them if they are in the dict and not None.
            # But the user asked to automatically generate them. Let's handle it in Python to ensure they exist.
            columns = ", ".join(user_data.keys())
            placeholders = ", ".join(["%s"] * len(user_data))
            sql = f"INSERT INTO hackathon_entries ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(user_data.values()))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def delete_hackathon(entry_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM hackathon_entries WHERE entry_id = %s", (entry_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def update_hackathon(entry_id: int, update_data: dict):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            set_clauses = []
            values = []
            for k, v in update_data.items():
                if k not in ['entry_id', 'user_id', 'created_at'] and v is not None:
                    set_clauses.append(f"{k} = %s")
                    values.append(v)
            
            if not set_clauses:
                return False
                
            sql = f"UPDATE hackathon_entries SET {', '.join(set_clauses)} WHERE entry_id = %s"
            values.append(entry_id)
            cursor.execute(sql, tuple(values))
        conn.commit()
        return True
    finally:
        conn.close()