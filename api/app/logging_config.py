import logging

from app import config


def setup_logging() -> None:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s level=%(levelname)s service=api msg=%(message)s",
    )
