from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.product import Product
from src.models.sku import SKU


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_product_with_skus(self, product_id: UUID) -> Product | None:
        """Получает товар с SKU (без фильтрации полей — сделает схема)"""
        query = (
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.skus))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()