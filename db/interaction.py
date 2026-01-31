from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connection import AsyncSessionLocal
from sqlalchemy import insert, select, update, and_
from db.models import User, UserAgreementStatus, SubStatus, UserCourse, Order
from config import lg as lg


class DataBaseInteraction:

    # Функция для добавления нового пользователя
    @staticmethod
    async def add_user(db: AsyncSession, user_telegram_id: int, user_name: str) -> None:
        # Формирование запроса на вставку данных
        stmt = (
            insert(User)
            .values(
            user_telegram_id=user_telegram_id,
            user_name=user_name)
            .returning(User.user_id)
            )
        try:
            # Выполнение запроса в блоке try, для отлова ошибок
            await db.execute(stmt)
            await db.commit()
            # Добавление связей в таблицу "пользователь <-> курс"
            await DataBaseInteraction.combine_user_courses(db, user_telegram_id)
        except Exception as e:
            lg.error(e)

    # Добавление в таблицу многие ко многим(пользователь <-> курс) все курсы к пользователю
    @staticmethod
    async def combine_user_courses(db: AsyncSession, user_telegram_id: int) -> None:
        try:
            user_id = await DataBaseInteraction.get_user_id_by_tg(db, user_telegram_id)
            for i in range(1, 6):  # Цикл, чтобы добавить сразу несколько строк
                stmt = (
                    insert(UserCourse)
                    .values(
                        user_id=user_id,
                        course_id=i)
                    .returning(UserCourse.id)
                )
                await db.execute(stmt)

            await db.commit()
        except Exception as e:
            lg.error(e)

    # Обновление статуса в таблице "пользователь <-> курс"
    @staticmethod
    async def update_user_course_status(db: AsyncSession, user_telegram_id: int, course_id: int) -> None:
        try:
            user_id = await DataBaseInteraction.get_user_id_by_tg(db, user_telegram_id)
            stmt = (
                update(UserCourse)
                .where(
                    and_(
                        UserCourse.user_id == user_id,
                        UserCourse.course_id == course_id))
                .values(status_id=1))

            await db.execute(stmt)
            await db.commit()

        except Exception as e:
            lg.error(e)

    # Функция помощник, для получения user_id
    @staticmethod
    async def get_user_id_by_tg(db: AsyncSession, user_telegram_id: int) -> int | None:
        stmt_for_id = (
            select(User.user_id)
            .where(User.user_telegram_id == user_telegram_id)
        )
        try:
            user_id = await db.scalar(stmt_for_id)
            return user_id or None

        except Exception as e:
            lg.error(e)
            return None

    # Функция для проверки, существует ли такой пользователь
    @staticmethod
    async def check_user(db: AsyncSession, user_telegram_id: int) -> bool:
        user_name = await DataBaseInteraction.user_name_helper(user_telegram_id, db)
        if user_name:
            return False
        else:
            return True

        # Получить имя по tg id

    @staticmethod
    async def get_username_by_id(user_telegram_id: int, db: AsyncSession) -> str | bool:
        return await DataBaseInteraction.user_name_helper(user_telegram_id, db) or False

    @staticmethod
    async def user_name_helper(user_telegram_id: int, db: AsyncSession) -> str | bool:
        # Формирование запроса на выборку данных
        stmt = (
            select(User.user_name)
            .where(User.user_telegram_id == user_telegram_id)
        )
        try:
            # Получение данных из запроса
            user_name = await db.scalar(stmt)
            if user_name:
                return user_name
            else:
                return False
        except Exception as e:
            lg.error(e)
            return False

    # Функция для обновления имени пользователя
    @staticmethod
    async def update_user_name(db: AsyncSession, user_telegram_id: int, user_name: str) -> None:
        # Формирование запроса на обновление данных
        stmt = (
            update(User)
            .where(User.user_telegram_id == user_telegram_id)
            .values(user_name=user_name)
        )
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            lg.error(e)

    # Обновление статуса ознакомления с соглашением (Обновляет с False на True)
    @staticmethod
    async def switch_user_agreement(db: AsyncSession, user_telegram_id: int) -> None:
        # Формирование запроса
        stmt = (
            update(User)
            .where(User.user_telegram_id == user_telegram_id)
            .values(user_agreement_status_id=1)
        )
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            lg.error(e)

    # Проверка статуса ознакомления с соглашением
    @staticmethod
    async def check_user_agreement_status_id(db: AsyncSession, user_telegram_id: int) -> bool:
        # Формирование запроса
        stmt = (
            select(User.user_agreement_status_id)
            .where(User.user_telegram_id == user_telegram_id)
        )
        try:
            # Получение данных из запроса
            user_agreement_status_id = await db.scalar(stmt)
            if user_agreement_status_id == 1:
                return True
            else:
                return False

        except Exception as e:
            lg.error(e)
            return False

    @staticmethod
    async def get_user_sub_status(db: AsyncSession, user_telegram_id: int) -> str:
        stmt = (
            select(SubStatus.sub_status_name)
            .join(User, User.sub_status_id == SubStatus.sub_status_id)
            .where(User.user_telegram_id == user_telegram_id)
        )
        try:
            user_sub_status = await db.scalar(stmt)
            return user_sub_status
        except Exception as e:
            lg.error(e)

    @staticmethod
    async def get_user_sub_status_id_from_order(db: AsyncSession, order_id: str) -> int:
        stmt = (
            select(Order.sub_status_id)
            .where(Order.order_id == order_id)
        )
        try:
            user_sub_status_from_order = await db.scalar(stmt)
            return user_sub_status_from_order
        except Exception as e:
            lg.error(e)

    # Обновление статуса подписки пользователя
    @staticmethod
    async def update_user_sub_status(db: AsyncSession, user_telegram_id: int, new_sub_status_id: int) -> bool:
            try:
                stmt = (
                    update(User)
                    .where(User.user_telegram_id == user_telegram_id)
                    .values(sub_status_id=new_sub_status_id)
                )
                await db.execute(stmt)
                await db.commit()

                return True

            except Exception as e:
                lg.error(e)
                return False

    # Обновление последней активности пользователя
    @staticmethod
    async def update_last_active(db: AsyncSession, user_telegram_id: int) -> None:
            # Формирование запроса
            stmt = (
                update(User)
                .where(User.user_telegram_id == user_telegram_id)
                .values(last_active=datetime.now(timezone.utc))  # Получение текущей даты и времени
            )
            try:
                await db.execute(stmt)
                await db.commit()
            except Exception as e:
                lg.error(e)

    # Функция для проверки, открыт ли блок у пользователя
    @staticmethod
    async def check_block_access(db: AsyncSession, user_telegram_id: int, course_id: int) -> bool:
        try:
            # Получение user_id
            user_id = await DataBaseInteraction.get_user_id_by_tg(db, user_telegram_id)
            stmt = (
                select(UserCourse.status_id)
                .where(
                    and_(
                        UserCourse.user_id == user_id,
                        UserCourse.course_id == course_id,
                    )
                )
            )
            status_id = await db.scalar(stmt)
            if status_id == 1:  # 1 - доступ открыт

                return True
            else:
                return False  # 2 - доступ закрыт

        except Exception as e:
            lg.error(e)
            return False

    # Функция для создания нового заказа
    @staticmethod
    async def create_new_order(db: AsyncSession, order_id: str, user_id: int,sub_status_id: int, amount: int,
                               currency: str, order_status_id: int) -> None:

        stmt = (
            insert(Order)
            .values(
                order_id=order_id,  # UUID, который генерируется, когда срабатывает callback
                user_id=user_id,  # id пользователя в бд
                sub_status_id=sub_status_id,  # Какая подписка оформляется
                amount=amount,  # Сколько денег
                currency=currency,  # В какой валюте
                order_status_id=order_status_id,  # Статус заказа. По дефолту 0
            ))
        try:
            await db.execute(stmt)
            await db.commit()

        except Exception as e:
            lg.error(e)

    # Функция для получения order_id по user_id
    @staticmethod
    async def get_order_by_payment_id(db: AsyncSession, order_id: str) -> str | None:
        #
        stmt = (
            select(Order)
            .where(Order.order_id == order_id)
        )  # Запрос на получение order_id
        try:

            order_from_db = await db.scalar(stmt)
            return order_id or None

        except Exception as e:
            lg.error(e)
            return None
    # Смена статуса заказа
    @staticmethod
    async def update_order_status_id(db: AsyncSession, order_id: str, new_order_status_id: int) -> None:
        try:
            if new_order_status_id == 1:  # Если новый статус "оплачено", то добавляем также время оплаты
                stmt = (
                    update(Order)
                    .where(Order.order_id == order_id)
                    .values(order_status_id=new_order_status_id,
                            paid_at=datetime.now(timezone.utc))
                    )

                await db.execute(stmt)
                await db.commit()

            else:  # Иначе, если како-либо другой статус, то не добавляем время оплаты
                stmt = (
                    update(Order)
                    .where(Order.order_id == order_id)
                    .values(order_status_id=new_order_status_id)
                )
                await db.execute(stmt)
                await db.commit()

        except Exception as e:
                lg.error(e)

    @staticmethod
    async def update_provider_payment_id(db: AsyncSession, user_telegram_id: int, provider_payment_id: str) -> None:
        user_id = await DataBaseInteraction.get_user_id_by_tg(db, user_telegram_id)
        stmt = (
            update(Order)
            .where(Order.user_id == user_id)
            .values(provider_payment_id=provider_payment_id)
        )
        try:
            await db.execute(stmt)
            await db.commit()

        except Exception as e:
            lg.error(e)





