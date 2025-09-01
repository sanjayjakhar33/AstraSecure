"""
Company management endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.services.company_service import company_service

router = APIRouter()


@router.get("/", response_model=List[schemas.Company])
def read_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Retrieve companies (superuser only)
    """
    companies = company_service.get_multi(db, skip=skip, limit=limit)
    return companies


@router.post("/", response_model=schemas.Company)
def create_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.CompanyCreate,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new company
    """
    company = company_service.create(db, obj_in=company_in)
    return company


@router.get("/me", response_model=schemas.Company)
def read_my_company(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current user's company
    """
    if not current_user.company_id:
        raise HTTPException(status_code=404, detail="User not associated with any company")
    
    company = company_service.get(db, id=current_user.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company


@router.put("/me", response_model=schemas.Company)
def update_my_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.CompanyUpdate,
    current_user: schemas.User = Depends(deps.get_current_company_admin)
) -> Any:
    """
    Update current user's company (company admin only)
    """
    if not current_user.company_id:
        raise HTTPException(status_code=404, detail="User not associated with any company")
    
    company = company_service.get(db, id=current_user.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company = company_service.update(db, db_obj=company, obj_in=company_in)
    return company


@router.get("/me/stats", response_model=schemas.CompanyStats)
def get_company_stats(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get company statistics and metrics
    """
    if not current_user.company_id:
        raise HTTPException(status_code=404, detail="User not associated with any company")
    
    stats = company_service.get_company_stats(db, company_id=current_user.company_id)
    return stats


@router.get("/{company_id}", response_model=schemas.Company)
def read_company(
    company_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Get company by ID (superuser only)
    """
    company = company_service.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/{company_id}", response_model=schemas.Company)
def update_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    company_in: schemas.CompanyUpdate,
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Update company (superuser only)
    """
    company = company_service.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company = company_service.update(db, db_obj=company, obj_in=company_in)
    return company


@router.delete("/{company_id}", response_model=schemas.Company)
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Delete company (superuser only)
    """
    company = company_service.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company = company_service.delete(db, id=company_id)
    return company