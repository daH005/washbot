from aiogram.fsm.state import StatesGroup, State

__all__ = (
    'SetRoomStateGroup',
)


class SetRoomStateGroup(StatesGroup):
    value = State()
