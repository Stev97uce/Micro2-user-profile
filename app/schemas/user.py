from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str  # se usará para enviar al auth-service
    full_name: str
    phone: Optional[str]
    address: Optional[str]

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str]
    address: Optional[str]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
