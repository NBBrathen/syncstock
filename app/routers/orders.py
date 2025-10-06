from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("", response_model=schemas.Order, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    try:
        return crud.create_order(db, order=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.Order])
def get_orders(limit: int = None, db: Session = Depends(get_db)):
    return crud.get_orders(db, limit=limit)

@router.get("/{order_id}", response_model = schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, status: schemas.OrderStatus, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    updated_order = crud.update_order_status(db, order_id=order_id, status=status.value)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}/cancel", response_model=schemas.Order)
def cancel_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    try:
        cancelled_order = crud.cancel_order(db, order_id=order_id)
        if cancelled_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return cancelled_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))