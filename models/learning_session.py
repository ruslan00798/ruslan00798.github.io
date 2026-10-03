from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class LearningSession(Base):
    __tablename__ = "learning_session"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    level: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=text("now()"),
    )

    mode: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        server_default=text("'new'"),
    )