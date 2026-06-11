from sqlalchemy import String, Integer, BigInteger, Boolean, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from datetime import datetime
from src.core.database import Base


class SKU(Base):
    __tablename__ = "skus"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(BigInteger)
    discount: Mapped[int] = mapped_column(BigInteger, default=0)
    cost_price: Mapped[int] = mapped_column(BigInteger)
    active_quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    characteristics: Mapped[dict] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="skus")