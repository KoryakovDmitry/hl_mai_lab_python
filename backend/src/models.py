from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime,
    DECIMAL,
    TEXT,
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(256), unique=True, index=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email = Column(String(256))


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    description = Column(TEXT)
    cost = Column(DECIMAL(10, 2))


# Association table for the many-to-many relationship between Order and Service
order_service_table = Table(
    "order_service",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("service_id", ForeignKey("services.id"), primary_key=True),
)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime, default=datetime.utcnow)

    # Establishing the many-to-many relationship with Service
    services = relationship("Service", secondary=order_service_table, lazy="subquery")
