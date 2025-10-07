from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user

router = APIRouter(
    prefix="/products",
    tags=["products"],
)



@router.get("/search", response_model=List[schemas.Product])
def search_products(
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock_only: bool = False,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.search_products(
        db,
        search=search,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
        skip=skip,
        limit=limit
    )

@router.get("", response_model=List[schemas.Product])
def get_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):

    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/low-stock", response_model=List[schemas.Product])
def get_low_stock_products(db: Session = Depends(get_db)):
    return crud.get_low_stock_products(db)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404,detail="Product not Found")
    return product



@router.post('', response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):

    return crud.create_product(db, product=product)



@router.patch('/{product_id}', response_model=schemas.Product)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):

    updated_product = crud.update_product(db, product_id=product_id, product_update=product_update)
    if updated_product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return updated_product



@router.delete('/{product_id}', response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    deleted_product = crud.delete_product(db, product_id=product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return deleted_product

