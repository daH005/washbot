import logging

from config import LOGS_PATH

__all__ = (
    'start_logging',
)


def start_logging() -> None:
    logging.basicConfig(
        filename=LOGS_PATH,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
