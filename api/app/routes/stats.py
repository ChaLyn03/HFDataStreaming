from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import db, schemas
from app.security import get_current_user

router = APIRouter()


@router.get("/stats/summary", response_model=List[schemas.StatsSummary])
def stats_summary(
    session: Session = Depends(db.get_session),
    _user=Depends(get_current_user),
):
    signal_stmt = (
        select(
            db.Signal.station_id,
            func.count(db.Signal.id).label("count"),
            func.avg(db.Signal.snr_db).label("avg_snr"),
        )
        .group_by(db.Signal.station_id)
    )
    alert_stmt = (
        select(
            db.AlertRecord.station_id,
            func.count(db.AlertRecord.id).label("alert_count"),
        )
        .group_by(db.AlertRecord.station_id)
    )
    signals = {row.station_id: row for row in session.execute(signal_stmt)}
    alerts = {row.station_id: row for row in session.execute(alert_stmt)}

    station_ids = set(signals) | set(alerts)
    response = []
    for station_id in sorted(station_ids):
        sig = signals.get(station_id)
        alert = alerts.get(station_id)
        response.append(
            schemas.StatsSummary(
                station_id=station_id,
                count=int(sig.count) if sig else 0,
                avg_snr=float(sig.avg_snr) if sig and sig.avg_snr is not None else 0.0,
                alert_count=int(alert.alert_count) if alert else 0,
            )
        )
    return response
