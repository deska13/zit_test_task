import logging
import math
from typing import Any
from uuid import UUID

from sqlalchemy import Result, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infra.dto import Page, Product, ProductIn

from .exception import NotFoundError
from .exception.alredy_exist import AlredyExistError, check_already_exists
from .orm import ProductORM
from .utils import build_filters

logger = logging.getLogger(__name__)


class ProductRepositry:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product_in: ProductIn) -> Product:
        product = ProductORM(**product_in.model_dump())
        try:
            async with self.session.begin():
                self.session.add(product)
        except IntegrityError as exc:
            if check_already_exists(exc):
                raise AlredyExistError("Product already exists") from exc
            logger.exception("Failed to add product %s", product_in)
        await self.session.refresh(product)
        return Product.model_validate(product)

    async def get_by_id(self, product_id: UUID) -> Product:
        query_result = await self.session.execute(
            select(ProductORM).where(ProductORM.id == product_id)
        )
        product = query_result.scalar()
        if product is None:
            raise NotFoundError("Product not found")
        return Product.model_validate(product)

    async def get_by_filter(
        self,
        *,
        count: int,
        page: int,
        **kwargs: Any,
    ) -> Page[Product]:
        query = select(ProductORM)
        for query_filter in build_filters(ProductORM, **kwargs):
            query = query.filter(query_filter)
        query = query.limit(count)
        query = query.offset(count * (page - 1))
        query_result = await self.session.execute(query)
        products = query_result.scalars().all()
        total = await self.get_count(**kwargs)
        return Page[Product](
            result=[Product.model_validate(product) for product in products],
            total=total,
            total_page=math.ceil(total / count),
        )

    async def get_count(
        self,
        **kwargs: Any,
    ) -> int:
        query = select(func.count()).select_from(ProductORM)
        for query_filter in build_filters(ProductORM, **kwargs):
            query = query.filter(query_filter)
        query_result: Result[tuple[int]] = await self.session.execute(query)
        return query_result.scalar() or 0
