from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .utils import utcnow

if TYPE_CHECKING:
    from .product_type import ProductTypeORM


class ProductORM(Base):
    __tablename__ = "product"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    product_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("product_type.id"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )

    product_type: Mapped[list["ProductTypeORM"]] = relationship(
        back_populates="products"
    )
