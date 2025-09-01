"""
Scan result model for tracking scan executions
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class ScanStatus(str, Enum):
    """Scan execution status"""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScanType(str, Enum):
    """Types of security scans"""
    NETWORK_SCAN = "network_scan"
    WEB_SCAN = "web_scan"
    CLOUD_CONFIG_SCAN = "cloud_config_scan"
    CODE_SCAN = "code_scan"
    COMPLIANCE_SCAN = "compliance_scan"
    FULL_AUDIT = "full_audit"


class ScanResult(Base):
    """Scan execution results and metadata"""
    
    __tablename__ = "scan_results"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Scan identification
    scan_type = Column(String, nullable=False)
    status = Column(String, default=ScanStatus.QUEUED)
    
    # Execution details
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Configuration
    scan_config = Column(JSON, default={})  # Scan parameters and options
    scanner_version = Column(String, nullable=True)
    
    # Results summary
    total_vulnerabilities = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)
    
    # Risk metrics
    risk_score = Column(Integer, default=0)  # 0-100
    risk_score_delta = Column(Integer, default=0)  # Change from previous scan
    
    # Raw data
    raw_output = Column(Text, nullable=True)  # Original scanner output
    parsed_data = Column(JSON, default={})  # Structured scan data
    
    # Error handling
    error_message = Column(Text, nullable=True)
    warnings = Column(JSON, default=[])
    
    # Performance metrics
    targets_scanned = Column(Integer, default=0)
    ports_scanned = Column(Integer, default=0)
    services_discovered = Column(Integer, default=0)
    
    # Relationships
    target_id = Column(Integer, ForeignKey("scan_targets.id"), nullable=False)
    target = relationship("ScanTarget", back_populates="scan_results")
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="scan_results")
    
    vulnerabilities = relationship("Vulnerability", back_populates="scan_result")
    
    # Audit trail
    initiated_by = Column(String, nullable=True)  # User ID who started the scan
    scan_name = Column(String, nullable=True)  # Custom name for the scan
    tags = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ScanResult(id={self.id}, type='{self.scan_type}', status='{self.status}')>"
    
    @property
    def is_completed(self) -> bool:
        """Check if scan is completed"""
        return self.status in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED]
    
    @property
    def success_rate(self) -> float:
        """Calculate scan success rate"""
        if self.targets_scanned == 0:
            return 0.0
        return (self.targets_scanned - len(self.warnings or [])) / self.targets_scanned