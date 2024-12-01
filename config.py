from os import getenv
from dotenv import load_dotenv

__all__ = (
    'TOKEN',
    'ROOM_RANGE',
    'DB_URL',
    'TIME_WINDOWS_RESET_TIMEOUT',
    'MAX_RECORDS',
    'LOGS_PATH',
)

load_dotenv()

TOKEN: str = getenv('TOKEN')
ROOM_RANGE: tuple[int, int] = tuple(map(int, getenv('ROOM_RANGE').split(',')))  # type: ignore
DB_URL: str = getenv('DB_URL')
TIME_WINDOWS_RESET_TIMEOUT: float = float(getenv('TIME_WINDOWS_RESET_TIMEOUT'))
MAX_RECORDS: int = int(getenv('MAX_RECORDS'))
LOGS_PATH: str = getenv('LOGS_PATH')
