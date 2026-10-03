from sqlalchemy import Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Words(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    word: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    translation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    level: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default="1",
    )

    category: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    audio_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        Index(
            "idx_words_unique",
            "word",
            "translation",
            "language",
            unique=True,
        ),
    )