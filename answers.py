from enum import StrEnum

from commands import CommandName

__all__ = (
    'Answer',
)


class Answer(StrEnum):

    START = (f'День добрый! Установите номер вашей комнаты для начала работы - {CommandName.SET_ROOM.with_slash}\n'
             f'Далее можно записаться с помощью {CommandName.WASH.with_slash} '
             f'либо отменить запись через {CommandName.CANCEL_WASH.with_slash}')
    SET_ROOM = 'Введите номер комнаты (от 200 до 226)'
    ROOM_IS_INSTALLED = 'Комната успешно установлена.'
    ROOM_IS_NOT_INSTALLED = f'Сначала установите комнату с помощью {CommandName.SET_ROOM.with_slash}'
    WASH = 'Выберите день недели:'
    ALL_TIME_WINDOWS_ARE_TAKEN = 'Весь день занят.'
    WEEKDAY_TO_ORDER_SELECTED = 'Выберите время для записи:'
    MAX_RECORDS = 'У вас уже слишком много записей.'
    TIME_TO_ORDER_SELECTED = 'Вы успешно записались.'
    NO_ORDERS = 'У вас пока нет записей.'
    CANCEL_WASH = 'Выберите запись, которую нужно убрать:'
    TIME_TO_CANCEL_SELECTED = 'Запись успешно снята.'
