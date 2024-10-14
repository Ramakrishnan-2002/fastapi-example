# schemas.py

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel,EmailStr, Field
from .models import Post

class Postdata_validator(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


    
class User_out(BaseModel):
    id:int
    email: EmailStr
    created_at : datetime
    class Config:
        from_attributes=True
class Postdata_response(BaseModel):
    id:int
    title: str
    created_at : datetime
    owner_id :int
     # Assuming your Post model has an 'id' field
    owner : User_out
    class Config:
        from_attributes = True 
         # Ensure ORM mode is enabled

class PostVote(BaseModel):
    post: Postdata_response  # Use lowercase 'post' to match the response
    vote: int  # Use 'vote' instead of 'vote_count' for consistency

    class Config:
        from_attributes = True  # Enable ORM compatibility
#Basemodel validates only the json data so we're using config orm_mode


class User_create(BaseModel):
    email : EmailStr  #Emailstr is to validate the email given by pydantic
    password : str



# class Loginuser(BaseModel):
#     email: EmailStr
#     password :str No need as we have created oauth2passwordrequestform


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenResponseData(BaseModel):
    id : int



#Schema for vote
class Vote(BaseModel):
    post_id :int
    dir: Annotated[int, Field(ge=0, le=1)]