from .base.declarative import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class OrganizationActivity(Base):
    __tablename__ = 'organization_activities'

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"))