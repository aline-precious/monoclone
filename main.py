from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from app.db.session import engine
from app.db.base import Base
from app.routers import auth, customers, orders, products, webhooks, analytics


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="2.0.0",
        description="""
## 🛒 Monoclone — Order Management API

A lightweight Amazon-like backend with:
- **JWT Auth** — register, login, token refresh
- **Product Catalogue** — categories, stock management, search
- **Order Management** — full lifecycle with automatic total calculation
- **Analytics** — revenue, top products, customer stats
- **Webhooks** — real-time order status change notifications
        """,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Routers
    app.include_router(auth.router)
    app.include_router(products.router)
    app.include_router(customers.router)
    app.include_router(orders.router)
    app.include_router(webhooks.router)
    app.include_router(analytics.router)

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    @app.get("/", tags=["Health"])
    def root():
        return {
            "status": "online",
            "project": settings.PROJECT_NAME,
            "version": "2.0.0",
            "docs": "/docs",
        }

    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "healthy"}

    return app


app = create_app()
