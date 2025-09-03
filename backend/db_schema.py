import psycopg2

def create_tables(conn):
    """
    Creates the necessary tables in the database if they do not already exist.
    """
    create_health_data_table = """
    CREATE TABLE IF NOT EXISTS health_data (
        machine_id VARCHAR(255) PRIMARY KEY,
        timestamp TIMESTAMP,
        os_info VARCHAR(255),
        disk_encrypted BOOLEAN,
        os_up_to_date BOOLEAN,
        antivirus_active BOOLEAN,
        inactivity_sleep_ok BOOLEAN
    );
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_health_data_table)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()
