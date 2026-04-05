from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class IoTData(BaseModel):
    device_id: str
    timestamp: datetime
    data_size_kb: float
    temperature: float
    firmware_version: str
    metadata: Optional[Dict] = {}

class SecurityAlert(BaseModel):
    device_id: str
    event_type: str
    severity: str
    description: str
    timestamp: datetime