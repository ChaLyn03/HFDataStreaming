from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app import config

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


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
