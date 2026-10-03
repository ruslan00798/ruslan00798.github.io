from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class History(Base):
    __tablename__ = "history"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    original_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    translated_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    favorite: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
    )

    study_known: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    study_unknown: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    last_review: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    next_review: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    review_interval: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=1,
    )

