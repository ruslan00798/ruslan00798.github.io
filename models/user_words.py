from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class UserWords(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    word_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    known: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    unknown: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    next_review: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=text("now()"),
    )

    __table_args__ = (
        UniqueConstraint(
            "telegram_id",
            "word_id",
            name="user_words_telegram_id_word_id_key",
        ),
    )