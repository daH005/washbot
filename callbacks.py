from aiogram.filters.callback_data import CallbackData

__all__ = (
    'WeekDayToOrderSelectedCallbackData',
    'TimeToOrderSelectedCallbackData',
    'TimeToCancelSelectedCallbackData',
)


class WeekDayToOrderSelectedCallbackData(CallbackData, prefix='c1'):
    weekday_id: int


class TimeToOrderSelectedCallbackData(CallbackData, prefix='c2'):
    time_window_id: int


class TimeToCancelSelectedCallbackData(CallbackData, prefix='c4'):
    time_window_id: int
