"""
Vulnerability management endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.services.vulnerability_service import vulnerability_service

router = APIRouter()


@router.get("/", response_model=List[schemas.Vulnerability])
def read_vulnerabilities(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    severity: str = None,
    status: str = None,
    target_id: int = None,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve vulnerabilities for current user's company
    """
    vulnerabilities = vulnerability_service.get_multi(
        db=db,
        company_id=current_user.company_id,
        skip=skip,
        limit=limit,
        severity=severity,
        status=status,
        target_id=target_id
    )
    return vulnerabilities


@router.get("/stats", response_model=dict)
def get_vulnerability_stats(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get vulnerability statistics for the company
    """
    stats = vulnerability_service.get_vulnerability_stats(
        db, company_id=current_user.company_id
    )
    return stats


@router.get("/{vulnerability_id}", response_model=schemas.Vulnerability)
def read_vulnerability(
    vulnerability_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get vulnerability by ID
    """
    vulnerability = vulnerability_service.get(db, id=vulnerability_id)
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    # Check permissions through target company
    if not vulnerability_service.can_user_access_vulnerability(
        db, current_user.id, vulnerability_id
    ):
        raise HTTPException(status_code=403, detail="Not authorized to view this vulnerability")
    
    return vulnerability


@router.put("/{vulnerability_id}/status", response_model=schemas.Vulnerability)
def update_vulnerability_status(
    *,
    db: Session = Depends(deps.get_db),
    vulnerability_id: int,
    status_update: dict,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update vulnerability status
    """
    vulnerability = vulnerability_service.get(db, id=vulnerability_id)
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    # Check permissions
    if not vulnerability_service.can_user_access_vulnerability(
        db, current_user.id, vulnerability_id
    ):
        raise HTTPException(status_code=403, detail="Not authorized to update this vulnerability")
    
    vulnerability = vulnerability_service.update_status(
        db=db,
        vulnerability_id=vulnerability_id,
        status=status_update.get("status"),
        resolved_by=current_user.email
    )
    return vulnerability


@router.put("/{vulnerability_id}/assign", response_model=schemas.Vulnerability)
def assign_vulnerability(
    *,
    db: Session = Depends(deps.get_db),
    vulnerability_id: int,
    assignment: dict,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Assign vulnerability to a user
    """
    from app.models.user import UserRole
    
    # Only analysts and above can assign vulnerabilities
    if current_user.role not in [UserRole.COMPANY_ADMIN, UserRole.ANALYST, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions to assign vulnerabilities")
    
    vulnerability = vulnerability_service.get(db, id=vulnerability_id)
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    # Check permissions
    if not vulnerability_service.can_user_access_vulnerability(
        db, current_user.id, vulnerability_id
    ):
        raise HTTPException(status_code=403, detail="Not authorized to assign this vulnerability")
    
    vulnerability = vulnerability_service.assign_vulnerability(
        db=db,
        vulnerability_id=vulnerability_id,
        assigned_to=assignment.get("assigned_to"),
        due_date=assignment.get("due_date")
    )
    return vulnerability