from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .base.declarative import Base
from .base import TimestampMixin


class Building(Base, TimestampMixin):
    __tablename__ = 'building'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(300))  # Адрес здания
    latitude: Mapped[float]  # Широта
    longitude: Mapped[float]  # Долгота

    def __repr__(self):
        return f"<Building(id={self.id}, address={self.address}, latitude={self.latitude}, longitude={self.longitude})>"


    @staticmethod
    async def get_building_by_address(session: AsyncSession, address: str):
        query = select(Building).where(Building.address==address)
        result = await session.scalars(query)
        try:
            building_db = result.one()    
        except NoResultFound:
            return None
        return building_db