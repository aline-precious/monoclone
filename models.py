"""Database models for the Monoclone Order Management API."""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Customer(Base):
    """Represents a customer in the system."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Order(Base):
    """Represents a customer order."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    customer = relationship("Customer", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    """Represents a single item inside an order."""

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)

    order = relationship("Order", back_populates="items")

    @property
    def total_price(self):
        """Calculate total price for this line item."""
        return self.quantity * self.unit_price
