from datetime import datetime
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql.base import UUID

from db.db_connection import Base
from sqlalchemy import (Column, String,
                        Integer, ForeignKey,
                        TIMESTAMP, func, BigInteger, DateTime, BigInteger)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_telegram_id = Column(BigInteger, unique=True)

    user_email = Column(String(100))
    user_name = Column(String(30))

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_active = Column(TIMESTAMP(timezone=True))

    sub_status_id = Column(Integer, ForeignKey('sub_statuses.sub_status_id'))
    user_agreement_status_id = Column(Integer, ForeignKey('user_agreement_statuses.user_agreement_status_id'))

class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(30), unique=True)

    file_path = Column(String(60))

class UserCourse(Base):
    __tablename__ = 'user_courses'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.user_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    status_id = Column(Integer, ForeignKey('statuses.status_id'))

class SubStatus(Base):
    __tablename__ = 'sub_statuses'
    sub_status_id = Column(Integer, primary_key=True)
    sub_status_name = Column(String(20), nullable=False)

class Status(Base):
    __tablename__ = 'statuses'
    status_id = Column(Integer, primary_key=True)
    status_name = Column(String(20), nullable=False)

class UserAgreementStatus(Base):
    __tablename__ = 'user_agreement_statuses'
    user_agreement_status_id = Column(Integer, primary_key=True)
    user_agreement_status_ds = Column(String(250), nullable=False)

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String(100), primary_key=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    sub_status_id = Column(Integer, ForeignKey("sub_statuses.sub_status_id"), nullable=False)

    amount = Column(BigInteger, nullable=False)
    currency = Column(String(10), nullable=False)

    order_status_id = Column(Integer, ForeignKey("orders_statuses.order_status_id"), nullable=False, default=0)

    provider_payment_id = Column(String(100))

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    paid_at = Column(TIMESTAMP(timezone=True))

class OrderStatus(Base):
    __tablename__ = 'order_statuses'
    order_status_id = Column(Integer, primary_key=True)
    order_status_name = Column(String(20), nullable=False)