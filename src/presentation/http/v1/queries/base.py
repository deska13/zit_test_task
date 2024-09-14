from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from infra.dto.model import Datetime


class BaseFilters(BaseModel):
    from_created_at: Datetime | SkipJsonSchema[None] = Field(
        Query(
            default=None,
            description="Filter objects created from this Datetime",
        )
    )
    to_created_at: Datetime | SkipJsonSchema[None] = Field(
        Query(
            default=None,
            description="Filter objects created after this Datetime",
        )
    )
    from_updated_at: Datetime | SkipJsonSchema[None] = Field(
        Query(
            default=None,
            description="Filter objects updated after this Datetime",
        )
    )
    to_updated_at: Datetime | SkipJsonSchema[None] = Field(
        Query(
            default=None,
            description="Filter objects updated before this Datetime",
        )
    )
