#this is for pydantic schemas or that can be used for data validation

from pydantic import BaseModel, EmailStr 
from typing import Literal
from datetime import datetime
#this comes from a frontend post signup request
#validates username, email and password are of correct type
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "vendor", "customer"] #this is a string but can only be one of these values

#we dont need to return password to frontend
#orm_mode = True allows converting from SQLALchemy objects to dict
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    model_config = {
        "from_attributes": True
    }
#this is for token generation
#sent to frontend to store for auth 
class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None

class ProductBase(BaseModel):
    
    id: int
    name : str
    description: str | None = None
    price:float
    quantity: int
    category: str
    brand: str | None = None
    vendor: str


class ProductCreate(ProductBase):
    pass
class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    category: str
    brand: str
    vendor: str

    def to_dict(self):
        return self.model_dump()
    

class ProductUpdate(ProductBase):
    pass

class OrderCreate(BaseModel):
    user_id: int
    total_price: float
    payment_method: str
    status: str | None = "PENDING"

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    payment_method: str | None = None

    class Config:
        from_attributes = True