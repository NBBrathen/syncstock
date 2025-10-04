from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

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

class OrderBase(BaseModel):
    """ Base Fields shared across order schemas """
    customer_name: str = Field(..., min_length=1, max_length=255, description="Customer's full name")
    customer_email: EmailStr = Field(..., description="Customer's email address")
    customer_phone: Optional[str] = Field(None, max_length=20, description="Customer's phone number")
    customer_address: str = Field(..., min_length=5, max_length=512, description="Shipping address")

class OrderCreate(OrderBase):
    pass

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
