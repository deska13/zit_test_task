from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .model import PrintableStr
from .page import Page


class Product(BaseModel):
    id: UUID
    name: str
    product_type_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ProductIn(BaseModel):
    name: PrintableStr
    product_type_id: UUID


class PageProduct(Page[Product]):
    pass
