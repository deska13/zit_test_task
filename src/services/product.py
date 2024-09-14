from typing import Any
from uuid import UUID

from infra.dto import Page, Product, ProductIn
from repository import SQLAlchemyUnitOfWork


class ProductService:
    def __init__(self, repository_uow: SQLAlchemyUnitOfWork):
        self.repository_uow = repository_uow

    async def add(self, product_in: ProductIn) -> Product:
        async with self.repository_uow as repository_uow:
            await repository_uow.product_type.get_by_id(
                product_type_id=product_in.product_type_id,
            )
            created_product = await repository_uow.product.add(product_in)
            return created_product

    async def get_by_id(self, product_id: UUID) -> Product:
        async with self.repository_uow as repository_uow:
            return await repository_uow.product.get_by_id(product_id=product_id)

    async def get_products(self, **kwargs: Any) -> Page[Product]:
        async with self.repository_uow as repository_uow:
            return await repository_uow.product.get_by_filter(**kwargs)
