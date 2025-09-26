from sqlalchemy.orm import declarative_base
Base = declarative_base()


#here wwe will be Createing the SQLAlchemy base class that all ORM models inherit f
# rom (class Customer(Base): ...). It centralizes metadata for table creation.