from sqlalchemy import Column, Integer, String
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True),
    username = Column(String,index=True ,unique=True, nullable=False),
    email = Column(String, index=True, unique=True, nullable=False),
    hashed_password = Column(String, nullable=False),
    role = Column(String, nullable=False)
