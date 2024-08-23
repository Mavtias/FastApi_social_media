from pydantic import BaseModel, EmailStr, conint
from datetime import datetime





class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True



class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime

#Here we define the response model for the queries of postman
class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime = datetime.now()
    user : UserOut


class PostOut(BaseModel):
    Post : Post
    votes: int

    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
    username: str | None = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge = 0, le = 1)# 1 for upvote, -1 for downvote, 0 to remove vote