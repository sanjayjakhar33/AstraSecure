"""
Scan target service layer
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.scan_target import ScanTarget
from app.schemas.scan import ScanTargetCreate, ScanTargetUpdate


class ScanTargetService:
    """Scan target service for CRUD operations"""
    
    def get(self, db: Session, id: int) -> Optional[ScanTarget]:
        """Get scan target by ID"""
        return db.query(ScanTarget).filter(ScanTarget.id == id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        company_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ScanTarget]:
        """Get multiple scan targets for a company"""
        return db.query(ScanTarget).filter(
            ScanTarget.company_id == company_id
        ).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: ScanTargetCreate, company_id: int) -> ScanTarget:
        """Create new scan target"""
        db_obj = ScanTarget(
            name=obj_in.name,
            description=obj_in.description,
            target_type=obj_in.target_type,
            target_value=obj_in.target_value,
            cloud_provider=obj_in.cloud_provider,
            cloud_region=obj_in.cloud_region,
            scan_config=obj_in.scan_config,
            scan_frequency=obj_in.scan_frequency,
            criticality=obj_in.criticality,
            tags=obj_in.tags,
            company_id=company_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: ScanTarget, obj_in: ScanTargetUpdate) -> ScanTarget:
        """Update scan target"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> ScanTarget:
        """Delete scan target"""
        obj = db.query(ScanTarget).get(id)
        db.delete(obj)
        db.commit()
        return obj


# Create service instance
scan_target_service = ScanTargetService()