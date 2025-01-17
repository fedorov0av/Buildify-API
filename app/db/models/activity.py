from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

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
    
    
    @staticmethod
    async def get_activity_by_name(session: AsyncSession, name: str):
        query = select(Activity).where(Activity.name==name)
        result = await session.scalars(query)
        try:
            activity_db = result.one()    
        except NoResultFound:
            return None
        return activity_db
    
    @staticmethod
    async def get_childs_activities_by_id(session: AsyncSession, id: int):
        query = select(Activity).where(Activity.parent_id==id)
        result = await session.scalars(query)
        try:
            childs_activity_db = result.all()    
        except NoResultFound:
            return None
        return childs_activity_db