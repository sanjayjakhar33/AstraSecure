"""
Scan endpoints for initiating and managing security scans
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import schemas
from app.schemas.scan import NetworkScanRequest, ScanResult
from app.api import deps
from app.services.scan_service import scan_service
from app.services.network_scanner import network_scanner

router = APIRouter()


@router.post("/network", response_model=dict)
def start_network_scan(
    *,
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks,
    scan_request: schemas.NetworkScanRequest,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Start a network security scan
    """
    # Validate that user can scan the target
    if not scan_service.can_user_scan_target(db, current_user.id, scan_request.target_id):
        raise HTTPException(status_code=403, detail="Not authorized to scan this target")
    
    # Create scan record
    scan_result = scan_service.create_scan_result(
        db=db,
        target_id=scan_request.target_id,
        scan_type="network_scan",
        config=scan_request.config,
        initiated_by=current_user.id
    )
    
    # Start background scan
    background_tasks.add_task(
        scan_service.execute_network_scan,
        db=db,
        scan_result_id=scan_result.id,
        scan_options=scan_request.config
    )
    
    return {
        "message": "Network scan started",
        "scan_id": scan_result.id,
        "status": "queued"
    }


@router.get("/profiles", response_model=dict)
def get_scan_profiles(
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get available scan profiles
    """
    return network_scanner.get_scan_profiles()


@router.get("/results", response_model=List[schemas.ScanResult])
def get_scan_results(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    target_id: int = None,
    status: str = None,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get scan results for user's company
    """
    results = scan_service.get_scan_results(
        db=db,
        company_id=current_user.company_id,
        skip=skip,
        limit=limit,
        target_id=target_id,
        status=status
    )
    return results


@router.get("/results/{scan_id}", response_model=schemas.ScanResult)
def get_scan_result(
    scan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get specific scan result
    """
    scan_result = scan_service.get_scan_result(db, scan_id)
    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan result not found")
    
    # Check permissions
    if scan_result.company_id != current_user.company_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to view this scan")
    
    return scan_result


@router.delete("/results/{scan_id}", response_model=dict)
def delete_scan_result(
    scan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_company_admin)
) -> Any:
    """
    Delete scan result (company admin only)
    """
    scan_result = scan_service.get_scan_result(db, scan_id)
    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan result not found")
    
    # Check permissions
    if scan_result.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this scan")
    
    scan_service.delete_scan_result(db, scan_id)
    return {"message": "Scan result deleted successfully"}


@router.post("/results/{scan_id}/cancel", response_model=dict)
def cancel_scan(
    scan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Cancel a running scan
    """
    scan_result = scan_service.get_scan_result(db, scan_id)
    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan result not found")
    
    # Check permissions
    if scan_result.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this scan")
    
    if scan_result.status not in ["queued", "running"]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed scan")
    
    scan_service.cancel_scan(db, scan_id)
    return {"message": "Scan cancelled successfully"}