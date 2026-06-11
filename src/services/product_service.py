from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.product_repository import ProductRepository
from src.schemas.product import ProductPublicResponse


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def get_product_for_b2c(self, product_id: UUID) -> ProductPublicResponse:
        """Получает товар для B2C — БЕЗ cost_price и reserved_quantity"""
        product = await self.repo.get_active_product_with_skus(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Блокированный товар тоже 404 для B2C
        if product.status in ("BLOCKED", "HARD_BLOCKED") or product.deleted:
            raise HTTPException(status_code=404, detail="Product not available")

        return ProductPublicResponse.model_validate(product)