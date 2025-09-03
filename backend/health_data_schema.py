from datetime import datetime
from pydantic import BaseModel, Field

class SystemData(BaseModel):
    machine_id: str
    timestamp: datetime
    os_info: str
    disk_encrypted: bool
    os_up_to_date: bool
    antivirus_active: bool
    inactivity_sleep_ok: bool