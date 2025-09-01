"""
Company service layer
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.company import Company
from app.models.scan_target import ScanTarget
from app.models.scan_result import ScanResult
from app.models.vulnerability import Vulnerability
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyStats


class CompanyService:
    """Company service for CRUD operations"""
    
    def get(self, db: Session, id: int) -> Optional[Company]:
        """Get company by ID"""
        return db.query(Company).filter(Company.id == id).first()
    
    def get_by_domain(self, db: Session, domain: str) -> Optional[Company]:
        """Get company by domain"""
        return db.query(Company).filter(Company.domain == domain).first()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Company]:
        """Get multiple companies with pagination"""
        return db.query(Company).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CompanyCreate) -> Company:
        """Create new company"""
        db_obj = Company(
            name=obj_in.name,
            domain=obj_in.domain,
            address=obj_in.address,
            phone=obj_in.phone,
            website=obj_in.website,
            industry=obj_in.industry,
            size=obj_in.size,
            billing_email=obj_in.billing_email,
            subscription_tier=obj_in.subscription_tier,
            compliance_frameworks=obj_in.compliance_frameworks
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: Company, obj_in: CompanyUpdate) -> Company:
        """Update company"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> Company:
        """Delete company"""
        obj = db.query(Company).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def get_company_stats(self, db: Session, company_id: int) -> CompanyStats:
        """Get company statistics"""
        # Get scan target count
        scan_target_count = db.query(ScanTarget).filter(
            ScanTarget.company_id == company_id,
            ScanTarget.is_active == True
        ).count()
        
        # Get vulnerability counts
        active_vulnerabilities = db.query(Vulnerability).join(ScanTarget).filter(
            ScanTarget.company_id == company_id,
            Vulnerability.status == "open"
        ).count()
        
        resolved_vulnerabilities = db.query(Vulnerability).join(ScanTarget).filter(
            ScanTarget.company_id == company_id,
            Vulnerability.status == "resolved"
        ).count()
        
        # Get last scan date
        last_scan = db.query(ScanResult).filter(
            ScanResult.company_id == company_id
        ).order_by(ScanResult.created_at.desc()).first()
        
        last_scan_date = last_scan.created_at if last_scan else None
        
        # Calculate average risk score
        avg_risk_score = db.query(func.avg(ScanTarget.risk_score)).filter(
            ScanTarget.company_id == company_id,
            ScanTarget.is_active == True
        ).scalar() or 0
        
        # Get user count
        user_count = db.query(User).filter(
            User.company_id == company_id,
            User.is_active == True
        ).count()
        
        # Calculate compliance score (simplified)
        compliance_score = max(0, 100 - (active_vulnerabilities * 2))
        
        return CompanyStats(
            total_scan_targets=scan_target_count,
            active_vulnerabilities=active_vulnerabilities,
            resolved_vulnerabilities=resolved_vulnerabilities,
            compliance_score=min(100, compliance_score),
            risk_score=int(avg_risk_score),
            last_scan_date=last_scan_date,
            scan_frequency="weekly",  # Default, could be configurable
            user_count=user_count
        )


# Create service instance
company_service = CompanyService()