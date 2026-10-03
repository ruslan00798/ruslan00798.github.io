from datetime import date

from sqlalchemy import BigInteger, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class DailyGoal(Base):
    __tablename__ = "daily_goal"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    goal_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    completed: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    target: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=10,
    )