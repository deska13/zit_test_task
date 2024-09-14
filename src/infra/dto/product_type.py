from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .model import PrintableStr
from .page import Page


class ProductType(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ProductTypeIn(BaseModel):
    name: PrintableStr


class PageProductType(Page[ProductType]):
    pass
