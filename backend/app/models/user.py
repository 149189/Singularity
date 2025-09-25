from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserClass(str, Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    user_class: UserClass

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    level: int = 1
    experience: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserResponse):
    hashed_password: str
    energy: int = 100
    last_energy_update: datetime = datetime.utcnow()