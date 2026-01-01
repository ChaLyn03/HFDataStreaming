from datetime import datetime, timezone
from uuid import uuid4

from processor import rules
from processor.models import SignalEvent


def _event(**overrides):
    base = dict(
        id=uuid4(),
        station_id="STATION-001",
        frequency_hz=7_100_000,
        snr_db=10.0,
        power_dbm=10.0,
        timestamp=datetime.now(timezone.utc),
        band="40m",
    )
    base.update(overrides)
    return SignalEvent(**base)


def test_low_snr_rule():
    event = _event(snr_db=2.0)
    alerts = rules.evaluate_rules(event)
    assert any(a.alert_type == "LOW_SNR" for a in alerts)


def test_out_of_band_rule():
    event = _event(frequency_hz=50_000_000)
    alerts = rules.evaluate_rules(event)
    assert any(a.alert_type == "OUT_OF_BAND" for a in alerts)
