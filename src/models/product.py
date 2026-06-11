from sqlalchemy import String, Text, Boolean, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from datetime import datetime
import enum
from src.core.database import Base


class ProductStatus(str, enum.Enum):
    CREATED = "CREATED"
    ON_MODERATION = "ON_MODERATION"
    MODERATED = "MODERATED"
    BLOCKED = "BLOCKED"
    HARD_BLOCKED = "HARD_BLOCKED"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    seller_id: Mapped[UUID]
    category_id: Mapped[UUID]
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[ProductStatus] = mapped_column(SQLEnum(ProductStatus), default=ProductStatus.CREATED)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    skus = relationship("SKU", back_populates="product", cascade="all, delete-orphan")