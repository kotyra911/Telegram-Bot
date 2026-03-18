import asyncio
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher

import config
from app.handler import router as bot_router
from middlewares.db_middleware import DBSessionMiddleware


"""async def start_fastapi():
    server = uvicorn.Server(
        uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
        )
    )
    await server.serve()


async def start_bot():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    dp.include_router(bot_router)
    dp.update.middleware(DBSessionMiddleware())

    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(
        start_fastapi(),
        start_bot(),
    )"""

async def start_bot():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    dp.include_router(bot_router)
    dp.update.middleware(DBSessionMiddleware())

    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)


async def main():
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())