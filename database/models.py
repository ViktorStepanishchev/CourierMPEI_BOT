from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)


class Courier(Base):
    __tablename__ = "courier"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=False)
    order_id = Column(BigInteger, nullable=True, default=None)
    phone_number = Column(String, nullable=True, default=None)

    customers = relationship("Customer", back_populates="courier")


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
    courier_id = Column(BigInteger, ForeignKey('courier.user_id'), default=None)
    in_edit = Column(Boolean, default=False)

    courier = relationship("Courier", back_populates="customers")

class MsgToAdministration(Base):
    __tablename__ = "msg_to_administration"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    msg_id = Column(BigInteger, nullable=False)
