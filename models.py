from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Association table for the many-to-many relationship between orders and items
order_items = Table(
    "order_items",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("item_id", ForeignKey("items.id"), primary_key=True),
)


# SQLAlchemy model for User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    datetime = Column(Date)

    items = relationship("Item", back_populates="owner")
    orders = relationship("Order", back_populates="user")


# SQLAlchemy model for Item
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    orders = relationship("Order", secondary=order_items, back_populates="items")


# SQLAlchemy model for Order
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date)
    total = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    items = relationship("Item", secondary=order_items, back_populates="orders")


# Database configuration
DATABASE_URL = "postgresql://postgres:new_password@localhost:5432/test"

# Set up the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to create the database
def create_db():
    """
    Create all tables in the database.
    """
    Base.metadata.create_all(bind=engine)
    print("Database and tables created.")


# Function to drop (clear) the database
def clear_db():
    """
    Drop all tables in the database.
    """
    Base.metadata.drop_all(bind=engine)
    print("Database cleared (tables dropped).")
