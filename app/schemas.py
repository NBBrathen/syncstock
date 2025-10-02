from typing import Optional
from pydantic import BaseModel, Field


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