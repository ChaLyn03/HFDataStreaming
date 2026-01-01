import os


def _get_env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:9092")
KAFKA_SIGNAL_TOPIC = os.getenv("KAFKA_SIGNAL_TOPIC", "hf.signals")
KAFKA_ALERT_TOPIC = os.getenv("KAFKA_ALERT_TOPIC", "hf.alerts")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "processor-service")

THRESHOLD_SNR_DB = _get_env_float("THRESHOLD_SNR_DB", 6.0)
THRESHOLD_POWER_DBM = _get_env_float("THRESHOLD_POWER_DBM", 20.0)
BAND_MIN_HZ = _get_env_float("BAND_MIN_HZ", 3_000_000)
BAND_MAX_HZ = _get_env_float("BAND_MAX_HZ", 30_000_000)

DB_URL = os.getenv("DB_URL", "sqlite:///./hf.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
