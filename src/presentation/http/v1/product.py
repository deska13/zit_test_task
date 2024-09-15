from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status

from infra.dto import Page, Product, ProductIn
from presentation.http.v1.queries import ProductFilters
from repository.exception import NotFoundError
from services import ProductService

from .exception import HTTPErrorModel

router = APIRouter()


@router.post(
    path="",
    summary="Создание продукции",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPErrorModel},
    },
)
@inject
async def create_product(
    product_in: ProductIn,
    product_service: FromDishka[ProductService],
) -> Product:
    """
    Создание продукции

    Args:
        product_in (ProductIn): данные продукции

    Returns:
        Product: созданная продукция

    Raises:
        HTTPException: если не удалось создать продукцию
            с кодом 404, если не найден тип продукции
    """
    try:
        return await product_service.add(product_in=product_in)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    path="/{product_id}",
    summary="Получить продукцию по id",
)
@inject
async def get_product_by_id(
    product_id: UUID,
    product_service: FromDishka[ProductService],
) -> Product:
    """
    Получение продукции по id

    Args:
        product_id (UUID): id продукции

    Returns:
        Product: продукция

    Raises:
        HTTPException: если не удалось найти продукцию
            с кодом 404, если не найден тип продукции
    """
    try:
        return await product_service.get_by_id(product_id=product_id)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    path="",
    summary="Получить продукцию",
)
@inject
async def get_products(
    count: Annotated[int, Query(gt=0, le=5000)],
    page: Annotated[int, Query(gt=0, le=500)],
    filters: ProductFilters = Depends(),
    product_service: FromDishka[ProductService] = Depends(),
) -> Page[Product]:
    """
    Получение списка продукции с помощью фильтров

    Args:
        count (int): количество объектов на странице
        page (int): номер страницы
        filters (ProductFilters): фильтры

    Returns:
        Page[Product]: страница с продукцией
    """
    products = await product_service.get_products(
        count=count,
        page=page,
        **filters.model_dump(),
    )
    return products
