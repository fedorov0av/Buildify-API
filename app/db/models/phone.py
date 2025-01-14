from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref
from .base.declarative import Base
from .base import TimestampMixin

class Phone(Base, TimestampMixin):
    __tablename__ = 'phone'

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str] = mapped_column(String(300))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization = relationship('Organization', backref=backref('phone', lazy='dynamic'))

    def __repr__(self):
        return f"<Phone(id={self.id}, number={self.number})>"