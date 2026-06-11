import pytest
from uuid import uuid4
from httpx import AsyncClient
from src.core.config import settings
from src.models.product import Product, ProductStatus
from src.models.sku import SKU
from src.core.database import AsyncSessionLocal


async def create_test_product():
    async with AsyncSessionLocal() as session:
        product = Product(
            id=uuid4(),
            seller_id=uuid4(),
            category_id=uuid4(),
            title="Security Test Product",
            slug="security-test",
            description="Test",
            status=ProductStatus.MODERATED,
            deleted=False,
        )
        session.add(product)
        await session.flush()

        sku = SKU(
            product_id=product.id,
            name="Test SKU",
            price=1000000,
            discount=0,
            cost_price=500000,
            active_quantity=10,
            reserved_quantity=5,
            image="/s3/test.jpg",
        )
        session.add(sku)
        await session.commit()
        return product.id


@pytest.mark.asyncio
async def test_access_without_service_key_returns_403(client: AsyncClient):
    product_id = await create_test_product()
    response = await client.get(f"/api/v1/public/products/{product_id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_service_key_returns_403(client: AsyncClient):
    product_id = await create_test_product()
    response = await client.get(
        f"/api/v1/public/products/{product_id}",
        headers={"X-Service-Key": "wrong-key-123"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_deleted_product_returns_404(client: AsyncClient):
    async with AsyncSessionLocal() as session:
        product = Product(
            id=uuid4(),
            seller_id=uuid4(),
            category_id=uuid4(),
            title="Deleted Product",
            slug="deleted",
            status=ProductStatus.MODERATED,
            deleted=True,
        )
        session.add(product)
        await session.commit()
        product_id = product.id

    response = await client.get(
        f"/api/v1/public/products/{product_id}",
        headers={"X-Service-Key": settings.service_key},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_nonexistent_product_returns_404(client: AsyncClient):
    fake_id = uuid4()
    response = await client.get(
        f"/api/v1/public/products/{fake_id}",
        headers={"X-Service-Key": settings.service_key},
    )
    assert response.status_code == 404