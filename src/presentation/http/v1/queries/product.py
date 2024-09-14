from uuid import UUID

from fastapi import Query
from pydantic import Field

from .base import BaseFilters


class ProductFilters(BaseFilters):
    name: str | None = Field(
        Query(
            default=None,
        )
    )
    product_type_id: UUID | None = Field(
        Query(
            default=None,
        )
    )
