import asyncio
from aiogram import Bot

from dp import dp
from config import TOKEN
from change_date_task import start_change_date_task
from logs import start_logging


async def main() -> None:
    start_logging()
    start_change_date_task()
    await dp.start_polling(Bot(TOKEN))


if __name__ == "__main__":
    print('Бот успешно запущен.')
    asyncio.run(main())
