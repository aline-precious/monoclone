# monoclone
A lightweight Amazon-like backend built with FastAPI, designed for managing customers, orders, and order items. This project is a learning-by-building exercise to practice modern backend development with Python.
#Project Structure
app/
├── main.py         # Application entrypoint
├── core/           # Config & error handlers
├── db/             # Database setup (engine, sessions, base)
├── models.py       # SQLAlchemy models
├── schemas.py      # Pydantic schemas
├── crud.py         # Business logic
└── routers/        # API endpoints
#Clone the repository
git clone https://github.com/aline-precious/monoclone.git
cd mini-amazon
#with virtual environment & installing some dependencies
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
DATABASE_URL=sqlite:///./test.db
APP_HOST=0.0.0.0
APP_PORT=8000
uvicorn app.main:app --reload
#order example
{
  "customer": {
    "name": "Alice Johnson",
    "email": "alice@example.com"
  },
  "status": "pending",
  "shipping_address": "123 Main St",
  "items": [
    {"product_name": "Book – Python Basics", "unit_price": 25.5, "quantity": 2}
  ]
}
{
  "id": 1,
  "status": "pending",
  "total": 51.0,
  "customer": {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
  "items": [
    {"id": 1, "product_name": "Book – Python Basics", "unit_price": 25.5, "quantity": 2, "total_price": 51.0}
  ]
}

