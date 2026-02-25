"""CRUD operations for customers and orders."""

from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas


# ─── Customer Operations 

def get_customer_by_email(db: Session, email: Optional[str]) -> Optional[models.Customer]:
    """Look up a customer by email address."""
    if not email:
        return None
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customer_by_id(db: Session, customer_id: int) -> Optional[models.Customer]:
    """Look up a customer by their ID."""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_all_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    """Return a paginated list of all customers."""
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer_in: schemas.CustomerCreate) -> models.Customer:
    """Create a new customer, checking for duplicate email first."""
    existing = get_customer_by_email(db, customer_in.email)
    if existing:
        raise ValueError(f"Customer with email '{customer_in.email}' already exists.")

    db_customer = models.Customer(**customer_in.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(
    db: Session,
    customer_id: int,
    updates: schemas.CustomerUpdate
) -> Optional[models.Customer]:
    """Partially update a customer's details."""
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return None

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int) -> bool:
    """Delete a customer and all their orders (cascade)."""
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True


# ─── Order Operations ──────────────────────────────────────────────────────────

def get_order_by_id(db: Session, order_id: int) -> Optional[models.Order]:
    """Look up a single order by ID."""
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders_by_customer(db: Session, customer_id: int) -> List[models.Order]:
    """Return all orders belonging to a customer."""
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()


def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    """
    Create an order with its line items.

    Steps:
    1. Verify the customer exists
    2. Create the order row
    3. Create each order item row
    4. Compute and store the total amount
    5. Commit and return the full order
    """
    # Step 1 — find or raise
    db_customer = get_customer_by_id(db, order_in.customer_id)
    if not db_customer:
        raise ValueError(f"Customer with ID {order_in.customer_id} not found.")

    # Step 2 — create order row
    db_order = models.Order(
        customer_id=order_in.customer_id,
        status=order_in.status or "pending",
        notes=order_in.notes,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Step 3 & 4 — create items and compute total
    total_amount = Decimal("0.00")
    for item in order_in.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            description=item.description,
        )
        total_amount += Decimal(str(item.unit_price)) * item.quantity
        db.add(db_item)

    # Step 5 — commit and return
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    """Delete an order and all its items (cascade)."""
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True
