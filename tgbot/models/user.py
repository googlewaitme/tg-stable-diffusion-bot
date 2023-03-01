from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, String, Integer

from tgbot.models.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer(), unique=True)
    name: Mapped[str] = mapped_column(String(100))

    generations = relationship(
        'Generation', back_populates='user', cascade='all, delete-orphan'
    )

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        array = [
            "User(id={self.id!r}",
            "name={self.name!r}",
            "time_created={self.time_created})",
            "time_updated={self.time_updated}<p></p>"
        ]
        return ", ".join(array)
