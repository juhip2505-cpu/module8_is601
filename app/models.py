from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    calculations: Mapped[list["Calculation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    a: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    b: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    result: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="calculations",
    )