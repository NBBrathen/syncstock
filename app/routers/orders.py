from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

# @router.post("", response_model=schemas.Order, status_code=201)
# def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
#     return crud.create_order(db, order=order)

@router.get("", response_model=List[schemas.Order])
def get_orders(limit: int = None, db: Session = Depends(get_db)):
    return crud.get_orders(db, limit=limit)

@router.get("/{order_id}", response_model = schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order