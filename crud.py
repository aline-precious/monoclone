##with this small functions that encapsulate common DB tasks: look up a customer, create a customer, create an order with items, compute totals, and return the created order
#Routes call these functions to keep route handlers thin and let tests target business logic easily. They must run after models and session are available.
from sqlalchemy.orm import Session
from app import models, schemas
from decimal import Decimal

def get_customer_by_email(db: Session, email: Optional[str]):
    if not email:
        return None
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_customer(db: Session, customer_in: schemas.CustomerCreate):
    db_c = models.Customer(**customer_in.dict())
    db.add(db_c)
    db.commit()
    db.refresh(db_c)
    return db_c

def create_order(db: Session, order_in: schemas.OrderCreate):
    db_c = db.query(models.Customer).filter(models.Customer.id == order_in.customer_id).first()
    if not db_c:
        raise ValueError("Customer not found")
    db_o = models.Order(customer_id=order_in.customer_id)
    db.add(db_o)
    db.commit()
    db.refresh(db_o)

    total_amount = Decimal('0.00')
    for item in order_in.items:
        db_oi = models.OrderItem(
            order_id=db_o.id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        )
        total_amount += item.price * item.quantity
        db.add(db_oi)
    db_o.total_amount = total_amount
    db.commit()
    db.refresh(db_o)
    return db_o
## find or create customer
    # create order row
    # create items rows, compute totals
    # commit and return order