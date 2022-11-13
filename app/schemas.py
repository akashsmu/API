from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    email : str
    id: int
    create_at: datetime

    class Config:
        orm_mode = True
    pass

class Post (BaseModel):
    title : str 
    content : str
    published : bool = True

class PostCreate(Post):
    pass


class PostResponse(Post):
    id: int
    create_at : datetime
    user_id: int
    owner : UserResponse

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token :str
    token_type:str

class TokenData(BaseModel):
    id : Optional[str] = None