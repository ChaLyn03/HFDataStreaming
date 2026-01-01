from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db, schemas
from app.security import get_current_user

router = APIRouter()


@router.get("/alerts", response_model=List[schemas.AlertOut])
def list_alerts(
    station_id: Optional[str] = None,
    severity: Optional[str] = None,
    since: Optional[datetime] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: Session = Depends(db.get_session),
    _user=Depends(get_current_user),
):
    stmt = select(db.AlertRecord)
    if station_id:
        stmt = stmt.where(db.AlertRecord.station_id == station_id)
    if severity:
        stmt = stmt.where(db.AlertRecord.severity == severity)
    if since:
        stmt = stmt.where(db.AlertRecord.created_at >= since)

    stmt = stmt.order_by(db.AlertRecord.created_at.desc()).offset(offset).limit(limit)
    results = session.execute(stmt).scalars().all()
    return [
        schemas.AlertOut(
            id=row.id,
            signal_id=row.signal_id,
            station_id=row.station_id,
            severity=row.severity,
            alert_type=row.alert_type,
            message=row.message,
            created_at=row.created_at,
        )
        for row in results
    ]
