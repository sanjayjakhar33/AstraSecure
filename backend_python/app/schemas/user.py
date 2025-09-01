"""
User schemas for API requests and responses
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    is_active: bool = True


class UserCreate(UserBase):
    """User creation schema"""
    password: str
    company_id: Optional[int] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    company_id: Optional[int] = None


class UserInDB(UserBase):
    """User schema for database operations"""
    id: int
    hashed_password: str
    company_id: Optional[int] = None
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    api_key: Optional[str] = None
    api_key_expires: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserBase):
    """User schema for API responses"""
    id: int
    company_id: Optional[int] = None
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserToken(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


class PasswordReset(BaseModel):
    """Password reset request schema"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class APIKeyResponse(BaseModel):
    """API key response schema"""
    api_key: str
    expires_at: datetime