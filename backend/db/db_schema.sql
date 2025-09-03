CREATE TABLE IF NOT EXISTS health_data (
    machine_id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMP,
    os_info VARCHAR(255),
    disk_encrypted BOOLEAN,
    os_up_to_date BOOLEAN,
    antivirus_active BOOLEAN,
    inactivity_sleep_ok BOOLEAN
);