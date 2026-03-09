from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("", response_model=schemas.WebhookRead, status_code=201)
def create_webhook(
    data: schemas.WebhookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Register a URL to receive order status change events."""
    return crud.create_webhook(db, current_user.id, data)


@router.get("", response_model=List[schemas.WebhookRead])
def list_webhooks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.list_webhooks(db, current_user.id)


@router.delete("/{webhook_id}", status_code=204)
def delete_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    crud.delete_webhook(db, webhook_id, current_user.id)
