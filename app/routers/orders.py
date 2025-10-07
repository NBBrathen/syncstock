from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth import get_current_active_user
from app.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/filter", response_model=List[schemas.Order])
def filter_order(
    status: Optional[str] = None,
    customer_email: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.filter_orders(
        db, status=status, customer_email=customer_email, skip=skip, limit=limit
    )


@router.post("", response_model=schemas.Order, status_code=201)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    try:
        return crud.create_order(db, order=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status", response_model=schemas.Order)
def update_order_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    updated_order = crud.update_order_status(
        db, order_id=order_id, status=status_update.status.value
    )
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.delete("/{order_id}/cancel", response_model=schemas.Order)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    try:
        cancelled_order = crud.cancel_order(db, order_id=order_id)
        if cancelled_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return cancelled_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
