"""
Scan target management endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.services.scan_target_service import scan_target_service

router = APIRouter()


@router.get("/", response_model=List[schemas.ScanTarget])
def read_scan_targets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve scan targets for current user's company
    """
    targets = scan_target_service.get_multi(
        db, company_id=current_user.company_id, skip=skip, limit=limit
    )
    return targets


@router.post("/", response_model=schemas.ScanTarget)
def create_scan_target(
    *,
    db: Session = Depends(deps.get_db),
    target_in: schemas.ScanTargetCreate,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new scan target
    """
    target = scan_target_service.create(
        db, obj_in=target_in, company_id=current_user.company_id
    )
    return target


@router.get("/{target_id}", response_model=schemas.ScanTarget)
def read_scan_target(
    target_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get scan target by ID
    """
    target = scan_target_service.get(db, id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Scan target not found")
    
    # Check permissions
    if target.company_id != current_user.company_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to view this target")
    
    return target


@router.put("/{target_id}", response_model=schemas.ScanTarget)
def update_scan_target(
    *,
    db: Session = Depends(deps.get_db),
    target_id: int,
    target_in: schemas.ScanTargetUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update scan target
    """
    target = scan_target_service.get(db, id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Scan target not found")
    
    # Check permissions
    if target.company_id != current_user.company_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to update this target")
    
    target = scan_target_service.update(db, db_obj=target, obj_in=target_in)
    return target


@router.delete("/{target_id}", response_model=schemas.ScanTarget)
def delete_scan_target(
    *,
    db: Session = Depends(deps.get_db),
    target_id: int,
    current_user: schemas.User = Depends(deps.get_current_company_admin)
) -> Any:
    """
    Delete scan target (company admin only)
    """
    target = scan_target_service.get(db, id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Scan target not found")
    
    # Check permissions
    if target.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this target")
    
    target = scan_target_service.delete(db, id=target_id)
    return target