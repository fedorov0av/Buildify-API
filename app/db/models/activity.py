from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base.declarative import Base
from .base import TimestampMixin


class Activity(Base, TimestampMixin):
    __tablename__ = 'activity'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))
    parent_id: Mapped[int] = mapped_column(ForeignKey("activity.id"), nullable=True)
    
    # Связь с родительским элементом
    parent = relationship('Activity', remote_side=[id], backref='children')
    
    def __repr__(self):
        return f"<Activity(id={self.id}, name={self.name}, parent_id={self.parent_id})>"