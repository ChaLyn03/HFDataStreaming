from simulator.utils import band_for_frequency


def test_band_for_frequency_known_band():
    assert band_for_frequency(7_100_000) == "40m"


def test_band_for_frequency_unknown():
    assert band_for_frequency(5_000_000) == "unknown"
