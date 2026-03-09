from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, crud
from app.core.security import get_current_user, require_admin
from app.db.session import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/categories", response_model=schemas.CategoryRead, status_code=201)
def create_category(
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_admin),
):
    return crud.create_category(db, data)


@router.get("/categories", response_model=List[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


@router.post("", response_model=schemas.ProductRead, status_code=201)
def create_product(
    data: schemas.ProductCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_admin),
):
    """Create a new product (admin only)."""
    return crud.create_product(db, data)


@router.get("", response_model=List[schemas.ProductRead])
def list_products(
    category_id: Optional[int] = Query(None),
    in_stock: Optional[bool] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List products with optional filtering by category, stock, and search."""
    return crud.list_products(db, category_id=category_id, in_stock=in_stock, search=search, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@router.patch("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_admin),
):
    return crud.update_product(db, product_id, data)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_admin),
):
    crud.delete_product(db, product_id)
