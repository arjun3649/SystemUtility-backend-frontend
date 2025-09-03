from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_connect import get_db_connection
from health_data_schema import SystemData
from db_schema import create_tables
import psycopg2

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the table if it doesn't exist on startup
conn = get_db_connection()
if conn:
    create_tables(conn)
    conn.close()

@app.post("/api/health-check")
def health_check(data: SystemData):
    """
    Receives system health data and saves it to the database.
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            # Use ON CONFLICT to handle updates for existing machine_id
            cursor.execute(
                """
                INSERT INTO health_data (
                    machine_id, timestamp, os_info, disk_encrypted, 
                    os_up_to_date, antivirus_active, inactivity_sleep_ok
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (machine_id) DO UPDATE SET
                    timestamp = EXCLUDED.timestamp,
                    os_info = EXCLUDED.os_info,
                    disk_encrypted = EXCLUDED.disk_encrypted,
                    os_up_to_date = EXCLUDED.os_up_to_date,
                    antivirus_active = EXCLUDED.antivirus_active,
                    inactivity_sleep_ok = EXCLUDED.inactivity_sleep_ok;
                """,
                (
                    data.machine_id, data.timestamp, data.os_info, data.disk_encrypted,
                    data.os_up_to_date, data.antivirus_active, data.inactivity_sleep_ok
                )
            )
        conn.commit()
        return {"status": "success", "message": "Health data saved"}
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/api/machines")
def get_all_machines():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT machine_id, timestamp, os_info, disk_encrypted, 
                       os_up_to_date, antivirus_active, inactivity_sleep_ok
                FROM health_data 
                ORDER BY timestamp DESC
                """
            )
            results = cursor.fetchall()
            
            machines = []
            for result in results:
                machines.append({
                    "machine_id": result[0],
                    "timestamp": result[1],
                    "os_info": result[2],
                    "disk_encrypted": result[3],
                    "os_up_to_date": result[4],
                    "antivirus_active": result[5],
                    "inactivity_sleep_ok": result[6]
                })
            
            return machines
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/api/machine-state/{machine_id}")
def get_machine_state(machine_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT machine_id, timestamp, os_info, disk_encrypted, 
                       os_up_to_date, antivirus_active, inactivity_sleep_ok
                FROM health_data 
                WHERE machine_id = %s
                """,
                (machine_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Machine not found")
            
            return {
                "machine_id": result[0],
                "timestamp": result[1],
                "os_info": result[2],
                "disk_encrypted": result[3],
                "os_up_to_date": result[4],
                "antivirus_active": result[5],
                "inactivity_sleep_ok": result[6]
            }
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
