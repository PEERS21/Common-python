from typing import List, Optional

from sqlalchemy import BigInteger, JSON, Boolean, Index
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
import logging
from datetime import datetime, timedelta, UTC

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)

    img_filename: Mapped[str] = mapped_column(String(512), nullable=True)
    img_width: Mapped[int] = mapped_column(Integer, nullable=True)
    img_height: Mapped[int] = mapped_column(Integer, nullable=True)

    client_img_filename: Mapped[str] = mapped_column(String(512), nullable=True)
    client_img_width: Mapped[int] = mapped_column(Integer, nullable=True)
    client_img_height: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    categories: Mapped[list[int]] = mapped_column(MutableList.as_mutable(JSON), default=list)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "title": self.title,
            "content": self.content,
            "img_filename": self.img_filename,
            "img_width": self.img_width,
            "img_height": self.img_height,
            "client_img_filename": self.client_img_filename,
            "client_img_width": self.client_img_width,
            "client_img_height": self.client_img_height,
            "categories": self.categories,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "available": self.available,
        }

class Disk(Base):
    __tablename__ = "disks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    disk_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))

    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="disk")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disk_id: Mapped[int] = mapped_column(Integer, ForeignKey("disks.id", ondelete="CASCADE"), nullable=False)
    user_login: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    pickup_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    return_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))

    disk: Mapped[List["Disk"]] = relationship("Disk", back_populates="bookings")

    __table_args__ = (
        Index("idx_disk_time_overlap", "disk_id", "start_time", "end_time"),
    )

class IssuedToken(Base):
    __tablename__ = 'issued_tokens'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_login: Mapped[str] = mapped_column(String(128), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    issued_at = mapped_column(BigInteger, nullable=False)
    expires_at = mapped_column(BigInteger, nullable=False)

class State(Base):
    __tablename__ = 'states'
    state: Mapped[str] = mapped_column(String(128), primary_key=True)
    next: Mapped[str] = mapped_column(String(2048), nullable=True)
    created_at = mapped_column(BigInteger, nullable=False)
    expires_at = mapped_column(BigInteger, nullable=False)

class Blacklist(Base):
    __tablename__ = "blacklist"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    reason: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())