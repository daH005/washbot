from enum import StrEnum

from aiogram.types import BotCommand

__all__ = (
    'CommandName',
    'COMMANDS',
)


class CommandName(StrEnum):

    SET_ROOM = 'set_room'
    WASH = 'wash'
    CANCEL_WASH = 'cancel_wash'

    @property
    def with_slash(self) -> str:
        return '/' + str(self)


COMMANDS = [
    BotCommand(
        command=CommandName.SET_ROOM.with_slash,
        description='Установить комнату',
    ),
    BotCommand(
        command=CommandName.WASH.with_slash,
        description='Записаться',
    ),
    BotCommand(
        command=CommandName.CANCEL_WASH.with_slash,
        description='Отменить запись',
    ),
]