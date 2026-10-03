from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class WordProgress(Base):
    __tablename__ = "word_progress"

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

    learned: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
    )

    correct_answers: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    wrong_answers: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    next_review: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    streak: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    learning_stage: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=1,
    )

    __table_args__ = (
        UniqueConstraint(
            "telegram_id",
            "word_id",
            name="word_progress_telegram_id_word_id_key",
        ),
    )