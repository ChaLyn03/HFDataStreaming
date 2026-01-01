# Design Decisions

- **Kafka for streaming**: demonstrates partitioned ingest, consumer groups, and event-driven processing.
- **FastAPI**: quick OpenAPI docs and typed request/response modeling.
- **SQLite default**: low-friction dev DB; swap to Postgres via `DB_URL`.
- **Simple JWT auth**: minimal demo authentication; production would use OIDC/IdP.
- **Separation of ingest and query**: processor writes to DB; API only reads.
