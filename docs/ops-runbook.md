# Ops Runbook

## Start/stop

- Start all services: `docker-compose up --build`
- Stop: `docker-compose down`

## Health checks

- API: `GET /health`
- UI: open http://localhost:5173

## Logs

- Simulator, processor, api: `docker-compose logs -f <service>`
- Look for processor metrics every 30s: `metrics consumed=... invalid=... alerts=...`

## Verify data flow

1. Ensure simulator is emitting logs.
2. Ensure processor consumed count increases.
3. Call `GET /alerts` with a token and see rows.
4. UI shows alerts and status summary.

## Common issues

- **Kafka not ready**: wait for broker to start, restart simulator/processor.
- **DB locked**: if using SQLite with multiple writers, stop services, delete `hf.db`, restart.
- **Auth failures**: ensure `.env` matches `DEMO_USER/DEMO_PASSWORD`.

## Secret rotation (demo)

- Update `JWT_SECRET` and restart the API service. Existing tokens will expire.
