import asyncio
from aiogram import Bot, Dispatcher
import config
from app.handler import router
from middlewares.db_middleware import DBSessionMiddleware


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.update.middleware(DBSessionMiddleware())

    # Очистка очереди обновлений. Это нужно, чтобы бот не отвечал на сообщения, которые пришли пока он был оффлайн
    await bot.get_updates(offset=-1)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n!BOT STOP!\n')
