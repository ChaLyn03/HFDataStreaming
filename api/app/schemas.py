from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SignalOut(BaseModel):
    id: str
    station_id: str
    frequency_hz: float
    snr_db: float
    power_dbm: Optional[float] = None
    band: str
    timestamp: datetime
    lat: Optional[float] = None
    lon: Optional[float] = None


class AlertOut(BaseModel):
    id: str
    signal_id: str
    station_id: str
    severity: str
    alert_type: str
    message: str
    created_at: datetime


class StatsSummary(BaseModel):
    station_id: str
    count: int
    avg_snr: float
    alert_count: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    scopes: List[str] = []
