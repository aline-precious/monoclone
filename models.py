from sqlalchemy import (
    Column, Integer, String, Numeric, ForeignKey,
    Text, DateTime, Boolean, func
)
from sqlalchemy.orm import relationship
from app.db.base import Base


# ── Users ────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String(255), unique=True, index=True, nullable=False)
    name       = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active  = Column(Boolean, default=True, nullable=False)
    is_admin   = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    webhooks   = relationship("Webhook", back_populates="user", cascade="all, delete-orphan")


# ── Customers ────────────────────────────────────────────────────────────────

class Customer(Base):
    __tablename__ = "customers"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(255), nullable=False)
    email      = Column(String(255), unique=True, index=True, nullable=True)
    phone      = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders     = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


# ── Product Catalogue ────────────────────────────────────────────────────────

class Category(Base):
    __tablename__ = "categories"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    products    = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    sku         = Column(String(100), unique=True, index=True, nullable=True)
    price       = Column(Numeric(12, 2), nullable=False)
    stock       = Column(Integer, default=0, nullable=False)
    image_url   = Column(String(500), nullable=True)
    is_active   = Column(Boolean, default=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    category    = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


# ── Orders ───────────────────────────────────────────────────────────────────

class Order(Base):
    __tablename__ = "orders"

    id               = Column(Integer, primary_key=True, index=True)
    customer_id      = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status           = Column(String(50), nullable=False, index=True, default="pending")
    total            = Column(Numeric(12, 2), nullable=False, default=0)
    shipping_address = Column(Text, nullable=True)
    notes            = Column(Text, nullable=True)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
    updated_at       = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="orders")
    items    = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id           = Column(Integer, primary_key=True, index=True)
    order_id     = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id   = Column(Integer, ForeignKey("products.id"), nullable=True)
    product_name = Column(String(255), nullable=False)
    unit_price   = Column(Numeric(12, 2), nullable=False)
    quantity     = Column(Integer, nullable=False)
    total_price  = Column(Numeric(12, 2), nullable=False)

    order   = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


# ── Webhooks ─────────────────────────────────────────────────────────────────

class Webhook(Base):
    __tablename__ = "webhooks"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    url        = Column(String(500), nullable=False)
    events     = Column(String(500), nullable=False, default="order.status_changed")
    secret     = Column(String(255), nullable=True)
    is_active  = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="webhooks")
