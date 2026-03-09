from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, crud
from app.core.security import get_current_user
from app.db.session import get_db
from app.webhooks import fire_order_status_changed

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=schemas.OrderRead, status_code=201)
def create_order(
    data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    """Create a new order with items. Auto-creates customer if not existing."""
    return crud.create_order(db, data)


@router.get("", response_model=List[schemas.OrderRead])
def list_orders(
    status: Optional[str] = Query(None),
    customer_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return crud.list_orders(db, status=status, customer_id=customer_id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return crud.get_order(db, order_id)


@router.patch("/{order_id}/status", response_model=schemas.OrderRead)
async def update_order_status(
    order_id: int,
    data: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    """Update order status and fire webhooks to all registered listeners."""
    order, old_status = crud.update_order_status(db, order_id, data)

    # Fire webhooks asynchronously — don't block the response
    if old_status != order.status:
        await fire_order_status_changed(db, order, old_status, order.status)

    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    crud.delete_order(db, order_id)
