import json
import logging
import random
import time
from datetime import datetime, timezone
from uuid import uuid4

from kafka import KafkaProducer

from simulator import config
from simulator.models import SignalEvent
from simulator.utils import band_for_frequency

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s level=%(levelname)s service=simulator msg=%(message)s",
)
logger = logging.getLogger("simulator")


def _build_event() -> SignalEvent:
    freq = random.uniform(config.FREQ_MIN_HZ, config.FREQ_MAX_HZ)
    snr = random.gauss(config.SNR_MEAN_DB, config.SNR_STD_DB)
    power = random.gauss(config.POWER_MEAN_DBM, config.POWER_STD_DBM)
    station_id = f"STATION-{random.randint(1, config.NUM_STATIONS):03d}"
    event = SignalEvent(
        id=uuid4(),
        station_id=station_id,
        frequency_hz=freq,
        snr_db=snr,
        power_dbm=power,
        timestamp=datetime.now(timezone.utc),
        band=band_for_frequency(freq),
        lat=random.uniform(-90, 90),
        lon=random.uniform(-180, 180),
    )
    return event


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    interval = 1.0 / max(config.GEN_RATE_EVENTS_PER_SEC, 1)
    logger.info("starting simulator rate=%s topic=%s", config.GEN_RATE_EVENTS_PER_SEC, config.KAFKA_SIGNAL_TOPIC)
    try:
        while True:
            event = _build_event()
            producer.send(config.KAFKA_SIGNAL_TOPIC, event.model_dump(mode="json"))
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("shutdown requested")
    finally:
        producer.flush(5)
        producer.close()


if __name__ == "__main__":
    main()
