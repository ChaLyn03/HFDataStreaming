import json
import logging
import time
from datetime import datetime, timezone
from uuid import uuid4

from kafka import KafkaConsumer, KafkaProducer
from pydantic import ValidationError

from processor import config, db, models, rules
from processor.logging_config import setup_logging


logger = logging.getLogger("processor")


def _parse_message(raw_value: bytes) -> models.SignalEvent | None:
    try:
        payload = json.loads(raw_value.decode("utf-8"))
        return models.SignalEvent.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("invalid message error=%s", exc)
        return None


def main() -> None:
    setup_logging()
    db.init_db()

    consumer = KafkaConsumer(
        config.KAFKA_SIGNAL_TOPIC,
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        group_id=config.KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: v,
    )
    producer = KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    totals = {"consumed": 0, "invalid": 0, "alerts": 0}
    last_log = time.time()

    logger.info("processor started topic=%s", config.KAFKA_SIGNAL_TOPIC)
    for message in consumer:
        event = _parse_message(message.value)
        totals["consumed"] += 1
        if event is None:
            totals["invalid"] += 1
            continue

        alert_rules = rules.evaluate_rules(event)
        alerts = []
        now = datetime.now(timezone.utc)
        for rule in alert_rules:
            alerts.append(
                models.Alert(
                    id=uuid4(),
                    signal_id=event.id,
                    station_id=event.station_id,
                    severity=rule.severity,
                    alert_type=rule.alert_type,
                    message=rule.message,
                    created_at=now,
                )
            )

        with db.SessionLocal() as session:
            db.insert_signal(session, event)
            if alerts:
                db.insert_alerts(session, alerts)
            session.commit()

        if alerts:
            totals["alerts"] += len(alerts)
            for alert in alerts:
                producer.send(config.KAFKA_ALERT_TOPIC, alert.model_dump(mode="json"))

        if time.time() - last_log >= 30:
            logger.info(
                "metrics consumed=%s invalid=%s alerts=%s",
                totals["consumed"],
                totals["invalid"],
                totals["alerts"],
            )
            last_log = time.time()


if __name__ == "__main__":
    main()
