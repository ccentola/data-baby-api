from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_on: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class BottleBase(BaseModel):
    """
    date
    time
    brand
    amount
    notes
    """

    brand: str
    amount: int
    notes: Optional[str] = None


class BottleCreate(BottleBase):
    pass


class Bottle(BottleBase):
    id: int
    created_on: datetime
    parent_id: int
    parent: UserOut

    class Config:
        orm_mode = True


class DiaperBase(BaseModel):
    soil_type: str
    notes: Optional[str] = None


class DiaperCreate(DiaperBase):
    pass


class Diaper(DiaperBase):
    id: int
    created_on: datetime
    parent_id: int
    parent: UserOut

    class Config:
        orm_mode = True
