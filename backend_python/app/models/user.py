"""
User model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class UserRole(str, Enum):
    """User roles enum"""
    SUPER_ADMIN = "super_admin"
    COMPANY_ADMIN = "company_admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base):
    """User model for multi-tenant authentication"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default=UserRole.VIEWER)
    
    # Company relationship
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="users")
    
    # Profile information
    phone = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # API access
    api_key = Column(String, nullable=True, unique=True)
    api_key_expires = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"