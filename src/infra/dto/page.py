from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class Page(BaseModel, Generic[DataT]):
    result: list[DataT]

    total: int
    total_page: int
