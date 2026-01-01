from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db, schemas
from app.security import get_current_user

router = APIRouter()


@router.get("/signals", response_model=List[schemas.SignalOut])
def list_signals(
    station_id: Optional[str] = None,
    band: Optional[str] = None,
    since: Optional[datetime] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: Session = Depends(db.get_session),
    _user=Depends(get_current_user),
):
    stmt = select(db.Signal)
    if station_id:
        stmt = stmt.where(db.Signal.station_id == station_id)
    if band:
        stmt = stmt.where(db.Signal.band == band)
    if since:
        stmt = stmt.where(db.Signal.timestamp >= since)

    stmt = stmt.order_by(db.Signal.timestamp.desc()).offset(offset).limit(limit)
    results = session.execute(stmt).scalars().all()
    return [
        schemas.SignalOut(
            id=row.id,
            station_id=row.station_id,
            frequency_hz=row.frequency_hz,
            snr_db=row.snr_db,
            power_dbm=row.power_dbm,
            band=row.band,
            timestamp=row.timestamp,
            lat=row.lat,
            lon=row.lon,
        )
        for row in results
    ]
