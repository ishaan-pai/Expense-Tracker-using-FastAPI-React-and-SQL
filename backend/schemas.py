from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Literal

class UserBase(BaseModel):
    email:EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime | None

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    type: Literal["income", "expense"]

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    created_at: datetime | None

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    name: str
    category_id: int
    amount: Decimal
    transaction_date: date
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime | None

    class Config:
        from_attributes = True