from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from decimal import Decimal
from typing import Optional, List
from fastapi import HTTPException

from app import models, schemas
from app.core.security import hash_password


# ── Auth / Users ─────────────────────────────────────────────────────────────

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, data: schemas.UserRegister) -> models.User:
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = models.User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── Categories ───────────────────────────────────────────────────────────────

def create_category(db: Session, data: schemas.CategoryCreate) -> models.Category:
    cat = models.Category(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def list_categories(db: Session) -> List[models.Category]:
    return db.query(models.Category).all()


# ── Products ─────────────────────────────────────────────────────────────────

def create_product(db: Session, data: schemas.ProductCreate) -> models.Product:
    product = models.Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(
    db: Session,
    category_id: Optional[int] = None,
    in_stock: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Product]:
    q = db.query(models.Product).filter(models.Product.is_active == True)
    if category_id:
        q = q.filter(models.Product.category_id == category_id)
    if in_stock:
        q = q.filter(models.Product.stock > 0)
    if search:
        q = q.filter(models.Product.name.ilike(f"%{search}%"))
    return q.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> models.Product:
    p = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p


def update_product(db: Session, product_id: int, data: schemas.ProductUpdate) -> models.Product:
    product = get_product(db, product_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    product.is_active = False
    db.commit()


# ── Customers ────────────────────────────────────────────────────────────────

def get_customer_by_email(db: Session, email: Optional[str]) -> Optional[models.Customer]:
    if not email:
        return None
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def create_customer(db: Session, data: schemas.CustomerCreate) -> models.Customer:
    customer = models.Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def list_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int) -> models.Customer:
    c = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c


def update_customer(db: Session, customer_id: int, data: schemas.CustomerCreate) -> models.Customer:
    customer = get_customer(db, customer_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    customer = get_customer(db, customer_id)
    db.delete(customer)
    db.commit()


# ── Orders ───────────────────────────────────────────────────────────────────

def create_order(db: Session, data: schemas.OrderCreate) -> models.Order:
    # Resolve or create customer
    customer = get_customer_by_email(db, data.customer.email)
    if not customer:
        customer = create_customer(db, data.customer)

    # Validate status
    if data.status not in schemas.ORDER_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status: {data.status}")

    order = models.Order(
        customer_id=customer.id,
        status=data.status,
        shipping_address=data.shipping_address,
        notes=data.notes,
    )
    db.add(order)
    db.flush()

    total = Decimal("0.00")
    for item in data.items:
        item_total = Decimal(str(item.unit_price)) * item.quantity
        total += item_total

        # Deduct stock if product_id provided
        if item.product_id:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            if product:
                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient stock for '{product.name}' (available: {product.stock})"
                    )
                product.stock -= item.quantity

        db_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            total_price=item_total,
        )
        db.add(db_item)

    order.total = total
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> models.Order:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def list_orders(
    db: Session,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Order]:
    q = db.query(models.Order)
    if status:
        q = q.filter(models.Order.status == status)
    if customer_id:
        q = q.filter(models.Order.customer_id == customer_id)
    return q.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, data: schemas.OrderStatusUpdate) -> models.Order:
    if data.status not in schemas.ORDER_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {schemas.ORDER_STATUSES}")
    order = get_order(db, order_id)
    old_status = order.status
    order.status = data.status
    if data.notes:
        order.notes = data.notes
    db.commit()
    db.refresh(order)
    return order, old_status


def delete_order(db: Session, order_id: int) -> None:
    order = get_order(db, order_id)
    db.delete(order)
    db.commit()


# ── Webhooks ─────────────────────────────────────────────────────────────────

def create_webhook(db: Session, user_id: int, data: schemas.WebhookCreate) -> models.Webhook:
    webhook = models.Webhook(user_id=user_id, **data.model_dump())
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


def list_webhooks(db: Session, user_id: int) -> List[models.Webhook]:
    return db.query(models.Webhook).filter(models.Webhook.user_id == user_id).all()


def delete_webhook(db: Session, webhook_id: int, user_id: int) -> None:
    wh = db.query(models.Webhook).filter(
        models.Webhook.id == webhook_id,
        models.Webhook.user_id == user_id
    ).first()
    if not wh:
        raise HTTPException(status_code=404, detail="Webhook not found")
    db.delete(wh)
    db.commit()


def get_active_webhooks_for_event(db: Session, event: str) -> List[models.Webhook]:
    return db.query(models.Webhook).filter(
        models.Webhook.is_active == True,
        models.Webhook.events.contains(event),
    ).all()


# ── Analytics ────────────────────────────────────────────────────────────────

def get_analytics(db: Session, days: int = 30) -> schemas.AnalyticsResponse:
    from datetime import datetime, timedelta

    since = datetime.utcnow() - timedelta(days=days)

    total_revenue = db.query(func.sum(models.Order.total)).scalar() or 0
    total_orders = db.query(func.count(models.Order.id)).scalar() or 0
    total_customers = db.query(func.count(models.Customer.id)).scalar() or 0
    total_products = db.query(func.count(models.Product.id)).filter(models.Product.is_active == True).scalar() or 0

    # Revenue by day
    daily = (
        db.query(
            cast(models.Order.created_at, Date).label("date"),
            func.sum(models.Order.total).label("revenue"),
            func.count(models.Order.id).label("order_count"),
        )
        .filter(models.Order.created_at >= since)
        .group_by(cast(models.Order.created_at, Date))
        .order_by(cast(models.Order.created_at, Date))
        .all()
    )
    revenue_by_day = [
        schemas.RevenueByDay(date=str(r.date), revenue=float(r.revenue), order_count=r.order_count)
        for r in daily
    ]

    # Top products
    top_prods = (
        db.query(
            models.OrderItem.product_name,
            func.sum(models.OrderItem.quantity).label("total_sold"),
            func.sum(models.OrderItem.total_price).label("total_revenue"),
        )
        .group_by(models.OrderItem.product_name)
        .order_by(func.sum(models.OrderItem.total_price).desc())
        .limit(10)
        .all()
    )
    top_products = [
        schemas.TopProduct(
            product_name=p.product_name,
            total_sold=p.total_sold,
            total_revenue=float(p.total_revenue),
        )
        for p in top_prods
    ]

    # Top customers
    top_custs = (
        db.query(
            models.Customer.id,
            models.Customer.name,
            func.count(models.Order.id).label("order_count"),
            func.sum(models.Order.total).label("total_spent"),
        )
        .join(models.Order, models.Order.customer_id == models.Customer.id)
        .group_by(models.Customer.id)
        .order_by(func.sum(models.Order.total).desc())
        .limit(10)
        .all()
    )
    top_customers = [
        schemas.CustomerStat(
            customer_id=c.id,
            customer_name=c.name,
            order_count=c.order_count,
            total_spent=float(c.total_spent),
        )
        for c in top_custs
    ]

    # Orders by status
    status_rows = (
        db.query(models.Order.status, func.count(models.Order.id).label("count"))
        .group_by(models.Order.status)
        .all()
    )
    orders_by_status = {row.status: row.count for row in status_rows}

    return schemas.AnalyticsResponse(
        total_revenue=float(total_revenue),
        total_orders=total_orders,
        total_customers=total_customers,
        total_products=total_products,
        revenue_by_day=revenue_by_day,
        top_products=top_products,
        top_customers=top_customers,
        orders_by_status=orders_by_status,
    )
