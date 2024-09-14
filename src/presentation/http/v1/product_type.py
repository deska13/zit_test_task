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
    summary="Получить продукцию",
    description="Get all products",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": HTTPErrorModel},
    },
)
@inject
async def create(
    product_type: ProductTypeIn,
    product_type_service: FromDishka[ProductTypeService],
) -> ProductType:
    try:
        return await product_type_service.add(product_type)
    except AlredyExistError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    path="",
    summary="Получить продукцию",
    description="Get all products",
)
@inject
async def get_product_types(
    count: Annotated[int, Query(gt=0, le=5000)],
    page: Annotated[int, Query(gt=0, le=500)],
    filters: ProductTypeFilters = Depends(),
    product_type_service: FromDishka[ProductTypeService] = Depends(),
) -> Page[ProductType]:
    return await product_type_service.get_by_filter(
        count=count,
        page=page,
        **filters.model_dump(),
    )
