"""
Scan target model for infrastructure discovery
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class TargetType(str, Enum):
    """Types of scan targets"""
    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"
    IP_RANGE = "ip_range"
    CLOUD_RESOURCE = "cloud_resource"
    CODE_REPOSITORY = "code_repository"
    WEB_APPLICATION = "web_application"


class CloudProvider(str, Enum):
    """Cloud providers"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    OCI = "oci"


class ScanTarget(Base):
    """Scan targets for vulnerability assessment"""
    
    __tablename__ = "scan_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Target identification
    target_type = Column(String, nullable=False)
    target_value = Column(String, nullable=False)  # Domain, IP, repo URL, etc.
    
    # Cloud-specific fields
    cloud_provider = Column(String, nullable=True)
    cloud_region = Column(String, nullable=True)
    cloud_resource_id = Column(String, nullable=True)
    
    # Repository-specific fields
    repository_url = Column(String, nullable=True)
    repository_branch = Column(String, default="main")
    repository_access_token = Column(String, nullable=True)  # Encrypted
    
    # Configuration
    scan_config = Column(JSON, default={})  # Scan-specific settings
    tags = Column(JSON, default=[])  # For organization and filtering
    
    # Status and scheduling
    is_active = Column(Boolean, default=True)
    scan_frequency = Column(String, default="manual")  # manual, daily, weekly, monthly
    last_scan_at = Column(DateTime, nullable=True)
    next_scan_at = Column(DateTime, nullable=True)
    
    # Risk assessment
    risk_score = Column(Integer, default=0)  # 0-100
    criticality = Column(String, default="medium")  # low, medium, high, critical
    
    # Company relationship
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="scan_targets")
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    scan_results = relationship("ScanResult", back_populates="target")
    vulnerabilities = relationship("Vulnerability", back_populates="target")
    
    def __repr__(self):
        return f"<ScanTarget(id={self.id}, name='{self.name}', type='{self.target_type}')>"