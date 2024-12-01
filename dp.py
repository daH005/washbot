from aiogram import Dispatcher
from aiogram.filters import (
    CommandStart,
    Command,
)
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from config import ROOM_RANGE, MAX_RECORDS
from db import (
    User,
    WeekDay,
    TimeWindow,
)
from callbacks import (
    WeekDayToOrderSelectedCallbackData,
    TimeToOrderSelectedCallbackData,
    TimeToCancelSelectedCallbackData,
)
from commands import CommandName, COMMANDS
from answers import Answer
from decorators import (
    register_user,
    check_room_having,
)
from states import SetRoomStateGroup

__all__ = (
    'dp',
)

dp = Dispatcher()


@dp.message(CommandStart())
@register_user
async def command_start_handler(message: Message) -> None:
    await message.bot.set_my_commands(COMMANDS)
    await message.answer(Answer.START)


@dp.message(Command(CommandName.SET_ROOM))
@register_user
async def set_room(message: Message,
                   state: FSMContext,
                   ) -> None:
    await message.answer(Answer.SET_ROOM)
    await state.set_state(SetRoomStateGroup.value)


@dp.message(SetRoomStateGroup.value)
@register_user
async def room_is_installed(message: Message,
                            state: FSMContext,
                            ) -> None:
    try:
        room = int(message.text)
        if room < ROOM_RANGE[0] or room > ROOM_RANGE[1]:
            raise ValueError
    except (TypeError, ValueError, IndexError):
        await message.answer(Answer.SET_ROOM)
        return

    User.by_id(message.from_user.id).room = room
    User.get_session().commit()

    await message.answer(Answer.ROOM_IS_INSTALLED)
    await state.clear()


@dp.message(Command(CommandName.WASH))
@register_user
@check_room_having
async def wash(message: Message) -> None:
    keyboard = InlineKeyboardBuilder()
    for weekday in WeekDay.all_sorted():
        keyboard.row(InlineKeyboardButton(
            text=weekday.text,
            callback_data=WeekDayToOrderSelectedCallbackData(weekday_id=weekday.id).pack(),
        ))

    await message.answer(Answer.WASH, reply_markup=keyboard.as_markup())


@dp.callback_query(WeekDayToOrderSelectedCallbackData.filter())
@register_user
@check_room_having
async def weekday_to_order_selected(callback: CallbackQuery,
                                    callback_data: WeekDayToOrderSelectedCallbackData,
                                    ) -> None:
    time_windows: list[TimeWindow] = WeekDay.by_id(callback_data.weekday_id).time_windows

    keyboard = InlineKeyboardBuilder()
    for time_window in time_windows:
        if time_window.taken:
            continue

        keyboard.row(InlineKeyboardButton(
            text=time_window.text,
            callback_data=TimeToOrderSelectedCallbackData(time_window_id=time_window.id).pack(),
        ))

    await callback.answer()

    if not list(keyboard.buttons):
        await callback.message.answer(Answer.ALL_TIME_WINDOWS_ARE_TAKEN)
        return

    await callback.message.answer(Answer.WEEKDAY_TO_ORDER_SELECTED, reply_markup=keyboard.as_markup())


@dp.callback_query(TimeToOrderSelectedCallbackData.filter())
@register_user
@check_room_having
async def time_to_order_selected(callback: CallbackQuery,
                                 callback_data: TimeToOrderSelectedCallbackData,
                                 ) -> None:
    user: User = User.by_id(callback.from_user.id)
    if user.records_count >= MAX_RECORDS:
        await callback.message.answer(Answer.MAX_RECORDS)
        await callback.answer()
        return

    time_window: TimeWindow = TimeWindow.by_id(callback_data.time_window_id)

    time_window.user_id = user.id
    TimeWindow.get_session().commit()

    await callback.message.answer(Answer.TIME_TO_ORDER_SELECTED)
    await callback.answer()


@dp.message(Command(CommandName.CANCEL_WASH))
@register_user
@check_room_having
async def cancel_wash(message: Message) -> None:
    keyboard = InlineKeyboardBuilder()

    time_windows: list[TimeWindow] = User.by_id(message.from_user.id).time_windows
    if not list(time_windows):
        await message.answer(Answer.NO_ORDERS)
        return

    for time_window in time_windows:
        keyboard.row(InlineKeyboardButton(
            text=time_window.text,
            callback_data=TimeToCancelSelectedCallbackData(time_window_id=time_window.id).pack(),
        ))

    await message.answer(Answer.CANCEL_WASH, reply_markup=keyboard.as_markup())


@dp.callback_query(TimeToCancelSelectedCallbackData.filter())
@register_user
@check_room_having
async def time_to_cancel_selected(callback: CallbackQuery,
                                  callback_data: TimeToCancelSelectedCallbackData,
                                  ) -> None:
    time_window: TimeWindow = TimeWindow.by_id(callback_data.time_window_id)
    if time_window.user_id == callback.from_user.id:
        time_window.user_id = None
        TimeWindow.get_session().commit()

        await callback.message.answer(Answer.TIME_TO_CANCEL_SELECTED)

    await callback.answer()
