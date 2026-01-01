from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SignalEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    schema_version: str = "1.0"
    id: UUID
    station_id: str
    frequency_hz: float
    snr_db: float
    power_dbm: Optional[float] = None
    timestamp: datetime
    lat: Optional[float] = None
    lon: Optional[float] = None
    band: str


class Alert(BaseModel):
    id: UUID
    signal_id: UUID
    station_id: str
    severity: str
    alert_type: str
    message: str
    created_at: datetime
