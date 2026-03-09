from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from decimal import Decimal


# ── Auth ─────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


# ── Categories ───────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryRead(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Products ─────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    sku: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    is_active: bool = True
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str]
    sku: Optional[str]
    price: Decimal
    stock: int
    image_url: Optional[str]
    is_active: bool
    category: Optional[CategoryRead]
    created_at: datetime


# ── Customers ────────────────────────────────────────────────────────────────

class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerRead(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ── Orders ───────────────────────────────────────────────────────────────────

ORDER_STATUSES = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled", "refunded"]


class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: str = Field(..., min_length=1)
    unit_price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: Optional[int]
    product_name: str
    unit_price: Decimal
    quantity: int
    total_price: Decimal


class OrderCreate(BaseModel):
    customer: CustomerCreate
    status: str = Field(default="pending")
    shipping_address: Optional[str] = None
    notes: Optional[str] = None
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., description=f"One of: {', '.join(ORDER_STATUSES)}")
    notes: Optional[str] = None


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer: CustomerRead
    status: str
    total: Decimal
    shipping_address: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemRead]


# ── Webhooks ─────────────────────────────────────────────────────────────────

class WebhookCreate(BaseModel):
    url: str = Field(..., description="HTTPS URL to receive webhook POST requests")
    events: str = Field(default="order.status_changed")
    secret: Optional[str] = Field(None, description="Optional secret for HMAC signature verification")


class WebhookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    events: str
    is_active: bool
    created_at: datetime


# ── Analytics ────────────────────────────────────────────────────────────────

class RevenueByDay(BaseModel):
    date: str
    revenue: float
    order_count: int


class TopProduct(BaseModel):
    product_name: str
    total_sold: int
    total_revenue: float


class CustomerStat(BaseModel):
    customer_id: int
    customer_name: str
    order_count: int
    total_spent: float


class AnalyticsResponse(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int
    revenue_by_day: List[RevenueByDay]
    top_products: List[TopProduct]
    top_customers: List[CustomerStat]
    orders_by_status: dict
