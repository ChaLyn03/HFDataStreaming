from __future__ import annotations

from dataclasses import dataclass
from typing import List

from processor import config
from processor.models import SignalEvent


@dataclass(frozen=True)
class AlertRule:
    alert_type: str
    severity: str
    message: str


def evaluate_rules(event: SignalEvent) -> List[AlertRule]:
    alerts: List[AlertRule] = []
    if event.snr_db < config.THRESHOLD_SNR_DB:
        alerts.append(
            AlertRule(
                alert_type="LOW_SNR",
                severity="warning",
                message=f"SNR {event.snr_db:.1f} below {config.THRESHOLD_SNR_DB}",
            )
        )
    if not (config.BAND_MIN_HZ <= event.frequency_hz <= config.BAND_MAX_HZ):
        alerts.append(
            AlertRule(
                alert_type="OUT_OF_BAND",
                severity="critical",
                message=f"Frequency {event.frequency_hz:.0f} outside {config.BAND_MIN_HZ}-{config.BAND_MAX_HZ}",
            )
        )
    if event.power_dbm is not None and event.power_dbm > config.THRESHOLD_POWER_DBM:
        alerts.append(
            AlertRule(
                alert_type="HIGH_POWER",
                severity="warning",
                message=f"Power {event.power_dbm:.1f} above {config.THRESHOLD_POWER_DBM}",
            )
        )
    return alerts
