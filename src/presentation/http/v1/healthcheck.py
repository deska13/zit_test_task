from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/healthcheck",
    tags=["healthcheck"],
    summary="Проверка доступности API",
    status_code=status.HTTP_200_OK,
)
async def get_health() -> str:
    return "PONG"
