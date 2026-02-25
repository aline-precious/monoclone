# monoclone

# 🛒 Mini Amazon – Order Management API

A lightweight **Amazon-like backend** built with **FastAPI** for managing customers, orders, and order items.
This project is a learning-by-building exercise to practice modern Python backend development.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Pylint](https://github.com/aline-precious/monoclone/actions/workflows/pylint.yml/badge.svg)

---

## Features

- 👤 Customer creation, retrieval, update, and deletion
- 📦 Create orders with multiple items and automatic total calculation
- ✅ Pydantic v2 validation with consistent JSON error responses
- 🗄️ SQLAlchemy 2.0 ORM models with relationship handling
- ⚙️ Environment-based configuration via `.env`
- 🧱 Modular structure ready for extension (auth, payments, migrations)

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework |
| **SQLAlchemy** | ORM and database engine |
| **Pydantic v2** | Schema validation |
| **Uvicorn** | ASGI server |
| **Pydantic-Settings** | Environment config |
| **Alembic** *(optional)* | Database migrations |

---

## Project Structure

```
monoclone/
├── main.py                  # App entry point, middleware, routers
├── models.py                # SQLAlchemy ORM models (Customer, Order, OrderItem)
├── schemas.py               # Pydantic request/response schemas
├── crud.py                  # Database operations (create, read, update, delete)
├── engine.py                # DB engine, session factory, get_db() dependency
├── base.py                  # SQLAlchemy declarative base
├── core.py                  # Exception handlers and custom errors
├── config.py                # App settings loaded from .env
├── .github/workflows/
│   └── pylint.yml           # CI pipeline
└── .env                     # Environment variables (not committed)
```

---

## Getting Started

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
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings pydantic[email]
```

### 4. Set up your `.env` file

Create a `.env` file in the root of the project:

```env
DATABASE_URL=sqlite:///./monoclone.db
PROJECT_NAME=Monoclone Order Management API
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive API docs (Swagger UI).

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/customers` | Create a new customer |
| `GET` | `/customers` | List all customers |
| `GET` | `/customers/{id}` | Get a customer by ID |
| `PATCH` | `/customers/{id}` | Update a customer |
| `DELETE` | `/customers/{id}` | Delete a customer |
| `POST` | `/orders` | Create an order with items |
| `GET` | `/orders/{id}` | Get an order by ID |
| `DELETE` | `/orders/{id}` | Delete an order |

---

## Error Responses

All errors return a consistent JSON shape:

```json
{
  "error": true,
  "status_code": 404,
  "message": "Customer not found.",
  "path": "/customers/99"
}
```

---

## CI/CD

This project uses **GitHub Actions** with Pylint to check code quality on every push across Python 3.8, 3.9, and 3.10.

---

## What I Learned

- Building a REST API with FastAPI from scratch
- Structuring a Python backend with separation of concerns (models, schemas, crud, routes)
- Using SQLAlchemy ORM relationships across multiple tables
- Pydantic v2 validation and settings management
- Setting up GitHub Actions for automated code quality checks

---

## Author

**aline-precious** — built as a hands-on backend learning project.
