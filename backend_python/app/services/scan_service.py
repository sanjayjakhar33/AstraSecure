"""
Scan service layer for managing security scans
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.scan_result import ScanResult, ScanStatus, ScanType
from app.models.scan_target import ScanTarget
from app.models.vulnerability import Vulnerability
from app.services.network_scanner import network_scanner


class ScanService:
    """Scan service for managing security scans"""
    
    def can_user_scan_target(self, db: Session, user_id: int, target_id: int) -> bool:
        """Check if user can scan the target"""
        from app.models.user import User
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
            
        target = db.query(ScanTarget).filter(ScanTarget.id == target_id).first()
        if not target:
            return False
            
        # User can scan if they belong to the same company or are superuser
        return user.is_superuser or user.company_id == target.company_id
    
    def create_scan_result(
        self,
        db: Session,
        *,
        target_id: int,
        scan_type: str,
        config: dict,
        initiated_by: int
    ) -> ScanResult:
        """Create a new scan result record"""
        target = db.query(ScanTarget).filter(ScanTarget.id == target_id).first()
        if not target:
            raise ValueError("Target not found")
        
        db_obj = ScanResult(
            target_id=target_id,
            company_id=target.company_id,
            scan_type=scan_type,
            status=ScanStatus.QUEUED,
            scan_config=config,
            initiated_by=str(initiated_by)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_scan_result(self, db: Session, scan_id: int) -> Optional[ScanResult]:
        """Get scan result by ID"""
        return db.query(ScanResult).filter(ScanResult.id == scan_id).first()
    
    def get_scan_results(
        self,
        db: Session,
        *,
        company_id: int,
        skip: int = 0,
        limit: int = 100,
        target_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[ScanResult]:
        """Get scan results for a company"""
        query = db.query(ScanResult).filter(ScanResult.company_id == company_id)
        
        if target_id:
            query = query.filter(ScanResult.target_id == target_id)
        if status:
            query = query.filter(ScanResult.status == status)
        
        return query.order_by(ScanResult.created_at.desc()).offset(skip).limit(limit).all()
    
    def update_scan_status(self, db: Session, scan_id: int, status: ScanStatus, **kwargs) -> ScanResult:
        """Update scan status and related fields"""
        scan_result = self.get_scan_result(db, scan_id)
        if not scan_result:
            raise ValueError("Scan result not found")
        
        scan_result.status = status
        
        # Update additional fields based on status
        if status == ScanStatus.RUNNING and not scan_result.started_at:
            scan_result.started_at = datetime.utcnow()
        elif status in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED]:
            scan_result.completed_at = datetime.utcnow()
            if scan_result.started_at:
                duration = scan_result.completed_at - scan_result.started_at
                scan_result.duration_seconds = int(duration.total_seconds())
        
        # Update other fields if provided
        for key, value in kwargs.items():
            if hasattr(scan_result, key):
                setattr(scan_result, key, value)
        
        db.add(scan_result)
        db.commit()
        db.refresh(scan_result)
        return scan_result
    
    def delete_scan_result(self, db: Session, scan_id: int) -> None:
        """Delete scan result and associated vulnerabilities"""
        scan_result = self.get_scan_result(db, scan_id)
        if not scan_result:
            raise ValueError("Scan result not found")
        
        # Delete associated vulnerabilities
        db.query(Vulnerability).filter(Vulnerability.scan_result_id == scan_id).delete()
        
        # Delete scan result
        db.delete(scan_result)
        db.commit()
    
    def cancel_scan(self, db: Session, scan_id: int) -> None:
        """Cancel a running scan"""
        self.update_scan_status(db, scan_id, ScanStatus.CANCELLED)
    
    def execute_network_scan(self, db: Session, scan_result_id: int, scan_options: dict) -> None:
        """Execute network scan in background"""
        try:
            # Update status to running
            scan_result = self.update_scan_status(db, scan_result_id, ScanStatus.RUNNING)
            
            # Get target information
            target = db.query(ScanTarget).filter(ScanTarget.id == scan_result.target_id).first()
            if not target:
                raise ValueError("Target not found")
            
            # Perform the scan
            scan_profile = scan_options.get("scan_profile", "basic")
            result = network_scanner.scan_target(
                target=target.target_value,
                scan_type=scan_profile
            )
            
            if result["status"] == "completed":
                # Process scan results
                vulnerabilities = result.get("vulnerabilities", [])
                
                # Save vulnerabilities to database
                for vuln_data in vulnerabilities:
                    vulnerability = Vulnerability(
                        title=vuln_data["title"],
                        description=vuln_data["description"],
                        category=vuln_data["category"],
                        severity=vuln_data["severity"],
                        affected_asset=vuln_data["affected_asset"],
                        scanner_name="nmap",
                        remediation_guidance=vuln_data.get("remediation"),
                        target_id=target.id,
                        scan_result_id=scan_result.id
                    )
                    db.add(vulnerability)
                
                # Update scan result with summary
                vulnerability_counts = {}
                for vuln in vulnerabilities:
                    severity = vuln["severity"]
                    vulnerability_counts[f"{severity}_count"] = vulnerability_counts.get(f"{severity}_count", 0) + 1
                
                self.update_scan_status(
                    db, scan_result_id, ScanStatus.COMPLETED,
                    total_vulnerabilities=len(vulnerabilities),
                    critical_count=vulnerability_counts.get("critical_count", 0),
                    high_count=vulnerability_counts.get("high_count", 0),
                    medium_count=vulnerability_counts.get("medium_count", 0),
                    low_count=vulnerability_counts.get("low_count", 0),
                    info_count=vulnerability_counts.get("info_count", 0),
                    raw_output=result.get("raw_output"),
                    parsed_data=result.get("parsed_data")
                )
                
                # Update target's last scan time and risk score
                target.last_scan_at = datetime.utcnow()
                target.risk_score = min(100, len(vulnerabilities) * 10)  # Simple risk calculation
                db.add(target)
                
                db.commit()
                
            else:
                # Scan failed
                error_message = result.get("error", "Unknown scan error")
                self.update_scan_status(
                    db, scan_result_id, ScanStatus.FAILED,
                    error_message=error_message
                )
                
        except Exception as e:
            # Handle any unexpected errors
            self.update_scan_status(
                db, scan_result_id, ScanStatus.FAILED,
                error_message=str(e)
            )


# Create service instance
scan_service = ScanService()