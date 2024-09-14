from fastapi import Query
from pydantic import Field

from .base import BaseFilters


class ProductTypeFilters(BaseFilters):
    name: str | None = Field(
        Query(
            default=None,
        )
    )
