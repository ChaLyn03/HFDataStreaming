from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SignalEvent(BaseModel):
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

    class Config:
        json_schema_extra = {
            "example": {
                "schema_version": "1.0",
                "id": "6b5c7f5f-52a7-4f44-9208-6efc0bda51a2",
                "station_id": "STATION-001",
                "frequency_hz": 7100000.0,
                "snr_db": 10.4,
                "power_dbm": 12.3,
                "timestamp": "2024-01-01T00:00:00Z",
                "lat": 40.7,
                "lon": -74.0,
                "band": "40m",
            }
        }
