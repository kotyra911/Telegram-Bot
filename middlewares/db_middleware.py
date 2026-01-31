from aiogram import BaseMiddleware
from db.db_connection import AsyncSessionLocal

# Создание middleware для передачи db
class DBSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with AsyncSessionLocal() as db:
            data['db'] = db
            return await handler(event, data)

""" 
    Пользователь отправил сообщение
    ↓
    Aiogram получил событие
    ↓
    Aiogram запускает middleware:
    - создаём db
    - кладём её в data
    - вызываем handler
    - после — закрываем db
    ↓
    handler работает с db, просто принимая аргумент
    
    """
