from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum


# ORDER STATUS ENUM
class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# PRODUCT SCHEMA
class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=512, description='Name of the product')
    price: float = Field(..., gt=0, description='Price of the product')
    stock: int = Field(..., ge=0, description="Number of product items in stock")

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int = Field(..., description="Unique identifier of the product")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of the product')
    price: Optional[float] = Field(None, gt=0, description='Price of the product')
    stock: Optional[int] = Field(None, ge=0, description="Number of product items in stock")


# ORDER ITEM SCHEMA
class OrderItemBase(BaseModel):
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., gt=0, description="Quantity ordered")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    price_at_purchase: float

    class Config:
        from_attributes = True


# ORDER SCHEMA
class OrderBase(BaseModel):
    """ Base Fields shared across order schemas """
    customer_name: str = Field(..., min_length=1, max_length=255, description="Customer's full name")
    customer_email: EmailStr = Field(..., description="Customer's email address")
    customer_phone: Optional[str] = Field(None, max_length=20, description="Customer's phone number")
    customer_address: str = Field(..., min_length=5, max_length=512, description="Shipping address")

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Items in the order")

class Order(OrderBase):
    id: int = Field(..., description="Unique identifier of the order")
    order_date: datetime = Field(..., description="When the order was created")
    status: OrderStatus = Field(..., description="Current status of the order")
    total_amount: float = Field(..., ge=0, description="Total order amount in dollars")

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Customer's full name")
    customer_email: Optional[EmailStr] = Field(None, description="Customer's email address")
    customer_phone: Optional[str] = Field(None, max_length=20, description="Customer's phone number")
    customer_address: Optional[str] = Field(None, min_length=5, max_length=512, description="Shipping address")
    status: Optional[OrderStatus] = None

