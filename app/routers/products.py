from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
)



@router.get("", response_model=List[schemas.Product])
def get_products(limit: int = None, db: Session = Depends(get_db)):

    products = crud.get_products(db, limit=limit)
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404,detail="Product not Found")
    return product



@router.post('', response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    return crud.create_product(db, product=product)



@router.patch('/{product_id}', response_model=schemas.Product)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):

    updated_product = crud.update_product(db, product_id=product_id, product_update=product_update)
    if updated_product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return updated_product



@router.delete('/{product_id}', response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud.delete_product(db, product_id=product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return deleted_product