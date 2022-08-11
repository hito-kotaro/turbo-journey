from datetime import datetime as dt
from sqlalchemy.schema import Column
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Boolean, Text
from db.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(100))
    hmt = Column(Float, nullable=False)
    created_at = Column("created_at", DateTime, default=dt.now(), nullable=False)
    updated_at = Column(
        "updated_at",
        DateTime,
        default=dt.now(),
        onupdate=dt.now(),
        nullable=False,
    )


class Bank(Base):
    __tablename__ = "banks"
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(100))
    hmt = Column(Float, nullable=False)
    gas = Column(Float, nullable=False)
    created_at = Column("created_at", DateTime, default=dt.now(), nullable=False)
    updated_at = Column(
        "updated_at",
        DateTime,
        default=dt.now(),
        onupdate=dt.now(),
        nullable=False,
    )


class Request(Base):
    __tablename__ = "requests"
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text(), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    order_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reward = Column(Float, nullable=False)
    public = Column(Boolean)
    status = Column(Boolean)
    is_bank = Column(Boolean)
    created_at = Column("created_at", DateTime, default=dt.now(), nullable=False)
    updated_at = Column(
        "updated_at",
        DateTime,
        default=dt.now(),
        onupdate=dt.now(),
        nullable=False,
    )


class Approve(Base):
    __tablename__ = "approves"
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column("created_at", DateTime, default=dt.now(), nullable=False)
    updated_at = Column(
        "updated_at",
        DateTime,
        default=dt.now(),
        onupdate=dt.now(),
        nullable=False,
    )
