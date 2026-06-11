import pytest
from uuid import uuid4
from httpx import AsyncClient
from src.models.product import Product, ProductStatus
from src.models.sku import SKU
from src.core.database import AsyncSessionLocal
from src.core.config import settings


async def create_test_product():
    async with AsyncSessionLocal() as session:
        product = Product(
            id=uuid4(),
            seller_id=uuid4(),
            category_id=uuid4(),
            title="iPhone 15 Pro Max",
            slug="iphone-15-pro-max",
            description="Флагманский смартфон",
            status=ProductStatus.MODERATED,
            deleted=False,
        )
        session.add(product)
        await session.flush()

        sku1 = SKU(
            product_id=product.id,
            name="256GB Black",
            price=12999000,
            discount=0,
            cost_price=9000000,
            active_quantity=10,
            reserved_quantity=5,
            image="/s3/black.jpg",
            characteristics=[{"name": "Цвет", "value": "Чёрный"}],
        )
        sku2 = SKU(
            product_id=product.id,
            name="256GB White",
            price=12999000,
            discount=500000,
            cost_price=9000000,
            active_quantity=3,
            reserved_quantity=1,
            image="/s3/white.jpg",
            characteristics=[{"name": "Цвет", "value": "Белый"}],
        )
        session.add_all([sku1, sku2])
        await session.commit()
        return product.id


async def create_blocked_product():
    async with AsyncSessionLocal() as session:
        product = Product(
            id=uuid4(),
            seller_id=uuid4(),
            category_id=uuid4(),
            title="Blocked Product",
            slug="blocked",
            status=ProductStatus.BLOCKED,
            deleted=False,
        )
        session.add(product)
        await session.commit()
        return product.id


@pytest.mark.asyncio
async def test_product_card_returns_full_data_with_skus(client: AsyncClient):
    product_id = await create_test_product()

    response = await client.get(
        f"/api/v1/public/products/{product_id}",
        headers={"X-Service-Key": settings.service_key},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == str(product_id)
    assert data["title"] == "iPhone 15 Pro Max"
    assert "skus" in data
    assert len(data["skus"]) == 2

    for sku in data["skus"]:
        assert "price" in sku
        assert "discount" in sku
        assert "active_quantity" in sku


@pytest.mark.asyncio
async def test_cost_price_absent_in_response(client: AsyncClient):
    product_id = await create_test_product()

    response = await client.get(
        f"/api/v1/public/products/{product_id}",
        headers={"X-Service-Key": settings.service_key},
    )

    data = response.json()
    for sku in data["skus"]:
        assert "cost_price" not in sku
        assert "reserved_quantity" not in sku


@pytest.mark.asyncio
async def test_blocked_product_returns_404(client: AsyncClient):
    product_id = await create_blocked_product()

    response = await client.get(
        f"/api/v1/public/products/{product_id}",
        headers={"X-Service-Key": settings.service_key},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sku_without_stock_is_shown_as_unavailable(client: AsyncClient):
    async with AsyncSessionLocal() as session:
        product = Product(
            id=uuid4(),
            seller_id=uuid4(),
            category_id=uuid4(),
            title="Out of Stock Product",
            slug="out-of-stock",
            status=ProductStatus.MODERATED,
            deleted=False,
        )
        session.add(product)
        await session.flush()

        sku = SKU(
            product_id=product.id,
            name="Out of Stock SKU",
            price=1000000,
            discount=0,
            cost_price=500000,
            active_quantity=0,
            reserved_quantity=0,
            image="/s3/out.jpg",
        )
        session.add(sku)
        await session.commit()
        product_id = product.id

    response = await client.get(
        f"/api/v1/public/products/{product_id}",
        headers={"X-Service-Key": settings.service_key},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["skus"]) == 1
    assert data["skus"][0]["active_quantity"] == 0