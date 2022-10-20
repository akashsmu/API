from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr

class Post (BaseModel):
    title : str 
    content : str
    published : bool = True

class PostCreate(Post):
    pass


class PostResponse(Post):
    id: int
    create_at : datetime

    class Config:
        orm_mode = True

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

class UserLogin(BaseModel):
    email: EmailStr
    password : str