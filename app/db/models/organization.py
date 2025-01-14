from __future__ import annotations

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from .base import TimestampMixin
from .base.declarative import Base

class Organization(Base, TimestampMixin):
    __tablename__ = "organization"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(300))
    organization_building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    organization_building = relationship('Building')
    organization_activities: Mapped[str] = mapped_column(String(300))
    
    @staticmethod
    async def add_organization(session: AsyncSession, organization_name: str, organization_telephone: str, organization_building: str,
                       organization_activities: str,): # fix me
        organization = Organization(organization_name=organization_name, page_description=organization_telephone, page_path=organization_building,
                     page_content=organization_activities,)
        session.add(organization)
        await session.commit()
        return organization
    
    @staticmethod
    async def get_organization_by_name(session: AsyncSession, organization_name: str): # fix me
        organization_db = await Organization.get_or_none(session, organization_name=organization_name)
        return organization_db
    