from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.security import verify_service_key
from src.services.product_service import ProductService
from src.schemas.product import ProductPublicResponse

router = APIRouter()


@router.get(
    "/public/products/{product_id}",
    response_model=ProductPublicResponse,
    summary="B2C карточка товара",
)
async def get_public_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_service_key),
) -> ProductPublicResponse:
    """
    Получение карточки товара для B2C витрины.
    - НЕ возвращает cost_price и reserved_quantity
    - Заблокированные товары → 404
    - Удалённые товары → 404
    """
    service = ProductService(db)
    return await service.get_product_for_b2c(product_id)