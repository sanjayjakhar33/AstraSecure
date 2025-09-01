"""
Scan-related schemas
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.models.scan_result import ScanStatus, ScanType


class ScanTargetBase(BaseModel):
    """Base scan target schema"""
    name: str
    description: Optional[str] = None
    target_type: str
    target_value: str
    cloud_provider: Optional[str] = None
    cloud_region: Optional[str] = None
    tags: List[str] = []


class ScanTargetCreate(ScanTargetBase):
    """Scan target creation schema"""
    scan_config: Dict[str, Any] = {}
    scan_frequency: str = "manual"
    criticality: str = "medium"


class ScanTargetUpdate(BaseModel):
    """Scan target update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    scan_config: Optional[Dict[str, Any]] = None
    scan_frequency: Optional[str] = None
    criticality: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ScanTarget(ScanTargetBase):
    """Scan target response schema"""
    id: int
    company_id: int
    scan_config: Dict[str, Any]
    scan_frequency: str
    last_scan_at: Optional[datetime]
    next_scan_at: Optional[datetime]
    risk_score: int
    criticality: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ScanResultBase(BaseModel):
    """Base scan result schema"""
    scan_type: ScanType
    scan_config: Dict[str, Any] = {}


class ScanResult(ScanResultBase):
    """Scan result response schema"""
    id: int
    status: ScanStatus
    target_id: int
    company_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    risk_score: int
    risk_score_delta: int
    error_message: Optional[str] = None
    initiated_by: Optional[str] = None
    scan_name: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NetworkScanRequest(BaseModel):
    """Network scan request schema"""
    target_id: int
    scan_profile: str = "basic"  # basic, comprehensive, quick, stealth
    config: Dict[str, Any] = {}


class VulnerabilityBase(BaseModel):
    """Base vulnerability schema"""
    title: str
    description: str
    category: str
    severity: str


class Vulnerability(VulnerabilityBase):
    """Vulnerability response schema"""
    id: int
    status: str
    cve_id: Optional[str]
    cvss_score: Optional[float]
    affected_asset: Optional[str]
    port: Optional[int]
    service: Optional[str]
    scanner_name: str
    remediation_guidance: Optional[str]
    business_impact: Optional[str]
    target_id: int
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    resolved_at: Optional[datetime]
    first_seen: datetime
    last_seen: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True