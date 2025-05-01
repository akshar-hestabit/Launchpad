from pydantic import BaseModel, EmailStr 
from typing import Literal
from datetime import datetime

# -------- User Schemas -------- #

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "vendor", "customer"]

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None


# -------- Category, Brand, Vendor Nested Schemas -------- #

class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class BrandOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class VendorOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


# -------- Product Schemas -------- #

class ProductBase(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    quantity: int
    category_id: int
    brand: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    category: CategoryOut      # changed from category_id: str
    brand: BrandOut            # changed from brand: Optional[str]
    vendor: VendorOut          # added vendor field

    model_config = {
        "from_attributes": True
    }


# -------- Order Schemas -------- #

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

    model_config = {
        "from_attributes": True
    }
