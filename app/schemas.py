#this is for pydantic schemas or that can be used for data validation

from pydantic import BaseModel, EmailStr 
from typing import Literal

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
class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True 
class ProductUpdate(ProductBase):
    pass