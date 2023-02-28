from pydantic import BaseModel
from typing import Optional

class CreateSeller(BaseModel):
    seller_unique_id:int
    username:str
    email:str
    hashed_password:str


class CreateProducts(BaseModel):
    name:str
    description:str
    price:int
    seller_id:int


class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    username : Optional[str] = None


class Seller(BaseModel):
    username:str
    email:str
    hashed_password:str

