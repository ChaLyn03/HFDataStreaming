# Architecture

## Overview

The platform simulates HF signal events, streams them via Kafka, processes them into alerts, stores results in a relational database, and exposes read-only APIs for a React dashboard.

## Components

- **Simulator**: Generates synthetic HF signal events and publishes to Kafka topic `hf.signals`.
- **Processor**: Consumes `hf.signals`, validates messages, applies alert rules, writes `signals` and `alerts` tables, and publishes alerts to `hf.alerts`.
- **API**: FastAPI service that queries the database for signals, alerts, and summary stats. Protected with JWT.
- **UI**: React dashboard that authenticates and displays alerts, status summaries, and an SNR trend.

## Data flow

1. Simulator publishes JSON events to Kafka.
2. Processor consumes events, applies rules, writes DB rows, emits alerts.
3. API queries DB for read-only data.
4. UI calls API using a bearer token.

## Kafka

- Topics: `hf.signals` (3 partitions), `hf.alerts` (optional)
- Consumer groups: `processor-service`
- Strategy: keep ingest (Kafka) and query (DB/API) separate for scaling and failure isolation.

## Deployment

- **Local dev**: Docker Compose (Kafka, simulator, processor, API, UI)
- **K8s**: manifests in `infra/k8s/`

## Security

Demo JWT auth with one configured user. In production, replace with an IdP (OIDC) or centralized auth service.
