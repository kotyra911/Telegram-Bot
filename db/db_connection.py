from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import config as c

URL = c.SQLALCHEMY_DATA_BASE_URL

# Создания движка, который держит подключение к дб
engine = create_async_engine(URL,echo=True)
# Базовый класс, для того, чтобы алхимия отличала орм модели
Base = declarative_base()
# Фабрика сессий
AsyncSessionLocal = sessionmaker(bind=engine, class_=SQLAlchemyAsyncSession, expire_on_commit=False)

# Функция для получения новой сессии
#async def get_db() -> AsyncSession:

   # try:
    #    db = AsyncSession()
     #   yield db

  #  finally:
     #   db.close()