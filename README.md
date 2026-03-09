# 🛒 Monoclone — Order Management API v2.0

A lightweight Amazon-like backend built with **FastAPI**, **SQLAlchemy 2.0**, and **SQLite** — fully restructured with authentication, a product catalogue, analytics, and real-time webhooks.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange)
![CI](https://github.com/aline-precious/monoclone/actions/workflows/ci.yml/badge.svg)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **JWT Auth** | Register, login, access + refresh tokens |
| 🏷️ **Product Catalogue** | Categories, stock tracking, image URLs, search |
| 📦 **Order Management** | Full lifecycle, automatic totals, stock deduction |
| 📊 **Analytics** | Revenue by day, top products, top customers |
| 🔔 **Webhooks** | Real-time POST notifications on order status change |
| ✅ **Pydantic v2** | Full validation with consistent JSON error shape |
| 🗄️ **SQLAlchemy 2.0** | Modern ORM with relationship handling |

---

## 🗂 Project Structure

```
monoclone/
├── app/
│   ├── main.py              # App factory, middleware, routers
│   ├── models.py            # SQLAlchemy ORM: User, Customer, Product, Order, Webhook
│   ├── schemas.py           # Pydantic v2 request/response schemas
│   ├── crud.py              # All database operations
│   ├── webhooks.py          # Async webhook dispatcher with HMAC signing
│   ├── core/
│   │   ├── config.py        # Settings loaded from .env
│   │   ├── security.py      # JWT creation, verification, dependencies
│   │   └── errors.py        # Consistent JSON error handlers
│   ├── db/
│   │   ├── base.py          # SQLAlchemy DeclarativeBase
│   │   └── session.py       # Engine, SessionLocal, get_db()
│   └── routers/
│       ├── auth.py          # /auth — register, login, refresh, me
│       ├── products.py      # /products — catalogue + categories
│       ├── customers.py     # /customers — CRUD
│       ├── orders.py        # /orders — create, list, status update
│       ├── webhooks.py      # /webhooks — register/delete listeners
│       └── analytics.py     # /analytics — revenue, top products
├── .github/workflows/
│   └── ci.yml               # Lint + startup verification (Python 3.10–3.12)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/aline-precious/monoclone.git
cd monoclone
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your `.env` file

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=sqlite:///./monoclone.db
PROJECT_NAME=Monoclone Order Management API
SECRET_KEY=your-long-random-secret-here
DEBUG=True
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for interactive Swagger UI.

---

## 📡 API Overview

### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | ❌ | Create a new account |
| `POST` | `/auth/login` | ❌ | Get access + refresh tokens |
| `POST` | `/auth/refresh` | ❌ | Exchange refresh token |
| `GET` | `/auth/me` | ✅ | Get current user |

### Products
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/products/categories` | ✅ Admin | Create category |
| `GET` | `/products/categories` | ❌ | List categories |
| `POST` | `/products` | ✅ Admin | Create product |
| `GET` | `/products` | ❌ | List products (filter by category, stock, search) |
| `GET` | `/products/{id}` | ❌ | Get product |
| `PATCH` | `/products/{id}` | ✅ Admin | Update product |
| `DELETE` | `/products/{id}` | ✅ Admin | Soft-delete product |

### Customers
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/customers` | ✅ | Create customer |
| `GET` | `/customers` | ✅ | List customers |
| `GET` | `/customers/{id}` | ✅ | Get customer |
| `PATCH` | `/customers/{id}` | ✅ | Update customer |
| `DELETE` | `/customers/{id}` | ✅ | Delete customer |

### Orders
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/orders` | ✅ | Create order (auto-creates customer) |
| `GET` | `/orders` | ✅ | List orders (filter by status, customer) |
| `GET` | `/orders/{id}` | ✅ | Get order |
| `PATCH` | `/orders/{id}/status` | ✅ | Update status + fire webhooks |
| `DELETE` | `/orders/{id}` | ✅ | Delete order |

### Webhooks
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/webhooks` | Register a URL to receive order events |
| `GET` | `/webhooks` | List your webhooks |
| `DELETE` | `/webhooks/{id}` | Delete a webhook |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/analytics?days=30` | Full dashboard: revenue, top products, top customers |

---

## 🔔 Webhook Payload

When an order status changes, all registered webhooks receive:

```json
{
  "event": "order.status_changed",
  "timestamp": "2025-01-01T12:00:00+00:00",
  "data": {
    "order_id": 42,
    "customer_id": 7,
    "old_status": "pending",
    "new_status": "shipped",
    "total": "149.99"
  }
}
```

If you provide a `secret` when registering your webhook, the request will include an `X-Monoclone-Signature: sha256=<hmac>` header for verification.

---

## ❌ Error Responses

All errors return a consistent JSON shape:

```json
{
  "error": true,
  "status_code": 404,
  "message": "Order not found",
  "path": "/orders/99"
}
```

---

## 🧪 CI/CD

GitHub Actions runs on every push to `main`:
- Pylint across Python 3.10, 3.11, 3.12
- App startup verification
- Route existence checks for all 6 modules

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLAlchemy 2.0 | ORM |
| Pydantic v2 | Schema validation |
| python-jose | JWT tokens |
| passlib + bcrypt | Password hashing |
| httpx | Async webhook delivery |
| Uvicorn | ASGI server |
| SQLite | Default database (swap via `DATABASE_URL`) |

---

## Author

**aline-precious** — built as a hands-on backend learning project.
