from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)


class Courier(Base):
    __tablename__ = "courier"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    order_id = Column(Integer)

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    order_id = Column(Integer)
    order_text = Column(String)
    order_photo = Column(String)
    order_phone_number = Column(String)
    in_execution = Column(Boolean, default=False)

class MsgToAdministration(Base):
    __tablename__ = "msg_to_administration"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    msg_id = Column(BigInteger, nullable=False)
