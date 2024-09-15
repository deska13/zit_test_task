import logging
import math
from typing import Any
from uuid import UUID

from sqlalchemy import Result, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infra.dto import Page, ProductType, ProductTypeIn

from .exception import NotFoundError
from .exception.alredy_exist import AlredyExistError, check_already_exists
from .orm import ProductTypeORM
from .utils import build_filters

logger = logging.getLogger(__name__)


class ProductTypeRepositry:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, product_type_in: ProductTypeIn) -> ProductType:
        product_type = ProductTypeORM(**product_type_in.model_dump())
        try:
            async with self.session.begin():
                self.session.add(product_type)
        except IntegrityError as exc:
            if check_already_exists(exc):
                raise AlredyExistError("Product type already exists") from exc
            logger.exception("Failed to add product type %s", product_type_in)
        await self.session.refresh(product_type)
        return ProductType.model_validate(product_type)

    async def get_by_id(self, product_type_id: UUID) -> ProductType:
        query_result = await self.session.execute(
            select(ProductTypeORM).where(ProductTypeORM.id == product_type_id)
        )
        product_type = query_result.scalar()
        if product_type is None:
            logging.error("Product type %s not found", product_type_id)
            raise NotFoundError("Product type not found")
        return ProductType.model_validate(product_type)

    async def get_by_filter(
        self,
        *,
        count: int,
        page: int,
        **kwargs: Any,
    ) -> Page[ProductType]:
        query = select(ProductTypeORM)
        for query_filter in build_filters(ProductTypeORM, **kwargs):
            query = query.filter(query_filter)
        query = query.limit(count)
        query = query.offset(count * (page - 1))
        query_result = await self.session.execute(query)
        product_types = query_result.scalars().all()
        total = await self.get_count(**kwargs)
        return Page[ProductType](
            result=[
                ProductType.model_validate(product_type)
                for product_type in product_types
            ],
            total=total,
            total_page=math.ceil(total / count),
        )

    async def get_count(self, **kwargs: Any) -> int:
        query = select(func.count()).select_from(ProductTypeORM)
        for query_filter in build_filters(ProductTypeORM, **kwargs):
            query = query.filter(query_filter)
        query_result: Result[tuple[int]] = await self.session.execute(query)
        return query_result.scalar() or 0
