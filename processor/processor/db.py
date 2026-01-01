from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable

from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from processor import config
from processor.models import Alert, SignalEvent

Base = declarative_base()


class Signal(Base):
    __tablename__ = "signals"

    id = Column(String, primary_key=True)
    station_id = Column(String, index=True)
    frequency_hz = Column(Float)
    snr_db = Column(Float)
    power_dbm = Column(Float, nullable=True)
    band = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    raw_json = Column(Text)


class AlertRecord(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    signal_id = Column(String, index=True)
    station_id = Column(String, index=True)
    severity = Column(String, index=True)
    alert_type = Column(String, index=True)
    message = Column(String)
    created_at = Column(DateTime, index=True)


def _build_engine():
    connect_args = {"check_same_thread": False} if config.DB_URL.startswith("sqlite") else {}
    return create_engine(config.DB_URL, future=True, echo=False, connect_args=connect_args)


ENGINE = _build_engine()
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=ENGINE)


def insert_signal(session: Session, event: SignalEvent) -> None:
    record = Signal(
        id=str(event.id),
        station_id=event.station_id,
        frequency_hz=event.frequency_hz,
        snr_db=event.snr_db,
        power_dbm=event.power_dbm,
        band=event.band,
        timestamp=event.timestamp,
        lat=event.lat,
        lon=event.lon,
        raw_json=json.dumps(event.model_dump(mode="json")),
    )
    session.add(record)


def insert_alerts(session: Session, alerts: Iterable[Alert]) -> None:
    for alert in alerts:
        session.add(
            AlertRecord(
                id=str(alert.id),
                signal_id=str(alert.signal_id),
                station_id=alert.station_id,
                severity=alert.severity,
                alert_type=alert.alert_type,
                message=alert.message,
                created_at=alert.created_at,
            )
        )
