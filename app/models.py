from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime, timezone

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(512), nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20))
    customer_address = Column(String(512), nullable=False)
    order_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = Column(String(100), nullable=False, default="pending")
    total_amount = Column(Float, nullable=False, default=0.0)