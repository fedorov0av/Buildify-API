from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .mixin import BaseQuery


class Base(AsyncAttrs, DeclarativeBase, BaseQuery):
    id: Mapped[int] = mapped_column(primary_key=True)
    type_annotation_map = {
        str: String(255),
    }
    pass
