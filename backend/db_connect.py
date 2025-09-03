import psycopg2
import os

def get_db_connection():
    """
    Establishes and returns a database connection.
    Uses environment variables for connection details.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "healthdb"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password")
        )
        return conn
    except psycopg2.OperationalError as e:
       
        print(f"Failed to connect to the database: {e}")
        return None

con=get_db_connection()