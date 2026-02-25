"""Pydantic schemas for request validation and response serialization."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# ─── Order Item Schemas ────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    """Schema for creating a new order item."""

    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., gt=0, description="Must be at least 1")
    unit_price: float = Field(..., gt=0, description="Price per unit")
    description: Optional[str] = None


class OrderItemRead(OrderItemCreate):
    """Schema for reading an order item."""

    id: int
    order_id: int
    total_price: float

    class Config:
        """Pydantic config."""
        from_attributes = True


# ─── Order Schemas ─────────────────────────────────────────────────────────────

class OrderCreate(BaseModel):
    """Schema for creating a new order."""

    customer_id: int
    status: Optional[str] = Field(default="pending", max_length=50)
    notes: Optional[str] = None
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderRead(BaseModel):
    """Schema for reading an order."""

    id: int
    customer_id: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemRead] = []

    class Config:
        """Pydantic config."""
        from_attributes = True


# ─── Customer Schemas ──────────────────────────────────────────────────────────

class CustomerCreate(BaseModel):
    """Schema for creating a new customer."""

    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)


class CustomerRead(CustomerCreate):
    """Schema for reading a customer, including their orders."""

    id: int
    created_at: datetime
    orders: List[OrderRead] = []

    class Config:
        """Pydantic config."""
        from_attributes = True


class CustomerUpdate(BaseModel):
    """Schema for partially updating a customer."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
