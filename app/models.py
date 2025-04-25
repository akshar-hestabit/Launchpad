

from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,index=True ,unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    vendor  = Column(String, nullable=True)

#    vendor_id = Column(Integer, nullable=False)


