from datetime import date
from sqlalchemy import BigInteger, Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class User(Base):
    __tablename__ = "users"


    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        default="en",
    )

    xp: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    streak: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    last_activity: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    voice_enabled: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
    )