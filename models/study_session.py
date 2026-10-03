from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class StudySession(Base):
    __tablename__ = "study_session"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    total_answers: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
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