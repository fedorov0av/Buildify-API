from __future__ import annotations
from typing import List
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.schemes.geo import GeoSquare
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
    async def get_organization_by_name(session: AsyncSession, name: str):
        query = select(Organization).where(Organization.organization_name==name)\
                    .options(selectinload(Organization.organization_building))\
                    .options(selectinload(Organization.organization_activities))
        result = await session.scalars(query)
        try:
            organization_db = result.one()    
        except NoResultFound:
            return None
        return organization_db
    
    @staticmethod
    async def get_organization_by_id(session: AsyncSession, id: str):
        query = select(Organization).where(Organization.id==id)\
                    .options(selectinload(Organization.organization_building))\
                    .options(selectinload(Organization.organization_activities))
        result = await session.scalars(query)
        try:
            organization_db = result.one()    
        except NoResultFound:
            return None
        return organization_db
    
    @staticmethod
    async def get_organization_by_building_id(session: AsyncSession, building_id: str):
        query = select(Organization).where(Organization.organization_building_id==building_id)\
                    .options(selectinload(Organization.organization_building))\
                    .options(selectinload(Organization.organization_activities))
        result = await session.scalars(query)
        try:
            organization_db = result.one()    
        except NoResultFound:
            return None
        return organization_db
    
    @staticmethod
    async def get_organizations_by_activity_id(session: AsyncSession, activity_id: str):
        query = select(Organization).where(Organization.organization_activities.any(Activity.id == activity_id),)\
                    .options(selectinload(Organization.organization_building))\
                    .options(selectinload(Organization.organization_activities))
        result = await session.scalars(query)
        try:
            organization_db = result.all()    
        except NoResultFound:
            return None
        return organization_db