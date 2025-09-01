"""
Compliance check model for regulatory requirements
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class ComplianceFramework(str, Enum):
    """Supported compliance frameworks"""
    SOC2 = "soc2"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"
    HIPAA = "hipaa"
    GDPR = "gdpr"
    NIST = "nist"
    CIS = "cis"
    OWASP = "owasp"


class ComplianceStatus(str, Enum):
    """Compliance check status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNKNOWN = "unknown"


class ComplianceCheck(Base):
    """Compliance checks and regulatory requirements"""
    
    __tablename__ = "compliance_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Framework information
    framework = Column(String, nullable=False)
    control_id = Column(String, nullable=False)  # e.g., "CC6.1", "PCI-DSS-4.1"
    control_title = Column(String, nullable=False)
    control_description = Column(Text, nullable=False)
    
    # Check details
    check_name = Column(String, nullable=False)
    check_description = Column(Text, nullable=False)
    check_rationale = Column(Text, nullable=True)
    
    # Implementation guidance
    implementation_guidance = Column(Text, nullable=True)
    testing_procedures = Column(Text, nullable=True)
    remediation_guidance = Column(Text, nullable=True)
    
    # Categorization
    category = Column(String, nullable=True)  # e.g., "Access Control", "Encryption"
    subcategory = Column(String, nullable=True)
    
    # Assessment
    status = Column(String, default=ComplianceStatus.UNKNOWN)
    evidence = Column(JSON, default={})
    assessment_notes = Column(Text, nullable=True)
    
    # Risk and priority
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    priority = Column(Integer, default=5)  # 1-10 scale
    
    # Automation
    is_automated = Column(Boolean, default=False)
    automated_check_config = Column(JSON, nullable=True)
    last_automated_check = Column(DateTime, nullable=True)
    
    # References
    references = Column(JSON, default=[])  # Standards, documentation links
    
    # Company-specific implementation
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Related vulnerabilities
    related_vulnerabilities = Column(JSON, default=[])  # List of vulnerability IDs
    
    # Assignment and tracking
    assigned_to = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    reviewed_by = Column(String, nullable=True)
    review_date = Column(DateTime, nullable=True)
    
    # Audit trail
    last_assessment_date = Column(DateTime, nullable=True)
    next_assessment_date = Column(DateTime, nullable=True)
    assessment_frequency = Column(String, default="annual")  # monthly, quarterly, annual
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ComplianceCheck(id={self.id}, framework='{self.framework}', control='{self.control_id}')>"
    
    @property
    def is_due_for_assessment(self) -> bool:
        """Check if compliance check is due for assessment"""
        if not self.next_assessment_date:
            return True
        from datetime import datetime
        return datetime.utcnow() >= self.next_assessment_date
    
    @property
    def compliance_score(self) -> int:
        """Calculate compliance score (0-100)"""
        if self.status == ComplianceStatus.COMPLIANT:
            return 100
        elif self.status == ComplianceStatus.PARTIALLY_COMPLIANT:
            return 50
        elif self.status == ComplianceStatus.NON_COMPLIANT:
            return 0
        else:
            return 0  # Unknown or not applicable