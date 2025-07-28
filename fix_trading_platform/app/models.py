from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship   # ORM architecture # TODO: REUSE AND EXTEND. 27/07/25
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relationship
    trades = relationship("Trade", back_populates="user")
    reservations = relationship("CashReservation", back_populates="user", cascade="all, delete-orphan")

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    quantity = Column(Float)
    side = Column(String)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship
    user = relationship("User", back_populates="trades")

class CashReservation(Base):
    __tablename__ = "cash_reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    is_finalized = Column(Boolean, default=False)
    # Relationship
    user = relationship("User", back_populates="reservations")