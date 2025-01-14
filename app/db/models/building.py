from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

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
