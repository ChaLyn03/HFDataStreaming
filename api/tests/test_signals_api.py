from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import db
from app.main import create_app
from app.security import create_access_token


def test_list_signals_requires_auth():
    app = create_app()
    client = TestClient(app)
    resp = client.get("/signals")
    assert resp.status_code == 403


def test_list_signals():
    engine = create_engine("sqlite:///:memory:", future=True)
    db.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, future=True)

    app = create_app()

    def _get_session_override():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.get_session] = _get_session_override

    with Session(engine) as session:
        session.add(
            db.Signal(
                id="signal-1",
                station_id="STATION-001",
                frequency_hz=7_100_000,
                snr_db=12.0,
                power_dbm=10.0,
                band="40m",
                timestamp=datetime.now(timezone.utc),
                lat=10.0,
                lon=20.0,
                raw_json="{}",
            )
        )
        session.commit()

    token = create_access_token("demo")
    client = TestClient(app)
    resp = client.get("/signals", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
