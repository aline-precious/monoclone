from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, crud
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("", response_model=schemas.AnalyticsResponse)
def get_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to include in daily revenue chart"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    """
    Returns:
    - Total revenue, orders, customers, products
    - Revenue broken down by day (last N days)
    - Top 10 products by revenue
    - Top 10 customers by spend
    - Order counts grouped by status
    """
    return crud.get_analytics(db, days=days)
