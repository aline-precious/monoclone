from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
# ... Order and OrderItem similar


#by Defineing DB tables as Python classes. Each attribute maps to a column. Relationships define how rows relate (customer → orders → order items)
#its more of declaring and defining what we will be needing , values and how long will they be