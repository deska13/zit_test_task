from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status

from infra.dto import Page, ProductType, ProductTypeIn
from presentation.http.v1.queries import ProductTypeFilters
from repository.exception import AlredyExistError
from services import ProductTypeService

from .exception import HTTPErrorModel

router = APIRouter()


@router.post(
    path="",
    summary="Создать тип продукции",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": HTTPErrorModel},
    },
)
@inject
async def create(
    product_type_in: ProductTypeIn,
    product_type_service: FromDishka[ProductTypeService],
) -> ProductType:
    """
    Создание типа продукции

    Args:
        product_type_in (ProductTypeIn): данные создаваемого типа продукции

    Returns:
        ProductType: созданный тип продукции

    Raises:
        HTTPException: если не удалось создать тип продукции
            с кодом 409, если тип продукции уже существует
    """
    try:
        return await product_type_service.add(product_type_in)
    except AlredyExistError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    path="",
    summary="Получить список типов продукции",
)
@inject
async def get_product_types(
    count: Annotated[int, Query(gt=0, le=5000)],
    page: Annotated[int, Query(gt=0, le=500)],
    filters: ProductTypeFilters = Depends(),
    product_type_service: FromDishka[ProductTypeService] = Depends(),
) -> Page[ProductType]:
    """
    Получение списка типов продукции

    Args:
        count (int): количество типов продукции на странице
        page (int): номер страницы
        filters (ProductTypeFilters): фильтры

    Returns:
        Page[ProductType]: страница с типами продукции
    """
    return await product_type_service.get_by_filter(
        count=count,
        page=page,
        **filters.model_dump(),
    )
