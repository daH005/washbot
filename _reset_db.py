from datetime import time, datetime, timedelta
from os import remove as remove_file

from db import Base, WeekDay, TimeWindow

if __name__ == '__main__':
    answer = None
    while answer != 'yes':
        answer = input('Для сброса БД введите yes: ')

    try:
        remove_file('db.db')
    except FileNotFoundError:
        pass
        
    Base.reset_db()

    weekdays_dates = {}

    cur_datetime = datetime.now()
    WEEKDAY_INDICES = range(0, 7)
    for _ in WEEKDAY_INDICES:
        weekdays_dates[cur_datetime.weekday()] = cur_datetime.date()
        cur_datetime += timedelta(days=1)

    TIME_WINDOWS = (
        (
            time(8, 0),
            time(10, 0),
        ),
        (
            time(10, 0),
            time(12, 0),
        ),
        (
            time(12, 0),
            time(14, 0),
        ),
        (
            time(14, 0),
            time(16, 0),
        ),
        (
            time(16, 0),
            time(18, 0),
        ),
        (
            time(18, 0),
            time(20, 0),
        ),
        (
            time(20, 0),
            time(22, 0),
        ),
    )

    for weekday_index in WEEKDAY_INDICES:

        wash_weekday = WeekDay(value=weekday_index)
        Base.get_session().add(wash_weekday)
        Base.get_session().flush()

        for start, end in TIME_WINDOWS:
            wash_time_window = TimeWindow(
                weekday_id=wash_weekday.id,
                date=weekdays_dates[weekday_index],
                start=start,
                end=end,
            )
            Base.get_session().add(wash_time_window)

        Base.get_session().commit()

    print('Операция успешно выполнена.')
    while True:
        pass
