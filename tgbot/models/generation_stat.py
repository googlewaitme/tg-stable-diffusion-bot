from sqlalchemy.orm import Mapped

from tgbot.models.base import Base
from sqlalchemy import Float, String, Column, DateTime, ForeignKey
from sqlalchemy import Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship


class Generation(Base):
    __tablename__ = 'generation'

    id: Mapped[int] = mapped_column(primary_key=True)
    prompt_text: Mapped[str] = mapped_column(String(2000))
    generation_time = Column(Float())
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship('User', back_populates='generations')
