import os


def _get_env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


def _get_env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:9092")
KAFKA_SIGNAL_TOPIC = os.getenv("KAFKA_SIGNAL_TOPIC", "hf.signals")

GEN_RATE_EVENTS_PER_SEC = _get_env_int("GEN_RATE_EVENTS_PER_SEC", 5)
NUM_STATIONS = _get_env_int("NUM_STATIONS", 5)
FREQ_MIN_HZ = _get_env_float("FREQ_MIN_HZ", 3_000_000)
FREQ_MAX_HZ = _get_env_float("FREQ_MAX_HZ", 30_000_000)

SNR_MEAN_DB = _get_env_float("SNR_MEAN_DB", 12.0)
SNR_STD_DB = _get_env_float("SNR_STD_DB", 4.0)
POWER_MEAN_DBM = _get_env_float("POWER_MEAN_DBM", 10.0)
POWER_STD_DBM = _get_env_float("POWER_STD_DBM", 5.0)
