from datetime import datetime as dt
from sqlalchemy.schema import Column
from sqlalchemy import DateTime, Float, Integer, String
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
    hmt = Column(Float, nullable=False)
    created_at = Column("created_at", DateTime, default=dt.now(), nullable=False)
    updated_at = Column(
        "updated_at",
        DateTime,
        default=dt.now(),
        onupdate=dt.now(),
        nullable=False,
    )
