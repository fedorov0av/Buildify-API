from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from ..base import TimestampMixin
from ..base.declarative import Base


class Organization(Base, TimestampMixin):
    __tablename__ = "organization"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(300))
    organization_telephone: Mapped[str] = mapped_column(String(300))
    organization_building: Mapped[str] = mapped_column(String(300))
    organization_activities: Mapped[str] = mapped_column(String(6096), nullable=True)
    
    @staticmethod
    async def add_page(session: AsyncSession, page_title: str, page_description: str, page_path: str,
                       page_content: str, page_url: str,):
        page = Organization(page_title=page_title, page_description=page_description, page_path=page_path,
                     page_content=page_content, page_url=page_url,)
        session.add(page)
        await session.commit()
        return page
    
    @staticmethod
    async def get_organization_by_url(session: AsyncSession, page_url: str):
        page_db = await Organization.get_or_none(session, page_url=page_url)
        return page_db
    