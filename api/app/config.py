import os


def _get_env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


DB_URL = os.getenv("DB_URL", "sqlite:///./hf.db")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_EXPIRE_MINUTES = _get_env_int("JWT_EXPIRE_MINUTES", 60)
DEMO_USER = os.getenv("DEMO_USER", "demo")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "demo")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
