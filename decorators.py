from aiogram.types import Message, CallbackQuery
from functools import wraps

from db import User
from answers import Answer

__all__ = (
    'register_user',
    'check_room_having',
)


def register_user(func):
    @wraps(func)
    async def wrapper(message_or_query: Message | CallbackQuery, *args, **kwargs):
        user_id = message_or_query.from_user.id
        if not User.exists(user_id):
            new_user = User(id=user_id, name=message_or_query.from_user.first_name)
            User.get_session().add(new_user)
            User.get_session().commit()
        return await func(message_or_query, *args, **kwargs)
    return wrapper


def check_room_having(func):
    @wraps(func)
    async def wrapper(message_or_query: Message | CallbackQuery, *args, **kwargs):
        if not User.by_id(message_or_query.from_user.id).room:
            await message_or_query.answer(Answer.ROOM_IS_NOT_INSTALLED)
            return
        return await func(message_or_query, *args, **kwargs)
    return wrapper
