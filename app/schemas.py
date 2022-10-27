from token import OP
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Union
from pydantic.types import conint


class UserBase(BaseModel):
    email:EmailStr
    username:str

class CreateUser(UserBase):
    password:str


class ReadUser(UserBase):
    id:int
    created_at:datetime

    class Config():
        orm_mode = True

class PostBase(BaseModel):
    title:str
    content:str
    published:bool= True



class CreatePost(PostBase):
    pass






class ReadPost(PostBase):
    id:int
    created_at:datetime
    owner:ReadUser
    # likes:Optional[int]
    class Config:
        orm_mode=True

class UserPosts(BaseModel):
    id:int
    title:str
    content:str
    published:bool= True
    class Config:
        orm_mode=True


class ReadUserPosts(ReadUser):
    posts:List[UserPosts]
    is_admin:bool



class UserLogin(BaseModel):
    email: Optional[EmailStr]=None
    username: Optional[str]=None
    password: str

class RefreshToken(BaseModel):
    refresh_token:str
    token_type:str



class Token(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]




class Vote(BaseModel):
    post:int
    dir: conint(le=1, gt=-1)
    hi:Optional[str]



class PostVote(BaseModel):
    PostModel: ReadPost
    likes:int