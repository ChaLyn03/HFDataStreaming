# Data Model

## Tables

### signals

- `id` (PK, UUID string)
- `station_id` (string, indexed)
- `frequency_hz` (float)
- `snr_db` (float)
- `power_dbm` (float, nullable)
- `band` (string)
- `timestamp` (datetime)
- `lat` (float, nullable)
- `lon` (float, nullable)
- `raw_json` (text)

### alerts

- `id` (PK, UUID string)
- `signal_id` (UUID string, indexed)
- `station_id` (string, indexed)
- `severity` (string)
- `alert_type` (string)
- `message` (string)
- `created_at` (datetime)

## Kafka message schemas

### hf.signals

```json
{
  "schema_version": "1.0",
  "id": "uuid",
  "station_id": "STATION-001",
  "frequency_hz": 7100000.0,
  "snr_db": 10.2,
  "power_dbm": 12.1,
  "timestamp": "2024-01-01T00:00:00Z",
  "lat": 40.7,
  "lon": -74.0,
  "band": "40m"
}
```

Invalid example:

```json
{
  "id": "not-a-uuid",
  "station_id": 123,
  "timestamp": "nope"
}
```

### hf.alerts

```json
{
  "id": "uuid",
  "signal_id": "uuid",
  "station_id": "STATION-001",
  "severity": "warning",
  "alert_type": "LOW_SNR",
  "message": "SNR 4.1 below 6.0",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Versioning

Messages include `schema_version` and can evolve by adding optional fields. Unknown fields are ignored by the processor.
