import asyncio
from datetime import datetime, timedelta

from db import TimeWindow
from config import TIME_WINDOWS_RESET_TIMEOUT

__all__ = (
    'start_change_date_task',
)


def start_change_date_task() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(_task())


async def _task() -> None:
    print('Поток сброса окон подключен.')

    while True:
        await asyncio.sleep(TIME_WINDOWS_RESET_TIMEOUT)
        print('Проверка окон...')

        now = datetime.now()
        for time_window in TimeWindow.all():
            if now > datetime.combine(time_window.date, time_window.end):
                time_window.date += timedelta(days=7)
                time_window.user_id = None
                TimeWindow.get_session().commit()

                print(f'Сброшено окно {time_window.text} ({time_window.weekday.text}).')
