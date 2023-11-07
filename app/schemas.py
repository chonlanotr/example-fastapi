
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    phone_number: Optional[str] 

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class PostBase (BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # sqlAlchemy 1.0
    # class Config:
    #     orm_mode = True
    # Sql Alchemy 2.0
    class Config:
        from_attributes = True    

class PostOut(BaseModel):
    Post: Post
    votes: int

    # Sql Alchemy 2.0
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None



class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)
    
