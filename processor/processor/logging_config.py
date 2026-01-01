import logging

from processor import config


def setup_logging() -> None:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s level=%(levelname)s service=processor msg=%(message)s",
    )
