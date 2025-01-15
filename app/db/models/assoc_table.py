from .base.declarative import Base
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column

organization_activity = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id")),
    Column("activity_id", ForeignKey("activity.id")),
)


# class OrganizationActivity(Base):
#     __tablename__ = 'organization_activities'

#     organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
#     activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"))