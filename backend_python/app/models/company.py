"""
Company model for multi-tenant architecture
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class SubscriptionTier(str, Enum):
    """Subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class Company(Base):
    """Company model for multi-tenant SaaS"""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    domain = Column(String, unique=True, index=True, nullable=True)
    
    # Contact information
    address = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    # Business information
    industry = Column(String, nullable=True)
    size = Column(String, nullable=True)  # e.g., "1-10", "11-50", "51-200", etc.
    
    # Subscription and billing
    subscription_tier = Column(String, default=SubscriptionTier.FREE)
    subscription_status = Column(String, default="active")  # active, suspended, cancelled
    billing_email = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    
    # Settings and configuration
    settings = Column(JSON, default={})
    
    # Cloud provider credentials (encrypted)
    aws_credentials = Column(JSON, nullable=True)
    gcp_credentials = Column(JSON, nullable=True)
    azure_credentials = Column(JSON, nullable=True)
    
    # Compliance requirements
    compliance_frameworks = Column(JSON, default=[])  # ["SOC2", "PCI-DSS", "ISO27001"]
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="company")
    scan_targets = relationship("ScanTarget", back_populates="company")
    scan_results = relationship("ScanResult", back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', tier='{self.subscription_tier}')>"