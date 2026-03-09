from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, crud
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=schemas.CustomerRead, status_code=201)
def create_customer(
    data: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return crud.create_customer(db, data)


@router.get("", response_model=List[schemas.CustomerRead])
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return crud.list_customers(db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return crud.get_customer(db, customer_id)


@router.patch("/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(
    customer_id: int,
    data: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return crud.update_customer(db, customer_id, data)


@router.delete("/{customer_id}", status_code=204)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    crud.delete_customer(db, customer_id)
