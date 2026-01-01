from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BandRange:
    name: str
    min_hz: float
    max_hz: float


HF_BANDS = [
    BandRange("160m", 1_800_000, 2_000_000),
    BandRange("80m", 3_500_000, 4_000_000),
    BandRange("40m", 7_000_000, 7_300_000),
    BandRange("20m", 14_000_000, 14_350_000),
    BandRange("15m", 21_000_000, 21_450_000),
    BandRange("10m", 28_000_000, 29_700_000),
]


def band_for_frequency(freq_hz: float) -> str:
    for band in HF_BANDS:
        if band.min_hz <= freq_hz <= band.max_hz:
            return band.name
    return "unknown"
