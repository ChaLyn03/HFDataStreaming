from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from processor import db, models


def test_insert_signal_and_alerts():
    engine = create_engine("sqlite:///:memory:", future=True)
    db.Base.metadata.create_all(bind=engine)

    event = models.SignalEvent(
        id=uuid4(),
        station_id="STATION-001",
        frequency_hz=7_100_000,
        snr_db=5.0,
        power_dbm=25.0,
        timestamp=datetime.now(timezone.utc),
        band="40m",
    )
    alert = models.Alert(
        id=uuid4(),
        signal_id=event.id,
        station_id=event.station_id,
        severity="warning",
        alert_type="HIGH_POWER",
        message="Power high",
        created_at=datetime.now(timezone.utc),
    )

    with Session(engine) as session:
        db.insert_signal(session, event)
        db.insert_alerts(session, [alert])
        session.commit()

        assert session.execute(select(db.Signal)).first() is not None
        assert session.execute(select(db.AlertRecord)).first() is not None
