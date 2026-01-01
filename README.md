# HF Signal Monitoring & Alert Platform (demo)

Simulated HF signal events are streamed through Kafka, processed into alerts, stored in SQLite, and surfaced via a FastAPI backend and React dashboard. Everything runs in containers with optional Kubernetes manifests.

## Quickstart (Docker)

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Start services:
   ```bash
   docker-compose up --build
   ```
3. Open UI: http://localhost:5173
4. Login with `demo / demo`.

## Local (bare metal)

- Start Kafka + Zookeeper via Docker:
  ```bash
  docker-compose up zookeeper broker
  ```
- Run simulator:
  ```bash
  cd simulator
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  python -m simulator.main
  ```
- Run processor:
  ```bash
  cd processor
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  python -m processor.main
  ```
- Run API:
  ```bash
  cd api
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  ```
- Run UI:
  ```bash
  cd ui
  npm install
  npm run dev
  ```

## Smoke test

- `GET /health` returns `{"status":"ok"}`.
- Simulator logs show events emitted.
- Processor logs show metrics every 30s.
- Alerts appear in the UI dashboard.

## Repo layout

- `simulator/` HF signal simulator
- `processor/` Kafka consumer + alert logic + DB writes
- `api/` FastAPI query service
- `ui/` React dashboard
- `docs/` architecture and operational docs
- `infra/` Kubernetes manifests

## Tests

- Python: `pytest` in `simulator/`, `processor/`, `api/`
- UI: `npm test` in `ui/`

## Kubernetes

See `infra/k8s/` for manifests. Use `kind` or `minikube`.

## Notes

- SQLite is used by default for dev. Swap `DB_URL` to Postgres if desired.
- Kafka topics are auto-created by the broker if missing.
