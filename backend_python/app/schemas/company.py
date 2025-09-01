"""
Company schemas for API requests and responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime

from app.models.company import SubscriptionTier


class CompanyBase(BaseModel):
    """Base company schema"""
    name: str
    domain: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Company creation schema"""
    billing_email: Optional[str] = None
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    compliance_frameworks: List[str] = []


class CompanyUpdate(BaseModel):
    """Company update schema"""
    name: Optional[str] = None
    domain: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    billing_email: Optional[str] = None
    subscription_tier: Optional[SubscriptionTier] = None
    compliance_frameworks: Optional[List[str]] = None
    settings: Optional[Dict[str, Any]] = None


class Company(CompanyBase):
    """Company schema for API responses"""
    id: int
    subscription_tier: SubscriptionTier
    subscription_status: str
    billing_email: Optional[str] = None
    compliance_frameworks: List[str] = []
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    user_count: Optional[int] = None
    scan_target_count: Optional[int] = None
    last_scan_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CompanySettings(BaseModel):
    """Company settings schema"""
    scan_frequency: Optional[str] = "weekly"
    notification_preferences: Dict[str, bool] = {
        "email_alerts": True,
        "slack_notifications": False,
        "weekly_reports": True
    }
    risk_thresholds: Dict[str, int] = {
        "critical": 90,
        "high": 70,
        "medium": 40
    }
    compliance_settings: Dict[str, Any] = {}


class CloudCredentials(BaseModel):
    """Cloud provider credentials schema"""
    provider: str  # aws, gcp, azure, oci
    credentials: Dict[str, str]  # Provider-specific credential fields
    region: Optional[str] = None
    is_active: bool = True


class CompanyStats(BaseModel):
    """Company statistics schema"""
    total_scan_targets: int
    active_vulnerabilities: int
    resolved_vulnerabilities: int
    compliance_score: float
    risk_score: int
    last_scan_date: Optional[datetime]
    scan_frequency: str
    user_count: int