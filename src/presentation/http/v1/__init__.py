from fastapi import APIRouter

from .product import router as product_router
from .product_type import router as product_type_router

router = APIRouter(prefix="/v1")
router.include_router(product_router, prefix="/products", tags=["products"])
router.include_router(
    product_type_router, prefix="/product_types", tags=["product_types"]
)
