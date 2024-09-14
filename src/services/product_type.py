from typing import Any

from infra.dto import Page, ProductType, ProductTypeIn
from repository import SQLAlchemyUnitOfWork


class ProductTypeService:
    def __init__(self, repository_uow: SQLAlchemyUnitOfWork):
        self.repository_uow = repository_uow

    async def add(self, product_type: ProductTypeIn) -> ProductType:
        async with self.repository_uow as repository_uow:
            return await repository_uow.product_type.add(product_type)

    async def get_by_filter(self, **kwargs: Any) -> Page[ProductType]:
        async with self.repository_uow as repository_uow:
            return await repository_uow.product_type.get_by_filter(**kwargs)
