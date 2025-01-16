from __future__ import annotations
from typing import List
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from .base import TimestampMixin
from .base.declarative import Base
from app.db.models.assoc_table import organization_activity
from app.db.models.activity import Activity
from app.db.models.building import Building

class Organization(Base, TimestampMixin):
    __tablename__ = "organization"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(300))
    organization_building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    organization_building: Mapped['Building'] = relationship(foreign_keys=[organization_building_id])
    organization_activities: Mapped[List[Activity]] = relationship(secondary=organization_activity)
    
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
    
    @staticmethod
    async def get_organization_by_id(session: AsyncSession, organization_id: str): # fix me
        query = select(Organization).where(Organization.id == organization_id)\
                    .options(selectinload(Organization.organization_building))\
                    .options(selectinload(Organization.organization_activities))
        result = await session.scalars(query)
        try:
            organization_db = result.one()    
        except NoResultFound:
            return None
        return organization_db
    