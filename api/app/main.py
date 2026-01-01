from fastapi import FastAPI

from app.logging_config import setup_logging
from app.routes import alerts, auth, health, signals, stats


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="HF Signal Monitoring API")
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(signals.router)
    app.include_router(alerts.router)
    app.include_router(stats.router)
    return app


app = create_app()
