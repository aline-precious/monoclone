from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class CustomerRead(CustomerCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# OrderCreate, OrderRead, OrderItemCreate, OrderItemRead ...
#through defining the data shapes used for inbound requests (Create) and outbound responses (Read). orm_mode = True 
# lets Pydantic read ORM objects directly (SQLAlchemy models).