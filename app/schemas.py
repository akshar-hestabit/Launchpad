#this is for pydantic schemas or that can be used for data validation

from pydantic import BaseModel, EmailStr 


#this comes from a frontend post signup request
#validates username, email and password are of correct type
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#we dont need to return password to frontend
#orm_mode = True allows converting from SQLALchemy objects to dict
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    class Config:
        orm_mode = True


#this is for token generation
#sent to frontend to store for auth 
class Token(BaseModel):
    access_token: str
    token_type: str 

