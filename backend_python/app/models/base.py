"""
Database models base
"""
from app.core.database import Base

# Import all models to ensure they are registered with SQLAlchemy
from app.models.user import User  # noqa
from app.models.company import Company  # noqa
from app.models.scan_target import ScanTarget  # noqa
from app.models.vulnerability import Vulnerability  # noqa
from app.models.scan_result import ScanResult  # noqa
from app.models.compliance_check import ComplianceCheck  # noqa